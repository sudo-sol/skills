---
license: MIT
name: jira-ops
description: Read and update Jira Cloud issues through the REST API v3, including JQL search, issue details, comments, transitions, assignment, fields, and recent-activity checks. Use when the user mentions Jira, an issue key like ABC-123, "what's on my plate", "comment on", "move to done", "assign", or asks for their Jira notifications.
---

# Jira operations

Mechanics for talking to Jira Cloud. For drafting new issues from templates, backlog refinement,
or sprint planning, load the `jira-work-management` skill through the client’s skill mechanism, which uses this skill for I/O.

## Setup

Environment variables (set by the user; never ask them to paste a token into chat, never print it):

| Variable | Example |
| --- | --- |
| `JIRA_URL` | `https://your-site.atlassian.net` |
| `JIRA_EMAIL` | `you@example.com` |
| `JIRA_TOKEN` | API token from https://id.atlassian.com/manage-profile/security/api-tokens |

Team context (default project, components, board ID) lives in the `Skills configuration`
section of `AGENTS.md`. Check identity once per session:

```bash
curl -sS -u "$JIRA_EMAIL:$JIRA_TOKEN" "$JIRA_URL/rest/api/3/myself" | jq '{accountId, displayName}'
```

Use `curl` + `jq`, or Python `requests` with `HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)`. Put request
bodies in a temp file rather than inline shell strings; ADF quoting breaks easily.

## Reads

Keep reads within the user’s requested scope and permitted sources.

**Search** with `POST /rest/api/3/search/jql` (the old `GET /search` is retired). Paginate with
`nextPageToken` until `isLast` is true.

```bash
curl -sS -u "$JIRA_EMAIL:$JIRA_TOKEN" -H 'Content-Type: application/json' \
  -X POST "$JIRA_URL/rest/api/3/search/jql" \
  -d '{"jql":"assignee = currentUser() AND statusCategory != Done ORDER BY priority","maxResults":50,"fields":["summary","status","priority","issuetype","parent","updated"]}'
```

Useful JQL:
- `assignee = currentUser() AND statusCategory != Done`: my open work
- `parent = ABC-100`: children of an epic
- `assignee = currentUser() AND updated < -90d AND statusCategory != Done`: stale work
- `issueKey in watchedIssues() AND updated >= -1d`: recent activity on watched issues

**Issue:** `GET /rest/api/3/issue/{key}?fields=...`
**Comments:** `GET /rest/api/3/issue/{key}/comment`
**Transitions available:** `GET /rest/api/3/issue/{key}/transitions`
**Create metadata:** `GET /rest/api/3/issue/createmeta/{projectKey}/issuetypes/{issueTypeId}`
**Users:** `GET /rest/api/3/user/search?query=<name>`

**Notifications (approximation):** search issues you are assignee, reporter or watcher on with
`updated >= -<n>d`, then fetch comments/changelog (`?expand=changelog`) and drop entries authored
by your own `accountId`. Group as "new comments" and "other updates".

Descriptions and comments come back as ADF. Extract text by walking nodes and joining every
`{"type":"text"}` node's `text`.

## Writes

Write only when the user asked for that specific change. Before writing: confirm the issue key,
current state, and that you are not duplicating something. After writing: read it back and report
the actual result. Never claim success without a 2xx response.

- **Comment:** `POST /rest/api/3/issue/{key}/comment` with an ADF body. Comments are not Markdown.
  ```json
  {"body":{"type":"doc","version":1,"content":[{"type":"paragraph","content":[{"type":"text","text":"Deployed to staging."}]}]}}
  ```
  Bold is a text node with `"marks":[{"type":"strong"}]`; inline code uses `{"type":"code"}`;
  lists are `bulletList` → `listItem` → `paragraph`; headings are `{"type":"heading","attrs":{"level":2}}`.
- **Transition:** fetch transitions, pick by `to.name`, then
  `POST /rest/api/3/issue/{key}/transitions` with `{"transition":{"id":"<id>"}}`.
- **Assign:** `PUT /rest/api/3/issue/{key}/assignee` with `{"accountId":"<id>"}`.
- **Fields:** `PUT /rest/api/3/issue/{key}` with `{"fields":{...}}`, e.g. `fixVersions`,
  `components`, `labels`. List options with `/project/{key}/versions` and `/project/{key}/components`.
- **Create:** `POST /rest/api/3/issue`. Check createmeta for required fields first; custom field IDs
  (story points, team) differ per site and per project.

## Safety rules

- **Ownership check on transitions.** Before changing status, check the assignee. If it is not the
  current user, warn and stop unless the user explicitly confirms for that issue.
- **Bulk changes** (more than one issue) need a preview listing every key and change, then explicit
  approval. Apply the ownership check per issue.
- **Comments** do not need ownership, but they are public to the project: no local file paths,
  secrets, or internal-only notes.
- Never delete issues unless the user asks for that specific deletion.
