#!/usr/bin/env python3
"""Private-data gate for aiac-facilitator-pack.

Scans STAGED CONTENT (what is being committed), never the working tree.
Exit codes:  0 = clean   1 = leak found   3 = gate could not run (FAIL LOUD)

Modes:
  (none)      staged blobs, for the pre-commit hook
  --message F scan a commit message file, for the commit-msg hook
  --tree      every tracked path, read as the blob in the INDEX by its git
              mode (symlinks scanned as link text, never followed; submodules
              reported UNSCANNABLE). In CI the index equals the checkout.
              Locally, unstaged edits are not read: stage them first.
  --history   every object reachable from every ref, including commit and tag
              headers and messages (raw and, if re-encoded, decoded). A GitHub
              no-reply address is accepted only as the identity in an author,
              committer or tagger header, or (users' no-reply forms only) on an
              exact `Co-authored-by: Name <address>` line of a commit message.
              Historical submodule entries are reported UNSCANNABLE, as in
              --tree.

Findings never print an address: addresses are shown as `address#<8 hex>`
(prefix of the deny-list hash) and path components holding one are redacted.

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
import codecs
import fnmatch
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
LOCAL_PART_CHARS = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._%+-")
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
# GitHub-issued no-reply identities. A user's address comes in two forms:
# `<id>+<login>@users.noreply.github.com` (accounts since 2017) and the legacy
# `<login>@users.noreply.github.com` (older accounts still show it under
# Settings > Emails > "Keep my email addresses private"). The third form is
# the committer GitHub stamps on web-UI merges. They route to no one, so any
# contributor may commit with one. Allowed ONLY as the identity in a commit or
# tag header (see github_identity) or, users' forms only, on an exact
# Co-authored-by trailer line (see github_coauthor); written anywhere else
# they are ordinary addresses. A login is 1-39 letters, digits and hyphens,
# never starting with a hyphen.
GITHUB_USER_NOREPLY_RE = re.compile(
    r"(?:\d+\+)?[A-Za-z0-9][A-Za-z0-9-]{0,38}@users\.noreply\.github\.com",
    re.IGNORECASE)
GITHUB_NOREPLY_RE = re.compile(
    GITHUB_USER_NOREPLY_RE.pattern + r"|noreply@github\.com", re.IGNORECASE)
IDENTITY_HEADERS = ("author ", "committer ", "tagger ")
# The one trailer form in which a co-author's no-reply address may appear in a
# commit message: the whole line, `Co-authored-by: Name <address>`.
COAUTHOR_LINE_RE = re.compile(
    r"co-authored-by:[ \t]+[^<>\n]*[^<>\s][ \t]+<([^<>\s]+)>[ \t]*\r?",
    re.IGNORECASE)


def die(msg):
    print(f"GATE ERROR: {log_safe(msg)}", file=sys.stderr)
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


def fingerprint(addr):
    """How a finding names an address in output. CI logs are public, so the
    gate never prints an address, not even masked (a masked address still
    shows its domain). The 8-hex prefix of the deny-list hash tells findings
    apart and lets a maintainer confirm a suspected address locally."""
    return f"address#{h(addr)[:8]}"


# Categories whose characters must never reach a log line as themselves:
# controls (newline, CR, ESC, ...), format characters (bidi overrides,
# zero-width), lone surrogates (undecodable bytes carried by
# surrogateescape) and line/paragraph separators.
UNSAFE_CATEGORIES = {"Cc", "Cf", "Cs", "Zl", "Zp"}


def _escape_char(ch):
    o = ord(ch)
    if 0xDC80 <= o <= 0xDCFF:  # a raw byte carried by surrogateescape
        return "\\x%02x" % (o - 0xDC00)
    if o < 0x100:
        return "\\x%02x" % o
    if o < 0x10000:
        return "\\u%04x" % o
    return "\\U%08x" % o


def log_safe(text):
    """Text from a pull request (paths, ref names, git's stderr) printed to a
    CI log. GitHub Actions reads any output line that starts, after leading
    whitespace, with `::` or `##[` as a workflow command, so a file named
    `x<newline>::error::...` could forge annotations or stop command parsing.
    Every unsafe character is printed as a visible escape (newline -> `\\x0a`),
    so the text can never start a new line; leading whitespace and a leading
    `:` or `#` are escaped too, so it cannot start a command even when
    printed at the start of a line."""
    out = [_escape_char(ch) if unicodedata.category(ch) in UNSAFE_CATEGORIES
           else ch for ch in text]
    i = 0
    while i < len(out) and len(out[i]) == 1 and out[i].isspace():
        out[i] = _escape_char(out[i])
        i += 1
    if i < len(out) and out[i] in (":", "#"):
        out[i] = _escape_char(out[i])
    return "".join(out)


def redact(label):
    """A path or ref name can carry an address. Replace every '/'-separated
    component that holds one (raw, entity-encoded or obfuscated) before it is
    printed, keeping the rest of the path so the file can still be found.
    The result is also log-safe (see log_safe): pull-request text never
    starts a line or a workflow command in the CI log."""
    suffix = " (file name)" if label.endswith(" (file name)") else ""
    body = label[:len(label) - len(suffix)]
    parts = []
    for part in body.split("/"):
        unescaped = html.unescape(part)
        if any(True for v in (part, unescaped, deobfuscate(unescaped))
               for _ in address_matches(v)):
            part = f"[redacted#{h(part)[:8]}]"
        parts.append(part)
    return log_safe("/".join(parts)) + suffix


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
    for leaky in (f"notes/{CANARY}.md", CANARY.replace("@", "\uff20")):
        if "@" in redact(leaky) or "\uff20" in redact(leaky):
            die("self-test FAILED — path redaction left an address visible")
    for spoof in ("a\n::error::x", "::error::x", "  ##[error]x", "a\rb\x1b"):
        safe = redact(spoof)
        if (any(unicodedata.category(c) in UNSAFE_CATEGORIES for c in safe) or
                safe.lstrip().startswith(("::", "##["))):
            die("self-test FAILED — path text can still start a log command")
    if "canary" in fingerprint(CANARY):
        die("self-test FAILED — address fingerprint echoes the address")


def address_matches(text):
    """Preserve finditer's greedy, non-overlapping matches in linear time.
    Each at-sign gets one anchored match attempt, rather than retrying every
    suffix of a local-part run. The cursor also permits adjacent matches."""
    cursor = 0
    while True:
        at = text.find("@", cursor)
        if at == -1:
            return
        start = at
        while start > cursor and text[start - 1] in LOCAL_PART_CHARS:
            start -= 1
        match = ADDR_RE.match(text, start)
        cursor = match.end() if match else at + 1
        if match:
            yield match


def github_identity(variant, m):
    """True for a GitHub-issued no-reply address used as an identity: inside
    the <...> of an author, committer or tagger header line, before the first
    blank line of a commit or tag object. Any contributor's own no-reply
    address passes there; the same address anywhere else (a message, a file)
    is still UNALLOWLISTED."""
    if not GITHUB_NOREPLY_RE.fullmatch(m.group(0)):
        return False
    start, end = m.span()
    if (start == 0 or end >= len(variant) or variant[start - 1] != "<" or
            variant[end] != ">"):
        return False
    header_end = variant.find("\n\n")
    if header_end != -1 and start > header_end:
        return False
    line_start = variant.rfind("\n", 0, start) + 1
    return variant.startswith(IDENTITY_HEADERS, line_start)


def github_coauthor(variant, m):
    """True for a GitHub user no-reply address that is the address of an
    exact `Co-authored-by: Name <address>` line (the trailer GitHub itself
    writes). The address must be the whole <...> of that line; the same
    address in prose, in another trailer or in a file is still UNALLOWLISTED."""
    if not GITHUB_USER_NOREPLY_RE.fullmatch(m.group(0)):
        return False
    start, end = m.span()
    line_start = variant.rfind("\n", 0, start) + 1
    line_end = variant.find("\n", end)
    if line_end == -1:
        line_end = len(variant)
    line = COAUTHOR_LINE_RE.fullmatch(variant, line_start, line_end)
    return bool(line) and line.span(1) == (start, end)


def scan_blob(data, path, deny_hashes, allow, findings, identity_headers=False,
              coauthor_trailers=False):
    """Content scan. A deny-hash match is unconditional; the allowlist can
    only suppress the generic UNALLOWLISTED rule, never a known address.
    identity_headers=True (commit and tag objects only) also lets GitHub
    no-reply identities through, see github_identity(). coauthor_trailers=True
    (commit messages only) lets a user's no-reply address through on an exact
    Co-authored-by line, see github_coauthor()."""
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
        for m in address_matches(variant):
            a = m.group(0)
            known = h(a) in deny_hashes
            if not known and (deny_only or a.lower() in allow_l or
                              (identity_headers and github_identity(variant, m)) or
                              (coauthor_trailers and github_coauthor(variant, m))):
                continue
            line = variant.count("\n", 0, m.start()) + 1
            why = "KNOWN-PRIVATE" if known else "UNALLOWLISTED"
            key = (path, line, why, a.lower())
            if key in seen:
                continue
            seen.add(key)
            findings.append((path, line, f"{why} {fingerprint(a)}"))


# Results of scanning one git blob, keyed by (sha, deny_only). The history
# walk visits the same blob once per commit that contains it; the content and
# therefore the verdict cannot change, so it is read and scanned once.
_BLOB_CACHE = {}


def scan_git_blob(sha, path, deny_hashes, allow, findings):
    key = (sha, path in DENY_ONLY_CONTENT)
    if key not in _BLOB_CACHE:
        local = []
        scan_blob(git("cat-file", "blob", sha), path, deny_hashes, allow, local)
        _BLOB_CACHE[key] = [(line, why) for _, line, why in local]
    findings.extend((path, line, why) for line, why in _BLOB_CACHE[key])


def check_path(path, bad_base, bad_path):
    """Case-folded, NFC-normalized path check. Returns a reason or None.
    Basenames are glob patterns (`*`, `?`, `[...]`), as CI's `find -iname`
    reads them; paths are exact."""
    base = norm(path.rsplit("/", 1)[-1])
    if any(fnmatch.fnmatchcase(base, pat) for pat in bad_base):
        return "FORBIDDEN BASENAME"
    if norm(path) in bad_path:
        return "FORBIDDEN PATH"
    return None


def scan_name(path, deny_hashes, allow, findings):
    """A file NAME is published as surely as its contents: a file named after
    an address would ship it without any content scan ever reading it."""
    scan_blob(path.encode("utf-8", "surrogateescape"), f"{path} (file name)",
              deny_hashes, allow, findings)


def object_encodings(headers):
    """Values of a commit or tag's `encoding` header(s). Continuation lines of
    multi-line headers (gpgsig, mergetag) start with a space and never match."""
    return [l[len(b"encoding "):].strip()
            for l in headers.split(b"\n") if l.startswith(b"encoding ")]


ASCII = bytes(range(128))


def ascii_compatible(enc):
    """True when every ASCII byte decodes to itself, alone and in a run.
    Commit headers are ASCII bytes; under an encoding where they are not
    (UTF-16, UTF-32, UTF-7, stateful ISO-2022 and the like) neither the raw
    bytes nor a decode of the object means what a reader sees."""
    try:
        return (ASCII.decode(enc) == ASCII.decode("ascii") and
                all(bytes([c]).decode(enc) == chr(c) for c in ASCII))
    except (LookupError, UnicodeError, ValueError, TypeError):
        return False


def decoded_forms(sha, obj, message, encodings, kind="commit"):
    """For metadata whose `encoding` header is not UTF-8, the object as a
    reader sees it after decoding: ([(label, bytes)], problems). Raw bytes
    alone can hide an address, so the message and WHOLE object (including
    headers) are also decoded strictly by Python. For commits, scan Git's own
    re-encoded identities and message too; Git does not re-encode tags. An
    unknown encoding, one that is not ASCII-compatible, or a failed decode
    is a FAILED MEASUREMENT: reported UNSCANNABLE, never certified clean."""
    forms, problems = [], []
    decoded_path = f"<{kind} decoded>"
    message_path = f"<{kind} message decoded>"
    for raw_enc in encodings:
        enc = raw_enc.decode("ascii", "replace")
        try:
            enc = codecs.lookup(enc).name
            if enc == "utf-8":
                continue  # the strict UTF-8 scan of the raw bytes covers it
        except (LookupError, ValueError):
            problems.append((decoded_path,
                             f"UNSCANNABLE — unknown {kind} encoding"))
            continue
        if not ascii_compatible(enc):
            problems.append((decoded_path,
                             f"UNSCANNABLE — {kind} encoding {enc!r} is not "
                             f"ASCII-compatible"))
            continue
        for label, data in ((message_path, message), (decoded_path, obj)):
            try:
                # strict decode, then strict encode: lone surrogates fail too
                forms.append((label, data.decode(enc).encode("utf-8")))
            except (UnicodeError, ValueError):
                problems.append((label, f"UNSCANNABLE — not decodable as {enc!r}"))
        # git may decode with a different converter than Python; scan its view
        # too. scan_blob's strict UTF-8 read flags it if git could not convert.
        if kind == "commit":
            forms.append((decoded_path,
                          git("log", "-1", "--no-show-signature", "--encoding=UTF-8",
                              "--format=author %an <%ae>%ncommitter %cn <%ce>%n%n%B",
                              sha)))
    return forms, problems


def metadata_object(sha, kind):
    """Read metadata byte for byte; formatting commands can truncate at NUL."""
    obj = git("cat-file", kind, sha)
    headers, _, message = obj.partition(b"\n\n")
    forms, problems = [], []
    encodings = object_encodings(headers)
    if encodings:
        forms, problems = decoded_forms(sha, obj, message, encodings, kind)
    return headers, message, forms, problems


def scan_metadata(sha, kind, headers, message, forms, problems,
                  deny_hashes, allow, findings):
    # Strict UTF-8 for raw bytes, even when a declared encoding is also read.
    # Headers (and decoded whole objects, which start with them) may carry a
    # GitHub no-reply identity; messages may not.
    scan_blob(headers, f"<{kind} header> {sha[:12]}", deny_hashes, allow, findings,
              identity_headers=True)
    # Commit messages may carry a co-author's no-reply address on an exact
    # Co-authored-by line; tag messages may not.
    commit = kind == "commit"
    scan_blob(message, f"<{kind} message> {sha[:12]}", deny_hashes, allow, findings,
              coauthor_trailers=commit)
    for label, problem in problems:
        findings.append((f"{label} {sha[:12]}", 0, problem))
    for label, form in forms:
        # Decoded whole objects and git's re-encoded view both hold the
        # message after the headers, so the trailer rule applies to them too.
        scan_blob(form, f"{label} {sha[:12]}", deny_hashes, allow, findings,
                  identity_headers=(label == f"<{kind} decoded>"),
                  coauthor_trailers=commit)


def commit_objects(tips=()):
    """(sha, raw header bytes, raw message bytes, decoded (label, bytes)
    forms, (label, problem) pairs) for every commit reachable from every ref. Each commit is read on
    its own with `cat-file`, never parsed out of a `git log` stream: %B stops
    at a NUL byte and a separator byte inside a message splits its record,
    and either one hides the text after it. The WHOLE object is scanned, as
    bytes: headers (author, committer, mergetag, gpgsig) and message."""
    for raw_sha in git("rev-list", "--all", *sorted(tips)).splitlines():
        if not re.fullmatch(rb"[0-9a-f]{40}", raw_sha):
            die("git rev-list --all returned an invalid commit SHA")
        sha = raw_sha.decode("ascii")
        yield sha, *metadata_object(sha, "commit")


def ref_objects():
    """Keep ref names as bytes until the two ASCII fields are separated.
    Git forbids LF and spaces in ref names, but permits non-UTF-8 bytes."""
    for record in git("for-each-ref",
                      "--format=%(objectname) %(objecttype) %(refname)").split(b"\n"):
        if not record:
            continue
        fields = record.split(b" ", 2)
        if (len(fields) != 3 or not re.fullmatch(rb"[0-9a-f]{40}", fields[0]) or
                fields[1] not in (b"commit", b"tag", b"tree", b"blob") or
                not fields[2].startswith(b"refs/")):
            die("git for-each-ref returned an invalid object record")
        sha, kind, name = fields
        yield sha.decode("ascii"), kind, name.decode("utf-8", "surrogateescape")


def tag_target(headers):
    """Peel exactly one level and verify the declared target type."""
    lines = headers.split(b"\n")
    if (len(lines) < 2 or not re.fullmatch(rb"object [0-9a-f]{40}", lines[0]) or
            lines[1] not in (b"type commit", b"type tag", b"type tree", b"type blob")):
        die("annotated tag has invalid target headers")
    sha = lines[0][len(b"object "):].decode("ascii")
    kind = lines[1][len(b"type "):]
    if git("cat-file", "-t", sha).strip() != kind:
        die("annotated tag target type does not match its object")
    return sha, kind


def scan_history_tree(tree, deny_hashes, allow, bad_base, bad_path, findings):
    """Scan every path, including reused trees and directory names."""
    scanned = 0
    for entry in git("ls-tree", "-r", "-t", "-z", tree).split(b"\0"):
        if not entry:
            continue
        meta, raw_name = entry.split(b"\t", 1)
        _, kind, sha = meta.split()
        name = raw_name.decode("utf-8", "surrogateescape")
        scanned += 1
        if check_path(name, bad_base, bad_path):
            findings.append((name, 0, "FORBIDDEN IN HISTORY"))
        scan_name(name, deny_hashes, allow, findings)
        if kind == b"blob":
            scan_git_blob(sha.decode("ascii"), name, deny_hashes, allow, findings)
        elif kind != b"tree":
            # A submodule (gitlink, type commit) or anything else: nothing was
            # read, so nothing may be certified -- the same verdict as --tree.
            findings.append((name, 0, "UNSCANNABLE — not a regular file"))
    return scanned


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
        scan_blob(msg_file.read_bytes(), COMMIT_MSG_PATH, deny_hashes, allow, findings,
                  coauthor_trailers=True)
    elif history:
        refs = list(ref_objects())
        tag_targets, commit_tips = {}, set()
        for sha, kind, name in refs:
            scanned += 1
            scan_name(name, deny_hashes, allow, findings)
            chain = set()
            while kind == b"tag":
                if sha in chain:
                    die("cycle in annotated tag targets")
                chain.add(sha)
                if sha not in tag_targets:
                    metadata = metadata_object(sha, "tag")
                    scan_metadata(sha, "tag", *metadata, deny_hashes, allow, findings)
                    scanned += 1
                    tag_targets[sha] = tag_target(metadata[0])
                sha, kind = tag_targets[sha]
            if kind == b"commit":
                commit_tips.add(sha)
            elif kind == b"blob":
                scanned += 1
                scan_git_blob(sha, name, deny_hashes, allow, findings)
            elif kind == b"tree":
                scanned += scan_history_tree(sha, deny_hashes, allow,
                                             bad_base, bad_path, findings)
        # Commit headers and messages are scanned separately as raw bytes
        # and, if re-encoded, decoded forms. Git history makes leaks permanent.
        commits = list(commit_objects(commit_tips))
        if not commits and not refs:
            die("no objects -- refusing to certify an empty history scan")
        for sha, headers, message, forms, problems in commits:
            # Keep the per-commit walk: object enumeration gives a reused
            # tree only one name, which can hide a historical directory name.
            scanned += scan_history_tree(sha, deny_hashes, allow,
                                         bad_base, bad_path, findings)
            scanned += 1
            scan_metadata(sha, "commit", headers, message, forms, problems,
                          deny_hashes, allow, findings)
    elif tree:
        # Every tracked path, read as the blob git tracks for it (the index),
        # never through the filesystem: a tracked symlink is scanned as its
        # link text and never followed out of the repo.
        entries = [e for e in git("ls-files", "-s", "-z").split(b"\0") if e]
        if not entries:
            die("git ls-files returned no paths -- refusing to certify an empty scan")
        for entry in entries:
            meta, sep, raw = entry.partition(b"\t")
            fields = meta.split()
            if (not sep or len(fields) != 3 or
                    not re.fullmatch(rb"[0-9a-f]{40}", fields[1])):
                die("git ls-files -s returned an invalid index entry")
            mode, sha = fields[0], fields[1].decode("ascii")
            path = raw.decode("utf-8", "surrogateescape")
            scanned += 1
            why = check_path(path, bad_base, bad_path)
            if why:
                findings.append((path, 0, why))
                continue
            scan_name(path, deny_hashes, allow, findings)
            if mode in (b"100644", b"100755", b"120000"):
                scan_git_blob(sha, path, deny_hashes, allow, findings)
            else:
                # A submodule (160000) or anything else: nothing was read,
                # so nothing may be certified.
                findings.append((path, 0, "UNSCANNABLE — not a regular file"))
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
        # Paths and ref names are redacted: CI logs are public, and a finding
        # in a file name would otherwise print the very address it caught.
        for path, line, why in sorted(set(findings)):
            print(f"  {redact(path)}{f':{line}' if line else ''}  [{why}]",
                  file=sys.stderr)
        sys.exit(1)

    mode = ("message" if msg_file is not None else
            "history" if history else "tree" if tree else "staged")
    print("gate: clean (%d objects scanned, %s; %d hashes loaded, "
          "matchers self-tested)" % (scanned, mode, len(deny_hashes)))
    sys.exit(0)


if __name__ == "__main__":
    main()
