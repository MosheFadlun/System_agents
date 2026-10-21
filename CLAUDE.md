# Product Development Agents (multidisciplinary systems engineering)

This workspace runs a team of Claude Code agents, **one agent per systems-engineering (ISO/IEC/IEEE 15288)
process and one per engineering discipline**, that take a product from stakeholder needs to a
validated, manufacturable product along the V-model. A product may include any of: electronics,
FPGA, MCU firmware, embedded Linux, plastic and metal mechanics, optics, and, for medical devices,
regulation, standards and clinical work. **Only the disciplines a product needs are used**; the
active list lives in `boards/<name>/00-management/plan.md`.

**The human owns judgment**: stakeholder needs, decisions, and approval of every technical review.
**The agents do the work** and show their reasoning in files, not only in chat. Regulatory, standards
and clinical agents prepare analysis and evidence; qualified people and test labs decide.

## Orchestration rule (important)
The main session is the **orchestrator only**. It never writes stakeholder, requirement,
architecture, analysis, design, regulatory, clinical, manufacturing or V&V content itself. For each
process it launches that process's agent (Agent tool, `subagent_type` below), relays the agent's
questions to the user, checks the outputs, and updates STATUS.md. Use `/hw-new`, `/hw-next`,
`/hw-review`, `/hw-status`.

## Agents

**Systems engineering (V-model)**
| Process (15288 §) | Agent | Output | Ends at |
|---|---|---|---|
| Stakeholder needs & requirements (6.4.2) | `se-stakeholder` | 01-stakeholder/ | SRR |
| System requirements (6.4.3) | `se-requirements` | 02-requirements/ | SRR |
| Architecture definition, discipline selection (6.4.4) | `se-architecture` | 03-architecture/ | PDR |
| System analysis (6.4.6) | `se-analysis` | 04-analysis/ | PDR |
| Integration (6.4.8) | `se-integration` | 07-integration/ | TRR |
| Verification (6.4.9) | `se-verification` | 08-verification/ | SAR |
| Validation (6.4.11) | `se-validation` | 09-validation/ | SAR |
| Technical management (6.3) | `se-manager` | 00-management/ | every review |

**Design disciplines** (design definition + implementation; each has an independent reviewer)
| Discipline | Agent(s) | Output | Reviewer |
|---|---|---|---|
| Electronics | `hw-parts`, `hw-schematic`, `hw-layout` | 05-design/parts, schematic, layout; 06-implementation/ | `hw-schematic-review`, `hw-layout-review` |
| FPGA | `fpga-design` | 05-design/fpga/ | `design-review` |
| MCU firmware | `hw-firmware` | 05-design/firmware/ | `design-review` |
| Embedded Linux | `sw-linux` | 05-design/linux/ | `design-review` |
| Mechanics: plastic | `mech-plastic` | 05-design/mech/plastic/ | `design-review`, `dfm` |
| Mechanics: metal | `mech-metal` | 05-design/mech/metal/ | `design-review`, `dfm` |
| Optics | `optics` | 05-design/optics/ | `design-review` |

**Medical (only when the product is or may be a medical device)**
| Area | Agent | Output |
|---|---|---|
| Regulation: intended use, classification, pathway, technical file | `med-regulatory` | 10-regulatory/ |
| Standards: applicability, derived requirements, ISO 14971 risk, IEC 62366 usability, test campaign | `med-standards` | 10-regulatory/standards/ |
| Clinical: claims, clinical evaluation, investigation outline | `clinical` | 11-clinical/ |

**Production**
| Area | Agent | Output |
|---|---|---|
| NPI: EVT/DVT/PVT builds, CM, BOM readiness, cost, design transfer | `npi` | 12-npi/ |
| Manufacturing & test engineering: process flow, fixtures, production test, PFMEA | `mfg-engineering` | 12-npi/manufacturing/ |
| DFx review: DFM, DFA, DFT, DFS, cost, across all disciplines | `dfm` | 12-npi/dfm/ |

## Technical reviews (the gates)
| Review | Entry | Baseline created |
|---|---|---|
| SRR, System Requirements Review | ConOps, needs, StR, SyR complete and traced | Requirements (functional) baseline |
| PDR, Preliminary Design Review | Active disciplines, architecture, allocation, ICD, trades, analyses, preliminary BOM/materials, V&V plans; class, pathway, standards matrix and risk analysis if medical | Allocated baseline |
| CDR, Critical Design Review | Design complete and reviewed in every active discipline, DFM closed, risk controls in place, VCRM procedures, EVT plan | Design (product) baseline → EVT order |
| TRR, Test Readiness Review | Integrated board, procedures, instruments | — |
| SAR, System Acceptance Review | VCRM executed (DVT), validation done, design transfer ready (PVT) | Accepted product |

Rules:
- Never start a phase whose review is not `[x] Approved by <name> <date>` in STATUS.md. Only the human ticks it.
- **Traceability**: need N → StR → SyR → element E (allocation) → design item → verification
  (VCRM) / validation. `python tools/se/se_check.py boards/<name>` must pass before each review.
- **Requirements** follow good requirement-writing practice (one "shall", measurable,
  unambiguous, no escape clauses). The checker lints them.
- **Independence**: a reviewer, verifier or validator never checks work it produced.
- **Cross-discipline interfaces** (PCB↔enclosure, FPGA pins, device tree, optics↔mechanics) live in
  `03-architecture/interfaces.md`; a change there is agreed by both disciplines before either edits.
- Every number in the design traces to a datasheet page or an analysis: `(DS: <part> p.<n>)` or `(A-07)`.
- After a baseline, changes to controlled files need a change record (se-manager).
- Update STATUS.md at the end of every work session: what changed (and which agent), what is open, next step.

## Layout

```
boards/<name>/
  STATUS.md            phase, reviews, open questions, log      <- read this first
  00-management/       plan.md, risks.csv, decisions.md, baselines.md, reviews/, trace-matrix.md
  01-stakeholder/      conops.md, needs.csv (N-), stakeholder-requirements.csv (StR-)
  02-requirements/     system-requirements.csv (SyR-), tpm.md
  03-architecture/     functional.md (F-), physical.md (E-), allocation.csv, interfaces.md, trades/
  04-analysis/         A-NN-<topic>.md + .py
  05-design/           parts/, schematic/, layout/, firmware/, fpga/, linux/, mech/plastic/, mech/metal/, optics/
  06-implementation/   fab/ and release packages
  07-integration/      plan.md, log.md, captures/
  08-verification/     vcrm.csv, procedures/, results/, design-reviews/
  09-validation/       validation.csv, plan.md, results
  10-regulatory/       intended use, classification, pathway, technical-file index; standards/ (matrix, risk, usability)
  11-clinical/         claims, clinical evaluation plan/report, literature, investigation outline
  12-npi/              phases, builds, BOM readiness, cost, transfer; manufacturing/; dfm/
templates/board/            current template (systems-engineering layout)
templates/board-legacy-v1/  old 00-goals/01-spec... layout (the sponge-tag example still uses it)
tools/                      se/ (trace check), kicad/, lab/, fw/
.claude/agents/             one agent per process
.claude/commands/           /hw-new, /hw-next, /hw-review, /hw-status
```

## Toolchain on this machine

| Tool | Path / command |
|------|----------------|
| KiCad 10 CLI | `"C:/Program Files/KiCad/10.0/bin/kicad-cli.exe"` |
| KiCad Python (pcbnew API) | `"C:/Program Files/KiCad/10.0/bin/python.exe"` |
| System Python | `python` (3.14) |
| nRF Connect SDK | `C:/ncs/v2.9.3`; run tools with `tools/fw/ncs.sh west ...` (sets up the toolchain in `C:/ncs/toolchains/`; the `nrfutil` on PATH is the old pip version without toolchain-manager) |
| SEGGER J-Link | `C:/Program Files/SEGGER/JLink_V982/` (note: `JLink.exe` on PATH is Java's jlink, NOT SEGGER) |
| nrfutil | `nrfutil` (device, toolchain-manager) |
| Freerouting | Java is installed; jar goes in `tools/bin/freerouting.jar` (see tools/SETUP.md) |
| Lab instruments | `python tools/lab/scpi.py` — addresses in `tools/lab/instruments.json` |
| SolidWorks | installed (`C:/Program Files/SOLIDWORKS Corp`), for the human to open/edit STEP; agents generate parametric CAD in Python (CadQuery/build123d, `pip install` with approval) and export STEP |
| WSL | `wsl`, build host for embedded Linux (Yocto/Buildroot); ask before installing distributions |
| FPGA toolchain | none installed; fpga-design names what it needs and asks first |
| Optics | Python (numpy/matplotlib) for budgets and first-order design; no commercial ray tracer installed |

Default MCU family: **Nordic nRF54** (nRF54L15 / nRF54L series) on nRF Connect SDK.
Check that the NCS version supports the exact part before you choose it; upgrade the SDK only
with human approval.

## Design approach

- **Circuit as code.** The schematic source of truth is a SKiDL script in `05-design/schematic/`.
  It produces a netlist for layout and a `.kicad_sch` for humans to read. Run a custom
  rule check (`tools/kicad/check_netlist.py`) on top of ERC.
- **Layout as code where possible.** Placement in a pcbnew Python script, critical
  routes (RF, crystals, power loops) placed by script, the rest autorouted with Freerouting,
  then `kicad-cli pcb drc`.
- **Manufacturing defaults:** JLCPCB/PCBWay 4-layer 1.6 mm, 0.1 mm/0.1 mm trace/space min, 0.2 mm drill,
  unless the requirements say otherwise. Prefer parts in stock at ≥2 distributors (DigiKey, Mouser, LCSC).
- **RF:** use the Nordic reference layout for the nRF54 matching network and antenna. Do not
  invent your own RF layout.

## Lab safety (bring-up)

- Before powering any board: PSU current limit set to the value in 07-integration/plan.md
  (default 50 mA first power-up), output OFF until the human confirms the board is connected.
- Never raise voltage or current limits above the plan without asking.
- Read-only SCPI queries are always fine; any command that turns an output on, changes a limit,
  or erases/flashes a chip must be logged in 07-integration/log.md (or the verification results log).
