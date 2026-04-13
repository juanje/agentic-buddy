---
last_accessed: YYYY-MM-DD
access_count: 0
created: YYYY-MM-DD
---

# Skill: Monthly maintenance

## When to use

Triggered by the `/monthly` command — either by the user manually or by the
automated cron job (1st of each month at 00:01). This is the deepest
maintenance cycle — focused on forgetting what's abandoned, deep generalization
across the full knowledge base, and structural cleanup.

**Autonomous mode (cron):** All phases run without user interaction. Act with
judgment; log all decisions and changes made. No approval gates — the git
history and observation journal provide the correction mechanism.

Lighter maintenance happens at other levels:
- `/daily` — concept creation, associations, initial promotion, skill/rule
  creation from mature observations.
- `/weekly` — Hebbian calibration of promotions, generalization across the
  week, light pruning flags.

This cycle handles what only makes sense at monthly scale.

## Phases

### Phase 0: Check prerequisite cycles

Before deep maintenance, ensure lower-level cycles are current:

1. **Reflect:** Run the reflect procedure first (read and execute
   `agent_brain/skills/process-conversation.md`).
2. **Weekly:** Check if `/weekly` was run in the last 10 days. Look for a
   recent weekly log. If not, run the weekly review procedure first (which
   will cascade into daily/reflect as needed) to ensure the monthly has
   complete data. Log that a weekly was run as prerequisite.

---

Execute remaining phases in order. Each phase is independent: if one
fails, log the error and continue with the next.

---

### Phase 1: Log compaction

**Goal:** Keep `logs/` manageable while preserving valuable context.

1. List files in `logs/` older than 30 days (exclude maintenance logs).
2. For each old log:
   - Check if its key content (decisions, lessons) has been extracted to
     `agent_brain/`.
   - If fully extracted: move to `logs/archive/`.
   - If it contains unextracted knowledge: extract it to the appropriate
     `agent_brain/` location first, then archive the log.
3. Never delete logs outright — always archive.
4. Record what was compacted.

---

### Phase 2: Full pruning (archive)

**Goal:** Move truly abandoned information out of the active space. This is
the "forgetting" that the weekly cycle only flags.

1. Scan all files in `agent_brain/` subdirectories (excluding `identity/`,
   `skills/`, and `archive/`).
2. Read their metadata (`last_accessed`, `access_count`).
3. If a file hasn't been accessed in >30 days AND has fewer than 5 total
   accesses:
   - Move it to `agent_brain/archive/`.
   - If it was linked in Active context of AGENTS.md, remove the link.
   - If other files reference it, update cross-references to point to the
     archive location.
   - Record the move.
4. If a file hasn't been accessed in >30 days BUT has >5 accesses:
   - Don't move it. Flag it as a review candidate in the maintenance log.
     It was important once — the user should decide.

**Exception:** Never move or prune files in `agent_brain/identity/`,
`agent_brain/skills/`, or `user/`. Those require human decision.

**Why archive, not delete:** Archive keeps files indexable by the editor — a
search can still surface them even when the agent doesn't remember they exist
(passive recognition). Deletion removes them from the workspace entirely;
only git history preserves them, and that requires knowing the file existed
(active recall). Prefer archiving over deletion.

---

### Phase 3: Prune unused learned skills and rules

**Goal:** Review skills and rules that were created by the agent through use,
and weaken or archive those that haven't been confirmed by continued use.

Skills fall into two categories:

**Core skills** (never pruned — they are the system's architecture):
`process-conversation.md`, `daily-consolidation.md`, `weekly-review.md`,
`monthly-maintenance.md`.

**Learned skills** (subject to Hebbian pruning — everything else):
Skills created by the agent during `/daily` consolidation based on
observed patterns. These earned their place through repeated use, and
they keep it the same way.

**Procedure:**

1. Review all learned skills in `agent_brain/skills/` (skip core skills).
2. For each learned skill, check if it was referenced or triggered in the
   last month's logs.
   - Referenced and used → keep.
   - Not referenced but less than 1 month old → keep (still new).
   - Not referenced and 1-3 months old → **archive**. Move to
     `agent_brain/archive/`, remove from Skills section of AGENTS.md.
     If the skill is plausibly seasonal (e.g., sprint planning, quarterly
     releases), add a `seasonal: true` note in its frontmatter and keep it
     in archive — retrievable when the season comes. Log the decision.
   - Archived and not retrieved in >3 months → can be deleted. Git
     history preserves it if ever needed again.
3. Review rules in AGENTS.md: any added by the agent (not original rules)
   that seem to conflict with observed behavior or are consistently
   ignored?
   - Log them as candidates for review. Flag in the monthly maintenance log.
4. **Promote mature rules to character.** Review rules in AGENTS.md that have
   been consistently active for 3+ months. If a rule applies universally, has
   never been questioned, and describes who the agent IS rather than what it
   should DO — promote to SOUL.md as a character trait, rewritten in identity
   language. Remove from AGENTS.md Rules. Log the promotion.

---

### Phase 4: Deep generalization

**Goal:** Find patterns across the full knowledge base that haven't been
caught by weekly generalization. This operates at a broader scale — looking
across weeks and months of accumulated knowledge.

1. Scan all concept files in `agent_brain/concepts/`.
2. Look for clusters of related concepts that share an underlying principle
   but haven't been linked or generalized yet.
3. If 2-3+ specific concepts (A, B, C) share a pattern:
   - Create a general concept file (AA) that captures the shared principle.
   - In AA, link to the specific instances with explanations:
     ```markdown
     ## Specific instances
     - [A](path/to/A.md) — how A relates
     - [B](path/to/B.md) — how B relates
     - [C](path/to/C.md) — how C relates
     ```
   - For each specific file (A, B, C), consider whether a link to the
     general pattern (AA) would **serve the reader** of that file — i.e.,
     genuinely deepen their understanding of the specific concept. Add it
     only if it does; don't add back-references for graph completeness.
   - If the general concept is broadly useful, add it to Active context.
4. Do the same for skills: if multiple skills follow a similar pattern for
   different domains, consider creating a general skill that covers the
   common procedure, referencing the specific skills for domain details.
5. Check existing generalizations: are they still accurate? Do they need
   updating based on new specific instances?
6. Apply the same generalization logic to **all brain structures** — not
   just concepts. Projects, teams, and any other directories can also
   contain related files that share an underlying pattern.
7. Create generalizations with judgment. Log the reasoning and what was created.
8. **Consider form.** Generalizations that guide decisions should be written
   as frameworks (when to apply, how to decide), not just descriptions.
   Knowledge describes; attractors guide.

---

### Phase 5: Ideas review

**Goal:** Keep `agent_brain/ideas/` healthy.

1. Read `agent_brain/ideas/_scratchpad.md`.
   - Any item older than 7 days? Flag it: promote to its own file or remove.
2. Scan all idea files in `agent_brain/ideas/` (excluding `_scratchpad.md`).
3. For each idea:
   - `seed` not accessed in >14 days → flag as stale.
   - `developing` not accessed in >21 days → flag as stuck.
   - `ready` not accessed in >7 days → flag for action.
   - `converted` or `archived` older than 30 days → move to
     `agent_brain/archive/`.
4. Record findings.

---

### Phase 6: Contradiction detection

**Goal:** Maintain coherence in the knowledge base. Contradictions erode trust
in memory — if the agent finds conflicting information, it can't know which to
use, weakening the "Memory first" principle.

1. Scan concept and project files for contradictions: information in one
   file that conflicts with information in another.
2. Check recent logs (last month) for information that contradicts existing
   brain files.
3. For each contradiction:
   - Clear contradiction + reliable new info → update the old file.
   - Ambiguous → add a note:
     ```
     > ⚠️ CONTRADICTION (YYYY-MM-DD): [description]. Pending human review.
     ```
4. Record contradictions found and how they were resolved.

---

### Phase 7: Structure review

**Goal:** Ensure `agent_brain/` structure matches how the system is actually
used. The directory structure should emerge from use, not from upfront design.

1. Review structure candidates in `agent_brain/observations.md`.
2. Scan files in `agent_brain/` — are there files that don't fit their
   current directory?
3. **Cluster detection** (applies to ALL directories — projects, concepts,
   etc.): scan for files sharing a common prefix or with heavy mutual
   cross-references. If 3+ files form a cluster within the same directory:
   - Create the subdirectory with an `index.md` hub; move the files; update
     all cross-references (AGENTS.md, other brain files, etc.) and "Where to
     find things." Log what was moved and why.
   - See Core Behavior rule 6.
4. If a new category has accumulated (3+ files of a similar type in an
   ill-fitting directory):
   - Create the dedicated directory, move the files, update "Where to find
     things" in AGENTS.md. Log the change.
5. Check existing directories: any empty or with only 1 file after >30 days?
   - The directory may be premature. Flag it.
6. **Index coverage:** check directories with 3+ files and no `index.md` —
   flag and propose creation. Indexes enable progressive disclosure: the
   agent reads the map before diving in. See Rule 2.
7. Record structural changes and proposals.

---

### Phase 7b: Identity file curation

Review `agent_brain/identity/` files:

1. Check `USER.md` for stale facts, redundancy, or excessive growth.
   Update observed facts from the month's logs. Remove outdated information.
2. If extensions exist (`background.md`, `health.md`, etc.), verify links
   from `USER.md` are accurate and load conditions still make sense.
3. Compact where possible — identity files should be reference material,
   not accumulated history.

### Phase 8: Clear resolved observations

**Goal:** Keep the observation journal clean.

1. Read `agent_brain/observations.md`.
2. Move all entries in the "Resolved" section that are older than 30 days
   out of the file (they've served their purpose).
3. Check remaining unresolved observations: any older than 60 days with
   only 1 occurrence? They're probably noise — remove them.

---

### Finalize

1. Create `logs/monthly_YYYY-MM-DD.md`:

```markdown
# Monthly maintenance — YYYY-MM-DD

## Compaction
- Logs archived: [list or "none"]
- Knowledge extracted: [list or "none"]

## Pruning
- Files archived: [list or "none"]
- Review candidates (high access, old): [list or "none"]

## Skills and rules pruned
- Skills removed: [list or "none"]
- Skills flagged: [list or "none"]
- Rules flagged: [list or "none"]

## Generalization
- General concepts created: [list or "none"]
- General skills created: [list or "none"]
- Existing generalizations updated: [list or "none"]

## Ideas
- Scratchpad items flagged: [list or "none"]
- Stale/stuck ideas flagged: [list or "none"]
- Ideas archived: [list or "none"]

## Contradictions
- Detected: [list or "none"]
- Resolved: [list or "none"]
- Pending human review: [list or "none"]

## Structure
- Directories created: [list or "none"]
- Files moved: [list or "none"]
- Proposals pending approval: [list or "none"]

## Observations cleaned
- Resolved entries cleared: [count]
- Stale entries removed: [count]
```

2. Git commit:

```bash
git add AGENTS.md agent_brain/ logs/ user/ && git commit -m "monthly: YYYY-MM-DD" 2>/dev/null || true
```
