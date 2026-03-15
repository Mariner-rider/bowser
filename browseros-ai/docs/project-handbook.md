# Project Handbook (End-to-End)

This handbook is the single operational reference for contributors working on BrowserOS AI.

## 1. Purpose

BrowserOS AI is a modular AI-browser platform with strict runtime boundaries:
- User interfaces (text/voice/dashboard/UI)
- Intelligence systems (agents, LLM routing, memory, learning)
- Execution systems (automation engine and workflow runner)
- Infrastructure (browser bridge, security, networking, local AI, mobile runtime)

## 2. Design Principles (Do's)

1. Keep module boundaries explicit via documented APIs and protocol contracts.
2. Route all model calls through `llm/llm_router.py`.
3. Route browser actions through automation + bridge adapters.
4. Emit telemetry for critical actions and errors.
5. Prefer deterministic local behavior in tests.
6. Keep user data handling privacy-first and minimal.

## 3. Anti-Patterns (Don'ts)

1. Do not call provider SDKs directly from agents.
2. Do not bypass `ActionValidator` when performing browser actions.
3. Do not store plaintext secrets in code or logs.
4. Do not add external runtime dependencies for core tests.
5. Do not copy third-party proprietary code into this repository.

## 4. Architecture Map

- Canonical architecture: `docs/architecture.md`
- Module interfaces: `docs/module-interfaces.md`
- Python protocol boundaries: `core/module_api_protocols.py`

## 5. Module-by-Module Responsibilities

### Core
- `core/chromium_bridge/*`: runtime bridge and clean-room local runtime.
- `core/networking/*`: request allow/deny policy checks.
- `core/security/*`: permission boundaries.

### Agents
- Kernel + registry + planners + specialized agents.
- Orchestrates tasks and lifecycle management.

### LLM
- Provider routing, fallback, embeddings, local/hybrid routing.

### Memory
- Short/long-term stores, vector retrieval, knowledge graph.

### Learning
- Feedback collection, outcome processing, preference/policy updates.

### Automation
- Workflow runner, step interpretation, action validation/execution.

### Interface
- Command parser and routing from text/voice/UI.

### Dashboard
- Snapshot, telemetry logs, task status, feedback submission surface.

### Local AI
- Local inference, model lifecycle, compute orchestration.

### Web3
- Wallet, identity, and token authorization boundaries.

## 6. Feedback System (Implemented)

Feedback is implemented in:
- `learning/core/feedback_collector.py`
- `learning/core/learning_engine.py`
- `dashboard/backend/dashboard_api.py` (`submit_feedback` API)

Flow:
1. Client submits explicit feedback (and optional implicit metrics).
2. Dashboard API forwards to LearningEngine.
3. LearningEngine updates reinforcement policy score and persists local learning state.
4. Dashboard snapshot includes feedback summary for monitoring.

## 7. Runtime and Local E2E

No external BrowserOS clone is required for local execution.

Run local E2E:
```bash
python scripts/run-e2e.py
```

NPM wrapper:
```bash
npm run run:e2e
```

## 8. Build and Test Commands

```bash
npm run lint
npm test
npm run build-pwa
npm run build-mobile
npm run run:e2e
```

## 9. Security and Privacy Checklist

- Validate selectors/URLs/text before automation execution.
- Enforce permission checks for sensitive actions.
- Use risk-based routing for high-risk tasks.
- Keep local tracking opt-out (`tracking_enabled`) in learning engine.
- Redact sensitive values from logs.

## 10. Performance and Optimization Checklist

- Keep LLM provider fallback deterministic and deduplicated.
- Use bounded in-memory queues for feedback/interaction events.
- Cache repeated embeddings to reduce repeated vectorization calls.
- Prefer typed dataclasses and small immutable payloads where possible.

## 11. Contribution Workflow

- `main`: stable
- `develop`: integration
- `feature/*`: isolated features

Before opening a PR:
1. Run lint, test, and e2e commands.
2. Update relevant docs.
3. Add/adjust tests for behavior changes.
4. Keep commits scoped and descriptive.

## 12. Troubleshooting

- Import path errors in script mode:
  - Use the provided script entrypoints under `scripts/`.
- Missing build artifacts:
  - Run `npm run build-pwa` and `npm run build-mobile`.
- Learning data reset:
  - Call `LearningEngine.reset_user_learning_data(user_id)`.

## 13. Sequence for New Features

1. Define/adjust API protocol.
2. Implement module behavior.
3. Add tests (unit + integration).
4. Update architecture/module docs.
5. Validate via full command suite.
