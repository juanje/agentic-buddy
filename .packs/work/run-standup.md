---
last_accessed: YYYY-MM-DD
access_count: 0
created: YYYY-MM-DD
---

# Skill: Run standup

## When to use

Use when the user says "standup", "what's on my plate", "what did I do yesterday",
"what should I work on", "daily", or starts a session without a specific request.

## Procedure

### 1. Gather data

Run these in parallel to save time:
- `did yesterday` (or `did last friday` on Mondays) — what was done.
- `jira-pending sprint` — current sprint tickets and their status.
- Read `user/BOARD.md` — board state.

If any tool is unavailable or fails, skip it and note it.

### 2. Present the standup

**What was done** (from `did`):
- Summarize key activities grouped by project or theme.
- If `did` returned nothing or wasn't available, say so honestly.

**Sprint status** (from `jira-pending sprint`):
- Show current sprint tickets with their status.
- Highlight any that changed status since yesterday.

Present board sections in **file order** (same as `BOARD.md`):

**Currently doing** (from board):
- Show the "Doing" section.
- If more than 2 items in Doing, warn about WIP (AGENTS.md Rule 9).

**Next up** (from board):
- Show the "Next Actions" queue (max 3–4 items).
- Cross-reference with sprint tickets — if a sprint ticket isn't on the board, flag it.
- If Next Actions is empty or stale, suggest pulling from Sprint Backlog, sprint tickets, Inbox, or Parked.
- Ask: "Does this look right, or should we adjust priorities?"

**Waiting/Blocked:**
- Show board "Waiting" items and how long each has been waiting (from `added` date).
- Cross-reference with `jira-pending blocked` if relevant.
- Items waiting >7 days: suggest escalation.

**Sprint backlog** (from board):
- Show the "Sprint Backlog" section — committed sprint work not yet in Next Actions.

**Inbox check:**
- If there are untriaged items: "You have N items in Inbox to triage."

**Parked (optional):**
- Mention count or highlights only if relevant to the day.

### 3. Update the board

If the user adjusts priorities or moves items, update `user/BOARD.md` accordingly.
