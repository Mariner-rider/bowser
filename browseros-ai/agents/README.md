# agents

Multi-agent orchestration runtime.

## Responsibilities
- Task decomposition and planning.
- Tool and model selection delegation.
- Policy-aware execution state machine.

## Framework Files
- `agent_base.py`: abstract contracts (`execute_task`, `plan_task`, `call_tools`) + shared interfaces for LLM, memory, and automation engines.
- `task_planner.py`: reusable planner that builds deterministic execution plans.
- `agent_registry.py`: specialized agents and registry factory for all capabilities.
- `agent_kernel.py`: task intake, routing, execution management, and lifecycle tracking.

## Multi-Agent Collaboration
- `collaboration/agent_orchestrator.py`: coordinator for phased parallel multi-agent workflows.
- `collaboration/agent_communication_bus.py`: inter-agent message bus for coordination events.
- `collaboration/task_scheduler.py`: schedule builder for parallel agent execution plans.
- `collaboration/shared_memory.py`: shared context/results store for collaborating agents.
- `security/privacy_security_guardian.py`: AI privacy/security guardian (phishing, scripts, downloads, cookies, extension risk).

## Self-Learning Integration
- `AgentKernel` can be wired with `learning/core/learning_engine.py` to capture interaction/outcome signals and improve future decisions.
