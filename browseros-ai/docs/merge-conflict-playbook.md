# Merge Conflict Playbook

If your PR shows **"This branch has conflicts that must be resolved"** for the known UI/doc/package files:

## 1) Update and merge target branch

```bash
git fetch origin
git merge origin/main
```

## 2) Auto-resolve the known conflict set

```bash
bash browseros-ai/scripts/resolve-pr-conflicts.sh
```

The script handles these recurring files by taking current branch changes:
- `README.md`
- `dashboard/frontend/agent_panel.tsx`
- `dashboard/frontend/dashboard_ui.tsx`
- `dashboard/frontend/marketplace_panel.tsx`
- `docs/project-handbook.md`
- `package.json`
- `tests/test_structure.py`

## 3) Validate and finish merge

```bash
npm --prefix browseros-ai test
git commit -m "Resolve merge conflicts against main"
```

## 4) Push and re-check PR

```bash
git push
```

---

Also note: `tests/test_no_merge_conflicts.py` blocks unresolved merge markers (`<<<<<<<`, `=======`, `>>>>>>>`) from passing CI.
