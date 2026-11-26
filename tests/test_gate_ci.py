"""The CI side of the gate: bin/gate_surface_pin.sh, bin/gate_pr_check.sh and
the workflow files that call them.

CI logs are public, so the main property tested here is that a changed or
offending file NAME never reaches the output, whatever it holds. Synthetic
addresses are built from fragments (this file is itself scanned by the gate)
and live at the reserved `.test` TLD.
"""
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"
WORKFLOWS = ROOT / ".github" / "workflows"

DOMAIN = "example-invalid" + ".test"
UNKNOWN = "someone.else" + "@" + DOMAIN
GIT_EMAIL = "t" + "@" + DOMAIN
# A file name that is sensitive without holding an address: nothing in the
# output may echo it either.
PRIVATE_WORD = "participant-surname-zqxv"


class CiSandbox(unittest.TestCase):
    """A repo whose `main` holds the REAL gate scripts and pattern files (deny
    list swapped for the synthetic fixture), plus a `pr` branch to judge.
    The working tree stays on main: like CI, the checkout is the base."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="gateci-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        (self.tmp / "bin").mkdir()
        for name in ("gate_scan.py", "gate_surface_pin.sh", "gate_pr_check.sh"):
            shutil.copy2(ROOT / "bin" / name, self.tmp / "bin" / name)
        shutil.copytree(ROOT / ".githooks", self.tmp / ".githooks")
        shutil.copy2(FIXTURES / "deny-hashes-test.txt",
                     self.tmp / ".githooks" / "deny-hashes.txt")
        with open(self.tmp / ".githooks" / "allow-patterns.txt", "a",
                  encoding="utf-8") as f:
            f.write("\n%s\n" % GIT_EMAIL)
        (self.tmp / ".github").mkdir()
        (self.tmp / ".github" / "ci.yml").write_text("name: ci\n", encoding="utf-8")
        (self.tmp / "doc.md").write_text("clean body\n", encoding="utf-8")
        self.git("init", "-q")
        self.git("config", "user.email", GIT_EMAIL)
        self.git("config", "user.name", "t")
        self.git("checkout", "-q", "-b", "main")
        self.git("add", "-A")
        self.git("commit", "-q", "--no-verify", "-m", "base")
        self.git("branch", "pr")

    def git(self, *args, **kw):
        return subprocess.run(["git", *args], cwd=str(self.tmp), check=True,
                              capture_output=True, **kw)

    def on_pr(self, files, message="pr change"):
        """Commit `files` ({path: text}) on the pr branch without touching
        main's working tree: objects only, the way CI receives a PR."""
        idx = self.tmp / ".git" / "pr-index"
        env = dict(os.environ, GIT_INDEX_FILE=str(idx))
        self.git("read-tree", "pr", env=env)
        for path, text in files.items():
            blob = self.git("hash-object", "-w", "--stdin",
                            input=text.encode("utf-8")).stdout.strip().decode()
            self.git("update-index", "--add", "--cacheinfo",
                     "100644,%s,%s" % (blob, path), env=env)
        tree = self.git("write-tree", env=env).stdout.strip().decode()
        idx.unlink()
        sha = self.git("commit-tree", tree, "-p", "pr", "-m", message
                       ).stdout.strip().decode()
        self.git("update-ref", "refs/heads/pr", sha)
        return sha

    def run_script(self, name, *args):
        return subprocess.run(["bash", str(self.tmp / "bin" / name), *args],
                              cwd=str(self.tmp), capture_output=True, text=True)

    def assertNothingLeaks(self, r, *needles):
        out = r.stdout + r.stderr
        for n in needles + (DOMAIN, PRIVATE_WORD):
            self.assertNotIn(n, out)


class TestSurfacePin(CiSandbox):
    def test_changed_surface_names_are_never_printed(self):
        self.on_pr({".github/%s.yml" % UNKNOWN: "x\n",
                    "bin/%s.sh" % PRIVATE_WORD: "x\n",
                    ".githooks/notes %s" % PRIVATE_WORD: "x\n"})
        r = self.run_script("gate_surface_pin.sh", "main", "pr")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("BLOCKED", r.stdout)
        self.assertIn("3 path(s)", r.stdout)
        self.assertNothingLeaks(r, UNKNOWN, "someone.else")

    def test_name_with_newline_counts_once_and_is_not_printed(self):
        self.on_pr({".github/a\n%s.yml" % PRIVATE_WORD: "x\n"})
        r = self.run_script("gate_surface_pin.sh", "main", "pr")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("1 path(s)", r.stdout)
        self.assertNothingLeaks(r)

    def test_edit_to_existing_surface_file_is_blocked(self):
        self.on_pr({".github/ci.yml": "name: neutered\n"})
        r = self.run_script("gate_surface_pin.sh", "main", "pr")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertNotIn("ci.yml", r.stdout + r.stderr)

    def test_change_outside_the_surface_passes(self):
        self.on_pr({"doc.md": "changed body\n"})
        r = self.run_script("gate_surface_pin.sh", "main", "pr")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_branch_behind_a_main_side_gate_change_passes(self):
        # main changed the surface after the PR branched; the PR did not.
        self.on_pr({"doc.md": "changed body\n"})
        (self.tmp / ".github" / "ci.yml").write_text("name: ci v2\n",
                                                     encoding="utf-8")
        self.git("commit", "-q", "--no-verify", "-am", "main-side gate change")
        r = self.run_script("gate_surface_pin.sh", "main", "pr")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_codeowners_change_is_blocked_and_not_named(self):
        # CODEOWNERS decides who must review the surface, so it is surface.
        self.on_pr({"CODEOWNERS": "* @%s\n" % PRIVATE_WORD})
        r = self.run_script("gate_surface_pin.sh", "main", "pr")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("1 path(s)", r.stdout)
        self.assertNothingLeaks(r)

    def test_codeowners_in_docs_is_blocked_and_not_named(self):
        # GitHub falls back to docs/CODEOWNERS; it is pinned too.
        self.on_pr({"docs/CODEOWNERS": "* @%s\n" % PRIVATE_WORD})
        r = self.run_script("gate_surface_pin.sh", "main", "pr")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("1 path(s)", r.stdout)
        self.assertNotIn("docs/", r.stdout + r.stderr)
        self.assertNothingLeaks(r)

    def test_edit_to_existing_codeowners_is_blocked(self):
        (self.tmp / "CODEOWNERS").write_text("* @owner\n", encoding="utf-8")
        self.git("add", "CODEOWNERS")
        self.git("commit", "-q", "--no-verify", "-m", "codeowners")
        self.git("branch", "-f", "pr", "main")
        self.on_pr({"CODEOWNERS": "# emptied\n"})
        r = self.run_script("gate_surface_pin.sh", "main", "pr")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("1 path(s)", r.stdout)

    def test_gate_tests_are_not_pinned(self):
        # Tests never run in the gate job, so they are reviewed (CODEOWNERS)
        # but not pinned: a test-only PR is not an admin merge.
        self.on_pr({"tests/test_gate_new.py": "x = 1\n",
                    "tests/fixtures/extra.txt": "x\n"})
        r = self.run_script("gate_surface_pin.sh", "main", "pr")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_unresolvable_commit_fails_loud(self):
        r = self.run_script("gate_surface_pin.sh", "main", "f" * 40)
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertIn("GATE ERROR", r.stderr)


class TestPrCheck(CiSandbox):
    def test_clean_pr_passes(self):
        sha = self.on_pr({"kit/new doc.md": "clean\n"})
        r = self.run_script("gate_pr_check.sh", "main", sha)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("tree", r.stdout)
        self.assertIn("history", r.stdout)

    def test_address_in_pr_file_is_blocked_and_redacted(self):
        sha = self.on_pr({"kit/doc.md": "route to %s\n" % UNKNOWN})
        r = self.run_script("gate_pr_check.sh", "main", sha)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("UNALLOWLISTED", r.stderr)
        self.assertNothingLeaks(r, UNKNOWN)

    def test_pr_file_is_scanned_though_main_checkout_lacks_it(self):
        # The working tree is main's: the PR's file exists only as objects.
        sha = self.on_pr({"kit/doc.md": "route to %s\n" % UNKNOWN})
        self.assertFalse((self.tmp / "kit").exists())
        self.assertEqual(self.run_script("gate_pr_check.sh", "main", sha).returncode, 1)

    def test_sensitive_surface_name_never_printed_by_any_check(self):
        sha = self.on_pr({".github/%s.yml" % UNKNOWN: "x\n",
                          "bin/%s.sh" % PRIVATE_WORD: "x\n"})
        r = self.run_script("gate_pr_check.sh", "main", sha)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("2 path(s)", r.stdout)
        self.assertIn("[redacted#", r.stderr)  # the scanner's own finding
        out = r.stdout + r.stderr
        self.assertNotIn(UNKNOWN, out)
        self.assertNotIn(DOMAIN, out)
        # The non-address name is reported only by the surface pin, by count.
        self.assertNotIn(PRIVATE_WORD, out)

    def test_withheld_file_in_pr_is_blocked(self):
        sha = self.on_pr({"kit/00 — Trainer Registry.md": "x\n"})
        r = self.run_script("gate_pr_check.sh", "main", sha)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("FORBIDDEN BASENAME", r.stderr)

    def test_pr_cannot_loosen_the_scanner_that_judges_it(self):
        # The PR replaces the scanner with one that always passes and adds a
        # leak. The check runs main's scanner, so the leak is still caught.
        sha = self.on_pr({"bin/gate_scan.py": "import sys\nsys.exit(0)\n",
                          ".githooks/allow-patterns.txt": UNKNOWN + "\n",
                          "kit/doc.md": "route to %s\n" % UNKNOWN})
        r = self.run_script("gate_pr_check.sh", "main", sha)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("UNALLOWLISTED", r.stderr)
        self.assertIn("BLOCKED: this change edits the gate surface", r.stdout)

    def test_address_in_pr_commit_message_is_blocked(self):
        sha = self.on_pr({"doc.md": "changed\n"}, "thanks %s" % UNKNOWN)
        r = self.run_script("gate_pr_check.sh", "main", sha)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("commit message", r.stderr)
        self.assertNothingLeaks(r, UNKNOWN)

    def test_head_not_reachable_from_a_ref_fails_loud(self):
        sha = self.on_pr({"doc.md": "changed\n"})
        self.git("update-ref", "refs/heads/pr", "main")
        r = self.run_script("gate_pr_check.sh", "main", sha)
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertIn("not reachable", r.stderr)

    def test_unresolvable_head_fails_loud(self):
        r = self.run_script("gate_pr_check.sh", "main", "f" * 40)
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)


class TestWorkflows(unittest.TestCase):
    """Static checks on the workflow text: the trust boundary is in YAML, and
    a careless edit to it would not fail any other test."""

    def setUp(self):
        self.gate = (WORKFLOWS / "gate.yml").read_text(encoding="utf-8")
        self.tests = (WORKFLOWS / "tests.yml").read_text(encoding="utf-8")

    def code(self, text):
        return "\n".join(l for l in text.splitlines()
                         if not l.lstrip().startswith("#"))

    def test_gate_runs_from_main_not_from_the_pr(self):
        gate = self.code(self.gate)
        self.assertRegex(gate, r"(?m)^  pull_request_target:")
        self.assertNotRegex(gate, r"(?m)^  pull_request:")
        self.assertIn("bash bin/gate_pr_check.sh", gate)

    def test_gate_judges_only_pull_requests_into_main(self):
        # On pull_request_target the trusted code is the base branch's tip;
        # only main is protected, so only PRs into main may be judged.
        gate = self.code(self.gate)
        self.assertRegex(gate, r"(?m)^  pull_request_target:\n"
                               r"    branches: \[main\]$")

    def test_pin_and_codeowners_cover_the_same_surface(self):
        pin = (ROOT / "bin" / "gate_surface_pin.sh").read_text(encoding="utf-8")
        m = re.search(r"(?m)^SURFACE=\(([^)]*)\)$", pin)
        self.assertIsNotNone(m)
        surface = m.group(1).split()
        owners = (ROOT / "CODEOWNERS").read_text(encoding="utf-8")
        owned = {l.split()[0] for l in owners.splitlines()
                 if l.strip() and not l.startswith("#")}
        for path in surface:
            self.assertTrue({"/" + path, "/" + path + "/"} & owned,
                            "%s is pinned but has no code-owner rule" % path)
        self.assertIn("CODEOWNERS", surface)

    def test_gate_never_checks_out_or_runs_pr_code(self):
        gate = self.code(self.gate)
        self.assertIn("ref: ${{ github.sha }}", gate)
        self.assertNotRegex(gate, r"ref:\s*\$\{\{\s*github\.event\.pull_request")
        self.assertNotRegex(gate, r"ref:\s*refs/pull")
        self.assertNotIn("unittest", gate)
        self.assertNotIn("secrets.", gate)
        # PR-controlled event fields reach shell only through env, never
        # interpolated into a run: script.
        for line in gate.splitlines():
            if "github.event.pull_request" in line:
                self.assertRegex(line, r"^\s+PR_[A-Z]+: \$\{\{ github\.event\."
                                       r"pull_request\.(number|head\.sha) \}\}$")

    def test_gate_token_is_read_only_and_checkout_pinned(self):
        for text in (self.gate, self.tests):
            code = self.code(text)
            self.assertRegex(code, r"(?m)^permissions:\n  contents: read$")
            self.assertIn("persist-credentials: false", code)
            for uses in re.findall(r"uses: (\S+)", code):
                self.assertRegex(uses, r"@[0-9a-f]{40}$")

    def test_no_workflow_prints_file_names(self):
        # The old pin step echoed `git diff --name-only` verbatim.
        for text in (self.gate, self.tests):
            code = self.code(text)
            self.assertNotIn("--name-only", code)
            self.assertNotIn("$changed", code)

    def test_tests_workflow_runs_the_suite(self):
        self.assertIn("python3 -m unittest discover -s tests", self.tests)


if __name__ == "__main__":
    unittest.main()
