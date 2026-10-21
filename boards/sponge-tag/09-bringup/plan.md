# sponge-tag — bring-up plan

Instruments: `psu` (CH1 → battery holder contacts via clip leads), `dmm`, `scope`, J-Link + TC2030-NL.
Every state-changing command is logged to `log.md` (`psu.py --log boards/sponge-tag/09-bringup/log.md`).

| # | Step | Setup | Expected (source) | Pass / stop limit |
|---|---|---|---|---|
| 1 | Visual: orientation of U1 pin 1, Q1, D1, BT1; no bridges on QFN | microscope, human | — | human OK |
| 2 | Resistance VDD–GND and VBAT–GND, unpowered | DMM ohms | > 100 kΩ (MLCC only) | < 1 kΩ → stop, short |
| 3 | First power: PSU 3.0 V, **limit 20 mA**, output OFF until the human confirms | `psu.py set --v 3.0 --i 0.02` → human OK → `psu.py on` → `psu.py watch --seconds 5 --i-max 0.015` | blank chip: < 5 mA | > 15 mA → auto OFF, stop |
| 4 | Rails | DMM on TP VDD, scope on DCC | VDD ≈ 3.0 V (Q1 drop < 10 mV, A02) | VDD < 2.95 V → stop |
| 5 | SWD connect | `nrfutil device device-info` / J-Link | nRF54L15 detected | no ID → check SWD/NRESET |
| 6 | Flash bring-up firmware | `tools/fw/ncs.sh west flash` | log "sponge-tag starting" on UART_TX | — |
| 7 | HFXO / LFXO running | scope on XC1 (10x probe, caution: loading) or firmware clock status | 32 MHz / 32.768 kHz | — |
| 8 | SHT40 | log lines every 60 s | plausible T/RH vs a reference (REQ-001/002) | ±0.5 °C, ±3 %RH |
| 9 | LED + button | press button | LED on, adv 100 ms for 30 s (REQ-004/006) | — |
| 10 | BLE | nRF Connect app at 1 m and 10 m | name "sponge-tag", correct data (REQ-013) | RSSI > −90 dBm @ 10 m |
| 11 | Sleep / average current | PPK2 (or DMM avg), release build, 2 s adv | avg ≤ 15 µA (REQ-011), sleep ≤ 5 µA (REQ-012), A01 | above → investigate before acceptance |
| 12 | Supply sweep | PSU 3.3 → 1.8 V in 0.1 V steps, limit 20 mA | works to 1.8 V (REQ-009) | brown-out above 1.9 V → finding |
| 13 | Reverse polarity | PSU −3.0 V, **limit 10 mA**, human confirms | < 10 µA, then works at +3 V (REQ-014) | > 10 µA → OFF, finding |

Results go in `results.md` (REQ | measured | limit | pass/fail | evidence).
