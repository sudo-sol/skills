# Persistence and recovery

Read before any memory write. Not needed for a read-only task.

## Writing changed state

1. Re-read the target file immediately before writing. Preserve concurrent and manual edits.
2. Update only the affected sections. Use stable headings:
   `Current state`, `Next action`, `Blockers and decisions`, `Evidence`, `History`.
3. Record: concise outcome, decision and rationale, evidence (links, commands, IDs), next
   action, blockers, pending approvals, and the working version (branch/commit, and whether
   it is local, uncommitted, pushed, or applied).
4. Optional front matter: `id`, `type`, `status`, `updated_at`, `verified_at`, `aliases`, `source`.
   Only an actual verification changes `verified_at`. Editing text changes `updated_at`.
5. Explicit user corrections beat your inference.

Update `work-index.md` only when routing changes (new owner, rename, move). Keep
`activeContext.md` short: objective, result, next action, blocker, owner pointers. Do not
overwrite an unrelated workstream's handoff with the current task.

## Size and rotation

Aim to keep the always-read set (`activeContext.md` + `work-index.md` + this skill) around
10-15 KB. Bytes are a proxy, not tokens or cost. Never drop a live constraint or pending
decision to hit a number.

Move durable facts to `knowledge/`, open detail to its task owner, and resolved narrative to
`archive/YYYY-MM-<slug>.md`, leaving a one-line link. Do not prune by age, auto-close
waiting work, or expire decisions. After moving, verify IDs, constraints and links survived.
A task is complete only with outcome evidence.

## Privacy

Keep anything personal about the user out of tracked files. If the user wants private notes,
put them under a path listed in `.gitignore` and confirm it is not already tracked
(`git ls-files <path>`). Ignoring a path does not erase published history.

## Verification

Read the result back before claiming it saved; check content, not just existence. If a
canonical file is missing or contradictory, fall back to its dated sources. If essential facts
remain missing, label the gap and ask.

Saving memory never implies committing or pushing. Git publication needs its own explicit
request.
