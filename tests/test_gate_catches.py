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
REGISTRY = "00 — Trainer Registry (ALBERT ONLY).md"
GIT_EMAIL = "t" + "@" + DOMAIN  # fragments: this file is itself scanned by the gate


def run_gate(sandbox, *args):
    return subprocess.run(
        [sys.executable, str(sandbox / "bin" / "gate_scan.py")] + list(args),
        capture_output=True, text=True, cwd=str(sandbox))


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

    # --- finding 5: path matching is case- and NFC-insensitive ------------
    def test_case_variant_withheld_basename_is_caught(self):
        # Lowercase "registry". The vault volume is case-insensitive APFS, so
        # mirroring this would overwrite the real registry — no undo.
        self.write("Trainer Pack (EN)/00 — Trainer registry (ALBERT ONLY).md", "x\n")
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


if __name__ == "__main__":
    unittest.main()
