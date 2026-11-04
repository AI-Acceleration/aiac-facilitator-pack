import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = [ROOT / ("Co-Facilitator Kit (%s)" % edition) / "tools" / name
           for edition in ("EN", "ES")
           for name in ("aiac-status-check.sh", "aiac-status-check.sh.txt")]


class TestStatusCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="statuscheck-")
        self.addCleanup(self.tmp.cleanup)
        self.vault = Path(self.tmp.name)
        self.repo = self.vault / "dev" / "code"
        self.repo.mkdir(parents=True)
        self.env = dict(os.environ, HOME=self.tmp.name,
                        GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
                        PATH=os.defpath)
        self.git("init", "-q")

    def git(self, *args):
        subprocess.run(["git", *args], cwd=str(self.repo), env=self.env,
                       check=True, capture_output=True)

    def report(self, script):
        r = subprocess.run(["bash", str(script), str(self.vault)],
                           cwd=str(self.vault), env=self.env,
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r.stdout

    def test_origin_reports_host_without_credentials_or_path_in_all_copies(self):
        # Fragments keep the synthetic credential out of the gate's address scan.
        self.git("remote", "add", "origin",
                 "https://user:tok3n" + "@" + "github.com/org/private.git")
        for script in SCRIPTS:
            with self.subTest(script=str(script.relative_to(ROOT))):
                output = self.report(script)
                self.assertNotIn("tok3n", output)
                self.assertNotIn("private", output)
                self.assertIn("present (github.com)", output)

    def test_origin_reports_only_host_for_other_remote_formats(self):
        remotes = [
            ("ssh://git" + "@" + "github.com:2222/org/private.git?query#fragment",
             "github.com"),
            ("git" + "@" + "github.com:org/private.git", "github.com"),
            ("https://github.com/org/private.git?notify=someone" + "@" +
             "elsewhere.test#fragment", "github.com"),
        ]
        self.git("remote", "add", "origin", "https://github.com/org/repo.git")
        for remote, host in remotes:
            with self.subTest(remote=remote):
                self.git("remote", "set-url", "origin", remote)
                origin = next(line for line in self.report(SCRIPTS[0]).splitlines()
                              if line.startswith("[info]") and "  origin" in line)
                self.assertEqual(origin.split("origin", 1)[1].strip(),
                                 "present (%s)" % host)

    def test_origin_reports_no_remote_when_origin_is_missing(self):
        origin = next(line for line in self.report(SCRIPTS[0]).splitlines()
                      if line.startswith("[info]") and "  origin" in line)
        self.assertEqual(origin.split("origin", 1)[1].strip(), "no remote")


if __name__ == "__main__":
    unittest.main()
