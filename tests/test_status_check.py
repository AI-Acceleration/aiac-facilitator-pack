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
    "Doc 01 - GitHub CLI signed in",
    "Doc 01 - Claude Code installed",
    "Doc 01 - jq installed",
    "Doc 01 - Python 3 installed",
    "Doc 01 - Obsidian installed",
    "Doc 01 - Ghostty terminal",
    "Doc 01 - Granola or other transcription tool",
    "Pre-flight - vault folder exists",
    "Pre-flight - vault not in a cloud-synced folder",
    "Pre-flight - vault opened in Obsidian",
    "Doc 02-S - hardened global settings (Part 2b)",
    "Doc 02-S - sandbox config in the vault (Part 2a)",
    "Doc 02 - global settings file is valid",
    "Doc 02 - no blanket approvals in settings",
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
    "Doc 02 - repo connected to GitHub",
    "Doc 03 - starter skills (all 6)",
    "Doc 03 - plugins (superpowers, playground)",
    "Doc 03 - lessons.md",
}
OPTIONAL = {"Doc 01 - Ghostty terminal",
            "Doc 01 - Granola or other transcription tool"}
SANDBOX_NAMES = {"Doc 02-S - hardened global settings (Part 2b)",
                 "Doc 02-S - sandbox config in the vault (Part 2a)"}
STATUSES = ("DONE", "NOT DONE", "SKIPPED (optional)")
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
            "permissions": {"allow": ["Bash(ls *)", "Bash(mkdir *)", "Bash(wc *)",
                                      "Bash(git status)", "Bash(git remote -v)",
                                      "Glob", "Grep"],
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
        for plugin in ("superpowers", "playground"):
            key = plugin + "@claude-plugins-official"
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
                       "zeb-secret-login", "SYNTHETIC-KEY", str(self.home)):
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
        self.assertEqual(statuses(output)["Doc 01 - GitHub CLI signed in"], "DONE")
        self.assertNotIn("zeb-secret-login", output)

    def test_broad_rules_are_counted_not_listed_by_default(self):
        self.install_tools()
        vault = self.make_vault(self.home / "AIAC-Vault", full=True)
        self.write_router(vault)
        settings = self.write_settings()
        settings["permissions"]["allow"] += ["Bash(git *)", "Bash(python3 *)",
                                             "Bash(cat *)", "Bash(git remote *)"]
        write(self.home / ".claude" / "settings.json", json.dumps(settings))
        output = self.run_script()
        self.assertEqual(statuses(output)["Doc 02 - no blanket approvals in settings"],
                         "NOT DONE")
        self.assertIn("4 broad rule(s) found", output)
        self.assertNotIn("Bash(git *)", output)
        self.assertIn("broad rule: Bash(git *)", self.run_script("--details"))


@unittest.skipUnless(BASH and shutil.which("git"), "bash and git required")
class TestOrigin(StatusCheckCase):
    """Remote redaction: only a recognised host ever reaches the output."""

    def setUp(self):
        super().setUp()
        vault = self.make_vault(self.home / "AIAC-Vault")
        self.repo = self.make_repo("code")
        self.write_router(vault, "code")

    def origin(self, script=None):
        return next(line for line in self.run_script(script=script).splitlines()
                    if line.startswith("[info]") and "  origin" in line
                    ).split("origin", 1)[1].strip()

    def test_origin_reports_host_without_credentials_or_path_in_all_copies(self):
        self.git(self.repo, "remote", "add", "origin",
                 "https://user:tok3n" + "@" + "github.com/org/private.git")
        for script in SCRIPTS:
            with self.subTest(script=str(script.relative_to(ROOT))):
                output = self.run_script(script=script)
                self.assertNotIn("tok3n", output)
                self.assertNotIn("private.git", output)
                self.assertIn("present (github.com)", output)

    def test_origin_reports_only_host_for_other_remote_formats(self):
        remotes = [
            ("ssh://git" + "@" + "github.com:2222/org/private.git?query#fragment", "github.com"),
            ("git" + "@" + "github.com:org/private.git", "github.com"),
            ("https://github.com/org/private.git?notify=someone" + "@" +
             "elsewhere.test#fragment", "github.com"),
        ]
        self.git(self.repo, "remote", "add", "origin", "https://github.com/org/repo.git")
        for remote, host in remotes:
            with self.subTest(remote=remote):
                self.git(self.repo, "remote", "set-url", "origin", remote)
                self.assertEqual(self.origin(), "present (%s)" % host)

    def test_origin_reports_no_remote_when_origin_is_missing(self):
        output = self.run_script()
        self.assertIn("no remote", output)
        self.assertEqual(statuses(output)["Doc 02 - repo connected to GitHub"], "NOT DONE")

    def test_origin_redacts_local_and_unrecognized_remotes_in_all_copies(self):
        remotes = ["client-private.git", "client-private/backup.git", "/abs/path/repo.git",
                   "file:///x/repo.git", "file://localhost/x/repo.git",
                   "github.com:org/private.git"]
        self.git(self.repo, "remote", "add", "origin", "https://github.com/org/repo.git")
        for remote in remotes:
            self.git(self.repo, "remote", "set-url", "origin", remote)
            for script in SCRIPTS:
                with self.subTest(remote=remote, script=str(script.relative_to(ROOT))):
                    output = self.run_script(script=script)
                    self.assertIn("origin: present (local/unrecognized)", output)
                    self.assertNotIn(remote, output)

    def test_origin_preserves_bracketed_ipv6_host(self):
        remotes = ["ssh://git" + "@" + "[2001:db8::1]/repo.git",
                   "ssh://git" + "@" + "[2001:db8::1]:2222/repo.git",
                   "git" + "@" + "[2001:db8::1]:repo.git"]
        self.git(self.repo, "remote", "add", "origin", "https://github.com/org/repo.git")
        for remote in remotes:
            with self.subTest(remote=remote):
                self.git(self.repo, "remote", "set-url", "origin", remote)
                self.assertEqual(self.origin(), "present ([2001:db8::1])")


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
                                       "Doc 01 - GitHub CLI signed in",
                                       "Doc 01 - Claude Code installed",
                                       "Doc 01 - Obsidian installed",
                                       "Pre-flight - vault folder exists",
                                       "Pre-flight - vault not in a cloud-synced folder",
                                       "Pre-flight - vault opened in Obsidian",
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
        self.assertEqual(st["Doc 03 - plugins (superpowers, playground)"], "NOT DONE")

    @unittest.skipUnless(JQ, "jq required")
    def test_disabled_plugin_does_not_count(self):
        self.complete_setup()
        path = self.home / ".claude" / "settings.json"
        settings = json.loads(path.read_text())
        settings["enabledPlugins"]["playground@claude-plugins-official"] = False
        path.write_text(json.dumps(settings))
        st = statuses(self.run_script())
        self.assertEqual(st["Doc 03 - plugins (superpowers, playground)"], "NOT DONE")

    @unittest.skipUnless(JQ, "jq required")
    def test_obsidian_settings_checked_by_value(self):
        vault = self.complete_setup()
        write(vault / ".obsidian" / "app.json", json.dumps({"alwaysUpdateLinks": True}))
        output = self.run_script()
        self.assertEqual(statuses(output)["Doc 02 - Obsidian settings (Files and links)"],
                         "NOT DONE")
        self.assertIn("new notes go to INBOX", output)

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
        self.assertEqual(st["Pre-flight - vault opened in Obsidian"], "NOT DONE")


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

    @unittest.skipUnless(JQ, "jq required")
    def test_strict_sandbox_config_is_done(self):
        write(self.vault / ".claude" / "settings.json", json.dumps({"sandbox": {
            "enabled": True, "failIfUnavailable": True, "allowUnsandboxedCommands": False,
            "filesystem": {"denyRead": ["~/.ssh/**"], "allowRead": ["~/.claude/**"],
                           "allowWrite": []},
            "network": {"allowedDomains": ["github.com"]}}}))
        st = statuses(self.run_script())
        self.assertEqual(st["Doc 02-S - sandbox config in the vault (Part 2a)"], "DONE")


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
        self.assertEqual(st["Pre-flight - vault opened in Obsidian"], "DONE")


if __name__ == "__main__":
    unittest.main()
