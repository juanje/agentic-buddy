#!/usr/bin/env python3
"""
auto-consolidate.py — Auto-consolidation hook for Agentic Buddy.

Triggered by: sessionStart/SessionStart.
Checks usage-based cycle thresholds and spawns a background agent to run
/daily, /weekly, or /monthly as appropriate.

Works on both Cursor and claude-code.

Dependencies: python3 (stdlib only), platform CLI (agent or claude)
"""

import json
import os
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path


LOCK_NAME = "consolidate.lock"
STATE_FILE = "consolidate.json"
DAILY_HOURS_THRESHOLD = 24
WEEKLY_DAILIES_THRESHOLD = 7
MONTHLY_DAILIES_THRESHOLD = 28
MONTHLY_DAILIES_ALT_THRESHOLD = 21
MONTHLY_WEEKLIES_ALT_THRESHOLD = 3

SKILLS = {
    "daily": Path("agent_brain/skills/daily-consolidation.md"),
    "weekly": Path("agent_brain/skills/weekly-review.md"),
    "monthly": Path("agent_brain/skills/monthly-maintenance.md"),
}


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


def detect_cli() -> str:
    return "agent" if os.environ.get("CURSOR_PROJECT_DIR") else "claude"


def default_consolidate_state() -> dict:
    return {
        "last_daily": "",
        "last_weekly": "",
        "last_monthly": "",
        "dailies_since_weekly": 0,
        "dailies_since_monthly": 0,
        "weeklies_since_monthly": 0,
    }


def load_consolidate_state(path: Path) -> dict:
    if path.exists():
        try:
            data = json.loads(path.read_text())
            base = default_consolidate_state()
            base.update(data)
            return base
        except (json.JSONDecodeError, IOError):
            pass
    return default_consolidate_state()


def save_consolidate_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2) + "\n")


def parse_log_dates(logs_dir: Path) -> list[date]:
    if not logs_dir.is_dir():
        return []
    dates = []
    for path in logs_dir.glob("*.md"):
        if path.name == "index.md" or path.name.startswith("monthly_"):
            continue
        match = re.match(r"(\d{4}-\d{2}-\d{2})\.md$", path.name)
        if match:
            try:
                dates.append(date.fromisoformat(match.group(1)))
            except ValueError:
                continue
    return sorted(dates)


def has_content_since(log_dates: list[date], since: str) -> bool:
    if not log_dates:
        return False
    if not since:
        return True
    try:
        since_date = date.fromisoformat(since)
    except ValueError:
        return True
    return any(d > since_date for d in log_dates)


def hours_since(date_str: str) -> float:
    if not date_str:
        return float("inf")
    try:
        last = datetime.fromisoformat(date_str)
    except ValueError:
        return float("inf")
    # Treat stored date as start of that calendar day
    last = datetime.combine(last.date(), datetime.min.time())
    return (datetime.now() - last).total_seconds() / 3600


def determine_cycle(state: dict, log_dates: list[date], config: dict) -> str | None:
    """Return highest due cycle: monthly > weekly > daily, or None."""
    daily_hours = config.get("daily_hours_threshold", DAILY_HOURS_THRESHOLD)
    weekly_dailies = config.get("weekly_dailies_threshold", WEEKLY_DAILIES_THRESHOLD)
    monthly_dailies = config.get("monthly_dailies_threshold", MONTHLY_DAILIES_THRESHOLD)
    monthly_dailies_alt = config.get(
        "monthly_dailies_alt_threshold", MONTHLY_DAILIES_ALT_THRESHOLD
    )
    monthly_weeklies_alt = config.get(
        "monthly_weeklies_alt_threshold", MONTHLY_WEEKLIES_ALT_THRESHOLD
    )

    daily_due = (
        hours_since(state["last_daily"]) >= daily_hours
        and has_content_since(log_dates, state["last_daily"])
    )
    weekly_due = state["dailies_since_weekly"] >= weekly_dailies
    monthly_due = state["dailies_since_monthly"] >= monthly_dailies or (
        state["dailies_since_monthly"] >= monthly_dailies_alt
        and state["weeklies_since_monthly"] >= monthly_weeklies_alt
    )

    if monthly_due:
        return "monthly"
    if weekly_due:
        return "weekly"
    if daily_due:
        return "daily"
    return None


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


def invoke_consolidation_agent(
    cli: str, prompt: str, workspace: Path, lock_file: Path
) -> bool:
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


def build_consolidation_prompt(
    workspace: Path, cycle: str, skill_content: str
) -> str:
    today_str = date.today().isoformat()
    commit_msgs = {
        "daily": f'daily: {today_str}',
        "weekly": f'weekly: {today_str}',
        "monthly": f'monthly: {today_str}',
    }
    commit_msg = commit_msgs[cycle]
    return (
        "You are a maintenance agent for an Agentic Buddy instance.\n"
        f"The workspace root is {workspace}/.\n\n"
        "Run autonomously. No user interaction. Log all decisions made.\n"
        "Do not ask for approval — git history is the correction mechanism.\n\n"
        f"Execute the {cycle} consolidation cycle using the skill below.\n"
        "The skill may cascade into prerequisite cycles (weekly includes "
        "daily, monthly includes weekly) — follow the skill's own steps.\n\n"
        f"--- SKILL: {cycle} ---\n{skill_content}\n--- END SKILL ---\n\n"
        f'When done, commit: git add CLAUDE.md agent_brain/ logs/ user/ && '
        f'git commit -m "{commit_msg}" 2>/dev/null || true\n'
    )


def update_state_after_trigger(state: dict, cycle: str) -> dict:
    today_str = date.today().isoformat()
    if cycle == "daily":
        state["last_daily"] = today_str
        state["dailies_since_weekly"] = state.get("dailies_since_weekly", 0) + 1
        state["dailies_since_monthly"] = state.get("dailies_since_monthly", 0) + 1
    elif cycle == "weekly":
        state["last_weekly"] = today_str
        state["dailies_since_weekly"] = 0
        state["weeklies_since_monthly"] = state.get("weeklies_since_monthly", 0) + 1
    elif cycle == "monthly":
        state["last_monthly"] = today_str
        state["dailies_since_monthly"] = 0
        state["dailies_since_weekly"] = 0
        state["weeklies_since_monthly"] = 0
    return state


def main() -> None:
    if os.environ.get("AB_MAINTENANCE") == "1":
        return

    hook_input = read_hook_input()
    workspace = resolve_workspace(hook_input)
    config = load_config(workspace)

    if config.get("consolidation_enabled") is False:
        return

    state_path = state_dir(workspace)
    state_file = state_path / STATE_FILE
    lock_file = state_path / LOCK_NAME
    state = load_consolidate_state(state_file)

    log_dates = parse_log_dates(workspace / "logs")
    cycle = determine_cycle(state, log_dates, config)
    if not cycle:
        return

    skill_path = SKILLS[cycle]
    skill_content = read_file(workspace / skill_path)
    if not skill_content:
        print(f"auto-consolidate: missing skill {skill_path}", file=sys.stderr)
        return

    prompt = build_consolidation_prompt(workspace, cycle, skill_content)

    if not invoke_consolidation_agent(detect_cli(), prompt, workspace, lock_file):
        return

    state = update_state_after_trigger(state, cycle)
    save_consolidate_state(state_file, state)


if __name__ == "__main__":
    main()
