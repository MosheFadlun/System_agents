# A02: Supply path, coin-cell droop, reverse polarity

**Question:** Does the nRF54L15 stay above its minimum VDD during radio peaks at the end of
battery life, and how do we protect against a reversed cell?

## Supply range
- nRF54L15 VDD: 1.7–3.6 V (datasheet, recommended operating conditions). SHT40: 1.08–3.6 V.
  A CR2032 (3.0 V fresh, 2.0 V at end) can feed VDD directly. **No regulator needed**; the
  nRF54L15 internal DC/DC does the conversion.

## Droop during radio TX
- Peak current during TX at 0 dBm, DC/DC on: ~6 mA at 3 V (estimate; the DC/DC current grows as VBAT falls).
  At 2.2 V: ≈ 6 mA × 3.0/2.2 ≈ 8 mA.
- CR2032 internal resistance: ~10–20 Ω fresh, rising to ~50 Ω near end of life and in the cold.
- Worst case drop: 8 mA × 50 Ω = 0.40 V → 2.2 V open-circuit falls to **1.80 V**, still above 1.7 V.
- A bulk cap helps only on fast edges: τ = 50 Ω × ~15 µF effective = 0.75 ms, shorter than the
  ~3 ms advertising event. **Decision:** 10 µF 0603 bulk at the battery plus Nordic's decoupling.
  A large (100 µF+) cap is not worth its leakage and size.
- **Firmware:** declare "low battery" at VDD < 2.2 V under load (REQ-008).

## Reverse polarity
- A reversed CR2032 in the Keystone 3034 holder is possible. −3 V on VDD exceeds the abs max
  (−0.3 V) and would damage the nRF54L15 and the SHT40.
- Options: series Schottky (0.2–0.3 V drop, wastes 10% of the battery range: rejected),
  or a P-MOSFET as an ideal diode (only mΩ drop when correctly inserted).
- **Decision:** P-MOSFET **DMG2305UX** (SOT-23, Vgs(th) −0.9 V max): drain → battery +,
  source → VDD, gate → GND. At VBAT = 2.0 V, Vgs = −2.0 V, and the datasheet gives RDS(on) at
  Vgs −1.8 V of about 0.1 Ω (verify), so the drop is under 1 mV.
- Leakage when off: negligible.

## Result
Net VBAT (battery side) → Q1 → net **VDD** (everything else). 10 µF bulk on VDD.
