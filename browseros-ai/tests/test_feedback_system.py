import unittest

from pathlib import Path

from dashboard.backend.agent_monitor import AgentMonitor
from dashboard.backend.dashboard_api import DashboardAPI
from dashboard.backend.event_logger import EventLogger
from dashboard.backend.task_manager import TaskManager
from learning.core.learning_engine import LearningEngine


class FeedbackSystemTest(unittest.TestCase):
    def test_dashboard_feedback_submission_updates_learning(self) -> None:
        learning = LearningEngine(storage_path=Path("/tmp/browseros_ai_test_learning.json"))
        api = DashboardAPI(
            task_manager=TaskManager(),
            agent_monitor=AgentMonitor(),
            event_logger=EventLogger(),
            learning_engine=learning,
        )

        response = api.submit_feedback(
            user_id="u1",
            agent_name="research",
            task_kind="research",
            feedback="great",
            implicit={"latency_ms": 200},
        )

        self.assertTrue(response["ok"])
        self.assertIn("policy_score", response)
        self.assertEqual(response["summary"]["feedback_events"], 1)
        snapshot = api.get_snapshot()
        self.assertIn("feedback", snapshot)
        self.assertEqual(snapshot["feedback"]["feedback_events"], 1)


if __name__ == "__main__":
    unittest.main()
