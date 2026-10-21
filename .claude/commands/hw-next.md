---
description: Run the next systems-engineering process for a board by dispatching its agent (respects the technical-review gates)
argument-hint: <board-name> [process]
---
Board: `boards/<first word of $ARGUMENTS>/`. An optional second word names the process to run.
You are the orchestrator: every process is done by its own agent; you only dispatch, check, relay
questions and update STATUS.md.

1. Read STATUS.md and `00-management/plan.md`. Find the next process in this order:

   | Phase | Process → agent | Gate before it |
   |---|---|---|
   | Needs | se-stakeholder | — |
   | Medical track (only if medical) | med-regulatory (intended use, class, pathway), clinical (claims), med-standards (standards matrix, risk analysis start) | stakeholder needs done |
   | Requirements | se-requirements (merges standards/regulatory/clinical/production proposals) | — |
   | Review | se-manager prepares SRR | — |
   | Architecture | se-architecture (sets the active disciplines), se-analysis (as needed), hw-parts and other discipline part/material selection | SRR approved |
   | Planning | se-verification + se-validation plans; npi phases; mfg-engineering test strategy | SRR approved |
   | Review | se-manager prepares PDR | — |
   | Design (only active disciplines, in parallel where independent) | electronics hw-schematic ⇄ hw-schematic-review, hw-layout ⇄ hw-layout-review; fpga-design, hw-firmware (only if the user asked), sw-linux, mech-plastic, mech-metal, optics, each ⇄ design-review; dfm on all; med-standards updates risk controls | PDR approved |
   | Review | se-manager prepares CDR | — |
   | Implementation / EVT | fab packages; npi EVT build plan → human orders | CDR approved |
   | Integration | se-integration | EVT parts received |
   | Review | se-manager prepares TRR | — |
   | Verification (DVT) | se-verification (execute; standards test campaign if medical) | TRR approved |
   | Validation | se-validation (usability/clinical if medical) | verification done |
   | Production (PVT, transfer) | npi, mfg-engineering, dfm | DVT exit |
   | Review | se-manager prepares SAR | — |

   Skip processes for disciplines marked "not in scope" in `00-management/plan.md`.

2. If the gate for that process is not `[x] Approved` in STATUS.md, stop: run se-manager to
   prepare the review package, show me the recommendation and what I must check, and ask for approval.
3. Otherwise run the agent with the board path and the context it needs (decisions I made, quoted).
   - Design ⇄ review loops: the reviewer never reviews its own work. After blockers/majors, run the
     designer to fix them, then the reviewer on the changes. At most 3 rounds, then hand the rest to me.
   - If an agent returns questions, relay them to me and send my answers back to the same agent.
   - Independent processes may run in parallel (e.g. discipline designs with agreed interfaces,
     se-analysis runs, V&V planning). Two agents never write the same files.
4. Verify the outputs yourself: files exist, `python tools/se/se_check.py <board>` passes, and the
   process checks pass (ERC/DRC/build). Don't trust an agent's summary alone.
5. Run se-manager to update risks, decisions and TPMs. Update STATUS.md (log line naming the agent).
   Tell me what was done, the key decisions, the open questions, and what I review next.
