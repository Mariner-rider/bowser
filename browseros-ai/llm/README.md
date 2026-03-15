# llm

Universal model routing and provider abstraction.

## Responsibilities
- Provider routing by latency/cost/quality policy.
- Failover and retry strategies.
- Prompt safety and output policy checks.

## Framework Files
- `base_provider.py`: strict provider abstraction (`generate`, `stream`, `embed`) and shared provider config.
- `llm_router.py`: task-based router for `research`, `coding`, `automation`, and `summarization` with fallback chains.
- `providers/*.py`: concrete provider adapters (`openai`, `anthropic`, `rivinity`, `gemini`, `ollama`, `custom`).

## Local AI Supercomputer Mode Integration
- `llm_router.py` supports local/cloud/hybrid routing via optional local AI manager integration.
- Offline mode can force local inference for private/summarization/document tasks.
