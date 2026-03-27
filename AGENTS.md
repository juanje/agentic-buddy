# Agentic Buddy — Not yet configured

This system needs initial setup before it can help you.

Run `/setup` to start the guided configuration, or `/setup <language>` to run it in your preferred language (e.g., `/setup español`, `/setup français`).

## How to handle `/setup`

When the user types `/setup` or `/setup <language>`:

1. Read `.cursor/commands/setup.md` — it contains the full setup procedure.
2. Follow the instructions in that file step by step.
3. If a language was specified (e.g., `/setup español`), pass it as context to the procedure.

This applies to all agents, whether or not they support slash commands natively.

Until setup is complete, this agent cannot help with anything else. If the user asks for something unrelated, politely redirect them to run `/setup` first.

**POST-SETUP:** This file gets replaced by the operational AGENTS.md from `templates/`.
