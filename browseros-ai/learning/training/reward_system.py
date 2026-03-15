"""Reward signal computation for reinforcement learning updates."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RewardSystem:
    """Converts outcomes and user feedback into scalar rewards."""

    def reward_from_outcome(self, status: str) -> float:
        normalized = status.lower()
        if normalized in {"completed", "success", "accepted"}:
            return 1.0
        if normalized in {"failed", "aborted", "rejected"}:
            return -1.0
        return 0.0

    def reward_from_feedback(self, feedback: str) -> float:
        normalized = feedback.strip().lower()
        if normalized in {"good", "up", "thumbs_up", "like", "positive"}:
            return 1.0
        if normalized in {"bad", "down", "thumbs_down", "dislike", "negative"}:
            return -1.0
        return 0.0

    def reward_from_implicit_signals(self, *, reading_time_s: int = 0, scroll_depth: float = 0.0, repeated_search: bool = False) -> float:
        reward = 0.0
        if reading_time_s >= 45:
            reward += 0.3
        if scroll_depth >= 0.7:
            reward += 0.3
        if repeated_search:
            reward += 0.2
        return reward
