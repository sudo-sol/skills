---
license: MIT
name: jira-work-management
description: Policy layer for heavier Jira work, such as drafting a story, task or epic from a template, backlog refinement, and sprint planning, with previews before any change. Use when the user asks to write up a ticket, create an epic, refine the backlog, or plan the next sprint. Not for quick single-issue actions; those go straight to jira-ops.
---

# Jira work management

Decides *what* to create or propose and *what to check first*. All reads and writes go through
`jira-ops` (load the `jira-ops` skill through the client’s skill mechanism). Quick one-issue actions (status, a supplied
comment, a transition, a reassignment, a search) skip this skill entirely.

## Configuration

From the `Skills configuration` section of `AGENTS.md`: `jira_default_project`, `jira_board_id`,
`jira_default_labels` (empty list), `jira_default_component`, `jira_default_fix_version`,
`jira_default_team` (unset), and `jira_estimate_tasks` (false). Treat any cached field ID as dated
and confirm it against createmeta before use.

## Defaults

- **Story** for user-facing or planned product work. **Task** for operational, technical,
  support, or enablement work. **Epic** for an outcome bigger than one sprint that groups several items.
- Stories and tasks go into sprints; epics do not unless the team explicitly does that.
- Use checklists for small actionable steps and acceptance criteria for "done".
- Keep the user's terminology and voice (see `drafting-for-others`).
- **Never invent** assignees, story points, priorities, dates, acceptance criteria, dependencies, or
  business value. **Priority and assignee are per ticket**; ask before creating if absent.
  Ask for story points on stories and on tasks only when `jira_estimate_tasks` is true;
  epics are not estimated by default. An explicit unassigned or no-estimate choice is valid
  where Jira permits it. Never copy these fields from config or a previous ticket.
- Mark unresolved required values as `Needs confirmation: <specific question>` in drafts.
  Omit empty optional sections. Resolve required fields before creating an issue.

## Write policy

- **Draft freely.** Drafts change nothing.
- **Create one issue** when the user explicitly asked and project, type, outcome and the
  applicable per-ticket fields are resolved.
- **Preview, then wait for approval** for: bulk creation, moving issues in or out of a sprint,
  starting/completing/renaming/deleting a sprint. The preview lists every key, every change, and
  unresolved fields.
- If Jira is unreachable, return a paste-ready draft and say Jira was not changed.

## Create an issue from a template

1. Identify project, type, summary and intended outcome.
2. Read createmeta for that project and type. Custom fields (story points especially) vary.
3. Search for likely duplicates using distinctive summary terms, epic, component, labels.
4. Draft with `references/issue-templates.md`. **Fit the template to the work**: a one-step task
   does not need a user story, risks, or validation sections. Cut what does not help.
5. If the source is a private working note (incident log, journal, local memory), distill a clean
   standalone ticket. Do not paste internal narrative, ruled-out theories, or anything sensitive,
   and **never cite local file paths**; link team-visible artifacts instead.
6. Check: outcome-focused summary, clear problem, testable acceptance criteria, correct parent,
   no invented field values.
7. Create via `jira-ops`, then report key, summary, type, parent, status, assignee, points and link
   as returned by Jira.

## Sprint planning

1. Find the board and the active/next sprint.
2. Gather: unfinished work in the active sprint, prioritized ready backlog, blockers and dependencies,
   estimates, assignees, parent epics, and any capacity info that actually exists.
3. Separate carryover from new work. Flag items missing refinement, required fields, or with
   unresolved dependencies.
4. Propose: sprint goal, carryover with reasons, new candidates in priority order, total points only
   when estimates are real, ownership gaps, risks, and decisions the team must make.
5. Use historical velocity only when there are several completed sprints of reliable data, and say which.
6. Present the proposal. Change sprint membership only after approval, then verify each change.

## Backlog refinement

Flag duplicate, blocked, unestimated, unowned, stale, or under-specified items and suggest fixes.
Change nothing without approval.

## Output

```
Summary            what was found or changed
Changes            issue keys, exact field changes, links
Risks and gaps     missing data, blockers, assumptions
Next decision      the one decision needed, or "done"
```
