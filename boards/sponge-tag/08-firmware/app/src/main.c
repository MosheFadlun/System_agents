/*
 * sponge-tag firmware: SHT40 every 60 s, broadcast in BLE advertising (no connections).
 *
 * REQ-003 measure every 60 s          REQ-004 button -> 100 ms adv for 30 s
 * REQ-006 LED blink on button press   A01 default adv interval 2 s
 *
 * Advertising payload (manufacturer data, little endian):
 *   [0..1] company ID 0xFFFF (test/unassigned)  [2] format version = 1
 *   [3..4] temperature, 0.01 degC (int16)        [5..6] humidity, 0.01 %RH (uint16)
 *   [7..8] battery mV (uint16, 0 until OQ-3 is resolved)
 */
#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/sensor.h>
#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/sys/byteorder.h>
#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(sponge_tag, LOG_LEVEL_INF);

#define MEAS_INTERVAL      K_SECONDS(60)
#define ADV_SLOW_UNITS     3200 /* 2 s in 0.625 ms units (A01) */
#define ADV_FAST_UNITS     160  /* 100 ms (REQ-004) */
#define FAST_ADV_DURATION  K_SECONDS(30)

static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(DT_ALIAS(status_led), gpios);
static const struct gpio_dt_spec button = GPIO_DT_SPEC_GET(DT_ALIAS(user_button), gpios);
static const struct device *const sht = DEVICE_DT_GET_ONE(sensirion_sht4x);

static uint8_t mfg_data[9] = {0xFF, 0xFF, 0x01};
static const struct bt_data ad[] = {
	BT_DATA_BYTES(BT_DATA_FLAGS, BT_LE_AD_NO_BREDR),
	BT_DATA(BT_DATA_MANUFACTURER_DATA, mfg_data, sizeof(mfg_data)),
};
static const struct bt_data sd[] = {
	BT_DATA(BT_DATA_NAME_COMPLETE, CONFIG_BT_DEVICE_NAME, sizeof(CONFIG_BT_DEVICE_NAME) - 1),
};

static struct gpio_callback button_cb;
static struct k_work_delayable fast_adv_end;
static struct k_work fast_adv_start;

static int adv_start(uint16_t interval)
{
	const struct bt_le_adv_param param =
		BT_LE_ADV_PARAM_INIT(BT_LE_ADV_OPT_USE_IDENTITY, interval, interval, NULL);

	bt_le_adv_stop();
	int err = bt_le_adv_start(&param, ad, ARRAY_SIZE(ad), sd, ARRAY_SIZE(sd));

	if (err) {
		LOG_ERR("adv start failed (%d)", err);
	} else {
		LOG_INF("advertising every %u ms", interval * 5 / 8);
	}
	return err;
}

static void fast_adv_start_fn(struct k_work *work)
{
	adv_start(ADV_FAST_UNITS);
	k_work_reschedule(&fast_adv_end, FAST_ADV_DURATION);
}

static void fast_adv_end_fn(struct k_work *work)
{
	adv_start(ADV_SLOW_UNITS);
}

static void button_pressed(const struct device *dev, struct gpio_callback *cb, uint32_t pins)
{
	gpio_pin_toggle_dt(&led); /* REQ-006 blink: on now, off at the next measurement tick */
	k_work_submit(&fast_adv_start);
}

static int measure(void)
{
	struct sensor_value t, h;
	int err = sensor_sample_fetch(sht);

	if (err) {
		LOG_ERR("SHT40 fetch failed (%d)", err);
		return err;
	}
	sensor_channel_get(sht, SENSOR_CHAN_AMBIENT_TEMP, &t);
	sensor_channel_get(sht, SENSOR_CHAN_HUMIDITY, &h);

	int16_t t_centi = (int16_t)(t.val1 * 100 + t.val2 / 10000);
	uint16_t h_centi = (uint16_t)(h.val1 * 100 + h.val2 / 10000);

	sys_put_le16((uint16_t)t_centi, &mfg_data[3]);
	sys_put_le16(h_centi, &mfg_data[5]);
	sys_put_le16(0, &mfg_data[7]); /* battery mV: TODO after OQ-3 (SAADC VDD input) */

	LOG_INF("T=%d.%02d C  RH=%u.%02u %%", t_centi / 100, abs(t_centi % 100),
		h_centi / 100, h_centi % 100);
	return bt_le_adv_update_data(ad, ARRAY_SIZE(ad), sd, ARRAY_SIZE(sd));
}

static int init_io(void)
{
	if (!gpio_is_ready_dt(&led) || !gpio_is_ready_dt(&button)) {
		return -ENODEV;
	}
	gpio_pin_configure_dt(&led, GPIO_OUTPUT_INACTIVE);
	gpio_pin_configure_dt(&button, GPIO_INPUT);
	gpio_pin_interrupt_configure_dt(&button, GPIO_INT_EDGE_TO_ACTIVE);
	gpio_init_callback(&button_cb, button_pressed, BIT(button.pin));
	return gpio_add_callback(button.port, &button_cb);
}

int main(void)
{
	LOG_INF("sponge-tag starting");

	if (init_io()) {
		LOG_ERR("GPIO init failed");
		return 0;
	}
	if (!device_is_ready(sht)) {
		LOG_ERR("SHT40 not ready: check I2C wiring / address 0x44");
	}

	k_work_init(&fast_adv_start, fast_adv_start_fn);
	k_work_init_delayable(&fast_adv_end, fast_adv_end_fn);

	int err = bt_enable(NULL);

	if (err) {
		LOG_ERR("bt_enable failed (%d)", err);
		return 0;
	}
	adv_start(ADV_SLOW_UNITS);

	while (1) {
		if (device_is_ready(sht)) {
			measure();
		}
		gpio_pin_set_dt(&led, 0);
		k_sleep(MEAS_INTERVAL);
	}
	return 0;
}
