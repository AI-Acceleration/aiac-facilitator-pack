import json
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
# The setup docs' "ask" rules. A wildcard in an ask rule only adds prompts, so
# these exact literals are exempt from the text scan; the JSON check below makes
# sure none of them ever lands in an allow list.
ASK_RULES = ("Bash(git show *)", "Bash(git -C *)", "Bash(git -c *)",
             "Bash(git add *)", "Bash(git commit *)", "Bash(git push *)")
JSON_BLOCK = re.compile(r"^```json\n(.*?)\n```$", re.DOTALL | re.MULTILINE)


def tracked(*patterns):
    out = subprocess.run(["git", "ls-files", "-z", "--"] + list(patterns),
                         cwd=str(ROOT), check=True, capture_output=True).stdout.split(b"\0")
    return [raw.decode("utf-8", "surrogateescape") for raw in out if raw]


def allow_rules(text):
    """Every allow entry of every parseable JSON block in a document."""
    rules = []
    for raw in JSON_BLOCK.findall(text):
        try:
            data = json.loads(raw)
        except ValueError:
            continue
        stack = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                if isinstance(node.get("allow"), list):
                    rules.extend(r for r in node["allow"] if isinstance(r, str))
                stack.extend(node.values())
            elif isinstance(node, list):
                stack.extend(node)
    return rules


def unsafe_git_rules(text, exempt=()):
    """Literal git permission rules that pre-approve more than one exact command.

    Any wildcard is unsafe: almost every git subcommand accepts options that
    write files (--output), run programs (--ext-diff, -c) or plant hooks
    (--template, --separate-git-dir), and a trailing * approves them silently.
    Rules are inspected even in prose or in shell strings that print settings.
    """
    unsafe = []
    for match in GIT_RULE.finditer(text):
        if match.group(0) in exempt:
            continue
        command = match.group(1).strip()
        if ("*" in command
                or command == "git"
                or DANGEROUS_OPTIONS.search(command)
                or (REMOTE_RULE.search(command) and command not in REMOTE_ALLOWED)):
            unsafe.append(match.group(0))
    return unsafe


class TestGitAllowlist(unittest.TestCase):
    def test_tracked_files_have_only_exact_option_safe_git_rules(self):
        paths = tracked("*.md", "*.sh", "*.txt")
        self.assertTrue(paths, "no tracked Markdown, shell or text files were checked")
        rules_checked = 0
        for path in paths:
            text = (ROOT / path).read_text(encoding="utf-8")
            rules_checked += len(GIT_RULE.findall(text))
            with self.subTest(path=path):
                self.assertEqual(unsafe_git_rules(text, exempt=ASK_RULES), [],
                                 "unsafe git permission in %s" % path)
        self.assertGreater(rules_checked, 0, "no git permission rules were checked")

    def test_allow_lists_never_hold_a_git_wildcard_or_ask_rule(self):
        checked = 0
        for path in tracked("*.md"):
            text = (ROOT / path).read_text(encoding="utf-8")
            for rule in allow_rules(text):
                checked += 1
                with self.subTest(path=path, rule=rule):
                    self.assertNotIn(rule, ASK_RULES)
                    self.assertEqual(unsafe_git_rules('"%s"' % rule), [])
        self.assertGreater(checked, 0, "no allow lists were checked")

    def test_ask_exemption_is_exact(self):
        for rule in ASK_RULES:
            with self.subTest(rule=rule):
                self.assertEqual(unsafe_git_rules('"%s"' % rule, exempt=ASK_RULES), [])
                self.assertEqual(unsafe_git_rules('"%s"' % rule), [rule])
        self.assertEqual(unsafe_git_rules('"Bash(git push --force *)"', exempt=ASK_RULES),
                         ["Bash(git push --force *)"])

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
