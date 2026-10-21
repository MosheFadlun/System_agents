# Hardware Design Agents (INCOSE systems engineering)

This workspace runs a team of Claude Code agents, **one agent per INCOSE / ISO/IEC/IEEE 15288
process**, that take a board from stakeholder needs to a validated prototype along the V-model.

**The human owns judgment**: stakeholder needs, decisions, and approval of every technical review.
**The agents do the work** and show their reasoning in files, not only in chat.

## Orchestration rule (important)
The main session is the **orchestrator only**. It never writes stakeholder, requirement,
architecture, analysis, design, or V&V content itself. For each process it launches that process's
agent (Agent tool, `subagent_type` below), relays the agent's questions to the user, checks the
outputs, and updates STATUS.md. Use `/hw-new`, `/hw-next`, `/hw-review`, `/hw-status`.

## Processes, agents and the V-model

```
 Stakeholder needs (se-stakeholder) ............................ Validation (se-validation)
     System requirements (se-requirements) ................ Verification (se-verification)
         Architecture (se-architecture) + Analysis (se-analysis) ... Integration (se-integration)
             Design: parts / schematic / layout / firmware   (hw-parts, hw-schematic, hw-layout, hw-firmware)
                 Design verification (hw-schematic-review, hw-layout-review) -> Implementation (fab)
 Technical management across all phases: se-manager (plan, risks, decisions, baselines, TPMs, reviews)
```

| INCOSE process (15288 §) | Agent | Output folder | Ends at |
|---|---|---|---|
| Stakeholder needs & requirements (6.4.2) | `se-stakeholder` | 01-stakeholder/ | SRR |
| System requirements (6.4.3) | `se-requirements` | 02-requirements/ | SRR |
| Architecture definition (6.4.4) | `se-architecture` | 03-architecture/ | PDR |
| System analysis (6.4.6) | `se-analysis` | 04-analysis/ | PDR |
| Design definition: parts (6.4.5) | `hw-parts` | 05-design/parts/ | PDR |
| Design definition: schematic | `hw-schematic` | 05-design/schematic/ | CDR |
| Design definition: layout; Implementation (6.4.7) | `hw-layout` | 05-design/layout/, 06-implementation/ | CDR |
| Design definition: firmware | `hw-firmware` | 05-design/firmware/ | CDR |
| Design verification (peer reviews) | `hw-schematic-review`, `hw-layout-review` | 08-verification/design-reviews/ | CDR |
| Integration (6.4.8) | `se-integration` | 07-integration/ | TRR |
| Verification (6.4.9) | `se-verification` | 08-verification/ | SAR |
| Validation (6.4.11) | `se-validation` | 09-validation/ | SAR |
| Technical management (6.3) | `se-manager` | 00-management/ | every review |

## Technical reviews (the gates)
| Review | Entry | Baseline created |
|---|---|---|
| SRR, System Requirements Review | ConOps, needs, StR, SyR complete and traced | Requirements (functional) baseline |
| PDR, Preliminary Design Review | Architecture, allocation, ICD, trades, analyses, preliminary BOM, V&V plans | Allocated baseline |
| CDR, Critical Design Review | Schematic, layout, firmware design, design reviews closed, VCRM procedures | Design (product) baseline → order |
| TRR, Test Readiness Review | Integrated board, procedures, instruments | — |
| SAR, System Acceptance Review | VCRM executed, validation done | Accepted product |

Rules:
- Never start a phase whose review is not `[x] Approved by <name> <date>` in STATUS.md. Only the human ticks it.
- **Traceability**: need N → StR → SyR → element E (allocation) → design item → verification
  (VCRM) / validation. `python tools/se/se_check.py boards/<name>` must pass before each review.
- **Requirements** follow the INCOSE Guide to Writing Requirements (one "shall", measurable,
  unambiguous, no escape clauses). The checker lints them.
- **Independence**: a reviewer, verifier or validator never checks work it produced.
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
  05-design/           parts/, schematic/, layout/, firmware/
  06-implementation/   fab/
  07-integration/      plan.md, log.md, captures/
  08-verification/     vcrm.csv, procedures/, results/, design-reviews/
  09-validation/       validation.csv, plan.md, results
templates/board/            current template (INCOSE)
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
