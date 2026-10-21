"""Wrappers around kicad-cli for the agent.

    python tools/kicad/kicad_checks.py erc    <file.kicad_sch>          -> erc.json next to it, prints a summary
    python tools/kicad/kicad_checks.py drc    <file.kicad_pcb>          -> drc.json next to it, prints a summary
    python tools/kicad/kicad_checks.py render <file.kicad_pcb> <outdir> -> top.png / bottom.png
    python tools/kicad/kicad_checks.py fab    <file.kicad_pcb> <outdir> -> gerbers, drill, pos, step, renders

Exit code 1 if ERC/DRC report errors.
"""
import json
import subprocess
import sys
from pathlib import Path

KICAD_CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"


def run(*args):
    cmd = [KICAD_CLI, *map(str, args)]
    print(">", " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode not in (0, 5):  # 5 = violations found (with --exit-code-violations)
        print(r.stdout, r.stderr)
        raise SystemExit(f"kicad-cli failed ({r.returncode})")
    return r


def summarize(report_path):
    rep = json.loads(Path(report_path).read_text(encoding="utf-8"))
    items = list(rep.get("violations", []))
    for sheet in rep.get("sheets", []):
        items += sheet.get("violations", [])
    items += rep.get("unconnected_items", [])
    items += rep.get("schematic_parity", [])
    counts = {}
    for v in items:
        counts[v.get("severity", "?")] = counts.get(v.get("severity", "?"), 0) + 1
    print(f"{report_path}: {counts or 'clean'}")
    for v in items:
        if v.get("severity") == "error":
            print(f"  [{v.get('type')}] {v.get('description')}")
    return counts.get("error", 0)


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return
    action, src = argv[0], Path(argv[1])
    if action == "erc":
        out = src.with_name("erc.json")
        run("sch", "erc", "--format", "json", "--severity-all", "-o", out, src)
        sys.exit(1 if summarize(out) else 0)
    if action == "drc":
        out = src.with_name("drc.json")
        run("pcb", "drc", "--format", "json", "--severity-all", "--schematic-parity", "-o", out, src)
        sys.exit(1 if summarize(out) else 0)
    outdir = Path(argv[2])
    outdir.mkdir(parents=True, exist_ok=True)
    if action in ("render", "fab"):
        for side in ("top", "bottom"):
            run("pcb", "render", "--side", side, "--quality", "high", "-w", 1600, "-h", 1200,
                "-o", outdir / f"{side}.png", src)
    if action == "fab":
        g = outdir / "gerbers"
        g.mkdir(exist_ok=True)
        run("pcb", "export", "gerbers", "-o", g, src)
        run("pcb", "export", "drill", "-o", g, src)
        run("pcb", "export", "pos", "--format", "csv", "--units", "mm", "-o", outdir / "positions.csv", src)
        run("pcb", "export", "step", "-o", outdir / f"{src.stem}.step", src)
        print(f"Fab outputs in {outdir}")


if __name__ == "__main__":
    main(sys.argv[1:])
