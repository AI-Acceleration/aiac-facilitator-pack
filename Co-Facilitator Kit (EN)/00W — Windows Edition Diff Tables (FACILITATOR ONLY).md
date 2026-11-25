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
> Participants hand the setup docs to Claude Code by file path (*"Read the file … and follow its
> instructions"*) — Claude reads the **whole** file, so anything appended to a doc would be read as
> instructions. This file exists **separately** so the Windows variants stay auditable without riding
> along into someone's setup.
>
> Pattern borrowed from Mangan, who nearly lost his own diff tables into a student's copy-paste.

# Windows Edition — what changed and why

**Principle: variants, not forks.** Every Windows document is the EN document plus a listed set of
changes. That means each deviation can be reviewed, questioned, or reverted, and the edition never
silently drifts from the kit.

| Document | Status |
|---|---|
| `01 — Pre-Session Setup Instructions` | **Shared** — no Windows variant. It was already OS-branched; the Windows section was strengthened in place (5 additions below). |
| `02W — Main Setup Prompt (Windows)` | Variant — **17 changes** |
| `03W — Skills & Config Setup Prompt (Windows)` | Variant — **10 changes** |
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

## Doc 02W — 17 changes vs `02 — Main Setup Prompt (Participant)`

| # | Where | Kit says | 02W says | Why |
|---|---|---|---|---|
| 1 | Frontmatter | generic | title/tags marked Windows | Discoverability |
| 2 | Header | load-by-file steps for all OSes | **Three Windows rules** (give the file by path, right-click for short pastes · Git Bash · forward slashes) | The three things that break Windows sessions |
| 3 | Header, how to load | Finder / File Explorer / Linux copy-path | File Explorer **Copy as path** only, plus **Open Git Bash here** + `pwd -W` | Starts Claude in the right folder from the right shell |
| 4 | Header, trust prompt | "choose Yes" | adds: **the highlighted default on Windows is "No, exit"** | People press Enter and Claude Code quits |
| 5 | Start of the Claude section | (none) | **Environment declaration** (Windows, Git Bash, forward slashes, no macOS commands) inside the file | Removes ~6 "detect my OS" round-trips; no separate paste needed |
| 6 | Vault location check | `pwd`; Windows + macOS cloud-sync branches | **`pwd -W`**; Windows OneDrive branch only (`Documents`/`Desktop` redirection), default `C:/Users/YOUR-USER/AIAC-Vault` | OneDrive redirection is the Windows trap; the macOS iCloud branch doesn't apply |
| 7 | Router, vault path | `pwd` | **`pwd -W`** | `pwd` prints `/c/Users/…`; the router needs `C:/Users/…` |
| 8 | Router verify | read back 20 lines | 25 lines + **`grep -c '\\'` must be 0** | Catches a backslash path before it breaks the router silently |
| 9 | STEP 3 Stop hook | `afplay …` | **Windows beep baked in** + a "did you hear it / delete it" check | Fires every turn; a wrong line = an error every turn for 90 min |
| 10 | STEP 3 callout | pick-by-OS list | Rewritten: don't swap in `afplay`; delete the block if no beep | Removes the choice that produces the failure |
| 11 | STEP 3.5 OS detection + `jq` | `uname`, per-OS `jq` install lines | OS already declared; **`winget install jqlang.jq`** (not bundled with Git for Windows) | `jq` missing is the common Windows failure in Layers 2–3 |
| 12 | STEP 3.5 statusline | one Windows note | **Known bug documented + 3-step fallback + 3-min stop-loss + the "bar is only display" reframe** | Landmine #3 |
| 13 | STEP 3.5 sound | `afplay` in `statusline.sh` | **Windows beep baked into the script**; note rewritten | The one genuinely executable `afplay` in the doc |
| 14 | STEP 4 | `xcode-select --install` | `winget install --id Git.Git -e` or git-scm.com/download/win, keep Git Bash | macOS command in a Windows session |
| 15 | STEP 5 | `gh` check | adds **`winget install --id GitHub.cli -e`** if missing | Same install route as the prerequisites |
| 16 | STEP 6 `~/dev` + location check | Mac-only phrasing; plain path compare | adds the `C:/Users/YOUR-USER/dev` translation; compare normalised with **`cd … && pwd -P`** | Git prints `C:/…`, Git Bash `/c/…` — a correct repo would show a false `WRONG LOCATION` |
| 17 | STEP 7 `.gitignore` | `.DS_Store` | adds `Thumbs.db`, `desktop.ini` | Windows equivalents |

## Doc 03W — 10 changes vs `03 — Skills & Config Setup Prompt (Participant)`

| # | Where | Kit says | 03W says | Why |
|---|---|---|---|---|
| 1–2 | Frontmatter + header | generic | Windows title/tags; three rules restated; File Explorer copy-path + Open Git Bash here; environment declaration inside the file | A new session loses Doc 02W's context |
| 3 | STEP 1 router check | read back 20 lines, 2 checks | 25 lines + **3rd check: zero backslashes** | The check that catches landmine #2 |
| 4 | STEP 1 routing test | second window, trust `~/dev` | second window **as Git Bash**; trust default is "No, exit" | Same two Windows traps as Doc 02W |
| 5 | STEP 3 `lessons.md` | empty | seeded with the forward-slash rule | Puts the Windows rule where Claude re-reads it every session |
| 6 | ⭐ **STEP 7** | "Create a Python script … run it once" | **Detect `python`/`py`/`python3` first**; missing Python explicitly NOT a blocker; run once with normal approval, never added to `allow` | ⭐ Landmine #4 — the kit's final check otherwise fails on Windows for an unrelated reason |
| 7 | STEP 7 | (none) | `jq .` JSON-validity check on `settings.json`, with a read-back fallback when `jq` is missing | Cheap; catches a corrupted merge from Doc 02W |
| 8 | STEP 7 | (none) | adds `claude doctor` | First thing to run when something breaks later |
| 9–10 | STEP 6 cheat sheet | OS-neutral | Windows notes block (window · paths · paste · `claude doctor`) | The four things they'll forget by next week |

Removed from the kit in v0.2 (so no longer Windows rows): the Granola cached-token helper (old STEP 2.6b) and the `gws` CLI install (old STEP 2.5b, now "not today").

## Verification run (2026-11-25)

| Check | 02W | 03W |
|---|---|---|
| Code-fence balance | ✅ 82, balanced | ✅ 26, balanced |
| macOS commands inside code blocks | ✅ 0 | ✅ 0 |
| `~/Library` paths inside code blocks | ✅ 0 | ✅ 0 |
| `bash -n` on every bash block | ✅ 18 clean / 3 placeholder-only (`<repo-name>`) — same 3 as the EN baseline | ✅ 9 clean, 0 failing |
| `settings.json` block parses, Stop hook de-escapes correctly | ✅ `powershell.exe -c "[console]::beep(1000,400)"` | n/a |
| Smart quotes inside code blocks | ✅ 0 | ✅ 0 |

**Note on permissions:** like the rest of the kit, these variants use the **narrow** permissions
block: only local, everyday git commands (`status`, `diff`, `log`, `add`, `commit`, `init`,
`remote -v`), plus `ls`, `mkdir`, `wc`, `Glob`, `Grep`. No blanket `Bash(git *)`, no `cat`/`head`, no
interpreter (`python`, `py`, `python3`, `node`), no `pip install`, no bare `Read`/`Write`/`Edit` — and
the block is merged into existing settings, never overwritten. The Windows STEP 7 change above keeps
that hardening: it runs the greeting once with normal approval using the Python command that actually
exists, without adding it to `allow`.
