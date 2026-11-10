# Scoped journal sync (Git)

Only used when `journal_sync: git` and the user explicitly authorizes the relevant Git actions.
A morning, check-out, greeting, or memory-save request alone does not authorize pulling,
committing, or pushing. Existing explicit session authorization may be reused within its scope.
Save journal answers locally before asking for missing Git authorization.

Run the steps below only for the authorized direction and actions. A commit request does not
authorize pushing; a push request does not authorize publishing unrelated commits.

## Before either direction

- Confirm the working directory, branch, upstream, and worktree/index status (filenames only).
- Stop on unresolved merges, unexpected staged changes, conflicts, or unclear ownership.
- Never reset, stash, switch branches, rebase, amend, force-push, or auto-resolve conflicts.

## Morning

Only if the tree and index are clean, there are no unrelated unpushed commits, and the upstream
is the expected one: `git pull --ff-only`. If it fails or diverges, stop syncing and carry on
journaling.

## Check-out

1. Build an explicit list of files this check-out changed (today's note, tomorrow's note, the
   achievements file, any memory owner updated). It is a file list, not a directory.
2. Drop anything ignored (`git check-ignore`) or private. Never use `git add -A`, `git add .`,
   directory pathspecs, or `git add -f`.
3. Review the diffs of those files for sensitive content or unexpected deletions. If unrelated
   edits are mixed in, show a short summary and ask what may be published.
4. Stage exact paths: `git add -- <file> ...`. The staged set must equal the approved list. If
   something else is already staged, stop; do not unstage someone else's work.
5. Commit with `Journal sync YYYY-MM-DD`. Nothing staged means no commit.
6. Before pushing, confirm every unpushed commit is part of this sync and the upstream still
   matches. Push normally, never force.
7. Report the end state: local only, committed but not pushed, or published. On a failed push,
   keep the commit and do not retry destructively.
