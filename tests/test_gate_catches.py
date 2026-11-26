"""Positive controls: prove the gate CATCHES, not merely that it runs.

Every other gate test asserts the real repo reports clean. A gate that reports
clean on everything passes all of them. Each test here plants one specific
leak in a throwaway git repo and asserts exit 1 (or exit 3 for a failed
measurement) — so reverting any of the fixes turns a test red.

No real address appears anywhere in this file or in its fixture. The synthetic
addresses are built from fragments at runtime (so this file's own source
carries no match for the gate's address regex) and live at `.test`, the
reserved-invalid TLD. Their hashes are in `tests/fixtures/deny-hashes-test.txt`
and must never be copied into `.githooks/deny-hashes.txt`.
"""
import hashlib
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"

DOMAIN = "example-invalid" + ".test"
DENIED = "trainer.private" + "@" + DOMAIN      # hash IS in the test deny list
UNKNOWN = "someone.else" + "@" + DOMAIN        # hash is NOT in any deny list
REGISTRY = "00 — Trainer Registry (MAINTAINER ONLY).md"
GIT_EMAIL = "t" + "@" + DOMAIN  # fragments: this file is itself scanned by the gate
# A GitHub no-reply identity of a contributor who is not the maintainer.
NOREPLY_DOMAIN = "users.noreply" + ".github.com"
OUTSIDE = "98765+outside-contrib" + "@" + NOREPLY_DOMAIN
# The legacy login-only no-reply form older accounts still use.
LEGACY = "outside-contrib" + "@" + NOREPLY_DOMAIN
WEB_MERGE = "noreply" + "@" + "github.com"
# The service address on the assistant-attribution trailer, the one entry of
# the real .githooks/allow-patterns.txt.
SERVICE = "noreply" + "@" + "anthropic.com"
# A path word that is private without holding an address: CI output must
# never echo it.
PRIVATE_WORD = "participant-surname-zqxv"


def fp(addr):
    """How the gate names an address in its output."""
    return "address#" + hashlib.sha256(addr.lower().encode()).hexdigest()[:8]


def pid(name):
    """How the gate names a file or ref name in CI output."""
    return "path#" + hashlib.sha256(
        name.encode("utf-8", "surrogateescape")).hexdigest()[:8]


def gate_env(ci=False, path=None):
    """The test's own environment minus the CI markers, so local-mode tests
    stay local when the suite itself runs in GitHub Actions."""
    env = {k: v for k, v in os.environ.items()
           if k not in ("GITHUB_ACTIONS", "CI")}
    if ci:
        env["GITHUB_ACTIONS"] = "true"
    if path:
        env["PATH"] = path + os.pathsep + env.get("PATH", "")
    return env


def run_gate(sandbox, *args, ci=False, path=None):
    return subprocess.run(
        [sys.executable, str(sandbox / "bin" / "gate_scan.py")] + list(args),
        capture_output=True, text=True, cwd=str(sandbox),
        env=gate_env(ci, path))


def fake_git(directory, subcommand, stderr_text):
    """A `git` that fails `subcommand` with `stderr_text` on stderr and runs
    the real git for everything else. Put `directory` first on PATH."""
    real = shutil.which("git")
    script = Path(directory) / "git"
    script.write_text(
        "#!/bin/sh\n"
        "if [ \"$1\" = %s ]; then printf '%%s\\n' %s >&2; exit 128; fi\n"
        "exec %s \"$@\"\n" % (shlex.quote(subcommand), shlex.quote(stderr_text),
                              shlex.quote(real)), encoding="utf-8")
    script.chmod(0o755)
    return str(directory)


class GateSandbox(unittest.TestCase):
    """A git repo holding the REAL gate and the REAL pattern files, with the
    deny list swapped for the synthetic test fixture."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="gatecatch-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        (self.tmp / "bin").mkdir()
        shutil.copy2(ROOT / "bin" / "gate_scan.py", self.tmp / "bin" / "gate_scan.py")
        shutil.copytree(ROOT / ".githooks", self.tmp / ".githooks")
        shutil.copy2(FIXTURES / "deny-hashes-test.txt",
                     self.tmp / ".githooks" / "deny-hashes.txt")
        # --history scans whole commit objects, author/committer included:
        # permit the sandbox's own synthetic identity, exactly as the real
        # allowlist permits the repo's commit identities.
        with open(self.tmp / ".githooks" / "allow-patterns.txt", "a",
                  encoding="utf-8") as f:
            f.write("\n%s\n" % GIT_EMAIL)
        for cmd in (["init", "-q"],
                    ["config", "user.email", GIT_EMAIL],
                    ["config", "user.name", "t"]):
            subprocess.run(["git", *cmd], cwd=str(self.tmp), check=True,
                           capture_output=True)

    def write(self, rel, data):
        p = self.tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))
        subprocess.run(["git", "add", "--", rel], cwd=str(self.tmp),
                       check=True, capture_output=True)
        return p

    def assertBlocked(self, r, needle):
        self.assertEqual(r.returncode, 1,
                         "expected exit 1, got %d\n%s%s" % (r.returncode, r.stdout, r.stderr))
        self.assertIn(needle, r.stderr)

    def assertRedacted(self, r, *addrs):
        """CI logs are public: the gate must never print what it caught."""
        out = r.stdout + r.stderr
        for a in addrs:
            self.assertNotIn(a, out)
        self.assertNotIn(DOMAIN, out)

    # --- baseline: the gate is capable of catching at all -----------------
    def test_plain_unallowlisted_address_is_caught(self):
        self.write("doc.md", "write to %s please\n" % UNKNOWN)
        self.assertBlocked(run_gate(self.tmp, "--tree"), "UNALLOWLISTED")

    # --- obfuscated addresses: still read as addresses, must still match --
    def test_fullwidth_at_sign_is_caught(self):
        self.write("doc.md", "write to %s\n" % UNKNOWN.replace("@", "\uff20"))
        self.assertBlocked(run_gate(self.tmp, "--tree"), "UNALLOWLISTED")

    def test_zero_width_space_inside_address_is_caught(self):
        self.write("doc.md", "write to %s\n" % UNKNOWN.replace("@", "\u200b@"))
        self.assertBlocked(run_gate(self.tmp, "--tree"), "UNALLOWLISTED")

    def test_percent_encoded_at_sign_is_caught(self):
        self.write("doc.md", "mailto:%s\n" % UNKNOWN.replace("@", "%40"))
        self.assertBlocked(run_gate(self.tmp, "--tree"), "UNALLOWLISTED")

    # --- a file NAME is published too ------------------------------------
    def test_address_in_file_name_is_caught_staged(self):
        self.write("notes/%s.md" % UNKNOWN, "clean body\n")
        self.assertBlocked(run_gate(self.tmp), "UNALLOWLISTED")

    def test_address_in_file_name_is_caught_tree(self):
        self.write("notes/%s.md" % UNKNOWN, "clean body\n")
        self.assertBlocked(run_gate(self.tmp, "--tree"), "UNALLOWLISTED")

    # --- finding 1: non-UTF-8 is a failed measurement, not a clean file ---
    def test_non_utf8_file_is_reported_unscannable(self):
        # A cp1252 "ñ" (0xf1) is not valid UTF-8. Before the fix the file was
        # counted in `scanned` and skipped, hiding its address entirely.
        self.write("kit/sesión.md",
                   b"sesi\xf1n: " + UNKNOWN.encode("ascii") + b"\n")
        self.assertBlocked(run_gate(self.tmp, "--tree"), "UNSCANNABLE")

    def test_non_utf8_file_is_caught_in_staged_mode_too(self):
        self.write("kit/notes.md", b"\xff\xfe" + UNKNOWN.encode("utf-16-le"))
        self.assertBlocked(run_gate(self.tmp), "UNSCANNABLE")

    # --- finding 2: the allowlist must never override the deny list -------
    def test_denied_address_cannot_be_allowlisted_away(self):
        allow = self.tmp / ".githooks" / "allow-patterns.txt"
        allow.write_text(allow.read_text(encoding="utf-8") + DENIED + "\n",
                         encoding="utf-8")
        self.write("doc.md", "contact %s\n" % DENIED)
        self.assertBlocked(run_gate(self.tmp, "--tree"), "KNOWN-PRIVATE")

    def test_allowlist_file_itself_is_scanned_for_denied_addresses(self):
        # The allowlist is exempt only from the generic UNALLOWLISTED rule.
        self.write(".githooks/allow-patterns.txt",
                   "maintainer" + "@" + DOMAIN + "\n%s\n" % DENIED)
        self.assertBlocked(run_gate(self.tmp, "--tree"), "KNOWN-PRIVATE")

    def test_case_variant_allowlist_path_does_not_inherit_the_exemption(self):
        # `load()` opens the exact-cased `.githooks/allow-patterns.txt`. If the
        # deny-only exemption were case-folded, `.githooks/ALLOW-PATTERNS.TXT`
        # would be exempt from the generic rule while never being loaded as an
        # allowlist -- committable, with its addresses invisible. On a
        # case-sensitive filesystem (CI, any Linux contributor) that is a live
        # bypass; here it is exercised through the INDEX rather than the working
        # tree, so the assertion holds on case-insensitive APFS too.
        variant = ".githooks/ALLOW-PATTERNS.TXT"
        blob = subprocess.run(
            ["git", "hash-object", "-w", "--stdin"], cwd=str(self.tmp),
            input=("route to %s\n" % UNKNOWN).encode("utf-8"),
            check=True, capture_output=True).stdout.decode().strip()
        subprocess.run(
            ["git", "update-index", "--add", "--cacheinfo",
             "100644,%s,%s" % (blob, variant)],
            cwd=str(self.tmp), check=True, capture_output=True)
        r = run_gate(self.tmp)  # staged mode: reads the index, not the tree
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertIn(variant, r.stderr)

    def test_allowlist_file_does_not_flag_its_own_legitimate_entries(self):
        # ...and the suppression still works, or the gate is unusable.
        self.write("doc.md", "ok\n")
        r = run_gate(self.tmp, "--tree")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    # --- finding 3: the gate does not exempt its own source ---------------
    def test_address_planted_in_the_gates_own_source_is_caught(self):
        p = self.tmp / "bin" / "gate_scan.py"
        p.write_text(p.read_text(encoding="utf-8") + "\n# route to %s\n" % UNKNOWN,
                     encoding="utf-8")
        subprocess.run(["git", "add", "--", "bin/gate_scan.py"], cwd=str(self.tmp),
                       check=True, capture_output=True)
        self.assertBlocked(run_gate(self.tmp, "--tree"), "bin/gate_scan.py")

    # --- finding 4: --history refuses to certify an empty scan ------------
    def test_history_mode_refuses_zero_objects(self):
        r = run_gate(self.tmp, "--history")  # no commits exist yet
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertIn("GATE ERROR", r.stderr)

    def test_history_mode_catches_address_in_renamed_directory(self):
        self.write("%s/doc.md" % UNKNOWN, "clean body\n")
        self.git("commit", "-q", "--no-verify", "-m", "original directory")
        self.git("mv", "--", UNKNOWN, "notes")
        self.git("commit", "-q", "--no-verify", "-m", "rename directory")
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertIn("[redacted#", r.stderr)
        self.assertIn("(file name)", r.stderr)
        self.assertRedacted(r, UNKNOWN)

    def test_history_mode_catches_shared_blob_under_later_denied_name(self):
        # Same blob, two names: git's object dedup lists it once under the
        # FIRST name, so a later path that carries an address must still be
        # checked through the per-commit tree walk.
        self.write("notes.md", "identical clean body\n")
        self.git("commit", "-q", "--no-verify", "-m", "first name")
        self.write("%s.md" % UNKNOWN, "identical clean body\n")
        self.git("commit", "-q", "--no-verify", "-m", "same content, second name")
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertIn("[redacted#", r.stderr)
        self.assertRedacted(r, UNKNOWN)

    def test_history_mode_preserves_tabs_and_newlines_in_names(self):
        name = "notes\tarchive\n" + UNKNOWN
        self.write(name + "/doc.md", "clean body\n")
        self.git("commit", "-q", "--no-verify", "-m", "unusual path")
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertIn("[redacted#", r.stderr)
        self.assertRedacted(r, UNKNOWN)

    # --- refs can publish blobs, trees and annotated tag objects too ------
    def clean_commit(self):
        self.write("doc.md", "clean body\n")
        self.git("commit", "-q", "--no-verify", "-m", "clean message")
        return self.git("rev-parse", "HEAD").stdout.strip().decode("ascii")

    def test_history_mode_scans_lightweight_tag_blob(self):
        self.clean_commit()
        blob = self.git("hash-object", "-w", "--stdin",
                        input=DENIED.encode("ascii")).stdout.strip().decode("ascii")
        self.git("tag", "lw", blob)
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "KNOWN-PRIVATE")
        self.assertIn("refs/tags/lw", r.stderr)

    def test_history_mode_scans_direct_tree_ref_names(self):
        self.clean_commit()
        name = "notes\tarchive\n" + UNKNOWN
        self.write(name + "/doc.md", "clean body\n")
        tree = self.git("write-tree").stdout.strip().decode("ascii")
        self.git("update-ref", "refs/data/tree", tree)
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertIn("[redacted#", r.stderr)
        self.assertRedacted(r, UNKNOWN)

    def test_history_mode_scans_direct_tree_ref_blobs(self):
        self.clean_commit()
        self.write("notes/private.md", DENIED)
        tree = self.git("write-tree").stdout.strip().decode("ascii")
        self.git("update-ref", "refs/data/tree", tree)
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "KNOWN-PRIVATE")
        self.assertIn("notes/private.md", r.stderr)

    def test_history_mode_scans_annotated_tag_message(self):
        self.clean_commit()
        self.git("tag", "-a", "release", "-m", "route to " + DENIED)
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "KNOWN-PRIVATE")
        self.assertIn("tag message", r.stderr)

    def test_history_mode_scans_annotated_tag_tagger_email(self):
        self.clean_commit()
        self.git("-c", "user.email=" + DENIED,
                 "tag", "-a", "release", "-m", "clean message")
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "KNOWN-PRIVATE")
        self.assertIn("tag header", r.stderr)

    def test_history_mode_scans_outer_tag_in_chain(self):
        self.clean_commit()
        self.git("tag", "-a", "inner", "-m", "clean message")
        self.git("tag", "-a", "outer", "inner", "-m", "route to " + DENIED)
        # The inner tag must be reached by peeling, not by its own ref.
        self.git("tag", "-d", "inner")
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "KNOWN-PRIVATE")
        self.assertIn("tag message", r.stderr)

    def test_history_mode_scans_inner_tag_in_chain(self):
        self.clean_commit()
        self.git("tag", "-a", "inner", "-m", "route to " + DENIED)
        self.git("tag", "-a", "outer", "inner", "-m", "clean message")
        self.git("tag", "-d", "inner")
        self.assertBlocked(run_gate(self.tmp, "--history"), "KNOWN-PRIVATE")

    def test_history_mode_clean_annotated_tag_passes(self):
        self.clean_commit()
        self.git("tag", "-a", "release", "-m", "clean message")
        r = run_gate(self.tmp, "--history")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def raw_tag(self, message, encoding=None, tag_name=b"release", tagger=None,
                commit=None):
        """Publish raw tag bytes, including headers `git tag` cannot emit."""
        if commit is None:
            commit = self.clean_commit()
        if tagger is None:
            tagger = ("t <%s>" % GIT_EMAIL).encode("ascii")
        obj = (b"object " + commit.encode("ascii") + b"\ntype commit\ntag " + tag_name +
               b"\ntagger " + tagger + b" 1700000000 -0400\n")
        if encoding is not None:
            obj += b"encoding " + encoding + b"\n"
        obj += b"\n" + message
        sha = self.git("hash-object", "-t", "tag", "-w", "--literally",
                       "--stdin", input=obj).stdout.strip().decode("ascii")
        self.git("update-ref", "refs/tags/release", sha)

    def test_history_mode_scans_tag_name_header(self):
        # The name inside a tag object need not equal the ref publishing it.
        self.raw_tag(b"clean message\n", tag_name=DENIED.encode("ascii"))
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "KNOWN-PRIVATE")
        self.assertIn("tag header", r.stderr)

    def test_history_mode_scans_tag_message_after_nul(self):
        self.raw_tag(b"clean\x00 " + DENIED.encode("ascii") + b"\n")
        self.assertBlocked(run_gate(self.tmp, "--history"), "KNOWN-PRIVATE")

    def test_history_mode_non_utf8_tag_is_unscannable(self):
        self.raw_tag(b"caf\xe9\n")
        self.assertBlocked(run_gate(self.tmp, "--history"), "UNSCANNABLE")

    def test_history_mode_decodes_latin1_tag(self):
        self.raw_tag(("caf\u00e9 %s\n" % DENIED).encode("iso-8859-1"),
                     encoding=b"ISO-8859-1",
                     tagger=("Caf\u00e9 <%s>" % DENIED).encode("iso-8859-1"))
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "KNOWN-PRIVATE")
        self.assertIn("UNSCANNABLE", r.stderr)
        self.assertRegex(r.stderr, r"<tag message decoded> [0-9a-f]+:\d+  \[KNOWN-PRIVATE")
        self.assertRegex(r.stderr, r"<tag decoded> [0-9a-f]+:\d+  \[KNOWN-PRIVATE")

    def test_history_mode_unsafe_tag_encoding_is_unscannable(self):
        commit = self.clean_commit()
        for encoding, problem in ((b"UTF-7", "not ASCII-compatible"),
                                  (b"UTF-16LE", "not ASCII-compatible"),
                                  (b"X-NOT-A-CHARSET", "unknown tag encoding"),
                                  (b"UTF-8\x00", "unknown tag encoding")):
            with self.subTest(encoding=encoding):
                self.raw_tag(b"clean message\n", encoding=encoding, commit=commit)
                r = run_gate(self.tmp, "--history")
                self.assertBlocked(r, "UNSCANNABLE")
                self.assertIn(problem, r.stderr)
                self.assertNotIn("Traceback", r.stderr)

    def test_history_mode_peels_annotated_blob_and_tree_tags(self):
        self.clean_commit()
        blob = self.git("hash-object", "-w", "--stdin",
                        input=DENIED.encode("ascii")).stdout.strip().decode("ascii")
        self.git("tag", "-a", "blob", blob, "-m", "clean message")
        self.write("notes/" + UNKNOWN + "/doc.md", "clean body\n")
        tree = self.git("write-tree").stdout.strip().decode("ascii")
        self.git("tag", "-a", "tree", tree, "-m", "clean message")
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "KNOWN-PRIVATE")
        self.assertIn("refs/tags/blob", r.stderr)
        self.assertIn("notes/[redacted#", r.stderr)
        self.assertRedacted(r, UNKNOWN, DENIED)

    def test_history_mode_includes_commit_reachable_only_through_tag_chain(self):
        self.write("doc.md", DENIED)
        self.git("commit", "-q", "--no-verify", "-m", "route to " + UNKNOWN)
        self.git("tag", "-a", "inner", "-m", "clean message")
        self.git("tag", "-a", "outer", "inner", "-m", "clean message")
        self.git("tag", "-d", "inner")
        branch = self.git("symbolic-ref", "HEAD").stdout.strip().decode("ascii")
        self.git("update-ref", "-d", branch)
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "KNOWN-PRIVATE")
        self.assertIn("commit message", r.stderr)
        self.assertIn("UNALLOWLISTED", r.stderr)

    def test_history_mode_clean_blob_and_tree_refs_without_commits_pass(self):
        blob = self.git("hash-object", "-w", "--stdin",
                        input=b"clean body\n").stdout.strip().decode("ascii")
        self.git("tag", "lw", blob)
        self.write("notes/doc.md", "clean body\n")
        tree = self.git("write-tree").stdout.strip().decode("ascii")
        self.git("update-ref", "refs/data/tree", tree)
        r = run_gate(self.tmp, "--history")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_history_mode_preserves_non_utf8_ref_name(self):
        # Git ref names may contain arbitrary non-UTF-8 bytes. Parse the
        # for-each-ref output as bytes and preserve the complete name.
        self.clean_commit()
        blob = self.git("hash-object", "-w", "--stdin",
                        input=DENIED.encode("ascii")).stdout.strip().decode("ascii")
        # Packed refs also work on filesystems that reject non-UTF-8 file
        # names (a loose ref with this name cannot be written on macOS).
        (self.tmp / ".git" / "packed-refs").write_bytes(
            blob.encode("ascii") + b" refs/data/non-utf8-\xff\n")
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "KNOWN-PRIVATE")
        self.assertIn("UNSCANNABLE", r.stderr)
        self.assertNotIn("Traceback", r.stderr)

    def test_history_mode_does_not_load_allowlist_from_ref_tree(self):
        self.clean_commit()
        self.write(".githooks/allow-patterns.txt", UNKNOWN + "\n")
        self.write("private.md", UNKNOWN + "\n")
        tree = self.git("write-tree").stdout.strip().decode("ascii")
        self.git("update-ref", "refs/data/tree", tree)
        # Restore the approved policy before scanning the historical tree.
        (self.tmp / ".githooks" / "allow-patterns.txt").write_text(
            GIT_EMAIL + "\n", encoding="utf-8")
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertIn("private.md", r.stderr)

    # --- finding 5: path matching is case- and NFC-insensitive ------------
    def test_case_variant_withheld_basename_is_caught(self):
        # Lowercase "registry". The vault volume is case-insensitive APFS, so
        # mirroring this would overwrite the real registry — no undo.
        self.write("Trainer Pack (EN)/00 — Trainer registry (maintainer only).md", "x\n")
        self.assertBlocked(run_gate(self.tmp, "--tree"), "FORBIDDEN BASENAME")

    def test_case_variant_withheld_path_is_caught(self):
        self.write("Co-Facilitator Kit (EN)/00 — Design spec.md", "x\n")
        self.assertBlocked(run_gate(self.tmp, "--tree"), "FORBIDDEN PATH")

    def test_exact_case_withheld_basename_still_caught(self):
        self.write("Trainer Pack (EN)/" + REGISTRY, "x\n")
        self.assertBlocked(run_gate(self.tmp, "--tree"), "FORBIDDEN BASENAME")

    # --- finding 6: commit messages are scanned ---------------------------
    def test_commit_message_with_an_address_is_caught(self):
        msg = self.tmp / "COMMIT_EDITMSG"
        msg.write_text("fix routing for %s\n" % UNKNOWN, encoding="utf-8")
        self.assertBlocked(run_gate(self.tmp, "--message", str(msg)),
                           "UNALLOWLISTED")

    def test_clean_commit_message_passes(self):
        msg = self.tmp / "COMMIT_EDITMSG"
        msg.write_text("Add the ES edition diff table\n", encoding="utf-8")
        r = run_gate(self.tmp, "--message", str(msg))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_history_mode_scans_commit_messages(self):
        self.write("doc.md", "clean body\n")
        subprocess.run(["git", "commit", "-q", "--no-verify", "-m",
                        "route to %s" % UNKNOWN],
                       cwd=str(self.tmp), check=True, capture_output=True)
        self.assertBlocked(run_gate(self.tmp, "--history"), "commit message")

    def test_history_mode_catches_denied_address_after_record_separator(self):
        self.write("doc.md", "clean body\n")
        subprocess.run(["git", "commit", "-q", "--no-verify", "-F", "-"],
                       input=("ok\x01%s\n" % DENIED).encode("utf-8"),
                       cwd=str(self.tmp), check=True, capture_output=True)
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "KNOWN-PRIVATE")
        self.assertIn("commit message", r.stderr)
        self.assertIn(fp(DENIED), r.stderr)
        self.assertRedacted(r, DENIED)

    # --- whole commit objects: headers, NUL bytes, re-encoded messages ---
    def git(self, *args, **kw):
        return subprocess.run(["git", *args], cwd=str(self.tmp), check=True,
                              capture_output=True, **kw)

    def commit_message_bytes(self, message, *config):
        """Commit with a message given as raw bytes, optionally under git -c
        settings (e.g. i18n.commitEncoding)."""
        self.write("doc.md", "clean body\n")
        cfg = [a for c in config for a in ("-c", c)]
        # A fixed negative timezone: in UTF-7 a '+0000' (CI runs in UTC)
        # would open a shift sequence and make the whole commit undecodable.
        date = "1700000000 -0400"
        env = dict(os.environ, GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date)
        self.git(*cfg, "commit", "-q", "--no-verify", "-F", "-", input=message,
                 env=env)

    def test_history_mode_scans_commit_author_header(self):
        self.write("doc.md", "clean body\n")
        self.git("-c", "user.email=" + DENIED, "commit", "-q", "--no-verify",
                 "-m", "clean message")
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "KNOWN-PRIVATE")
        self.assertIn("commit header", r.stderr)

    def test_history_mode_catches_address_after_nul_in_message(self):
        # `git commit` refuses a NUL in a message, but a commit object can
        # carry one; git log's %B stops at it and hides what follows.
        self.write("doc.md", "clean body\n")
        tree = self.git("write-tree").stdout.strip().decode("ascii")
        ident = ("t <%s> 0 +0000" % GIT_EMAIL).encode("utf-8")
        obj = (b"tree " + tree.encode("ascii") + b"\n"
               b"author " + ident + b"\ncommitter " + ident + b"\n\n"
               b"ok\x00 " + DENIED.encode("utf-8") + b"\n")
        sha = self.git("hash-object", "-t", "commit", "-w", "--literally",
                       "--stdin", input=obj).stdout.strip().decode("ascii")
        self.git("update-ref", "HEAD", sha)
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "KNOWN-PRIVATE")
        self.assertIn("commit message", r.stderr)

    def test_history_mode_utf7_message_is_unscannable(self):
        # In UTF-7 '@' may be written '+AEA-': the raw bytes hold no address.
        # UTF-7 is not ASCII-compatible, so the commit cannot be measured.
        self.commit_message_bytes(
            ("ok %s\n" % DENIED.replace("@", "+AEA-")).encode("ascii"),
            "i18n.commitEncoding=UTF-7")
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "UNSCANNABLE")
        self.assertIn("not ASCII-compatible", r.stderr)

    def test_history_mode_utf16_message_is_unscannable(self):
        # A UTF-16 message interleaves NULs: no address in the raw bytes, and
        # the ASCII headers mean nothing decoded as UTF-16. Fail closed.
        self.raw_commit(("t <%s>" % GIT_EMAIL).encode("ascii"),
                        ("ok %s\n" % DENIED).encode("utf-16-le"), b"UTF-16LE")
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "UNSCANNABLE")
        self.assertIn("commit encoding 'utf-16-le' is not ASCII-compatible",
                      r.stderr)

    def test_history_mode_scans_latin1_message_decoded(self):
        # Raw Latin-1 bytes are not UTF-8 (UNSCANNABLE); the decoded message
        # must still be read, so the address itself is reported.
        self.commit_message_bytes(
            ("caf\u00e9 %s\n" % DENIED).encode("iso-8859-1"),
            "i18n.commitEncoding=ISO-8859-1")
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "KNOWN-PRIVATE")
        self.assertIn("UNSCANNABLE", r.stderr)
        # ...and found by decoding the message on its own, not only the object.
        self.assertRegex(r.stderr, r"<commit message decoded> [0-9a-f]+:\d+  \[KNOWN-PRIVATE")

    def test_history_mode_undecodable_encoding_is_unscannable(self):
        self.commit_message_bytes(b"clean message\n",
                                  "i18n.commitEncoding=X-NOT-A-CHARSET")
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "UNSCANNABLE")
        self.assertIn("[UNSCANNABLE — unknown commit encoding]", r.stderr)
        self.assertNotIn("X-NOT-A-CHARSET", r.stderr)

    def test_history_mode_encoding_header_does_not_echo_denied_address(self):
        self.raw_commit(("t <%s>" % GIT_EMAIL).encode("ascii"),
                        b"clean message\n", DENIED.encode("ascii"))
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "KNOWN-PRIVATE")
        self.assertNotIn(DENIED, r.stdout)
        self.assertNotIn(DENIED, r.stderr)
        self.assertIn("[UNSCANNABLE — unknown commit encoding]", r.stderr)

    def test_history_mode_encoding_header_with_nul_is_unscannable(self):
        self.raw_commit(("t <%s>" % GIT_EMAIL).encode("ascii"),
                        b"clean message\n", b"UTF-8\x00")
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "UNSCANNABLE")
        self.assertIn("[UNSCANNABLE — unknown commit encoding]", r.stderr)
        self.assertNotIn("Traceback", r.stdout + r.stderr)

    def raw_commit(self, author, message, encoding=None):
        """Write a commit object byte for byte (author ident given as raw
        bytes, so its encoding is ours to choose) and point HEAD at it. The
        timezone is negative on purpose: in UTF-7 a '+0000' would open a shift
        sequence."""
        self.write("doc.md", "clean body\n")
        tree = self.git("write-tree").stdout.strip()
        ident = ("t <%s> 1700000000 -0400" % GIT_EMAIL).encode("ascii")
        obj = (b"tree " + tree + b"\n"
               b"author " + author + b" 1700000000 -0400\n"
               b"committer " + ident + b"\n")
        if encoding:
            obj += b"encoding " + encoding + b"\n"
        obj += b"\n" + message
        sha = self.git("hash-object", "-t", "commit", "-w", "--literally",
                       "--stdin", input=obj).stdout.strip().decode("ascii")
        self.git("update-ref", "HEAD", sha)

    def test_history_mode_utf7_author_header_is_unscannable(self):
        # The `encoding` header governs the whole commit: an author email
        # written in UTF-7 holds no '@' in its raw bytes. Fail closed.
        hidden = DENIED.replace("@", "+AEA-")
        self.raw_commit(("t <%s>" % hidden).encode("ascii"),
                        b"clean message\n", b"UTF-7")
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "UNSCANNABLE")
        self.assertIn("not ASCII-compatible", r.stderr)

    def test_history_mode_decodes_latin1_author_header(self):
        # A Latin-1 author name makes the raw header undecodable as UTF-8;
        # the address beside it must still be read and reported.
        self.raw_commit(("Caf\u00e9 <%s>" % DENIED).encode("iso-8859-1"),
                        b"clean message\n", b"ISO-8859-1")
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "KNOWN-PRIVATE")
        self.assertIn("commit decoded", r.stderr)

    def test_history_mode_clean_commit_passes(self):
        self.commit_message_bytes(b"clean message\n")
        r = run_gate(self.tmp, "--history")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


    # --- GitHub no-reply identities: any contributor, headers only --------
    def commit_as(self, author, committer, message="clean message"):
        self.write("doc.md", "clean body %s\n" % message)
        env = dict(os.environ, GIT_AUTHOR_NAME="outside", GIT_AUTHOR_EMAIL=author,
                   GIT_COMMITTER_NAME="outside", GIT_COMMITTER_EMAIL=committer)
        self.git("commit", "-q", "--no-verify", "-m", message, env=env)

    def test_outside_contributor_noreply_identity_passes_history(self):
        # Not on the allowlist: any GitHub-issued no-reply identity is fine as
        # the author/committer, so outside contributors' PRs can go green.
        self.commit_as(OUTSIDE, OUTSIDE)
        self.commit_as(OUTSIDE, WEB_MERGE, "merged in the web UI")
        r = run_gate(self.tmp, "--history")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_outside_contributor_noreply_tagger_passes_history(self):
        self.clean_commit()
        self.git("-c", "user.email=" + OUTSIDE, "tag", "-a", "release",
                 "-m", "clean message")
        r = run_gate(self.tmp, "--history")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_noreply_identity_in_commit_message_is_still_caught(self):
        self.commit_as(OUTSIDE, OUTSIDE, "thanks to %s" % OUTSIDE)
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertIn("commit message", r.stderr)
        self.assertNotIn("commit header", r.stderr)
        self.assertRedacted(r, OUTSIDE)

    def test_noreply_identity_in_a_file_is_still_caught(self):
        self.write("doc.md", "write to %s\n" % OUTSIDE)
        self.assertBlocked(run_gate(self.tmp, "--tree"), "UNALLOWLISTED")

    def test_legacy_login_only_noreply_identity_passes_history(self):
        self.commit_as(LEGACY, LEGACY)
        self.clean_commit()
        self.git("-c", "user.email=" + LEGACY, "tag", "-a", "legacy",
                 "-m", "clean message")
        r = run_gate(self.tmp, "--history")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_legacy_noreply_in_message_or_file_is_still_caught(self):
        self.commit_as(LEGACY, LEGACY, "thanks to %s" % LEGACY)
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertIn("commit message", r.stderr)
        self.assertRedacted(r, LEGACY)
        self.write("doc.md", "write to %s\n" % LEGACY)
        self.assertBlocked(run_gate(self.tmp, "--tree"), "UNALLOWLISTED")

    def test_noreply_lookalikes_in_headers_are_caught(self):
        base = self.clean_commit()
        for fake in ("out.side" + "@" + NOREPLY_DOMAIN,                  # dot in login
                     "-outside" + "@" + NOREPLY_DOMAIN,                  # leading hyphen
                     "x" * 40 + "@" + NOREPLY_DOMAIN,                    # login too long
                     "98765+" + "@" + NOREPLY_DOMAIN,                    # id, no login
                     OUTSIDE + ".evil.test",                             # suffix
                     "outside" + "@" + "users-noreply.github.com",       # wrong host
                     "98765+outside" + "@" + "users.noreply.github.co"):  # typo
            with self.subTest(fake=fake):
                self.git("reset", "-q", "--hard", base)
                env = dict(os.environ, GIT_AUTHOR_EMAIL=fake,
                           GIT_COMMITTER_EMAIL=OUTSIDE)
                self.git("commit", "-q", "--no-verify", "--allow-empty",
                         "-m", "clean message", env=env)
                r = run_gate(self.tmp, "--history")
                self.assertBlocked(r, "UNALLOWLISTED")
                self.assertIn("commit header", r.stderr)
                self.assertRedacted(r, fake)

    # --- Co-authored-by trailers: users' no-reply forms, exact line only ---
    def test_noreply_coauthor_trailer_passes_history_and_message_hook(self):
        msg = ("clean message\n\nCo-authored-by: Outside One <%s>\n"
               "co-authored-by: Outside Two <%s>\n" % (OUTSIDE, LEGACY))
        self.commit_message_bytes(msg.encode("utf-8"))
        r = run_gate(self.tmp, "--history")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        f = self.tmp / "COMMIT_EDITMSG"
        f.write_text(msg, encoding="utf-8")
        r = run_gate(self.tmp, "--message", str(f))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_coauthor_trailer_lookalikes_are_caught(self):
        for line in ("Thanks Outside <%s>" % OUTSIDE,                 # not a trailer
                     "Co-authored-by: <%s>" % OUTSIDE,                 # no name
                     "Co-authored-by: Outside %s" % OUTSIDE,           # no brackets
                     "Co-authored-by: Outside <%s> extra" % OUTSIDE,   # trailing text
                     "Signed-off-by: Outside <%s>" % OUTSIDE,          # other trailer
                     "Co-authored-by: Outside <%s>" % WEB_MERGE,       # service address
                     "Co-authored-by: Outside <%s>" % UNKNOWN):        # not no-reply
            with self.subTest(line=line):
                f = self.tmp / "COMMIT_EDITMSG"
                f.write_text("clean message\n\n%s\n" % line, encoding="utf-8")
                r = run_gate(self.tmp, "--message", str(f))
                self.assertBlocked(r, "UNALLOWLISTED")
                self.assertRedacted(r, OUTSIDE, UNKNOWN)

    def test_denied_address_in_coauthor_trailer_is_never_excused(self):
        f = self.tmp / "COMMIT_EDITMSG"
        f.write_text("clean message\n\nCo-authored-by: X <%s>\n" % DENIED,
                     encoding="utf-8")
        self.assertBlocked(run_gate(self.tmp, "--message", str(f)), "KNOWN-PRIVATE")

    def test_noreply_coauthor_trailer_in_tag_message_is_caught(self):
        self.clean_commit()
        self.git("tag", "-a", "release", "-m",
                 "clean\n\nCo-authored-by: Outside <%s>" % OUTSIDE)
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertIn("tag message", r.stderr)

    # --- trailers count only in the message's final trailer block --------
    def assertMessage(self, msg, passes):
        """Judge `msg` as the commit-msg hook does and as --history does."""
        f = self.tmp / "COMMIT_EDITMSG"
        f.write_text(msg, encoding="utf-8")
        hook = run_gate(self.tmp, "--message", str(f))
        if not getattr(self, "_msg_base", None):
            self._msg_base = self.clean_commit()
        self.write("change.md", "a change to commit\n")
        self.commit_message_bytes(msg.encode("utf-8"))
        hist = run_gate(self.tmp, "--history")
        self.git("reset", "-q", "--hard", self._msg_base)
        for r in (hook, hist):
            if passes:
                self.assertEqual(r.returncode, 0, msg + r.stdout + r.stderr)
            else:
                self.assertBlocked(r, "UNALLOWLISTED")
                self.assertRedacted(r, OUTSIDE, SERVICE)

    def test_coauthor_trailer_in_final_block_passes(self):
        # Positive control: tightening must not break the attribution the
        # repo's own history uses. (Passes on the looser old gate by design.)
        for addr in (OUTSIDE, LEGACY, SERVICE):
            with self.subTest(addr=addr):
                self.assertMessage("subject\n\nWhy the change.\n\n"
                                   "Reviewed-by: Nobody Real\n"
                                   "Co-authored-by: Helper <%s>\n" % addr, True)

    def test_coauthor_line_mid_body_fails(self):
        for addr in (OUTSIDE, SERVICE):
            with self.subTest(addr=addr):
                line = "Co-authored-by: Helper <%s>" % addr
                self.assertMessage("subject\n\n%s\n\nMore text after it.\n"
                                   % line, False)
                # In the last paragraph, but beside a line that is not a trailer.
                self.assertMessage("subject\n\nThanks for the help!\n%s\n"
                                   % line, False)
                # The subject is never a trailer block.
                self.assertMessage("%s\n" % line, False)

    def test_service_address_in_mid_body_line_fails(self):
        self.assertMessage("subject\n\nAttribution goes to %s here.\n\n"
                           "Co-Authored-By: Claude <%s>\n" % (SERVICE, SERVICE),
                           False)

    def test_service_address_only_on_coauthor_trailer(self):
        # A final block of trailers, but the address is on another trailer.
        self.assertMessage("subject\n\nSigned-off-by: Claude <%s>\n" % SERVICE,
                           False)

    def test_service_address_in_a_file_fails(self):
        self.write("doc.md", "Co-Authored-By: Claude <%s>\n" % SERVICE)
        r = run_gate(self.tmp, "--tree")
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertRedacted(r, SERVICE)

    def test_service_address_in_tag_message_fails(self):
        self.clean_commit()
        self.git("tag", "-a", "release", "-m",
                 "clean\n\nCo-Authored-By: Claude <%s>" % SERVICE)
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertIn("tag message", r.stderr)

    def test_hook_ignores_the_comment_template_after_trailers(self):
        # The commit-msg hook runs before git strips the editor template.
        f = self.tmp / "COMMIT_EDITMSG"
        f.write_text("subject\n\nCo-authored-by: Helper <%s>\n\n"
                     "# Please enter the commit message for your changes.\n"
                     "#\n# ------------------------ >8 ------------------------\n"
                     "diff --git a/x b/x\n" % SERVICE, encoding="utf-8")
        r = run_gate(self.tmp, "--message", str(f))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        # ...but only the trailing template is dropped: a real line after
        # the trailer makes that paragraph something other than trailers.
        f.write_text("subject\n\nCo-authored-by: Helper <%s>\nnot a trailer\n"
                     "# Please enter the commit message for your changes.\n"
                     % SERVICE, encoding="utf-8")
        r = run_gate(self.tmp, "--message", str(f))
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertRedacted(r, SERVICE)

    def test_denied_address_in_header_is_never_excused(self):
        self.commit_as(DENIED, OUTSIDE)
        self.assertBlocked(run_gate(self.tmp, "--history"), "KNOWN-PRIVATE")

    # --- output never echoes an address -----------------------------------
    def test_tree_findings_are_redacted(self):
        self.write("notes/%s/doc.md" % UNKNOWN, "route to %s\n" % DENIED)
        r = run_gate(self.tmp, "--tree")
        self.assertBlocked(r, "KNOWN-PRIVATE")
        self.assertIn(fp(DENIED), r.stderr)
        self.assertIn("notes/[redacted#", r.stderr)
        self.assertIn("/doc.md", r.stderr)
        self.assertRedacted(r, UNKNOWN, DENIED)

    def test_obfuscated_address_in_file_name_is_redacted(self):
        self.write("notes/%s.md" % UNKNOWN.replace("@", "\uff20"), "clean\n")
        r = run_gate(self.tmp, "--tree")
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertNotIn(UNKNOWN.replace("@", "\uff20"), r.stderr)
        self.assertRedacted(r, UNKNOWN)

    # --- PR-controlled path text cannot forge CI log commands -------------
    def stage_blob(self, path, text):
        """Index a path the filesystem may refuse (newline, CR, leading ':')."""
        blob = self.git("hash-object", "-w", "--stdin",
                        input=text.encode("utf-8")).stdout.strip().decode()
        self.git("update-index", "--add", "--cacheinfo",
                 "100644,%s,%s" % (blob, path))

    def assertNoLogCommand(self, r):
        """GitHub Actions reads a line starting (after whitespace) with `::`
        as a workflow command, and older runners the legacy `##[` anywhere in
        a line. No output line may hold either sequence, anywhere."""
        out = r.stdout + r.stderr
        self.assertNotIn("\r", out)
        for line in out.splitlines():
            self.assertNotIn("::", line, "workflow command sequence: %r" % line)
            self.assertNotIn("##", line, "legacy command sequence: %r" % line)
            self.assertFalse(line.lstrip().startswith((":", "#")),
                             "output line could start a command: %r" % line)

    def test_newline_in_path_cannot_start_a_workflow_command_tree(self):
        self.stage_blob("notes/a\n::error title=x::spoofed.md",
                        "route to %s\n" % UNKNOWN)
        r = run_gate(self.tmp, "--tree")
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertNoLogCommand(r)
        # The escape is visible, so the file can still be found.
        self.assertIn("notes/a\\x0a\\x3a\\x3aerror title=x\\x3a\\x3aspoofed.md:1",
                      r.stderr)
        self.assertRedacted(r, UNKNOWN)

    def test_path_starting_with_command_prefix_is_escaped(self):
        self.stage_blob("::error::spoofed.md", "route to %s\n" % UNKNOWN)
        self.stage_blob("##[error]spoofed.md", "route to %s\n" % UNKNOWN)
        r = run_gate(self.tmp, "--tree")
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertNoLogCommand(r)
        self.assertIn("\\x3a\\x3aerror\\x3a\\x3aspoofed.md:1", r.stderr)
        self.assertIn("\\x23\\x23[error]spoofed.md:1", r.stderr)

    def test_control_characters_in_historical_path_are_escaped(self):
        self.stage_blob("a\r::warning::b ::notice::c.md",
                        "route to %s\n" % UNKNOWN)
        self.git("commit", "-q", "--no-verify", "-m", "odd path")
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertNoLogCommand(r)
        self.assertIn("a\\x0d\\x3a\\x3awarning\\x3a\\x3ab\\u2028"
                      "\\x3a\\x3anotice\\x3a\\x3ac.md", r.stderr)
        self.assertRedacted(r, UNKNOWN)

    def test_embedded_command_sequences_in_path_are_neutralised(self):
        # Not at the start of the line: GitHub's legacy `##[` parser matched
        # anywhere, and a name ending in `:` meets the `:line` printed after it.
        for name in ("notes/x ##[error]spoofed.md", "notes/x ::error::y.md",
                     "notes/x:", "notes/x#", "notes/a#[b ##c::d"):
            self.stage_blob(name, "route to %s\n" % UNKNOWN)
        for args in (("--tree",), ()):
            with self.subTest(args=args):
                r = run_gate(self.tmp, *args)
                self.assertBlocked(r, "UNALLOWLISTED")
                self.assertNoLogCommand(r)
                self.assertIn("notes/x \\x23\\x23[error]spoofed.md:1", r.stderr)
                self.assertIn("notes/x\\x3a:1", r.stderr)
                self.assertRedacted(r, UNKNOWN)

    # --- CI mode: names a pull request controls are never printed ---------
    def plant_hostile_names(self):
        names = ["notes/%s ##[error]x.md" % PRIVATE_WORD,
                 "notes/a\n::error::%s.md" % PRIVATE_WORD,
                 "notes/%s.md" % UNKNOWN]
        for name in names:
            self.stage_blob(name, "route to %s\n" % UNKNOWN)
        return names

    def assertOpaque(self, r, names):
        out = r.stdout + r.stderr
        self.assertNoLogCommand(r)
        self.assertRedacted(r, UNKNOWN)
        for word in (PRIVATE_WORD, "notes/", "spoofed", "error]"):
            self.assertNotIn(word, out)
        for name in names:
            self.assertIn(pid(name), r.stderr)

    def test_ci_mode_prints_path_ids_not_names_tree(self):
        names = self.plant_hostile_names()
        for kw in ({"ci": True}, {}):
            args = ("--tree",) if kw else ("--tree", "--ci")
            with self.subTest(args=args, **kw):
                r = run_gate(self.tmp, *args, **kw)
                self.assertBlocked(r, "UNALLOWLISTED")
                self.assertOpaque(r, names)
                self.assertIn("3 file or ref name(s)", r.stderr)
                self.assertIn("not printed in CI", r.stderr)

    def test_ci_mode_prints_path_ids_not_names_history(self):
        names = self.plant_hostile_names()
        self.git("commit", "-q", "--no-verify", "-m", "route to %s" % UNKNOWN)
        blob = self.git("hash-object", "-w", "--stdin",
                        input=("route to %s\n" % UNKNOWN).encode("ascii")
                        ).stdout.strip().decode("ascii")
        ref = "refs/data/%s" % PRIVATE_WORD
        self.git("update-ref", ref, blob)
        r = run_gate(self.tmp, "--history", ci=True)
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertOpaque(r, names)
        self.assertNotIn("refs/", r.stdout + r.stderr)
        self.assertIn(pid(ref), r.stderr)
        # Labels the gate builds itself (object kind + SHA) stay readable.
        self.assertIn("<commit message> ", r.stderr)

    def test_local_finding_carries_the_same_path_id_as_ci(self):
        names = self.plant_hostile_names()
        r = run_gate(self.tmp, "--tree")
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertNoLogCommand(r)
        for name in names:
            self.assertIn(pid(name), r.stderr)
        self.assertIn(PRIVATE_WORD, r.stderr)  # locally the name is readable

    # --- git's own error text never reaches a CI log -----------------------
    def test_git_failure_message_is_fixed_in_ci(self):
        self.write("doc.md", "clean\n")
        bindir = Path(tempfile.mkdtemp(prefix="gatefakegit-"))
        self.addCleanup(shutil.rmtree, bindir, True)
        stderr = "fatal: bad path '%s'\n::error::forged ##[error]x" % PRIVATE_WORD
        path = fake_git(bindir, "ls-files", stderr)
        r = run_gate(self.tmp, "--tree", ci=True, path=path)
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertIn("GATE ERROR: git ls-files failed (exit 128)", r.stderr)
        self.assertNotIn(PRIVATE_WORD, r.stdout + r.stderr)
        self.assertNotIn("forged", r.stdout + r.stderr)
        self.assertNoLogCommand(r)

    def test_git_failure_message_is_log_safe_locally(self):
        self.write("doc.md", "clean\n")
        bindir = Path(tempfile.mkdtemp(prefix="gatefakegit-"))
        self.addCleanup(shutil.rmtree, bindir, True)
        stderr = "fatal: bad path '%s'\n::error::forged ##[error]x" % PRIVATE_WORD
        path = fake_git(bindir, "rev-list", stderr)
        r = run_gate(self.tmp, "--history", path=path)
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertIn(PRIVATE_WORD, r.stderr)  # local: git's reason is shown
        self.assertNoLogCommand(r)

    # --- tree mode reads tracked blobs by mode ----------------------------
    def test_tree_mode_does_not_follow_symlinks(self):
        outside = Path(tempfile.mkdtemp(prefix="gateoutside-"))
        self.addCleanup(shutil.rmtree, outside, True)
        (outside / "secret.md").write_text("route to %s\n" % DENIED,
                                           encoding="utf-8")
        (self.tmp / "link.md").symlink_to(outside / "secret.md")
        self.git("add", "--", "link.md")
        r = run_gate(self.tmp, "--tree")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_tree_mode_scans_symlink_target_text(self):
        (self.tmp / "link.md").symlink_to("../%s/doc.md" % UNKNOWN)
        self.git("add", "--", "link.md")
        r = run_gate(self.tmp, "--tree")
        self.assertBlocked(r, "UNALLOWLISTED")
        self.assertIn("link.md:1", r.stderr)

    def test_tree_mode_scans_index_not_working_file(self):
        self.write("doc.md", "route to %s\n" % DENIED)
        (self.tmp / "doc.md").write_text("clean now\n", encoding="utf-8")
        self.assertBlocked(run_gate(self.tmp, "--tree"), "KNOWN-PRIVATE")

    def test_tree_mode_submodule_is_unscannable(self):
        self.write("doc.md", "clean\n")
        self.git("update-index", "--add", "--cacheinfo",
                 "160000,%s,vendored" % ("a" * 40))
        self.assertBlocked(run_gate(self.tmp, "--tree"), "UNSCANNABLE")

    def test_history_mode_reports_historical_submodule_unscannable(self):
        # A gitlink that existed in an earlier commit: --tree no longer sees
        # it, --history must give it the same verdict --tree would have.
        self.write("doc.md", "clean\n")
        self.git("update-index", "--add", "--cacheinfo",
                 "160000,%s,vendored" % ("a" * 40))
        self.git("commit", "-q", "--no-verify", "-m", "add a submodule")
        self.git("rm", "-q", "--cached", "vendored")
        self.git("commit", "-q", "--no-verify", "-m", "drop the submodule")
        self.assertEqual(run_gate(self.tmp, "--tree").returncode, 0)
        r = run_gate(self.tmp, "--history")
        self.assertBlocked(r, "UNSCANNABLE — not a regular file")
        self.assertIn("vendored", r.stderr)

    def test_shared_blob_is_reported_under_every_path(self):
        # Blob scans are memoised by SHA; each path must still be reported.
        self.write("a.md", "route to %s\n" % DENIED)
        self.write("b.md", "route to %s\n" % DENIED)
        r = run_gate(self.tmp, "--tree")
        self.assertBlocked(r, "KNOWN-PRIVATE")
        self.assertIn("a.md:1", r.stderr)
        self.assertIn("b.md:1", r.stderr)

    def test_withheld_basename_pattern_covers_variants(self):
        self.write("kit/00 — Trainer Registry.md", "x\n")
        self.assertBlocked(run_gate(self.tmp, "--tree"), "FORBIDDEN BASENAME")

if __name__ == "__main__":
    unittest.main()
