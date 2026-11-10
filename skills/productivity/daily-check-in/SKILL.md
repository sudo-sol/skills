---
license: MIT
name: daily-check-in
description: Keep a daily work journal through short morning, afternoon, and end-of-day check-ins that record mood, energy, goals, and outcomes, then prepare the next workday's note. Use when the user says "start my day", "morning check-in", "afternoon check-in", "EOD", "wrap up", "check out", or asks for help with their work journal.
---

# Daily check-in

A lightweight work journal the agent maintains with the user. Three touchpoints, one file per
day. The agent asks, records, and prepares tomorrow. It never nags and never schedules itself.

## Configuration

Read the `Skills configuration` section of `AGENTS.md`:

- `journal_dir` (default `journal/daily/`), one file per day: `YYYY-MM-DD.md`
- `journal_template` (default `references/journal-template.md` in this skill)
- `achievements_file` (optional; weekly highlights)
- `journal_sync` (`none` by default; `git` enables the scoped sync below)

An overridden `journal_template` path is relative to the consumer repo; otherwise use the
reference bundled with this skill.

Use the user's configured timezone for dates and check-out times. Prefer the client-provided
clock; otherwise use `date` with that timezone. If the timezone is unknown and the date could
change the journal filename, ask before creating the note.

## Principles

- **Check-out is the main session.** Record the day while it is fresh, then prepare the next one.
- **Ask in groups.** Each phase asks for all of its missing fields in one compact prompt. Accept
  partial answers. Do not re-ask what was answered.
- **Never invent.** No guessed times, ratings, reasons, owners, dates or outcomes. Unknown stays
  blank or `Not provided`. Do not backfill a missed morning or afternoon rating later.
- **Facts, not spin.** Distinguish completed work from plans. Use the user's words for outcomes.
- **The `Notes` section belongs to the user.** Read it only for context. Never write, rewrite,
  clear or carry it forward.
- **Preserve.** Re-read the file before every save and keep existing entries and manual edits.
- **A journal is not a task tracker.** If an answer confirms a real task state change and the
  repo uses `memory-bank`, load the `memory-bank` skill through the client’s skill mechanism to update the owner file.

## Morning

1. Read today's note. It was usually prepared at the last check-out.
2. If it exists, keep its Goals. Do not start planning from backlogs unless asked.
3. Ask, in one prompt, for whatever is missing: actual start time, work location, and
   before-work energy and mood (1-10, with a brief reason each).
4. If no note exists and the user asked for journal help, create it from the template.
   Never create notes for days the user did not work.

## Afternoon

1. Read today's note (create from template only if the user asked).
2. Ask for afternoon energy and mood (1-10 with brief reasons) in one prompt. Update only those.

## Check-out

1. Read today's note and the template. Confirm the date if ambiguous.
2. Work out what is already filled. Ask for everything else in **one** structured prompt
   (a short checklist or table is fine):
   - Goals: which are done, which are still open; any unplanned work
   - Waiting on: still open? anything new?
   - Missing start time or location (only actual values; never estimate)
   - Productivity, end-of-day energy, end-of-day mood (1-10 with brief reasons)
   - Learnings, and what could improve
   - On the last workday of the week, if `achievements_file` is set: which of this week's
     evidenced outcomes to add (including "none")
3. Save partial answers; follow up only on genuine gaps or ambiguities.
4. Record the actual check-out time right after the last answer, before bookkeeping.
5. Save, re-read, and verify date, answers, ratings at the right timepoints, and untouched Notes.

## Prepare the next workday

1. Ask which day the user next expects to work if it is not clear. Do not assume weekends or leave.
2. If that day's note exists, never replace it. Otherwise create it from the template with only
   the date filled.
3. Offer today's unfinished Goals and open Waiting On items as a numbered list. Carry forward
   only what the user picks. Never carry ratings, reflections, completed goals, or Notes.
4. Re-read and verify.

## Sync

If `journal_sync: git`, read `references/scoped-sync.md` before any Git command beyond a
read-only status. Configuration enables the workflow, not permission to run Git mutations.
Ask for an explicit request to pull, commit, or push unless that exact action is already
authorized in this session. A morning or check-out request alone authorizes journaling.
Skipping or failing sync must never lose the journal answers.
