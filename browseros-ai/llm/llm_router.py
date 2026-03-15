"""Universal AI model router with task-based routing, fallback, streaming, and local AI mode."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterator, Protocol

from .base_provider import BaseProvider


class SupportedTask(str, Enum):
    RESEARCH = "research"
    CODING = "coding"
    AUTOMATION = "automation"
    SUMMARIZATION = "summarization"


@dataclass(slots=True)
class RoutePolicy:
    """Task routing policy with primary and fallback providers."""

    primary_provider: str
    fallback_providers: list[str] = field(default_factory=list)


class LocalAIManagerProtocol(Protocol):
    """Protocol for local AI supercomputer mode integration."""

    def route_inference(self, *, task_kind: str, prefer_local: bool = True, offline_mode: bool = False) -> str:
        ...

    def generate(self, *, model_id: str, prompt: str, stream: bool = False) -> str | Iterator[str]:
        ...


@dataclass(slots=True)
class LLMRouter:
    """Routes tasks across local/cloud providers through a clean abstraction layer."""

    providers: dict[str, BaseProvider]
    task_routes: dict[SupportedTask, RoutePolicy]
    default_route: RoutePolicy
    local_ai_manager: LocalAIManagerProtocol | None = None
    local_task_models: dict[SupportedTask, str] = field(default_factory=dict)

    def generate(self, task: SupportedTask | str, prompt: str, **kwargs: Any) -> str:
        """Generate full response for task with local/cloud/hybrid fallback."""

        normalized = self._normalize_task(task)
        prefer_local = bool(kwargs.pop("prefer_local", False))
        offline_mode = bool(kwargs.pop("offline_mode", False))

        local_output = self._generate_local(normalized, prompt, prefer_local=prefer_local, offline_mode=offline_mode)
        if local_output is not None:
            return local_output

        provider_errors: list[str] = []
        for provider in self._provider_chain(normalized):
            try:
                return provider.generate(prompt, **kwargs)
            except Exception as exc:
                provider_errors.append(f"{provider.name}: {exc}")

        joined_errors = "; ".join(provider_errors) or "no providers available"
        raise RuntimeError(f"All providers failed for task={normalized.value}: {joined_errors}")

    def stream(self, task: SupportedTask | str, prompt: str, **kwargs: Any) -> Iterator[str]:
        """Stream response chunks with local/cloud/hybrid fallback."""

        normalized = self._normalize_task(task)
        prefer_local = bool(kwargs.pop("prefer_local", False))
        offline_mode = bool(kwargs.pop("offline_mode", False))

        local_stream = self._stream_local(normalized, prompt, prefer_local=prefer_local, offline_mode=offline_mode)
        if local_stream is not None:
            yield from local_stream
            return

        provider_errors: list[str] = []
        for provider in self._provider_chain(normalized):
            try:
                yield from provider.stream(prompt, **kwargs)
                return
            except Exception as exc:
                provider_errors.append(f"{provider.name}: {exc}")

        joined_errors = "; ".join(provider_errors) or "no providers available"
        raise RuntimeError(f"All providers failed for streaming task={normalized.value}: {joined_errors}")

    def embed(self, text: str, provider_name: str | None = None, **kwargs: Any) -> list[float]:
        """Compute embeddings using explicit provider or default primary."""

        if provider_name:
            return self._get_provider(provider_name).embed(text, **kwargs)

        default_provider = self._get_provider(self.default_route.primary_provider)
        return default_provider.embed(text, **kwargs)

    def _normalize_task(self, task: SupportedTask | str) -> SupportedTask:
        if isinstance(task, SupportedTask):
            return task
        return SupportedTask(task)

    def _get_provider(self, name: str) -> BaseProvider:
        if name not in self.providers:
            raise KeyError(f"Provider '{name}' is not registered")
        return self.providers[name]

    def _provider_chain(self, task: SupportedTask | str) -> list[BaseProvider]:
        normalized = self._normalize_task(task)
        route = self.task_routes.get(normalized, self.default_route)
        seen: set[str] = set()
        ordered_names: list[str] = []
        for name in [route.primary_provider, *route.fallback_providers]:
            if name not in seen:
                ordered_names.append(name)
                seen.add(name)
        return [self._get_provider(name) for name in ordered_names]

    def _generate_local(self, task: SupportedTask, prompt: str, *, prefer_local: bool, offline_mode: bool) -> str | None:
        if self.local_ai_manager is None:
            return None

        decision = self.local_ai_manager.route_inference(
            task_kind=task.value,
            prefer_local=prefer_local,
            offline_mode=offline_mode,
        )
        if decision not in {"local", "hybrid"}:
            return None

        local_model_id = self.local_task_models.get(task)
        if not local_model_id:
            return None

        try:
            output = self.local_ai_manager.generate(model_id=local_model_id, prompt=prompt, stream=False)
            return output if isinstance(output, str) else "".join(output)
        except Exception:
            if decision == "local":
                raise
            return None

    def _stream_local(
        self,
        task: SupportedTask,
        prompt: str,
        *,
        prefer_local: bool,
        offline_mode: bool,
    ) -> Iterator[str] | None:
        if self.local_ai_manager is None:
            return None

        decision = self.local_ai_manager.route_inference(
            task_kind=task.value,
            prefer_local=prefer_local,
            offline_mode=offline_mode,
        )
        if decision not in {"local", "hybrid"}:
            return None

        local_model_id = self.local_task_models.get(task)
        if not local_model_id:
            return None

        try:
            local_output = self.local_ai_manager.generate(model_id=local_model_id, prompt=prompt, stream=True)
            if isinstance(local_output, str):
                return iter([local_output])
            return iter(local_output)
        except Exception:
            if decision == "local":
                raise
            return None
