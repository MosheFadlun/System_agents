---
description: Summarize one board (phase, reviews, trace check, risks) or list all boards
argument-hint: [board-name]
---
If `$ARGUMENTS` is empty, list every folder in `boards/` with its current phase and next review (one
line each; say "legacy layout" for boards without `00-management/`).

Otherwise, for `boards/$ARGUMENTS/`: read STATUS.md, run `python tools/se/se_check.py boards/$ARGUMENTS`,
read `00-management/risks.csv` and the open design-review findings, and summarize: phase,
reviews approved, counts (needs / StR / SyR / allocated / verified / validated), trace errors,
top risks (score ≥ 12), open questions, next process and agent.
