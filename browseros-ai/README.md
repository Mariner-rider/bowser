# AI Browser OS (BrowserOS AI Extension)

This repository provides an AI extension architecture that keeps BrowserOS runtime boundaries intact while adding agent orchestration, LLM routing, memory, automation, learning, local AI, dashboarding, and mobile delivery.

## Repository Structure

```text
browseros-ai/
├ core/
│  ├ chromium_bridge/
│  ├ networking/
│  └ security/
├ agents/
│  ├ agent_kernel.py
│  ├ agent_registry.py
│  ├ agent_base.py
│  └ agents/
├ llm/
├ memory/
├ automation/
├ learning/
├ local_ai/
├ interface/
├ dashboard/
├ web3/
├ mobile/
│  ├ capacitor.config.ts
│  ├ ios/
│  ├ android/
│  └ pwa/
├ ui/
├ sdk/
├ tests/
├ docs/
├ scripts/
├ docker/
├ package.json
└ LICENSE
```

## Key Principles

- **Non-invasive integration:** AI modules connect via `core/chromium_bridge` adapter boundaries.
- **Security-first execution:** capability checks, permission gates, and isolated wallet flows.
- **Composable architecture:** each subsystem can evolve independently.
- **Cloud/local hybrid:** `llm/` + `local_ai/` support policy-aware routing.

## Roadmap

See `docs/roadmap.md` for the prototype-to-production 10-phase plan.

## Build Commands

```bash
npm run build-pwa
npm run build-mobile
npm run build-extension
npm run build-desktop
```


## End-to-End Local Runtime (No External Repo Required)

This project includes a **clean-room local BrowserOS-compatible runtime** under `core/chromium_bridge/browseros_runtime.py`.
It allows developers to run the full pipeline locally (command parsing -> agent kernel -> automation -> runtime) without cloning any external browser repository.

```bash
python scripts/run-e2e.py
```

> Legal note: this repository does **not** copy third-party proprietary source code. Runtime components are implemented in-project to avoid external copyright/licensing conflicts.


## Automatic Theme by Time

Dashboard UI now supports automatic day/night theming based on local system time, with manual toggle override in the header.


## Browser Extension + Desktop App

- `extension/`: cross-browser companion extension scaffold (popup/background/content script).
- `desktop/`: Electron desktop shell scaffold for macOS/Windows/Linux distribution.


## If GitHub Says “This branch has conflicts that must be resolved”

Run this single command from your branch:

```bash
bash browseros-ai/scripts/fix-pr-conflicts.sh
```

Then push:

```bash
git push
```
