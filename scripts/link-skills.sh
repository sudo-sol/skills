#!/usr/bin/env bash
# Link skills into local agent directories. Existing installations are never replaced.
# Arguments are destination directories; quote paths containing spaces.
# Legacy SKILL_DESTS is a whitespace-separated list (paths with spaces require arguments).
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
if (( $# )); then
  DESTS=("$@")
elif [[ -n "${SKILL_DESTS:-}" ]]; then
  read -r -a DESTS <<< "$SKILL_DESTS"
else
  DESTS=("$HOME/.claude/skills" "$HOME/.agents/skills")
fi
for DEST in "${DESTS[@]}"; do
  [[ -n "$DEST" ]] || { echo 'error: empty destination' >&2; exit 1; }
  resolved="$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$DEST")"
  case "$resolved" in
    "$REPO"|"$REPO"/*) echo "error: destination is inside this repo: $DEST" >&2; exit 1 ;;
  esac
  mkdir -p "$DEST"
  while IFS= read -r -d '' skill_md; do
    src="$(dirname "$skill_md")"
    target="$DEST/$(basename "$src")"
    if [[ -e "$target" || -L "$target" ]]; then
      echo "skip $target (already exists; inspect and remove it manually to replace)" >&2
      continue
    fi
    ln -s "$src" "$target"
    echo "linked $(basename "$src") -> $DEST"
  done < <(find "$REPO/skills" -name SKILL.md -print0)
done
