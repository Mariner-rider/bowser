import pathlib
import unittest


class MergeConflictMarkerTest(unittest.TestCase):
    def test_repo_has_no_unresolved_merge_markers(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[1]
        markers = ("<<<<<<<", "=======", ">>>>>>>")
        offenders: list[str] = []

        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if any(part in {".git", "node_modules", "__pycache__"} for part in path.parts):
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except Exception:
                continue
            lines = content.splitlines()
            for i, line in enumerate(lines, start=1):
                if line.startswith(markers):
                    offenders.append(f"{path.relative_to(root)}:{i}:{line}")

        self.assertFalse(offenders, "Unresolved merge conflict markers found:\n" + "\n".join(offenders))


if __name__ == "__main__":
    unittest.main()
