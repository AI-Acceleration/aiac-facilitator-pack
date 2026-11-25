"""Permissions contract for the setup prompts (EN + ES).

Setup never grants blanket or lasting approvals, and the settings block is
merged into an existing ~/.claude/settings.json, never written over it.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDITIONS = ("EN", "ES")
# Docs that carry the ~/.claude/settings.json permissions block.
SETTINGS_DOCS = (
    "02 — Main Setup Prompt (Participant).md",
    "02W — Main Setup Prompt (Windows).md",
    "02-S — Sandbox Setup (Participant, opt-in).md",
)
SETUP_DOCS = SETTINGS_DOCS + (
    "03 — Skills & Config Setup Prompt (Participant).md",
    "03W — Skills & Config Setup Prompt (Windows).md",
)
# The one allow list every settings block must carry, in this order: read-only
# commands only, no lasting write grant (no mkdir) and no bare tool names.
EXPECTED_ALLOW = [
    "Bash(git status)",
    "Bash(git status --short)",
    "Bash(git diff)",
    "Bash(git log --oneline)",
    "Bash(git remote -v)",
    "Bash(ls *)",
    "Bash(wc *)",
]
# Claude Code runs built-in read-only commands (cat, head, tail, grep...) without
# a prompt unless an ask or deny rule covers them, and an ask rule wins over any
# allow rule. These are the confirmations the docs promise.
EXPECTED_ASK = [
    "Bash(cat *)",
    "Bash(head *)",
    "Bash(tail *)",
    "Bash(grep *)",
    "Bash(git add *)",
    "Bash(git commit *)",
    "Bash(git push *)",
    "Bash(gh repo create *)",
]
# Doc 02-S Part 3b: the complete credential deny list, anchored at home.
CANONICAL_DENY = [
    "Read(~/.ssh/**)",
    "Read(~/.aws/**)",
    "Read(~/.gnupg/**)",
    "Read(~/.config/gh/**)",
    "Read(~/Library/Keychains/**)",
    "Read(~/**/.env)",
    "Read(~/**/*.pem)",
    "Read(~/**/*.key)",
]
# Rules that must never sit in an allow list.
NEVER_ALLOWED = set(EXPECTED_ASK) | {
    "Bash", "Bash(*)", "Read", "Write", "Edit", "Glob", "Grep", "Bash(mkdir *)"}
# Literal rules that must never appear anywhere in the tracked Markdown.
FORBIDDEN_LITERALS = (
    "Bash(%s *)" % "git",
    "Bash(git remote *)",
    "Bash(%s *)" % "mkdir",
    "Bash(%s *)" % "gws",
    "Bash(~/bin/%s *)" % "gws",
)
# Interpreter / package-manager rules (python, py, python3, node, ...).
INTERPRETER_RULE = re.compile(
    r"Bash\((?:python3?|py|node|npx|deno|bun|ruby|perl|pip3?|uv)(?:\s|\))")
JSON_BLOCK = re.compile(r"^```json\n(.*?)\n```$", re.DOTALL | re.MULTILINE)
MERGE_WORDS = re.compile(r"\b(merge|merged|fusiona|fusionar|fusiónalo|fusionado)\b",
                         re.IGNORECASE)
OVERWRITE_PHRASES = ("this step overwrites them", "este paso los sobrescribe")


def kit_doc(edition, name):
    return ROOT / ("Co-Facilitator Kit (%s)" % edition) / name


def tracked_markdown():
    out = subprocess.run(["git", "ls-files", "-z", "--", "*.md"], cwd=str(ROOT),
                         check=True, capture_output=True).stdout.split(b"\0")
    return [raw.decode("utf-8", "surrogateescape") for raw in out if raw]


def settings_blocks(text):
    """Parsed JSON blocks that carry a permissions object."""
    blocks = []
    for raw in JSON_BLOCK.findall(text):
        if '"permissions"' not in raw:
            continue
        blocks.append(json.loads(raw))
    return blocks


PYTHON_BLOCK = re.compile(r"^```python\n(.*?)^```$", re.DOTALL | re.MULTILINE)
DENY_HEADING = "#### Canonical deny list"
SANDBOX_DOC = "02-S — Sandbox Setup (Participant, opt-in).md"
MAIN_DOCS = ("02 — Main Setup Prompt (Participant).md",
             "02W — Main Setup Prompt (Windows).md")
SKILLS_DOCS = ("03 — Skills & Config Setup Prompt (Participant).md",
               "03W — Skills & Config Setup Prompt (Windows).md")


def merge_script(text):
    """The aiac-merge-settings.py block a doc tells the reader to save."""
    found = [b for b in PYTHON_BLOCK.findall(text) if "aiac-merge-settings.py" in b]
    return found


def all_json_allow_rules(text):
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


def canonical_deny_block(text):
    at = text.index(DENY_HEADING)
    m = re.search(r"^```text\n(.*?)\n```$", text[at:], re.DOTALL | re.MULTILINE)
    return m.group(1).splitlines()


def gitignore_glob_match(pattern, path):
    """Match a ~/-anchored Claude Code path pattern ("**" spans folders)."""
    rx = ""
    i = 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            rx += "(?:.*/)?"
            i += 3
        elif pattern.startswith("**", i):
            rx += ".*"
            i += 2
        elif pattern[i] == "*":
            rx += "[^/]*"
            i += 1
        else:
            rx += re.escape(pattern[i])
            i += 1
    return re.fullmatch(rx, path) is not None


class TestSetupPermissions(unittest.TestCase):
    # Short failure messages: never echo a whole document into the log.
    def has(self, needle, text, msg=""):
        self.assertTrue(needle in text, msg or "missing: %s" % needle)

    def lacks(self, needle, text, msg=""):
        self.assertFalse(needle in text, msg or "unexpected: %s" % needle)

    def test_tracked_markdown_has_no_blanket_rules(self):
        paths = tracked_markdown()
        self.assertTrue(paths, "no tracked Markdown files were checked")
        for path in paths:
            text = (ROOT / path).read_text(encoding="utf-8")
            for literal in FORBIDDEN_LITERALS:
                with self.subTest(path=path, rule=literal):
                    self.lacks(literal, text,
                                     "blanket permission %s in %s" % (literal, path))

    def test_tracked_markdown_has_no_interpreter_allow_rules(self):
        for path in tracked_markdown():
            text = (ROOT / path).read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertEqual(INTERPRETER_RULE.findall(text), [],
                                 "interpreter permission in %s" % path)

    def test_interpreter_pattern_catches_known_forms(self):
        for rule in ("Bash(python *)", "Bash(py *)", "Bash(python3 *)",
                     "Bash(node *)", "Bash(pip install *)", "Bash(python)"):
            with self.subTest(rule=rule):
                self.assertTrue(INTERPRETER_RULE.search(rule))
        for rule in ("Bash(pwd)", "Bash(git push)", "Bash(ls *)"):
            with self.subTest(rule=rule):
                self.assertIsNone(INTERPRETER_RULE.search(rule))

    def test_settings_blocks_use_the_narrow_allow_list(self):
        for edition in EDITIONS:
            for name in SETTINGS_DOCS:
                path = kit_doc(edition, name)
                with self.subTest(doc=str(path.relative_to(ROOT))):
                    blocks = settings_blocks(path.read_text(encoding="utf-8"))
                    self.assertEqual(len(blocks), 1,
                                     "expected exactly one permissions block")
                    perms = blocks[0]["permissions"]
                    self.assertEqual(perms["allow"], EXPECTED_ALLOW)
                    self.assertEqual(perms["ask"], EXPECTED_ASK)
                    if "02-S" in name:
                        self.assertEqual(perms["deny"], CANONICAL_DENY)
                    else:
                        self.assertEqual(perms["deny"], [])

    def test_settings_are_merged_not_overwritten(self):
        for edition in EDITIONS:
            for name in SETTINGS_DOCS:
                path = kit_doc(edition, name)
                text = path.read_text(encoding="utf-8")
                with self.subTest(doc=str(path.relative_to(ROOT))):
                    for phrase in OVERWRITE_PHRASES:
                        self.lacks(phrase, text)
                    # The merge instruction sits before the permissions block.
                    block_at = text.index('"permissions"')
                    self.assertTrue(MERGE_WORDS.search(text[:block_at]),
                                    "no merge instruction before the settings block")
                    if "02-S" not in name:
                        # Doc 02/02W back the file up before merging.
                        self.has("settings.json.bak", text)

    def test_setup_docs_switch_modes_with_shift_tab_not_model(self):
        for edition in EDITIONS:
            for name in SETUP_DOCS:
                path = kit_doc(edition, name)
                with self.subTest(doc=str(path.relative_to(ROOT))):
                    self.lacks("`/model`", path.read_text(encoding="utf-8"))

    def test_starter_skills_pinned_to_the_org_release(self):
        for path in tracked_markdown():
            text = (ROOT / path).read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.lacks("wildbuffaloman/cc-starter-pack", text)
                self.lacks("cc-starter-pack/main", text)
        for edition in EDITIONS:
            for name in ("03 — Skills & Config Setup Prompt (Participant).md",
                         "03W — Skills & Config Setup Prompt (Windows).md"):
                text = kit_doc(edition, name).read_text(encoding="utf-8")
                with self.subTest(doc="%s/%s" % (edition, name)):
                    self.has("git clone --depth 1 --branch v1.0.0 "
                                  "https://github.com/AI-Acceleration/cc-starter-pack.git",
                                  text)

    def test_no_classic_token_or_cached_token_instructions(self):
        for edition in EDITIONS:
            for name in SETUP_DOCS:
                text = kit_doc(edition, name).read_text(encoding="utf-8")
                with self.subTest(doc="%s/%s" % (edition, name)):
                    self.lacks("Personal access tokens (classic)", text)
                    self.lacks("`repo` + `workflow`", text)
                    self.lacks("supabase.json", text)
                    self.lacks("workos_tokens", text)

    def test_first_push_checks_private_visibility(self):
        for edition in EDITIONS:
            for name in ("02 — Main Setup Prompt (Participant).md",
                         "02W — Main Setup Prompt (Windows).md"):
                text = kit_doc(edition, name).read_text(encoding="utf-8")
                with self.subTest(doc="%s/%s" % (edition, name)):
                    self.has("--private", text)
                    self.has('"visibility": "PRIVATE"', text)
                    self.has("git status --short", text)


    def test_no_allow_list_carries_a_promised_confirmation_or_write_grant(self):
        for path in tracked_markdown():
            text = (ROOT / path).read_text(encoding="utf-8")
            for rule in all_json_allow_rules(text):
                with self.subTest(path=path, rule=rule):
                    self.assertNotIn(rule, NEVER_ALLOWED,
                                     "%s must never be in an allow list" % rule)

    def test_sandbox_deny_list_is_canonical_anchored_and_identical(self):
        lists = {}
        for edition in EDITIONS:
            text = kit_doc(edition, SANDBOX_DOC).read_text(encoding="utf-8")
            with self.subTest(edition=edition):
                listed = canonical_deny_block(text)
                self.assertEqual(listed, CANONICAL_DENY)
                lists[edition] = listed
        self.assertEqual(lists["EN"], lists["ES"])
        for rule in CANONICAL_DENY:
            with self.subTest(rule=rule):
                # Unprefixed patterns are relative to the launch folder and miss
                # files outside the vault: every rule is home- or root-anchored.
                self.assertTrue(rule.startswith(("Read(~/", "Read(//")), rule)

    def test_sandbox_canary_is_covered_by_the_deny_rules(self):
        for edition in EDITIONS:
            text = kit_doc(edition, SANDBOX_DOC).read_text(encoding="utf-8")
            with self.subTest(edition=edition):
                self.has('mktemp -d "$HOME/aiac-canary.XXXXXX"', text)
                self.has('"$CANARY_DIR/test.key"', text)
        canary = "~/aiac-canary.Ab12Cd/test.key"
        patterns = [r[len("Read("):-1] for r in CANONICAL_DENY]
        self.assertTrue(any(gitignore_glob_match(p, canary) for p in patterns),
                        "no deny rule covers the 02-S canary key")
        self.assertFalse(any(gitignore_glob_match(p, "~/aiac-canary.Ab12Cd/secret.txt")
                             for p in patterns),
                         "the canary secret.txt must be outside the deny list (prompt test)")

    def test_merge_script_is_identical_everywhere(self):
        scripts = []
        for edition in EDITIONS:
            for name in SETTINGS_DOCS:
                text = kit_doc(edition, name).read_text(encoding="utf-8")
                with self.subTest(doc="%s/%s" % (edition, name)):
                    found = merge_script(text)
                    self.assertEqual(len(found), 1, "expected one merge script")
                    scripts.append(found[0])
        self.assertEqual(len(set(scripts)), 1, "merge script differs between docs")

    def run_merge(self, home, block, extra=()):
        script = merge_script(kit_doc("EN", SETTINGS_DOCS[0]).read_text(encoding="utf-8"))[0]
        path = Path(home) / "aiac-merge-settings.py"
        path.write_text(script, encoding="utf-8")
        env = dict(os.environ, HOME=str(home), USERPROFILE=str(home))
        return subprocess.run([sys.executable, str(path)] + list(extra) + ["-"],
                              input=json.dumps(block), capture_output=True, text=True,
                              env=env, timeout=60)

    def test_merge_script_merges_without_printing_existing_values(self):
        secret = "sk-test-SYNTHETIC-0000"
        block = settings_blocks(kit_doc("EN", SETTINGS_DOCS[0]).read_text(encoding="utf-8"))[0]
        with tempfile.TemporaryDirectory() as home:
            target = Path(home) / ".claude" / "settings.json"
            target.parent.mkdir()
            existing = {"env": {"API_KEY": secret},
                        "permissions": {"allow": ["Bash(npm test)"], "deny": ["Read(./private/**)"]},
                        "model": secret + "-model"}
            target.write_text(json.dumps(existing), encoding="utf-8")
            run = self.run_merge(home, block)
            self.assertEqual(run.returncode, 0, run.stderr[-300:])
            self.assertNotIn(secret, run.stdout + run.stderr)
            self.assertTrue(run.stdout.strip().splitlines()[-1].startswith("Verified:"))
            merged = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(merged["env"]["API_KEY"], secret)
            self.assertEqual(merged["model"], secret + "-model")
            self.assertIn("Bash(npm test)", merged["permissions"]["allow"])
            self.assertIn("Read(./private/**)", merged["permissions"]["deny"])
            for rule in EXPECTED_ALLOW:
                self.assertIn(rule, merged["permissions"]["allow"])
            self.assertEqual(merged["permissions"]["ask"], EXPECTED_ASK)
            # A second run adds nothing and still verifies.
            again = self.run_merge(home, block)
            self.assertEqual(again.returncode, 0, again.stderr[-300:])
            self.assertIn("(0 added)", again.stdout)

    def test_merge_script_refuses_invalid_json_and_keeps_differing_values_hidden(self):
        secret = "sk-test-SYNTHETIC-1111"
        with tempfile.TemporaryDirectory() as home:
            target = Path(home) / ".claude" / "settings.json"
            target.parent.mkdir()
            target.write_text('{"env": {"TOKEN": "%s"' % secret, encoding="utf-8")
            run = self.run_merge(home, {"env": {"CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "75"}})
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("STOP:", run.stderr)
            self.assertNotIn(secret, run.stdout + run.stderr)
            self.assertIn(secret, target.read_text(encoding="utf-8"))  # untouched
            target.write_text(json.dumps({"statusLine": {"command": secret}}), encoding="utf-8")
            run = self.run_merge(home, {"statusLine": {"type": "command", "command": "x.sh"}})
            self.assertEqual(run.returncode, 0, run.stderr[-300:])
            self.assertIn("kept your existing value (not shown): statusLine", run.stdout)
            self.assertNotIn(secret, run.stdout + run.stderr)

    def test_setup_never_displays_existing_settings(self):
        reading = re.compile(r"read it first|léelo primero|read the file\s+back|"
                             r"lee el archivo de vuelta|jq \. ~/\.claude/settings\.json(?! >)|"
                             r"cat ~/\.claude/settings\.json")
        for edition in EDITIONS:
            for name in SETUP_DOCS:
                text = kit_doc(edition, name).read_text(encoding="utf-8")
                with self.subTest(doc="%s/%s" % (edition, name)):
                    self.assertEqual(reading.findall(text), [])
            for name in MAIN_DOCS:
                text = kit_doc(edition, name).read_text(encoding="utf-8")
                with self.subTest(doc="%s/%s" % (edition, name)):
                    self.has({"EN": "do not open, read or print",
                              "ES": "no abras, no leas ni"}[edition], text)

    def test_first_push_checks_the_effective_destination(self):
        for edition in EDITIONS:
            for name in MAIN_DOCS:
                text = kit_doc(edition, name).read_text(encoding="utf-8")
                with self.subTest(doc="%s/%s" % (edition, name)):
                    # Fresh repo folder only.
                    self.has("if [ -e ~/dev/<repo-name> ]; then", text)
                    self.lacks("mkdir -p ~/dev/<repo-name>", text)
                    # Unstaging before the first commit works without HEAD.
                    self.has("git rm --cached -- <file>", text)
                    self.lacks("git restore --staged <file>", text)
                    # Effective push URL and the outgoing history, before the push.
                    step12 = text[text.index("git commit -m"):]
                    push_at = step12.index("git push -u origin main")
                    self.has("git remote get-url --push --all origin", step12[:push_at])
                    self.has("git log --oneline", step12[:push_at])
                    self.has('"visibility": "PRIVATE"', step12[:push_at])
                    # Server-side confirmation afterwards.
                    self.has("git ls-remote origin refs/heads/main", step12[push_at:])

    def test_starter_pack_installer_runs_only_after_clone_or_verification(self):
        for edition in EDITIONS:
            for name in SKILLS_DOCS:
                text = kit_doc(edition, name).read_text(encoding="utf-8")
                with self.subTest(doc="%s/%s" % (edition, name)):
                    self.has("cc-starter-pack.git ~/.aiac/cc-starter-pack \\\n"
                             "    && (cd ~/.aiac/cc-starter-pack && bash ./install.sh)", text)
                    # No installer line on its own, where a failed clone could reach it.
                    self.assertIsNone(re.search(r"^\(cd ~/\.aiac/cc-starter-pack && bash \./install\.sh\)$",
                                                text, re.MULTILINE))
                    self.has("refs/tags/v1.0.0^{}", text)
                    self.has("git status --porcelain --untracked-files=all", text)


if __name__ == "__main__":
    unittest.main()
