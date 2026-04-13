---
last_accessed: YYYY-MM-DD
access_count: 0
created: YYYY-MM-DD
---

# Skill: Sync board

## When to use

Lightweight mid-day sync to keep the board and Active context current.
Use when the user says "sync", "refresh", "update board status", or runs `/sync`.
Can be run multiple times a day — designed to be fast (seconds, not minutes).

NOT a replacement for `/daily` (end-of-day consolidation and learning) or
`/monthly` (deep pruning, generalization, contradiction detection).

## Procedure

### 1. Gather current state

Run in parallel:
- Read `user/BOARD.md`.
- Run `jira-pending sprint` — current sprint ticket statuses.
- Run `jira-pending updated` — tickets updated recently.

If any tool is unavailable or fails, skip it and note it.

### 2. Cross-reference board with Jira

For each ticket in **Sprint Backlog**, **Next Actions**, **Doing**, and **Waiting**:
- Compare board status with Jira status.
- If a Jira ticket was resolved/closed but is still active on the board → flag it.
- If a Jira ticket changed status (e.g. New → In Progress) → flag it.
- If a ticket in Waiting has new comments → flag it (may be unblocked).

For **Inbox** items that reference Jira tickets:
- Check if the ticket was already created (some Inbox items are "create ticket" tasks).

### 3. Check for unblocked Waiting items

For each Waiting item:
- If it references an MR: check if the MR was merged (use `did today` filtered
  to the relevant source to avoid long queries).
- If it references a person's action: no automated check — just note how long it's
  been waiting.

### 4. Apply changes

- Move resolved items to Done with today's date.
- Update ticket statuses on the board if they changed in Jira.
- Add any new context discovered (new comments, status changes).
- Flag anything that needs the user's decision (don't auto-move ambiguous items).

### 5. Refresh Active context (AGENTS.md)

Update the Board line in the "Active context" section of AGENTS.md:
- Refresh item counts per section in **actionable order:** Doing, Next Actions, Waiting, Sprint Backlog, Inbox, Parked (count open items), Done.
- If **Doing** has more than **2** items, flag WIP exceeded (see AGENTS.md Rule 9).
- If **Next Actions** has more than 4 items, flag it (WIP limit is 3–4).
- Only update other Active context entries if files were created or heavily
  accessed since last sync.

### 6. Summary

Present a brief sync report:

```
## Sync — HH:MM

**Changes applied:**
- [list of moves/updates, or "none"]

**Flags (need your input):**
- [items needing decision, or "none"]

**Board state:** N Doing | N Next | N Waiting | N Sprint Backlog | N Inbox | N Parked | N Done
```

Don't create a log file — this is lightweight. Changes are tracked by git commits.

### 7. Git commit

```bash
git add user/BOARD.md AGENTS.md && git commit -m "sync: YYYY-MM-DD HH:MM" 2>/dev/null || true
```
