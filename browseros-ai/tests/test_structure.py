import pathlib
import unittest


class StructureTest(unittest.TestCase):
    def test_expected_directories_exist(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[1]
        expected = [
            "core",
            "agents",
            "llm",
            "memory",
            "automation",
            "learning",
            "local_ai",
            "interface",
            "dashboard",
            "web3",
            "mobile",
            "ui",
            "sdk",
            "tests",
            "docs",
            "scripts",
            "docker",
        ]
        for directory in expected:
            self.assertTrue((root / directory).exists(), f"missing: {directory}")


if __name__ == "__main__":
    unittest.main()
