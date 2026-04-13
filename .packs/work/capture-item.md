---
last_accessed: YYYY-MM-DD
access_count: 0
created: YYYY-MM-DD
---

# Skill: Capture item

## When to use

Use for complex captures that need more thought than the quick capture described
in AGENTS.md Core Behavior. Examples: items that should go to multiple destinations,
batch processing from a meeting dump, or unclear classification.

For simple, obvious captures (a task → Inbox, an idea → Parked), the Core Behavior
in AGENTS.md is sufficient — don't read this skill for those.

## Procedure

### 1. Identify the item type

- **Task** (something to do) → `user/BOARD.md` Inbox
- **Bug or known error** → board Inbox + `agent_brain/concepts/` if it's a pattern worth documenting
- **Decision and its reasoning** → `agent_brain/projects/<project>.md` or `agent_brain/concepts/`
- **Meeting notes** → `agent_brain/projects/<project>.md` under the relevant project
- **Lesson learned** → `agent_brain/concepts/`
- **Improvement idea / tech debt** (concrete, actionable) → `user/BOARD.md` Parked
- **Unformed idea / project concept / draft proposal** → `agent_brain/ideas/YYYY-MM-DD_short-description.md` (or `_scratchpad.md` for one-liners)
- **Anything else** (cross-team requests, team notes, etc.) → create the appropriate directory inside `agent_brain/` if it doesn't exist, and capture there + board if actionable.

### 2. Capture with context

For board items, use the standard format. **Each distinct task or ticket is its own item** — never bury a second task under "Related" inside one line. Link with **Related to:** on both items (see AGENTS.md Board item format).

```
- [ ] Short description | added: YYYY-MM-DD
  - Context: why this matters, what it blocks, who asked, etc.
```

For `agent_brain/` files, create with frontmatter:

```yaml
---
last_accessed: YYYY-MM-DD
access_count: 1
created: YYYY-MM-DD
---
```

### 3. Confirm

Tell the user what was captured and where: "Captured [X] in [location]."

### 4. Prioritization

If the item seems urgent or high priority:
- Ask: "This seems important. Should it go to Next Actions, Sprint Backlog, or Doing?" If suggesting **Doing**, check WIP: target 1 task there, max 2 if related (AGENTS.md Rule 9).
- **Next Actions** holds at most 3–4 immediate items; **Sprint Backlog** holds triaged sprint work that is not yet "next."
- If it clearly blocks other work, suggest moving it up.
- If unclear, leave in Inbox for triage.
