# A01: Power budget and battery life

**Question:** Can a CR2032 run the tag for ≥ 1 year (REQ-010), and what advertising interval does that allow?

## Assumptions
| Input | Value | Source | Confidence |
|---|---|---|---|
| CR2032 capacity | 220 mAh nominal, 176 mAh usable (−20%) | typical CR2032 datasheets; derating for pulse load and 2.0 V cutoff | medium |
| nRF54L15 System ON idle, GRTC + RAM retention | 3.0 µA | nRF54L15 datasheet, current consumption chapter | **verify on the bench (REQ-011)** |
| BLE adv event, 3 ch, 0 dBm, DC/DC on | 15 µC/event | typical for Nordic BLE SoCs; Nordic Online Power Profiler | **verify with PPK2 (TEST-04)** |
| SHT40 measurement | 320 µA × 8.3 ms | SHT4x datasheet, high-repeatability mode | medium |
| SHT40 idle | 0.08 µA | SHT4x datasheet | medium |
| MCU awake for the I2C read | 2.5 mA × 2 ms | estimate | low |

## Calculation
`a01_power_budget.py` (run 2026-10-18):

| Adv interval | Avg current | Life |
|---|---|---|
| 0.5 s | 33.2 µA | 0.60 y |
| 1.0 s | 18.2 µA | 1.10 y |
| **2.0 s** | **10.7 µA** | **1.87 y** |
| 3.0 s | 8.2 µA | 2.45 y |
| 5.0 s | 6.2 µA | 3.23 y |

Advertising dominates: at 2 s it is 7.5 µA of the 10.7 µA. Sleep is the second contributor (3 µA).
The sensor at once per minute adds < 0.1 µA.

## Result / decision
- Default advertising interval **2.0 s**. That gives 1.87 years, an 87% margin over the 1-year
  goal, which covers the unverified adv-event charge. At 1 s the margin would be only 10%.
- Fast advertising (100 ms) only for 30 s after a button press (REQ-004). Its cost is negligible
  unless the button is pressed more than ~10 times per day.
- Firmware must keep the HFXO off between events and use the LFXO (lower sleep current than LFRC).
- **Bench check:** average current at 2 s must be ≤ 15 µA (REQ-011). Above that, the 1-year
  target is at risk.
