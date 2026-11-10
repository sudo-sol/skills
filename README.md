# skills

Practical agent workflows for the work surrounding a code change: recover project context,
prepare a review, maintain operational documents, and keep Jira and Confluence up to date.
The collection also includes a work journal and guidance for drafting messages.

Start with the task you need help with. Each entry below opens the instructions the agent
will follow; review them before giving it access to your project or accounts.

## Background

I drafted and used these skills in my own work. When preparing this collection for public
release, I used [mattpocock/skills](https://github.com/mattpocock/skills) as a reference for
repository structure and packaging. This collection reflects my own workflows and is
maintained separately. See [acknowledgements and retained notices](./THIRD_PARTY_NOTICES.md).

## Find a workflow

| Your task | Skill | Result |
| --- | --- | --- |
| Configure this collection for a repository | [setup-skills](./skills/setup/setup-skills/SKILL.md) | A shared configuration section in AGENTS.md |
| Resume work after a break or context reset | [memory-bank](./skills/productivity/memory-bank/SKILL.md) | Updated Markdown records with a clear owner for each fact |
| Plan and close out the workday | [daily-check-in](./skills/productivity/daily-check-in/SKILL.md) | Journal entries, outcomes, and a starting point for tomorrow |
| Prepare a message for someone else | [drafting-for-others](./skills/productivity/drafting-for-others/SKILL.md) | An audience-aware draft with context and a proposed next step |
| Document an operational procedure | [runbook-authoring](./skills/engineering/runbook-authoring/SKILL.md) | Verified steps, expected results, recovery, and escalation |
| Create or improve an agent skill | [writing-skills](./skills/engineering/writing-skills/SKILL.md) | Focused instructions and metadata for supported clients |
| Check which organizational rules apply | [standards-check](./skills/engineering/standards-check/SKILL.md) | A local standards cache and an evidence-based applicability report |
| Assess an open review queue | [mr-policy-triage](./skills/engineering/mr-policy-triage/SKILL.md) | Read-only REDIRECT / SCRUTINY / ROUTINE classifications |
| Look up or change Jira data | [jira-ops](./skills/work-tracking/jira-ops/SKILL.md) | REST v3 queries, ADF comments, fields, and ownership-aware transitions |
| Refine tickets or plan a sprint | [jira-work-management](./skills/work-tracking/jira-work-management/SKILL.md) | Ticket drafts and proposed planning changes for review |
| Maintain Confluence content | [confluence-ops](./skills/work-tracking/confluence-ops/SKILL.md) | Search results, readable pages, and version-aware page edits |

## Use a local checkout

The files follow the [Agent Skills format](https://agentskills.io). A client that can load a
skill directory can use a complete folder from `skills/<category>/<name>/`. License and
attribution files are maintained at the repository root. If distributing selected skills
separately, include the root LICENSE and applicable third-party notices with that distribution.

For clients that discover skills in `~/.claude/skills` or `~/.agents/skills`, the included
helper creates links to a checkout:

```bash
git clone https://github.com/sudo-sol/skills.git
cd skills
scripts/link-skills.sh
```

The helper needs Bash and Python 3. To choose another discovery directory, pass its path:

```bash
scripts/link-skills.sh "$HOME/my agent/skills"
```

The helper skips occupied names, including broken links. Inspect an existing entry before
removing it to replace an installation. Linked skills follow changes in the checkout;
rerun the helper to add newly created skill folders. Copied folders need to be updated
manually. Uninstall by removing the specific links or copies you installed.

## Use a client installer

Plugin catalogs are included for clients that support them. Use one installation route
per client to prevent duplicate entries. These are version-dependent interfaces; consult
the installed client's `--help` when a command is unavailable. Runtime compatibility has
not yet been tested across these clients.

| Client | Register this repository | Install the collection |
| --- | --- | --- |
| Claude Code | `claude plugin marketplace add sudo-sol/skills` | `claude plugin install skills@skills` |
| Codex | `codex plugin marketplace add sudo-sol/skills` | `codex plugin add skills@skills` |
| Copilot CLI | `copilot plugin marketplace add sudo-sol/skills` | `copilot plugin install skills@skills` |

For Copilot in VS Code, supply the repository URL `https://github.com/sudo-sol/skills` to
the command palette action **Chat: Install Plugin From Source**.

Gemini CLI accepts a category path; run this for the four shipped categories:

```bash
for category in setup productivity engineering work-tracking; do
  gemini skills install https://github.com/sudo-sol/skills.git --path "skills/$category"
done
```

The community installer provides another route for compatible agents:

```bash
npx skills@latest add sudo-sol/skills
```

Use the selected installer's own update and removal commands for installations it manages.
The local checkout route above is available when a client lacks plugin support.

## Configure and run

Select `setup-skills` once in each project. In Codex, use `$setup-skills`; a Claude Code
plugin installation exposes `/skills:setup-skills`. Other clients may provide a skill picker.
Setup collects repository settings in `## Skills configuration` within `AGENTS.md`.
That section holds site URLs, working paths, project choices, and writing preferences;
each skill documents its defaults for missing values.

Setup requires a user request: its metadata disables automatic invocation in Claude Code
and Codex. The remaining skills permit selection by a matching task. Clients may interpret
these settings differently, so verify invocation behavior in the client you use.

A workflow may need another installed skill. Resolve it using the client's loader and
namespace, such as `skills:jira-ops`, or open its installed `SKILL.md` directly. If that
skill is absent, report the dependency and install it before resuming the affected steps.

## Working boundaries

- Drafts and proposed changes need an explicit request before sending, posting, approving,
  or merging. Optional journal Git operations also require explicit authorization.
- Missing facts remain unresolved. Verify owners, dates, field values, and policy findings
  against project evidence or ask for the information.
- Keep organization details in the consumer project's configuration. Examples in this
  collection must be suitable for public distribution.
- Supply secrets through environment variables. Do not paste them into configuration or
  include them in agent output.

## Credentials

Atlassian skills read `JIRA_URL`, `JIRA_EMAIL` and `JIRA_TOKEN` from your environment;
Confluence also accepts `CONFLUENCE_URL`. Examples target the standard Atlassian Cloud
site URL with email/API-token basic authentication. Scoped tokens or organization-specific
gateways may require a different API base; follow your tenant’s authentication documentation.
Review triage uses an already-authenticated `gh` or `glab`. Credentials are not saved by setup.

Tools are needed only for the workflow being used: `curl` and `jq` or Python `requests` for
Atlassian APIs; `pandoc` or `markdownify` for page conversion; `mmdc` optionally for diagrams.
Install these separately when needed. Skills are instructions, not sandboxing or an access
control system; the agent still needs the relevant tools, permissions, and user authorization.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Run `scripts/check-skills.sh` before opening a PR.

## License

[MIT](./LICENSE), including the skill instructions, scripts, templates, and documentation.
You may use, modify, and redistribute the collection, including commercially, while preserving
the required notices. See [third-party notices](./THIRD_PARTY_NOTICES.md) for the reference
project’s retained attribution. Both files are kept at the repository root. When redistributing
individual skills outside the repository, include the root license and applicable notices
with that distribution. The upstream notice is retained conservatively while adaptation
history remains uncertain; it does not assert that each skill was copied from the reference project.
External clients, tools, and services retain their own licenses and terms.

## Packaging and verification

`.claude-plugin/plugin.json` registers the 11 skill folders explicitly so the category
directories are not mistaken for individual skills. `.claude-plugin/marketplace.json`
registers the repository root as the `skills` plugin in the `skills` marketplace.
The version remains `0.1.0` for the unreleased initial package. Unreleased fixes are in
`CHANGELOG.md`; bump the manifest version for subsequent releases.

From the repository root, with Bash and Python 3.10+ (including `venv`) installed:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
scripts/check-skills.sh
python3 -m unittest discover -s tests -v
for script in scripts/*.sh; do bash -n "$script" || exit; done
```

If `venv` reports that `ensurepip` is unavailable, install your distribution’s Python venv
and pip packages first (on Debian/Ubuntu these are `python3-venv` and `python3-pip`), then
recreate the environment. If your managed environment already provides PyYAML, you can run
the three check commands directly with that Python; this does not verify the clean venv setup.

Dependency installation needs network access once; the checks themselves run offline.
PyYAML is a development dependency and is not required to use the installed skills.

The checker parses YAML, rejects missing front-matter boundaries and duplicate keys, checks
picker metadata and boolean invocation flags, and validates root notices, local links,
manifest/catalog registrations, and the README skill list. Regression tests exercise invalid
packages and installation into temporary directories.
It is an offline structure check, not a live-agent compatibility or API test. No agent installation
or third-party account is needed. Client installation and behavioral checks remain required
before claiming runtime compatibility; see `CONTRIBUTING.md`.

Installation and packaging references: [Claude plugin manifests](https://code.claude.com/docs/en/plugins-reference),
[Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces),
[Codex plugin packaging](https://developers.openai.com/plugins/build/plugins), and
[Copilot CLI plugins](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference).

`setup-skills` intentionally keeps Claude's `disable-model-invocation: true` and Codex's
`policy.allow_implicit_invocation: false`. A generic front-matter validator that does not
recognize Claude's extension rejects that field; this is a validator compatibility limit,
not a reason to enable automatic setup. See [Claude invocation controls](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill).

## Repository layout

Skills are grouped by the work they support:

| Folder | Scope |
| --- | --- |
| `skills/setup/` | Collection configuration |
| `skills/productivity/` | Work continuity, journaling, and communication |
| `skills/engineering/` | Reviews, standards, runbooks, and skill authoring |
| `skills/work-tracking/` | Jira workflows and Confluence content |

Each skill folder is an installable unit containing instructions, picker metadata, any
supporting references. Shared development and distribution files live outside
these folders:

- `.claude-plugin/`: plugin and marketplace catalogs.
- `scripts/`: offline package validator, skill listing, and local symlink installer.
- `tests/`: validator and installer regression tests.
- `requirements-dev.txt`: validation dependency range.
- `CONTRIBUTING.md`: change and release checks.

There is no build step or bundled agent runtime. This initial package has offline validation;
installation and behavioral testing across the advertised clients remain unverified.
See [release review](./RELEASE_REVIEW.md) for the checks actually performed and remaining limits.
