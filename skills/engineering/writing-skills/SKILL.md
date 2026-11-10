---
license: MIT
name: writing-skills
description: Create, revise, or review agent skills (SKILL.md folders) so they trigger reliably and work across agents like Claude Code, Codex, Copilot, Cursor and Gemini. Use when the user wants to turn a repeatable workflow into a skill, improve a skill's description or steps, or check a skill for clarity, overlap, and side effects.
---

# Writing skills

A skill is a folder with a `SKILL.md` that teaches an agent one repeatable job. Good skills are
small, specific, and safe to run on autopilot.

## Format (Agent Skills standard)

```
<skill-name>/
├── SKILL.md            # required: YAML front matter + instructions
├── references/         # optional: detail loaded only when a step says so
├── scripts/            # optional: executable helpers
└── agents/openai.yaml  # optional: Codex picker metadata and invocation policy
```

Front matter:

```yaml
---
name: skill-name          # lowercase-hyphenated, must equal the folder name
license: MIT              # this collection; preserve required notices
description: What it does. Use when <concrete triggers and phrases>.
disable-model-invocation: true   # only for user-invoked skills
---
```

`agents/openai.yaml`:

```yaml
interface:
  display_name: "Skill Name"
  short_description: "One short line"
policy:                       # only for user-invoked skills
  allow_implicit_invocation: false
```

Keep the two invocation settings in sync for Claude Code and Codex. Other clients may ignore
these fields; verify their controls before claiming explicit-only invocation.

## Workflow

1. **Set the boundary.** What job, acting on what, producing what, and what it must never do.
   Search existing skills first; extend one when that is clearer than adding an overlapping one.
2. **Pick the invocation.** Model-invoked (default) if the agent could usefully reach for it on
   its own; its description is model-facing and lists triggers. User-invoked if it should only
   run when typed (setup, destructive, or orchestration flows); its description is a one-line
   human summary.
3. **Resolve choices that change behavior.** Trigger, inputs, outputs, interaction points, tools,
   side effects. Ask only when the answer materially changes behavior, authority, privacy or scope.
4. **Write for use.** Ordered steps, explicit boundaries, a clear output format. Prefer direct,
   testable instructions over exhortation. Move bulky, conditional material to `references/`
   and say exactly when to read it.
5. **Make it portable.** No user names, company names, internal URLs, hostnames, ticket IDs, or
   hard-coded paths. Read site-specific values from the repo's `AGENTS.md` configuration section
   and give a sensible default. Load another skill through the client’s skill mechanism
   rather than linking into its folder. Use the installed namespace; if no skill-loading tool
   exists, read its installed SKILL.md. Report missing dependencies instead of inventing a tool.
6. **Keep it safe.** A skill can narrow what an agent does; it can never grant new permissions.
   Writes to external systems, sending messages, approvals and merges need an explicit user
   request. Never embed or print secrets.
   Maintain licensing and attribution in the repository-root LICENSE and THIRD_PARTY_NOTICES.md.
7. **Validate.** Run the repo's checks (here: `scripts/check-skills.sh`). Then try a few realistic
   prompts: two that should trigger it, one near-miss that should not. An offline check proves
   format, not runtime discovery or model behavior; say which you did.
8. **Report.** Files changed, checks run, and whether the skill is drafted, linted, or tested in a
   real agent. Do not commit or publish unless asked.

## Review prompts

- Positive: "Make a skill that <specific reusable workflow>."
- Revision: "Update <skill> so it also covers <concrete gap>."
- Negative: "Can you <similar but out-of-scope task>?" The skill should not trigger or claim authority.
