---
last_accessed: YYYY-MM-DD
access_count: 0
created: YYYY-MM-DD
---

# Skill: Weekly review

## When to use

Triggered by the `/weekly` command — either by the user manually or by the
auto-consolidate hook (after 7 completed dailies since last weekly).
Also triggered when the user says "weekly review", "what did I do this week",
"end of week", or for broader reviews ("what have I done this quarter",
"review for my manager").

**Autonomous mode (hooks):** All steps run without user interaction. Steps
that ask the user (e.g., "prepare upcoming priorities") are skipped —
priorities are inferred from workspace state and recent activity. Log all
decisions and changes made. No approval gates — the maintenance cycles
and git history provide the correction mechanism.

## Procedure

### 0. Check prerequisite cycles

Before starting the weekly review:

1. **Reflect:** Run the reflect procedure first (read and execute
   `agent_brain/skills/process-conversation.md`) to capture the current
   conversation.
2. **Daily:** Check if `/daily` was run in the last 2 days. Look for a
   "Day summary" section in recent logs. If `/daily` hasn't been run
   recently, execute the daily consolidation procedure (skip Step 0
   since reflect was already done above). Log that a daily was triggered
   as prerequisite.

### 1. Gather data

- Read `logs/index.md` to identify active sessions since the last weekly
  review (check `user/journal/` for the most recent weekly file to
  determine the boundary; if none exists, use the last 7 active sessions).
- Read the corresponding daily logs from `logs/`.
- Read `user/` to understand current state of the user's workspace.

### 2. Compile the weekly summary

Write the following summary to today's log (under a `## Weekly summary`
section). In interactive mode, also present it to the user. In autonomous
mode, the log entry is the output.

**Completed since last weekly:**
- Items completed or resolved, based on logs and `user/` content.

**Still in progress:**
- Ongoing items. On track or at risk?

**Waiting/Blocked:**
- Anything the user is waiting on.

**Decisions and context** (from logs):
- Key decisions made and their reasoning.
- Lessons learned.

**Unplanned work:**
- Things that came up during the period since last weekly that weren't planned.

### 3. Review user workspace

Walk through `user/` content:
- Any completed items that can be archived or removed?
- Any stale items that need attention?
- Is the structure still serving the user well, or does it need adjustment?
- Any items that should be prioritized for the upcoming period?

### 3b. Review ideas

- Read `agent_brain/ideas/_scratchpad.md` — any items worth promoting to their own file?
- Scan idea files in `agent_brain/ideas/`:
  - `seed` ideas: still interesting? Promote to `developing` or archive.
  - `developing` ideas: any progress since last weekly? Anything to add from recent context?
  - `ready` ideas: should any be converted now? (create project, start task, etc.)
- Act on what's clear; log decisions made (promotions, status changes, archives).

### 3c. Link hygiene (weekly pass)

As you scan concepts and projects since last weekly, look for **missed functional
links** — places where a reader would genuinely benefit from a pointer to
another file:

- New files that **extend, clarify, or provide examples** for older ones but
  are not linked yet — and where the reader of the older file would benefit
  from knowing about the new one.
- Older files that mention concepts now fleshed out elsewhere — where a link
  would help the reader navigate to deeper content.

Add a link only if it serves the reader of that specific file. Don't add
links to maintain bidirectional relationships — a concept's importance is
shown by how many files naturally link to it through use, not by enforced
backlinks. Don't cap the number of links; every genuinely functional link
should exist.

### 4. Calibrate promotions (Hebbian)

Review visibility levels across the full knowledge base. The weekly cycle
looks at the whole gradient, not just Active context. Promotion and demotion
are gradual — one level at a time (see daily-consolidation Step 7 for the
level table).

1. **Active context (level 4):** for each file, check `access_count` growth
   since last weekly.
   - Grew across multiple days → **reinforce** (keep, enrich description).
   - Didn't grow → **demote one level**: move to "Where to find things"
     (level 3) if the file still has periodic relevance, or back to its
     directory index (level 1-2) if the spike is clearly over.
2. **"Where to find things" (level 3):** check entries that were added
   beyond the base set (user workspace, projects, concepts, ideas, journal,
   observations are base). Any added entry whose underlying files haven't
   been accessed since last weekly → demote back to directory index (level 1-2).
3. **Directory indexes (level 1-2):** scan `index.md` files for entries
   whose underlying file hasn't been accessed in >21 days → flag for
   potential demotion within the index. Don't act automatically — flag.
4. **New promotions:** scan files accessed repeatedly across different days
   since last weekly. Promote **one level up** from current position, not directly
   to Active context. Only files already at level 3 that continue to be
   accessed in most sessions graduate to level 4.
5. **Missing indexes:** if a promoted file has no index pathway (standalone,
   no parent `index.md`) → flag the missing index as a structure candidate.

Also update the **Right now** subsection with current state. See the daily
skill Step 7 for format and full guidance on both subsections.

Log changes across all levels in today's log (Decisions section):
"Level 4: kept [X], demoted [Y]. Level 3: added [A], removed [B].
Level 1-2: enriched [C], flagged [D]." In interactive mode, also present
this to the user. If any demotion from Active context affects files the
user actively references, write to `agent_brain/deferred.md`:
`- **info** (YYYY-MM-DD, weekly): [description].`

### 4b. Identity file check

If `agent_brain/identity/USER.md` has grown significantly (rough threshold:
80+ lines of content), consider splitting detailed sections into separate
files under `agent_brain/identity/` (e.g., `background.md`, `health.md`).
Keep `USER.md` lean — identity, current context, and preferences. Each
extension should have explicit load conditions at the top:
`Load when discussing [topic]`. Link from `USER.md` with:
`[Label](filename.md) — load when [trigger]`.

Also check `USER.md` for new facts from recent logs (since last weekly) that should be
added (new projects, changes in routine, people mentioned, context shifts).

**Episodic entries:** For time-bounded situations (illness, injury, travel,
temporary care load), collapse the accumulated day-by-day history to a
single summary line once the episode is clearly resolved or stable. Format:
`[Topic] (dates): [one-sentence outcome]. Detail in journal.`
The day-by-day detail lives in the journal entries — `USER.md` only needs
the current state and a pointer. Don't wait for the file to grow large;
collapse when the episode closes.

**Extension file candidates (people, domains):** When a person or topic
appears repeatedly across conversations and requires structured background
context beyond a one-liner, consider creating an extension file under
`agent_brain/identity/` (e.g., `background.md`, `health.md`, `family.md`,
`work.md`). The criterion is not file size — it's whether there is enough
*stable, structured reference material* that an agent would genuinely need
when the topic appears. Three questions:
1. Is there a clear load trigger? ("when discussing X in depth")
2. Is the content reference material (stable facts, dynamics, history) —
   not episodic history that belongs in the journal?
3. Does it appear in multiple conversations, making the file worth
   maintaining?

If yes to all three, track candidates in `agent_brain/observations.md`
under "Structure candidates" until they mature. When a candidate is ready,
execute the split autonomously: create the extension file, compress the
source entry in USER.md to a one-line summary + link. Log the decision in
today's log. Structural splits are internal organization — they don't
require user approval. Guideline: ~1 line for people not present in
most conversations, ~3 lines max for frequently present people (partner,
immediate family). The goal is to minimize session-start token cost while
preserving navigability.

### 5. Calibrate learned skills and rules

Review **learned** skills and rules (created by the agent during `/daily`,
not core system skills) that were created or modified since last weekly:

- **Used and referenced** since last weekly → keep as-is, or adjust if usage revealed
  issues with triggers or procedure.
- **Not used at all** since creation → flag. The trigger description may be
  too vague, or the skill may have been premature. Don't remove yet — give
  it another week. Premature pruning loses the signal; the monthly cycle
  handles archiving after longer disuse.

### 6. Generalize

Look across concepts, skills, and brain files since last weekly for patterns
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
   - For each specific file (A, B, C), consider whether a link to the
     general pattern (AA) would **serve the reader** of that file. Add it
     only if knowing about the broader principle genuinely deepens the
     reader's understanding of the specific concept. Don't add back-
     references just for graph completeness.
   - If AA is heavily relevant right now, add it to Active context in
     CLAUDE.md. The general version is more broadly useful than any
     specific instance.
3. Do the same for skills: if skills X and Y follow a similar procedure for
   different domains, consider a general skill that covers both.
4. Create generalizations with judgment. Log the reasoning and what was created.
5. **Consider form, not just content.** Is the generalization actionable —
   does it guide future decisions? If so, write it as a framework: when to
   apply, how to decide, what to watch for. A concept that only describes a
   pattern is knowledge; a concept that guides judgment is an attractor.

Don't force generalizations. If nothing connects naturally since last weekly,
skip this step. Generalization emerges from accumulated data, not from a
single review period.

5. **Structural clustering** (applies to all brain structures, not just
   concepts): scan directories for files sharing a prefix or referencing
   each other heavily. If 3+ files form a cluster → propose consolidation
   into a subdirectory with an `index.md` hub. See Core Behavior rule 6.

### 7. Light pruning (flag only)

Scan brain files for staleness signals:
- Files not accessed in >21 days → log them in the weekly maintenance note.
  Don't move them — that's the monthly cycle's job.
- If any flagged files are in Active context → demote one level per the
  gradient (Step 4). Files untouched for 3 weeks shouldn't be at level 4.

### 8. Write weekly summary to journal

Write a summary of the week to `user/journal/weekly/YYYY-WNN.md` (create the
file). This is a user artifact for future reference — not a log, not agent
memory. Include:

- What was completed, key decisions, metrics if available
- Themes and patterns from the week
- Top 3-5 priorities for the upcoming period (based on urgency, dependencies, open
  threads)

### 9. Git commit

```bash
git add CLAUDE.md agent_brain/ logs/ user/ && git commit -m "weekly: YYYY-WNN" 2>/dev/null || true
```

### 10. Broader review mode

If the user asks for a monthly or quarterly review:

- Scan journal files in `user/journal/` for the period (weekly, monthly as needed).
- Scan logs in `logs/` for the period.
- Group by project or theme.
- Highlight: major deliverables, contributions, problems solved, skills developed.
- Present in a format suitable for sharing or personal reflection.
