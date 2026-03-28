#!/bin/bash
# Query pending tickets from Jira Cloud (Atlassian)
# Uses POST /rest/api/3/search/jql (Atlassian Cloud endpoint)
#
# Setup:
#   1. Edit the variables below with your Jira details.
#   2. Create the token file with your Jira API token.
#   3. chmod +x scripts/jira-pending.sh
#   4. ln -s "$(pwd)/scripts/jira-pending.sh" ~/.local/bin/jira-pending

# --- Configuration (edit these) ---
JIRA_URL="https://your-instance.atlassian.net"
JIRA_USER="your.email@example.com"
JIRA_TOKEN_FILE="$HOME/.did/jira.token"
PROJECT="YOUR_PROJECT"
# -----------------------------------

JIRA_TOKEN=$(cat "$JIRA_TOKEN_FILE" 2>/dev/null)
if [[ -z "$JIRA_TOKEN" ]]; then
    echo "Error: token not found in $JIRA_TOKEN_FILE" >&2
    exit 1
fi

ACTION="${1:-assigned}"

case "$ACTION" in
    assigned)
        JQL="assignee = currentUser() AND resolution = Unresolved AND project = $PROJECT ORDER BY priority DESC"
        ;;
    sprint)
        JQL="assignee = currentUser() AND sprint in openSprints() AND project = $PROJECT ORDER BY status"
        ;;
    new)
        JQL="assignee = currentUser() AND created >= -7d AND project = $PROJECT ORDER BY created DESC"
        ;;
    updated)
        JQL="assignee = currentUser() AND updated >= -7d AND project = $PROJECT ORDER BY updated DESC"
        ;;
    blocked)
        JQL="assignee = currentUser() AND (status = Blocked OR labels = impediment) AND project = $PROJECT"
        ;;
    summary)
        curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
            -X POST -H "Content-Type: application/json" \
            -d "{\"jql\":\"assignee = currentUser() AND resolution = Unresolved AND project = $PROJECT\",\"maxResults\":200,\"fields\":[\"status\"]}" \
            "$JIRA_URL/rest/api/3/search/jql" \
            | python3 -c "
import sys, json
from collections import Counter
data = json.load(sys.stdin)
issues = data.get('issues', [])
counts = Counter(i['fields']['status']['name'] for i in issues)
total = len(issues)
for status, count in sorted(counts.items(), key=lambda x: -x[1]):
    print(f'{status:<20} {count}')
print(f'{\"\":-<20} {\"\":-<3}')
print(f'{\"Total\":<20} {total}')
"
        exit 0
        ;;
    *)
        echo "Usage: $(basename "$0") [assigned|sprint|new|updated|blocked|summary]"
        exit 1
        ;;
esac

curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
    -X POST -H "Content-Type: application/json" \
    -d "{\"jql\":\"$JQL\",\"maxResults\":50,\"fields\":[\"summary\",\"status\",\"priority\"]}" \
    "$JIRA_URL/rest/api/3/search/jql" \
    | python3 -c "
import sys, json
data = json.load(sys.stdin)
issues = data.get('issues', [])
if not issues:
    print('No issues found.')
    sys.exit(0)
for issue in issues:
    key = issue['key']
    fields = issue['fields']
    summary = fields.get('summary', '')
    status = fields.get('status', {}).get('name', '?')
    priority = fields.get('priority', {}).get('name', '?')
    print(f'{key:<16} {status:<15} {priority:<10} {summary}')
"
