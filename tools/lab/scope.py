"""Oscilloscope helpers: screenshots and measurements over SCPI.

    python tools/lab/scope.py capture <instrument> <outdir> <name>   # saves <name>.png (+ <name>.txt with measurements)
    python tools/lab/scope.py measure <instrument> <channel> <item>  # e.g. C1 FREQ / PKPK / MEAN / RISE

Screenshot and measurement commands differ per vendor; extend VENDORS for your scope.
"""
import sys
from pathlib import Path

from scpi import Instrument

VENDORS = {
    "siglent": {"screenshot": "SCDP", "measure": "{ch}:PAVA? {item}"},
    "rigol": {"screenshot": ":DISP:DATA? ON,OFF,PNG", "measure": ":MEAS:ITEM? {item},{ch}"},
    "keysight": {"screenshot": ":DISP:DATA? PNG,COL", "measure": ":MEAS:{item}? {ch}"},
}


def vendor_cmds(inst):
    return VENDORS[inst.cfg.get("vendor", "siglent")]


def capture(name_inst, outdir, name):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    with Instrument(name_inst, timeout=20) as scope:
        data = scope.query_block(vendor_cmds(scope)["screenshot"])
    # Siglent SCDP returns BMP; detect the format from the magic bytes.
    ext = "png" if data[:4] == b"\x89PNG" else "bmp" if data[:2] == b"BM" else "bin"
    path = out / f"{name}.{ext}"
    path.write_bytes(data)
    print(path)


def measure(name_inst, ch, item):
    with Instrument(name_inst) as scope:
        print(scope.query(vendor_cmds(scope)["measure"].format(ch=ch, item=item)))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
    elif sys.argv[1] == "capture":
        capture(*sys.argv[2:5])
    elif sys.argv[1] == "measure":
        measure(*sys.argv[2:5])
    else:
        print(__doc__)
