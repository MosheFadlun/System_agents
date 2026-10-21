# A04: I/O, pin map, I2C, LED and button

## nRF54L15 power domains and pins
On nRF54L15 the serial peripherals are tied to GPIO ports: P1 serves the PERI-domain instances
(TWIM/SPIM/UARTE 20–22, SAADC), P2 the fast MCU-domain instances, and P0 the low-power domain.
Using a peripheral on another port's pins is restricted (check the datasheet's "Pin assignments"
and GPIO chapters). The nRF54L15 DK uses P1 for UART20 and for buttons/LEDs, so we keep
everything on **P1** where possible.

## Pin map (frozen in the schematic, used by the firmware)
| Net | nRF pin | QFN48 pin | Peripheral | Notes |
|---|---|---|---|---|
| XL1 / XL2 | P1.00 / P1.01 | 1 / 2 | LFXO | 32.768 kHz |
| UART_TX | P1.04 | 5 | UARTE20 TXD | test pad, log fallback |
| UART_RX | P1.05 | 6 | UARTE20 RXD | test pad |
| LED | P1.10 | 38 | GPIO | active high |
| I2C_SDA | P1.11 | 39 | TWIM21 | 10 k pull-up |
| I2C_SCL | P1.12 | 40 | TWIM21 | 10 k pull-up |
| BUTTON | P1.13 | 41 | GPIO | active low, internal pull-up |
| SWO | P2.07 | 18 | TRACE | to TC2030 pin 6 |
| SWDIO / SWDCLK / nRESET | — | 25 / 26 / 30 | debug | TC2030 |

## I2C pull-ups
Bus capacitance ≈ 20 pF (one device, short traces). Fast mode (400 kHz) needs t_r ≤ 300 ns.
t_r = 0.8473 × R × C = 0.8473 × 10 kΩ × 20 pF = 170 ns. OK. Static current only while a
line is low (300 µA at 3 V, a few µs per read). **10 kΩ.**

## LED
Red LED (Vf ≈ 1.9 V @ 2 mA, Würth 150060RS75000). At 3.0 V: (3.0 − 1.9) / 470 Ω = 2.3 mA.
At 2.2 V: 0.6 mA, dim but visible. **470 Ω.** The GPIO drives it directly (standard drive
handles the current).

## Button / ESD
The button is user-touched: add a **PESD5V0S1BL** TVS (SOD-882) to GND and a 100 Ω series
resistor between the button node and P1.13. The internal pull-up (~13 kΩ) is enabled only while
the button is pressed, or uses SENSE wake-up; no static current when released.

## Battery voltage
Measured with the SAADC on the internal VDD input: no divider, no leakage.
**OQ-3:** confirm the nRF54L15 SAADC can sample VDD internally. If not, add a switched divider.
