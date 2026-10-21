# System_agents: multidisciplinary product development agents for Claude Code

A Claude Code workspace that runs a team of agents, **one per systems-engineering (ISO/IEC/IEEE 15288)
process and one per engineering discipline**, to take a product from stakeholder needs to a validated,
manufacturable product along the V-model. A product may use any of these disciplines (only the
ones it needs are activated): electronics, FPGA, MCU firmware, embedded Linux, plastic and metal
mechanics, optics, and for medical devices regulation, standards/risk and clinical, plus NPI,
manufacturing/test engineering and DFM.

The human owns judgment (needs, decisions, approval of each technical review: SRR, PDR, CDR, TRR, SAR).
The agents do the work and write their reasoning into files.

## What's inside
| Path | What |
|---|---|
| `CLAUDE.md` | Rules for the orchestrator, process → agent map, review gates, toolchain |
| `.claude/agents/` | 26 agents. **Systems engineering:** `se-stakeholder`, `se-requirements`, `se-architecture`, `se-analysis`, `se-integration`, `se-verification`, `se-validation`, `se-manager`. **Disciplines:** `hw-parts`, `hw-schematic`, `hw-layout` (electronics), `fpga-design`, `hw-firmware`, `sw-linux`, `mech-plastic`, `mech-metal`, `optics`. **Reviews:** `hw-schematic-review`, `hw-layout-review`, `design-review`, `dfm`. **Medical:** `med-regulatory`, `med-standards`, `clinical`. **Production:** `npi`, `mfg-engineering` |
| `.claude/commands/` | `/hw-new`, `/hw-next`, `/hw-review`, `/hw-status` |
| `templates/board/` | Folder template per product (00-management … 12-npi, incl. 10-regulatory and 11-clinical) |
| `tools/se/se_check.py` | Traceability (N → StR → SyR → element → VCRM/validation) and requirement-quality lint (requirement-writing rules) |
| `tools/kicad/` | SKiDL/KiCad helpers: netlist rule check, ERC/DRC/fab export wrappers, symbol generator |
| `tools/lab/` | SCPI over LAN for PSU/DMM/scope, with a safe PSU wrapper (hard limits, overcurrent trip, logging) |
| `tools/fw/ncs.sh` | Run nRF Connect SDK tools without nrfutil toolchain-manager |
| `boards/sponge-tag/` | Worked example (older folder layout): coin-cell BLE temperature/humidity tag on nRF54L15 |

## Quick start
1. Install KiCad 10, Python 3, `pip install skidl`, nRF Connect SDK (see `tools/SETUP.md`), and adjust the paths in `CLAUDE.md`.
2. Open Claude Code in this folder and run `/hw-new <board>`.
3. Answer the stakeholder questions; then `/hw-next <board>` runs one process at a time, and `/hw-review <board> SRR` prepares a review.

Regulatory, standards and clinical agents prepare analysis and evidence only; qualified people,
notified bodies/FDA and accredited test labs make the decisions.

Status: experimental. The example's RF matching network and some reference-circuit wiring are
marked unverified on purpose. Check everything against the datasheets before ordering boards.
