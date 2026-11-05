import re
import runpy
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GATE = runpy.run_path(str(ROOT / "bin" / "gate_scan.py"))


class TestGateMatching(unittest.TestCase):
    def test_scan_blob_without_at_sign_is_linear(self):
        # Bound the child process too: the old matcher takes minutes on this
        # input, so a regression must fail without stalling the whole suite.
        code = """
import runpy
import time
gate = runpy.run_path('bin/gate_scan.py')
data = b'a' * (200 * 1024)
findings = []
start = time.perf_counter()
gate['scan_blob'](data, 'long.txt', set(), [], findings)
elapsed = time.perf_counter() - start
assert not findings, findings
print(elapsed)
"""
        try:
            r = subprocess.run([sys.executable, "-c", code], cwd=str(ROOT),
                               capture_output=True, text=True, timeout=2)
        except subprocess.TimeoutExpired:
            self.fail("scan_blob on 200 KB without '@' did not finish within 2 seconds")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertLess(float(r.stdout), 0.5)

    def test_scan_blob_pathological_at_runs_are_bounded(self):
        # '@'-dense inputs that make a backtracking address regex retry from
        # every start index must still finish in bounded time.
        code = """
import runpy
import time
gate = runpy.run_path('bin/gate_scan.py')
cases = [b'@' * (200 * 1024), b'a@' * (100 * 1024), (b'a.' * 1000 + b'@') * 100, b'a' * (100 * 1024) + b'@' + b'b' * (100 * 1024)]
worst = 0.0
for data in cases:
    findings = []
    start = time.perf_counter()
    gate['scan_blob'](data, 'p.txt', set(), [], findings)
    worst = max(worst, time.perf_counter() - start)
print(worst)
"""
        try:
            r = subprocess.run([sys.executable, "-c", code], cwd=str(ROOT),
                               capture_output=True, text=True, timeout=5)
        except subprocess.TimeoutExpired:
            self.fail("scan_blob on '@'-dense input did not finish within 5 seconds")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertLess(float(r.stdout), 1.0)

    def test_address_matches_preserve_existing_spans(self):
        self.assertTrue(callable(GATE.get("address_matches")),
                        "gate must expose the linear address matcher")
        legacy = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
        for local in ("a", ".lead+tag%", "a_b-c", "a..b", "!prefix", "éname"):
            for domain in ("example.test", "sub.example.test", "bad.t",
                           "-odd..test", "a.test123", "a.étest"):
                text = "(%s%s%s), next %s%sother.test!" % (local, "@", domain, local, "@")
                with self.subTest(local=local, domain=domain):
                    expected = [(m.span(), m.group()) for m in legacy.finditer(text)]
                    actual = [(m.span(), m.group()) for m in GATE["address_matches"](text)]
                    self.assertEqual(actual, expected)

        # '+' ends the domain but can begin the next local part. A fixed
        # lookbehind must not hide that second address after the first match.
        domain = "example-invalid" + ".test"
        first = "first" + "@" + domain
        second = "+second" + "@" + domain
        text = first + second
        expected = [(m.span(), m.group()) for m in legacy.finditer(text)]
        actual = [(m.span(), m.group()) for m in GATE["address_matches"](text)]
        self.assertEqual(actual, expected)
        findings = []
        GATE["scan_blob"](text.encode("utf-8"), "doc.md", set(), [], findings)
        self.assertEqual(len(findings), 2, findings)


if __name__ == "__main__":
    unittest.main()
