"""Behavior analyzer for user interests and task success patterns."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .pattern_detector import PatternDetector


@dataclass(slots=True)
class BehaviorAnalyzer:
    """Analyzes browsing/task history and extracts preference signals."""

    detector: PatternDetector = field(default_factory=PatternDetector)

    def analyze(self, interactions: list[dict[str, Any]]) -> dict[str, Any]:
        descriptions = [str(i.get("description", "")) for i in interactions]
        interests = self.detector.top_terms(descriptions, limit=8)
        frequent_tasks = self.detector.frequent_values(interactions, "task_kind", limit=5)
        outcomes = self.detector.frequent_values(interactions, "status", limit=3)

        return {
            "interests": interests,
            "frequent_workflows": frequent_tasks,
            "task_success_patterns": outcomes,
        }
