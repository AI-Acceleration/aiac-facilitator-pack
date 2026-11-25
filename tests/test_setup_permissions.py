"""Permissions contract for the setup prompts (EN + ES).

Setup never grants blanket or lasting approvals, and the settings block is
merged into an existing ~/.claude/settings.json, never written over it.
"""
import json
import re
import subprocess
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
# The one allow list every settings block must carry, in this order.
EXPECTED_ALLOW = [
    "Bash(git status)",
    "Bash(git status --short)",
    "Bash(git diff)",
    "Bash(git log --oneline)",
    "Bash(git remote -v)",
    "Bash(ls *)",
    "Bash(mkdir *)",
    "Bash(wc *)",
    "Glob",
    "Grep",
]
# Literal rules that must never appear anywhere in the tracked Markdown.
FORBIDDEN_LITERALS = (
    "Bash(%s *)" % "git",
    "Bash(%s *)" % "cat",
    "Bash(%s *)" % "head",
    "Bash(git remote *)",
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
                    self.assertIsInstance(perms["deny"], list)

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


if __name__ == "__main__":
    unittest.main()
