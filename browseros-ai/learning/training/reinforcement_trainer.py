"""Reinforcement trainer that updates policy model from reward signals."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..models.policy_model import PolicyModel
from .reward_system import RewardSystem


@dataclass(slots=True)
class ReinforcementTrainer:
    """Updates policy decisions based on outcomes and feedback loops."""

    policy_model: PolicyModel = field(default_factory=PolicyModel)
    reward_system: RewardSystem = field(default_factory=RewardSystem)

    def update_from_outcome(self, *, agent_name: str, task_kind: str, outcome_status: str) -> float:
        reward = self.reward_system.reward_from_outcome(outcome_status)
        key = f"{agent_name}:{task_kind}"
        return self.policy_model.update_score(key, reward)

    def update_from_feedback(self, *, agent_name: str, task_kind: str, feedback: str, implicit: dict[str, Any] | None = None) -> float:
        reward = self.reward_system.reward_from_feedback(feedback)
        if implicit:
            reward += self.reward_system.reward_from_implicit_signals(
                reading_time_s=int(implicit.get("reading_time_s", 0)),
                scroll_depth=float(implicit.get("scroll_depth", 0.0)),
                repeated_search=bool(implicit.get("repeated_search", False)),
            )
        key = f"{agent_name}:{task_kind}"
        return self.policy_model.update_score(key, reward)
