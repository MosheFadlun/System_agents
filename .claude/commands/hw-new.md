---
description: Start a new board (INCOSE stakeholder needs) - copy the template and run the se-stakeholder agent
argument-hint: <board-name>
---
Create a new board named `$ARGUMENTS`. You are the orchestrator: do not write stakeholder content yourself.

1. Copy `templates/board/` to `boards/$ARGUMENTS/` (fail if it exists), and replace `<board>` with
   `$ARGUMENTS` in STATUS.md, plan.md and conops.md.
2. Ask me for a short free-text description of the product and any reference material (existing
   product docs, earlier boards, related repos, sessions). Wait for my answer.
3. Run the **se-stakeholder** agent with the board path, my words quoted exactly, and the references.
4. Relay its questions to me (at most 6 at a time). Send my answers back to the same agent
   (SendMessage to its id) until it reports no blocking questions.
5. Run `python tools/se/se_check.py boards/$ARGUMENTS`, then summarize the ConOps, the needs and
   stakeholder requirements, and the open TBDs. Log it in STATUS.md.
