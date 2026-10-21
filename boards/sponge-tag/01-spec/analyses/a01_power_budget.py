"""A01 power budget / battery life for sponge-tag. Run: python a01_power_budget.py

Every input is an ASSUMPTION with its source listed in A01-power-budget.md. Change the numbers
there and here together.
"""

HOURS_PER_YEAR = 8766

# Battery: CR2032 220 mAh nominal; derate 20% for pulse load, self-discharge, and the 2.0 V cutoff.
cap_mAh = 220 * 0.8

# nRF54L15 System ON idle with GRTC running and RAM retained (assumption, verify in datasheet)
i_sleep_uA = 3.0

# One BLE legacy advertising event, 3 channels, 0 dBm, ~31 B payload, DC/DC on (assumption)
q_adv_uC = 15.0

# SHT40 high-repeatability measurement: 320 uA typ for 8.3 ms max (SHT4x datasheet, assumption)
q_sht_uC = 320e-6 * 8.3e-3 * 1e6  # uC
i_sht_idle_uA = 0.08

# MCU awake for the sensor read + I2C (~2 ms at ~2.5 mA, assumption)
q_mcu_read_uC = 2.5e-3 * 2e-3 * 1e6

# SAADC battery read once per 10 min, negligible but included
q_adc_uC = 1.0

# Button pull-up: internal, no static current when released. LED: user-triggered, ignored.


def avg_current_uA(adv_interval_s, meas_interval_s=60, adc_interval_s=600):
    return (
        i_sleep_uA
        + i_sht_idle_uA
        + q_adv_uC / adv_interval_s
        + (q_sht_uC + q_mcu_read_uC) / meas_interval_s
        + q_adc_uC / adc_interval_s
    )


if __name__ == "__main__":
    print(f"usable capacity: {cap_mAh:.0f} mAh")
    print(f"{'adv interval':>12} | {'avg uA':>7} | {'life (years)':>12}")
    for adv in (0.5, 1.0, 2.0, 3.0, 5.0):
        i = avg_current_uA(adv)
        years = cap_mAh * 1000 / i / HOURS_PER_YEAR
        print(f"{adv:>11.1f}s | {i:7.2f} | {years:12.2f}")
