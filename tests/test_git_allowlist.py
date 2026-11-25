import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GIT_RULE = re.compile(r"\bBash\((git(?:\s+[^)]*)?)\)")
TRANSPORT_WILDCARD = re.compile(
    r"^git\s+(?:clone|push|pull|fetch|submodule)\b.*\s\*$", re.DOTALL)
COMMAND_OPTIONS = re.compile(r"upload-pack|receive-pack|(?:^|\s)-c")
# Remote rules may only list remotes; anything else (add, set-url, *) asks.
REMOTE_RULE = re.compile(r"^git\s+remote\b")
REMOTE_ALLOWED = ("git remote -v",)


def unsafe_git_rules(text):
    # Inspect literal rules even in prose or shell strings that print settings.
    unsafe = []
    for match in GIT_RULE.finditer(text):
        command = match.group(1).strip()
        if (TRANSPORT_WILDCARD.search(command)
                or COMMAND_OPTIONS.search(command)
                or command in ("git", "git *")
                or (REMOTE_RULE.search(command) and command not in REMOTE_ALLOWED)):
            unsafe.append(match.group(0))
    return unsafe


class TestGitAllowlist(unittest.TestCase):
    def test_tracked_allow_rules_have_no_git_transport_wildcards_or_command_options(self):
        paths = subprocess.run(
            ["git", "ls-files", "-z", "--", "*.md", "*.sh", "*.txt"],
            cwd=str(ROOT), check=True, capture_output=True).stdout.split(b"\0")
        paths = [raw.decode("utf-8", "surrogateescape") for raw in paths if raw]
        self.assertTrue(paths, "no tracked Markdown, shell or text files were checked")
        rules_checked = 0
        for path in paths:
            text = (ROOT / path).read_text(encoding="utf-8")
            rules_checked += len(GIT_RULE.findall(text))
            with self.subTest(path=path):
                self.assertEqual(unsafe_git_rules(text), [],
                                 "unsafe git permission in %s" % path)
        self.assertGreater(rules_checked, 0, "no git permission rules were checked")

    def test_rejects_transport_wildcards_command_options_and_broad_remote(self):
        commands = ["git %s *" % command
                    for command in ("clone", "push", "pull", "fetch", "submodule")]
        commands += [
            "git *",
            "git push origin main *",
            "git submodule update *",
            "git clone --upload-pack=helper https://example.com/repo.git",
            "git push --receive-pack helper origin main",
            "git pull --upload-pack helper",
            "git -c core.sshCommand=helper pull",
            "git -ccore.sshCommand=helper fetch",
            "git push -c helper",
            "git remote *",
            "git remote add *",
            "git remote set-url origin *",
        ]
        for command in commands:
            rule = "Bash(%s)" % command
            with self.subTest(rule=rule):
                self.assertEqual(unsafe_git_rules('"%s"' % rule), [rule])

    def test_accepts_exact_option_free_rules(self):
        commands = [
            "git push", "git pull", "git push origin main", "git pull origin main",
            "git clone https://example.com/repo.git", "git fetch origin",
            "git submodule update", "git remote -v", "git status *", "git commit *",
        ]
        for command in commands:
            with self.subTest(command=command):
                self.assertEqual(unsafe_git_rules('"Bash(%s)"' % command), [])


if __name__ == "__main__":
    unittest.main()
