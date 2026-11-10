# Contributing

Thanks for helping. Small, focused changes are easiest to review.

## Adding or changing a skill

1. Read [AGENTS.md](./AGENTS.md) for layout and conventions. The `writing-skills` skill walks
   through the process if you want your agent to help.
2. Keep skills portable: no company names, internal URLs, people, or hard-coded paths. Read
   site-specific values from the `Skills configuration` section and document new keys in
   `skills/setup/setup-skills/SKILL.md`.
3. Keep skills safe: drafting is not publishing. Approving, merging, and posting need an
   explicit request; never print secrets, even as an example or on request.
4. Follow the development setup in [README.md](./README.md), then run `scripts/check-skills.sh`
   and `python3 -m unittest discover -s tests -v`.
5. Try the skill in at least one real agent with two prompts that should trigger it and one that
   should not. Say which agent you used in the PR.

## Bugs and ideas

Open an issue with the agent you used, the prompt, what happened, and what you expected.

## Licensing contributions

Submit only work you have the right to share under this repository’s MIT license. Contributions
are distributed under [LICENSE](./LICENSE). Identify copied or adapted material, link its source
and revision, and retain its required notices in [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md).
Do not remove an upstream copyright notice or replace it with the project’s name.

Keep LICENSE and THIRD_PARTY_NOTICES.md at the repository root; the checker requires both.
Distributions containing selected skills must retain the license and applicable notices. Dependencies
installed for development are not bundled into the skills and retain their own licenses.

## Before a release

- Run the documented validation commands and review every file intended for publication.
- Check that names, examples, URLs, and templates contain no employer or private project material.
- Confirm root license and third-party attribution are complete.
- Test installation and invocation in each client for which runtime compatibility is claimed.
  For explicit-only skills, check that a near-miss does not invoke setup automatically.
- Record actual client versions and outcomes; leave untested clients explicitly unverified.
- The first package is `0.1.0`, still unreleased. When publishing it, date its changelog entry;
  later releases must update both the changelog and manifest version.
- Review `git status` and the staged diff. New files must be staged and committed before a push
  includes them. Release tags, GitHub publication, and pushes are separate explicit actions.
