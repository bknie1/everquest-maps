#!/usr/bin/env bash
# safety_commit.sh -- Stop-hook backstop so worktree work is NEVER left behind.
#
# Fires when the agent finishes a turn. If the working tree has uncommitted
# changes it commits them as a clearly-labelled WIP commit. It NEVER pushes
# (pushes stay a human-confirmed step) and NEVER commits on the default branch
# (main/master) -- there it only warns, to respect the branch-first workflow.
#
# To keep history tidy during a task, consecutive safety commits ROLL into one:
# if HEAD is an un-pushed "WIP: auto-commit safety net" commit, this amends it
# instead of stacking a new one. When you finalise real work, reword that WIP
# HEAD with `git commit --amend -m "..."` rather than a fresh commit.
set -u

input="$(cat 2>/dev/null || true)"
# Loop guard: never re-trigger ourselves.
case "$input" in *'"stop_hook_active":true'*) exit 0 ;; esac

# Must be inside a git work tree.
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo HEAD)"
dirty="$(git status --porcelain 2>/dev/null)"

emit() { printf '{"systemMessage":%s}\n' "$1"; }   # $1 must be a JSON string literal

# Default branch: do not auto-commit; just warn if dirty.
if [ "$branch" = "main" ] || [ "$branch" = "master" ] || [ "$branch" = "HEAD" ]; then
  [ -n "$dirty" ] && emit "\"[safety-commit] Uncommitted changes on $branch -- not auto-committing on the default branch. Commit manually or branch first.\""
  exit 0
fi

# Clean tree: remind about un-pushed commits, then done.
if [ -z "$dirty" ]; then
  ahead="$(git rev-list --count @{upstream}..HEAD 2>/dev/null || echo 0)"
  if [ "${ahead:-0}" -gt 0 ] 2>/dev/null; then
    emit "\"[safety-commit] $ahead commit(s) on $branch not yet pushed -- push when ready (pushes are never automatic).\""
  fi
  exit 0
fi

ts="$(date '+%Y-%m-%d %H:%M:%S')"
git add -A >/dev/null 2>&1

body="Uncommitted worktree changes captured automatically by the Stop hook so nothing is lost. Reword/squash when finalizing; NOT pushed."
trailer="Co-Authored-By: Claude Code safety-commit <noreply@anthropic.com>"

head_msg="$(git log -1 --pretty=%s 2>/dev/null || echo '')"
on_remote="$(git branch -r --contains HEAD 2>/dev/null || echo '')"

case "$head_msg" in
  "WIP: auto-commit safety net"*)
    if [ -z "$on_remote" ]; then
      git commit --amend -m "WIP: auto-commit safety net ($ts)" -m "$body" -m "$trailer" >/dev/null 2>&1
      emit "\"[safety-commit] Rolled changes into the WIP safety commit on $branch (not pushed). Finalize with 'git commit --amend -m ...' and push when ready.\""
      exit 0
    fi
    ;;
esac

git commit -m "WIP: auto-commit safety net ($ts)" -m "$body" -m "$trailer" >/dev/null 2>&1
emit "\"[safety-commit] Captured a WIP safety commit on $branch (not pushed). Reword/squash and push when ready.\""
exit 0
