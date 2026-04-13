---
last_accessed: YYYY-MM-DD
access_count: 0
created: YYYY-MM-DD
---

# Skill: Daily consolidation

## When to use

Triggered by the `/daily` command — either by the user manually or by the
automated cron job (daily at 23:50). This is the "sleep" cycle — where the
system consolidates the day's work and learns from it.

**Autonomous mode (cron):** All steps run without user interaction. Act with
judgment; log all decisions and changes made. No approval gates — the
maintenance cycles and git history provide the correction mechanism.

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

Add a link **only if it serves the reader of that file** — if following it
would genuinely amplify, deepen, or contextualize what they're reading.
Don't add links to establish bidirectional relationships between files.
Each link must answer: "Why would someone reading *this* file want to go
*there*?"

```markdown
> Related: [other-file](path/to/other-file.md) — brief explanation of
> what is on the other side and how it extends the current topic.
```

A well-connected concept doesn't need explicit backlinks to be important.
If it genuinely amplifies many topics, many files will link to it naturally
— creating implicit connectivity through use, not through enforced
bidirectionality.

When you create or significantly extend a **concept or project file**, ask
for each potential link:

- "Does this file build on, clarify, or exemplify the other one?"
- "Would a reader of *that* file benefit from knowing about *this* one?"

Add every link where both answers are yes. Don't cap the number — if there
are five genuine functional connections, create five links. The quality
criterion is the only filter. Don't force connections either; if nothing
connects naturally today, skip this step.

#### 6. Act on mature observations

Read `agent_brain/observations.md`. For each observation with **2 or more
occurrences** (seen across different conversations or days):

**Skill candidates (seen 2+):**
1. Create the skill in `agent_brain/skills/verb-object.md`.
2. Include: frontmatter, "When to use" with clear triggers, "Procedure"
   with numbered steps. For each step, include its **purpose** when not
   obvious — an agent that understands WHY a step exists can adapt when the
   exact procedure doesn't fit. Distinguish fixed steps (must always happen)
   from judgment calls (adapt based on context).
3. Add it to the Skills section of AGENTS.md with a trigger description.
4. Mark the observation as resolved in the journal.

**Rule candidates (seen 2+):**
1. Evaluate where it belongs:
   - Universal trait describing who the agent IS → add to SOUL.md Character.
   - Contextual operational rule → add to AGENTS.md Rules, with WHY.
   - If unclear, default to AGENTS.md — it can be promoted later.
2. Formulate the rule with its reasoning: `[rule]. [why — what it prevents,
   enables, or protects]`.
3. Add to the appropriate file. Mark the observation as resolved. Log the
   decision and reasoning.

**Concept candidates (seen 2+):**
1. Create the concept file if not already created in step 4 above.
2. Mark the observation as resolved in the journal.

**Structure candidates (seen 2+):**
1. Create the new directory, move relevant files, update "Where to find
   things" in AGENTS.md. Log the change.
2. Mark the observation as resolved.

Observations with only 1 occurrence stay in the journal — they need more
data before acting.

#### 7. Update Active context

Active context has two subsections: **Right now** (ephemeral state) and
**Files** (pointers to semantic memory).

**### Right now** — current state the agent should know at every session
start, without opening any file. Volatile facts that change every few days:

- Current situation (vacation, sick, deadline week, travel)
- Most immediate next actions (1-3 items, with dates if known)
- Health or personal context affecting daily activity
- Constraints or blockers

Keep it to 3-5 bullet points. This is the scratchpad of working memory —
not a task list, not a log. Replace the full contents each time; don't
append.

**### Files** — pointers to brain files worth keeping in the agent's
peripheral awareness. Updated based on today's activity:

Promotion and demotion are **gradual** — one level at a time, not jumps.
The visibility levels are:

| Level | Where | Signal to promote |
|---|---|---|
| 0 | File in subdirectory, basic one-liner in its `index.md` | default state |
| 1 | Prominent in its `index.md` (richer description, moved higher) | used this week |
| 2 | Parent directory's `index.md` highlights the subdir/project | used across weeks |
| 3 | "Where to find things" gets a specific entry with trigger | sustained high use |
| 4 | Active context "Files" | hot — needed in most sessions |

Steps:

1. Scan files in `agent_brain/` (excluding `identity/`, `skills/`, `archive/`).
2. Read metadata (`access_count`, `last_accessed`). Identify files whose
   access has grown since last `/daily`.
3. For each growing file, **promote one level** — not to Active context
   directly. A file accessed once today becomes more prominent in its
   subdir index. A file accessed repeatedly across sessions over multiple
   days earns a higher level. Only files at level 3 that continue to be
   accessed in most sessions graduate to Active context (level 4).
4. For each file in Active context whose `access_count` hasn't grown →
   **demote one level** (to "Where to find things" or back to its index).
   Don't remove from the system — just move it one step further from
   working memory. Gradual cooling, not deletion.
5. Skip files linked from `USER.md` as structural context (team, primary
   project) — they're always accessible through identity, not subject to
   Hebbian dynamics.
6. Keep Active context "Files" at 5-7 entries.

Each file entry has two layers — **hot data** inline and a **read trigger**:

```
- [Short name](path/to/file.md) — key fact or core principle (useful
  without opening the file). Read when [clear trigger for when to open it].
```

Examples:
- `[Wedding](path) — July 10 2026. Read when wedding tasks come up.`
- `[Project X](path) — blocked on API approval. Read when discussing project X or planning sprints.`

Avoid: accumulated history, internal scores, operational detail that only
matters during maintenance.

---

### Finalize

#### 8. Git commit

```bash
git add AGENTS.md agent_brain/ logs/ user/ && git commit -m "daily: YYYY-MM-DD" 2>/dev/null || true
```
