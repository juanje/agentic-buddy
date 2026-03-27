# Tool setup guide

Reference for the setup agent. Contains installation and configuration details
for the CLI tools used by the system. Read this during Step 4 of the setup
procedure.

This file is deleted along with the rest of `templates/` after setup completes.

---

## did — activity aggregator

[`did`](https://github.com/psss/did) gathers status reports from development
tools (Git, GitLab, GitHub, Jira, Bugzilla, etc.).

### Install

```bash
pip install did
```

### Configure

Create `~/.did/config`:

```ini
[general]
email = <user-email>

[git]
type = git
apps = /path/to/repos/*

[github]
type = github
url = https://api.github.com/
token = <github-token>
login = <github-username>

[gitlab]
type = gitlab
url = https://gitlab.example.com
token = <gitlab-token>

[jira]
type = jira
url = https://<instance>.atlassian.net
token = <jira-api-token>
user = <user-email>
project = <PROJECT_KEY>
```

Only include the sections for tools the user actually uses. The `[general]`
section is always required. See the
[did documentation](https://github.com/psss/did) for all available plugins
(Bugzilla, Pagure, Gerrit, Sentry, etc.).

### Test

```bash
did yesterday
did this week
did yesterday --jira       # filter by source
did yesterday --git        # faster, single source
```

If the user doesn't have `did` installed and doesn't want to install it now,
skip this section. The system works without it — standups and reviews will
rely on board + logs instead.

---

## jira-pending — current Jira state

Queries pending Jira tickets. Included in `scripts/jira-pending.sh`.

### Configure

1. Edit `scripts/jira-pending.sh` and set these variables:
   ```bash
   JIRA_URL="https://<instance>.atlassian.net"
   JIRA_USER="<user-email>"
   PROJECT="<PROJECT_KEY>"
   ```

2. Create a Jira API token:
   - Go to https://id.atlassian.com/manage-profile/security/api-tokens
   - Create a new token and copy it.

3. Save the token:
   ```bash
   mkdir -p ~/.did
   echo "<token>" > ~/.did/jira.token
   chmod 600 ~/.did/jira.token
   ```

4. Make executable and link:
   ```bash
   chmod +x scripts/jira-pending.sh
   mkdir -p ~/.local/bin
   ln -sf "$(pwd)/scripts/jira-pending.sh" ~/.local/bin/jira-pending
   ```

### Test

```bash
jira-pending assigned   # all open tickets assigned to me
jira-pending sprint     # my tickets in the current sprint
jira-pending summary    # count by status
```

### Subcommands

| Subcommand | What it returns |
|------------|----------------|
| `assigned` | All unresolved tickets assigned to the user |
| `sprint`   | User's tickets in the current open sprint |
| `new`      | Tickets assigned in the last 7 days |
| `updated`  | Tickets updated in the last 7 days |
| `blocked`  | Tickets with Blocked status or impediment label |
| `summary`  | Count of open tickets grouped by status |

---

## jira-detail — ticket details

Shows full ticket detail (description, comments, links). Included in
`scripts/jira-detail.sh`. Uses the same Jira credentials as `jira-pending`.

### Configure

1. Edit `scripts/jira-detail.sh` and set:
   ```bash
   JIRA_URL="https://<instance>.atlassian.net"
   JIRA_USER="<user-email>"
   ```
   (Same values as `jira-pending`. Token file is shared.)

2. Make executable and link:
   ```bash
   chmod +x scripts/jira-detail.sh
   mkdir -p ~/.local/bin
   ln -sf "$(pwd)/scripts/jira-detail.sh" ~/.local/bin/jira-detail
   ```

### Test

```bash
jira-detail PROJ-1234                  # full ticket detail
jira-detail PROJ-1234 --comments-only  # just comments
jira-detail PROJ-1234 --last 3         # last 3 comments
```

### Flags

| Flag | Effect |
|------|--------|
| `--comments-only` | Skip description and metadata, show only comments |
| `--last N` | Show last N comments (default: 5) |

---

## Non-Jira setups

If the user doesn't use Jira, the setup agent should:

1. **Remove** `scripts/jira-pending.sh` and `scripts/jira-detail.sh`.
2. **Remove** references to `jira-pending` and `jira-detail` from:
   - `templates/AGENTS.md` → "Getting work data" section
   - `agent_brain/skills/run-standup.md` → step 1 (remove `jira-pending` calls)
   - `agent_brain/skills/sync-board.md` → steps 1-3 (remove Jira cross-referencing, simplify to board-only sync)
   - `agent_brain/skills/weekly-review.md` → step 1 (remove `jira-pending` calls)
   - `agent_brain/skills/next-task.md` → step 3 (remove `jira-detail` call)
3. If the user has a **different issue tracker** with CLI tools, add those to
   the "Getting work data" section following the same format: tool name, what
   it does, basic syntax.
4. If the user has **no issue tracker CLI tools**, simplify the skills to work
   with board + logs only. The system still works — external tools are a bonus.

Similarly, if the user doesn't use `did`:

1. **Remove** `did` references from `templates/AGENTS.md` → "Getting work data".
2. **Remove** `did` calls from `agent_brain/skills/run-standup.md` and `agent_brain/skills/weekly-review.md`.
3. The standup and weekly review will rely on board + logs for activity data.
