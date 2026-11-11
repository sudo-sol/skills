# Initial package review

Reviewed 2026-11-09 for the planned 0.1.0 release. The package is not tagged or published.

## Licensing and provenance

The project uses MIT with the generic copyright holder “skills contributors”. Each installable
skill declares MIT in its metadata; LICENSE and THIRD_PARTY_NOTICES.md are kept at the root.
The reference project, mattpocock/skills, is also MIT; its original copyright and permission text
are retained in the third-party notices. See that file for the source revision.

The initial comparison against that revision and 1,446 historical Markdown, shell, and YAML
text objects identified shared installation prose in README and no contiguous 12-word matches
in the skill bodies. The README was subsequently rewritten around this collection’s tasks,
with a local-checkout guide and a compact client command table replacing the reference-style
installation sections. Client command syntax and compatible packaging fields are retained.
The follow-up scan of this package’s Markdown, shell, and YAML files found no contiguous
12-word matches against those 1,446 historical text objects. This word-token comparison
does not detect paraphrases or establish authorship. The upstream extensionless LICENSE
is outside that scan; its MIT notice remains deliberately preserved in this package.
This is a bounded comparison against the identified source, not proof of independent authorship
or an audit of every possible source. Future contributions must identify additional sources.

## Category and provenance follow-up

The maintainer states that they drafted and used these skills in their own work and consulted
mattpocock/skills when structuring the repository for public release. README now presents that
background; the acknowledgement preserves the uncertainty about historical adaptation.

Reviewed the purpose, entrypoint, and supporting files of all 11 skills. The existing categories
fit their primary uses: setup (configuration), productivity (continuity, journal, communication),
engineering (review, standards, runbooks, skill authoring), and work-tracking (Jira and Confluence).
No folder moves or skill splits were needed. Skill authoring fits engineering; Confluence stays
with the Jira integrations because it provides service operations rather than general writing.

At the maintainer’s request, notices are now consolidated at the repository root. All 22
per-skill copies were removed, and the checker requires the two root files instead. The
redistribution instructions explain that selected-skill distributions must retain the license
and applicable notices. The root upstream notice remains a conservative retention choice
given uncertain adaptation history, not a finding of upstream content in every skill.

## Verification

Executed with Python 3.12 and PyYAML 6.0.1:

- `scripts/check-skills.sh`: passed for all 11 skills, including manifests, links and root notices.
- `python3 -m unittest discover -s tests -v`: all 11 regression tests passed. Invalid YAML,
  missing delimiters/root notices, invocation mismatches, duplicate keys and unregistered skills
  are rejected. Temporary installation tests preserve existing entries and handle spaces.
- `for script in scripts/*.sh; do bash -n "$script" || exit; done`: all shell scripts passed.
- A credential/private-path pattern scan found no matches. This is not a comprehensive secret audit.

## Remaining limits

- Clean `venv` setup could not run on the review machine because its Python installation lacks
  ensurepip/venv support. The documented preinstalled-PyYAML route passed; the README explains
  the missing prerequisites. No system packages were changed.
- No live agent installation, trigger-behavior evaluation, or authenticated Atlassian API test
  was performed. Compatibility is a target, not a runtime certification.
- The generic skill validator accepts 10 skills but rejects setup-skills’ Claude-specific
  `disable-model-invocation` field. The repository validator explicitly supports that extension
  and verifies its agreement with Codex metadata.
- The shared `.github/scripts/check_completion.py` gate is not installed in this standalone
  repository, so that completion check could not run. No existing open GitHub issue was found
  to update. Repository checks above are the recorded verification, not a CI or release result.

## Zen import, 2026-11-10

Imported the skill entrypoint from the maintainer-supplied archive into `skills/productivity/zen/`
and registered it in the plugin and README. Package validation covered all 12 skills, all 11
regression tests passed, and the skill-creator validator accepted the Zen entrypoint.
Live client invocation remains unverified. No open issue with Zen in its title was found.
The shared completion check remains unavailable in this repository.
