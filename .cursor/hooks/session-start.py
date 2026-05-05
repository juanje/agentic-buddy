#!/usr/bin/env python3
"""
session-start.py — sessionStart hook for WAB instances.

Injects SOUL.md, USER.md, logs/index.md, and the last active session
log into additional_context. Replaces the manual "Session start" section
that previously relied on agent compliance.

Works with both Cursor and claude-code. AGENTS.md is NOT included —
the platform already loads it as a workspace/project rule.
"""

import json
import os
import re
import sys
from pathlib import Path


def read_file(path: Path) -> str:
    """Read a file, return empty string if missing or unreadable."""
    try:
        return path.read_text().strip()
    except (IOError, OSError):
        return ""


def find_last_active_log(workspace: Path, index_content: str) -> str:
    """Parse logs/index.md to find and read the last active session log."""
    last_date = None
    for line in index_content.splitlines():
        if "active" in line.lower():
            match = re.search(r"(\d{4}-\d{2}-\d{2})", line)
            if match:
                last_date = match.group(1)

    if not last_date:
        return ""

    log_path = workspace / "logs" / f"{last_date}.md"
    return read_file(log_path)


def main() -> None:
    # claude-code passes hook input as JSON on stdin
    try:
        raw = sys.stdin.read()
        hook_input = json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, IOError):
        hook_input = {}

    workspace = Path(
        os.environ.get("CURSOR_PROJECT_DIR", "")
        or hook_input.get("cwd", "")
        or os.environ.get("CLAUDE_PROJECT_DIR", "")
        or os.getcwd()
    )

    soul = read_file(workspace / "agent_brain" / "identity" / "SOUL.md")
    user = read_file(workspace / "agent_brain" / "identity" / "USER.md")
    logs_index = read_file(workspace / "logs" / "index.md")
    last_log = find_last_active_log(workspace, logs_index)

    parts = []

    if soul:
        parts.append(soul)
    if user:
        parts.append(user)
    if logs_index:
        parts.append(logs_index)
    if last_log:
        parts.append(last_log)

    if not parts:
        print(json.dumps({}))
        return

    context = "\n\n---\n\n".join(parts)

    if os.environ.get("CURSOR_PROJECT_DIR"):
        output = {"additional_context": context}
    else:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context,
            }
        }

    print(json.dumps(output))


if __name__ == "__main__":
    main()
