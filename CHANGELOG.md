# Changelog

All notable changes to the AIAC Facilitator Pack. Dates are in YYYY-MM-DD.

## v0.2.0 — 2026-11-25

This release makes the kit safer to hand to people who have never used Claude
Code, and closer to how sessions actually run. Every change is in both the
English and the Spanish kit.

### Security

- **The status check no longer shows private details.** It now ends with a
  short block marked "safe to share" that holds only check names, `DONE` /
  `NOT DONE` / `SKIPPED (optional)`, the operating system and one verdict.
  Participants send only that block. The rest of the report never shows an
  email address, a token or a settings value; folder paths are hidden, and
  the repository's remote is shown only as a kind ("GitHub", "other host").
  With `--details` it adds `~/…` paths and the remote's host name for the
  participant's own eyes, under a do-not-share warning. It writes nothing: it
  doesn't even run `gh` or `claude`, which can create files on first run.
- **Setup grants far fewer standing permissions.** Claude is pre-approved
  only for a short list of read-only commands (such as `git status` and
  `git diff`), with no lasting write permission. Explicit `ask` rules make
  it ask every time before it adds or commits files, publishes anything
  (including `git -C …` and `git -c …` forms), or prints a file through the
  shell (`cat`, `head`, `tail`, `grep`, `diff`, `sed`, `sort`, `git show`),
  and it asks before running a script. The docs now say plainly which
  read-only commands Claude Code still runs without asking (for example
  `git log -p`), and why an `ask` rule can't cover them without also
  catching the allowed commands.
- **Settings are merged locally, without showing them.** A small script
  merges the kit's entries into the participant's existing
  `~/.claude/settings.json`, keeps every key and rule already there, and
  prints only what it added and the names of keys it left alone, never
  their values (the file can hold API keys). It stops without changing
  anything if the kit block is damaged or a section has an unexpected type,
  creates the file private from the start, and writes through a symlinked
  `settings.json`. Re-running the step never overwrites the first backup.
- **Safer first upload to GitHub.** Sign-in happens in the browser (or
  through the Git Credential Manager on Windows), with no token to create or
  paste (`gh` and the credential manager store their own). The repository
  starts in a new, empty folder. Any error while creating or connecting it
  stops the setup. Before the first upload, Claude checks the address git
  will really push to, confirms with the participant who owns the
  repository and that it is **Private**, and shows exactly which files and
  commits are going up. Every command in that step starts by moving into the
  repository folder, so none of them runs in the vault by mistake.
- **Removed a meeting-notes shortcut** that read a login token from another
  app's files and depended on an unofficial connection.
- **The opt-in sandbox (Doc 02-S) is described honestly.** It says what the
  sandbox does and does not cover. Its self-test uses made-up files in a
  temporary folder, never a real key. Its credential deny rules are anchored
  to the home folder, so they cover the self-test's files too, and the
  complete list sits in one place. It also blocks Claude Code's login file on
  Linux and WSL2 (`~/.claude/.credentials.json`), which sandboxed commands
  could otherwise read and send to an allowed site such as GitHub. Its quotes
  from the Claude Code docs are re-checked against the live pages and dated.
- **New `SECURITY.md`** explains how to report a security or privacy problem
  privately.
- **The private-data gate is stricter** (shipped as its own change, merged
  just before this release). It checks every commit in full, accepts any
  GitHub no-reply address, hides what it finds in public CI logs, and runs
  the trusted copy of itself when it reviews a pull request.

### Changed

- **Claude Pro is now the default plan.** Upgrade to Max only when the
  limits keep getting in the way.
- **Long prompts are loaded by file, not pasted.** Participants save the
  document and tell Claude "Read the file … and follow its instructions",
  because terminals (the Windows one especially) can cut a long paste short.
- **The starter skills moved to
  [`AI-Acceleration/cc-starter-pack`](https://github.com/AI-Acceleration/cc-starter-pack)**
  and are pinned to version **v1.0.0**, so every fresh install gets the same
  reviewed files (a skill the participant already has under the same name is
  skipped and keeps their version). The installer runs only after a
  successful clone that sits on the reviewed `v1.0.0` commit (`711372c`; a
  tag can be moved, a commit can't), or after checking that an existing copy
  is exactly that commit with no changes.
- **Doc 01 ends with a required pre-flight.** Claude creates the vault
  (never in OneDrive, Dropbox, Google Drive or iCloud), has the participant
  open it in Obsidian with "Open folder as vault", checks every tool, and
  finishes with one line to send the facilitator:
  `PREFLIGHT: READY · ACCOUNT: personal` (or `team`), or a list of what is
  missing.
- **Docs 01, 02, 03 and 07 go out about a week before the session.** The
  GitHub command-line tool (`gh`) and Python 3 are now prerequisites.
- **The facilitator manual (Doc 05) is more realistic:** 90 minutes is the
  best case for one person, so plan 2–3 hours for your first sessions and
  more for groups. It adds a machine-readiness cutoff, a dry run on a clean
  machine, a check that GitHub really has the repository, and an exit
  checklist where every item needs evidence.
- **The next-steps brief (Doc 04)** starts with closing any open setup
  steps, and explains how to keep plugins up to date.
- **Recording meetings is optional.** Granola, any other transcription tool,
  or a pasted transcript all work, and everyone in a meeting is asked first.
- **Team and Enterprise accounts** use the plugins their organization
  provides first, and install by hand only as a fallback.
- **Windows** instructions cover the "Do you trust this folder?" prompt,
  folders that OneDrive silently backs up, and installing tools with
  `winget`.
- **The front page (README / LEEME)** now explains in one screen what the
  kit is, who it is for, what it costs and how long it takes, with links for
  facilitators and participants.
- **Status check v2.0** works on macOS, Windows (Git Bash or WSL) and Linux,
  warns when the vault sits in a cloud-synced folder, checks that Obsidian's
  config folder is in the vault Claude uses, checks the ask-first rules and the
  complete sandbox deny list, looks for broad allow rules and risky permission
  modes in the global, vault and repository settings (including the
  `settings.local.json` files where "don't ask again" answers are saved),
  and only shows the sandbox checks when a
  sandbox is set up. Its labels say only what it can see on the machine (for
  example "repo origin points at GitHub"), and it lists what it cannot check
  from there, such as whether the repository exists on GitHub and is Private.

### Added

- **Doc 06 — Pro Plan Survival Kit:** how usage limits work and how to make
  the Pro plan last.
- **Doc 07 — Vocabulary:** the main terms of the kit on one page.
- A note that the method is not tied to one AI tool: the notes and habits
  are plain files that carry over if you switch tools.

### Removed

- Links to the old starter-skills location.
- Internal maintainer notes and links to private notes from the kit
  indexes, and the "draft" labels on the kit documents.
