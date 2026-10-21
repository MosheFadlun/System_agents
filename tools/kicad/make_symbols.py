"""Generate a KiCad symbol library from simple pin tables (for parts KiCad doesn't ship).

    from make_symbols import write_library
    write_library("lib/myboard.kicad_sym", {
        "PartName": {
            "footprint": "Lib:Footprint",          # optional
            "datasheet": "https://...",            # optional
            "pins": [(num, name, etype, side), ...],  # side: "L" or "R"
        },
    })

etype is a KiCad pin type: power_in, power_out, input, output, bidirectional, passive,
open_collector, no_connect. Pins named "NC"/"RESV" can use passive.
"""
from pathlib import Path

PITCH = 2.54
PIN_LEN = 3.81


def _symbol(name, spec):
    pins = spec["pins"]
    left = [p for p in pins if p[3] == "L"]
    right = [p for p in pins if p[3] == "R"]
    rows = max(len(left), len(right), 1)
    longest = max((len(p[1]) for p in pins), default=4)
    half_w = max(10.16, round((longest * 1.27 + 2.54) / 2.54) * 2.54)
    top = (rows // 2) * PITCH
    out = []
    for side, plist in (("L", left), ("R", right)):
        for i, (num, pname, etype, _) in enumerate(plist):
            y = top - i * PITCH
            x, angle = (-half_w - PIN_LEN, 0) if side == "L" else (half_w + PIN_LEN, 180)
            out.append(
                f'      (pin {etype} line (at {x:.2f} {y:.2f} {angle}) (length {PIN_LEN})\n'
                f'        (name "{pname}" (effects (font (size 1.27 1.27))))\n'
                f'        (number "{num}" (effects (font (size 1.27 1.27)))))'
            )
    y_top, y_bot = top + PITCH, top - rows * PITCH
    fp = spec.get("footprint", "")
    ds = spec.get("datasheet", "")
    return f'''  (symbol "{name}" (in_bom yes) (on_board yes)
    (property "Reference" "{spec.get('ref', 'U')}" (id 0) (at 0 {y_top + 2.54:.2f} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "{name}" (id 1) (at 0 {y_bot - 2.54:.2f} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "{fp}" (id 2) (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "{ds}" (id 3) (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (symbol "{name}_0_1"
      (rectangle (start {-half_w:.2f} {y_top:.2f}) (end {half_w:.2f} {y_bot:.2f})
        (stroke (width 0.254) (type default)) (fill (type background))))
    (symbol "{name}_1_1"
{chr(10).join(out)}
    )
  )'''


def write_library(path, parts, generator="hw_agent_make_symbols"):
    body = "\n".join(_symbol(n, s) for n, s in parts.items())
    text = f"(kicad_symbol_lib (version 20211014) (generator {generator})\n{body}\n)\n"
    Path(path).write_text(text, encoding="utf-8")
    return path
