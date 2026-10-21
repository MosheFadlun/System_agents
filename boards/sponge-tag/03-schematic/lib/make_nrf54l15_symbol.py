"""Generate nRF54L15.kicad_sym (QFN48, nRF54L15-QFAA) from the datasheet pin table.

Pin table: nRF54L15 datasheet, "QFN48 (QFAA) package pin assignments". Shared with sponge_tag.py.
Run: python make_nrf54l15_symbol.py
"""
from pathlib import Path

# (number, name, kicad electrical type, side)
PINS = [
    # left: supply, decoupling, ground
    (10, "VDD", "power_in", "L"), (22, "VDD", "power_in", "L"), (36, "VDD", "power_in", "L"),
    (47, "VDD", "power_in", "L"), (48, "VDD", "power_in", "L"),
    (46, "DCC", "power_out", "L"), (45, "DECD", "passive", "L"), (43, "DECA", "passive", "L"),
    (33, "DECRF", "passive", "L"),
    (34, "XC1", "passive", "L"), (35, "XC2", "passive", "L"),
    (31, "ANT", "passive", "L"),
    (25, "SWDIO", "bidirectional", "L"), (26, "SWDCLK", "input", "L"), (30, "nRESET", "input", "L"),
    (44, "VSS", "power_in", "L"), (32, "VSS_PA", "power_in", "L"), (49, "VSS_EP", "power_in", "L"),
    # right: GPIO
    (1, "P1.00/XL1", "bidirectional", "R"), (2, "P1.01/XL2", "bidirectional", "R"),
    (3, "P1.02/NFC1", "bidirectional", "R"), (4, "P1.03/NFC2", "bidirectional", "R"),
    (5, "P1.04/AIN0", "bidirectional", "R"), (6, "P1.05/AIN1", "bidirectional", "R"),
    (7, "P1.06/AIN2", "bidirectional", "R"), (8, "P1.07/AIN3", "bidirectional", "R"),
    (9, "P1.08/EXTREF", "bidirectional", "R"), (37, "P1.09", "bidirectional", "R"),
    (38, "P1.10", "bidirectional", "R"), (39, "P1.11/AIN4", "bidirectional", "R"),
    (40, "P1.12/AIN5", "bidirectional", "R"), (41, "P1.13/AIN6", "bidirectional", "R"),
    (42, "P1.14/AIN7", "bidirectional", "R"),
    (11, "P2.00", "bidirectional", "R"), (12, "P2.01", "bidirectional", "R"),
    (13, "P2.02", "bidirectional", "R"), (14, "P2.03", "bidirectional", "R"),
    (15, "P2.04", "bidirectional", "R"), (16, "P2.05", "bidirectional", "R"),
    (17, "P2.06", "bidirectional", "R"), (18, "P2.07/SWO", "bidirectional", "R"),
    (19, "P2.08", "bidirectional", "R"), (20, "P2.09", "bidirectional", "R"),
    (21, "P2.10", "bidirectional", "R"),
    (23, "P0.00", "bidirectional", "R"), (24, "P0.01", "bidirectional", "R"),
    (27, "P0.02", "bidirectional", "R"), (28, "P0.03", "bidirectional", "R"),
    (29, "P0.04", "bidirectional", "R"),
]

PITCH = 2.54
PIN_LEN = 3.81
HALF_W = 15.24


def symbol():
    left = [p for p in PINS if p[3] == "L"]
    right = [p for p in PINS if p[3] == "R"]
    rows = max(len(left), len(right))
    top = (rows // 2) * PITCH
    bottom = top - (rows - 1) * PITCH
    pins = []
    for side, plist in (("L", left), ("R", right)):
        for i, (num, name, etype, _) in enumerate(plist):
            y = top - i * PITCH
            x, angle = (-HALF_W - PIN_LEN, 0) if side == "L" else (HALF_W + PIN_LEN, 180)
            pins.append(
                f'      (pin {etype} line (at {x:.2f} {y:.2f} {angle}) (length {PIN_LEN})\n'
                f'        (name "{name}" (effects (font (size 1.27 1.27))))\n'
                f'        (number "{num}" (effects (font (size 1.27 1.27)))))'
            )
    y_top, y_bot = top + PITCH, bottom - PITCH
    return f'''(kicad_symbol_lib (version 20211014) (generator sponge_tag_script)
  (symbol "nRF54L15-QFAA" (in_bom yes) (on_board yes)
    (property "Reference" "U" (id 0) (at 0 {y_top + 2.54:.2f} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "nRF54L15-QFAA" (id 1) (at 0 {y_bot - 2.54:.2f} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Package_DFN_QFN:QFN-48-1EP_6x6mm_P0.4mm_EP4.6x4.6mm" (id 2) (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "https://docs.nordicsemi.com/bundle/ps_nrf54l15/" (id 3) (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (symbol "nRF54L15-QFAA_0_1"
      (rectangle (start {-HALF_W:.2f} {y_top:.2f}) (end {HALF_W:.2f} {y_bot:.2f})
        (stroke (width 0.254) (type default)) (fill (type background))))
    (symbol "nRF54L15-QFAA_1_1"
{chr(10).join(pins)}
    )
  )
)
'''


if __name__ == "__main__":
    out = Path(__file__).with_name("nRF54L15.kicad_sym")
    out.write_text(symbol(), encoding="utf-8")
    print(f"wrote {out} ({len(PINS)} pins)")
