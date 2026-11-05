import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestSetupPermissions(unittest.TestCase):
    def test_tracked_markdown_has_no_blanket_git_permission(self):
        paths = subprocess.run(["git", "ls-files", "-z", "--", "*.md"],
                               cwd=str(ROOT), check=True,
                               capture_output=True).stdout.split(b"\0")
        self.assertTrue(any(paths), "no tracked Markdown files were checked")
        for raw in paths:
            if not raw:
                continue
            path = raw.decode("utf-8", "surrogateescape")
            with self.subTest(path=path):
                self.assertFalse("Bash(%s *)" % "git" in
                                 (ROOT / path).read_text(encoding="utf-8"),
                                 "blanket git permission in %s" % path)

    def test_templates_have_no_blanket_python_permission(self):
        for edition in ("EN", "ES"):
            templates = list((ROOT / ("Co-Facilitator Kit (%s)" % edition)).glob("*.md"))
            self.assertTrue(templates, "no %s templates were checked" % edition)
            for path in templates:
                text = path.read_text(encoding="utf-8")
                for command in ("python", "py", "python3"):
                    with self.subTest(path=str(path.relative_to(ROOT)), command=command):
                        self.assertFalse("Bash(%s *)" % command in text,
                                         "blanket %s permission in %s" % (command, path.name))


if __name__ == "__main__":
    unittest.main()
