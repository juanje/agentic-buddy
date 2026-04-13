---
last_accessed: YYYY-MM-DD
access_count: 0
created: YYYY-MM-DD
---

# Skill: Next task

## When to use

When the user says "next", "what's next", "what should I work on now", or runs the `/next` command.

## Procedure

### 1. Read the board

Read `user/BOARD.md` and extract the **Next Actions** list (immediate queue; max 3–4 items). Optionally mention **Sprint Backlog** as upcoming work after the Next Actions queue.

### 2. Identify the top task

The first item in Next Actions is the next task. Extract its ticket ID (if any).

### 3. Get task detail

If the task has a Jira ticket ID (e.g. PROJ-1234):
- Run `jira-detail <TICKET_ID>` to get description, status, comments, and links.

Also check `agent_brain/projects/` for any related project context that might help.

### 4. Present the output

Format the response as:

```
## Next up: <ticket or short title>

<Summary of what this task is about, the problem it solves, and any
relevant context from the issue tracker, board notes, or brain files.
Keep it concise but actionable — enough to start working immediately.>

### Acceptance criteria
<From issue tracker description if available>

### Queue
1. **<current>** ← you are here
2. <next item>
3. <next item>
...
```

### 5. Offer to start

Ask if the user wants to move the task to Doing. If Doing already has 2 items, remind them of WIP (AGENTS.md Rule 9) before adding another.
