#!/usr/bin/env python3
"""Private-data gate for aiac-facilitator-pack.

Scans STAGED CONTENT (what is being committed), never the working tree.
Exit codes:  0 = clean   1 = leak found   3 = gate could not run (FAIL LOUD)

Modes:
  (none)      staged blobs, for the pre-commit hook
  --message F scan a commit message file, for the commit-msg hook
  --tree      every tracked path, read from the WORKING TREE, not from the
              blob at HEAD. Correct in CI, where the checkout is clean and
              there is no index. Run locally on a dirty tree it measures your
              uncommitted edits, which is a different question than "is HEAD
              clean" -- do not read a local --tree pass as a statement about
              what is committed.
  --history   every object reachable from every ref, plus every commit message

Four design choices, each answering a way this gate could have been useless:

1. NUL-separated paths, never a shell pipeline. Every path here contains a
   space and most contain U+2014; `--name-only | xargs grep` word-splits them,
   finds nothing, and exits 0 -- indistinguishable from clean.

2. The deny list holds SHA-256 hashes, not addresses. A plaintext deny list
   of real addresses, committed to the repo, IS the leak it exists to prevent.

3. Detection is ALLOWLIST-anchored. The trainer roster is designed to grow,
   so a fixed deny list goes stale the moment a fifth trainer registers.
   Any address that is not explicitly permitted fails, known or not.
   BUT the allowlist never overrides the deny list: a deny-hash match fails
   unconditionally. An address on both lists is a mistake, and the safe
   resolution of a mistake is "block".

4. A failed measurement is never a pass. Undecodable bytes, an empty object
   set, a missing pattern file -- each is loud, because a gate that scans
   nothing and prints "clean" is the failure mode this file exists to prevent.
"""
import hashlib
import html
import re
import subprocess
import sys
import unicodedata
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOKS = ROOT / ".githooks"
ADDR_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# Built at runtime so this source file contains no address literal.
CANARY = "canary.probe" + "@" + "example-invalid" + ".test"
# allow-patterns.txt necessarily names every permitted address, so the generic
# UNALLOWLISTED rule would flag its own legitimate entries. It is NOT exempt
# from content scanning: deny-hash matches inside it still fail. Nothing else
# is on this list -- in particular this file is not, so an address planted in
# the gate's own source is caught like any other.
#
# Matched EXACTLY, not case-folded, and that asymmetry with check_path() is
# deliberate. load() opens the exact-cased real file; if the exemption folded,
# `.githooks/ALLOW-PATTERNS.TXT` would inherit it on a case-sensitive
# filesystem (CI, any Linux contributor) while never being loaded as an
# allowlist -- a committable file whose unallowlisted addresses are invisible.
# The exemption must apply to precisely the one file load() actually reads.
DENY_ONLY_CONTENT = {".githooks/allow-patterns.txt"}
COMMIT_MSG_PATH = "<commit message>"


def die(msg):
    print(f"GATE ERROR: {msg}", file=sys.stderr)
    print("Refusing to certify this commit as clean.", file=sys.stderr)
    sys.exit(3)


# Characters that render as nothing but split a regex match: an address with a
# zero-width space inside reads as one address and matches as none. Written as
# escapes so this source file carries no invisible character itself.
INVISIBLE_RE = re.compile("[\u00ad\u200b-\u200f\u2060-\u2064\ufeff]")


def deobfuscate(text):
    """Fold the encodings under which an address still READS as an address but
    no longer MATCHES as one: NFKC (full-width \uff20 and letters), invisible
    characters, and percent-encoding (%40). Addresses assembled at runtime
    from string fragments are beyond any text scan; maintainer review is the
    backstop for those."""
    t = unicodedata.normalize("NFKC", text)
    t = INVISIBLE_RE.sub("", t)
    return urllib.parse.unquote(t)


def norm(s):
    """Fold a path for comparison: NFC (macOS/Linux disagree on U+2014
    decomposition) then casefold (the vault volume is case-insensitive APFS,
    so a case variant of a withheld filename overwrites the real one)."""
    return unicodedata.normalize("NFC", s).casefold()


def load(name, required=True):
    p = HOOKS / name
    if not p.is_file():
        if required:
            die(f"missing pattern file {p}")
        return []
    vals = [l.strip() for l in p.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.strip().startswith("#")]
    if required and not vals:
        die(f"{p} contains zero entries — 'no patterns' is not 'clean'")
    return vals


def h(addr):
    return hashlib.sha256(addr.lower().strip().encode()).hexdigest()


def mask(addr):
    local, _, dom = addr.partition("@")
    return f"{local[:3]}***@{dom}"


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True)
    if r.returncode != 0:
        die(f"git {' '.join(args)} failed: {r.stderr.decode('utf-8','replace')[:200]}")
    return r.stdout


def self_test(deny_hashes):
    """Prove every matcher fires on a known positive before trusting a zero."""
    if not ADDR_RE.search(f"see {CANARY} now"):
        die("self-test FAILED — address regex did not fire")
    if h(CANARY) == h(CANARY + "x"):
        die("self-test FAILED — hasher is not discriminating")
    if h(CANARY) == h(CANARY.replace("canary", "canery")):
        die("self-test FAILED — hasher collision")
    entity = "canary.probe" + "&#64;" + "example-invalid" + ".test"
    if html.unescape(entity) != CANARY:
        die("self-test FAILED — entity decoder did not decode")
    for hidden in (CANARY.replace("@", "\uff20"),
                   CANARY.replace("@", "\u200b@"),
                   CANARY.replace("@", "%40")):
        if not ADDR_RE.search(deobfuscate(hidden)):
            die("self-test FAILED — deobfuscation missed %r" % hidden)
    if norm("A — B.MD") != norm("a — b.md"):
        die("self-test FAILED — path folding is not case/NFC insensitive")


def scan_blob(data, path, deny_hashes, allow, findings):
    """Content scan. A deny-hash match is unconditional; the allowlist can
    only suppress the generic UNALLOWLISTED rule, never a known address."""
    deny_only = path in DENY_ONLY_CONTENT
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        # A file we cannot decode is a FAILED MEASUREMENT, not a clean file:
        # deny hashes, allowlist and the generic rule all silently miss it.
        findings.append((path, 0, "UNSCANNABLE — not valid UTF-8"))
        return
    allow_l = {a.lower() for a in allow}
    seen = set()
    unescaped = html.unescape(text)
    for variant in (text, unescaped, deobfuscate(unescaped)):
        for m in ADDR_RE.finditer(variant):
            a = m.group(0)
            known = h(a) in deny_hashes
            if not known and (deny_only or a.lower() in allow_l):
                continue
            line = variant.count("\n", 0, m.start()) + 1
            why = "KNOWN-PRIVATE" if known else "UNALLOWLISTED"
            key = (path, line, why, a.lower())
            if key in seen:
                continue
            seen.add(key)
            findings.append((path, line, f"{why} {mask(a)}"))


def check_path(path, bad_base, bad_path):
    """Case-folded, NFC-normalized path check. Returns a reason or None."""
    base = path.rsplit("/", 1)[-1]
    if norm(base) in bad_base:
        return "FORBIDDEN BASENAME"
    if norm(path) in bad_path:
        return "FORBIDDEN PATH"
    return None


def scan_name(path, deny_hashes, allow, findings):
    """A file NAME is published as surely as its contents: a file named after
    an address would ship it without any content scan ever reading it."""
    scan_blob(path.encode("utf-8", "surrogateescape"), f"{path} (file name)",
              deny_hashes, allow, findings)


def commit_messages():
    """(sha, message) for every commit reachable from every ref. \\x01 records,
    \\x02 field separator -- neither can appear in a commit message."""
    out = git("log", "--all", "--format=%x01%H%x02%B").decode("utf-8", "replace")
    for rec in out.split("\x01"):
        if not rec.strip():
            continue
        sha, _, body = rec.partition("\x02")
        yield sha.strip(), body


def main():
    argv = sys.argv[1:]
    history = "--history" in argv
    tree = "--tree" in argv
    msg_file = None
    if "--message" in argv:
        i = argv.index("--message")
        if i + 1 >= len(argv):
            die("--message requires a path to the commit message file")
        msg_file = Path(argv[i + 1])

    deny_hashes = set(load("deny-hashes.txt"))
    allow = load("allow-patterns.txt", required=False)
    bad_base = {norm(b) for b in load("forbidden-basenames.txt", required=False)}
    bad_path = {norm(p) for p in load("forbidden-paths.txt", required=False)}
    self_test(deny_hashes)

    findings, scanned = [], 0
    if msg_file is not None:
        if not msg_file.is_file():
            die(f"commit message file not found: {msg_file}")
        scanned = 1
        scan_blob(msg_file.read_bytes(), COMMIT_MSG_PATH, deny_hashes, allow, findings)
    elif history:
        objects = git("rev-list", "--objects", "--all").decode("utf-8", "replace").splitlines()
        if not objects:
            die("rev-list returned no objects -- refusing to certify an empty history scan")
        for line in objects:
            sha, _, name = line.partition(" ")
            if not name:
                continue
            scanned += 1
            why = check_path(name, bad_base, bad_path)
            if why:
                findings.append((name, 0, "FORBIDDEN IN HISTORY"))
            scan_name(name, deny_hashes, allow, findings)
            scan_blob(git("cat-file", "-p", sha), name, deny_hashes, allow, findings)
        # Commit MESSAGES carry no name in rev-list --objects and would
        # otherwise never be read. Git history is permanent; so is a leak in it.
        msgs = list(commit_messages())
        if not msgs:
            die("git log --all returned no commits -- refusing to certify an empty scan")
        for sha, body in msgs:
            scanned += 1
            scan_blob(body.encode("utf-8"), f"{COMMIT_MSG_PATH} {sha[:12]}",
                      deny_hashes, allow, findings)
    elif tree:
        # CI has no index. Scan every tracked file, read from the working tree.
        paths = [p for p in git("ls-files", "-z").split(b"\0") if p]
        if not paths:
            die("git ls-files returned no paths -- refusing to certify an empty scan")
        for raw in paths:
            path = raw.decode("utf-8", "surrogateescape")
            scanned += 1
            why = check_path(path, bad_base, bad_path)
            if why:
                findings.append((path, 0, why))
                continue
            scan_name(path, deny_hashes, allow, findings)
            f = ROOT / path
            if not f.exists():
                continue  # deleted in a dirty local tree; CI checkouts are clean
            if not f.is_file():
                # A submodule or a directory where a file is tracked: nothing
                # was read, so nothing may be certified.
                findings.append((path, 0, "UNSCANNABLE — not a regular file"))
                continue
            scan_blob(f.read_bytes(), path, deny_hashes, allow, findings)
    else:
        for raw in [p for p in git("diff", "--cached", "-z", "--name-only",
                                   "--diff-filter=ACMR").split(b"\0") if p]:
            path = raw.decode("utf-8", "surrogateescape")
            scanned += 1
            why = check_path(path, bad_base, bad_path)
            if why:
                findings.append((path, 0, why))
                continue
            scan_name(path, deny_hashes, allow, findings)
            scan_blob(git("show", f":{path}"), path, deny_hashes, allow, findings)

    if findings:
        print("BLOCKED — private data in the commit:", file=sys.stderr)
        for path, line, why in sorted(set(findings)):
            print(f"  {path}{f':{line}' if line else ''}  [{why}]", file=sys.stderr)
        sys.exit(1)

    mode = ("message" if msg_file is not None else
            "history" if history else "tree" if tree else "staged")
    print("gate: clean (%d objects scanned, %s; %d hashes loaded, "
          "matchers self-tested)" % (scanned, mode, len(deny_hashes)))
    sys.exit(0)


if __name__ == "__main__":
    main()
