import unittest

from marketplace.plugin_registry import PluginRegistry


class MarketplacePublicSubmissionTest(unittest.TestCase):
    def test_public_submission_publishes_manifest(self) -> None:
        registry = PluginRegistry()
        manifest = registry.publish_from_public_submission(
            {
                "agent_id": "community.alpha",
                "name": "Community Alpha",
                "version": "1.0.0",
                "description": "Public community agent",
                "capabilities": ["research", "automation"],
                "publisher_id": "pub-001",
                "publisher_name": "Alice",
                "price_usd": 9.99,
                "public_listing": True,
            }
        )
        self.assertEqual(manifest.publisher_name, "Alice")
        self.assertEqual(len(registry.list_public_marketplace()), 1)


if __name__ == "__main__":
    unittest.main()
