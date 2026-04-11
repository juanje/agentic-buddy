# Agentic Buddy

A self-organizing memory for any AI agent. Brain dump tasks, decisions, ideas, and context — the agent captures, organizes, and helps you stay on top of whatever you're working on. Works with any use case: work, personal productivity, writing, training, research, or anything else.

> **Early stage project.** This system is fully functional and in active daily use, but still evolving. Rules, skills, and project structure may change as better patterns are discovered. Your local copy is yours — upstream changes won't affect it. If you adopt this system, expect to adapt it to your workflow rather than follow a stable API.

## Table of contents

- [Getting started](#getting-started)
- [Migrating from an existing instance](#migrating-from-an-existing-instance)
- [What it does](#what-it-does)
- [Architecture: four memory zones](#architecture-four-memory-zones)
- [Learning cycles](#learning-cycles)
- [Structure](#structure)
- [Domain packs](#domain-packs)
- [Example use cases](#example-use-cases)
- [Structured workflows](#structured-workflows)
- [Compatibility](#compatibility)
- [Customization](#customization)
- [Design principles: why this works](#design-principles-why-this-works)
- [Known limitations](#known-limitations)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Getting started

1. Clone or copy this repository into a new directory.
2. Open it as a workspace in your AI-powered editor (Cursor, VS Code + Copilot, Claude Code, etc.).
3. Run `/setup` to start the guided configuration, or `/setup <language>` to run it in your preferred language (e.g., `/setup español`).
4. The agent will ask your name, what you want to use the system for, and how you prefer to work. If a matching domain pack exists, it will offer to set it up.
5. After setup, the system is ready. Start brain-dumping.

## Migrating from an existing instance

If you have an existing brain instance (Work Agentic Buddy or an older Agentic Buddy), you can import its accumulated knowledge into a new instance instead of starting from scratch.

1. Set up the new instance first (clone, `/setup`).
2. Run `/import <path>` with the path to your old instance:
   ```
   /import ~/git/work_brain
   ```
3. The agent will scan the source, show you a summary of what it found (concepts, projects, ideas, logs, skills, user artifacts), and ask for confirmation before importing.

The import handles structural differences automatically: `work/` maps to `user/`, outdated core skills are skipped (the new instance has updated versions), learned skills are preserved, and file metadata (`access_count`, `created` dates) is kept so that Hebbian dynamics work correctly with your historical usage patterns.

Identity (USER.md) is merged by section -- content from the old profile is added where the new one has placeholders, without overwriting anything you already configured during setup.

The import is additive and safe to run multiple times. If a file exists in both instances, the agent asks what to do. To undo, `git reset --hard HEAD~1` reverts the import commit.

## What it does

Talk to the agent naturally. It will:

- **Capture action items** → `user/` workspace (creates fitting structure: lists, boards, inboxes)
- **Capture decisions** → Project files or concept files, with reasoning
- **Capture ideas** → Ideas directory, with a lifecycle (seed → developing → ready → converted)
- **Capture lessons** → Concept files for future reference
- **Confirm what it captured** — always

You don't need to think about where things go. The agent classifies and files them based on what you say. Over time, your workspace becomes a searchable, structured knowledge base of everything you've worked on, decided, and learned.

When you start a new conversation, the agent automatically checks for today's log (or yesterday's) to pick up context from previous sessions — no need to repeat yourself.

## Architecture: four memory zones

The system's directory structure maps to distinct cognitive functions, each with its own purpose, lifecycle rules, and ownership.

| Directory | Cognitive function | Contents | Lifecycle | Ownership |
|---|---|---|---|---|
| `AGENTS.md` | Working memory | Active context, rules, skills index | Updated by `/daily` and `/weekly` | Agent |
| `agent_brain/` | Semantic memory | Concepts, projects, skills, identity | Hebbian: promote, degrade, archive | Agent |
| `logs/` | Episodic memory | Conversation records | Compact by age, archive after extraction | Agent |
| `user/` | Extended mind | Lists, drafts, documents, user files | No automatic pruning — user decides | User |

### `agent_brain/` — what the agent knows

The agent's internal knowledge: concepts, projects, observations, skills, identity. Subject to Hebbian plasticity — frequently accessed files get promoted to Active context; abandoned files get archived. The user can inspect it, but normally doesn't edit it directly.

### `user/` — the user's workspace

Artifacts produced *for* or *by* the user: task lists, drafts, articles, training programs, reference documents. The agent creates, modifies, and consults them — but they are not the agent's memory. They are tools on the user's desk.

The user **can and should** put content here directly: documents for the agent to read, files they're working on, references they need. The agent reads from `user/`, processes what it finds, and stores what it learns in `agent_brain/`. Like putting a document on your desk for your assistant to read — the document stays on the desk, the knowledge goes into the assistant's head.

Hebbian pruning does NOT apply to `user/`. The agent never auto-archives or deletes user content.

### `logs/` — what happened

Conversation records — the logbook. Not knowledge (that's `agent_brain/`), not user artifacts (that's `user/`). A processing buffer where episodes are recorded and later consolidated into semantic memory by the learning cycles.

### Why this separation matters

- **Clear capture destinations.** "Will the user act on this?" → `user/`. "Will the agent learn from this?" → `agent_brain/`. "Did this happen in a conversation?" → `logs/`.
- **Different lifecycle rules.** Each directory has rules that match its function. Hebbian pruning makes sense for knowledge, not for the user's task list. Age-based compaction makes sense for logs, not for concepts.
- **User can contribute directly.** The user adds documents, references, or drafts to `user/`. The agent reads and processes them. No need to paste content into chat — just drop the file.

## Learning cycles

The system learns through four temporal levels, modeled on how biological memory works — from short-term encoding to long-term consolidation and forgetting:

| Level | Command | What it does | When to run |
|-------|---------|-------------|-------------|
| **Encoding** | `/reflect` | Logs the conversation, detects patterns and observations | After each conversation |
| **Consolidation** | `/daily` | Creates concepts, forms associations, creates skills/rules from mature observations, first promotions | End of day |
| **Calibration** | `/weekly` | Calibrates promotions (reinforce or weaken), generalizes across concepts, light pruning flags | End of week |
| **Forgetting** | `/monthly` | Archives abandoned files, prunes unused skills, deep generalization, contradiction and structure review | Monthly |

Each level builds on the previous one's output. `/reflect` detects raw observations. `/daily` acts on them — creating knowledge and connections. `/weekly` checks whether those connections held up over time or were just noise. `/monthly` archives what's truly forgotten and looks for deep patterns across the full knowledge base.

Specific concepts that share an underlying pattern get abstracted into general concepts — the general version handles future unknown cases, while the specific instances remain for detailed reference.

## Structure

```
├── AGENTS.md                    → Agent working memory. Loaded automatically.
├── user/                        → User workspace. Action items, drafts, documents.
├── logs/                        → Daily conversation logs.
│   └── archive/                 → Compacted old logs.
└── agent_brain/
    ├── identity/
    │   ├── USER.md              → Your profile and preferences.
    │   └── SOUL.md              → Agent identity and character — who the agent is.
    ├── observations.md          → Learning journal: raw observations from /reflect.
    ├── skills/                  → Reusable procedures, loaded on demand.
    ├── projects/                → Active project context and decisions.
    ├── concepts/                → Lessons learned, patterns, knowledge.
    ├── ideas/                   → Ideas with lifecycle tracking.
    └── archive/                 → Files degraded by disuse.
```

The system starts nearly empty. Directories populate through use. The agent creates files and new directories inside `agent_brain/` and `user/` as needed — you don't have to set up anything manually beyond the initial configuration. The structure grows organically to match how you actually use it.

## Domain packs

The system ships with optional starter kits in `.packs/` that bootstrap specific use cases. Packs are hidden from the editor index (`.cursorignore`) and don't consume context until activated.

| Pack | What it provides |
|------|-----------------|
| **work** | Kanban board, standup skill, board sync, next-task, capture-item, tool setup guide |
| **personal** | GTD-style inbox with contexts (@home, @errands, @computer) |
| **writing** | Writing style template for the agent to learn your voice |

During setup, the agent offers a matching pack based on what you describe. You can also apply packs later by asking the agent ("I want to start tracking tasks") — it will check the available packs and propose one. Packs are never forced; you can always let structure emerge naturally instead.

## Example use cases

The same core produces different structures depending on how you use it:

### Work

You start talking about tasks, tickets, sprints. Over days, `user/` develops a board or task list. `agent_brain/` fills with project context, team patterns, and decision records. Skills like standup, sync, and next-task emerge (or you apply the work pack for a head start).

### Personal productivity

You dump errands, personal projects, "someday" ideas. `user/` develops an inbox, shopping lists, and context-based groupings. `agent_brain/` captures habits, patterns, and project notes. A weekly planning skill might emerge.

### Writing / research

You discuss article ideas, research notes, drafts. `user/` develops a drafts directory and published archive. `agent_brain/` fills with heavily cross-referenced concepts, a STYLE.md with your voice, and an active ideas pipeline. Skills like brainstorm and draft-review emerge.

### Sports training

You discuss training plans, sessions, progress. `user/` develops a program file and training log. `agent_brain/` captures training principles, adaptation patterns, and injury notes. A session-log or weekly-load-review skill might emerge.

In all cases, the same four learning cycles drive the system. `agent_brain/` captures what the agent learns. `user/` holds what the user acts on. The structure that emerges is different, but the mechanics are identical.

## Structured workflows

| Command | What it does |
|---------|-------------|
| `/reflect` | Processes the conversation into a structured daily log and detects learning observations |
| `/daily` | End-of-day consolidation: creates concepts, forms associations, acts on mature observations |
| `/weekly` | Weekly review + Hebbian calibration of promotions + generalization across concepts |
| `/monthly` | Deep maintenance: pruning, deep generalization, contradiction detection, structure review |
| `/refresh` | Re-reads AGENTS.md — useful when the agent loses context in long conversations |

These commands are available as slash commands in Cursor and Claude Code. For other agents, trigger them by asking directly (e.g., "do a weekly review").

## Compatibility

The system works with any AI agent that reads `AGENTS.md` from the workspace root:

- **Cursor** — full support (AGENTS.md + slash commands)
- **Claude Code** — full support via `CLAUDE.md` symlink + `.claude/commands/` symlinks (pre-created)
- **GitHub Copilot** — reads AGENTS.md
- **Windsurf, Zed, Gemini CLI, RooCode** — reads AGENTS.md

Slash commands are provided for Cursor (`.cursor/commands/`). Claude Code commands are pre-created as symlinks in `.claude/commands/` pointing to the Cursor originals — one source of truth, both agents supported. For other agents, trigger workflows by asking directly.

**Note:** Claude Code reads `CLAUDE.md`, not `AGENTS.md`. The included `CLAUDE.md` symlink ensures both files resolve to the same content. A `.cursorignore` file prevents Cursor from double-indexing the symlinked files.

## Customization

### Adding skills

Skills are reusable procedures in `agent_brain/skills/`. Create a new `.md` file with a "When to use" trigger and a numbered "Procedure", then add it to the Skills section in `AGENTS.md`. The agent will pick it up on the next conversation. Skills also emerge naturally through the learning cycles — repeated patterns get proposed as skills during `/daily`.

### Adding brain directories

The agent creates new directories inside `agent_brain/` as needed based on use. You can also create them manually — just add the new directory to the "Where to find things" section in `AGENTS.md` with a description of when the agent should look there.

### How the identity files work together

The system has three layers of instruction, each with a different role:

- **`SOUL.md`** describes WHO the agent is — character traits, not procedures. Keep it short and coherent; everything should connect. Each trait is a deep attractor that guides behavior across all situations. When you edit SOUL.md, write identity descriptions ("you value X"), not commands ("do X").
- **`AGENTS.md`** describes WHAT to do in specific contexts — operational rules with WHY. The reasoning enables the agent to generalize to situations the rule didn't explicitly cover. When adding rules, always include the purpose: `[rule]. [why — what it prevents, enables, or protects]`.
- **Skills** describe HOW to execute specific procedures — steps with purpose. An agent that understands why a step exists can adapt when the exact procedure doesn't fit. When writing skills, include the purpose of non-obvious steps and distinguish fixed steps from judgment calls.

The `/setup` command personalizes interaction style (how the agent communicates) but preserves character traits (what it values) — these are the foundation that enables good judgment in novel situations.

### Writing effective AGENTS.md entries

Two gotchas discovered through production use:

**Don't put instructions in HTML comments.** Claude Code strips HTML comments (`<!-- -->`) from `CLAUDE.md` during auto-injection (since v2.1.72). Since `CLAUDE.md` is a symlink to `AGENTS.md`, any instruction inside an HTML comment will be invisible to the agent at session start. HTML comments in *other* files (skills, observations, identity) are fine — those are read on demand with the Read tool, which preserves comments. Only `AGENTS.md` is affected because it's auto-injected.

**Use trigger patterns, not passive references.** The agent treats the "Where to find things" section as structural documentation — it registers what exists but doesn't act on it. If you want the agent to *do* something in response to user behavior, put it in the Skills section with explicit trigger patterns (e.g., "Use when the user says X, Y, or Z"). Without triggers, the agent sees the reference but doesn't associate it with the user's request.

## Design principles: why this works

Most AI coding assistants are stateless. Each conversation starts from zero. You repeat your context, re-explain your priorities, and lose the thread of what you were doing yesterday. This system gives the agent a persistent memory that grows with use.

But it's not just a note-taking system with an AI front-end. The design is grounded in principles from neuroscience, complex systems theory, and practical experience with AI agent limitations.

### Files as memory substrate

The brain doesn't store memories in a single location — it distributes them across networks that strengthen or weaken based on use. This system uses plain Markdown files as its memory substrate: distributed, human-readable, Git-versionable, and portable across any AI agent that can read files.

There are no databases, no embeddings, no vendor-specific formats. If your agent breaks, switches, or disappears, your knowledge is still there in files you can read, search, and edit yourself.

### Hebbian plasticity: use it or lose it

In neuroscience, Hebb's principle states that neurons that fire together wire together — connections strengthen with use and weaken without it. This system applies the same idea to information management.

Every file tracks when it was last accessed and how often. The learning cycles use these metrics to **promote** frequently-used files to the agent's active context (making them immediately visible) and **archive** files that haven't been touched in weeks. The agent's attention automatically mirrors what's actually relevant right now, without manual curation.

### Implicit connectivity: strength through use

In neuroscience, a memory isn't strong because it has a "strength counter." It's strong because many different cues can activate it — many neural pathways lead there. The memory's importance is a structural property of the network, not a stored number.

This system applies the same principle. A concept's importance is never calculated or declared — it emerges from how many other files link to it through organic use. If a concept genuinely matters, many files will reference it naturally, because their readers benefit from knowing about it. That network of incoming links *is* the concept's strength, just as the web of neural connections *is* the memory's strength.

Links must be **functional**: each one exists to serve the reader of the file it's in, not to maintain a graph structure. A link is added when — and only when — it answers: "Would someone reading *this* file benefit from navigating *there*?" This explicitly avoids Obsidian-style backlinks, where every link must be bidirectional. Mandatory backlinks cause central concepts to bloat with inbound references that don't serve their readers — the concept file becomes a noisy index instead of focused knowledge.

### Memory architecture: four zones

The directory structure maps to a cognitive model with four distinct memory systems:

| Zone | Location | Biological analog | Accessibility |
|---|---|---|---|
| **Working memory** | `AGENTS.md` | Prefrontal cortex | Always loaded. The agent sees this every conversation. |
| **Semantic memory** | `agent_brain/` | Neocortex | Accessible on demand. Frequently accessed files get promoted to Active context. |
| **Episodic memory** | `logs/` | Hippocampus | Processing buffer. Episodes are consolidated into semantic memory over time. |
| **Extended mind** | `user/` | Notebook, calendar, tools | The user's workspace. Not the agent's memory, but part of the cognitive system. |

The critical distinction between `agent_brain/archive/` and deletion: archived files remain in the workspace where a search can find them (**passive recognition** — "I forgot I knew this, but a search reminded me"). Deleted files only exist in git history, which requires knowing they existed in the first place (**active recall**). This is why the system archives before deleting.

### Progressive disclosure: load only what's needed

The agent doesn't read everything at startup. It reads a lightweight index file (`AGENTS.md`, ~100 lines) that contains just enough to know where things are and when to look deeper. Skills, project context, and knowledge files are loaded on demand — only when a task requires them.

This mirrors how human expertise works: you don't recall everything you know before starting a task. You activate relevant knowledge as the context demands it. For AI agents, this has a practical benefit too — it keeps the context window clean, which directly improves response quality.

### Self-regulation: the system forgets on purpose

The maintenance cycles aren't just organizational — they actively prune the knowledge base. `/monthly` archives files that haven't been accessed in weeks, `/weekly` flags candidates for degradation, and `/daily` consolidates redundant observations into fewer, stronger concepts. The system scales not by accumulating everything but by continuously discarding what's no longer relevant — the same way biological memory works.

Forgetting is not a failure of maintenance; it's a core mechanism. Without it, the signal-to-noise ratio degrades and the agent's context fills with stale information. A well-maintained instance doesn't grow unboundedly — it reaches a dynamic equilibrium where new knowledge enters at roughly the same rate old knowledge is archived or absorbed into generalizations.

Crucially, forgetting here doesn't mean losing information. Archived files move to `agent_brain/archive/` or `logs/archive/` — out of active memory but still searchable by the editor. A search can surface them even when the agent doesn't remember they exist. And since every change is committed to Git, the full history is always recoverable. The system forgets like a well-organized filing cabinet, not like amnesia.

### Learning pipeline: from observations to knowledge

The system doesn't just store what you tell it — it learns from patterns across conversations. The pipeline works in stages:

1. `/reflect` detects raw observations from the conversation ("this pattern appeared", "this approach failed") and records them in `observations.md`.
2. Observations accumulate as candidates. A single observation is noise.
3. When an observation recurs or gains supporting evidence across multiple sessions, `/daily` promotes it — to a formal concept in `concepts/`, a new rule in `AGENTS.md`, or a reusable skill in `skills/`.
4. `/weekly` and `/monthly` generalize across concepts: when specific instances share an underlying pattern, they get abstracted into a general concept that handles future unknown cases. The specific instances remain as supporting evidence.

This is how the system develops judgment, not just memory. A repeated pattern becomes knowledge. A generalized pattern becomes a principle the agent applies to situations it hasn't seen before.

### Identity as attractor: character over rules

The agent's behavior is governed primarily by identity (`SOUL.md`), not by rules. `SOUL.md` describes *who the agent is* — its character, values, and stance — rather than enumerating what it should or shouldn't do. Rules in `AGENTS.md` handle specific known failure modes (guardrails), but the agent's general orientation comes from character.

This distinction matters because instructions sit on a spectrum, each level progressively better at enabling judgment in novel situations:

1. **Bare rule** — "Never do X." Predictable but brittle: breaks in any situation the rule didn't anticipate.
2. **Rule with WHY** — "Do Y, because Z." The agent understands the purpose and can generalize to situations the rule didn't cover. Research confirms that LLMs follow rules better when given reasoning, because they can create meta-rules from the explanation.
3. **Character** — "You are someone who values Z." No rule needed per situation — the agent has the adaptive capacity to generate appropriate responses in any context, including ones never anticipated.

An agent following rules fails silently when it encounters a case no rule covers. An agent with internalized character makes a judgment call consistent with who it is — identity and character act as a cognitive offloader, guiding behavior in novel situations without having to search for a matching rule. In complex systems terms: `SOUL.md` is an attractor basin that shapes behavior across the full state space, while rules in `AGENTS.md` are boundary conditions that prevent specific known failures. Skills in `agent_brain/skills/` are adaptable techniques — procedures with purpose that the agent can modify when the exact steps don't fit.

Each layer enables the next: character guides rule interpretation, rules with WHY enable generalization, skills with purpose enable adaptation. The maintenance cycles evolve this system over time: rules that prove universally important get promoted to character traits during `/monthly` (Hebbian internalization), while unused rules decay and get archived.

### Emergence from simple rules

Complex systems theory shows that sophisticated behavior can emerge from simple rules applied consistently. This system doesn't try to be a complete project management tool, writing assistant, or training coach. Instead, it gives the agent a small set of clear behaviors:

- **Capture everything the user mentions.** Tasks, ideas, decisions, notes — file them in the right place.
- **Confirm what was captured.** Brief acknowledgment, no ceremony.
- **Don't reorganize proactively.** Structure emerges from use, not from upfront design.
- **When in doubt, capture.** A rough note is better than a lost thought.

Over time, these simple rules produce a knowledge base that reflects how you actually work — not how you planned to work. A work user ends up with a board and standup skills. A writer ends up with a drafts directory and a style guide. A trainer ends up with a program file and session logs. The same core, different emergent structures.

## Known limitations

This system runs on top of general-purpose AI coding agents, not a dedicated application. That means some things that would ideally be automatic require manual intervention.

**All learning cycles are manual.** You need to remember to run `/reflect`, `/daily`, `/weekly`, and `/monthly` at the appropriate times. There are no automatic triggers — most editors don't fire session-end events, and users typically start new conversations rather than closing existing ones. If you forget to reflect, conversation context is lost when it leaves the agent's context window.

**Partial workaround (Linux/macOS + Claude Code CLI):** The consolidation cycles (`/daily`, `/weekly`, `/monthly`) can be automated via cron since they don't require an active conversation — they work from the files in the repo. `/reflect` cannot be automated this way because it processes a specific conversation.

```cron
# Common config
PROJECT_DIR=/path/to/your/ab
CLAUDE_BIN=/path/to/claude          # e.g. ~/.local/bin/claude
CLAUDE_TOOLS="Bash(readonly=false),Read,Write,Edit,Glob,Grep"

# Daily — every night at 23:50
50 23 * * *   cd $PROJECT_DIR && $CLAUDE_BIN -p "/daily"   --allowedTools "$CLAUDE_TOOLS" >> logs/cron-daily.log 2>&1

# Weekly — Sundays at 23:55 (after daily)
55 23 * * 0   cd $PROJECT_DIR && $CLAUDE_BIN -p "/weekly"  --allowedTools "$CLAUDE_TOOLS" >> logs/cron-weekly.log 2>&1

# Monthly — 1st of each month at 00:01
1  0  1 * *   cd $PROJECT_DIR && $CLAUDE_BIN -p "/monthly" --allowedTools "$CLAUDE_TOOLS" >> logs/cron-monthly.log 2>&1
```

Log files land in `logs/` alongside the daily conversation logs.

**Cursor-first.** The system is developed and tested primarily in Cursor. Claude Code is fully functional via pre-created symlinks (`CLAUDE.md`, `.claude/commands/`), but some behavioral differences may exist. For other agents, workflows must be triggered by asking directly (e.g., "do a weekly review"). The core system (AGENTS.md + skills + file structure) works everywhere.

## Acknowledgments

The concept of identity files loaded at session start (`SOUL.md` for agent character, `USER.md` for the human's profile) was inspired by [OpenClaw](https://docs.openclaw.ai/concepts/agent#bootstrap-files-injected), an open-source AI agent runtime that uses a similar set of workspace files (`SOUL.md`, `USER.md`, `IDENTITY.md`, `BOOTSTRAP.md`) to give agents persistent identity and context. The implementation here diverged significantly — shaped by this project's own principles around complex systems, Hebbian memory, and emergent organization — but the seed idea of file-based identity deserves credit.

## License

MIT License. See [LICENSE](LICENSE) for details.
