#!/bin/bash
# Show details of a Jira ticket (description, status, comments, links)
# Companion to jira-pending. Uses the same credentials.
# Query pending tickets from Jira Cloud (Atlassian)
# Uses POST /rest/api/3/search/jql (Atlassian Cloud endpoint)
#
# Setup:
#   1. Edit the variables below with your Jira details.
#   2. Create the token file with your Jira API token.
#   3. chmod +x scripts/jira-detail.sh
#   4. ln -s "$(pwd)/scripts/jira-detail.sh" ~/.local/bin/jira-detail

# --- Configuration (edit these) ---
JIRA_URL="https://your-instance.atlassian.net"
JIRA_USER="your.email@example.com"
JIRA_TOKEN_FILE="$HOME/.did/jira.token"

JIRA_TOKEN=$(cat "$JIRA_TOKEN_FILE" 2>/dev/null)
if [[ -z "$JIRA_TOKEN" ]]; then
    echo "Error: token not found in $JIRA_TOKEN_FILE" >&2
    exit 1
fi

ISSUE_KEY="${1:-}"
if [[ -z "$ISSUE_KEY" ]]; then
    echo "Usage: $(basename "$0") ISSUE-KEY [--comments-only] [--last N]"
    echo ""
    echo "Options:"
    echo "  --comments-only   Show only comments, skip description and metadata"
    echo "  --last N          Show last N comments (default: 5)"
    exit 1
fi

COMMENTS_ONLY=false
LAST_N=5
shift
while [[ $# -gt 0 ]]; do
    case "$1" in
        --comments-only) COMMENTS_ONLY=true; shift ;;
        --last) LAST_N="$2"; shift 2 ;;
        *) shift ;;
    esac
done

FIELDS="summary,status,priority,description,comment,labels,issuelinks,created,updated,assignee,reporter"

RESULT=$(curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
    "$JIRA_URL/rest/api/3/issue/$ISSUE_KEY?fields=$FIELDS")

echo "$RESULT" | COMMENTS_ONLY="$COMMENTS_ONLY" LAST_N="$LAST_N" python3 -c '
import sys, json, os

def adf_to_text(node):
    """Extract plain text from Atlassian Document Format."""
    if isinstance(node, str):
        return node
    if not isinstance(node, dict):
        return ""

    text = node.get("text", "")
    node_type = node.get("type", "")

    if node_type == "hardBreak":
        return "\n"

    children = node.get("content", [])
    child_text = "".join(adf_to_text(c) for c in children)

    if node_type == "paragraph":
        return child_text + "\n"
    if node_type in ("bulletList", "orderedList"):
        return child_text
    if node_type == "listItem":
        return "  - " + child_text
    if node_type == "heading":
        level = node.get("attrs", {}).get("level", 1)
        return "#" * level + " " + child_text + "\n"
    if node_type == "codeBlock":
        return "```\n" + child_text + "```\n"
    if node_type == "blockquote":
        lines = child_text.strip().split("\n")
        return "\n".join("> " + l for l in lines) + "\n"
    if node_type == "mention":
        return "@" + node.get("attrs", {}).get("text", "?")
    if node_type == "inlineCard":
        return node.get("attrs", {}).get("url", "")

    return text + child_text


comments_only = os.environ.get("COMMENTS_ONLY") == "true"
last_n = int(os.environ.get("LAST_N", "5"))

data = json.load(sys.stdin)

if "errors" in data or "errorMessages" in data:
    msgs = data.get("errorMessages", []) or [str(data.get("errors", {}))]
    err = "; ".join(msgs)
    print(f"Error: {err}", file=sys.stderr)
    sys.exit(1)

fields = data["fields"]
sep = "=" * 70
thin = "-" * 70

if not comments_only:
    key = data["key"]
    summary = fields.get("summary", "?")
    status = fields.get("status", {}).get("name", "?")
    priority = fields.get("priority", {}).get("name", "?")
    labels = ", ".join(fields.get("labels", [])) or "-"
    assignee = (fields.get("assignee") or {}).get("displayName", "Unassigned")
    reporter = (fields.get("reporter") or {}).get("displayName", "?")
    created = fields.get("created", "?")[:10]
    updated = fields.get("updated", "?")[:10]

    print(sep)
    print(f"{key}  {summary}")
    print(sep)
    print(f"Status: {status}  |  Priority: {priority}  |  Labels: {labels}")
    print(f"Assignee: {assignee}  |  Reporter: {reporter}")
    print(f"Created: {created}  |  Updated: {updated}")

    links = fields.get("issuelinks", [])
    if links:
        print(f"\nLinks:")
        for link in links:
            if "outwardIssue" in link:
                other = link["outwardIssue"]
                direction = link.get("type", {}).get("outward", "?")
            elif "inwardIssue" in link:
                other = link["inwardIssue"]
                direction = link.get("type", {}).get("inward", "?")
            else:
                continue
            other_key = other.get("key", "?")
            other_summary = other.get("fields", {}).get("summary", "?")
            other_status = other.get("fields", {}).get("status", {}).get("name", "?")
            print(f"  {direction} {other_key} [{other_status}] {other_summary}")

    desc = fields.get("description")
    print(f"\n{thin}")
    print("Description:")
    print(thin)
    if desc:
        print(adf_to_text(desc).strip())
    else:
        print("(no description)")

comments = fields.get("comment", {}).get("comments", [])
if comments:
    shown = comments[-last_n:]
    total = len(comments)
    print(f"\n{thin}")
    print(f"Comments ({total} total, showing last {len(shown)}):")
    print(thin)
    for c in shown:
        author = c.get("author", {}).get("displayName", "?")
        ts = c.get("created", "?")[:16].replace("T", " ")
        body = adf_to_text(c.get("body", {})).strip()
        print(f"\n  [{ts}] {author}:")
        for line in body.split("\n"):
            print(f"    {line}")
elif not comments_only:
    print("\n(no comments)")
'
