import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GIT_RULE = re.compile(r"\bBash\((git(?:\s+[^)]*)?)\)")
# Options that write files, run programs, plant hooks or reroute transport.
DANGEROUS_OPTIONS = re.compile(
    r"upload-pack|receive-pack|--output|--ext-diff|--template|--separate-git-dir"
    r"|--exec-path|--exec\b|--config-env|(?:^|\s)-c")
# Remote rules may only list remotes; anything else (add, set-url) asks.
REMOTE_RULE = re.compile(r"^git\s+remote\b")
REMOTE_ALLOWED = ("git remote -v",)


def unsafe_git_rules(text):
    """Literal git permission rules that pre-approve more than one exact command.

    Any wildcard is unsafe: almost every git subcommand accepts options that
    write files (--output), run programs (--ext-diff, -c) or plant hooks
    (--template, --separate-git-dir), and a trailing * approves them silently.
    Rules are inspected even in prose or in shell strings that print settings.
    """
    unsafe = []
    for match in GIT_RULE.finditer(text):
        command = match.group(1).strip()
        if ("*" in command
                or command == "git"
                or DANGEROUS_OPTIONS.search(command)
                or (REMOTE_RULE.search(command) and command not in REMOTE_ALLOWED)):
            unsafe.append(match.group(0))
    return unsafe


class TestGitAllowlist(unittest.TestCase):
    def test_tracked_files_have_only_exact_option_safe_git_rules(self):
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

    def test_rejects_wildcards_dangerous_options_and_broad_remote(self):
        commands = ["git %s *" % sub for sub in (
            "clone", "push", "pull", "fetch", "submodule", "status", "diff", "log",
            "show", "add", "commit", "init", "config", "branch", "checkout")]
        commands += [
            "git *",
            "git push origin main *",
            "git diff --output=notes.txt",
            "git log --output ../x",
            "git diff --ext-diff",
            "git commit --template=msg.txt",
            "git init --template=hooks",
            "git init --separate-git-dir ../elsewhere",
            "git --exec-path=/tmp status",
            "git clone --upload-pack=helper https://example.com/repo.git",
            "git push --receive-pack helper origin main",
            "git -c core.sshCommand=helper pull",
            "git -ccore.sshCommand=helper fetch",
            "git remote add origin https://example.com/repo.git",
            "git remote set-url origin https://example.com/repo.git",
        ]
        for command in commands:
            rule = "Bash(%s)" % command
            with self.subTest(rule=rule):
                self.assertEqual(unsafe_git_rules('"%s"' % rule), [rule])

    def test_accepts_exact_option_safe_rules(self):
        commands = [
            "git status", "git status --short", "git diff", "git log --oneline",
            "git remote -v", "git push", "git pull origin main",
        ]
        for command in commands:
            with self.subTest(command=command):
                self.assertEqual(unsafe_git_rules('"Bash(%s)"' % command), [])


if __name__ == "__main__":
    unittest.main()
