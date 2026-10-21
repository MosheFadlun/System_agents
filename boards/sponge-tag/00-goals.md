# sponge-tag — goals (human-owned)

> EXAMPLE board, created to show the workflow end to end. The numbers are realistic but were
> chosen for the demo, not taken from a real product.

## Purpose
A small coin-cell tag that measures room temperature and humidity and broadcasts them over
Bluetooth LE, so a phone or gateway can read them without pairing.

## Must-have functions
- Measure temperature (±0.5 °C) and relative humidity (±3 %RH) once per minute.
- Broadcast the latest reading in BLE advertising packets.
- One button: short press = advertise fast for 30 s (for pairing/finding); long press 5 s = reset settings.
- One LED: blink once on button press, 3x on low battery.
- Report battery voltage in the advertising data.

## Interfaces & connectors
- No user connectors. Programming via a Tag-Connect TC2030-NL pad (no header).

## Power
- One CR2032 coin cell (3.0 V nominal, usable down to 2.0 V).
- Battery life: **≥ 1 year** at room temperature with default settings.

## Wireless / RF
- BLE 5, chip antenna, range ≥ 10 m indoors to a phone.

## Sensors & peripherals
- Sensirion SHT40 (or equivalent) over I2C.

## Mechanical
- Board ≤ 30 × 30 mm, 2 mounting holes M2. Coin cell on the back side.
- The sensor must sit at a board edge, away from the battery and the MCU, for airflow and to avoid self-heating.

## Environment
- Indoor, 0–50 °C, non-condensing. Handheld: ESD on the button and the exposed board.

## Production
- 10 prototypes, assembled by JLCPCB (PCBA) where possible. Target BOM < $6 at qty 100.

## What "done" looks like on the bench
- Flashes and logs over SWD/RTT.
- The sleep current measured on the bench supports the 1-year life.
- A phone (nRF Connect app) sees the advertisements at 10 m with correct temperature/humidity values.

## Out of scope
- Phone app, gateway, OTA updates (a later revision), NFC.
