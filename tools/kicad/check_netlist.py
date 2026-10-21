"""Custom netlist rule check on a KiCad S-expression netlist (.net), on top of ERC.

    python tools/kicad/check_netlist.py <board.net>

Errors: components without a footprint, single-pin nets, power-input pins left unconnected.
Warnings: auto-named nets ("Net-(...)") that join more than one component.
Exit code 1 if there are errors.
"""
import re
import sys
from pathlib import Path


def parse_sexpr(text):
    tokens = re.findall(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+', text)
    stack, cur = [], []
    for t in tokens:
        if t == "(":
            stack.append(cur)
            cur = []
        elif t == ")":
            done, cur = cur, stack.pop()
            cur.append(done)
        else:
            cur.append(t[1:-1] if t.startswith('"') else t)
    return cur[0]


def find(node, key):
    return [c for c in node if isinstance(c, list) and c and c[0] == key]


def val(node, key, default=None):
    f = find(node, key)
    return f[0][1] if f and len(f[0]) > 1 else default


def main(path):
    root = parse_sexpr(Path(path).read_text(encoding="utf-8"))
    errors, warnings = [], []

    comps = find(find(root, "components")[0], "comp")
    for c in comps:
        if not val(c, "footprint") and not val(c, "ref").startswith("#"):  # '#' = virtual (PWR_FLAG)
            errors.append(f"{val(c, 'ref')}: no footprint")

    used_pins = set()
    for net in find(find(root, "nets")[0], "net"):
        name = val(net, "name")
        nodes = find(net, "node")
        refs = {val(n, "ref") for n in nodes}
        for n in nodes:
            used_pins.add((val(n, "ref"), val(n, "pin")))
        if len(nodes) == 1 and not name.startswith("unconnected-"):
            n = nodes[0]
            errors.append(f"net '{name}' has a single pin ({val(n, 'ref')}.{val(n, 'pin')})")
        if name.startswith("Net-(") and len(refs) > 2:
            warnings.append(f"auto-named net '{name}' spans {len(refs)} components; give it a name")

    # Power-input pins left unconnected (needs pin types from libparts). KiCad's own netlist export
    # has them; SKiDL netlists don't, so the SKiDL script must check its own power pins.
    libparts = find(root, "libparts")
    if not libparts or not find(libparts[0], "libpart"):
        warnings.append("no libparts in netlist: unconnected power-input pins NOT checked here")
    pintypes = {}
    for lp in find(libparts[0], "libpart") if libparts else []:
        key = (val(lp, "lib"), val(lp, "part"))
        for pins in find(lp, "pins"):
            for pin in find(pins, "pin"):
                pintypes.setdefault(key, {})[val(pin, "num")] = val(pin, "type")
    for c in comps:
        ls = find(c, "libsource")
        key = (val(ls[0], "lib"), val(ls[0], "part")) if ls else None
        for num, typ in pintypes.get(key, {}).items():
            if typ == "power_in" and (val(c, "ref"), num) not in used_pins:
                errors.append(f"{val(c, 'ref')} pin {num}: power input not connected")

    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(comps)} components, {len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
