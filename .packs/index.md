# Domain packs

Optional starter kits that bootstrap the system for specific use cases. Each
pack provides templates (for `user/`) and skills (for `agent_brain/skills/`)
tailored to a domain. Packs are hidden from the editor index (`.cursorignore`)
and don't consume context until activated.

## When to use

- **During setup:** After asking the user what they want to use the system for,
  check if a matching pack exists. Offer it: "I have a starter pack for [domain]
  — want me to set it up?"
- **Later:** If the user starts using the system for a new purpose ("I want to
  start tracking tasks"), read this index and propose the relevant pack.
- **Never force it.** Packs are suggestions. The user can decline and let
  structure emerge naturally.

## How to apply a pack

1. Read the pack's directory (e.g., `.packs/work/`).
2. Copy templates to their destination:
   - Files marked `→ user/` go to `user/`.
   - Files marked `→ agent_brain/skills/` go to `agent_brain/skills/`.
   - Files marked `→ agent_brain/identity/` go to `agent_brain/identity/`.
3. Add any new skills to the Skills section of `AGENTS.md`.
4. If the pack includes commands, create the corresponding files in
   `.cursor/commands/` and symlinks in `.claude/commands/`.
5. Commit: `git add AGENTS.md agent_brain/ user/ .cursor/ .claude/ && git commit -m "pack: apply <name>"`

---

## Available packs

### work

A work-focused setup with Kanban board, standup, task sync, and issue tracker
integration. Recreates the [Work Agentic Buddy](https://github.com/juanje/work-agentic-buddy)
experience from this generic base.

| File | Destination | Description |
|------|-------------|-------------|
| `board.md` | `user/BOARD.md` | Kanban board with Doing, Next Actions, Waiting, Sprint Backlog, Inbox, Parked, Done |
| `run-standup.md` | `agent_brain/skills/` | Daily standup with activity data and board state |
| `sync-board.md` | `agent_brain/skills/` | Quick board sync with issue tracker |
| `next-task.md` | `agent_brain/skills/` | Next task with full context and queue |
| `capture-item.md` | `agent_brain/skills/` | Complex multi-destination captures |
| `tool-setup.md` | _(reference only)_ | Installation guide for `did` and Jira CLI tools |

**After applying:** Add commands for `/standup`, `/sync`, `/next` to
`.cursor/commands/` and `.claude/commands/`. Consider adding a WIP rule
to AGENTS.md (e.g., "Doing WIP: target 1, max 2").

### personal

A minimal personal productivity setup inspired by GTD (Getting Things Done).

| File | Destination | Description |
|------|-------------|-------------|
| `inbox.md` | `user/inbox.md` | Capture inbox with contexts (@home, @errands, @computer) |

**After applying:** The system will naturally develop lists, projects, and
a "someday/maybe" file as you use it. No additional skills needed at start.

### writing

A writing and research setup for articles, blog posts, or long-form content.

| File | Destination | Description |
|------|-------------|-------------|
| `style-guide.md` | `agent_brain/identity/STYLE.md` | Writing style preferences template |

**After applying:** Create `user/drafts/` for work in progress. The agent
will learn your style from the STYLE.md file and from reviewing your drafts.
Skills like `brainstorm-topic`, `draft-article`, and `review-draft` will
emerge naturally through use.
