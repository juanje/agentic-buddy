#!/usr/bin/env python3
"""
auto-reflect.py — Auto-reflect hook for Agentic Buddy.

Triggered by: sessionEnd/Stop (always), afterAgentResponse (with threshold).
Reads the conversation transcript, filters to user+assistant text, and
invokes the platform CLI to run the process-conversation skill.

Works on both Cursor and claude-code.

Dependencies: python3 (stdlib only), platform CLI (agent or claude)
"""

import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path


DEFAULT_REFLECT_THRESHOLD = 10
LOCK_NAME = "reflect.lock"
SKILL_PATH = Path("agent_brain/skills/process-conversation.md")


def resolve_workspace(hook_input: dict) -> Path:
    return Path(
        os.environ.get("CURSOR_PROJECT_DIR", "")
        or hook_input.get("cwd", "")
        or os.environ.get("CLAUDE_PROJECT_DIR", "")
        or os.getcwd()
    )


def state_dir(workspace: Path) -> Path:
    return workspace / ".cursor" / "hooks" / ".state"


def load_config(workspace: Path) -> dict:
    config_path = workspace / ".cursor" / "hooks" / "config.json"
    if config_path.exists():
        try:
            return json.loads(config_path.read_text())
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def read_file(path: Path) -> str:
    try:
        return path.read_text().strip()
    except (IOError, OSError):
        return ""


def read_hook_input() -> dict:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, IOError):
        return {}


def detect_platform(hook_input: dict) -> dict:
    """Resolve platform CLI and transcript path from env + stdin."""
    if os.environ.get("CURSOR_PROJECT_DIR"):
        return {
            "cli": "agent",
            "transcript": (
                hook_input.get("transcript_path")
                or os.environ.get("CURSOR_TRANSCRIPT_PATH", "")
            ),
        }
    return {
        "cli": "claude",
        "transcript": hook_input.get("transcript_path", ""),
    }


def load_state(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text())
        except (json.JSONDecodeError, IOError):
            pass
    return {"message_count": 0, "last_save_at": 0, "last_processed_line": 0}


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2) + "\n")


def filter_cursor_transcript(lines: list[str]) -> str:
    conversation = []
    for line in lines:
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        role = entry.get("role", "")
        content = entry.get("message", {}).get("content", [])
        if not isinstance(content, list):
            continue
        for block in content:
            if block.get("type") != "text":
                continue
            text = block.get("text", "").strip()
            if not text or text.startswith("<"):
                continue
            prefix = "USER" if role == "user" else "AGENT"
            conversation.append(f"{prefix}: {text}")
    return "\n\n".join(conversation)


def filter_claude_transcript(lines: list[str]) -> str:
    conversation = []
    skip_types = {
        "system",
        "attachment",
        "file-history-snapshot",
        "last-prompt",
        "permission-mode",
    }
    for line in lines:
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        entry_type = entry.get("type", "")
        if entry_type in skip_types:
            continue
        if entry_type == "user":
            content = entry.get("message", {}).get("content", "")
            if isinstance(content, str) and content.strip():
                conversation.append(f"USER: {content.strip()}")
            continue
        if entry_type == "assistant":
            content = entry.get("message", {}).get("content", [])
            if not isinstance(content, list):
                continue
            for block in content:
                if block.get("type") == "text":
                    text = block.get("text", "").strip()
                    if text:
                        conversation.append(f"AGENT: {text}")
    return "\n\n".join(conversation)


def filter_transcript(path: Path, cli: str, from_line: int = 0) -> tuple[str, int]:
    try:
        all_lines = path.read_text().splitlines()
    except IOError:
        return "", 0
    lines = all_lines[from_line:]
    if cli == "agent":
        return filter_cursor_transcript(lines), len(all_lines)
    return filter_claude_transcript(lines), len(all_lines)


def _is_pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def _acquire_lock(lock_file: Path) -> bool:
    if lock_file.exists():
        try:
            lock_data = json.loads(lock_file.read_text())
            pid = lock_data.get("pid", 0)
            if _is_pid_alive(pid):
                return False
        except (json.JSONDecodeError, IOError):
            pass
    return True


def _write_lock(lock_file: Path, pid: int) -> None:
    lock_file.parent.mkdir(parents=True, exist_ok=True)
    lock_file.write_text(json.dumps({"pid": pid}) + "\n")


def invoke_reflect_agent(cli: str, prompt: str, workspace: Path, lock_file: Path) -> bool:
    """Launch reflect agent in background."""
    if not _acquire_lock(lock_file):
        return False

    env = os.environ.copy()
    env["AB_MAINTENANCE"] = "1"
    cmd = [cli, "-p", prompt]
    if cli == "agent":
        cmd.extend(["--workspace", str(workspace), "--force"])
    else:
        cmd.extend(["--allowedTools", "Write", "Edit", "Bash(git *)"])
    try:
        proc = subprocess.Popen(
            cmd,
            env=env,
            cwd=str(workspace),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        _write_lock(lock_file, proc.pid)
        return True
    except (FileNotFoundError, OSError):
        return False


def build_reflect_prompt(workspace: Path, skill_content: str, filtered: str) -> str:
    today_str = date.today().isoformat()
    return (
        "You are a session processor for an Agentic Buddy instance.\n"
        f"The workspace root is {workspace}/.\n\n"
        "Run autonomously. No user interaction.\n\n"
        "Follow the process-conversation skill below, applied to the "
        "conversation transcript at the end of this prompt.\n\n"
        "Autonomous adaptations:\n"
        "- Skip Step 4 (patch stale active context) — the session is ending.\n"
        "- Always execute Step 6 (git commit).\n\n"
        f"--- SKILL: process-conversation ---\n{skill_content}\n--- END SKILL ---\n\n"
        "Apply the skill to this conversation (not the live session — use "
        "the transcript as your source of truth for what was discussed):\n\n"
        f"--- CONVERSATION ---\n{filtered}\n--- END ---\n\n"
        f'After writing, run: git add logs/ agent_brain/observations.md && '
        f'git commit -m "reflect: {today_str}" 2>/dev/null || true\n'
    )


def main() -> None:
    if os.environ.get("AB_MAINTENANCE") == "1":
        return

    hook_input = read_hook_input()
    workspace = resolve_workspace(hook_input)
    config = load_config(workspace)

    if config.get("reflect_enabled") is False:
        return

    threshold = config.get("auto_reflect_threshold", DEFAULT_REFLECT_THRESHOLD)
    platform = detect_platform(hook_input)

    transcript_path = (
        Path(platform["transcript"]) if platform["transcript"] else None
    )
    if not transcript_path or not transcript_path.exists():
        return

    today = date.today()
    transcript_mtime = date.fromtimestamp(transcript_path.stat().st_mtime)
    if transcript_mtime < today:
        return

    conversation_id = (
        hook_input.get("conversation_id")
        or hook_input.get("session_id")
        or "unknown"
    )

    state_path = state_dir(workspace)
    state_path.mkdir(parents=True, exist_ok=True)
    state_file = state_path / f"{conversation_id}.json"
    lock_file = state_path / LOCK_NAME
    state = load_state(state_file)

    hook_event = hook_input.get("hook_event_name", "")
    periodic_events = {"afterAgentResponse", "Stop"}
    forced_events = {"sessionEnd", "SessionEnd", "preCompact", "PreCompact"}
    is_periodic = hook_event in periodic_events
    is_forced = hook_event in forced_events

    if is_periodic:
        state["message_count"] += 1
        save_state(state_file, state)
        messages_since_save = state["message_count"] - state["last_save_at"]
        if messages_since_save < threshold:
            return

    if not is_periodic and not is_forced:
        return

    from_line = state["last_processed_line"]
    filtered, total_lines = filter_transcript(
        transcript_path, platform["cli"], from_line
    )
    if not filtered:
        return

    skill_content = read_file(workspace / SKILL_PATH)
    if not skill_content:
        skill_content = (
            "Extract decisions, tasks, ideas, lessons, and open threads "
            "into logs/YYYY-MM-DD.md and verify captures in agent_brain/ "
            "and user/."
        )

    prompt = build_reflect_prompt(workspace, skill_content, filtered)
    invoke_reflect_agent(platform["cli"], prompt, workspace, lock_file)

    state["last_save_at"] = state["message_count"]
    state["last_processed_line"] = total_lines
    save_state(state_file, state)


if __name__ == "__main__":
    main()
