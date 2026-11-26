# Contributing

Anyone is welcome to propose changes. Corrections from real sessions are the
most valuable thing you can send: a step that failed on a participant's
machine, a step that confused someone, a translation that reads wrong.

**Never put a participant's data in an issue or a PR**: no names, email
addresses, phone numbers, screenshots of their machine, or excerpts from their
vault. Describe what happened generically ("a Windows participant on Git
Bash", "a participant whose transcription account was a work address"). The
same goes for your own private details: no personal email addresses, local
paths from your machine (`/Users/<name>/...`), links to private repositories,
or internal company systems.

To report a security or privacy problem privately (for example, a prompt that
grants broader permissions than it says, or a status-check output that reveals
more than it should), follow [`SECURITY.md`](SECURITY.md) instead of opening a
public issue.

## Getting set up

```bash
git clone https://github.com/AI-Acceleration/aiac-facilitator-pack.git
cd aiac-facilitator-pack
bash bin/install-hooks.sh     # REQUIRED: git clone does not copy .git/hooks
```

Without that last command your commits are ungated. CI runs the same checks,
so a miss is caught rather than shipped, but it is caught noisily, in public,
on your PR.

### Commit with your GitHub no-reply address

Every commit records an author and committer email, and git history is
public and permanent. Commit with the private address GitHub gives you
(GitHub > Settings > Emails > "Keep my email addresses private"). It looks
like `<id>+<login>@users.noreply.github.com`; accounts that turned this on
before mid-2017 may show the older `<login>@users.noreply.github.com`.
Set it for this clone only:

```bash
git config user.email "<id>+<login>@users.noreply.github.com"
```

The gate accepts either form of a GitHub no-reply address as a commit's
author or committer (or a tag's tagger), and GitHub's own web-merge
committer. Any other address in those fields fails the history check.

To credit a co-author, end the commit message with a trailer block and put
their no-reply address on a line of exactly this form:

```text
Short summary of the change

Why it was needed, in as many paragraphs as you like.

Co-authored-by: Their Name <their no-reply address>
```

The line counts only inside the message's **final trailer block**: the last
paragraph (after the last blank line), which must not be the summary line
and in which **every** line is a `Key: value` trailer (`Co-authored-by:`,
`Signed-off-by:`, `Reviewed-by:` and so on, one per line, no wrapped
continuation lines). The same line in the middle of the message, or in a
last paragraph that also holds ordinary text, fails. So does the address on
any other trailer, in a tag message, in a file or in a file name.

The service addresses in `.githooks/allow-patterns.txt` (today only the one
an AI assistant puts on its `Co-Authored-By:` attribution line) follow the
same rule: accepted as a commit or tag identity and on a `Co-authored-by`
line of the final trailer block, nowhere else. Writing one in a document, or
in the body of a commit message, fails like any other address.

The `commit-msg` hook judges the message before git strips its comment
template, so it ignores a `# ...` template at the end of the message and
everything below a `--verbose` scissors line. The history check reads the
message as committed.

## Proposing a change

1. Fork, then branch: `git checkout -b fix/<short-description>`
2. Edit. Small, focused diffs review fastest.
3. Run the tests: `python3 -m unittest discover -s tests -v`
4. Push and open a PR. The `gate` and `tests` checks must be green, and a
   maintainer reviews. (The one exception, a change to the gate itself, is
   described under "Changing the gate itself" below.)

## Content rules

**English and Spanish land together.** A change to a document in
`Co-Facilitator Kit (EN)/` lands in the same PR as the matching change in
`Co-Facilitator Kit (ES)/`, and the other way round. If you cannot write the
other language, say so in the PR and a maintainer will add it before merging;
it is not merged half-done. The status-check script ships as four copies
(`.sh` and `.sh.txt` in both kits) that must stay byte-identical.

**Prompts, not commands.** Once Claude Code is installed, everything a
participant does is a prompt they give Claude, never a command they type.
The exceptions are installing Git and Claude Code themselves, and interactive
logins (`gh auth login`, the `claude` login), which run in a second terminal
window because Claude cannot answer their questions. Long prompts are loaded
by file, not pasted, because some terminals (Windows in particular) truncate
long pastes: the participant saves the document, copies its path and tells
Claude `Read the file <path> and follow its instructions`. A prompt of a few
lines may be pasted.

**Spanish register.** The Spanish kit is neutral Latin-American Spanish with
*tú* (tuteo). Argentine *voseo* lives in `00V` as a diff table, never as a
fork. If you change wording that `00E`, `00V` or `00W` maps, update those
tables too. Register is chosen per *participant*, not per facilitator.

## What the gate checks, and what it does not

The gate checks two things. Know where it stops: it is not a review.

1. **Email addresses.** Every address fails as `UNALLOWLISTED`, in file
   contents, file names, commit messages, commit and tag headers, and every
   object in history, except the attributions described under "Commit with
   your GitHub no-reply address": a no-reply or allowlisted identity in a
   commit or tag header, and a `Co-authored-by` line in the final trailer
   block of a commit message. If your PR fails on it, you pasted an address
   into a file or a message. Remove it; don't work around it. The gate reads
   addresses hidden with HTML entities, full-width or zero-width characters
   or `%40`, but not an address assembled at runtime from string fragments.
2. **Withheld files.** Internal files listed in `.githooks/forbidden-*.txt`
   (build specs and the trainer registry, which are not part of the public
   pack) are blocked by path and name, case-insensitively.

It does **not** detect names, phone numbers, secrets such as API keys or
tokens, private URLs or local paths. Those rely on the author's care and on
maintainer review.

Other verdicts you may see:

- `UNSCANNABLE — not valid UTF-8`: your editor saved the file in a legacy
  encoding (cp1252 is the usual culprit on Spanish text). Re-save it as UTF-8.
  The gate cannot read the file, and an unread file is never certified clean.
- `KNOWN-PRIVATE`: the address is on the deny list. This fails unconditionally;
  adding it to the allowlist does not help, by design.

The gate never prints an address it caught. It shows `address#<8 hex>` (the
start of the address's SHA-256) and the line number.

**In CI it never prints a file or ref name either**, because CI logs are
public and a name is text a pull request controls: it could hold an address,
a private word, or a sequence the runner would read as a workflow command
(`::error::`, `##[error]`). Each name is shown as `path#<8 hex>`, the start
of the SHA-256 of the name, and a count of the names involved. When git
itself fails during the check, CI prints a fixed message instead of git's
own error text, which can quote a file name. The scanner switches to this
output with `--ci`, which CI passes, or whenever the `GITHUB_ACTIONS` or `CI`
environment variable is set.

**Locally** (`python3 bin/gate_scan.py --tree`, `--history`, or the hooks)
each finding shows the file name and line, followed by the same
`path#<8 hex>`, so you can match a CI finding to its file. Even there, any
part of a path that holds an address is replaced with `[redacted#<8 hex>]`,
control characters print as escapes such as `\x0a`, and a `::` or `##` run
(or a `:` or `#` at either end of a name) prints as `\x3a` / `\x23`
escapes, so a name cannot fake a line of a log.

Commit **messages** are scanned too, by `.githooks/commit-msg` locally and by
`--history` in CI. Git history is permanent; don't paste an address into one.

## How CI judges a pull request

The `gate` check runs from `main`, not from your PR, and only for PRs into
`main`. It is a
`pull_request_target` workflow, so GitHub runs the copy of
`.github/workflows/gate.yml` that is on `main`, with `main`'s scanner and
pattern lists. Your PR's commits are fetched as data and read by that
scanner; nothing from your PR is executed by it, and editing the workflow in
your PR does not change what judges it. It checks, in order:

1. the gate surface pin (below);
2. every file in your PR's latest commit, the same scan as
   `python3 bin/gate_scan.py --tree`;
3. every commit in history, including yours, the same scan as
   `python3 bin/gate_scan.py --history`.

The CI log never prints an address, a file or ref name from your PR, or
git's own error text: logs are public. Findings name files as
`path#<8 hex>`; run the commands above locally to see which file and line
(the local output shows the same `path#<8 hex>` next to each name).

The `tests` check runs your PR's own unit tests with a read-only token.

## Changing the gate itself

**Changes under `.githooks/`, `bin/` or `.github/`, and changes to
`CODEOWNERS`, are a security review, not a docs review.** The folders alter
what the gate can see; `CODEOWNERS` decides who must review them. Raise them
in a PR of their own, with the reason in the description, so they are not
read past inside a larger content change.

Such a PR fails the `gate` check **by design**: the surface pin blocks any
PR that edits those paths, and the rest of the check still runs `main`'s
scanner, not your new one. A failing check is how the PR is flagged for this
review, not a request to rework it. It lands like this:

1. A code owner of those folders (see `CODEOWNERS`) reviews the diff as a
   security change. The `tests` check must be green: that is where the new
   scanner is exercised.
2. A repository admin merges it, overriding the failing `gate` check.
   Branch protection lets only admins override a required check.
3. The push to `main` runs the new gate over all of `main`. If that run is
   red, the change is reverted.

From then on, every PR is judged by the new gate.

The gate's tests (`tests/test_gate*.py`, `tests/fixtures/`) have the same
code owner but are not pinned: they never run in the `gate` check, so editing
them cannot change what the gate sees. A PR that only adds gate tests lands
with a normal review.

## License of contributions

By contributing you agree that your contribution is licensed under the
repo's licenses: CC BY 4.0 for content, MIT for code (see `README.md`).
