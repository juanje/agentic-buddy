---
last_accessed: YYYY-MM-DD
access_count: 0
created: YYYY-MM-DD
---

# Skill: Daily consolidation

## When to use

Triggered by the user via the `/daily` command, typically at the end of the
day or start of the next. This is the "sleep" cycle — where the system
consolidates the day's work and learns from it.

## Procedure

---

### Step 0: Reflect first

Before consolidating, always process the current conversation:

1. Read `agent_brain/skills/process-conversation.md` and execute it.
   This captures the current conversation into today's log and detects
   observations — even if the user already ran `/reflect` earlier.
   The reflect skill appends without duplicating, so running it twice
   is safe.

This ensures no conversation context is lost, even if the user forgot
to `/reflect` during the day.

---

The daily consolidation has two parts: first consolidate (summarize and
organize the day), then learn (create knowledge, form connections, act on
mature observations).

---

### Part 1: Consolidate

#### 1. Replay the day

Read `logs/YYYY-MM-DD.md` (today's date). The log now contains the reflect
pass from Step 0, plus any earlier `/reflect` passes from other
conversations today. Read it as a whole — understand the day's arc, not
isolated conversations.

If no log exists for today, check yesterday's. If neither exists, note it
and skip to Part 2 (the observation journal may still have actionable items).

#### 2. Day summary

Add a summary section at the top of the daily log (after the frontmatter),
or update it if one already exists:

```markdown
## Day summary
- **Key themes:** [2-3 main topics or threads of the day]
- **Moved forward:** [what progressed]
- **Learned:** [new knowledge acquired, if any]
- **Open:** [unresolved threads to pick up tomorrow]
```

Keep it brief — this makes the weekly review's job easier.

#### 3. Review user workspace

If `user/` has content, do a quick check:
- Any items that need attention or follow-up?
- Any completed items that should be noted?
- Don't do a full review — that's for `/weekly` and `/monthly`.

If `user/` is empty, skip this step.

---

### Part 2: Learn

#### 4. Create new concepts

Review the day's log (especially the Lessons, Decisions, and System
observations sections). Look for knowledge worth retaining:

- Patterns that apply beyond the specific situation discussed.
- Lessons that would be useful if the same situation arises again.
- Principles or heuristics the user articulated.

For each, check if it's already captured in `agent_brain/concepts/` or
`agent_brain/projects/`. If not, create a new file:

```
agent_brain/concepts/short-descriptive-name.md
```

With standard frontmatter and enough context to be useful without the
original conversation. Link to the daily log as source.

#### 5. Form associations

Look for connections between today's work and existing brain files:

- Does a concept discussed today relate to an existing concept?
- Did a project decision connect to a known pattern?
- Is there a link between an idea and a lesson learned?

For each meaningful connection, add cross-references to **both** files:

```markdown
> Related: [other-file](path/to/other-file.md) — brief explanation of
> how they connect.
```

These associations are the "synapses" of the system. They strengthen with
use across days and help surface relevant context in future sessions.

Don't force connections. If nothing connects naturally today, skip this step.

#### 6. Act on mature observations

Read `agent_brain/observations.md`. For each observation with **2 or more
occurrences** (seen across different conversations or days):

**Skill candidates (seen 2+):**
1. Create the skill in `agent_brain/skills/verb-object.md`.
2. Include: frontmatter, "When to use" with clear triggers, "Procedure"
   with numbered steps.
3. Add it to the Skills section of AGENTS.md with a trigger description.
4. Mark the observation as resolved in the journal.

**Rule candidates (seen 2+):**
1. Present the proposed rule to the user for approval.
2. If approved: add it to the Rules section of AGENTS.md.
3. Mark the observation as resolved in the journal.
4. If not approved: leave it in the journal, note the rejection.

**Concept candidates (seen 2+):**
1. Create the concept file if not already created in step 4 above.
2. Mark the observation as resolved in the journal.

**Structure candidates (seen 2+):**
1. Propose the new directory to the user.
2. If approved: create it, move relevant files, update "Where to find
   things" in AGENTS.md.
3. Mark the observation as resolved.

Observations with only 1 occurrence stay in the journal — they need more
data before acting.

#### 7. Update Active context (initial promotion)

Update the "Active context" section of AGENTS.md based on today's activity:

1. Scan files in `agent_brain/` (excluding `identity/`, `skills/`, `archive/`).
2. Calculate score: `score = access_count × recency_factor`
   - recency_factor: 1.0 (today), 0.9 (yesterday), 0.7 (this week),
     0.4 (this month), 0.1 (older).
3. Top 5-7 files by score get linked in "Active context".
4. Remove links whose files are no longer in the top scores.

Link format:
```
- [Brief description](path/to/file.md) — why it's relevant right now
```

This makes newly important files immediately visible in the next session.

---

### Finalize

#### 8. Git commit

```bash
git add AGENTS.md agent_brain/ logs/ user/ && git commit -m "daily: YYYY-MM-DD" 2>/dev/null || true
```
