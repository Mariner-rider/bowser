# interface

User-facing command and transport adapters.

## Responsibilities
- Text/voice/UI command normalization.
- Capacitor bridge adapters for mobile/desktop.
- Session and command context propagation.

## Framework Layout
- `core/command_schema.py`: structured command shape (`intent`, `entity`, constraints, metadata).
- `core/command_parser.py`: natural language to structured command conversion.
- `core/intent_router.py`: routes parsed commands to `AgentKernel` by intent.
- `voice/speech_to_text.py`: pluggable speech transcription adapter.
- `voice/voice_listener.py`: audio → text → command → AgentKernel pipeline.
- `text/text_input_handler.py`: text → command → AgentKernel pipeline.
- `capacitor_runtime.ts`: runtime detection/compatibility helper for web, iOS, and Android under Capacitor.

## Example Structured Command
```json
{
  "intent": "research_topic",
  "entity": "AI agents"
}
```
