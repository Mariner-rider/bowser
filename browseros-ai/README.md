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
```


## End-to-End Local Runtime (No External Repo Required)

This project includes a **clean-room local BrowserOS-compatible runtime** under `core/chromium_bridge/browseros_runtime.py`.
It allows developers to run the full pipeline locally (command parsing -> agent kernel -> automation -> runtime) without cloning any external browser repository.

```bash
python scripts/run-e2e.py
```

> Legal note: this repository does **not** copy third-party proprietary source code. Runtime components are implemented in-project to avoid external copyright/licensing conflicts.
