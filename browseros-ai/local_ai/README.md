# local_ai

Local AI Supercomputer Mode for offline/private/distributed inference.

## Structure
- `core/local_ai_manager.py`: local engine detection, model lifecycle, inference routing.
- `core/inference_engine.py`: local inference and streaming generation adapter.
- `models/model_registry.py`: installed model metadata tracking.
- `models/model_downloader.py`: trusted model download/update abstraction.
- `compute/gpu_scheduler.py`: GPU workload queueing and prioritization.
- `compute/resource_monitor.py`: resource snapshot telemetry for scheduling.
- `cluster/node_manager.py`: distributed node registration/management.
- `cluster/cluster_coordinator.py`: distributed inference dispatch.

## Supported backends
- Ollama
- llama.cpp
- vLLM
- LM Studio
- TensorRT-LLM

## Integration points
- `llm/llm_router.py` for local/cloud/hybrid inference routing.
- `agents/` via local inference policy preferences.
- `memory/` for private local-context inference.
- `automation/` for offline automation planning.
