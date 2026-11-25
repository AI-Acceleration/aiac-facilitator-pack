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
like `<id>+<login>@users.noreply.github.com`. Set it for this clone only:

```bash
git config user.email "<id>+<login>@users.noreply.github.com"
```

The gate accepts any GitHub no-reply address as a commit's author or
committer. Any other address in those fields fails the history check.

## Proposing a change

1. Fork, then branch: `git checkout -b fix/<short-description>`
2. Edit. Small, focused diffs review fastest.
3. Run the tests: `python3 -m unittest discover -s tests -v`
4. Push and open a PR. CI must be green; a maintainer reviews.

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

1. **Email addresses.** Any address that is not explicitly allowlisted fails
   as `UNALLOWLISTED`, in file contents, file names, commit messages, commit
   and tag headers, and every object in history. If your PR fails on it, you
   pasted an address into a file or a message. Remove it; don't work around
   it. The gate reads addresses hidden with HTML entities, full-width or
   zero-width characters or `%40`, but not an address assembled at runtime
   from string fragments.
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

The gate never prints an address it caught: CI logs are public. It shows
`address#<8 hex>` (the start of the address's SHA-256) and the line number,
and replaces any part of a file path that holds an address with
`[redacted#<8 hex>]`. Run `python3 bin/gate_scan.py --tree` locally to see
which file and line.

Commit **messages** are scanned too, by `.githooks/commit-msg` locally and by
`--history` in CI. Git history is permanent; don't paste an address into one.

**Changes under `.githooks/`, `bin/` or `.github/` are a security review, not
a docs review.** They alter what the gate can see. Raise them in a PR of
their own, with the reason in the description, so they are not read past inside
a larger content change. CI fails any PR that edits those folders, and it
always judges a PR with the scanner and pattern lists from `main`, not the
PR's own copy. A maintainer lands gate changes on `main` as a separate,
reviewed change.

## License of contributions

By contributing you agree that your contribution is licensed under the
repo's licenses: CC BY 4.0 for content, MIT for code (see `README.md`).
