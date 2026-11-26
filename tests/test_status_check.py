"""Tests for tools/aiac-status-check.sh (all four shipped copies).

The status check runs on participants' machines and its last block is shared
with a facilitator, so these tests pin three properties:

* privacy: synthetic identities, paths, tokens and setting values never
  appear in the default output, and the safe-to-share block holds nothing
  but fixed check names and statuses;
* honesty: each verdict is computed from the checks it summarises, optional
  checks never count against the participant, and the opt-in sandbox lines
  appear only when asked for or detected;
* safety: the script writes nothing.

Every run uses a synthetic HOME in a temporary directory and a minimal
environment, so nothing on the machine running the tests leaks in.
"""
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = [ROOT / ("Co-Facilitator Kit (%s)" % edition) / "tools" / name
           for edition in ("EN", "ES")
           for name in ("aiac-status-check.sh", "aiac-status-check.sh.txt")]
BASH = "/bin/bash" if os.path.exists("/bin/bash") else shutil.which("bash")
JQ = shutil.which("jq", path=os.defpath)
# Synthetic, assembled at runtime so no scanner mistakes it for a real key.
FAKE_KEY = "sk" + "-" + "SYNTHETIC-KEY-0000"
SAFE_START = "----- AIAC STATUS (safe to share) -----"
SAFE_END = "----- END -----"

# Every check name the safe block may carry. A new check must be added here
# on purpose, after confirming its label is a fixed string.
CHECK_NAMES = {
    "Doc 01 - Git installed",
    "Doc 01 - GitHub CLI (gh) installed",
    "Doc 01 - GitHub CLI credentials present",
    "Doc 01 - Claude Code installed",
    "Doc 01 - jq installed",
    "Doc 01 - Python 3 installed",
    "Doc 01 - Obsidian installed",
    "Doc 01 - Ghostty terminal",
    "Doc 01 - Granola or other transcription tool",
    "Pre-flight - vault folder exists",
    "Pre-flight - vault not in a cloud-synced folder",
    "Pre-flight - Obsidian config found in this folder",
    "Doc 02-S - hardened global settings (Part 3b)",
    "Doc 02-S - sandbox config in the vault (Part 3a)",
    "Doc 02 - global settings file is valid",
    "Doc 02 - no blanket approvals in settings",
    "Doc 02 - ask-first rules in settings",
    "Doc 02 - global router points at the vault",
    "Doc 02 - context monitoring (auto-compact 75 + statusline)",
    "Doc 02 - vault folders",
    "Doc 02 - vault CLAUDE.md",
    "Doc 02 - Obsidian settings (Files and links)",
    "Doc 02 - AIAC Journey brief",
    "Doc 02 - AIAC cheat sheet",
    "Doc 02 - git identity set",
    "Doc 02 - code repo in ~/dev (named in router)",
    "Doc 02 - repo CLAUDE.md",
    "Doc 02 - repo has a first commit",
    "Doc 02 - repo origin points at GitHub",
    "Doc 03 - starter skills (all 6)",
    "Doc 03 - plugins (compound-engineering, superpowers, playground)",
    "Doc 03 - lessons.md",
}
OPTIONAL = {"Doc 01 - Ghostty terminal",
            "Doc 01 - Granola or other transcription tool"}
SANDBOX_NAMES = {"Doc 02-S - hardened global settings (Part 3b)",
                 "Doc 02-S - sandbox config in the vault (Part 3a)"}
STATUSES = ("DONE", "NOT DONE", "SKIPPED (optional)")

# The settings blocks Docs 02 / 02W / 02-S write (STEP 3 and Part 3b).
DOC02_ALLOW = ["Bash(git status)", "Bash(git status --short)", "Bash(git diff)",
               "Bash(git log --oneline)", "Bash(git remote -v)",
               "Bash(ls *)", "Bash(wc *)"]
DOC02_ASK = ["Bash(cat *)", "Bash(head *)", "Bash(tail *)", "Bash(grep *)",
             "Bash(diff *)", "Bash(sed *)", "Bash(sort *)", "Bash(git show *)",
             "Bash(git -C *)", "Bash(git -c *)",
             "Bash(git add *)", "Bash(git commit *)", "Bash(git push *)",
             "Bash(gh repo create *)"]
# 02-S Part 3b canonical deny list, spelled exactly as the doc writes it.
DOC02S_DENY = ["Read(~/.ssh/**)", "Read(~/.aws/**)", "Read(~/.gnupg/**)",
               "Read(~/.config/gh/**)", "Read(~/Library/Keychains/**)",
               "Read(~/.claude/.credentials.json)", "Read(~/**/.env)", "Read(~/**/*.pem)", "Read(~/**/*.key)"]
FIXED_LINES = re.compile(
    r"^(Status check: v\d+(\.\d+)*"
    r"|OS: (macOS|Windows|Windows \(WSL\)|Linux|unsupported)"
    r"|BEFORE THE SESSION:|BUILT IN THE SESSION:"
    r"|VERDICT: (PRE-SESSION - homework complete, ready for the session"
    r"|PRE-SESSION - homework not complete \(\d+ item\(s\) NOT DONE\)"
    r"|PHASE 0 SETUP COMPLETE - all \d+ required checks DONE"
    r"|IN PROGRESS - \d+ of \d+ required checks NOT DONE"
    r"|UNSUPPORTED OPERATING SYSTEM - check by hand with your facilitator))$")

VAULT_FOLDERS = ["00 HUB/00 INBOX", "00 HUB/00 READ_REVIEW", "01 PROJECTS",
                 "02 AREAS/Learning", "03 REFERENCE", "04 ARCHIVES",
                 "05 AI/CLAUDE CODE/workspace", "05 AI/CLAUDE CODE/resources",
                 "Templates"]
SKILLS = ["project-create", "inbox-clear", "retro", "session-close",
          "skill-create", "meeting-minutes"]


def at(local, domain):
    # Built at runtime so this file carries no address literal for the gate.
    return local + "@" + domain


def write(path, text, mode=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    if mode is not None:
        path.chmod(mode)
    return path


def safe_block(output):
    lines = output.splitlines()
    start = lines.index(SAFE_START)
    end = lines.index(SAFE_END, start)
    return lines[start + 1:end]


def statuses(output):
    result = {}
    for entry in safe_block(output):
        name, sep, status = entry.rpartition(": ")
        if sep and name in CHECK_NAMES:
            result[name] = status
    return result


def verdict(output):
    return next(line for line in safe_block(output) if line.startswith("VERDICT: "))


class StatusCheckCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="statuscheck-")
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.home = self.base / "home" / "zebulon.quixote"
        self.home.mkdir(parents=True)
        self.bin = self.base / "fakebin"
        self.bin.mkdir()
        self.tmpdir = self.base / "tmpdir"
        self.tmpdir.mkdir()
        self.env = {
            "HOME": str(self.home),
            "PATH": str(self.bin) + os.pathsep + os.defpath,
            "TMPDIR": str(self.tmpdir),
            "LANG": "C",
            "LC_ALL": "C",
            "GIT_CONFIG_NOSYSTEM": "1",
            "AIAC_STATUS_OBSIDIAN_APP": str(self.base / "no-obsidian.app"),
            # No managed policy from the machine running the tests.
            "AIAC_STATUS_MANAGED_DIR": str(self.base / "no-managed-policy"),
        }

    # -- fixture builders ------------------------------------------------
    def stub(self, name, body):
        write(self.bin / name, "#!/bin/sh\n" + body + "\n", 0o755)

    def install_tools(self):
        self.stub("claude", 'echo "9.9.9 (Claude Code)"')
        self.stub("gh", 'echo "gh version 9.9.9"')
        self.stub("python3", 'echo "Python 3.12.0"')
        self.stub("obsidian", "exit 0")
        app = self.base / "Obsidian.app"
        app.mkdir(exist_ok=True)
        self.env["AIAC_STATUS_OBSIDIAN_APP"] = str(app)
        write(self.home / ".config" / "gh" / "hosts.yml",
              "github.com:\n    user: zeb-secret-login\n    git_protocol: https\n")

    def git(self, cwd, *args):
        subprocess.run(["git", *args], cwd=str(cwd), env=self.env,
                       check=True, capture_output=True)

    def make_vault(self, path, full=False):
        (path / ".obsidian").mkdir(parents=True, exist_ok=True)
        (path / "00 HUB" / "00 INBOX").mkdir(parents=True, exist_ok=True)
        if full:
            for folder in VAULT_FOLDERS:
                (path / folder).mkdir(parents=True, exist_ok=True)
            write(path / "CLAUDE.md", "# CLAUDE.md - My Vault\n")
            write(path / ".obsidian" / "app.json", json.dumps({
                "newFileLocation": "folder",
                "newFileFolderPath": "00 HUB/00 INBOX",
                "useMarkdownLinks": False,
                "showUnsupportedFiles": True,
                "alwaysUpdateLinks": True,
            }))
            write(path / "01 PROJECTS" / "AIAC Journey" / "AI Acceleration Club - Zeb Journey.md", "# J\n")
            write(path / "00 HUB" / "00 INBOX" / "AIAC Cheat Sheet.md", "# C\n")
            write(path / "05 AI" / "CLAUDE CODE" / "resources" / "lessons.md", "# L\n")
        return path

    def write_router(self, vault, repo_name=None):
        text = ("# CLAUDE.md - Global Router\n\n## Default Workspace\n\n"
                "All Claude Code sessions must load and follow the instructions in:\n\n"
                "**`%s/CLAUDE.md`**\n" % vault)
        if repo_name:
            text += "\n## My Code Repos\n\n- Zeta: ~/dev/%s\n" % repo_name
        write(self.home / ".claude" / "CLAUDE.md", text)

    def make_repo(self, name, origin=None, commit=False, claude_md=False):
        repo = self.home / "dev" / name
        repo.mkdir(parents=True)
        self.git(repo, "init", "-q")
        if claude_md:
            write(repo / "CLAUDE.md", "# CLAUDE.md - Zeta\n")
        if commit:
            self.git(repo, "add", "-A")
            self.git(repo, "commit", "-q", "--allow-empty", "-m", "first")
        if origin:
            self.git(repo, "remote", "add", "origin", origin)
        return repo

    def set_identity(self, name="Zebulon Quixote",
                     email=at("zq-private", "contoso-secret.test")):
        self.git(self.home, "config", "--global", "user.name", name)
        self.git(self.home, "config", "--global", "user.email", email)

    def write_settings(self, **extra):
        settings = {
            "permissions": {"allow": list(DOC02_ALLOW),
                            "ask": list(DOC02_ASK),
                            "deny": []},
            "env": {"CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "75",
                    "ANTHROPIC_API_KEY": FAKE_KEY},
            "statusLine": {"type": "command", "command": "~/.claude/statusline.sh",
                           "padding": 2},
            "hooks": {
                "UserPromptSubmit": [{"hooks": [{"type": "command", "command": "true"}]}],
                "PreCompact": [{"matcher": "auto",
                                "hooks": [{"type": "command", "command": "true"}]}],
            },
        }
        settings.update(extra)
        write(self.home / ".claude" / "settings.json", json.dumps(settings))
        write(self.home / ".claude" / "statusline.sh", "#!/bin/bash\necho ok\n", 0o755)
        return settings

    def install_skills_and_plugins(self, settings):
        for skill in SKILLS:
            write(self.home / ".claude" / "skills" / skill / "SKILL.md", "---\nname: x\n---\n")
        plugins = {}
        enabled = {}
        for plugin, market in (("compound-engineering", "compound-engineering-plugin"),
                               ("superpowers", "claude-plugins-official"),
                               ("playground", "claude-plugins-official")):
            key = plugin + "@" + market
            install = self.home / ".claude" / "plugins" / "cache" / plugin
            install.mkdir(parents=True)
            plugins[key] = [{"installPath": str(install), "version": "1.0.0"}]
            enabled[key] = True
        write(self.home / ".claude" / "plugins" / "installed_plugins.json",
              json.dumps({"version": 2, "plugins": plugins}))
        settings["enabledPlugins"] = enabled
        write(self.home / ".claude" / "settings.json", json.dumps(settings))

    def complete_setup(self, vault=None):
        self.install_tools()
        vault = self.make_vault(vault or (self.home / "AIAC-Vault"), full=True)
        self.set_identity()
        self.make_repo("client-zeta-secret", commit=True, claude_md=True,
                       origin="https://github.com/zeb-secret-login/client-zeta-secret.git")
        self.write_router(vault, "client-zeta-secret")
        settings = self.write_settings()
        self.install_skills_and_plugins(settings)
        return vault

    # -- running ---------------------------------------------------------
    def run_script(self, *args, script=None):
        r = subprocess.run([BASH, str(script or SCRIPTS[0]), *args],
                           cwd=str(self.base), env=self.env,
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r.stdout + r.stderr

    def assert_safe_block_shape(self, output):
        block = safe_block(output)
        self.assertTrue(block, "safe block is empty")
        for entry in block:
            if FIXED_LINES.match(entry):
                continue
            name, sep, status = entry.rpartition(": ")
            self.assertTrue(sep, "unexpected line in safe block: %r" % entry)
            self.assertIn(name, CHECK_NAMES, "unexpected check in safe block: %r" % entry)
            self.assertIn(status, STATUSES, "unexpected status: %r" % entry)
        self.assertEqual(sum(1 for e in block if e.startswith("VERDICT: ")), 1)
        self.assertEqual(sum(1 for e in block if e.startswith("OS: ")), 1)


class TestDocsUseShare(unittest.TestCase):
    def test_every_prompt_that_has_claude_run_the_check_uses_share(self):
        # Whatever Claude runs lands in its context: only the safe block may.
        prompt = re.compile(r"^```\n((?:Run|Corre) `bash [^`\n]*aiac-status-check[^`\n]*`[^\n]*)\n```$",
                            re.MULTILINE)
        for edition in ("EN", "ES"):
            path = ROOT / ("Co-Facilitator Kit (%s)" % edition) / \
                "01 — Pre-Session Setup Instructions (Participant).md"
            found = prompt.findall(path.read_text(encoding="utf-8"))
            with self.subTest(edition=edition):
                self.assertTrue(found)
                for line in found:
                    self.assertIn(".sh.txt --share`", line)


class TestShippedCopies(unittest.TestCase):
    def test_all_four_copies_are_byte_identical(self):
        first = SCRIPTS[0].read_bytes()
        for script in SCRIPTS[1:]:
            with self.subTest(script=str(script.relative_to(ROOT))):
                self.assertEqual(script.read_bytes(), first)

    def test_copies_are_ascii_only(self):
        for script in SCRIPTS:
            with self.subTest(script=str(script.relative_to(ROOT))):
                script.read_bytes().decode("ascii")

    @unittest.skipUnless(BASH, "bash not available")
    def test_copies_parse_with_system_bash(self):
        for script in SCRIPTS:
            with self.subTest(script=str(script.relative_to(ROOT))):
                r = subprocess.run([BASH, "-n", str(script)],
                                   capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, r.stderr)

    def test_no_heredocs_so_bash_writes_no_temp_files(self):
        # bash 3.2 backs here-documents and here-strings with temp files.
        text = SCRIPTS[0].read_text()
        code = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("#"))
        self.assertNotRegex(code, r"<<")


@unittest.skipUnless(BASH and shutil.which("git"), "bash and git required")
class TestPrivacy(StatusCheckCase):
    def synthetic_machine(self):
        token = "ghp_SYNTH" + "ETICTOKEN0123456789"
        vault = self.make_vault(self.home / "OneDrive - Contoso Secretco" / "Zeb Private Vault",
                                full=True)
        self.set_identity()
        self.make_repo("client-zeta-secret", commit=True, claude_md=True,
                       origin="https://zeb-secret-login:%s" % token + "@" +
                       "github.com/contoso-secretco/zeta-private.git")
        self.write_router(vault, "client-zeta-secret")
        settings = self.write_settings()
        settings["permissions"]["allow"].append("Bash(python3 /srv/acme-hidden/run.py)")
        write(self.home / ".claude" / "settings.json", json.dumps(settings))
        write(vault / ".claude" / "settings.json", json.dumps({"sandbox": {
            "enabled": True,
            "filesystem": {"allowRead": ["~/.claude/**", "/srv/acme-hidden/**"]}}}))
        self.install_tools()
        secrets = [token, "SYNTHETICTOKEN", "Zebulon", "Quixote", "zebulon.quixote",
                   "zq-private", "contoso-secret", "Contoso", "Secretco",
                   "Zeb Private Vault", "client-zeta-secret", "zeta-private",
                   "zeb-secret-login", "SYNTHETIC-KEY", "acme-hidden",
                   str(self.home), str(self.base),
                   os.path.realpath(str(self.base))]
        return secrets

    def test_synthetic_identity_paths_and_token_never_in_default_output(self):
        secrets = self.synthetic_machine()
        for script in SCRIPTS:
            with self.subTest(script=str(script.relative_to(ROOT))):
                output = self.run_script(script=script)
                for secret in secrets:
                    self.assertNotIn(secret, output)
                self.assert_safe_block_shape(output)

    def test_details_still_never_print_token_name_or_settings_values(self):
        secrets = self.synthetic_machine()
        output = self.run_script("--details")
        self.assertIn("do NOT share", output)
        for secret in ("ETICTOKEN", "Zebulon", "Quixote", "zq-private",
                       "zeb-secret-login", "SYNTHETIC-KEY", "acme-hidden", str(self.home)):
            self.assertNotIn(secret, output)
        # --details is the place for ~-relative paths, never absolute ones.
        self.assertIn("~/OneDrive - Contoso Secretco/Zeb Private Vault", output)

    def test_safe_block_holds_only_fixed_names_and_statuses(self):
        self.synthetic_machine()
        for args in ((), ("--sandbox",), ("--details",)):
            with self.subTest(args=args):
                self.assert_safe_block_shape(self.run_script(*args))

    def test_gh_account_name_is_never_printed(self):
        self.install_tools()
        output = self.run_script("--details")
        self.assertEqual(statuses(output)["Doc 01 - GitHub CLI credentials present"], "DONE")
        self.assertNotIn("zeb-secret-login", output)

    def test_broad_rules_are_counted_not_listed_by_default(self):
        self.install_tools()
        vault = self.make_vault(self.home / "AIAC-Vault", full=True)
        self.write_router(vault)
        settings = self.write_settings()
        settings["permissions"]["allow"] += ["Bash(git *)", "Bash(python3 *)",
                                             "Bash(cat *)", "Bash(git remote *)",
                                             "Bash(git diff *)", "Bash(git log:*)",
                                             "Bash(git add *)"]
        write(self.home / ".claude" / "settings.json", json.dumps(settings))
        output = self.run_script()
        self.assertEqual(statuses(output)["Doc 02 - no blanket approvals in settings"],
                         "NOT DONE")
        self.assertIn("7 broad rule(s) in 1 settings file(s)", output)
        self.assertNotIn("Bash(git *)", output)
        details = self.run_script("--details")
        # Even --details names a fixed file label and category, never the rule text.
        self.assertIn("broad rule (5): global settings.json: a git rule with a wildcard", details)
        self.assertIn("broad rule (1): global settings.json: a command rule with a wildcard", details)
        self.assertIn("broad rule (1): global settings.json: an interpreter or shell rule", details)
        self.assertNotIn("Bash(git *)", details)
        self.assertNotIn("Bash(python3 *)", details)

    def test_details_never_print_broad_rule_text(self):
        self.install_tools()
        vault = self.make_vault(self.home / "AIAC-Vault", full=True)
        self.write_router(vault)
        settings = self.write_settings()
        settings["permissions"]["allow"].append(
            "Bash(python3 /srv/acme-hidden/run.py --token %s)" % FAKE_KEY)
        write(self.home / ".claude" / "settings.json", json.dumps(settings))
        for args in ((), ("--details",)):
            output = self.run_script(*args)
            self.assertNotIn("acme-hidden", output)
            self.assertNotIn("SYNTHETIC-KEY", output)


@unittest.skipUnless(BASH and shutil.which("git"), "bash and git required")
class TestNoLeaksInDefaultOutput(StatusCheckCase):
    """Paths, tool error text, settings values and server names stay out."""

    LEAKS = ("acme-hidden", "ghp_", "SYNTH" + "ETIC", "zq-private", "contoso-private")

    def assert_no_leaks(self, output, extra=(), paths=True):
        leaks = self.LEAKS + tuple(extra)
        if paths:  # --details may show where a tool is installed, nothing more
            leaks += (str(ROOT), str(self.base), os.path.realpath(str(self.base)))
        for leak in leaks:
            self.assertNotIn(leak, output)
        self.assert_safe_block_shape(output)

    def test_missing_vault_message_never_prints_the_script_path(self):
        # Run from a folder outside HOME whose name would identify a client.
        hidden = self.base / "acme-hidden client folder"
        hidden.mkdir()
        copy = hidden / "aiac-status-check.sh.txt"
        shutil.copyfile(str(SCRIPTS[0]), str(copy))
        for script in (copy, SCRIPTS[0]):
            with self.subTest(script=script.name):
                output = self.run_script(script=script)
                self.assertEqual(statuses(output)["Pre-flight - vault folder exists"], "NOT DONE")
                self.assertIn('bash aiac-status-check.sh.txt "/path/to/your/vault"', output)
                self.assert_no_leaks(output)

    def test_help_and_unknown_option_print_fixed_text(self):
        hidden = self.base / "acme-hidden client folder"
        hidden.mkdir()
        copy = hidden / "aiac-status-check.sh"
        shutil.copyfile(str(SCRIPTS[0]), str(copy))
        r = subprocess.run([BASH, str(copy), "--help"], cwd=str(self.base), env=self.env,
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn("Usage: bash aiac-status-check.sh", r.stdout)
        self.assertNotIn("acme-hidden", r.stdout + r.stderr)
        r = subprocess.run([BASH, str(copy), "--acme-hidden-option"], cwd=str(self.base),
                           env=self.env, capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertNotIn("acme-hidden", r.stdout + r.stderr)

    def failing_tools(self):
        secret = "ghp_SYNTH" + "ETIC0000 /srv/acme-hidden " + at("zq-private", "example.test")
        self.stub("gh", 'echo "fatal: %s" >&2; exit 1' % secret)
        self.stub("claude", 'echo "9.9.9 (Claude Code) %s"; echo "%s" >&2' % (secret, secret))
        self.stub("python3", 'echo "Python 3.12.0 %s"' % secret)
        real_uname = shutil.which("uname", path=os.defpath)
        self.stub("uname", 'case "$1" in -m) echo "acme-hidden-arch" ;; '
                           '*) exec %s "$@" ;; esac' % real_uname)

    def test_failing_tool_with_secret_looking_stderr_is_not_echoed(self):
        self.failing_tools()
        for args in ((), ("--details",)):
            with self.subTest(args=args):
                output = self.run_script(*args)
                self.assert_no_leaks(output, paths=not args)
                self.assertRegex(output, r"Doc 01 - GitHub CLI \(gh\) installed +installed "
                                         r"\(version not read\)")
                # claude and gh are never run (either can write files on first run).
                self.assertRegex(output, r"Doc 01 - Claude Code installed +installed "
                                         r"\(version not read\)")
                # Extra text on the version line: Python counts, no version shown.
                self.assertRegex(output, r"Doc 01 - Python 3 installed +installed, version not "
                                         r"read \(python3\)")
                self.assertRegex(output, r"Chip / architecture +other")

    # -- round 4: version probes and --share -------------------------------
    PROBE_LEAKS = ("192.0.2.17", "probe-host.example.test", "ghp_" + "SYNTHPROBE0000")

    def test_failed_version_probe_output_is_never_shown(self):
        # A probe that fails but prints an address, a host name and a token on
        # stdout: the report says only "installed (version not read)".
        leak = " ".join(self.PROBE_LEAKS)
        self.stub("git", 'echo "git version %s"; exit 1' % leak)
        self.stub("jq", 'echo "jq-1.7.1 %s"; exit 3' % leak)
        for py in ("python3", "python", "py"):
            self.stub(py, 'echo "Python 3.12.0"; echo "%s"; exit 1' % leak)
        for args in ((), ("--details",), ("--share",)):
            with self.subTest(args=args):
                output = self.run_script(*args)
                for value in self.PROBE_LEAKS:
                    self.assertNotIn(value, output)
                if args != ("--share",):
                    self.assertRegex(output, r"Doc 01 - Git installed +installed \(version not read\)")
                    self.assertRegex(output, r"Doc 01 - jq installed +installed \(version not read\)")
                # A failed Python probe does not count as a working Python 3.
                self.assertEqual(statuses(output)["Doc 01 - Python 3 installed"], "NOT DONE")

    def test_successful_probe_shows_only_a_strict_version(self):
        self.stub("git", 'echo "git version 192.0.2.17"')  # address-shaped: refused
        self.stub("python3", 'echo "Python 3.12.0"')
        output = self.run_script()
        self.assertNotIn("192.0.2", output)
        self.assertRegex(output, r"Doc 01 - Git installed +installed \(version not read\)")
        self.assertRegex(output, r"Doc 01 - Python 3 installed +version 3\.12\.0 \(python3\)")
        self.stub("git", 'echo "git version 2.43.0.windows.1"')
        self.assertRegex(self.run_script(), r"Doc 01 - Git installed +version 2\.43\.0\n")
        self.stub("git", 'echo "git version 2.39.5 (Apple Git-154)"')
        self.assertRegex(self.run_script(), r"Doc 01 - Git installed +version 2\.39\.5\n")

    def test_share_prints_only_the_safe_block(self):
        self.failing_tools()
        full = self.run_script()
        for args in (("--share",), ("--share", "--details"), ("--details", "--share")):
            with self.subTest(args=args):
                shared = self.run_script(*args)
                lines = shared.splitlines()
                self.assertEqual(lines[0], SAFE_START)
                self.assertEqual(lines[-1], SAFE_END)
                self.assertEqual(lines[1:-1], safe_block(full))
                self.assert_no_leaks(shared)
                self.assertNotIn("--details was ON", shared)

    def test_gh_token_variable_counts_but_is_never_printed(self):
        self.env["GH_TOKEN"] = "ghp_SYNTH" + "ETICTOKENVALUE"
        output = self.run_script("--details")
        self.assertEqual(statuses(output)["Doc 01 - GitHub CLI credentials present"], "DONE")
        self.assert_no_leaks(output)

    @unittest.skipUnless(JQ, "jq required")
    def test_malformed_settings_values_are_never_printed(self):
        vault = self.make_vault(self.home / "AIAC-Vault", full=True)
        self.write_router(vault)
        sandboxes = [
            {"sandbox": {"enabled": "acme-hidden-value",
                         "failIfUnavailable": {"k": "acme-hidden-object"},
                         "allowUnsandboxedCommands": ["acme-hidden-list"],
                         "filesystem": {"denyRead": "acme-hidden-string",
                                        "allowRead": ["/srv/acme-hidden/**"],
                                        "allowWrite": {"x": "acme-hidden"}},
                         "network": {"allowedDomains": "acme-hidden.test"}}},
            {"sandbox": "acme-hidden-sandbox-string"},
            {"sandbox": {"enabled": True, "network": ["acme-hidden.test"],
                         "filesystem": "acme-hidden-fs"}},
        ]
        global_settings = [
            {"permissions": {"allow": {"x": "acme-hidden"}, "deny": "Read(acme-hidden)",
                             "ask": "acme-hidden"},
             "env": {"CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "acme-hidden"},
             "statusLine": {"type": "command", "command": "/srv/acme-hidden/s.sh"},
             "hooks": {"Stop": "acme-hidden"}},
            {"permissions": "acme-hidden-permissions", "sandbox": True},
            {"permissions": {"allow": ["Bash(acme-hidden *)", 7, None],
                             "deny": [1, {"acme-hidden": True}]}},
        ]
        for i, (vs, gs) in enumerate(zip(sandboxes, global_settings)):
            write(vault / ".claude" / "settings.json", json.dumps(vs))
            write(self.home / ".claude" / "settings.json", json.dumps(gs))
            for args in ((), ("--details",), ("--sandbox",)):
                with self.subTest(case=i, args=args):
                    output = self.run_script(*args)
                    self.assert_no_leaks(output)
                    self.assertEqual(statuses(output)[
                        "Doc 02-S - hardened global settings (Part 3b)"], "NOT DONE")
                    self.assertEqual(statuses(output)[
                        "Doc 02-S - sandbox config in the vault (Part 3a)"], "NOT DONE")
            if i == 0:
                output = self.run_script("--details")
                self.assertRegex(output, r"sandbox\.enabled +unexpected value")
                self.assertRegex(output, r"allowedDomains \(count\) +not a list")
                self.assertRegex(output, r"filesystem\.denyRead \(entries\) +not a list")
                self.assertRegex(output, r"filesystem\.allowRead \(entries\) +1")

    @unittest.skipUnless(JQ, "jq required")
    def test_synthetic_home_default_output_leaks_nothing(self):
        # Everything at once: identity, token-bearing private remote, failing
        # tool, malformed settings, a client-named vault and a broad rule.
        self.install_tools()
        self.failing_tools()
        self.env["GH_TOKEN"] = "ghp_SYNTH" + "ETICTOKENVALUE"
        vault = self.make_vault(self.home / "Zeb acme-hidden Vault", full=True)
        self.set_identity()
        self.make_repo("zeta-acme-hidden", commit=True, claude_md=True,
                       origin="https://deploy:ghp_SYNTH" + "ETIC1" + "@" +
                       "git.contoso-private.test/team/zeta.git")
        self.write_router(vault, "zeta-acme-hidden")
        settings = self.write_settings()
        settings["permissions"]["allow"].append("Bash(python3 /srv/acme-hidden/x.py)")
        settings["permissions"]["deny"] = ["Read(~/.ssh/**)", "Read(acme-hidden)"]
        write(self.home / ".claude" / "settings.json", json.dumps(settings))
        write(vault / ".claude" / "settings.json", json.dumps({"sandbox": {
            "enabled": "acme-hidden", "network": {"allowedDomains": ["acme-hidden.test"]}}}))
        for script in SCRIPTS:
            for args in ((), ("--sandbox",)):
                with self.subTest(script=str(script.relative_to(ROOT)), args=args):
                    output = self.run_script(*args, script=script)
                    self.assert_no_leaks(output, extra=(
                        "Zebulon", "Quixote", "zebulon.quixote", "zeb-secret-login",
                        "SYNTHETIC-KEY", "deploy", "zeta", str(self.home)))
                    self.assertIn("origin: other host", output)


@unittest.skipUnless(BASH and shutil.which("git"), "bash and git required")
class TestOrigin(StatusCheckCase):
    """Remotes are classified (GitHub / other host / local path), never shown."""

    def setUp(self):
        super().setUp()
        vault = self.make_vault(self.home / "AIAC-Vault")
        self.repo = self.make_repo("code")
        self.write_router(vault, "code")

    def set_origin(self, remote):
        if subprocess.run(["git", "remote", "get-url", "origin"], cwd=str(self.repo),
                          env=self.env, capture_output=True).returncode == 0:
            self.git(self.repo, "remote", "set-url", "origin", remote)
        else:
            self.git(self.repo, "remote", "add", "origin", remote)

    def origin(self, *args, script=None):
        return next(line for line in self.run_script(*args, script=script).splitlines()
                    if line.startswith("[info]") and "  origin" in line
                    ).split("origin", 1)[1].strip()

    def test_github_remote_is_classified_without_credentials_or_path(self):
        self.set_origin("https://user:tok3n" + "@" + "github.com/org/private.git")
        for script in SCRIPTS:
            with self.subTest(script=str(script.relative_to(ROOT))):
                output = self.run_script(script=script)
                self.assertNotIn("tok3n", output)
                self.assertNotIn("private.git", output)
                self.assertNotIn("github.com/", output)
                self.assertNotIn("(github.com)", output)
                self.assertIn("origin: GitHub", output)
                self.assertEqual(statuses(output)["Doc 02 - repo origin points at GitHub"],
                                 "DONE")

    def test_other_github_remote_formats_are_classified_github(self):
        for remote in ("ssh://git" + "@" + "github.com:2222/org/private.git?query#fragment",
                       "git" + "@" + "github.com:org/private.git",
                       "github.com:org/private.git",
                       "https://GitHub.com/org/private.git",
                       "https://github.com/org/private.git?notify=someone" + "@" +
                       "elsewhere.test#fragment"):
            with self.subTest(remote=remote):
                self.set_origin(remote)
                self.assertEqual(self.origin(), "GitHub")

    def test_private_remote_host_is_never_printed_by_default(self):
        for remote in ("https://git.contoso-private.test/team/zeta-private.git",
                       "git" + "@" + "git.contoso-private.test:team/zeta-private.git",
                       "ssh://deploy" + "@" + "git.contoso-private.test:2222/zeta-private.git",
                       "ssh://git" + "@" + "[2001:db8::1]:2222/repo.git",
                       "git" + "@" + "[2001:db8::1]:repo.git"):
            self.set_origin(remote)
            for script in SCRIPTS:
                with self.subTest(remote=remote, script=str(script.relative_to(ROOT))):
                    output = self.run_script(script=script)
                    self.assertIn("origin: other host", output)
                    for leak in ("contoso-private", "zeta-private", "2001:db8", "deploy"):
                        self.assertNotIn(leak, output)
                    self.assertEqual(
                        statuses(output)["Doc 02 - repo origin points at GitHub"], "NOT DONE")

    def test_details_add_the_host_but_never_credentials_or_path(self):
        self.set_origin("https://deploy:tok3n" + "@" + "git.contoso-private.test/team/zeta-private.git")
        output = self.run_script("--details")
        self.assertIn("other host (git.contoso-private.test)", output)
        for leak in ("tok3n", "deploy", "zeta-private"):
            self.assertNotIn(leak, output)

    def test_origin_reports_none_when_origin_is_missing(self):
        output = self.run_script()
        self.assertIn("origin: none", output)
        self.assertEqual(statuses(output)["Doc 02 - repo origin points at GitHub"], "NOT DONE")

    def test_local_and_unrecognized_remotes_are_classified_not_shown(self):
        remotes = [("client-private.git", "local path"),
                   ("client-private/backup.git", "local path"),
                   ("/abs/client-private/repo.git", "local path"),
                   ("../client-private/repo.git", "local path"),
                   ("file:///x/client-private/repo.git", "local path"),
                   ("file://localhost/x/client-private.git", "local path"),
                   ("C:/Users/zq/client-private.git", "local path"),
                   ("x:client-private", "unrecognized")]
        for remote, kind in remotes:
            self.set_origin(remote)
            for script in SCRIPTS:
                with self.subTest(remote=remote, script=str(script.relative_to(ROOT))):
                    output = self.run_script(script=script)
                    self.assertIn("origin: %s" % kind, output)
                    self.assertNotIn("client-private", output)
                    self.assertEqual(
                        statuses(output)["Doc 02 - repo origin points at GitHub"], "NOT DONE")


@unittest.skipUnless(BASH and shutil.which("git"), "bash and git required")
class TestVerdicts(StatusCheckCase):
    def test_pre_session_homework_complete(self):
        self.install_tools()
        self.make_vault(self.home / "AIAC-Vault")
        output = self.run_script()
        self.assertEqual(verdict(output),
                         "VERDICT: PRE-SESSION - homework complete, ready for the session")
        self.assertIn("[sess]", output)
        self.assert_safe_block_shape(output)

    def test_pre_session_homework_incomplete_counts_only_homework(self):
        output = self.run_script()  # no tools, no vault
        st = statuses(output)
        open_home = sum(1 for name in ("Doc 01 - GitHub CLI (gh) installed",
                                       "Doc 01 - GitHub CLI credentials present",
                                       "Doc 01 - Claude Code installed",
                                       "Doc 01 - Obsidian installed",
                                       "Pre-flight - vault folder exists",
                                       "Pre-flight - vault not in a cloud-synced folder",
                                       "Pre-flight - Obsidian config found in this folder",
                                       "Doc 01 - Git installed", "Doc 01 - jq installed",
                                       "Doc 01 - Python 3 installed")
                        if st.get(name) == "NOT DONE")
        self.assertEqual(verdict(output),
                         "VERDICT: PRE-SESSION - homework not complete (%d item(s) NOT DONE)"
                         % open_home)

    def test_optional_checks_are_never_not_done(self):
        output = self.run_script()
        for name, status in statuses(output).items():
            if name in OPTIONAL:
                self.assertIn(status, ("DONE", "SKIPPED (optional)"), name)

    @unittest.skipUnless(JQ, "jq required")
    def test_complete_setup_is_all_done(self):
        self.complete_setup()
        for script in SCRIPTS:
            with self.subTest(script=str(script.relative_to(ROOT))):
                output = self.run_script(script=script)
                st = statuses(output)
                not_done = [n for n, s in st.items() if s == "NOT DONE"]
                self.assertEqual(not_done, [], output)
                self.assertTrue(verdict(output).startswith(
                    "VERDICT: PHASE 0 SETUP COMPLETE"), output)
                self.assert_safe_block_shape(output)

    @unittest.skipUnless(JQ, "jq required")
    def test_one_skill_file_does_not_complete_skills_or_plugins(self):
        self.complete_setup()
        shutil.rmtree(self.home / ".claude" / "skills")
        write(self.home / ".claude" / "skills" / "session-close" / "SKILL.md", "x\n")
        registry = self.home / ".claude" / "plugins" / "installed_plugins.json"
        registry.unlink()
        (self.home / ".claude" / "plugins" / "marketplaces" / "claude-plugins-official"
         / "plugins" / "playground").mkdir(parents=True)
        st = statuses(self.run_script())
        self.assertEqual(st["Doc 03 - starter skills (all 6)"], "NOT DONE")
        self.assertEqual(st["Doc 03 - plugins (compound-engineering, superpowers, playground)"], "NOT DONE")

    @unittest.skipUnless(JQ, "jq required")
    def test_compound_engineering_plugin_is_required(self):
        self.complete_setup()
        settings = json.loads((self.home / ".claude" / "settings.json").read_text())
        settings["enabledPlugins"]["compound-engineering@compound-engineering-plugin"] = False
        write(self.home / ".claude" / "settings.json", json.dumps(settings))
        st = statuses(self.run_script())
        self.assertEqual(
            st["Doc 03 - plugins (compound-engineering, superpowers, playground)"], "NOT DONE")

    @unittest.skipUnless(JQ, "jq required")
    def test_disabled_plugin_does_not_count(self):
        self.complete_setup()
        path = self.home / ".claude" / "settings.json"
        settings = json.loads(path.read_text())
        settings["enabledPlugins"]["playground@claude-plugins-official"] = False
        path.write_text(json.dumps(settings))
        st = statuses(self.run_script())
        self.assertEqual(st["Doc 03 - plugins (compound-engineering, superpowers, playground)"], "NOT DONE")

    @unittest.skipUnless(JQ, "jq required")
    def test_obsidian_settings_checked_by_value(self):
        vault = self.complete_setup()
        write(vault / ".obsidian" / "app.json", json.dumps({"alwaysUpdateLinks": True}))
        output = self.run_script()
        self.assertEqual(statuses(output)["Doc 02 - Obsidian settings (Files and links)"],
                         "NOT DONE")
        self.assertIn("new notes go to INBOX", output)

    @unittest.skipUnless(JQ, "jq required")
    def test_ask_list_needs_every_rule(self):
        self.complete_setup()
        path = self.home / ".claude" / "settings.json"
        for rule in DOC02_ASK:
            with self.subTest(missing=rule):
                settings = json.loads(path.read_text())
                settings["permissions"]["ask"] = [r for r in DOC02_ASK if r != rule]
                path.write_text(json.dumps(settings))
                output = self.run_script()
                self.assertEqual(statuses(output)["Doc 02 - ask-first rules in settings"],
                                 "NOT DONE")
                name = rule[len("Bash("):-len(" *)")]
                self.assertIn("missing from permissions.ask: %s" % name, output)

    @unittest.skipUnless(JQ, "jq required")
    def test_ask_wildcards_are_not_blanket_but_allow_ones_are(self):
        self.complete_setup()
        path = self.home / ".claude" / "settings.json"
        self.assertEqual(statuses(self.run_script())[
            "Doc 02 - no blanket approvals in settings"], "DONE")
        for rule in ("Bash(mkdir *)", "Bash(mkdir:*)", "Glob", "Grep", "Bash(cat *)"):
            with self.subTest(allow=rule):
                settings = json.loads(path.read_text())
                settings["permissions"]["allow"] = DOC02_ALLOW + [rule]
                path.write_text(json.dumps(settings))
                self.assertEqual(statuses(self.run_script())[
                    "Doc 02 - no blanket approvals in settings"], "NOT DONE")

    def test_only_a_repo_named_in_the_router_is_inspected(self):
        vault = self.make_vault(self.home / "AIAC-Vault")
        self.write_router(vault)  # names no repo
        self.make_repo("aaa-first-unrelated", origin="https://unrelated-host.test/x.git")
        output = self.run_script("--details")
        self.assertEqual(statuses(output)["Doc 02 - code repo in ~/dev (named in router)"],
                         "NOT DONE")
        self.assertNotIn("aaa-first-unrelated", output)
        self.assertNotIn("unrelated-host", output)

    def test_router_vault_without_obsidian_folder_is_flagged(self):
        vault = self.home / "AIAC-Vault"
        (vault / "00 HUB" / "00 INBOX").mkdir(parents=True)
        self.write_router(vault)
        # A second, different folder that Obsidian did open must not satisfy it.
        self.make_vault(self.home / "Documents" / "Other Vault")
        st = statuses(self.run_script())
        self.assertEqual(st["Pre-flight - vault folder exists"], "DONE")
        self.assertEqual(st["Pre-flight - Obsidian config found in this folder"], "NOT DONE")


@unittest.skipUnless(BASH and shutil.which("git"), "bash and git required")
class TestCloudSyncedVault(StatusCheckCase):
    def test_synced_vault_paths_are_not_done(self):
        cases = [("OneDrive - Contoso", "OneDrive"), ("Dropbox", "Dropbox"),
                 ("Google Drive", "Google Drive"), ("My Drive", "Google Drive"),
                 ("Library/Mobile Documents/com~apple~CloudDocs", "iCloud")]
        for folder, kind in cases:
            with self.subTest(folder=folder):
                vault = self.make_vault(self.home / folder / "Vault")
                self.write_router(vault)
                output = self.run_script()
                self.assertEqual(
                    statuses(output)["Pre-flight - vault not in a cloud-synced folder"],
                    "NOT DONE")
                self.assertIn("the vault is inside %s" % kind, output)

    def test_local_vault_is_done(self):
        vault = self.make_vault(self.home / "AIAC-Vault")
        self.write_router(vault)
        st = statuses(self.run_script())
        self.assertEqual(st["Pre-flight - vault not in a cloud-synced folder"], "DONE")


@unittest.skipUnless(BASH and shutil.which("git"), "bash and git required")
class TestSandboxLines(StatusCheckCase):
    def setUp(self):
        super().setUp()
        self.vault = self.make_vault(self.home / "AIAC-Vault")
        self.write_router(self.vault)

    def test_sandbox_lines_hidden_by_default(self):
        output = self.run_script()
        self.assertFalse(SANDBOX_NAMES & set(statuses(output)))
        self.assertNotIn("02-S", "\n".join(safe_block(output)))
        self.assertNotIn("OPT-IN SANDBOX", output)

    def test_sandbox_lines_shown_with_flag(self):
        self.assertEqual(SANDBOX_NAMES & set(statuses(self.run_script("--sandbox"))),
                         SANDBOX_NAMES)

    def test_sandbox_lines_shown_when_sandbox_config_detected(self):
        write(self.vault / ".claude" / "settings.json", json.dumps({"sandbox": {"enabled": True}}))
        self.assertEqual(SANDBOX_NAMES & set(statuses(self.run_script())), SANDBOX_NAMES)

    def write_sandbox(self, **filesystem):
        fs = {"denyRead": ["~/", "~/.claude/.credentials.json"],
              "allowRead": [".", "~/.claude"], "allowWrite": []}
        fs.update(filesystem)
        write(self.vault / ".claude" / "settings.json", json.dumps({"sandbox": {
            "enabled": True, "failIfUnavailable": True, "allowUnsandboxedCommands": False,
            "filesystem": fs,
            "network": {"allowedDomains": ["github.com", "api.github.com",
                                           "codeload.github.com", "registry.npmjs.org",
                                           "pypi.org", "files.pythonhosted.org"]}}}))

    def sandbox_status(self):
        return statuses(self.run_script())["Doc 02-S - sandbox config in the vault (Part 3a)"]

    @unittest.skipUnless(JQ, "jq required")
    def test_part_3a_config_is_done(self):
        self.write_sandbox()
        self.assertEqual(self.sandbox_status(), "DONE")

    @unittest.skipUnless(JQ, "jq required")
    def test_part_3c_option_b_named_repo_is_done(self):
        self.write_sandbox(allowRead=[".", "~/.claude", "~/dev/client-zeta"],
                           allowWrite=["~/dev/client-zeta"])
        self.assertEqual(self.sandbox_status(), "DONE")

    @unittest.skipUnless(JQ, "jq required")
    def test_broad_or_weak_sandbox_configs_are_not_done(self):
        for fs in ({"denyRead": ["~/.ssh/**"]},
                   {"denyRead": ["~/"]},  # the login file inside ~/.claude stays readable
                   {"allowRead": [".", "~/.claude", "~"]},
                   {"allowRead": [".", "~/.claude", "~/dev"]},
                   {"allowRead": [".", "~/.claude", "~/Documents/**"]},
                   {"allowRead": ["."]},
                   {"allowWrite": ["~/"]},
                   {"allowWrite": ["~/dev/**"]}):
            with self.subTest(fs=fs):
                self.write_sandbox(**fs)
                self.assertEqual(self.sandbox_status(), "NOT DONE")

    # -- round 4: the effective sandbox, across every settings file --------
    DOMAINS = ["github.com", "api.github.com", "codeload.github.com",
               "registry.npmjs.org", "pypi.org", "files.pythonhosted.org"]

    def write_json(self, path, data):
        write(path, json.dumps(data))

    @unittest.skipUnless(JQ, "jq required")
    def test_domains_must_match_the_02s_list_exactly(self):
        for domains in (self.DOMAINS + ["acme-hidden-exfil.test"],
                        self.DOMAINS[:-1],
                        ["*"],
                        self.DOMAINS[:3] + ["*.github.com"] + self.DOMAINS[3:]):
            with self.subTest(domains=domains):
                self.write_sandbox()
                data = json.loads((self.vault / ".claude" / "settings.json").read_text())
                data["sandbox"]["network"]["allowedDomains"] = domains
                self.write_json(self.vault / ".claude" / "settings.json", data)
                output = self.run_script()
                self.assertEqual(statuses(output)[
                    "Doc 02-S - sandbox config in the vault (Part 3a)"], "NOT DONE")
                self.assertNotIn("acme-hidden", output)
        # Order and duplicates don't matter.
        self.write_sandbox()
        data = json.loads((self.vault / ".claude" / "settings.json").read_text())
        data["sandbox"]["network"]["allowedDomains"] = list(reversed(self.DOMAINS)) + ["pypi.org"]
        self.write_json(self.vault / ".claude" / "settings.json", data)
        self.assertEqual(self.sandbox_status(), "DONE")

    @unittest.skipUnless(JQ, "jq required")
    def test_at_most_the_one_chosen_repo_is_readable_or_writable(self):
        for fs in ({"allowRead": [".", "~/.claude", "~/dev/zeta", "~/dev/acme-hidden"],
                    "allowWrite": ["~/dev/zeta"]},
                   {"allowRead": [".", "~/.claude", "~/dev/zeta"],
                    "allowWrite": ["~/dev/zeta", "~/dev/acme-hidden"]},
                   {"allowRead": [".", "~/.claude", "~/dev/zeta"],
                    "allowWrite": ["~/dev/acme-hidden"]},
                   {"allowRead": [".", "~/.claude"], "allowWrite": ["~/dev/zeta"]}):
            with self.subTest(fs=fs):
                self.write_sandbox(**fs)
                output = self.run_script()
                self.assertEqual(statuses(output)[
                    "Doc 02-S - sandbox config in the vault (Part 3a)"], "NOT DONE")
                self.assertNotIn("acme-hidden", output)
        # Trailing / and /** spell the same repo.
        self.write_sandbox(allowRead=[".", "~/.claude", "~/dev/zeta/"], allowWrite=["~/dev/zeta/**"])
        self.assertEqual(self.sandbox_status(), "DONE")

    @unittest.skipUnless(JQ, "jq required")
    def test_the_repo_must_be_the_one_the_router_names(self):
        self.write_router(self.vault, repo_name="zeta")
        self.make_repo("zeta")
        self.write_sandbox(allowRead=[".", "~/.claude", "~/dev/zeta"], allowWrite=["~/dev/zeta"])
        self.assertEqual(self.sandbox_status(), "DONE")
        self.write_sandbox(allowRead=[".", "~/.claude", "~/dev/other"], allowWrite=["~/dev/other"])
        self.assertEqual(self.sandbox_status(), "NOT DONE")

    @unittest.skipUnless(JQ, "jq required")
    def test_other_settings_files_that_widen_or_weaken_the_sandbox(self):
        local = self.vault / ".claude" / "settings.local.json"
        user = self.home / ".claude" / "settings.json"
        cases = [
            (local, {"sandbox": {"enabled": False}}),
            (local, {"sandbox": {"allowUnsandboxedCommands": True}}),
            (local, {"sandbox": {"excludedCommands": ["git *"]}}),
            (local, {"sandbox": {"filesystem": {"allowWrite": ["~/acme-hidden"]}}}),
            (local, {"sandbox": {"network": {"allowedDomains": ["acme-hidden.test"]}}}),
            (local, {"permissions": {"allow": ["WebFetch(domain:acme-hidden.test)"]}}),
            (local, {"permissions": {"allow": ["Edit(~/acme-hidden/**)"]}}),
            (local, {"sandbox": "acme-hidden"}),
            (user, {"sandbox": {"filesystem": {"disabled": True}}}),
            (user, {"sandbox": {"filesystem": {"allowRead": ["~/acme-hidden"]}}}),
            (user, {"sandbox": {"excludedCommands": ["docker *"]}}),
            (user, {"sandbox": {"allowAppleEvents": True}}),
            (user, {"sandbox": {"enableWeakerNestedSandbox": True}}),
            (user, {"sandbox": {"network": {"allowUnixSockets": ["/var/run/acme-hidden.sock"]}}}),
            (user, {"sandbox": {"network": {"httpProxyPort": 8080}}}),
            (user, {"permissions": {"allow": list(DOC02_ALLOW), "additionalDirectories": ["~/acme-hidden"]}}),
        ]
        for path, data in cases:
            with self.subTest(file=path.name, data=data):
                self.write_sandbox()
                for f in (local, user):
                    if f.exists():
                        f.unlink()
                self.write_json(path, data)
                output = self.run_script()
                self.assertEqual(statuses(output)[
                    "Doc 02-S - sandbox config in the vault (Part 3a)"], "NOT DONE")
                self.assertNotIn("acme-hidden", output)
                self.assertNotIn("8080", output)

    @unittest.skipUnless(JQ, "jq required")
    def test_harmless_local_and_user_settings_keep_it_done(self):
        self.write_sandbox()
        self.write_json(self.vault / ".claude" / "settings.local.json",
                        {"sandbox": {"enabled": True, "autoAllowBashIfSandboxed": True},
                         "permissions": {"allow": ["Bash(npm test)", "WebFetch(domain:pypi.org)"]}})
        self.write_json(self.home / ".claude" / "settings.json", self.part_3b_settings())
        self.assertEqual(self.sandbox_status(), "DONE")

    @unittest.skipUnless(JQ, "jq required")
    def test_managed_policy_counts_and_unreadable_policy_is_unverified(self):
        managed = self.base / "managed"
        self.env["AIAC_STATUS_MANAGED_DIR"] = str(managed)
        self.write_sandbox()
        self.write_json(managed / "managed-settings.json", {"sandbox": {"filesystem": {"disabled": True}}})
        self.assertEqual(self.sandbox_status(), "NOT DONE")
        (managed / "managed-settings.json").unlink()
        self.write_json(managed / "managed-settings.d" / "10-acme-hidden.json",
                        {"sandbox": {"excludedCommands": ["acme-hidden *"]}})
        self.assertEqual(self.sandbox_status(), "NOT DONE")
        (managed / "managed-settings.d" / "10-acme-hidden.json").unlink()
        write(managed / "managed-settings.json", '{"sandbox": {"acme-hidden"')
        output = self.run_script()
        self.assertEqual(statuses(output)[
            "Doc 02-S - sandbox config in the vault (Part 3a)"], "NOT DONE")
        self.assertIn("unverified", output)
        self.assertNotIn("acme-hidden", output)
        write(managed / "managed-settings.json", json.dumps({"sandbox": {"enabled": True}}))
        self.assertEqual(self.sandbox_status(), "DONE")

    def part_3b_settings(self, stop=True):
        settings = self.write_settings()
        settings["permissions"]["allow"] = list(DOC02_ALLOW)
        settings["permissions"]["ask"] = list(DOC02_ASK)
        settings["permissions"]["deny"] = list(DOC02S_DENY)
        if stop:
            settings["hooks"]["Stop"] = [{"hooks": [{"type": "command", "command": "true"}]}]
        return settings

    def global_status(self, settings):
        write(self.home / ".claude" / "settings.json", json.dumps(settings))
        return statuses(self.run_script("--sandbox"))[
            "Doc 02-S - hardened global settings (Part 3b)"]

    @unittest.skipUnless(JQ, "jq required")
    def test_part_3b_global_settings_are_done(self):
        self.assertEqual(self.global_status(self.part_3b_settings()), "DONE")
        # 02-S says to delete the sound hook if unsure: still DONE without it.
        self.assertEqual(self.global_status(self.part_3b_settings(stop=False)), "DONE")
        st = statuses(self.run_script("--sandbox"))
        self.assertEqual(st["Doc 02 - no blanket approvals in settings"], "DONE")

    @unittest.skipUnless(JQ, "jq required")
    def test_part_3b_rejects_missing_deny_blanket_rules_and_empty_stop(self):
        missing_deny = self.part_3b_settings()
        missing_deny["permissions"]["deny"] = []
        blanket = self.part_3b_settings()
        blanket["permissions"]["allow"].append("Bash(git log *)")
        interpreter = self.part_3b_settings()
        interpreter["permissions"]["allow"].append("Bash(python3 *)")
        empty_stop = self.part_3b_settings()
        empty_stop["hooks"]["Stop"] = []
        for name, settings in (("missing deny", missing_deny), ("blanket git", blanket),
                               ("interpreter", interpreter), ("empty Stop", empty_stop)):
            with self.subTest(case=name):
                self.assertEqual(self.global_status(settings), "NOT DONE")

    @unittest.skipUnless(JQ, "jq required")
    def test_part_3b_needs_every_deny_rule(self):
        # Each canonical rule missing on its own must fail hardening, and the
        # detail line names the missing entry with a fixed label.
        labels = ["~/.ssh", "~/.aws", "~/.gnupg", "~/.config/gh",
                  "~/Library/Keychains", "~/.claude/.credentials.json",
                  ".env files", "*.pem files", "*.key files"]
        for rule, label in zip(DOC02S_DENY, labels):
            with self.subTest(missing=rule):
                settings = self.part_3b_settings()
                settings["permissions"]["deny"] = [r for r in DOC02S_DENY if r != rule]
                write(self.home / ".claude" / "settings.json", json.dumps(settings))
                output = self.run_script("--sandbox")
                self.assertEqual(statuses(output)[
                    "Doc 02-S - hardened global settings (Part 3b)"], "NOT DONE")
                self.assertIn("deny list incomplete - missing: %s" % label, output)

    @unittest.skipUnless(JQ, "jq required")
    def test_part_3b_relative_file_rules_do_not_count(self):
        # **/x only covers the folder Claude starts in; 02-S anchors them at ~.
        for rule in ("Read(~/**/.env)", "Read(~/**/*.pem)", "Read(~/**/*.key)"):
            with self.subTest(rule=rule):
                settings = self.part_3b_settings()
                settings["permissions"]["deny"] = [
                    r.replace("~/**/", "**/") if r == rule else r for r in DOC02S_DENY]
                self.assertEqual(self.global_status(settings), "NOT DONE")

    @unittest.skipUnless(JQ, "jq required")
    def test_part_3b_extra_deny_rules_are_fine(self):
        settings = self.part_3b_settings()
        settings["permissions"]["deny"] = ["Read(~/Private/**)"] + DOC02S_DENY
        self.assertEqual(self.global_status(settings), "DONE")


@unittest.skipUnless(BASH and shutil.which("git"), "bash and git required")
class TestReadOnly(StatusCheckCase):
    def snapshot(self):
        snap = {}
        for dirpath, dirnames, filenames in os.walk(str(self.base)):
            for name in dirnames + filenames:
                p = os.path.join(dirpath, name)
                st = os.lstat(p)
                snap[p] = (stat.S_IFMT(st.st_mode), st.st_size, st.st_mtime_ns,
                           stat.S_IMODE(st.st_mode))
        return snap

    def test_script_writes_nothing(self):
        vault = self.make_vault(self.home / "AIAC-Vault", full=True)
        self.set_identity()
        self.make_repo("code", commit=True, claude_md=True,
                       origin="https://github.com/org/code.git")
        self.write_router(vault, "code")
        self.write_settings()
        self.install_tools()
        before = self.snapshot()
        for args in ((), ("--details",), ("--sandbox",)):
            self.run_script(*args)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(list(self.tmpdir.iterdir()), [])

    def test_gh_and_claude_are_never_run(self):
        # gh can create ~/.config/gh/config.yml on its first run, and claude can
        # write its own state. Stubs that WOULD write prove neither is executed.
        vault = self.make_vault(self.home / "AIAC-Vault", full=True)
        self.write_router(vault)
        self.write_settings()
        marker_gh = self.home / ".config" / "gh" / "config.yml"
        marker_claude = self.home / ".claude.json"
        self.stub("gh", 'mkdir -p "$HOME/.config/gh" && echo x > "$HOME/.config/gh/config.yml"; '
                        'echo "gh version 9.9.9"')
        self.stub("claude", 'echo x > "$HOME/.claude.json"; echo "9.9.9 (Claude Code)"')
        before = self.snapshot()
        for args in ((), ("--details",), ("--sandbox",)):
            output = self.run_script(*args)
            self.assertRegex(output, r"Doc 01 - GitHub CLI \(gh\) installed +installed")
        self.assertFalse(marker_gh.exists())
        self.assertFalse(marker_claude.exists())
        self.assertEqual(self.snapshot(), before)

    def test_claude_and_gh_versions_come_from_the_install_path(self):
        versions = self.base / "share" / "claude" / "versions"
        write(versions / "2.1.300", "#!/bin/sh\necho x > \"$HOME/ran\"\n", 0o755)
        (self.bin / "claude").symlink_to(versions / "2.1.300")
        cellar = self.base / "Cellar" / "gh" / "2.63.0" / "bin"
        write(cellar / "gh", "#!/bin/sh\necho x > \"$HOME/ran\"\n", 0o755)
        (self.bin / "gh").symlink_to(cellar / "gh")
        output = self.run_script()
        self.assertRegex(output, r"Doc 01 - Claude Code installed +version 2\.1\.300")
        self.assertRegex(output, r"Doc 01 - GitHub CLI \(gh\) installed +version 2\.63\.0")
        self.assertFalse((self.home / "ran").exists())


@unittest.skipUnless(BASH and shutil.which("git") and JQ, "bash, git and jq required")
class TestBroadRules(StatusCheckCase):
    """"No blanket approvals" means what it says, in every settings file."""

    LABEL = "Doc 02 - no blanket approvals in settings"

    def setUp(self):
        super().setUp()
        self.vault = self.complete_setup()
        self.repo = self.home / "dev" / "client-zeta-secret"
        self.gs = self.home / ".claude" / "settings.json"
        self.base_settings = json.loads(self.gs.read_text())

    def status(self):
        return statuses(self.run_script())[self.LABEL]

    def with_global(self, allow=(), **perms):
        settings = json.loads(json.dumps(self.base_settings))
        settings["permissions"]["allow"] = DOC02_ALLOW + list(allow)
        settings["permissions"].update(perms)
        write(self.gs, json.dumps(settings))

    def test_complete_setup_is_done(self):
        self.assertEqual(self.status(), "DONE")

    def test_broad_allow_rules_and_modes_in_global_settings_are_not_done(self):
        for rule in ("Bash(rm *)", "Bash(sudo *)", "Bash(curl *)", "Bash(gh *)",
                     "Edit(~/**)", "Write(*)", "Read(~/Documents/**)",
                     "Bash(/usr/bin/python3 *)", "Bash(/usr/bin/python3 tool.py)",
                     "Bash(uv run *)", "Bash(osascript *)", "Bash(npm:*)",
                     "PowerShell(Remove-Item *)", "WebFetch", "Bash", "Edit",
                     "WebFetch(domain:*)", "mcp__server__*"):
            with self.subTest(allow=rule):
                self.with_global([rule])
                self.assertEqual(self.status(), "NOT DONE")
        for mode in ("auto", "acceptEdits", "dontAsk", "bypassPermissions"):
            with self.subTest(defaultMode=mode):
                self.with_global(defaultMode=mode)
                self.assertEqual(self.status(), "NOT DONE")

    def test_exact_and_scoped_rules_are_fine(self):
        self.with_global(["Bash(npm test)", "mcp__claude_ai_Granola__get_meetings",
                          "WebFetch(domain:example.com)", "WebSearch"], defaultMode="plan")
        self.assertEqual(self.status(), "DONE")

    def test_saved_approvals_in_vault_and_repo_files_count(self):
        cases = [
            (self.vault / ".claude" / "settings.local.json",
             {"permissions": {"allow": ["Bash"], "defaultMode": "bypassPermissions"}}),
            (self.vault / ".claude" / "settings.json",
             {"permissions": {"allow": ["Bash(git push *)"]}}),
            (self.repo / ".claude" / "settings.local.json",
             {"permissions": {"allow": ["Bash(python3 *)"]}}),
            (self.repo / ".claude" / "settings.json",
             {"permissions": {"additionalDirectories": ["~/"]}}),
            (self.home / ".claude" / "settings.local.json",
             {"permissions": {"allow": ["Bash(rm *)"]}}),
        ]
        for path, data in cases:
            with self.subTest(path=str(path.relative_to(self.home))):
                write(path, json.dumps(data))
                output = self.run_script()
                self.assertEqual(statuses(output)[self.LABEL], "NOT DONE")
                self.assertNotIn(str(self.home), output)
                path.unlink()
        self.assertEqual(self.status(), "DONE")

    def test_details_name_the_file_by_a_fixed_label_only(self):
        write(self.vault / ".claude" / "settings.local.json",
              json.dumps({"permissions": {"allow": ["Bash(acme-hidden-tool *)"]}}))
        details = self.run_script("--details")
        self.assertIn("broad rule (1): vault .claude/settings.local.json: "
                      "a command rule with a wildcard", details)
        self.assertNotIn("acme-hidden", details)

    def test_malformed_local_settings_file_is_not_done(self):
        write(self.vault / ".claude" / "settings.local.json", '{"permissions": {"allow": [')
        output = self.run_script()
        self.assertEqual(statuses(output)[self.LABEL], "NOT DONE")
        self.assertIn("1 settings file(s) could not be read", output)

    def test_broad_rule_line_also_counts_unreadable_files(self):
        write(self.vault / ".claude" / "settings.local.json", '{"permissions": {"allow": [')
        write(self.repo / ".claude" / "settings.local.json",
              json.dumps({"permissions": {"allow": ["Bash(rm *)"]}}))
        output = self.run_script()
        self.assertEqual(statuses(output)[self.LABEL], "NOT DONE")
        self.assertIn("1 broad rule(s) in 1 settings file(s) - remove them "
                      "(--details lists them); 1 file(s) unreadable", output)
        # Without an unreadable file the line carries no such suffix.
        (self.vault / ".claude" / "settings.local.json").unlink()
        output = self.run_script()
        self.assertIn("1 broad rule(s) in 1 settings file(s)", output)
        self.assertNotIn("unreadable", output)

@unittest.skipUnless(BASH and shutil.which("git"), "bash and git required")
class TestPlatforms(StatusCheckCase):
    def test_windows_git_bash_simulation(self):
        self.stub("uname", 'case "$1" in -s) echo MINGW64_NT-10.0-19045 ;; '
                           '-m) echo x86_64 ;; *) echo MINGW64_NT-10.0-19045 ;; esac')
        local = self.base / "LocalAppData"
        write(local / "Programs" / "Obsidian" / "Obsidian.exe", "")
        self.env["LOCALAPPDATA"] = str(local)
        output = self.run_script()
        self.assertIn("OS: Windows", safe_block(output))
        st = statuses(output)
        self.assertEqual(st["Doc 01 - Obsidian installed"], "DONE")
        self.assertNotIn("Doc 01 - Ghostty terminal", st)
        self.assertNotIn("/Applications", output)
        self.assert_safe_block_shape(output)

    def test_wsl_simulation_reads_windows_obsidian_and_vault_list(self):
        self.stub("uname", 'case "$1" in -s) echo Linux ;; -m) echo x86_64 ;; *) echo Linux ;; esac')
        mnt = self.base / "mnt"
        win_user = mnt / "c" / "Users" / "winuser"
        write(win_user / "AppData" / "Local" / "Programs" / "Obsidian" / "Obsidian.exe", "")
        self.make_vault(win_user / "AIAC-Vault")
        write(win_user / "AppData" / "Roaming" / "obsidian" / "obsidian.json",
              json.dumps({"vaults": {"abc": {"path": "C:\\Users\\winuser\\AIAC-Vault"}}}))
        self.env["WSL_DISTRO_NAME"] = "Ubuntu"
        self.env["AIAC_STATUS_WSL_MNT"] = str(mnt)
        output = self.run_script()
        self.assertIn("OS: Windows (WSL)", safe_block(output))
        st = statuses(output)
        self.assertEqual(st["Doc 01 - Obsidian installed"], "DONE")
        self.assertEqual(st["Pre-flight - vault folder exists"], "DONE")
        self.assertEqual(st["Pre-flight - Obsidian config found in this folder"], "DONE")


if __name__ == "__main__":
    unittest.main()
