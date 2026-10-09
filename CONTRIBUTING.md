# Contributing

Anyone is welcome to propose changes. Corrections from real sessions are the
most valuable thing you can send: a command that failed on a participant's
machine, a step that confused someone, a translation that reads wrong.

**Never put a participant's data in an issue or a PR**: no names, email
addresses, screenshots of their machine, or excerpts from their vault. Describe
what happened generically ("a Windows participant on Git Bash", "a student
whose Granola account was a work Gmail").

## Getting set up

```bash
git clone https://github.com/AI-Acceleration/aiac-facilitator-pack.git
cd aiac-facilitator-pack
bash bin/install-hooks.sh     # REQUIRED: git clone does not copy .git/hooks
```

Without that second command your commits are ungated. CI runs the same checks,
so a miss is caught rather than shipped, but it is caught noisily, in public,
on your PR.

## Proposing a change

1. Fork, then branch: `git checkout -b fix/<short-description>`
2. Edit. Small, focused diffs review fastest. If you change a document, change
   its other-language twin too, or say in the PR that it still needs it.
3. Run the tests: `python3 -m unittest discover -s tests -v`
4. Push and open a PR. CI must be green; a maintainer reviews.

## What the gate blocks

A commit gate blocks any email address that is not explicitly allowlisted, so
if your PR fails on `UNALLOWLISTED`, you have pasted a real address into a
file. Remove it; don't try to work around it. It also blocks, by path and
case-insensitively, the internal files listed in `.githooks/forbidden-*.txt`
(build specs and the trainer registry, which are not part of the public pack).
Two other verdicts you may see:

- `UNSCANNABLE — not valid UTF-8`: your editor saved the file in a legacy
  encoding (cp1252 is the usual culprit on Spanish text). Re-save it as UTF-8.
  The gate cannot read the file, and an unread file is never certified clean.
- `KNOWN-PRIVATE`: the address is on the deny list. This fails unconditionally;
  adding it to the allowlist does not help, by design.

Commit **messages** are scanned too, by `.githooks/commit-msg` locally and by
`--history` in CI. Git history is permanent; don't paste an address into one.

**Changes under `.githooks/**` or `bin/gate_scan.py` are a security review, not
a docs review.** They alter what the gate can see. Please raise them in a PR of
their own, with the reason in the description, so they are not read past inside
a larger content change. CI refuses any PR that edits anything under
`.githooks/`, `bin/` or `.github/`: a maintainer lands those on `main` as a
separate, reviewed change.

The gate is a text scan. It catches addresses that are hidden with HTML
entities, full-width characters, zero-width characters or `%40`, but it cannot
see an address assembled at runtime from string fragments. Review is the
backstop for that.

## Spanish register

Venezuelan **tuteo** is the default. Argentine voseo lives in `00V` as a diff
table, never as a fork. Register is chosen per *participant*, not per
facilitator.

## License of contributions

By contributing you agree that your contribution is licensed under the
repo's licenses: CC BY 4.0 for content, MIT for code (see `README.md`).
