# sponge-tag — part selection notes

> In this example the distributor stock / price / lifecycle columns are **NOT CHECKED**. The real
> `hw-parts` agent fills them from DigiKey/Mouser/LCSC searches, saves a dated snapshot in
> `stock-<date>.md`, and downloads every datasheet to `datasheets/`. The parts gate cannot be
> approved while any column says NOT CHECKED or any MPN says TBD.

| Part | Why this one | Analysis |
|---|---|---|
| NRF54L15-QFAA | REQ set + nRF54 default; QFN48 is hand-reworkable. NRF54L10 is pin compatible if the 1.5 MB flash isn't needed (cheaper) | A03 |
| SHT40-AD1B | ±0.2 °C / ±1.8 %RH beats REQ-001/002 by a wide margin; 0.08 µA idle; KiCad symbol + footprint exist | A01, A04 |
| DMG2305UX | Low Vgs(th) so it is fully on at 2.0 V; SOT-23 is cheap and everywhere | A02 |
| 2450AT18A100E | Common 2.4 GHz chip antenna with a KiCad footprint; needs a ground-clearance area → board edge | A03 |
| Murata RF parts | Exact parts from Nordic's QFN48 reference BOM. Do not substitute: the match depends on their parasitics | A03 |
| 0201 decoupling | As in the Nordic reference; JLC can place 0201. The SHT40 and other non-critical passives are 0402 for easier rework | A03 |
| PESD5V0S1BL | Low capacitance, 5 V working voltage above the 3.3 V max VDD | A04 |

## Still to select (OQ-4)
- X1 32.768 kHz 2012 and X2 32 MHz 2016: CL and ESR must sit inside the nRF54L15's LFXO/HFXO
  limits and the internal load-cap range. Prefer the parts on the nRF54L15 DK BOM.
- L1 4.7 µH 0603: Isat ≥ 100 mA, DCR as low as possible; prefer the DK's part.
- FB1: the DK's part.
