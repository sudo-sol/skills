# Issue templates

Sections marked *(optional)* appear only when they add real information for whoever picks up
the ticket. Omit empty optional sections. Mark required gaps as
`Needs confirmation: <specific question>` in drafts; resolve them before creation.

Fields vs description: **priority, assignee and applicable story points are never defaulted**;
ask if missing. Tasks need points only when `jira_estimate_tasks` is true; epics do not by
default. Explicit unassigned or no-estimate choices are valid where Jira permits them.
Labels, component, fix version and team may use the `jira_default_*` keys; confirm if unsure.

Never put local-only file paths in a ticket. Link team-visible artifacts instead.

## Story

**Summary:** `<outcome for a user or stakeholder>`

**Fields:** Priority `<ask>` · Story points `<ask>` · Assignee `<ask>` · Labels `<default or ask>` ·
Component `<default or ask>` · Fix version `<default or ask>`

### Description
Why this matters and what problem it solves.

### User story *(optional)*
As a `<persona>`, I want `<capability>`, so that `<outcome>`.

### Scope *(optional)*
- In: `<included>`
- Out: `<excluded>`

### Acceptance criteria
- `<observable completion condition>`

### Checklist *(optional; useful above half a point)*
- [ ] `<small actionable step>`

### Dependencies and risks *(optional)*
- `<known item>`

### Validation *(optional)*
- `<test, monitoring, docs, or rollout evidence>`

## Task

**Summary:** `<verb + concrete deliverable>`

**Fields:** Priority `<ask>` · Story points `<ask, if the team estimates tasks>` · Assignee `<ask>` ·
Labels · Component · Fix version

### Description
Why this matters and what problem it solves.

### Scope *(optional)*
- `<work item>`

### Acceptance criteria
- `<observable completion condition>`

### Checklist *(optional)*
- [ ] `<step>`

### Evidence *(optional)*
- `<PR, runbook, dashboard, test result, doc link>`

## Epic

**Summary:** `<outcome or capability>`

**Fields:** Priority `<ask>` · Assignee `<ask; often a lead or unassigned>` · Labels · Component

### Problem and opportunity
`<current state and why it is worth investing in>`

### Intended outcome
`<measurable or observable future state>`

### Goals
- `<goal>`

### Non-goals *(optional)*
- `<explicit exclusion>`

### Major deliverables
- `<story or workstream candidate>`

### Dependencies, assumptions and risks *(optional)*
- `<item>`

### Milestones *(optional)*
- `<milestone; dates only when supplied>`

### Definition of done
- Child work required for the outcome is complete.
- Operational docs and support readiness are done where applicable.
- Evidence of success is recorded.
