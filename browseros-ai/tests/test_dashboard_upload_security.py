import unittest

from dashboard.backend.agent_monitor import AgentMonitor
from dashboard.backend.dashboard_api import DashboardAPI
from dashboard.backend.event_logger import EventLogger
from dashboard.backend.task_manager import TaskManager


class DashboardUploadSecurityTest(unittest.TestCase):
    def test_secure_upload_and_recover(self) -> None:
        api = DashboardAPI(task_manager=TaskManager(), agent_monitor=AgentMonitor(), event_logger=EventLogger())
        secured = api.secure_upload(filename="wallet_secret.txt", content=b"very-sensitive", content_type="text/plain")
        self.assertTrue(secured["ok"])
        self.assertIn("sealed_upload", secured)

        recovered = api.recover_upload(secured["sealed_upload"])
        self.assertTrue(recovered["ok"])
        self.assertEqual(recovered["filename"], "wallet_secret.txt")
        self.assertEqual(recovered["content"], b"very-sensitive")


if __name__ == "__main__":
    unittest.main()
