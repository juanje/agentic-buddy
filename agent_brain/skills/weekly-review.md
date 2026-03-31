---
last_accessed: YYYY-MM-DD
access_count: 0
created: YYYY-MM-DD
---

# Skill: Weekly review

## When to use

Use when the user says "weekly review", "what did I do this week", "end of week",
or for broader reviews ("what have I done this quarter", "review for my manager").

## Procedure

### 0. Check prerequisite cycles

Before starting the weekly review:

1. **Reflect:** Run the reflect procedure first (read and execute
   `agent_brain/skills/process-conversation.md`) to capture the current
   conversation.
2. **Daily:** Check if `/daily` was run in the last 2 days. Look for a
   "Day summary" section in recent logs. If `/daily` hasn't been run
   recently, inform the user: "Daily consolidation hasn't been run in
   the last couple of days. I'll run a quick consolidation now to make
   sure this review has complete data." Then execute the daily
   consolidation procedure (skip Step 0 since reflect was already done
   above).

### 1. Gather data

- Read logs from `logs/` for the current week.
- Read `user/` to understand current state of the user's workspace.

### 2. Present the weekly summary

**Completed this week:**
- Items completed or resolved, based on logs and `user/` content.

**Still in progress:**
- Ongoing items. On track or at risk?

**Waiting/Blocked:**
- Anything the user is waiting on.

**Decisions and context** (from logs):
- Key decisions made and their reasoning.
- Lessons learned.

**Unplanned work:**
- Things that came up during the week that weren't planned.

### 3. Review user workspace

Walk through `user/` content:
- Any completed items that can be archived or removed?
- Any stale items that need attention?
- Is the structure still serving the user well, or does it need adjustment?
- Any items that should be prioritized for next week?

### 3b. Review ideas

- Read `agent_brain/ideas/_scratchpad.md` — any items worth promoting to their own file?
- Scan idea files in `agent_brain/ideas/`:
  - `seed` ideas: still interesting? Promote to `developing` or archive.
  - `developing` ideas: any progress this week? Anything to add from the week's context?
  - `ready` ideas: should any be converted this week? (create project, start task, etc.)
- Present a brief ideas summary to the user alongside the workspace review.

### 3c. Link hygiene (weekly pass)

As you scan concepts and projects this week, look for **missed links**:

- New files that clearly **extend, clarify, or provide examples** for older ones but are not
  linked yet.
- Older files that mention concepts now fleshed out elsewhere.

When you spot a gap, add links in **both directions** with a short explanation of what is
on the other side and why to go there (general pattern, deeper explanation, source, etc.).
Prioritize a few high-value links over exhaustive linking.

### 4. Calibrate promotions (Hebbian)

Review the "Active context" section of AGENTS.md against actual usage this
week. The goal is to check whether daily promotions held up over time.

1. For each file linked in Active context, check its `access_count` and
   `last_accessed` metadata.
2. **Reinforce:** files accessed repeatedly across different days this week →
   keep in Active context. Update the hot data and read trigger if the
   file's role has become clearer during the week.
3. **Weaken:** files promoted during a daily consolidation but barely touched
   since → remove from Active context. The initial connection didn't hold —
   it was a one-day spike, not sustained relevance.
4. **New promotions:** scan brain files for any that were heavily used this
   week but aren't in Active context yet → add them.

Each file entry should have **hot data** (key fact useful without opening
the file) and a **read trigger** (when the agent should open it).

Also update the **Right now** subsection with current state (situation,
next actions, health, constraints). See the daily skill Step 7 for format
and full guidance on both subsections.

Present the changes: "Promoted: [X], Removed: [Y], Kept: [Z]."

### 5. Calibrate learned skills and rules

Review **learned** skills and rules (created by the agent during `/daily`,
not core system skills) that were created or modified this week:

- **Used and referenced** this week → keep as-is, or adjust if usage revealed
  issues with triggers or procedure.
- **Not used at all** since creation → flag. The trigger description may be
  too vague, or the skill may have been premature. Don't remove yet — give
  it another week. The monthly cycle handles archiving after longer disuse.

### 6. Generalize

Look across the week's specific concepts, skills, and brain files for patterns
that can be abstracted into general knowledge.

1. Scan `agent_brain/concepts/` and `agent_brain/projects/` for files that
   share a common theme or pattern.
2. If 2-3+ specific items (A, B, C) are related and share an underlying
   principle:
   - Create a general concept file (AA) that captures the shared pattern.
   - In AA, explain the general principle and link to the specific instances:
     ```markdown
     ## Specific instances
     - [A](path/to/A.md) — how A relates to this pattern
     - [B](path/to/B.md) — how B relates to this pattern
     - [C](path/to/C.md) — how C relates to this pattern
     ```
   - In each specific file (A, B, C), add a back-reference:
     ```markdown
     > General pattern: [AA](path/to/AA.md) — the broader principle
     ```
   - If AA is heavily relevant right now, add it to Active context in
     AGENTS.md. The general version is more broadly useful than any
     specific instance.
3. Do the same for skills: if skills X and Y follow a similar procedure for
   different domains, consider a general skill that covers both.
4. Present generalizations to the user for approval before creating.

Don't force generalizations. If nothing connects naturally across the week,
skip this step. Generalization emerges from accumulated data, not from a
single week.

5. **Structural clustering** (applies to all brain structures, not just
   concepts): scan directories for files sharing a prefix or referencing
   each other heavily. If 3+ files form a cluster → propose consolidation
   into a subdirectory with an `index.md` hub. See Core Behavior rule 6.

### 7. Light pruning (flag only)

Scan brain files for staleness signals:
- Files not accessed in >21 days → flag them in a note to the user. Don't
  move them — that's the monthly cycle's job.
- If any flagged files are in Active context → remove them from Active
  context (they shouldn't be there if untouched for 3 weeks).

### 8. Prepare next week

- Ask: "What should be your top priorities next week?"
- Suggest items based on current `user/` content, recent logs, and patterns.

### 9. Git commit

```bash
git add AGENTS.md agent_brain/ logs/ user/ && git commit -m "weekly: YYYY-WNN" 2>/dev/null || true
```

### 10. Broader review mode

If the user asks for a monthly or quarterly review:

- Scan review files in `agent_brain/reviews/` for the period (if the directory exists).
- Scan logs in `logs/` for the period.
- Group by project or theme.
- Highlight: major deliverables, contributions, problems solved, skills developed.
- Present in a format suitable for sharing or personal reflection.
