---
license: MIT
name: setup-skills
description: Configure a repo for the skills collection by writing a "Skills configuration" section into AGENTS.md.
disable-model-invocation: true
---

# Setup skills

Run once per repo. Writes the configuration the other skills read, so none of them hard-code
paths, sites, or team details.

## Steps

1. Read the repo's `AGENTS.md` (create it if missing; if only `CLAUDE.md` exists, ask which file
   to use). Look for an existing `## Skills configuration` section and keep its values as defaults.
2. Ask the questions below **in one grouped prompt**. Offer the default in brackets. Skip groups
   the user says they will not use.
3. Show the resulting section and ask for confirmation before writing.
4. Write or update only that section. Preserve everything else in the file.
5. Create only the directories the user confirmed (e.g. memory root, journal dir). Do not create
   placeholder content.
6. If the user wants journal or memory content kept private, add those paths to `.gitignore` and
   check `git ls-files` that nothing there is already tracked.

## Questions

- **Memory** (`memory-bank`): memory root [`memory/`]. Private (gitignored)? [no]
- **Journal** (`daily-check-in`): journal dir [`journal/daily/`], achievements file [none],
  template [the template bundled with `daily-check-in`], sync [`none` | `git`].
  Git mode still requires explicit authorization for pull, commit, and push.
- **Voice** (`drafting-for-others`): tone notes, punctuation to avoid [em dashes], sign-off
- **Standards** (`standards-check`): standards dir [`docs/standards/`], source (wiki space, repo, URL)
- **Review queue** (`mr-policy-triage`): host [GitHub | GitLab], repo, rules file
  [`.agents/mr-triage-rules.md`]
- **Atlassian** (`jira-ops`, `jira-work-management`, `confluence-ops`): site URL, default project,
  board ID, default labels/component/fix version/team, whether tasks are estimated [no],
  default Confluence space. Leave unknown site-specific values unset.
  Credentials are **never** written here; they stay in environment variables.

## Section format

```markdown
## Skills configuration

- memory_root: memory/
- journal_dir: journal/daily/
- journal_template:
- achievements_file:
- journal_sync: none
- voice: warm, direct; no em dashes
- standards_dir: docs/standards/
- standards_source:
- mr_host: github
- mr_repo:
- mr_triage_rules: .agents/mr-triage-rules.md
- jira_site:
- jira_default_project:
- jira_board_id:
- jira_default_labels: []
- jira_default_component:
- jira_default_fix_version:
- jira_default_team:
- jira_estimate_tasks: false
- confluence_default_space:
```

Unset `journal_template` uses the journal template bundled with `daily-check-in`;
an override is relative to the consumer repo. Empty `achievements_file` disables highlights.
Empty standards source means local-only standards. Empty review repo means the current Git
repository; without a known host or rules, ask rather than invent policy. Empty Jira site
uses `JIRA_URL`; other unset Jira or Confluence values must be resolved when needed.
Labels default to an empty list; unset component, fix version, and team add no defaults.
`jira_estimate_tasks` defaults to false and controls whether to ask for task estimates.
Priority and assignee are always per ticket; story points are required only for estimated
issue types. Users may explicitly choose unassigned or no estimate where supported.
