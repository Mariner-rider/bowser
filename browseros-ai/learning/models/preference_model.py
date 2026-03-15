"""Long-term user preference model for personalized agent behavior."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PreferenceModel:
    """Stores per-user long-term preferences and interests."""

    profiles: dict[str, dict[str, Any]] = field(default_factory=dict)

    def update_preferences(self, user_id: str, updates: dict[str, Any]) -> None:
        profile = self.profiles.setdefault(
            user_id,
            {
                "interests": [],
                "preferred_models": [],
                "favorite_websites": [],
                "writing_style": "balanced",
                "technical_depth": "medium",
            },
        )

        for key, value in updates.items():
            if key in {"interests", "preferred_models", "favorite_websites"}:
                if isinstance(value, list):
                    existing = set(profile.get(key, []))
                    profile[key] = sorted(existing.union(set(value)))
            else:
                profile[key] = value

    def get_profile(self, user_id: str) -> dict[str, Any]:
        return dict(self.profiles.get(user_id, {}))

    def reset_profile(self, user_id: str) -> None:
        self.profiles.pop(user_id, None)
