"""Self-learning engine orchestrating feedback, analysis, preferences, and policy updates."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from ..analysis.behavior_analyzer import BehaviorAnalyzer
from ..models.preference_model import PreferenceModel
from ..training.reinforcement_trainer import ReinforcementTrainer
from .feedback_collector import FeedbackCollector


@dataclass(slots=True)
class LearningEngine:
    """Privacy-first local learning engine for self-improving agents."""

    feedback_collector: FeedbackCollector = field(default_factory=FeedbackCollector)
    behavior_analyzer: BehaviorAnalyzer = field(default_factory=BehaviorAnalyzer)
    preference_model: PreferenceModel = field(default_factory=PreferenceModel)
    reinforcement_trainer: ReinforcementTrainer = field(default_factory=ReinforcementTrainer)
    memory_engine: Any | None = None
    automation_engine: Any | None = None
    tracking_enabled: bool = True
    storage_path: Path = field(default_factory=lambda: Path("learning/local_learning_data.json"))

    def collect_interaction_data(self, event: dict[str, Any]) -> None:
        if not self.tracking_enabled:
            return
        self.feedback_collector.collect_interaction(event)
        self._store_learning_event(event)
        self._persist_local()

    def process_user_feedback(
        self,
        *,
        user_id: str,
        agent_name: str,
        task_kind: str,
        feedback: str,
        implicit: dict[str, Any] | None = None,
    ) -> float:
        """Capture explicit feedback and update reinforcement score."""
        if not self.tracking_enabled:
            return 0.0

        feedback_event = {
            "user_id": user_id,
            "agent_name": agent_name,
            "task_kind": task_kind,
            "feedback": feedback,
            "implicit": implicit or {},
        }
        self.feedback_collector.collect_feedback(feedback_event)
        self._store_learning_event(feedback_event)
        score = self.reinforcement_trainer.update_from_feedback(
            agent_name=agent_name,
            task_kind=task_kind,
            feedback=feedback,
            implicit=implicit,
        )
        self._persist_local()
        return score

    def update_from_outcome(self, *, user_id: str, agent_name: str, task_kind: str, status: str) -> float:
        if not self.tracking_enabled:
            return 0.0

        outcome_event = {
            "user_id": user_id,
            "agent_name": agent_name,
            "task_kind": task_kind,
            "status": status,
            "automation_signal": bool(self.automation_engine is not None),
        }
        self.feedback_collector.collect_interaction(outcome_event)
        self._store_learning_event(outcome_event)
        score = self.reinforcement_trainer.update_from_outcome(
            agent_name=agent_name,
            task_kind=task_kind,
            outcome_status=status,
        )
        self._persist_local()
        return score

    def update_preference_model(self, user_id: str) -> dict[str, Any]:
        interactions = self.feedback_collector.get_user_interactions(user_id)
        analysis = self.behavior_analyzer.analyze(interactions)
        self.preference_model.update_preferences(
            user_id,
            {
                "interests": analysis.get("interests", []),
            },
        )
        self._persist_local()
        return self.preference_model.get_profile(user_id)

    def recommended_policy_priority(self, agent_name: str, task_kind: str) -> str:
        key = f"{agent_name}:{task_kind}"
        return self.reinforcement_trainer.policy_model.recommend_priority(key)

    def get_feedback_summary(self, *, user_id: str | None = None) -> dict[str, Any]:
        """Return a compact summary for dashboard/API usage."""
        summary = self.feedback_collector.summary(user_id=user_id)
        return {
            **summary,
            "tracking_enabled": self.tracking_enabled,
            "known_users": len(self.preference_model.profiles),
        }

    def reset_user_learning_data(self, user_id: str) -> None:
        self.feedback_collector.reset_user(user_id)
        self.preference_model.reset_profile(user_id)
        self._persist_local()

    def set_tracking_enabled(self, enabled: bool) -> None:
        self.tracking_enabled = enabled
        self._persist_local()

    def _store_learning_event(self, event: dict[str, Any]) -> None:
        if self.memory_engine is None:
            return
        key = f"learning:{len(self.feedback_collector.interactions)}:{len(self.feedback_collector.feedback_events)}"
        self.memory_engine.remember("learning", key, event)

    def _persist_local(self) -> None:
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "tracking_enabled": self.tracking_enabled,
            "interactions": list(self.feedback_collector.interactions),
            "feedback_events": list(self.feedback_collector.feedback_events),
            "preferences": self.preference_model.profiles,
            "policy_scores": self.reinforcement_trainer.policy_model.policy_scores,
        }
        self.storage_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
