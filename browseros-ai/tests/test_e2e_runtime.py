import pathlib
import subprocess
import sys
import unittest


class EndToEndRuntimeTest(unittest.TestCase):
    def test_e2e_script_runs_successfully(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[1]
        proc = subprocess.run(
            [sys.executable, "scripts/run-e2e.py"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr or proc.stdout)
        self.assertIn('"status": "completed"', proc.stdout)


if __name__ == "__main__":
    unittest.main()
