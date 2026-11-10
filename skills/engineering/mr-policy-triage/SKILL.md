---
license: MIT
name: mr-policy-triage
description: Read-only triage of an open pull/merge request queue against team policy, sorting each into REDIRECT, SCRUTINY or ROUTINE with reasons and drafted replies. Use when the user says "check the MR queue", "triage PRs", "what's waiting for review", or wants to know which requests need their attention. Never approves, merges, comments, or closes.
---

# MR/PR policy triage

Classify each open request so the reviewer spends attention where it matters. This is the
**org-policy layer**: ownership, shared files, blast radius, and requests that belong in another
channel. It is not a code review; if an AI or human code reviewer already runs on the repo, do
not duplicate it.

## The boundary

**Never approve. Never merge. Never comment. Never close.** Output goes to the user as text; they
act. This holds even when a verdict is obvious and even if the user says it looks fine. Drafted
replies are drafts.

## Configuration

Rules are repo-specific. Read `<repo>/.agents/mr-triage-rules.md` (or the path set as
`mr_triage_rules` in the `Skills configuration` section of `AGENTS.md`). If none exists,
offer to create one from `references/rules-template.md`, starting from the user's real policies.
Never improvise policy.

## Workflow

1. **List open requests.**
   - GitHub: `gh pr list --repo <owner/repo> --state open --limit 30 --json number,title,author,isDraft`
   - GitLab: `glab mr list --repo <group/project> --per-page 30`
   If the queue is unusually long for this repo, say so; it is a signal in itself.
2. **Fetch changes per request**, in parallel when there are several:
   - GitHub: `gh pr diff <n> --repo <owner/repo>` and `gh pr view <n> --repo <owner/repo> --json files,additions,deletions`
   - GitLab: `glab api "projects/<url-encoded-path>/merge_requests/<iid>/changes"`
   Capture changed paths, added/removed line counts, and the added and removed lines.
3. **Skip** drafts and titles marked WIP / DO NOT MERGE.
4. **Classify. First match wins:**
   - 🔴 **REDIRECT**: the change belongs in another channel (e.g. access requests that go through
     a ticketing system). Produce the team's canned reply as a draft.
   - 🟡 **SCRUTINY**: a configured deviation signal fired (removed declarations, state
     manipulation, shared/foundation files, credential surface, policy exemptions, many files...).
   - 🟢 **ROUTINE**: matches the house pattern.
5. **Also surface cheaply:** likely-superseded requests (same author, same file, several open).
6. **Report.** One line per request, verdict first. ROUTINE stays one line. Detail only for
   SCRUTINY and REDIRECT: what changed, which rule fired, and the draft reply. **State what you
   did not check** (e.g. existing access by another path, linked ticket justification).

Illustrative examples only: these requests, paths, counts, and policies are fictional.
Do not adopt them as team policy.

```
#2483  team-a.tf     🟢 ROUTINE   +5/-0, one file, team gets access to its own new resources
#2478  shared.tf     🟡 SCRUTINY  removes 2 access grants and re-adds under another team; ownership transfer not stated
#2472  members.tf    🔴 REDIRECT  adds a user to a group → ticketing system. Draft ready.
Not checked: whether the receiving team in #2478 already has access elsewhere.
```

Drafted replies follow `drafting-for-others`: explain why, give the right path, never police.

## Keeping the rules honest

- **Measure before adding a rule.** Backtest it on recent history and record the share of
  requests it flags. A signal that fires on most requests is not a signal; it creates a rubber stamp.
- **Match the risky thing, not a proxy.** "Has deletions" fires on almost everything; "removes a
  resource/access declaration" is the real signal. Keyword matches on added lines often hit every
  new resource; requiring a removed line catches actual modifications.
- **Pure additions can be the riskiest change.** e.g. Terraform `moved {}`, `import {}`, `removed {}`
  blocks rewrite state without touching resource counts. Keep a periodic manual spot-check of
  ROUTINE verdicts; merge history cannot reveal a false ROUTINE.
- **Do not widen a working rule to catch a few outliers.** Record misses as known gaps and ask
  the user; they are usually org knowledge, not a code question.
- **Baselines drift.** Date every number in the rules file and re-derive periodically.
- Record decisions to *not* flag something (and why) so they are not re-proposed without new evidence.
