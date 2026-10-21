# sponge-tag — specification

Source: `00-goals.md`. Analyses in `analyses/` (cited as A0x).

## Block diagram
```
 CR2032 ──Q1 (rev. pol.)── VDD ──┬── nRF54L15 (DC/DC, LFXO, HFXO) ── matching ── chip antenna
                                 ├── SHT40 (I2C, P1.11/P1.12)
                                 ├── LED (P1.10)      button + TVS (P1.13)
                                 └── TC2030 SWD / RTT, UART test pads
```

## Requirements
| ID | Requirement | Verification | Pass criterion |
|---|---|---|---|
| REQ-001 | Measure temperature | bench test vs reference thermometer | ±0.5 °C at 20–30 °C |
| REQ-002 | Measure humidity | bench test vs reference hygrometer | ±3 %RH at 30–70 %RH |
| REQ-003 | Measurement every 60 s | firmware log timestamps | 60 ± 1 s |
| REQ-004 | Button short press → fast adv (100 ms) for 30 s | bench test | interval 100 ms ± 10%, ends after 30 ± 1 s |
| REQ-005 | Button long press 5 s → settings reset | bench test | log + LED |
| REQ-006 | LED blinks once on button press | inspection | — |
| REQ-007 | Battery voltage in adv data, mV | compare with DMM | ±50 mV |
| REQ-008 | Low battery: VDD < 2.2 V → LED blinks 3× every 60 s | PSU sweep | triggers at 2.2 ± 0.05 V |
| REQ-009 | Runs from 1.8 V to 3.3 V supply | PSU sweep | adv + sensor OK across range |
| REQ-010 | Battery life ≥ 1 year (CR2032, 2 s adv) | analysis A01 + REQ-011 | — |
| REQ-011 | Average current, 2 s adv, 1/min sensor | PPK2 or DMM averaging, 60 s | ≤ 15 µA |
| REQ-012 | Sleep current between events | PPK2 | ≤ 5 µA |
| REQ-013 | BLE range to a phone indoors | nRF Connect app | RSSI > −90 dBm at 10 m |
| REQ-014 | Reversed coin cell causes no damage | bench test with PSU −3 V, 10 mA limit | no current > 10 µA, board works after |
| REQ-015 | Board ≤ 30 × 30 mm, 2× M2 holes | inspection of layout | — |
| REQ-016 | Programmable via Tag-Connect TC2030-NL | bench | J-Link connects |
| REQ-017 | BOM < $6 at qty 100 | BOM cost roll-up | — |
| REQ-018 | Sensor away from heat sources | layout review | ≥ 8 mm from MCU and battery edge, slots optional |

## Key design decisions
| Decision | Why | Ref |
|---|---|---|
| nRF54L15-QFAA (QFN48) | BLE 5, low sleep current, NCS support, QFN easier than WLCSP | A03 |
| VDD straight from the cell, internal DC/DC | 1.7–3.6 V range covers the CR2032; no regulator quiescent current | A02 |
| P-MOSFET reverse protection | ~0 V drop vs 0.25 V Schottky | A02 |
| Adv interval 2 s | 1.87 y life, 87% margin | A01 |
| SHT40 over I2C on P1 | domain rules; KiCad symbol + footprint exist | A04 |
| Chip antenna + spare pi network | small board; allows retuning | A03 |

## Open questions
See STATUS.md (OQ-1 to OQ-5).
