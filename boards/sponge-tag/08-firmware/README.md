# sponge-tag firmware

nRF Connect SDK v2.9.3, Zephyr. Developed on the **nRF54L15 DK** with the sponge-tag pin map in
`app/boards/nrf54l15dk_nrf54l15_cpuapp.overlay`, with an SHT40 breakout wired to the DK header.
A custom `sponge_tag` board definition follows once the schematic is frozen.

## Build / flash (from the Hardware folder, Git Bash)
```
tools/fw/ncs.sh west build -p always -b nrf54l15dk/nrf54l15/cpuapp $PWD/boards/sponge-tag/08-firmware/app -d $PWD/boards/sponge-tag/08-firmware/build
tools/fw/ncs.sh west flash -d $PWD/boards/sponge-tag/08-firmware/build
```
Logs come out on UARTE20 (P1.04 TX), the DK's VCOM. On sponge-tag that is test pad TP UART_TX.

**Status:** not compiled yet. The NCS install at `C:/ncs/v2.9.3` is missing its west modules
(`modules/hal/nordic`, ...); run `tools/fw/ncs.sh west update` once.

## Pin table (must match 03-schematic net names)
| Net | nRF pin | Devicetree |
|---|---|---|
| LED_GPIO | P1.10 | `led1` → alias `status-led` |
| BTN_GPIO | P1.13 | `button0` → alias `user-button` |
| I2C_SDA / I2C_SCL | P1.11 / P1.12 | `i2c21` → `sht40@44` |
| UART_TX / UART_RX | P1.04 / P1.05 | `uart20` (console) |

## Advertising payload
Manufacturer data, company ID 0xFFFF (testing only; get a real ID before shipping):
`FF FF | 01 | temp int16 0.01 °C | RH uint16 0.01 % | batt uint16 mV`.

## TODO
- Battery mV via SAADC internal VDD (OQ-3), low-battery LED (REQ-008), long press reset (REQ-005).
- Custom board definition `boards/<vendor>/sponge_tag/`, with LFXO enabled and UART20 without RTS/CTS.
- Power optimisation: disable UART console in the product build (`prj_release.conf`), measure REQ-011/012.
