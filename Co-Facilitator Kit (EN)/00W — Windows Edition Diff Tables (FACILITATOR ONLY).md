---
title: "Windows Edition — Diff Tables (Facilitator Only)"
created: 2026-08-19
category: reference
status: active
tags: [aiac, phase0, co-facilitator-kit, windows, facilitator, diff]
related: ["[[README — Kit Index & How to Use]]"]
---

> # 🚨 DO NOT SEND TO A PARTICIPANT
>
> The participant docs tell them to *"open the file, select all, copy, paste"* — anything appended
> to a doc gets pasted into Claude Code along with it. This file exists **separately** so the
> Windows variants stay auditable without riding along into someone's paste buffer.
>
> Pattern borrowed from Mangan, who nearly lost his own diff tables into a student's copy-paste.

# Windows Edition — what changed and why

**Principle: variants, not forks.** Every Windows document is the EN document plus a listed set of
changes. That means each deviation can be reviewed, questioned, or reverted, and the edition never
silently drifts from the kit.

| Document | Status |
|---|---|
| `01 — Pre-Session Setup Instructions` | **Shared** — no Windows variant. It was already OS-branched; the Windows section was strengthened in place (5 additions below). |
| `02W — Main Setup Prompt (Windows)` | Variant — **12 changes** |
| `03W — Skills & Config Setup Prompt (Windows)` | Variant — **11 changes** |
| `04 — Next Steps Brief` | **Shared, unchanged.** Reading material; nothing OS-specific executes. |
| `02-S — Sandbox Setup` | **Not available on Windows.** Native Windows has no sandbox; WSL2 required. |

## The four landmines this edition exists to defuse

Verified against Anthropic's live docs, then against a real Windows machine.

1. ⛔ **Claude Code does not run on the free plan** — docs verbatim: *"The free Claude.ai plan does
   not include Claude Code access."* Made gate zero in Doc 01. Self-resolving: if `claude` opens
   logged in, the upgrade happened.
2. **Backslash paths fail *silently* in Git Bash.** An unquoted `\` is stripped and *"the command
   fails without a visible error."* A `C:\` path in the router breaks it **and looks identical to
   the classic profile-vs-router bug**, so you would debug the wrong thing. Three defenses:
   `pwd -W`, a `grep -c '\\'` must-equal-0 gate after writing the router, and telling Claude the
   rule up front.
3. **The custom statusline may never render** on Windows + Git Bash
   ([claude-code#66455](https://github.com/anthropics/claude-code/issues/66455)). Carries a
   3-step fallback and a **3-minute stop-loss**, made safe by the reframe that matters:
   **the bar is only the display — the 75% override and the two hooks are the actual guardrail**,
   and none of them depend on it.
4. **`python3` usually isn't a command on Windows** (it's `python` or `py`; bare `python3` opens the
   Microsoft Store) — **and Doc 03's STEP 7, the kit's final verification, writes and runs a Python
   script.** As shipped, the kit's last check fails on Windows for a reason unrelated to the setup.

## Doc 01 — strengthened in place (5 additions)

| # | Addition | Why |
|---|---|---|
| 1 | **Gate 0: free plan blocks Claude Code** | Blocks everything else; a Mac student was stuck for weeks on it |
| 2 | **Gate 0.5: which window am I in** (PowerShell vs Git Bash vs CMD table) | The student's error screenshots were CMD, his docs assumed PowerShell, the kit's blocks need Git Bash. Also: `where bash` failing is expected, not a failed install |
| 3 | **Forward-slash rule + `pwd -W`** | Landmine #2 |
| 4 | **PATH verification after the installer** | The official installer finished and reported in its own output that it had NOT added `.local/bin` to PATH → `'claude' is not recognized`, twice, across a week |
| 5 | **"This is prose, not commands" banner** | Prose pasted into PowerShell produced a `ParserError` and a stuck `>>` prompt — an unclosed quote from the apostrophe in *"you're"* |

## Doc 02W — 12 changes vs `02 — Main Setup Prompt (Participant)`

| # | Where | Kit says | 02W says | Why |
|---|---|---|---|---|
| 1 | Frontmatter | generic | title/tags marked Windows | Discoverability |
| 2 | Header | (none) | Three Windows rules above the paste line | Right-click paste · Git Bash · forward slashes |
| 3 | Preamble | (none) | A one-line environment declaration to paste first | Removes ~6 "detect my OS" round-trips from a live session |
| 4 | Vault path | `pwd` | **`pwd -W`** | `pwd` prints `/c/Users/…`; the router needs `C:/Users/…` |
| 5 | Router verify | `head -20` | `head -25` + **`grep -c '\\'` must be 0** | Catches a backslash path before it breaks the router silently |
| 6 | STEP 3 Stop hook | `afplay …` | **Windows beep baked in** + a "did you hear it / delete it" check | Fires every turn; a wrong line = an error every turn for 90 min |
| 7 | STEP 3 callout | pick-by-OS list | Rewritten: don't swap in `afplay`; delete the block if no beep | Removes the choice that produces the failure |
| 8 | STEP 4 | `xcode-select --install` | git-scm.com/download/win, accept Git Bash | macOS command in a Windows session |
| 9 | STEP 7 `.gitignore` | `.DS_Store` | adds `Thumbs.db`, `desktop.ini` | Windows equivalents |
| 10 | `~/dev` | Mac-only phrasing | adds the `C:\Users\…\dev` translation | So they can find it in File Explorer later |
| 11 | STEP 3.5 statusline | one Windows note | **Known bug documented + 3-step fallback + 3-min stop-loss + the "bar is only display" reframe** | Landmine #3 |
| 12 | STEP 3.5 sound | `afplay` in `statusline.sh` | **Windows beep baked into the script**; note rewritten | The one genuinely executable `afplay` in the doc |

## Doc 03W — 11 changes vs `03 — Skills & Config Setup Prompt (Participant)`

| # | Where | Kit says | 03W says | Why |
|---|---|---|---|---|
| 1–2 | Frontmatter + header | generic | Windows title/tags; three rules restated; environment declaration | A new session loses Doc 02's context |
| 3 | STEP 1 | `head -20`, 2 checks | `head -25` + **3rd check: zero backslashes** | The check that catches landmine #2 |
| 4 | STEP 2.6b Granola | `~/Library/Application Support/Granola/` + launchd/cron | `%APPDATA%\Granola\` (`~/AppData/Roaming/…`) + **Windows Task Scheduler**, and "confirm the real filenames, don't assume the Mac layout" | Optional/deferred, but the Mac paths simply do not exist |
| 5 | STEP 2.5b `gws` | `~/bin/gws`, `chmod +x`, zsh profile | `~/bin/gws.exe`, windows-amd64, `~/.bashrc` PATH line | The Mac instructions were unrunnable |
| 6 | STEP 3 `lessons.md` | empty | seeded with the forward-slash rule | Puts the Windows rule where Claude re-reads it every session |
| 7 | ⭐ **STEP 7** | "Create a Python script … and run it" | **Detect `python`/`py`/`python3` first**; missing Python explicitly NOT a blocker; add the real command to `allow` | ⭐ Landmine #4 — the kit's final check otherwise fails on Windows for an unrelated reason |
| 8 | STEP 7 | 8 checks | adds `jq .` JSON-validity check on `settings.json` | Cheap; catches a corrupted merge from Doc 02 |
| 9 | STEP 7 | (none) | adds `claude doctor` | First thing to run when something breaks later |
| 10–11 | STEP 6 cheat sheet | Mac-neutral | Windows notes block (window · paths · paste · `claude doctor`) | The four things they'll forget by next week |

## Verification run (2026-08-19)

| Check | 02W | 03W |
|---|---|---|
| Code-fence balance (a select-all paste won't truncate) | ✅ 68, balanced | ✅ 44, balanced |
| macOS commands inside code blocks | ✅ 0 executable (1 textual, inside the "do not offer me these" instruction) | ✅ 0 |
| `~/Library` paths inside code blocks | ✅ 0 | ✅ 0 |
| `bash -n` on every bash block | ✅ 10 clean / 5 placeholder-only — **identical to the EN baseline**, no regressions | ✅ 15 clean, 0 failing |
| `settings.json` block parses, Stop hook de-escapes correctly | ✅ `powershell.exe -c "[console]::beep(1000,400)"` | n/a |
| Smart quotes inside code blocks | ✅ 0 | ✅ 0 |

**Note on defect #12:** unlike the pack Mangan built for one of his participants — which deliberately shipped the original
permissions block — these variants inherit the **hardened** block (`Bash(python3 *)`,
`Bash(pip install *)`, bare `Read`/`Write`/`Edit` removed), per the maintainer's decision of 2026-08-19.
The Windows STEP 7 change above is what keeps that hardening from costing anything: it has Claude
add the *real* Python command to `allow` only if Python actually exists.
