---
license: MIT
name: standards-check
description: Find, cache, and apply an organization's engineering standards (RFCs, ADRs, policies, guidelines) to the current work, and report which ones apply with evidence. Use when designing, reviewing a PR/MR, writing docs or runbooks, touching auth, IAM, secrets, logging, CI/CD, infrastructure-as-code, APIs, containers or dependencies, or when the user asks "which standards apply" or "pull RFC-N".
---

# Standards check

Keep a local, versioned cache of the standards that govern this codebase, and check new work
against them before it ships. The output is an applicability statement with evidence, not a
compliance stamp.

## Configuration

From the `Skills configuration` section of `AGENTS.md`:

- `standards_dir` (default `docs/standards/`): local cache and catalog
- `standards_source`: where originals live (a wiki space, a repo path, a URL). Optional.
- If the source is Confluence, load the `confluence-ops` skill through the client’s skill mechanism for retrieval.

## Catalog

Examples below are fictional format illustrations, including IDs, versions, dates, and
requirements. They are not retrieved standards or evidence of an employer policy.

`<standards_dir>/README.md` is the master index:

```markdown
| ID | Title | Source | Version | Pulled | Topics |
|----|-------|--------|---------|--------|--------|
| RFC-12 | Secrets management | <link> | 7 | 2026-01-10 | secret, vault, credential |
```

Each cached document is `<ID>-<slug>.md` and starts with:

```markdown
# <ID> <Title>
**Source:** <link>   **Version:** <n>   **Last updated:** <date, author>   **Pulled:** <YYYY-MM-DD>
---
```

The `Topics` column is the keyword map used for proactive checks. Keep it short and accurate.

## Workflow

1. **Match.** Compare the task's topics (files touched, services, keywords) against the catalog.
2. **Classify each candidate** as one of:
   - **Confirmed applicable**: you read the relevant section and it governs this work.
   - **Candidate**: topic matches but you have not read it, or it is ambiguous.
   - **Missing source**: the catalog references it but no local copy or access exists.
3. **Freshen when it matters.** If a confirmed standard drives a decision and the source is
   reachable, compare the remote version with the cached one and re-pull if newer.
4. **Apply.** Quote or cite the specific requirement (ID + section) next to each finding.
5. **Report** before making changes:

```
Applicable standards
- RFC-12 Secrets management (v7, pulled 2026-01-10) — confirmed: §3 forbids static keys in CI vars.
- RFC-30 Package publishing — candidate: touches package.json; not yet read.
- RFC-45 Authentication — missing source: listed in catalog, no local copy.
Not checked: <what you did not look at>
```

## Rules

- Never invent a standard, a section, or compliance. If you have not read it, it is a candidate.
- A cached copy is dated evidence, not live truth; show the pulled date.
- Follow the task's limits: if the user said "local only", do not fetch remote sources.
- Reference applicable standards in deliverables (PR description, design doc, runbook) when relevant.
- Pulling a document into the cache is a local write; publishing anything back to the source is
  a separate, explicit request.
