#!/usr/bin/env bash
set -euo pipefail

# Resolve the known recurring PR conflict set by favoring this branch's versions,
# then re-run validation checks.

CONFLICT_FILES=(
  "browseros-ai/README.md"
  "browseros-ai/dashboard/frontend/agent_panel.tsx"
  "browseros-ai/dashboard/frontend/dashboard_ui.tsx"
  "browseros-ai/dashboard/frontend/marketplace_panel.tsx"
  "browseros-ai/docs/project-handbook.md"
  "browseros-ai/package.json"
  "browseros-ai/tests/test_structure.py"
)

echo "[resolve-pr-conflicts] checking for merge state"
if ! git rev-parse --verify MERGE_HEAD >/dev/null 2>&1; then
  echo "No merge in progress."
  echo "Usage: run this after 'git merge main' if conflicts appear."
  exit 0
fi

for f in "${CONFLICT_FILES[@]}"; do
  if git ls-files -u -- "$f" | grep -q .; then
    echo "[resolve-pr-conflicts] taking ours: $f"
    git checkout --ours -- "$f"
    git add "$f"
  fi
done

echo "[resolve-pr-conflicts] unresolved entries remaining:"
git diff --name-only --diff-filter=U || true

echo "[resolve-pr-conflicts] done. If no unresolved files remain, run:"
echo "  npm --prefix browseros-ai test"
echo "  git commit -m 'Resolve merge conflicts against main'"
