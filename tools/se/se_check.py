"""Traceability + requirement-quality check for one board.

    python tools/se/se_check.py boards/<name>            # check, exit 1 on errors
    python tools/se/se_check.py boards/<name> --matrix   # also write 00-management/trace-matrix.md

Chain checked (files are optional until their process has run):
  01-stakeholder/needs.csv                 N-xxx
  01-stakeholder/stakeholder-requirements.csv  StR-xxx  (parent = N-xxx)
  02-requirements/system-requirements.csv  SyR-xxx  (parent = StR-xxx or SyR-xxx)
  03-architecture/allocation.csv           SyR -> element E-xx / function F-xx
  08-verification/vcrm.csv                 SyR -> verification (I/A/D/T)
  09-validation/validation.csv             StR -> validation scenario

Requirement-quality rules are a subset of common requirement-writing rules:
singular "shall", no vague terms, no escape clauses, no open-ended lists, no combinators
(and/or), no superlatives, positive statements, measurable performance (number + unit), no TBD.
"""
import csv
import re
import sys
from pathlib import Path

VAGUE = ["adequate", "appropriate", "user-friendly", "user friendly", "easy", "simple", "fast", "quick",
         "rapid", "efficient", "flexible", "robust", "reliable", "sufficient", "low power", "high",
         "low", "small", "large", "significant", "approximately", "about", "several", "some", "many",
         "most", "typical", "normal", "reasonable", "minimal", "state of the art", "seamless", "support"]
ESCAPE = ["if possible", "as possible", "where possible", "if practical", "where practical",
          "as appropriate", "if necessary", "as required", "as needed", "to the extent"]
OPEN_ENDED = ["etc", "and so on", "including but not limited to", "such as"]
SUPERLATIVE = ["best", "optimal", "optimum", "minimize", "maximize", "minimise", "maximise", "fastest", "lowest", "highest"]
UNIT_RE = re.compile(r"\d\s*(%|°c|degc|v|mv|µv|uv|a|ma|µa|ua|na|w|mw|µw|uw|mah|ah|s|ms|µs|us|min|h|hz|khz|mhz|ghz|"
                     r"sps|dbm|db|m|mm|cm|g|kg|years?|months?|days?|hours?|kbit/s|mbit/s|kb|mb|b|bytes?|"
                     r"samples?|cycles?|times?|x|clicks?|°)\b", re.I)
METHODS = {"I", "A", "D", "T"}  # Inspection, Analysis, Demonstration, Test


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, m):
        self.errors.append(m)

    def warn(self, m):
        self.warnings.append(m)


def load(path):
    if not path.exists():
        return None
    with path.open(encoding="utf-8-sig", newline="") as f:
        return [{k.strip(): (v or "").strip() for k, v in row.items() if k} for row in csv.DictReader(f)]


def split_ids(cell):
    return [x for x in re.split(r"[;,\s]+", cell or "") if x]


def has_word(text, phrase):
    return re.search(r"(?<![\w-])" + re.escape(phrase) + r"(?![\w-])", text, re.I) is not None


def lint(rid, text, rtype, rep):
    t = text.lower()
    n_shall = len(re.findall(r"\bshall\b", t))
    if n_shall == 0:
        rep.err(f"{rid}: no 'shall' (requirements use 'shall')")
    elif n_shall > 1:
        rep.err(f"{rid}: {n_shall}x 'shall', split it (singular)")
    t_vague = re.sub(r"\bat (most|least)\b", "", t)  # "at most 3 uA" is a precise bound
    for w in VAGUE:
        if has_word(t_vague, w):
            rep.warn(f"{rid}: vague term '{w}' (unambiguous: give a value)")
    for w in ESCAPE:
        if w in t:
            rep.err(f"{rid}: escape clause '{w}' (not verifiable)")
    for w in OPEN_ENDED:
        if has_word(t, w):
            rep.err(f"{rid}: open-ended '{w}' (complete: list every item)")
    if "and/or" in t:
        rep.err(f"{rid}: 'and/or' (ambiguous combinator)")
    for w in SUPERLATIVE:
        if has_word(t, w):
            rep.warn(f"{rid}: superlative '{w}' (state the limit)")
    if re.search(r"\bshall not\b", t):
        rep.warn(f"{rid}: negative requirement ('shall not'), prefer a positive, verifiable form if one exists")
    if re.search(r"\btb[dcr]\b", t):
        rep.warn(f"{rid}: contains TBD/TBC/TBR (track until closed)")
    if rtype.lower().startswith("perf") and not UNIT_RE.search(text):
        rep.err(f"{rid}: performance requirement without a number + unit (measurable)")


def check_ids(rows, prefix, name, rep):
    seen = set()
    for r in rows:
        rid = r.get("id", "")
        if not re.fullmatch(prefix + r"-\d{2,4}[A-Za-z]?", rid):
            rep.err(f"{name}: bad id '{rid}' (expected {prefix}-NNN)")
        if rid in seen:
            rep.err(f"{name}: duplicate id {rid}")
        seen.add(rid)
    return seen


def main(board, write_matrix=False):
    b = Path(board)
    rep = Report()
    needs = load(b / "01-stakeholder" / "needs.csv")
    strs = load(b / "01-stakeholder" / "stakeholder-requirements.csv")
    syrs = load(b / "02-requirements" / "system-requirements.csv")
    alloc = load(b / "03-architecture" / "allocation.csv")
    vcrm = load(b / "08-verification" / "vcrm.csv")
    val = load(b / "09-validation" / "validation.csv")

    n_ids = check_ids(needs, "N", "needs", rep) if needs is not None else set()
    s_ids = check_ids(strs, "StR", "stakeholder-requirements", rep) if strs is not None else set()
    y_ids = check_ids(syrs, "SyR", "system-requirements", rep) if syrs is not None else set()

    if strs is not None:
        covered = set()
        for r in strs:
            lint(r["id"], r.get("text", ""), r.get("type", ""), rep)
            parents = split_ids(r.get("parent_needs", ""))
            if not parents:
                rep.err(f"{r['id']}: no parent need")
            for p in parents:
                if p not in n_ids:
                    rep.err(f"{r['id']}: parent {p} not in needs.csv")
                covered.add(p)
            if not r.get("validation_method"):
                rep.err(f"{r['id']}: no validation method")
        for n in sorted(n_ids - covered):
            rep.warn(f"{n}: need not addressed by any stakeholder requirement")

    if syrs is not None:
        covered = set()
        for r in syrs:
            lint(r["id"], r.get("text", ""), r.get("type", ""), rep)
            parents = split_ids(r.get("parent", ""))
            if not parents:
                rep.err(f"{r['id']}: no parent (StR-xxx or SyR-xxx)")
            for p in parents:
                if p not in s_ids and p not in y_ids:
                    rep.err(f"{r['id']}: parent {p} not found")
                covered.add(p)
            m = r.get("verification_method", "").upper()
            if not m or not set(split_ids(m.replace("/", " "))) <= METHODS:
                rep.err(f"{r['id']}: verification_method '{m}' must be I, A, D or T")
            if not r.get("rationale"):
                rep.warn(f"{r['id']}: no rationale (record why)")
        for s in sorted(s_ids - covered):
            rep.err(f"{s}: stakeholder requirement not traced to any system requirement")

    if alloc is not None:
        allocated = {r.get("syr_id") for r in alloc}
        for r in alloc:
            if r.get("syr_id") not in y_ids:
                rep.err(f"allocation: {r.get('syr_id')} not a system requirement")
            if not re.fullmatch(r"E-\d{2,3}", r.get("element_id", "")):
                rep.err(f"allocation: {r.get('syr_id')} has bad element_id '{r.get('element_id')}'")
        for y in sorted(y_ids - allocated):
            rep.err(f"{y}: not allocated to any architecture element")

    if vcrm is not None:
        verified = {}
        for r in vcrm:
            verified.setdefault(r.get("req_id"), []).append(r)
            if r.get("req_id") not in y_ids:
                rep.err(f"vcrm: {r.get('req_id')} not a system requirement")
            if r.get("status", "").lower() in ("pass", "fail") and not r.get("evidence"):
                rep.err(f"vcrm: {r.get('req_id')} status {r.get('status')} without evidence")
        for y in sorted(y_ids - set(verified)):
            rep.err(f"{y}: no entry in the VCRM")

    if val is not None:
        validated = {r.get("str_id") for r in val}
        for s in sorted(s_ids - validated):
            rep.err(f"{s}: no validation entry")

    if write_matrix and syrs is not None:
        al = {}
        for r in alloc or []:
            al.setdefault(r["syr_id"], []).append(r["element_id"])
        vc = {r["req_id"]: f"{r.get('method', '')} {r.get('status', '')}".strip() for r in vcrm or []}
        s_par = {r["id"]: r.get("parent_needs", "") for r in strs or []}
        lines = ["# Traceability matrix (generated by tools/se/se_check.py)", "",
                 "| Need | StR | SyR | Elements | Verification |", "|---|---|---|---|---|"]
        for r in syrs:
            for p in split_ids(r.get("parent", "")) or ["—"]:
                lines.append(f"| {s_par.get(p, '—')} | {p} | {r['id']} | {', '.join(al.get(r['id'], [])) or '—'} | {vc.get(r['id'], '—')} |")
        out = b / "00-management" / "trace-matrix.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"wrote {out}")

    counts = {k: (len(v) if v is not None else "—") for k, v in
              (("needs", needs), ("StR", strs), ("SyR", syrs), ("alloc", alloc), ("vcrm", vcrm), ("validation", val))}
    for w in rep.warnings:
        print("WARN ", w)
    for e in rep.errors:
        print("ERROR", e)
    print(f"{counts} -> {len(rep.errors)} errors, {len(rep.warnings)} warnings")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], "--matrix" in sys.argv))
