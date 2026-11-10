# Working on this repo

Instructions for agents (and humans) editing the skills in this repository.

## Layout

- `skills/<bucket>/<skill-name>/SKILL.md`: one skill per folder; buckets are `setup`,
  `productivity`, `engineering`, `work-tracking`.
- `skills/.../agents/openai.yaml`: Codex picker metadata, required for every skill.
- `skills/.../references/`: detail a skill loads only when a step tells it to.
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`: plugin manifests used by Claude Code,
  Codex and Copilot marketplaces. Every skill must be listed in `plugin.json`.
- `scripts/check-skills.sh`: offline format checks. `scripts/link-skills.sh`: local symlink install.

## Conventions

- Front matter `name` equals the folder name, lowercase-hyphenated.
- **Model-invoked** (default): description is model-facing and ends with concrete "Use when..."
  triggers. **User-invoked**: `disable-model-invocation: true` in `SKILL.md` *and*
  `policy.allow_implicit_invocation: false` in `agents/openai.yaml`; description is a one-line
  human summary. Keep the two in sync.
- Load dependencies through the client’s skill mechanism, using the installed name or namespace.
  If unavailable, read the installed SKILL.md directly; if missing, report the missing dependency.
  Do not assume every client exposes a tool named Skill. Do not link across skill folders.
  A user-invoked skill must be requested by the user.
- Site-specific values (paths, URLs, projects, voice) are read from the
  `## Skills configuration` section of the consumer repo's `AGENTS.md`, with a stated default.
  `setup-skills` documents every key; add new keys there.
- No private personal names, company details, internal hostnames/URLs, real ticket IDs, or metrics
  in examples. Preserve legally required public author names in license and attribution notices.
- Skills may narrow what an agent does but never grant permission. External writes, sending,
  approving and merging require an explicit user request. Never embed or print secrets.

## Before finishing a change

1. Set up the development environment documented in README. `scripts/check-skills.sh` and
   `python3 -m unittest discover -s tests -v` pass.
2. README skill list and `plugin.json` match the skills on disk.
3. Keep LICENSE and THIRD_PARTY_NOTICES.md at the repository root; do not duplicate them in skill folders.
4. Add a line to `CHANGELOG.md` and bump `version` in `.claude-plugin/plugin.json` for releases.
