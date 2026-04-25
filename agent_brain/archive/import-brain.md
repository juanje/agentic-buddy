---
last_accessed: YYYY-MM-DD
access_count: 0
created: YYYY-MM-DD
---

# Skill: Import brain

## When to use

Use when the user says "import my old brain", "migrate from my old instance",
"import from [path]", or runs `/import <path>`. The user provides the path to
an existing brain instance (Work Agentic Buddy or older Agentic Buddy) and
wants to migrate their accumulated knowledge into this new instance.

## Procedure

### Step 1: Scan and detect source type

1. Read the path provided by the user.
2. Check if the directory exists and contains `agent_brain/`. If not, abort:
   "That directory doesn't look like a brain instance — no `agent_brain/`
   found. Please provide the path to your old instance root."
3. Detect the source type:
   - Has `work/` but no `user/` → **WAB** (Work Agentic Buddy)
   - Has `user/` → **AB** (Agentic Buddy)
   - Has only `agent_brain/` → **Compatible** (unknown variant)
4. List what exists in the source:
   - Count files in `agent_brain/concepts/`, `agent_brain/projects/`,
     `agent_brain/ideas/`, `agent_brain/archive/`
   - List any custom directories in `agent_brain/` (beyond identity/,
     skills/, concepts/, projects/, ideas/, archive/)
   - Count files in `work/` or `user/`
   - Count files in `logs/` and `logs/archive/`
   - List skills in `agent_brain/skills/` and classify as core vs learned
   - Check if `agent_brain/observations.md` has unresolved entries
   - Check if `agent_brain/identity/USER.md` has content beyond placeholders

### Step 2: Present import summary

Present a summary to the user:

```
## Import summary

**Source:** [path] ([WAB/AB/Compatible])

**Knowledge (agent_brain/):**
- N concept files
- N project files
- N idea files (+ scratchpad entries)
- N archived files
- Custom directories: [list or "none"]

**User artifacts ([work/user]/):**
- N files

**Logs:**
- N daily logs + N archived logs

**Identity:**
- USER.md: [has content / placeholder only]

**Learned skills:**
- [list of non-core skills, or "none"]

**Observations:**
- N unresolved entries

Shall I proceed with the import?
```

Wait for user confirmation before proceeding.

### Step 3: Import knowledge

Copy files from `agent_brain/` subdirectories:

1. **Concepts:** Copy all `.md` files from source `agent_brain/concepts/`
   to `agent_brain/concepts/`. Skip `.gitkeep`.
2. **Projects:** Copy all `.md` files from source `agent_brain/projects/`
   to `agent_brain/projects/`.
3. **Ideas:** Copy all `.md` files from source `agent_brain/ideas/`
   to `agent_brain/ideas/`. For `_scratchpad.md`, append the source
   entries below the existing entries (don't overwrite).
4. **Archive:** Copy all files from source `agent_brain/archive/`
   to `agent_brain/archive/`.
5. **Custom directories:** For any directory in source `agent_brain/` that
   doesn't exist in the destination (e.g., `teams/`, `reviews/`), create
   it and copy all files. Add it to the "Where to find things" section of
   AGENTS.md with a brief description based on its contents.

**Conflict handling:** If a file with the same name exists in the
destination, ask the user: "File `[path]` exists in both. Keep current /
replace with source / skip?" Default: keep current.

**Metadata:** For each copied file, update `last_accessed` to today's date.
Keep the original `created` and `access_count` values.

### Step 4: Import user artifacts

1. Determine source directory:
   - WAB: source is `work/`
   - AB: source is `user/`
2. Copy all files and subdirectories to `user/`.
3. Same conflict handling as Step 3.
4. If the source is WAB and has `work/BOARD.md`, it becomes `user/BOARD.md`.

### Step 5: Import logs

1. Copy all `.md` files from source `logs/` to `logs/`.
2. Copy all files from source `logs/archive/` to `logs/archive/`.
3. Skip `.gitkeep` files.
4. Same conflict handling (unlikely for logs, but handle it).

### Step 6: Merge identity

1. Read source `agent_brain/identity/USER.md`.
2. Read current `agent_brain/identity/USER.md`.
3. Compare sections. For each section in the source that has real content
   (not just placeholder comments):
   - If the section doesn't exist in the current file → add it.
   - If the section exists but is still a placeholder in the current file
     → replace with the source content.
   - If the section exists with real content in the current file → keep
     current. Mention to the user: "Kept current [section] — source also
     had content. Review manually if needed."
4. Update metadata: set `last_accessed` to today, increment `access_count`.
5. **Skip SOUL.md** — the new instance has the updated agent identity.

### Step 7: Import learned skills

1. List all `.md` files in source `agent_brain/skills/`.
2. Identify core skills to skip:
   - WAB core: `process-conversation.md`, `daily-consolidation.md`,
     `weekly-review.md`, `monthly-maintenance.md`, `run-standup.md`,
     `capture-item.md`, `next-task.md`, `sync-board.md`
   - AB core: `process-conversation.md`, `daily-consolidation.md`,
     `weekly-review.md`, `monthly-maintenance.md`
3. For each non-core skill:
   - Copy to `agent_brain/skills/`.
   - Add it to the Skills section of AGENTS.md. Read the skill file to
     determine the trigger description — use the "When to use" section.
   - Update `last_accessed` to today.
4. If no learned skills exist, skip this step.

### Step 8: Merge observations

1. Read source `agent_brain/observations.md`.
2. Read current `agent_brain/observations.md`.
3. For each unresolved observation in the source (entries under Skill
   candidates, Rule candidates, Concept candidates, Structure candidates):
   - If an entry with the same description already exists → increment
     the count, add today's date.
   - If it's new → append it under the matching category.
4. For resolved observations: append them to the current Resolved section
   (they're historical records).
5. Update metadata.

### Step 9: Update AGENTS.md

1. **Active context:** Read the source AGENTS.md. Extract entries from its
   Active context section. For each entry:
   - Check if the linked file was imported (exists in the destination).
   - If yes and not already in the current Active context → add it.
   - Update the description if the path changed (e.g., `work/` → `user/`).

2. **Learned rules:** Read the source AGENTS.md Rules section. Compare with
   the current rules. For any rule in the source that isn't in the current
   list (beyond the standard numbered rules):
   - Present it to the user: "The source had this rule: [rule]. Want to
     keep it?"
   - If yes → add it to the Rules section.

3. **Where to find things:** If custom directories were imported (Step 3.5),
   they should already be added. Verify.

### Step 10: Git commit

```bash
git add AGENTS.md agent_brain/ user/ logs/ && git commit -m "import: migrate from [source-type] at [path]" 2>/dev/null || true
```

Replace `[source-type]` with WAB/AB/compatible and `[path]` with the
source path (abbreviated if long).

## After import

Tell the user:

> Import complete. Here's what was brought in:
> - [N] knowledge files (concepts, projects, ideas)
> - [N] user artifacts
> - [N] logs
> - [N] learned skills
> - USER.md sections merged: [list]
> - Observations merged: [N] entries
>
> Run `/daily` to consolidate the imported content — this will recalculate
> Active context scores based on the imported metadata and detect any new
> patterns across old and new knowledge.

## Notes

- This skill is safe to run multiple times. It's additive: it won't
  overwrite existing content without asking.
- If the user wants to undo the import, `git reset --hard HEAD~1` reverts
  the import commit.
- The import preserves `access_count` and `created` dates from the source
  so that Hebbian dynamics (promotion, archiving) work correctly with the
  historical usage patterns.
