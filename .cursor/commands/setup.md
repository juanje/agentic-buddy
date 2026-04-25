Run the Agentic Buddy setup.

If a language is specified after the command (e.g., `/setup español`), conduct the entire setup conversation in that language. If no language is specified, detect the user's language from their first response and continue in that language. All **generated content** (files, notes, logs) is always in English regardless of conversation language.

## Pre-flight check

First, determine if this is a fresh setup or a reconfiguration:

1. Read `AGENTS.md`.
2. If it contains `POST-SETUP:` → **Fresh setup.** Proceed with the full setup below.
3. If it does NOT contain that marker → **System already configured.** Switch to reconfiguration mode:
   > The system is already set up. I can help you with:
   > - Update your profile (`agent_brain/identity/USER.md`)
   > - Add a new project to `agent_brain/projects/`
   > - Apply a domain pack (see `.packs/index.md`)
   > - Review or adjust the current structure
   >
   > What would you like to update?

   In reconfiguration mode: **never overwrite AGENTS.md**. Only modify the specific files the user asks about.

   After changes, commit: `git add -A && git commit -m "reconfig: <what changed>"`

   **Do not continue with the steps below.** End here for reconfiguration.

---

## Full setup procedure

### Step 1: Introduction

Read `templates/AGENTS.md` to understand the system you're setting up (don't explain the whole system to the user).

Then tell the user (in their language):

> I'll help you set up your Agentic Buddy. I'll ask a few questions to personalize the system. It takes about 2 minutes.
>
> After that, the system is ready. You can start brain-dumping tasks, ideas, notes, and anything else right away.

### Step 2: Get to know the user

Start with a warm, conversational tone. This is a first meeting — get to know the person. Ask **one group at a time**, wait for answers, and adapt naturally.

**Who are you and what do you need?** (ask all of these together)
- What's your name?
- What do you want to use this for? (open-ended — let them describe it in their own words: work, personal projects, writing, training, anything)
- Anything else you'd like to share? How you like to work, what matters to you, how you prefer information presented... Whatever feels relevant. (This is optional and open — some people share a lot, others prefer to keep it brief. Both are fine.)

After this exchange, reflect back briefly what you understood.

### Step 3: Write agent_brain/identity/USER.md

Using the answers, fill in `agent_brain/identity/USER.md`. Follow the template structure already in the file but replace the placeholder comments with real content. Be concise — this file is reference, not a biography. If the user gave brief answers, fill in what you have and leave the rest as placeholders — it will fill in over time.

If the conversation was conducted in a non-English language (either specified via `/setup <language>` or detected from the user's messages), capture the chat language preference in USER.md → Preferences. Example: `- **Chat language:** Spanish`. This ensures future sessions (especially bare commands like `/daily`) reply in the right language.

### Step 3b: Personalize the agent (optional)

After writing USER.md, offer the user a chance to customize the agent:

> Want to personalize how I work? You can:
> - **Name:** Give me a name
> - **Interaction style:** Adjust how I communicate — tone (formal, casual),
>   verbosity (brief, detailed), or how I express disagreement
> - **Character:** The defaults include traits like intellectual curiosity,
>   honesty, and willingness to push back. These are the foundation that
>   enables good judgment in new situations. You can tune how they express
>   themselves, but removing them weakens the system.
>
> This is optional — the defaults work well and adapt as we work together.
> You can always change this later by editing `agent_brain/identity/SOUL.md`.

If the user wants to personalize:
1. Read `agent_brain/identity/SOUL.md`.
2. If they chose a name, add a `## Name` section at the top.
3. Adjust the `## Interaction style` section to reflect their preferences.
   Write preferences as defaults ("by default, lean; adjust up when asked"),
   not rigid constraints.
4. Character traits (## Character) are the foundation for judgment in novel
   situations — they work like culture: when you face something new, you act
   "as yourself" instead of searching for a matching rule. When personalizing:
   adjust HOW the agent communicates (tone, verbosity, formality), not WHAT it
   values (honesty, intellectual engagement, transparency). If the user requests
   something that contradicts a character trait (e.g., "never disagree with me"),
   explain the trade-off and propose adjusting the style instead of removing
   the trait.

If the user skips: proceed to Step 4. The default SOUL.md is already well-rounded.

### Step 4: Check domain packs

Based on what the user described in Step 2, check if a matching domain pack exists:

1. Read `.packs/index.md`.
2. If the user's purpose matches an available pack (work, personal, writing):
   > It sounds like [domain]. I have a starter pack for that — it includes
   > [brief description of what the pack provides]. Want me to set it up?
   >
   > You can also skip this and let the system develop its own structure
   > as you use it.
3. If the user wants the pack: follow the "How to apply a pack" instructions
   in `.packs/index.md`. Copy files to their destinations, add skills to
   AGENTS.md if applicable.
4. If the user's purpose doesn't match any pack, or they decline: proceed
   without a pack. The system will develop structure organically.

### Step 5: Set up agent commands (if applicable)

Check what editor/agent the user is running:

- **Cursor**: `.cursor/commands/` is already set up. No action needed.
- **Claude Code**: `CLAUDE.md` is a symlink to `AGENTS.md`, and `.claude/commands/` is a **directory symlink** to `.cursor/commands/`. Both are pre-created — any file added to `.cursor/commands/` is automatically visible to Claude Code. **Do not create individual symlinks or files inside `.claude/commands/`** — the directory symlink handles it. Additionally, create `.claude/settings.local.json` with basic permissions:
  ```json
  {
    "permissions": {
      "allow": [
        "Bash(git add:*)",
        "Bash(git commit:*)",
        "Bash(ls:*)",
        "Bash(mkdir:*)"
      ]
    }
  }
  ```
  If a domain pack was applied that includes external tools, add their permissions too.
- **Other agents**: The slash commands won't work, but the skills can be triggered by asking the agent directly (e.g., "do a weekly review"). No changes needed.

### Step 6: Activate the system

Execute these steps in order:

1. Copy the operational AGENTS.md into place:
   ```bash
   cp templates/AGENTS.md ./AGENTS.md
   ```

2. Remove setup-only files:
   ```bash
   rm -rf templates/
   rm -f LICENSE
   ```

3. Initial commit:
   ```bash
   git add -A && git commit -m "setup: initial configuration"
   ```

4. Tell the user (in their language):

> Your Agentic Buddy is ready.
>
> **To activate it now**, run **/refresh** so I reload the new AGENTS.md and start working in operational mode. Alternatively, start a new conversation — I'll pick up the new instructions automatically.
>
> **Quick start:**
> - Brain dump anything: tasks, ideas, decisions, notes. I'll capture and file them.
> - Use **/reflect** to process a conversation into your daily log.
> - Use **/daily** at the end of the day to consolidate and learn.
> - Use **/weekly** at the end of the week to review and plan ahead.
>
> The more you use it, the more it knows. Start talking.

## Rules during setup

1. Conduct the conversation in the user's preferred language. If specified with the command, use that. Otherwise, detect from their first message.
2. All **generated file content** (USER.md, notes, logs, brain files) must be in English, regardless of conversation language.
3. Be conversational, not bureaucratic. This should feel like a quick onboarding chat, not a form.
4. Don't overwhelm. Ask one group of questions at a time. Wait for answers.
5. If the user gives short answers, that's fine. The system fills in over time.
6. If the user wants to skip something, skip it. Everything can be added later.
