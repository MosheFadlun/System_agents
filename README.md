# System_agents: INCOSE hardware design agents for Claude Code

A Claude Code workspace that runs a team of agents, **one per INCOSE / ISO/IEC/IEEE 15288 process**,
to take an electronics board from stakeholder needs to a validated prototype along the V-model:
stakeholder needs → system requirements → architecture and analysis → parts, schematic, layout,
firmware → design reviews → fab → integration (bring-up) → verification → validation.

The human owns judgment (needs, decisions, approval of each technical review: SRR, PDR, CDR, TRR, SAR).
The agents do the work and write their reasoning into files.

## What's inside
| Path | What |
|---|---|
| `CLAUDE.md` | Rules for the orchestrator, process → agent map, review gates, toolchain |
| `.claude/agents/` | 14 agents: `se-stakeholder`, `se-requirements`, `se-architecture`, `se-analysis`, `se-manager`, `hw-parts`, `hw-schematic`, `hw-schematic-review`, `hw-layout`, `hw-layout-review`, `hw-firmware`, `se-integration`, `se-verification`, `se-validation` |
| `.claude/commands/` | `/hw-new`, `/hw-next`, `/hw-review`, `/hw-status` |
| `templates/board/` | Folder template per board (00-management … 09-validation) |
| `tools/se/se_check.py` | Traceability (N → StR → SyR → element → VCRM/validation) and requirement-quality lint (INCOSE Guide to Writing Requirements subset) |
| `tools/kicad/` | SKiDL/KiCad helpers: netlist rule check, ERC/DRC/fab export wrappers, symbol generator |
| `tools/lab/` | SCPI over LAN for PSU/DMM/scope, with a safe PSU wrapper (hard limits, overcurrent trip, logging) |
| `tools/fw/ncs.sh` | Run nRF Connect SDK tools without nrfutil toolchain-manager |
| `boards/sponge-tag/` | Worked example (older folder layout): coin-cell BLE temperature/humidity tag on nRF54L15 |

## Quick start
1. Install KiCad 10, Python 3, `pip install skidl`, nRF Connect SDK (see `tools/SETUP.md`), and adjust the paths in `CLAUDE.md`.
2. Open Claude Code in this folder and run `/hw-new <board>`.
3. Answer the stakeholder questions; then `/hw-next <board>` runs one process at a time, and `/hw-review <board> SRR` prepares a review.

Status: experimental. The example's RF matching network and some reference-circuit wiring are
marked unverified on purpose. Check everything against the datasheets before ordering boards.
