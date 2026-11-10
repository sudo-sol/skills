# MR/PR triage rules: <repo name>

Copy to `<repo>/.agents/mr-triage-rules.md` and replace the examples with your team's real
policy. Date every baseline. Each rule records the share of requests it flagged when tested.

**Repo:** `<owner/repo or group/project>`  **Host:** GitHub | GitLab
**Baselines measured:** YYYY-MM-DD over <N> requests

## 🔴 REDIRECT

| Rule | Match | Flag rate | Canned reply |
| --- | --- | --- | --- |
| Access/membership requests go through the ticketing system | diff edits a member/username list (e.g. Terraform `*_team_members` `usernames = [...]`) | <x%> | see below |

Canned reply (draft only, never posted by the agent):

> @<author> Thanks for this. We handle group membership changes through <system> rather than
> code changes, so access is approved and audited in one place. Could you raise a request here:
> <link>? Guide: <link>.

## 🟡 SCRUTINY (strongest first)

| # | Signal | How to match | Flag rate | Why it matters |
| --- | --- | --- | --- | --- |
| 1 | Resource or access declaration removed | `grep -E '^-.*resource "(<type_a>\|<type_b>)"'` | | access or infra disappears |
| 2 | State manipulation | added `moved {}`, `import {}`, `removed {}` blocks | | wrong address can destroy/recreate |
| 3 | Foundation/shared file touched | path in: `<file>`, `<file>` | | org-wide blast radius |
| 4 | Credential surface | tokens, variables marked sensitive | | secrets exposure |
| 5 | Runtime/version/execution settings modified | require a **removed** line matching the keyword | | past outages |
| 6 | Policy-as-code or exemptions | policy set paths, "exempt"/"bypass" | | governance |
| 7 | Many files | > <n> files (typical is <n>) | | unusual shape |

## 🟢 ROUTINE (house pattern)

All of: <e.g. one team-named file, pure additions, the team and the resource declared in the same file>.

## Deliberately not flagged

| Signal | Why not | Decided |
| --- | --- | --- |
| <e.g. admin access on own resources> | <x%> of grants; flagging it flags everything | YYYY-MM-DD |

## Known gaps

- <request IDs the rules got wrong, and the open question for the team>
