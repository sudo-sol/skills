---
license: MIT
name: confluence-ops
description: Search, read, create, update, and track Confluence Cloud pages through the REST API, converting between storage-format HTML and Markdown. Use when the user mentions Confluence, a wiki page or space, asks to pull a page for reference, draft or publish documentation, search with CQL, or see recent page changes.
---

# Confluence operations

Mechanics for Confluence Cloud. Uses the same Atlassian credentials as `jira-ops`.

## Setup

Environment variables (never ask the user to paste a token into chat, never print it):
`JIRA_URL` (or `CONFLUENCE_URL`) like `https://your-site.atlassian.net`, `JIRA_EMAIL`, `JIRA_TOKEN`.
Use `CONFLUENCE_URL` when set, otherwise `JIRA_URL`; strip a trailing slash and append
`/wiki` only if it is not already present. Team spaces and a default space live in the `Skills
configuration` section of `AGENTS.md`.

## Reads

- **Page by ID:** `GET /wiki/api/v2/pages/{id}?body-format=storage` (title, version, body).
  A page URL contains its ID: `.../wiki/spaces/<SPACE>/pages/<id>/<slug>`.
- **Search (CQL):** `GET /wiki/rest/api/search?cql=<url-encoded>&limit=25`
  e.g. `type=page AND space=DOCS AND title~"onboarding"`, `label="runbook"`, `text~"rotation"`.
- **Children:** `GET /wiki/api/v2/pages/{id}/children`
- **Current user / personal space:** `GET /wiki/rest/api/user/current?expand=personalSpace`.
  Use the returned `personalSpace.key` when present; do not construct it from an account ID.
  A personal space may not exist or may be unavailable to the caller.

To read a page as Markdown, fetch the storage body and convert it (e.g. Python `markdownify`, or
`pandoc -f html -t gfm`). Macros (`<ac:...>`) will not convert cleanly; keep their text and note
what was dropped. Save pulled pages with a header recording source URL, version and pull date.

**Recent changes (approximation):** CQL `space in (<keys>) AND lastmodified >= startOfDay("-1d")` plus
`contributor = currentUser() AND lastmodified >= startOfDay("-7d")`, then drop items last edited by you.
These windows start at midnight in the configured Confluence timezone, not exactly 24 or
168 hours ago. Follow pagination links when a complete result set is needed.

## Writes

Write only on an explicit request for that page. Confirm target space/parent and title, check for
an existing page with the same title, then read the result back and report the URL and version.

- **Body format is storage HTML, not Markdown.** Convert Markdown first
  (e.g. `pandoc -f gfm -t html`). For large bodies, write to a file and send the file.
- **Create:** `POST /wiki/api/v2/pages` with
  `{"spaceId":"<id>","status":"current","title":"...","parentId":"<id>","body":{"representation":"storage","value":"<html>"}}`.
  Get `spaceId` from `GET /wiki/api/v2/spaces?keys=<KEY>`.
- **Update:** read current version, then `PUT /wiki/api/v2/pages/{id}` with `id`, `status`, `title`,
  body, and `"version":{"number": current + 1}`. A version conflict means someone else edited;
  re-read and merge rather than overwrite.
- **Attachments:** `POST /wiki/rest/api/content/{id}/child/attachment` (multipart, header
  `X-Atlassian-Token: no-check`).
- **Diagrams:** if `mmdc` (Mermaid CLI) is installed, render Mermaid to SVG/PNG, upload as an
  attachment, and embed with `<ac:image><ri:attachment ri:filename="x.svg"/></ac:image>`.
  Otherwise fall back to a code block.

## Safety rules

- Keep reads within the user’s requested scope and permitted sources. Creates and updates need
  an explicit request; bulk edits (more than one
  page) need a preview and approval.
- Never move or delete pages unless asked for that specific page; a "move" across spaces may
  create a new page ID and break links, so say so first.
- Preserve other people's content on update. Never overwrite a newer version.
- Published pages are team-visible: no local file paths, secrets, or private notes.
