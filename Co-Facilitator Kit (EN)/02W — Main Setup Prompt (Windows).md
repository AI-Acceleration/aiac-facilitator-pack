---
title: "Main Setup Prompt (Participant, WINDOWS) — AI Acceleration Club Phase 0"
created: 2026-07-14
category: reference
status: draft
tags: [aiac, phase0, co-facilitator-kit, participant, setup-prompt, main-setup, windows]
---

**Supports:** Paste into Claude Code during Block 2 of the session.

# Main Setup Prompt (WINDOWS) — AI Acceleration Club Phase 0

> ## Three Windows rules — read before you paste
>
> 1. **Paste with right-click**, not Ctrl+V. Long blocks often don't paste with Ctrl+V in Windows Terminal.
> 2. **Run this in Git Bash**, not PowerShell and not CMD. The blocks below are bash. Git Bash comes
>    with Git for Windows; launch it from the Start menu. (`where bash` returning nothing is normal.)
> 3. **Forward slashes `/` in every path — never backslashes `\`.** In Git Bash an unquoted `\` is
>    silently stripped and the command **fails with no visible error**, and the damage looks exactly
>    like an unrelated bug. Get your vault path with `pwd -W`, never plain `pwd`.

**Before anything else, paste this one line so Claude stops offering Mac instructions:**

```
Environment: Windows. I am running Git Bash (not PowerShell, not CMD). Use forward slashes in all
paths. Do not offer me macOS commands such as afplay, xcode-select, brew, or open. If a step has a
macOS branch and a Windows branch, take the Windows branch without asking.
```

This is the prompt that builds your entire working environment: your Obsidian vault, your Claude Code configuration, and your first real project (we'll call it **the case**). It is self-contained — everything below the paste line goes into Claude Code, and Claude walks you through it one step at a time, starting with a short interview to get to know your work and pick the case together.

To run it: open your terminal, `cd` into your Obsidian vault folder, run `claude`, and paste everything below the line.

---

> **⚠️ NOTE FOR WINDOWS USERS — read before pasting:**
> In PowerShell and Windows Terminal, **Ctrl+V does not always work for pasting long blocks**.
> If the prompt doesn't appear when you paste, use the **mouse scroll-wheel click** (middle-click) or
> **right-click** inside the terminal. Remember this tip — you'll need it at every step.
>
> **If Claude Code blocks you while editing `~/.claude/settings.json` and mentions "auto mode":**
> Type `/model` or switch the mode to **default** before continuing (in Claude Code's bottom
> bar, switch from "auto" to "default"). In auto mode, some configuration edits are blocked.
> Once the file is edited, you can switch back to auto.

---

## PASTE EVERYTHING BELOW INTO CLAUDE CODE

---

You are helping me set up my complete working environment from scratch during a live AI Acceleration Club Phase 0 session. Before we build anything, you'll interview me to understand my work and help me pick my first real project (we'll call it **the case**). Then you'll walk me through the setup one step at a time, building everything around that case.

**Important rules for this setup:**
- Walk me through each step ONE AT A TIME. Do not dump everything at once.
- After each step, confirm what was created and ask "Ready for the next step?" before continuing.
- If something fails, help me troubleshoot before moving on.
- All Claude Code configuration and instruction files should live inside this Obsidian vault (not hidden away) so I can see and edit them in Obsidian.
- We start with a short interview (Step 0) so you understand my work and we choose the case together — then you build everything else around it.

---

## STEP 0: WHO I AM & WHAT WE'LL BUILD (LIVE INTERVIEW)

Before touching any files, get to know me and help me pick my first real project — **the case**. Do this conversationally, ONE question at a time. Don't dump all the questions at once, and don't move on until I've answered.

**1. My identity.** First, check whether my Git identity is already set:

```bash
git config --global user.name
git config --global user.email
```

- If both print a value, confirm them with me: "I have you as `<name>` `<<email>>` — is that right for your Git commits?"
- If either is missing, ask me for my full name and the email I want on my commits.

Hold my name and email — you'll use them in Git setup (Step 4), the vault CLAUDE.md (Step 2), the templates, and the briefs.

**2. My work.** Ask me: what do I do? My role, my organization or team, and the kind of work I'm responsible for day to day. Listen for the areas of my work life — these become my vault's areas of responsibility in Step 1.

**3. My problems.** Ask me to describe **1–3 real work problems** I'd like Claude to help with — the repetitive, manual, or slow tasks that eat my time. (I was asked to bring these to the session.) For each one, dig one level deeper: what data or tools are involved, how often it happens, and what "solved" would look like.

**4. Calibration (to set the pace).** Ask me 1–2 light questions so you know how much to explain at each step — don't quiz me, keep it friendly:
- How comfortable am I in a terminal / command line — never, a little, or comfortable?
- Have I used Git or GitHub before?

Use my answers to calibrate: more explanation and hand-holding if I'm new to the terminal or Git; a faster pace if I'm experienced. Adjust throughout the rest of the setup.

**5. Recommend the case.** From my problems, recommend **ONE** as my first case — the best starting project for Phase 0. Pick the one that is (a) painful enough to matter, (b) small enough to show real progress in the first week, and (c) built on data or files I can actually get my hands on. Explain in 2–3 sentences why that one is the right first project. Then propose:
- a short, human **project name** (e.g., "Sales Dashboard", "Invoice Reconciler", "Monthly Report Automation"), and
- a **repo name** derived from it in kebab-case (e.g., `sales-dashboard`, `invoice-reconciler`, `monthly-report`).

**6. Confirm.** Ask me to confirm the case, the project name, and the repo name — or adjust them with me. Once I confirm, summarize back to me in one line: **my name, my email, the case, the project name, and the repo name.**

At that point you have everything you need for the rest of the setup. You'll use it to:
- shape my vault's areas of responsibility (Step 1),
- write my vault and project CLAUDE.md files (Steps 2, 8),
- generate my project brief and Area MOC (Steps 10, 11),
- and create my repo and first commit (Steps 6, 7, 12).

Confirm the summary with me, then move to the vault-location check below and Step 1.

---

**⚠️ Vault location and naming — confirm before we start:**
Your Obsidian vault folder must already exist before running this prompt. If you haven't
created it yet:
- **Name it permanently** (not "Test", "Vault2", "Draft", etc.) — something like your
  name, your company, or "My Vault". You will use this name for years.
- **Save it in a stable location:** `Documents/` or your user home folder. **Do NOT
  save it in Downloads, the Desktop, or any folder that gets cleaned periodically.**
- **macOS:** `~/Documents/My Vault/` is the standard. Open Obsidian → "Create new vault"
  → name it → choose `Documents/` as the parent folder.
- **Windows:** `C:\Users\[your name]\Documents\My Vault\` is the standard. Avoid paths
  with spaces or accented characters if possible.
Tell me the full path to your vault folder (e.g. `C:\Users\Jose\Documents\JRamirez Vault`
or `/Users/jose/Documents/My Vault`) before we start — I'll use it throughout the setup.

---

## STEP 1: VAULT FOLDER STRUCTURE

We're inside my Obsidian vault folder right now. Create this PARA folder structure. Under `02 AREAS/`, create a subfolder for each area of responsibility you learned about in the Step 0 interview (for example `Business/`, `Health/`, `Learning/` — and any specific area my work centers on):

```
00 HUB/00 INBOX/
00 HUB/00 READ_REVIEW/
01 PROJECTS/
02 AREAS/
  [one subfolder per area of my life/work, from the Step 0 interview — always include Learning/]
03 REFERENCE/
04 ARCHIVES/
05 AI/
  CLAUDE CODE/
    workspace/
    resources/
Templates/
```

**What each folder is for:**
- `00 HUB/00 INBOX/` — Everything new lands here. Process it later.
- `00 HUB/00 READ_REVIEW/` — Articles, videos, and links you saved but haven't processed yet. Read and triage them from here, then route what's worth keeping.
- `01 PROJECTS/` — Active projects with clear outcomes and finish lines.
- `02 AREAS/` — Ongoing responsibilities (your work areas, health, learning).
- `03 REFERENCE/` — Useful information organized by topic.
- `04 ARCHIVES/` — Completed projects and inactive material.
- `05 AI/CLAUDE CODE/workspace/` — Claude's working files (drafts, intermediate analysis).
- `05 AI/CLAUDE CODE/resources/` — Guides, checklists, and Claude Code reference material.
- `Templates/` — Reusable note templates.

Confirm what was created. Then move to Step 1.5.

---

## STEP 1.5: OBSIDIAN SETTINGS (FILES AND LINKS)

Before we touch any CLAUDE.md, configure Obsidian itself so new notes land in the
right place and links never break when files move. These four settings are the
load-bearing ones — every vault rule and skill downstream assumes them.

I can't click Obsidian's settings UI for you, so walk me through it. In Obsidian:

**Open** Settings (gear icon, bottom-left, or `Cmd/Ctrl + ,`) → in the left
sidebar under "Options" click **Files and links** (older builds label it "Files & Links").

Set these:

| Setting | Set to | Why |
|---------|--------|-----|
| **Default location for new notes** | "In the folder specified below" | New notes go to a known place, not scattered in the vault root |
| → **Folder to create new notes in** | `00 HUB/00 INBOX` | Matches the GTD capture rule — everything lands in INBOX first |
| **Use [[Wikilinks]]** | **ON** | Links use `[[Note Name]]` format — the vault's linking convention; survives renames and renders in the graph |
| **Detect all file extensions** (a.k.a. "show all file types") | **ON** | PDFs, images, `.json`, `.csv` etc. show in the file explorer instead of hiding |
| **Automatically update internal links** | **ON** | When you move or rename a note, every `[[link]]` to it updates automatically — no broken links |

After I set them, confirm back to me which four are now ON / set, and tell me what
you see under "Folder to create new notes in".

> **Want more?** Power-up plugins (Dataview, Tasks, Templater, Calendar, Periodic
> Notes) and deeper settings are **optional** — they live in the "Level Up Your
> Obsidian" section of your Next Steps Brief, each with what it's for and how to
> set it up. Skip them now; the four above are all Phase 0 needs.

Confirm. Move to Step 2.

---

## STEP 2: VAULT CLAUDE.md

Create a file called `CLAUDE.md` in the vault root (current directory). This is the most important file — it tells Claude Code how to behave every time you start a session in this vault.

Use my first name (from Step 0) in the title. Content:

```markdown
# CLAUDE.md — My Vault

## Identity

You are an AI assistant helping manage a personal knowledge vault and code projects. The vault uses PARA (Projects, Areas, Reference, Archives) + GTD (Getting Things Done) principles. Your job: help capture, organize, connect, and review notes — and help build real things.

## Vault Root

**Working directory:** This vault folder.

## Folder Structure

```
00 HUB/00 INBOX/       — GTD capture. All new files land here first.
00 HUB/00 READ_REVIEW/ — Saved articles/videos/links awaiting reading + triage
01 PROJECTS/      — Active projects with defined outcomes and finish lines
02 AREAS/         — Ongoing areas of responsibility
03 REFERENCE/     — Useful reference material organized by topic
04 ARCHIVES/      — Completed/inactive projects and notes (cold storage)
05 AI/            — Claude Code workspace and resources
Templates/        — Reusable note templates
```

## Core Rules

### File Safety — CRITICAL
- **New files go to `00 HUB/00 INBOX/`** unless the user specifies otherwise.
- **Never modify existing files** without explicit permission.
- **Never delete files.** Prefer archiving to `04 ARCHIVES/`.
- When a task produces multiple files, create a descriptively named folder inside `00 HUB/00 INBOX/`.

### AI Workspace
- Claude's working files (reports, drafts, intermediate analysis) go in `05 AI/CLAUDE CODE/workspace/`.
- Deliverables that need user review go to `00 HUB/00 INBOX/`.

### Notes
- One note = one idea. Synthesize, don't copy.
- Use `[[wikilinks]]` to connect related notes — but only for real relationships.
- Capture fast, organize later. The inbox exists so you never lose a thought.

### Projects
- Every active project must have: **Outcome** (what "done" looks like), **Next Actions** (at least one), and a **Log**.
- Keep active projects manageable (aim for 5-7 max).
- If a project has no clear outcome, it's not a project — it's an area or a someday-maybe idea.

### Session Close-Out
When ending a work session:
1. Update relevant project Next Actions — check off completed, add new ones.
2. Add a Log entry with the date and what was accomplished.
3. Tell the user what was updated and where.

### Clarify Before Acting
Before executing any non-trivial task:
1. Ask clarifying questions until scope is clear.
2. Surface tradeoffs or alternatives when relevant.
3. Restate what you plan to do.
4. Get explicit confirmation before proceeding.
No silent assumptions. No action before confirmation.

### Surgical Edits
When modifying notes:
- Don't refactor adjacent content.
- Match existing style and formatting.
- Every change must trace directly to what was asked.
- Flag unrelated issues separately.

### Context Management
- Monitor context window usage. At ~50%, alert the user immediately.
- Save state to the active project brief before context fills up:
  - Add a "Continuation Prompt" section with: date, what we were doing, where to resume, key decisions made.
- Never let context silently degrade.

## What Claude Can Do
- Triage and classify inbox notes
- Turn ideas into project briefs with outcome + next actions
- Analyze data files (CSV, Excel, JSON)
- Write and run code (Python, SQL, scripts)
- Find connections between notes across the vault
- Generate reports on project status
- Help build my case project (the first real project we chose in Step 0)
```

Confirm the file was created. Then move to Step 3.

---

## STEP 3: CLAUDE CODE GLOBAL CONFIGURATION

Now set up the global Claude Code settings. These live in `~/.claude/settings.json` (outside the vault — this is the one exception because Claude Code requires it there).

Create or update `~/.claude/settings.json` with:

```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(ls *)",
      "Bash(mkdir *)",
      "Bash(cat *)",
      "Bash(head *)",
      "Bash(wc *)",
      "Glob",
      "Grep"
    ],
    "deny": []
  },
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe -c \"[console]::beep(1000,400)\""
          }
        ]
      }
    ]
  }
}
```

> **The Windows beep is already baked into the block above** — do not swap in the macOS `afplay`
> line you may see in other copies of this kit. The `Stop` hook fires at the end of **every turn**,
> so a macOS command here means a failing hook on every single turn of a 90-minute session.
>
> **Check it now:** finish this step and listen for a beep at the end of Claude's next reply.
> **No beep?** Delete the whole `"Stop"` block and move on — it is a convenience, nothing else in
> the setup depends on it. Do not spend session time debugging a sound.

> **Before writing this file:** if `~/.claude/settings.json` or `~/.claude/CLAUDE.md`
> already exists, back it up first — this step overwrites them.
>
> ```bash
> cp -a ~/.claude/settings.json ~/.claude/settings.json.bak 2>/dev/null
> cp -a ~/.claude/CLAUDE.md    ~/.claude/CLAUDE.md.bak    2>/dev/null
> ```
>
> On a brand-new machine both commands do nothing, which is fine.

> **Why this list is shorter than you might expect.** Two things were deliberately left out:
>
> - **`Bash(python3 *)` and `Bash(pip install *)`.** Python can read and write any file as a
>   subprocess, which permission rules cannot see. Pre-approving it would mean that any `deny`
>   rule you add later is decorative unless you also remove this line. You'll get a prompt the
>   first time Claude runs Python — that is the correct outcome on day one, and you can approve it.
> - **Bare `Read` / `Write` / `Edit`.** Listed without a path, these pre-approve those tools for
>   **anywhere on your disk**, which overrides Claude Code's sensible default of staying in the
>   directory you launched it from. Leaving them out makes your setup **more** scoped, not less —
>   your vault becomes the boundary for free.
>
> Everything that actually buys session-day smoothness (`git`, `ls`, `mkdir`, `cat`, `head`,
> `wc`, `Glob`, `Grep`) is still here.

**What this does:**
- **Permissions:** Pre-approves common safe commands so Claude doesn't ask for permission every time. You can add more later.
- **Sound hook:** Plays a sound when Claude finishes a task. Essential when you walk away and come back.

### Global Router — `~/.claude/CLAUDE.md`

Now create the **global router** at `~/.claude/CLAUDE.md`. This is the file that makes Claude Code load your vault rules at the start of EVERY session, no matter which folder you launch from. Two parts matter: the TOP is an **imperative router** (LOAD the vault CLAUDE.md at startup); the BOTTOM is your **profile** (who you are, what you're building).

Emit the file with this exact structure, filling `Who I Am`, the project brief path, and the repo path from the Step 0 interview and the case we chose:

```markdown
# CLAUDE.md — Global Router

## Default Workspace

All Claude Code sessions must load and follow the instructions in:

**`<VAULT_PATH>/CLAUDE.md`**

## Rules

1. At session start, read the vault CLAUDE.md above and follow its routing logic.
2. Default working directory is `<VAULT_PATH>/` unless I explicitly specify another.
3. **Code repositories live in `~/dev/<repo-name>` — never inside the vault.**
   (On Windows, `~/dev` in Git Bash is the same folder as `C:\Users\<you>\dev` in File Explorer — that is where to look for it later.)
   The test is mechanical: if it has its own `.git/`, it belongs in `~/dev/`.
   A git repo nested inside the vault fights Obsidian sync.
4. Scripts that operate on the vault itself (hooks, helpers, skills, analysis
   one-offs) stay in the vault under `05 AI/`. They're part of the vault, not a
   separate project — no `.git` of their own, no move.
5. Do not create files or folders outside the vault and `~/dev/` unless I ask.

---

## Who I Am

<A 2–4 sentence profile of me from the Step 0 interview: my role, my organization/team, the kind of work I do, and the case I'm building.>

## My Projects

My current project brief is at: <VAULT_PATH>/01 PROJECTS/<Project Name>/<Project Name>.md

## My Code Repos

- <Project Name>: ~/dev/<repo-name>

## Defaults

- Language: English. English for code comments and variable names.
- Database access: READ-ONLY by default. Confirm before any write operation.
- No fake data. If you don't have real data, say so.
- After every correction I give you, update the relevant CLAUDE.md so you don't make the same mistake twice.
- Compaction: never accept Claude Code's default **"Resume from summary"** — always choose **"Resume full session"**, or run `/session-close` first. The auto-summary is lossy and silently drops detail.
```

**Important:**
- Replace `<VAULT_PATH>` (both occurrences) with the actual absolute path to my vault — run **`pwd -W`** now (we're in the vault) and use that path. Use `pwd -W`, not plain `pwd`: `pwd` prints `/c/Users/...` which the router cannot resolve, while `pwd -W` prints `C:/Users/...` which it can.
- Fill `## Who I Am` from the Step 0 interview, and set the project brief path and repo path from the case name and repo name we chose.
- The "Default Workspace" router block MUST be at the top, above the profile — Claude uses file-position cues and the router belongs first.

Verify before moving on:

```bash
head -25 ~/.claude/CLAUDE.md

# This MUST print 0. Any other number means a backslash path got written into the router,
# which breaks it silently and looks like an unrelated bug.
grep -c '\\' ~/.claude/CLAUDE.md
```

Confirm: (1) the first section is `## Default Workspace` (not `## Who I Am`), and (2) no literal `<VAULT_PATH>` remains. The full outside-the-vault routing test runs later at the final validation gate.

Confirm. Move to Step 3.5.

---

## STEP 3.5: CONTEXT MONITORING (STATUSLINE + AUTO-COMPACT GUARDRAILS)

> **Why this step exists.** Claude Code has a limited context window. When it fills past its default threshold it **auto-compacts** — it summarizes and drops detail, and that is where sessions silently lose work. This step gives you a **visible bar** showing how full context is, an **audible warning at 50%**, and a **hard-stop before auto-compaction** so YOU decide when to compact (with `/session-close`, which preserves plans and tasks to disk before you `/clear`) instead of being surprised. Four small layers — install one at a time and pipe-test each before moving on.

**First, detect my OS.** Run `uname` (macOS/Linux). On Windows, ask me whether I'm in **PowerShell**, **Git Bash**, or **WSL** — the sound line and script execution depend on it (notes inline below).

### Layer 1 — Raise the auto-compact threshold to 75% (all OS, do this even if you skip the rest)

Merge into the top-level `env` object of `~/.claude/settings.json` (the file from Step 3 — **merge, do not replace the whole object**):

```json
"env": { "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "75" }
```

Validate: `jq -e '.env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE' ~/.claude/settings.json` prints `"75"`. This layer is OS-independent and is the single most important safety setting.

### Layer 2 — Visible statusline bar with a 50% warning

The statusline is the ONLY place that can see context %. Merge into `~/.claude/settings.json`:

```json
"statusLine": { "type": "command", "command": "~/.claude/statusline.sh", "padding": 2 }
```

Write `~/.claude/statusline.sh` with EXACTLY this content:

```bash
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name // "Claude"')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
SID=$(echo "$input" | jq -r '.session_id // "default"')
STATE_FILE="/tmp/claude-ctx-warn-${SID}"

FILLED=$((PCT / 10))
EMPTY=$((10 - FILLED))
BAR=$(printf "%${FILLED}s" | tr ' ' '▓')$(printf "%${EMPTY}s" | tr ' ' '░')

RESET=$'\033[0m'
if [ "$PCT" -ge 75 ]; then
  COLOR=$'\033[1;31m'
  ICON="🚨 "
elif [ "$PCT" -ge 50 ]; then
  COLOR=$'\033[1;33m'
  ICON="⚠ "
  if [ ! -f "$STATE_FILE" ]; then
    powershell.exe -c "[console]::beep(1000,400)" >/dev/null 2>&1 &
    touch "$STATE_FILE"
  fi
else
  COLOR=""
  ICON=""
  [ -f "$STATE_FILE" ] && rm -f "$STATE_FILE"
fi

BRANCH=""
if git rev-parse --git-dir > /dev/null 2>&1; then
  BRANCH=" | $(git branch --show-current 2>/dev/null)"
fi

echo "[$MODEL]$BRANCH | $BAR ${COLOR}${ICON}${PCT}%${RESET}"
```

`chmod +x ~/.claude/statusline.sh` (run this in **Git Bash**).

**Sound line — already set for Windows.** The block above uses `powershell.exe -c "[console]::beep(1000,400)"`. Do **not** replace it with the macOS `afplay` line you may see in other copies of this kit — that command does not exist on Windows and would fail every time the warning fires. If the beep doesn't work or annoys you, delete that one line and keep the visual bar; the colour and icon are the real signal.

> **⚠️ Windows — read this before you spend time on the bar.**
>
> `statusline.sh` is a bash script and runs fine under Git Bash. But there is a **known Claude Code
> bug on Windows + Git Bash where the custom status line simply never renders**
> ([claude-code#66455](https://github.com/anthropics/claude-code/issues/66455)). It may work; it may
> silently do nothing. That is not your setup being wrong.
>
> **If the bar doesn't appear, try in this order — and stop after 3 minutes:**
> 1. Fully quit and reopen Claude Code (the status line loads at startup).
> 2. Confirm the script runs on its own: pipe the test JSON below into it. If that prints a bar, the
>    script is fine and the bug is in the rendering, not your file.
> 3. Try an absolute path in `statusLine.command` (`/c/Users/<you>/.claude/statusline.sh`).
>
> **Then move on regardless.** This is the single most important reframe on Windows: **the bar is
> only a display. The real guardrail is the 75% auto-compact override plus the two hooks** — and
> none of those depend on the status line rendering. You can always type `/context` to see exactly
> the same number. Do not let a cosmetic bug eat your session.

**Pipe-test** (should print a yellow ⚠ at 55%):
```bash
echo '{"model":{"display_name":"Opus"},"context_window":{"used_percentage":55},"session_id":"test"}' | bash ~/.claude/statusline.sh
rm -f /tmp/claude-ctx-warn-test
```

### Layer 3 — Model-facing reminder at 50% (UserPromptSubmit hook)

The hook can't see context %, so it reads the state file the statusline writes. Create `~/.claude/hooks/` if needed and write `~/.claude/hooks/context-warn-prompt.sh`:

```bash
#!/bin/bash
input=$(cat)
SID=$(echo "$input" | jq -r '.session_id // "default"')
STATE_FILE="/tmp/claude-ctx-warn-${SID}"

if [ -f "$STATE_FILE" ]; then
  cat <<'EOF'
{"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "⚠ CONTEXT ≥50%. Auto-compact fires at 75%. Consider running /session-close then /clear to preserve plans/tasks before compaction strips context."}}
EOF
fi
```

`chmod +x ~/.claude/hooks/context-warn-prompt.sh`. **Pipe-test:**
```bash
touch /tmp/claude-ctx-warn-test
echo '{"session_id":"test"}' | bash ~/.claude/hooks/context-warn-prompt.sh | jq -e .
rm -f /tmp/claude-ctx-warn-test
```

### Layer 4 — Hard-stop before auto-compaction (PreCompact hook)

Write `~/.claude/hooks/context-warn-precompact.sh`:

```bash
#!/bin/bash
cat <<'EOF'
{"continue": false, "stopReason": "Auto-compact paused at 75%. Run /session-close to preserve plans/tasks to disk (then /clear), or run /compact to proceed with default compaction."}
EOF
```

`chmod +x ~/.claude/hooks/context-warn-precompact.sh`. **Pipe-test:** `echo '{}' | bash ~/.claude/hooks/context-warn-precompact.sh | jq -e .`

### Wire both hooks into settings.json + verify

**Merge** (do not replace) into the top-level `hooks` object of `~/.claude/settings.json`:

```json
"UserPromptSubmit": [
  { "hooks": [ { "type": "command", "command": "bash ~/.claude/hooks/context-warn-prompt.sh", "timeout": 3 } ] }
],
"PreCompact": [
  { "matcher": "auto", "hooks": [ { "type": "command", "command": "bash ~/.claude/hooks/context-warn-precompact.sh", "timeout": 3 } ] }
]
```

Validate (all three exit 0): `jq -e '.env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE' ~/.claude/settings.json`, `jq -e '.hooks.UserPromptSubmit[0].hooks[0].command' ~/.claude/settings.json`, `jq -e '.hooks.PreCompact[] | select(.matcher=="auto")' ~/.claude/settings.json`. Confirm `jq . ~/.claude/settings.json` exits 0 (no JSON corruption).

Tell me: which files were created/modified, whether existing hooks/env had to be merged, any OS sound swap made, and that I may need to open `/hooks` once (or restart Claude Code) for the new hook entries to register. End with: "Context monitoring is on. Next session, when context crosses 50% you'll see a yellow ⚠ in the status bar, hear one alert, and get a reminder each turn until you compact."

Confirm. Move to Step 4.

---

## STEP 4: GIT SETUP

Check if Git is installed:

```bash
git --version
```

- If installed: tell me the version and move on.
- If not: tell me to install **Git for Windows** from https://git-scm.com/download/win (accept the default options, and make sure **Git Bash** is included), then wait for me to confirm. Do NOT suggest `xcode-select` — that is macOS only.

Configure my Git identity using the name and email from Step 0 (if it was already set and I confirmed it, you can skip this; otherwise set it now):

```bash
git config --global user.name "<my full name>"
git config --global user.email "<my email>"
```

Confirm. Move to Step 5.

---

## STEP 5: GITHUB ACCOUNT

Ask me: **"Do you have a GitHub account? If yes, what's your username?"**

- If yes: note my username and move on.
- If no: walk me through creating one at https://github.com (just the signup). Then ask for my username.

**On authentication (matters when we create the repo and push, Steps 6 and 12) — `gh` is OPTIONAL, not required for Phase 0:** If `gh` CLI is installed, `gh auth login` is the easy path. If it isn't (common on corporate-managed Windows without admin rights), the first `git push` pops a browser via **Git Credential Manager** (bundled with Git for Windows) — or paste a **Personal Access Token** (github.com → Settings → Developer settings → Personal access tokens (classic), scopes `repo` + `workflow`) as the password when git prompts. Neither path needs admin rights. Note which applies to me so Steps 6 and 12 are smooth.

Move to Step 6.

---

## STEP 6: CREATE THE REPO — IN `~/dev`

**Critical:** the repo lives in `~/dev/<repo-name>`, NOT inside the Obsidian vault. Use the repo name we chose in Step 0.

Two workspaces, one rule to tell them apart: **if it has its own `.git/`, it belongs in `~/dev/`.** Knowledge (notes, briefs, project management) lives in the vault. Code repositories live in `~/dev/`. A git repo nested inside the vault fights Obsidian — Obsidian rewrites files just by displaying them, `.git` internals churn through sync, and data folders bloat the vault.

(This does NOT mean "code can't live in the vault." Small scripts that operate on the vault itself — hooks, helpers, one-off analysis — stay in the vault under `05 AI/`. They have no `.git` of their own. The rule is about *repositories*, not about *code*.)

> **⚠️ Windows:** `~/dev` works as written in **Git Bash** and **WSL**. In native **PowerShell** the same folder is `$HOME\dev` (i.e. `C:\Users\[your name]\dev`). Tell me which shell you're in and I'll use the right form throughout.

Because we're starting a brand-new project, there's nothing to clone yet — we create a fresh local repo. First make sure `~/dev` exists, then create and initialize the repo:

```bash
mkdir -p ~/dev
mkdir -p ~/dev/<repo-name>
cd ~/dev/<repo-name> && git init
```

**Verify the repo landed in `~/dev` — DO NOT SKIP:**

```bash
cd ~/dev/<repo-name> && test "$(git rev-parse --show-toplevel)" = "$HOME/dev/<repo-name>" \
  && echo "OK — repo is at $HOME/dev/<repo-name>" \
  || echo "WRONG LOCATION: $(git rev-parse --show-toplevel)"
```

That one check asserts both that the repo IS at `~/dev/<repo-name>` and that it is NOT inside the vault. If it prints `WRONG LOCATION`, **STOP** — do not continue with the repo in the wrong place. Paste me the path it printed and we'll fix it before Step 7.

Paste me the output of the verify command.

> **⚠️ STOP — check with your facilitator before continuing.**
> Show the facilitator the output of the verify command above so they can confirm the
> repo landed in the right place before you move on to Step 7.

Move to Step 7.

---

## STEP 7: REPO SETUP

Inside the `<repo-name>` folder, create this structure. These subfolders are sensible defaults for most projects — adapt them to the case if it clearly needs different ones:

**Subfolders:**
```
data/raw/        — original untouched inputs (gitignored)
data/working/    — intermediate files you are still shaping (gitignored)
data/processed/  — clean, final datasets (committed)
scripts/         — Python scripts for extraction and analysis
reports/         — generated reports and output
docs/            — project documentation
```

Create all three `data/` subfolders now — your Week-1 homework drops a real file into
`data/raw/`, so it has to exist before you leave today.

**`.gitignore`:**
```
.env
*.pyc
__pycache__/
.DS_Store
Thumbs.db
desktop.ini
*.xlsx.bak
.claude/
node_modules/
data/raw/
data/working/
```

**`README.md`:** Write a README for the case from the Step 0 interview. Include:
- a one-line description of the project and what problem it solves,
- the folder structure above (with one line each),
- a short "Data Sources" section listing the systems/files the data comes from (from the interview), and
- any key architectural principle or constraint I mentioned.

Confirm. Move to Step 8.

---

## STEP 8: REPO CLAUDE.md

Create `CLAUDE.md` in the `<repo-name>` repo root. This gives Claude Code full context about the project every time you open a session in this folder.

Generate it from the case we defined in the Step 0 interview. Write a focused, accurate project CLAUDE.md — do not invent facts; use only what I told you, and mark anything still unknown as "TBD". Include these sections:

```markdown
# CLAUDE.md — <Project Name>

## Project

<One or two sentences: what this project is and what problem it solves, from the interview.>

## Key Context

<The domain facts that matter: any architectural principle, constraint, or rule I stated. Skip if none.>

## Data Sources

| System / File | Data | Format |
|---------------|------|--------|
| <source> | <what it holds> | <format or TBD> |

## Milestones

<The rough plan we sketched — the first few concrete milestones toward the outcome.>

## Rules

- Language: English (comments, variable names, and output).
- Data files → `data/`; scripts → `scripts/`; generated reports → `reports/`; documentation → `docs/`.
- Explain what you're doing and why before writing code.
- Ask before complex tasks — don't assume.
- <Any project-specific rule, e.g. currency/units conventions, if I mentioned one.>
```

**Then append this bridge block to that same `CLAUDE.md`.** The repo (`~/dev/`) and the project brief (the vault) now live in different trees, so the link between them has to be written down. Without it, a session opened in `~/dev/<repo-name>` has no way to find the brief. Fill the paths from my vault path, the project name, and my first name:

```markdown
## Where My Notes Live

- **Vault:** `<VAULT_PATH>/`
- **Project brief:** `<VAULT_PATH>/01 PROJECTS/<Project Name>/<Project Name>.md`
- **AIAC Journey brief:** `<VAULT_PATH>/01 PROJECTS/AI Acceleration/<My Name>/AI Acceleration Club - <My Name> Journey.md`

Read the project brief before any non-trivial work in this repo. At the end of a
session, log what was accomplished back to the brief's Log table.
```

Confirm. Move to Step 9.

---

## STEP 9: PROJECT BRIEF TEMPLATE

Go back to the vault. Create the file `Templates/Project Brief Template.md` (use my full name from Step 0 as the owner):

```markdown
---
category: project
status: active
priority: standard
area: ""
owner: "<My Full Name>"
---

# {{title}}

## Outcome

> What does "done" look like? One clear paragraph.

## Why This Matters

- **If this succeeds:** ...
- **If this fails or stalls:** ...

---

## Next Actions

- [ ] First concrete next step
- [ ] Second step

## Waiting For

| Who | What | Since |
|-----|------|-------|
| | | |

## Dependencies

- Dependency 1
- Dependency 2

---

## Key Resources

- [Resource Name](URL)

## People

- **Name** — Role

---

## Plan (Milestones)

| # | Milestone | Target | Status |
|---|-----------|--------|--------|
| 1 | | | Pending |

---

## Working Notes

(scratch space for ideas, analysis, meeting notes)

---

## Log

| Date | Type | Update |
|------|------|--------|
| {{date}} | Milestone | Project created |
```

This is the template for every new project. Whenever you start a new project, copy this template and fill it in.

Confirm. Move to Step 10.

---

## STEP 10: PROJECT BRIEF

Create a dedicated folder for the **case project** at the vault root — `01 PROJECTS/<Project Name>/` — and place the case project brief inside it, exactly like any other real project (it does NOT nest under `01 PROJECTS/AI Acceleration/`). Only the AI Acceleration Club Journey brief (Step 11.5) lives under `01 PROJECTS/AI Acceleration/<My Name>/`, because that one tracks your program journey rather than the business project.

Create the file at `01 PROJECTS/<Project Name>/<Project Name>.md`. Generate it from the Project Brief Template (Step 9), filled with the case from the Step 0 interview:
- **Outcome:** one clear paragraph describing what "done" looks like for the case.
- **Why This Matters:** the payoff if it succeeds, the cost if it stalls — in my words.
- **Next Actions:** the first concrete steps (get the data, do the first audit/inventory, build the first prototype).
- **Waiting For / Dependencies:** anything I said I'm blocked on or need from someone else.
- **Key Resources / People:** links, files, and people I mentioned; include the repo path `~/dev/<repo-name>`.
- **Plan (Milestones):** the milestones we sketched.
- **Working Notes:** any numbers, structures, or context I shared.
- **Log:** one entry with today's date — "Project created. Phase 0 setup complete."

Use only what I told you; mark unknowns as TBD rather than inventing detail. Run `date +%Y-%m-%d` for today's date.

Confirm. Move to Step 11.

---

## STEP 11: AREA MOC

Create a simple Map of Content for the business area the case belongs to (from Step 0), at `02 AREAS/<Area>/<Area>.md`. Use this shape:

```markdown
# <Area Name>

Area of responsibility: <one-line description>.

## Active Projects

- [[<Project Name>]] — <one-line description of the case>

## Key Systems

| System | Function |
|--------|----------|
| <system> | <what it does> |

## Key People

- <Name> — <role>
```

Fill it from the interview. If the case doesn't map cleanly to a business area, create the MOC under the closest area folder you made in Step 1.

Confirm. Move to Step 11.5.

---

## STEP 11.5: AI ACCELERATION CLUB JOURNEY BRIEF

I'm a member of the AI Acceleration Club — the learning program through which I'm building this Claude Code setup. Create a Journey brief so I can track my own progression through the program (Phase 0 onboarding → Week 1 sprint → Phase 2 circle session → longer-term mastery).

**Where it lives:** `01 PROJECTS/AI Acceleration/<My Name>/` — the program-tracking folder (the case project lives in its OWN folder at `01 PROJECTS/<Project Name>/`, per Step 10). This Journey brief tracks my program journey, separate from the business project.

Use my first name and full name (from Step 0) and today's date (`date +%Y-%m-%d`) throughout. Create at: `01 PROJECTS/AI Acceleration/<My Name>/AI Acceleration Club - <My Name> Journey.md`

```markdown
---
tags:
  - project
  - ai-acceleration-club
  - journey
  - actionable
status: active
priority: standard
category: project
description: "My learning journey through the AI Acceleration Club — from Phase 0 onboarding to daily Claude Code fluency. Separate from case projects; this tracks my skill acquisition and program progress."
AREA:
  - "[[Learning]]"
parent: "[[AI Acceleration Club]]"
owner: "<My Full Name>"
created: <TODAY_DATE>
---

# AI Acceleration Club - <My Name> Journey

## Outcome

Reach an expert level of Claude Code fluency by working through Phase 0 → Phase 2 → Phase 3 on real, personal projects. Success = using Claude Code on real work at least 3x per week, with measurable time savings on my most repetitive tasks.

## Why This Matters

- If this succeeds: I stop doing manual work that Claude can automate; my weekly hours shift from busywork to higher-leverage thinking; I can teach the next member when the time comes.
- If this stalls: The setup sits unused; Claude Code feels like a chore instead of a leverage tool; I fall back to manual workflows.

## Next Actions

- [ ] Open Claude Code at least 10 min per day (habit formation — the single most important step of Week 1)
- [ ] Complete the Week 1 homework in [[Next Steps Brief]]
- [ ] Close every session with `/session-close` — no exceptions
- [ ] Capture at least 3 lessons in `05 AI/CLAUDE CODE/resources/lessons.md` this week
- [ ] Run the first real audit of my case data (stored in my case project brief)
- [ ] Schedule Phase 2 check-in with my facilitator once Week 1 is complete

## Waiting For

| Who | What | Since |
|-----|------|-------|
| My facilitator | Phase 2 scheduling (once Week 1 complete) | <TODAY_DATE> |

## Plan

### Milestones

- [x] **M0: Phase 0 Complete** — vault + repo + CLAUDE.md chain + first Claude Code session. *(Completed <TODAY_DATE>)*
- [ ] **M1: Week 1 Sprint Complete** — audit case data, generate first deliverable, capture 3+ lessons.
- [ ] **M2: Phase 2 Session** — hands-on circle session with my facilitator + other members.
- [ ] **M3: First Real Automation** — at least one workflow running end-to-end saving me time weekly.
- [ ] **M4: Phase 3** — Agent teams, skills, MCP. Building my own tools.

### Sessions Log

| Date | Phase | Session | Notes |
|------|-------|---------|-------|
| <TODAY_DATE> | Phase 0 | 1-on-1 with my facilitator | Setup completed. Case project initialized. |

## Reference

- [[AI Acceleration Club]] — master program brief
- [[AI Acceleration Club - Phase 0 Playbook]]
- [[Next Steps Brief]] — week-by-week homework
- [[<Project Name>]] — my case project

## Log

| Date | Type | Entry |
|------|------|-------|
| <TODAY_DATE> | Milestone | Phase 0 onboarding session completed with my facilitator. Full vault + Claude Code + repo setup operational. |
```

> If your vault names your learning/AI area differently, point the `AREA:` field at that area instead of `[[Learning]]`.

Confirm. Move to Step 12.

---

## STEP 12: FIRST COMMIT

Go to the `<repo-name>` repo (in `~/dev` — see Step 6) and commit everything:

```bash
cd ~/dev/<repo-name>
git add -A
git commit -m "Initial project setup: CLAUDE.md, folder structure, README, .gitignore"
```

**Now put it on GitHub under my own account.** Create the repo on GitHub first, then push:

- **If `gh` is installed:** `gh repo create <repo-name> --private --source=. --remote=origin --push` creates the repo under my account and pushes in one step.
- **If `gh` is not installed:** create an empty repo named `<repo-name>` at https://github.com/new (under my account, no README/gitignore/license), then connect and push:

```bash
git remote add origin https://github.com/<my-username>/<repo-name>.git
git branch -M main
git push -u origin main
```

**If the push asks for credentials or fails auth:** `gh` is not required. The first push opens a browser via **Git Credential Manager** (bundled with Git for Windows) — sign in and authorize. Manual fallback: when git prompts for username/password, use my GitHub username and paste a **Personal Access Token** (github.com → Settings → Developer settings → Personal access tokens (classic), scopes `repo` + `workflow`) as the password. No admin rights needed for either path. (See Step 5.)

If we can't connect to GitHub right now, a local-only commit is fine — we connect later.

Confirm. Move to Step 12.5.

---

## STEP 12.5: AIAC CHEAT SHEET — GUARANTEED INBOX LOCATION

Create a single, predictable cheat-sheet file I can always find. **Exact path — do not vary:**

```
00 HUB/00 INBOX/AIAC Cheat Sheet.md
```

Save it to `00 HUB/00 INBOX/` — the vault's INBOX folder, created in Step 1. Do NOT route this to `05 AI/`, `CLAUDE CODE RESOURCES/`, or any "Cloud Code Resources" folder — those are floating locations I will not remember.

Fill in the repo name, project name, and my first name. Content (use 4-backtick fences when pasting this into Claude Code so the nested triple-backticks inside don't terminate early):

````markdown
# AIAC Cheat Sheet — Quick Reference

> **Location:** `00 HUB/00 INBOX/AIAC Cheat Sheet.md` — this is your one-stop quick-reference. Pin this file in Obsidian.

## Start a session

```bash
cd "[vault path]" && claude       # vault session (notes, projects, thinking)
cd ~/dev/<repo-name> && claude    # repo session (data, code)
```

## Resolve a project from anywhere

In a fresh Claude Code session (any cwd), type:

```
let's work on my <Project Name> project
```

The router (in `~/.claude/CLAUDE.md`) resolves to your **case project** brief in
`01 PROJECTS/<Project Name>/`. No `cd` needed.

To reach your **program journey** brief instead, say *"let's work on my AI Acceleration
journey"* — that one lives at `01 PROJECTS/AI Acceleration/<My Name>/`.

## Essential commands

| Command | What it does |
|---------|-------------|
| `/session-close` | Close session properly — updates brief, logs work, creates continuation prompt. **Never end without this.** |
| `/context` | Show context window usage |
| `/clear` | Reset session (after `/session-close`) |
| `/project-create` | Create a NEW project brief through guided Q&A — use this for project #2 onwards |
| `/help` | List available commands |
| `Shift+Tab Shift+Tab` | Enter Plan Mode (review before executing) |

## Context window thresholds

- ≤50% → keep working
- 50% → ideal compaction point (`/session-close` then `/clear`)
- 70% → quality cliff; do not cross mid-task

## When stuck

24 hours of solo debugging first. Then ping your facilitator with: the prompt, the error, and what you already tried.

If blocked on tool install / auth / MCP config → ping immediately (don't burn a day on infra).

## Where things live

- **Vault** = knowledge (notes, briefs, project management)
- **`~/dev/`** = code repositories. If it has its own `.git/`, it lives here.

## File anchors

- Vault root CLAUDE.md: `[vault]/CLAUDE.md`
- Repo CLAUDE.md: `~/dev/<repo-name>/CLAUDE.md`
- Case project brief: `[vault]/01 PROJECTS/<Project Name>/<Project Name>.md`
- AIAC Journey brief: `[vault]/01 PROJECTS/AI Acceleration/<My Name>/AI Acceleration Club - <My Name> Journey.md`
- Next Steps Brief (homework): `[vault]/00 HUB/00 INBOX/Next Steps Brief.md`
- Lessons log: `[vault]/05 AI/CLAUDE CODE/resources/lessons.md`
````

Confirm. Move to Step 13.

---

## STEP 13: SETUP COMPLETE — SUMMARY AND NEXT STEPS

Give me a final summary:

**What was set up:**
1. Obsidian vault with PARA structure + AI workspace — plus core Files-and-links settings (new notes → `00 HUB/00 INBOX`, wikilinks ON, all file types shown, auto-update internal links ON)
2. Vault CLAUDE.md (Claude's behavioral rules)
3. Claude Code global settings (permissions + sound notification + **context monitoring** — visible statusline bar, yellow ⚠ at 50% with a sound, 75% auto-compact threshold, and a hard-stop before auto-compaction so you can `/session-close` first)
4. Git configured with my identity
5. My case code repository at `~/dev/<repo-name>` — outside the vault — with CLAUDE.md (full project context + a pointer back to the vault brief)
6. Project Brief template for future projects
7. My case project brief with full detail (outcome, milestones, contacts) at `01 PROJECTS/<Project Name>/` — the case project's OWN folder (only the Journey brief lives under `01 PROJECTS/AI Acceleration/<My Name>/`)
8. Area MOC linking everything together
9. AI Acceleration Club Journey brief (tracks my progress through the learning program itself) — lives in my participant folder
10. AIAC Cheat Sheet at `00 HUB/00 INBOX/AIAC Cheat Sheet.md` (canonical quick-reference — always lives here)

**Where everything lives:**
- Vault: [show path] — **knowledge**: notes, briefs, project management
- Repo: `~/dev/<repo-name>/` — **code**, outside the vault. Rule of thumb: if it has its own `.git/`, it lives in `~/dev/`.
- Vault-side scripts (hooks, helpers, skills): stay in the vault under `05 AI/` — they aren't repos, so they don't move
- Claude Code config: ~/.claude/settings.json

**Essential commands:**

| Command | What it does |
|---------|-------------|
| `claude` | Start a Claude Code session |
| `/exit` | End session |
| `/clear` | Clear context, start fresh |
| `/help` | See all commands |
| `Ctrl+C` | Cancel current operation |
| `Escape` | Cancel current input |

**Two ways to use Claude Code:**

1. **In the vault** (`cd [vault path] && claude`) — for notes, project management, thinking, research
2. **In the repo** (`cd ~/dev/<repo-name> && claude`) — for data analysis, coding, building

Claude reads the CLAUDE.md in whichever folder you're in. It already knows everything about your project.

**This week's homework (3 tasks):**

1. **Open Claude Code daily** (even 10 minutes). In the `<repo-name>` folder, drop a data file and ask Claude to analyze it.
2. **Gather your initial data** and save it in `<repo-name>/data/` (or the relevant subfolder)
3. **Run this prompt** in the `<repo-name>` folder:

```
Read the CLAUDE.md and look at the files in the repo.
Create an inventory document mapping what data we have, what's missing,
and how each piece connects to the project goals.
```

**End with:** "You're set up. Every time you open Claude Code in your `<repo-name>` folder, it already knows your entire project. Just tell it what you need."
