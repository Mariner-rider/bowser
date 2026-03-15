# automation

Autonomous web automation with guardrails.

## Responsibilities
- Browser task runner and action planner.
- Domain and permission safety enforcement.
- Confirmation checkpoints for sensitive actions.

## Framework Layout
- `core/automation_controller.py`: automation task lifecycle manager.
- `core/workflow_runner.py`: multi-step workflow executor.
- `page/page_interpreter.py`: interprets workflow steps into executable actions.
- `page/element_locator.py`: resolves semantic targets to selectors.
- `actions/action_executor.py`: primitive browser actions (`click_element`, `type_text`, `scroll_page`, `navigate_url`) with logging.
- `actions/action_validator.py`: input validation and guardrails for action execution.
- `builder/workflow_schema.py`: visual workflow node/definition schema.
- `builder/autonomous_workflow_builder.py`: visual AI workflow creation + execution (Zapier-style).
