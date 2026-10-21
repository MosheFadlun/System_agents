---
description: Run the next INCOSE process for a board by dispatching its agent (respects the technical-review gates)
argument-hint: <board-name> [process]
---
Board: `boards/<first word of $ARGUMENTS>/`. An optional second word names the process to run.
You are the orchestrator: every process is done by its own agent; you only dispatch, check, relay
questions and update STATUS.md.

1. Read STATUS.md and `00-management/plan.md`. Find the next process in this order:

   | Phase | Process → agent | Gate before it |
   |---|---|---|
   | Requirements | se-stakeholder → se-requirements | — |
   | Review | se-manager prepares SRR | — |
   | Architecture | se-architecture, se-analysis (as many runs as the trades need), hw-parts | SRR approved |
   | Planning V&V | se-verification (VCRM plan), se-validation (plan) | SRR approved |
   | Review | se-manager prepares PDR | — |
   | Design | hw-schematic ⇄ hw-schematic-review, then hw-layout ⇄ hw-layout-review; hw-firmware only if the user asked | PDR approved |
   | Review | se-manager prepares CDR | — |
   | Implementation | hw-layout (fab package) → human orders | CDR approved |
   | Integration | se-integration | boards received |
   | Review | se-manager prepares TRR | — |
   | Verification | se-verification (execute) | TRR approved |
   | Validation | se-validation (execute) | verification done |
   | Review | se-manager prepares SAR | — |

2. If the gate for that process is not `[x] Approved` in STATUS.md, stop: run se-manager to
   prepare the review package, show me the recommendation and what I must check, and ask for approval.
3. Otherwise run the agent with the board path and the context it needs (decisions I made, quoted).
   - Design ⇄ review loops: the reviewer never reviews its own work. After blockers/majors, run the
     designer to fix them, then the reviewer on the changes. At most 3 rounds, then hand the rest to me.
   - If an agent returns questions, relay them to me and send my answers back to the same agent.
   - Independent processes may run in parallel (e.g. se-analysis runs, V&V planning).
4. Verify the outputs yourself: files exist, `python tools/se/se_check.py <board>` passes, and the
   process checks pass (ERC/DRC/build). Don't trust an agent's summary alone.
5. Run se-manager to update risks, decisions and TPMs. Update STATUS.md (log line naming the agent).
   Tell me what was done, the key decisions, the open questions, and what I review next.
