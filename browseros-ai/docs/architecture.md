# System Architecture Specification

This document defines the production architecture for the BrowserOS AI extension, including module responsibilities, API boundaries, data flows, and dependency rules.

## 1) High-Level Layered Architecture

The system is organized into four layers.

### User Layer

- Voice commands
- Text commands
- Dashboard UI
- Browser UI components

Primary modules:
- `interface/voice/*`
- `interface/text/*`
- `interface/core/*`
- `dashboard/frontend/*`
- `ui/*`

### Intelligence Layer

- Agent Kernel
- LLM Router
- Memory System
- Learning Engine

Primary modules:
- `agents/*`
- `llm/*`
- `memory/*`
- `learning/*`

### Execution Layer

- Automation Engine
- Workflow Runner
- Page Interpreter
- Action Executor

Primary modules:
- `automation/core/*`
- `automation/page/*`
- `automation/actions/*`

### Infrastructure Layer

- BrowserOS runtime bridge
- Networking policy gateway
- Filesystem/runtime adapters
- Security sandbox and permissions

Primary modules:
- `core/chromium_bridge/*`
- `core/networking/*`
- `core/security/*`
- `local_ai/*`
- `mobile/*`

## 2) Core Component Interaction Map

```text
User
 ↓
Command Interface
 ↓
Intent Parser
 ↓
Agent Kernel
 ↓
Task Planner
 ↓
LLM Router
 ↓
Agent Execution
 ↓
Automation Engine
 ↓
Browser Runtime
 ↓
Website Interaction

Meanwhile:
Memory Engine   ←→ Agent Kernel
Learning Engine ←→ Agent Kernel
Dashboard       ← Event Logger ← All modules
```

## 3) Complete Interaction Diagram

```text
                    USER
                     │
        ┌────────────┴─────────────┐
        │                          │
   Voice Interface            Text Interface
        │                          │
        └────────────┬─────────────┘
                     │
               Command Parser
                     │
               Intent Router
                     │
                Agent Kernel
                     │
     ┌───────────────┼────────────────┐
     │               │                │
Memory Engine    LLM Router      Learning Engine
     │               │                │
     │               │         Preference Model
     │               │
     │        Local AI Manager
     │               │
     └───────────────┼────────────────┘
                     │
              Automation Engine
                     │
               Workflow Runner
                     │
               Action Executor
                     │
              BrowserOS Runtime
                     │
                  Internet
```

## 4) Module Responsibilities, APIs, Data Flow, Dependencies

### Agent Kernel (`agents/agent_kernel.py`)

Responsibilities:
- Receive normalized commands/tasks.
- Select agent(s) from registry.
- Track task lifecycle (`received → planned → running → completed/failed`).
- Coordinate memory, model calls, and automation execution.

Public API:
- `submit_task(task)`
- `get_task_status(task_id)`
- `cancel_task(task_id)`

Dependencies:
- `agents/agent_registry.py`
- `agents/task_planner.py`
- `llm/llm_router.py`
- `memory/core/memory_manager.py`
- `automation/core/automation_controller.py`
- `dashboard/backend/event_logger.py`

Data flow:
1. Receives task envelope from interface layer.
2. Queries memory for context.
3. Requests planning/generation through LLM Router.
4. Dispatches execution to agent/automation.
5. Emits telemetry and updates learning inputs.

### LLM Router (`llm/llm_router.py`)

Responsibilities:
- Route prompts to best provider/model.
- Support cloud/local/hybrid execution.
- Provide generation, streaming, and embeddings.

Public API:
- `generate(prompt)`
- `stream(prompt)`
- `embed(text)`

Dependencies:
- `llm/base_provider.py`
- `llm/providers/*`
- `local_ai/core/local_ai_manager.py`

Data flow:
1. Accepts generation request from agents.
2. Applies routing policy by task type/risk/privacy.
3. Invokes provider or local engine.
4. Returns model output + usage metadata.

### Memory Engine (`memory/*`)

Responsibilities:
- Persist and retrieve short/long-term memory.
- Support semantic search and graph-based context.
- Build user-centric knowledge context for agents.

Public API:
- `store_memory(data)`
- `search_memory(query)`
- `retrieve_context()`

Dependencies:
- `memory/core/*`
- `memory/vector/*`
- `memory/graph/*`

Data flow:
1. Stores task artifacts and user signals.
2. Returns context bundles to Agent Kernel.
3. Exposes semantic + graph retrieval for planning.

### Automation Engine (`automation/*`)

Responsibilities:
- Execute browser actions under guardrails.
- Interpret pages, validate actions, and run workflows.

Public API:
- `execute_action(action)`
- `run_workflow(workflow)`

Dependencies:
- `automation/core/workflow_runner.py`
- `automation/page/page_interpreter.py`
- `automation/actions/action_validator.py`
- `core/chromium_bridge/bridge_adapter.py`

Data flow:
1. Consumes action plan from Agent Kernel.
2. Resolves selectors/page state.
3. Validates against policy and risk.
4. Executes action and reports result/logs.

### Learning Engine (`learning/*`)

Responsibilities:
- Capture feedback and task outcomes.
- Update policy and user preference models.
- Provide adaptation hints to Agent Kernel.

Public API:
- `collect_feedback(event)`
- `train_policy(batch)`
- `update_preferences(user_id)`

Dependencies:
- `learning/core/*`
- `learning/models/*`
- `learning/training/*`

Data flow:
1. Ingests interaction/outcome events.
2. Produces updated preference/policy signals.
3. Feeds adaptation hints into planning/routing.

### Local AI Engine (`local_ai/*`)

Responsibilities:
- Run local/offline inference.
- Schedule GPU workloads and model assets.
- Coordinate distributed nodes when enabled.

Public API:
- `load_model(model_id)`
- `run_inference(request)`
- `schedule_workload(workload)`

Dependencies:
- `local_ai/core/inference_engine.py`
- `local_ai/compute/gpu_scheduler.py`
- `local_ai/models/model_downloader.py`
- `local_ai/cluster/cluster_coordinator.py`

Data flow:
1. Receives routed local request from LLM Router.
2. Ensures model availability.
3. Schedules compute and executes inference.
4. Returns output/metrics to LLM Router.

### Dashboard (`dashboard/*`)

Responsibilities:
- Aggregate telemetry, logs, and task metrics.
- Provide observability and operational controls.

Public API:
- `publish_event(event)`
- `get_system_snapshot()`
- `get_task_timeline(task_id)`

Dependencies:
- `dashboard/backend/event_logger.py`
- `dashboard/backend/dashboard_api.py`
- `dashboard/backend/agent_monitor.py`
- `dashboard/frontend/*`

Data flow:
1. Ingests events from all modules.
2. Stores and serves snapshots/timelines.
3. Renders live status in dashboard panels.

### Web3 Layer (`web3/*`)

Responsibilities:
- Wallet connection and identity verification.
- Token-based authorization for protected features.

Public API:
- `connect_wallet(request)`
- `verify_identity(address, signature)`
- `authorize_feature(token, capability)`

Dependencies:
- `web3/wallet_manager.ts`
- `web3/blockchain_connector.ts`
- `web3/identity_manager.ts`
- `web3/token_auth.ts`

Data flow:
1. Receives login/permission request.
2. Verifies ownership and chain identity.
3. Returns access decision/policy context.

### Capacitor Mobile Runtime (`mobile/*`, `interface/capacitor_runtime.ts`)

Responsibilities:
- Wrap web runtime for iOS/Android deployment.
- Bridge native features for voice, wallet handoff, and storage.

Public API:
- `initialize_mobile_runtime()`
- `sync_web_assets()`
- `invoke_native_capability(name, payload)`

Dependencies:
- `capacitor.config.ts`
- `mobile/capacitor.config.ts`
- `interface/capacitor_runtime.ts`

Data flow:
1. Loads Browser UI bundle into Capacitor shell.
2. Proxies runtime calls to native platform.
3. Returns responses back to interface modules.

## 5) Event and Monitoring Pipeline

```text
Agent Action
 ↓
Event Logger
 ↓
Event Database (or storage adapter)
 ↓
Dashboard API
 ↓
Dashboard UI
```

Event contract requirements:
- Include `trace_id`, `task_id`, `module`, `severity`, `timestamp`.
- Preserve causal ordering for per-task timelines.
- Redact sensitive payload fields before persistence.

## 6) Web3 Integration Flow

```text
User login
 ↓
Wallet Manager
 ↓
Blockchain Connector
 ↓
Identity verification
 ↓
Access browser features
```

Use cases:
- Token-based permissions
- Decentralized identity profile
- Marketplace payments

## 7) Cross-Platform Delivery Flow

```text
Browser UI
 ↓
Capacitor Runtime
 ↓
Android / iOS
```

The same UI and intelligence stack should execute on desktop, PWA, Android, and iOS with platform-specific adapters only at runtime boundaries.

## 8) Architecture Rules (Non-Negotiable)

1. AI modules must call browser runtime only through `core/chromium_bridge`.
2. High-risk actions require explicit policy checks in security layer.
3. Agents do not call model providers directly; they call `llm_router`.
4. All modules must emit telemetry with consistent trace IDs.
5. Web3 signing/identity flows remain isolated from general automation tasks.
6. Local AI execution must support explicit fallback to cloud providers.
