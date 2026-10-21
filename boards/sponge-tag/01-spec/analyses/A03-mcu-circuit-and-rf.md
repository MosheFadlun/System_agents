# A03: nRF54L15 support circuit, clocks and RF

**Question:** What surrounds the nRF54L15 (DC/DC, decoupling, crystals, RF matching, antenna)?

## Source
Nordic nRF54L15 datasheet, "Circuit configuration 1 for QFN48 (QFAA)": DC/DC supplied by
battery, NFC not used. Reference BOM values as published by Nordic:

| Ref (Nordic) | Value / part | Footprint |
|---|---|---|
| C1, C2 | 2.2 µF | 0201 |
| C4, C7, C8 | 100 nF | 0201 |
| C10 | 100 nF (optional) | 0201 |
| C12 | 10 nF | 0201 |
| C6 | Murata GJM0335C1E1R5WB01 (1.5 pF) | 0201 |
| C9 | Murata GJM0335C1E2R0WB01 (2.0 pF) | 0201 |
| L1 | 4.7 µH (DC/DC) | 0603 |
| L2 | Murata LQP03HQ2N7B02 (2.7 nH) | 0201 |
| L3, L4 | Murata LQP03HQ3N5B02 (3.5 nH) | 0201 |
| FB1 | ferrite bead | 0201 |
| X1 | 32.768 kHz | 2012 |
| X2 | 32 MHz | 2016 |

**Limitation:** the published text gives the values but not the full net-by-net topology (that is
in the schematic figure). The schematic stage implements the most likely topology, and review item
**OQ-1** requires a check against Nordic's reference schematic / DK design files before freezing.

## Decisions
- **Package:** QFN48 (nRF54L15-QFAA). 31 GPIOs is plenty, and it is easier to assemble and inspect than WLCSP.
- **DC/DC on** (L1 4.7 µH), needed for the A01 budget.
- **Crystals:** the nRF54L15 has on-chip tunable load capacitors for both HFXO and LFXO, so no
  external load caps (the Nordic BOM has none). Crystal CL and ESR must be in the datasheet's
  allowed ranges; that is checked at the parts stage.
- **LFXO** on P1.00/P1.01: needed for the 3 µA sleep with accurate BLE timing (A01).
- **NFC unused:** P1.02/P1.03 left unconnected, NFC pins configured as GPIO in firmware.
- **Antenna:** Johanson **2450AT18A100E** chip antenna (KiCad footprint exists), with an
  antenna-side pi pad (0 Ω series, 2× DNP shunts) so the antenna can be retuned on the real board.
  The Nordic matching network stays between ANT and the 50 Ω feed.
- **Layout constraint for stage 5:** copy the Nordic QFN48 RF layout, 50 Ω CPWG, antenna at the board edge with a copper keepout per the Johanson datasheet.

## Exposed pad
The nRF54L15 QFN48 is 6×6 mm, 0.4 mm pitch, exposed pad = pin 49 (VSS). Using KiCad
`QFN-48-1EP_6x6mm_P0.4mm_EP4.6x4.6mm` provisionally. **OQ-2:** check the EP size against the
datasheet's package drawing before layout.
