#!/usr/bin/env bash
set -euo pipefail

# One-command helper for the recurring BrowserOS AI PR conflict set.
# Usage:
#   bash browseros-ai/scripts/fix-pr-conflicts.sh
# Optional:
#   TARGET_BRANCH=main bash browseros-ai/scripts/fix-pr-conflicts.sh

TARGET_BRANCH="${TARGET_BRANCH:-main}"

echo "[fix-pr-conflicts] target branch: ${TARGET_BRANCH}"

echo "[fix-pr-conflicts] fetching latest refs"
git fetch --all --prune

# Merge target branch into current branch; continue if conflicts appear.
echo "[fix-pr-conflicts] merging ${TARGET_BRANCH} into $(git rev-parse --abbrev-ref HEAD)"
set +e
git merge "origin/${TARGET_BRANCH}" 2>/dev/null
merge_code=$?
set -e

if [[ $merge_code -ne 0 ]]; then
  echo "[fix-pr-conflicts] merge produced conflicts (expected for recurring files)"
fi

# Resolve known conflict set by preferring current branch implementation.
bash browseros-ai/scripts/resolve-pr-conflicts.sh

# Ensure no unresolved files remain.
if git diff --name-only --diff-filter=U | grep -q .; then
  echo "[fix-pr-conflicts] unresolved conflicts remain; please resolve manually:"
  git diff --name-only --diff-filter=U
  exit 1
fi

# Run tests.
echo "[fix-pr-conflicts] running tests"
npm --prefix browseros-ai test

# Commit merge resolution if there are staged/unstaged changes.
if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit -m "Resolve merge conflicts against ${TARGET_BRANCH}"
  echo "[fix-pr-conflicts] committed conflict resolution"
else
  echo "[fix-pr-conflicts] nothing to commit"
fi

echo "[fix-pr-conflicts] done. Next: git push"
