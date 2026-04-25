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

**Key structural note:** In the upstream repo, the operational AGENTS.md
lives at `templates/AGENTS.md`, not at the root. The root `AGENTS.md`
is the setup redirect for fresh installations. Always compare against
`templates/AGENTS.md`.

## Procedure

### 1. Clone upstream

Clone the full repo (not `--depth 1`) so git log is available for
understanding why changes were made:

```bash
git clone https://github.com/juanje/agentic-buddy.git /tmp/ab-upstream-$(date +%Y%m%d)
```

Store the path for the rest of the procedure.

### 2. Compare core skills

For each `.md` file in upstream `agent_brain/skills/`:

- **Exists locally and identical:** skip.
- **Exists locally with differences:** triage the diff to determine
  direction. Always diff as `diff <upstream> <local>` so that:
  - Lines with `-` = **upstream only** (candidate to import)
  - Lines with `+` = **local only** (already applied or local improvement)
  - Both present = **divergence** (needs judgment)
  For each difference, classify it:
  - **Upstream-only change:** read `git log --oneline -5 <file>` in the
    upstream clone to understand why it was made. Summarize for the
    update plan.
  - **Local-only change:** note as "local ahead" and skip — the instance
    already has this improvement (or a better version of it).
  - **Divergence (both changed the same area differently):** present both
    versions with reasoning so the user can decide.
  Only upstream-only changes and divergences go into the update plan.
- **New in upstream:** read the file's "When to use" section. Summarize
  for the update plan.

Core skills (managed by upstream): `process-conversation.md`,
`daily-consolidation.md`, `weekly-review.md`, `monthly-maintenance.md`,
`triage-inbox.md`, `update-upstream.md`.

Learned skills (local files not in upstream): **never touch**.

### 3. Compare commands

For each `.md` file in upstream `.cursor/commands/`:

- Same logic as skills: identical → skip, different → triage diff
  direction (upstream-only / local-only / divergence), new → summarize
  purpose. Only upstream-only changes and divergences go into the plan.
- `.claude/commands/` is a directory symlink to `.cursor/commands/` —
  **do not create or modify files inside `.claude/commands/`**.

### 4. Compare packs

For each file in upstream `.packs/`:

- Changed: triage diff direction (same as step 2). Only upstream-only
  changes go into the plan.
- New pack or new files in existing pack: summarize.

### 5. Compare identity templates

Diff the upstream `agent_brain/identity/SOUL.md` and
`agent_brain/identity/USER.md` against the local versions.

These files are **never overwritten** — they contain user-specific
content. However, the upstream templates may change *how instructions
are written* (structure, sections, guidance phrasing). If the upstream
template changed structurally:

- Read `git log` on the changed file to understand why.
- Flag to the user: "The upstream SOUL.md/USER.md template changed:
  [summary]. Your local version may benefit from adapting the spirit
  of this change. Review and apply via maintenance cycles if
  appropriate."
- **Do not apply changes directly.** Identity changes go through
  maintenance cycles or explicit user requests.

### 6. Compare AGENTS.md structural sections

The upstream AGENTS.md is at `templates/AGENTS.md` in the cloned repo.

The live `AGENTS.md` mixes upstream structure with instance content.
Compare only the structural sections:

- **Session start** — steps 1-4
- **Core behavior** — listen and capture rules, idea format, file metadata
- **Rules** — numbered list. Compare rule by rule, triaging direction:
  - Rule exists only in upstream → propose adding.
  - Rule exists only in local → note as "local addition" and skip.
  - Same rule, different wording → triage: upstream-only words are
    candidates to import; local-only words are local improvements.
  - Rules removed upstream → flag (don't auto-remove).
- **Skills section header** — only check if new core skills from upstream
  should be added. Don't touch learned or instance-specific entries.

**Never touch:**
- Active context (Right now, Files)
- Where to find things (instance-specific entries)
- Skills list (instance-specific entries)

### 7. Present update plan

Before applying anything, present a summary:

```
## Update plan

**Skills:**
- Updated: [name] ([reason])
- New: [name] ([brief description])
- Unchanged: N skills

**Commands:**
- Updated: [name] ([reason])
- Unchanged: N commands

**AGENTS.md:**
- New rule N: [description]
- Modified rule N: [brief diff]
- Session start: [changed / unchanged]
- Core behavior: [changed / unchanged]

**Identity templates:**
- SOUL.md: [no changes / structural change flagged]
- USER.md: [no changes / structural change flagged]

**Packs:**
- Updated: [pack/file] ([reason])

Apply all / review one by one / skip?
```

Wait for user decision.

### 8. Apply approved changes

For each approved change:

- **Skills:** Copy from upstream clone to local `agent_brain/skills/`.
  Update `last_accessed` to today in the local copy's metadata.
- **Commands:** Copy from upstream clone to local `.cursor/commands/`.
- **Packs:** Copy changed files from upstream `.packs/` to local `.packs/`.
- **AGENTS.md sections:** Patch the specific section in the live
  `AGENTS.md` (and `CLAUDE.md` if it's not a symlink). Be precise —
  replace only the structural section, preserve everything else.
- **New core skills in AGENTS.md:** Add them to the Skills section with
  trigger description from the skill's "When to use" section.

### 9. Clean up

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

- **Direction matters.** Always `diff <upstream> <local>`. Lines with
  `-` are upstream-only (candidates to import); lines with `+` are
  local-only (already applied or local improvements). Never present
  local improvements as upstream changes to import. When in doubt,
  read the upstream git log: if the change isn't in any upstream commit,
  it's local.
- **Per-entry judgment.** Don't copy mechanically. Evaluate each change
  in the context of the current instance. A generic template entry may
  not apply or may need adaptation.
- **Show reasoning.** For each proposed change, explain *why* it was
  made upstream (from git log). This helps the user decide.
- **Preserve user work.** User content, identity, knowledge, Active
  context, Where to find things — these are sacred. The update only
  touches system infrastructure.
- **Reversible.** The git commit makes the entire update revertible with
  `git revert HEAD`.
