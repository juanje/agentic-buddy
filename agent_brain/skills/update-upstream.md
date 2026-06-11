---
last_accessed: YYYY-MM-DD
access_count: 0
created: YYYY-MM-DD
---

# Skill: Update from upstream

## When to use

Triggered by `/update` or when the user says "update from upstream",
"sync with upstream", "check for upstream changes", or "pull latest
improvements".

## Context

This skill pulls improvements from the upstream agentic-buddy template
into a running instance. It applies changes intelligently — updating
system files (skills, commands, packs, rules) without touching user
content (identity, knowledge, logs, projects).

The upstream repo is https://github.com/juanje/agentic-buddy.

**Key structural note:** In the upstream repo, the operational CLAUDE.md
lives at `templates/CLAUDE.md`, not at the root. The root `CLAUDE.md`
is the setup redirect for fresh installations. Always compare against
`templates/CLAUDE.md`.

## Procedure

### 1. Clone upstream

Clone the full repo (not `--depth 1`) — the git history is essential
for understanding what changed and why:

```bash
git clone https://github.com/juanje/agentic-buddy.git /tmp/ab-upstream-$(date +%Y%m%d)
```

Store the path for the rest of the procedure.

### 2. Understand what changed (git log first, diffs second)

**This step is mandatory before any file comparison.** Without the
narrative of changes, diffs are uninterpretable — you see what's
different but can't tell direction, intent, or whether changes are
sweeping (rename, restructure) or incremental (bug fix, new feature).

1. Read the upstream git log since the last known sync:

   ```bash
   cd /tmp/ab-upstream-YYYYMMDD
   git log --oneline -20
   ```

   If you know the date of the last `/update`, limit to commits since
   then. Otherwise, read the last 20 commits — enough to spot the
   narrative.

2. **Identify structural changes first.** Look for commits that signal
   sweeping changes: renames (AGENTS.md → CLAUDE.md), new
   infrastructure (hooks, configs, new directories), removed files,
   or major refactors. These frame everything else — incremental
   changes to individual files only make sense after you understand
   the structural shifts.

3. For each structural commit, read its full message and stat:

   ```bash
   git show --stat <hash>
   git log --format="%B" -1 <hash>
   ```

   Build a summary: **what changed, why, and what it touches.** This
   is the lens through which you'll interpret all subsequent diffs.

4. **Check local context too.** Run `git log --oneline -10` in the
   local repo to understand what the instance has done since the last
   sync. Local changes that overlap with upstream changes are
   divergences, not duplicates.

5. Write a brief narrative summary of the upstream evolution before
   proceeding. Present it to yourself as: "Upstream moved from X to Y
   because Z. This affects files A, B, C."

**Only after this step do you have the context to interpret diffs
correctly.** Proceed to step 3.

### 3. Compare core skills

For each `.md` file in upstream `agent_brain/skills/`:

- **Exists locally and identical:** skip.
- **Exists locally with differences:** diff as `diff <upstream> <local>`:
  - Lines with `-` = **upstream only** (candidate to import)
  - Lines with `+` = **local only** (already applied or local
    improvement)
  - Both present = **divergence** (needs judgment)

  Use the narrative from step 2 to classify each difference. A change
  that looks "local only" may actually be upstream reverting something
  — the git log tells you which. For upstream-only changes, the commit
  message from step 2 already explains the why.

- **New in upstream:** read the file's "When to use" section. Summarize
  for the update plan.

Core skills (managed by upstream): `process-conversation.md`,
`daily-consolidation.md`, `weekly-review.md`, `monthly-maintenance.md`,
`triage-inbox.md`, `update-upstream.md`.

Learned skills (local files not in upstream): **never touch**.

### 4. Compare commands

For each `.md` file in upstream `.cursor/commands/`:

- Same logic as skills: identical → skip, different → triage using
  step 2 context, new → summarize purpose.
- `.claude/commands/` is a directory symlink to `.cursor/commands/` —
  **do not create or modify files inside `.claude/commands/`**.

### 5. Compare infrastructure and config

Check for new or changed infrastructure files that aren't skills or
commands but affect how the system works:

- `.cursor/hooks.json`, `.cursor/hooks/` — hook configs and scripts
  (session-start, auto-reflect, auto-consolidate, config.json)
- `.claude/settings.json` — claude-code settings (repo-committed; use
  `.claude/settings.local.json` for personal overrides)
- `.claude/hooks/` — symlink to `.cursor/hooks/`
- `.cursorignore` — file visibility rules
- Any new directories or config files at the repo root

For each: does it exist locally? Is it different? Was it intentionally
removed locally (check local git log)? The step 2 narrative should
already explain what these files do and why they were added.

### 6. Compare packs

For each file in upstream `.packs/`:

- Changed: triage diff using step 2 context.
- New pack or new files in existing pack: summarize.
- If the instance intentionally removed `.packs/`, note and skip.

### 7. Compare identity templates

Diff the upstream `agent_brain/identity/SOUL.md` and
`agent_brain/identity/USER.md` against the local versions.

These files are **never overwritten** — they contain user-specific
content. However, the upstream templates may change *how instructions
are written* (structure, sections, guidance phrasing). If the upstream
template changed structurally:

- The step 2 narrative should explain why.
- Flag to the user: "The upstream SOUL.md/USER.md template changed:
  [summary]. Your local version may benefit from adapting the spirit
  of this change. Review and apply via maintenance cycles if
  appropriate."
- **Do not apply changes directly.** Identity changes go through
  maintenance cycles or explicit user requests.

### 8. Compare CLAUDE.md structural sections

The upstream CLAUDE.md is at `templates/CLAUDE.md` in the cloned repo.

The live `CLAUDE.md` mixes upstream structure with instance content.
Compare only the structural sections:

- **Core behavior** — listen and capture rules, idea format, file
  metadata
- **Rules** — numbered list. Compare rule by rule, triaging direction:
  - Rule exists only in upstream → propose adding.
  - Rule exists only in local → note as "local addition" and skip.
  - Same rule, different wording → triage using step 2 context.
  - Rules removed upstream → flag (don't auto-remove).
- **Skills section header** — only check if new core skills from
  upstream should be added. Don't touch learned or instance-specific
  entries.

**Never touch:**
- Active context (Right now, Files)
- Where to find things (instance-specific entries)
- Skills list (instance-specific entries)

### 9. Present update plan

Before applying anything, present a summary. Start with the narrative
from step 2 so the user understands the upstream direction, then list
specific changes:

```
## Upstream summary

[2-3 sentences: what changed in upstream and why — from step 2]

## Update plan

**Infrastructure:**
- [new/changed config files, hooks, etc.]

**Skills:**
- Updated: [name] ([reason from git log])
- New: [name] ([brief description])
- Unchanged: N skills

**Commands:**
- Updated: [name] ([reason])
- Unchanged: N commands

**CLAUDE.md:**
- New rule N: [description]
- Modified rule N: [brief diff]
- Core behavior: [changed / unchanged]

**Identity templates:**
- SOUL.md: [no changes / structural change flagged]
- USER.md: [no changes / structural change flagged]

**Packs:**
- Updated: [pack/file] ([reason])

Apply all / review one by one / skip?
```

Wait for user decision.

### 10. Apply approved changes

For each approved change:

- **Skills:** Copy from upstream clone to local `agent_brain/skills/`.
  Update `last_accessed` to today in the local copy's metadata.
- **Commands:** Copy from upstream clone to local `.cursor/commands/`.
- **Infrastructure:** Copy hooks, configs. Merge settings files
  carefully (don't overwrite local permissions or instance-specific
  config).
- **Packs:** Copy changed files from upstream `.packs/` to local
  `.packs/`.
- **CLAUDE.md sections:** Patch the specific section in the live
  `CLAUDE.md`. Be precise — replace only the structural section,
  preserve everything else.
- **New core skills in CLAUDE.md:** Add them to the Skills section with
  trigger description from the skill's "When to use" section.
- **Sweeping changes** (renames, structural shifts identified in step
  2): apply across all affected files — skills, commands, concepts,
  README. Historical files (logs, journal, wiki) are records of what
  was true at the time and should not be updated.

### 11. Clean up

Remove the temp clone:

```bash
rm -rf /tmp/ab-upstream-*
```

Commit:

```bash
git add -A && git commit -m "update: sync with upstream agentic-buddy (YYYY-MM-DD)"
```

Report what was applied.

## Quality criteria

- **Git log first, diffs second.** Never compare files without first
  understanding the upstream narrative from git history. Diffs show
  what changed; git log explains why. Without the why, you can't tell
  if a difference is upstream-ahead, local-ahead, or a structural
  shift that reframes everything.
- **Direction matters.** Always `diff <upstream> <local>`. Lines with
  `-` are upstream-only (candidates to import); lines with `+` are
  local-only (already applied or local improvements). When in doubt,
  the git log is the tiebreaker.
- **Per-entry judgment.** Don't copy mechanically. Evaluate each change
  in the context of the current instance. A generic template entry may
  not apply or may need adaptation. Files that were intentionally
  removed locally should not be re-added.
- **Show reasoning.** For each proposed change, explain *why* it was
  made upstream (from git log). This helps the user decide.
- **Preserve user work.** User content, identity, knowledge, Active
  context, Where to find things — these are sacred. The update only
  touches system infrastructure.
- **Reversible.** The git commit makes the entire update revertible with
  `git revert HEAD`.
