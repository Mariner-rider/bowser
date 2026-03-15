# dashboard

Operational monitoring and governance surfaces.

## Responsibilities
- Trace, metric, and event aggregation.
- Agent run observability and failure analytics.
- Policy audit views and alerts.

## Framework Layout
- `backend/event_logger.py`: structured event/log storage.
- `backend/task_manager.py`: task status/progress tracking with automation-step history.
- `backend/agent_monitor.py`: active agent state tracking and pause/stop controls.
- `backend/dashboard_api.py`: API facade for snapshot reads and agent/task control actions.
- `frontend/dashboard_ui.tsx`: composed dashboard UI shell.
- `frontend/agent_panel.tsx`: active agent list with pause/stop controls.
- `frontend/task_viewer.tsx`: task progress and automation step viewer.
- `frontend/knowledge_brain_panel.tsx`: semantic knowledge search/topic exploration summary panel.
- `frontend/workflow_builder_panel.tsx`: visual autonomous workflow chain panel.
- `frontend/security_guardian_panel.tsx`: AI phishing/malicious activity warning panel.
- `frontend/marketplace_panel.tsx`: AI marketplace install surface for agent apps.
- `frontend/logs_panel.tsx`: realtime log panel.
