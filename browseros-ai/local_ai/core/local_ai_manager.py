"""Local AI manager for offline/hybrid model routing and lifecycle management."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator

from ..cluster.cluster_coordinator import ClusterCoordinator
from ..compute.gpu_scheduler import GPUScheduler
from ..models.model_downloader import ModelDownloader
from ..models.model_registry import ModelMetadata, ModelRegistry
from .inference_engine import InferenceEngine


SUPPORTED_ENGINES = ("ollama", "llama.cpp", "vllm", "lm_studio", "tensorrt_llm")


@dataclass(slots=True)
class LocalAIManager:
    """Facade for local AI supercomputer mode."""

    model_registry: ModelRegistry = field(default_factory=ModelRegistry)
    model_downloader: ModelDownloader = field(default_factory=ModelDownloader)
    gpu_scheduler: GPUScheduler = field(default_factory=GPUScheduler)
    cluster_coordinator: ClusterCoordinator = field(default_factory=ClusterCoordinator)
    inference_engines: dict[str, InferenceEngine] = field(
        default_factory=lambda: {name: InferenceEngine(name) for name in SUPPORTED_ENGINES}
    )

    def detect_local_engines(self) -> list[str]:
        return list(self.inference_engines.keys())

    def install_model(
        self,
        *,
        model_id: str,
        family: str,
        backend: str,
        source_url: str,
        target_dir: str,
        size_billion_params: float,
        quantization: str | None = None,
    ) -> ModelMetadata:
        metadata = self.model_downloader.download(
            model_id=model_id,
            family=family,
            backend=backend,
            source_url=source_url,
            target_dir=target_dir,
            size_billion_params=size_billion_params,
            quantization=quantization,
        )
        self.model_registry.register(metadata)
        return metadata

    def route_inference(self, *, task_kind: str, prefer_local: bool = True, offline_mode: bool = False) -> str:
        if offline_mode:
            return "local"
        if task_kind in {"summarization", "private_docs", "document_analysis"}:
            return "local"
        if task_kind in {"complex_reasoning"} and not prefer_local:
            return "cloud"
        return "local" if prefer_local else "hybrid"

    def generate(self, *, model_id: str, prompt: str, stream: bool = False) -> str | Iterator[str]:
        model = self.model_registry.get(model_id)
        if model is None:
            raise KeyError(f"Model not installed: {model_id}")

        workload = {
            "model_id": model_id,
            "estimated_gpu_gb": max(1.0, model.size_billion_params * 0.5),
            "prompt_len": len(prompt),
        }
        self.gpu_scheduler.enqueue(workload)
        self.gpu_scheduler.allocate_next()

        engine = self.inference_engines.get(model.backend)
        if engine is None:
            raise ValueError(f"Unsupported backend: {model.backend}")

        if stream:
            return engine.stream(model, prompt)
        return engine.generate(model, prompt)

    def distributed_inference(self, workload: dict[str, Any]) -> dict[str, Any]:
        return self.cluster_coordinator.dispatch(workload)
