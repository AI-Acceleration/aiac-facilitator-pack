import hashlib, re, subprocess, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def gate(*args):
    return subprocess.run(
        [sys.executable, str(ROOT / "bin" / "gate_scan.py")] + list(args),
        capture_output=True, text=True, cwd=str(ROOT))


class TestGateTreeMode(unittest.TestCase):
    def test_tree_mode_runs_and_reports_a_count(self):
        r = gate("--tree")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("tree", r.stdout)

    def test_tree_mode_scans_more_than_zero_objects(self):
        # A gate that scans nothing and prints "clean" is the failure mode
        # this whole file exists to prevent.
        r = gate("--tree")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        m = re.search(r"\((\d+) objects scanned", r.stdout)
        self.assertIsNotNone(m, "gate did not report a scanned count: %r" % r.stdout)
        self.assertGreater(int(m.group(1)), 0, "gate reported scanning zero objects")

    def test_deny_hashes_are_hashes_not_addresses(self):
        p = ROOT / ".githooks" / "deny-hashes.txt"
        body = p.read_text(encoding="utf-8")
        self.assertNotIn("@", body, "deny list must never contain a plaintext address")
        vals = [l.strip() for l in body.splitlines()
                if l.strip() and not l.startswith("#")]
        self.assertTrue(vals, "deny list must not be empty")
        for v in vals:
            self.assertEqual(len(v), 64, "expected sha256 hex, got %r" % v)
            int(v, 16)  # raises if not hex


if __name__ == "__main__":
    unittest.main()
