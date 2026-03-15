"""Policy model for agent decision preferences and reinforcement updates."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PolicyModel:
    """Tracks lightweight policy scores for agent-task combinations."""

    # Key format: "agent:task"
    policy_scores: dict[str, float] = field(default_factory=dict)

    def update_score(self, key: str, reward: float, learning_rate: float = 0.2) -> float:
        current = self.policy_scores.get(key, 0.0)
        updated = current + learning_rate * (reward - current)
        self.policy_scores[key] = updated
        return updated

    def get_score(self, key: str) -> float:
        return self.policy_scores.get(key, 0.0)

    def recommend_priority(self, key: str) -> str:
        score = self.get_score(key)
        if score >= 0.6:
            return "high"
        if score <= -0.2:
            return "low"
        return "medium"
