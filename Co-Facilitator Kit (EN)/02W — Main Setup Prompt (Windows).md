---
title: "Main Setup Prompt (Participant, WINDOWS) — AI Acceleration Club Phase 0"
created: 2026-07-14
category: reference
tags: [aiac, phase0, co-facilitator-kit, participant, setup-prompt, main-setup, windows]
---

**Supports:** Block 2 of the session. You give this file to Claude Code by its path; you do not paste it.

# Main Setup Prompt (WINDOWS) — AI Acceleration Club Phase 0

> ## Three Windows rules — read before you start
>
> 1. **Give Claude this file by its path — don't paste it** (steps below). For the short lines you do
>    paste, use **right-click** in the terminal, not Ctrl+V: Ctrl+V often fails in Windows terminals.
> 2. **Run Claude Code from Git Bash**, not PowerShell and not CMD. The commands Claude runs are bash.
>    Git Bash comes with Git for Windows; launch it from the Start menu. (`where bash` returning nothing is normal.)
> 3. **Forward slashes `/` in every path — never backslashes `\`.** In Git Bash an unquoted `\` is
>    silently stripped and the command **fails with no visible error**, and the damage looks exactly
>    like an unrelated bug. Get your vault path with `pwd -W`, never plain `pwd`.

This is the prompt that builds your entire working environment: your Obsidian vault, your Claude Code configuration, and your first real project (we'll call it **the case**). It is self-contained: Claude reads this file and walks you through it one step at a time, starting with a short interview to get to know your work and pick the case together.

> **The method is plain files and standard tools** — Markdown notes in folders, a git repository, a
> few settings files. Claude Code is the recommended tool to drive them today, but nothing here locks
> you in: the vault and the repo work with any editor or AI tool you use later.

## How to give this file to Claude (read this first)

**Do not copy and paste this document.** It is long, and terminals cut long pastes short (the
Windows terminal is the worst offender). You hand Claude the file itself:

1. **Save this file on your computer** — your facilitator sends it to you, or download it from GitHub
   (open the file → **Download raw file**). If you ran the pre-flight check in Doc 01, it is already in your vault's
   `00 HUB/00 INBOX` folder; otherwise keep it somewhere you can find, such as `Downloads`.
2. **Copy the file's full path.**
   In File Explorer, hold **Shift**, right-click the file, choose **Copy as path**. (It comes with
   quotes and backslashes — that's fine for this one line; Claude handles it.)
3. **Open the terminal and start Claude Code** in the right folder: `cd` into your vault folder if
   it already exists (your pre-flight check may have created it), otherwise stay in your home folder.
   The easy way: in File Explorer open the vault folder, right-click an empty spot → **Open Git Bash
   here** (on Windows 11 it may be under **Show more options**). Type `pwd -W` to confirm the folder,
   then run `claude`.
4. If Claude Code asks **"Do you trust the files in this folder?"**, choose **Yes** for your vault
   or home folder. **On Windows the highlighted default is the "No, exit" option** — move to **Yes** first.
5. Type this, paste the path (right-click) where it says `<path>`, and press Enter:

   ```
   Read the file <path> and follow its instructions, starting at "FOR CLAUDE — START HERE".
   ```

6. **If you have to stop midway** (closing the terminal to install something, for example), start
   Claude again in your vault folder and type:
   `Read the file <path> and continue from Step N.`

> **On every permission prompt, choose plain "Yes" (or "No") — never "Yes, and don't ask again".**
> The "don't ask again" option saves a lasting rule in your settings that lets that command run
> without asking from then on, and the status check will then report it.

> **If Claude Code blocks an edit to `~/.claude/settings.json` and mentions "auto mode":** press
> **Shift+Tab** (each press switches the mode shown in the bottom bar) until it shows the normal
> **default** mode, without "auto". Some configuration edits are blocked in auto mode. When the edit is
> done, you can press Shift+Tab again to go back.

---

## FOR CLAUDE — START HERE

---

**Environment: Windows.** I run Claude Code in **Git Bash** (not PowerShell, not CMD). Use forward
slashes `/` in all paths. Do not offer me macOS commands such as `afplay`, `xcode-select`, `brew` or
`open`. If a step has a macOS branch and a Windows branch, take the Windows branch without asking.

You are helping me set up my complete working environment from scratch during a live AI Acceleration Club Phase 0 session. Before we build anything, you'll interview me to understand my work and help me pick my first real project (we'll call it **the case**). Then you'll walk me through the setup one step at a time, building everything around that case.

**Important rules for this setup:**
- Walk me through each step ONE AT A TIME. Do not dump everything at once.
- After each step, confirm what was created and ask "Ready for the next step?" before continuing.
- If something fails, help me troubleshoot before moving on.
- All Claude Code configuration and instruction files should live inside this Obsidian vault (not hidden away) so I can see and edit them in Obsidian.
- We start with a short interview (Step 0) so you understand my work and we choose the case together — then you build everything else around it.
- When a step says **STOP**, really stop: show me the message and wait until I tell you to continue.
- Never add a blanket or lasting permission for me. Anything that publishes (a `git push`, creating a GitHub repo) or changes settings outside this vault, you explain first and wait for my OK.
- Never open or print `~/.claude/settings.json` or any other file that may hold keys or tokens. Step 3 shows how to merge settings without reading them.
- If a file you are about to write already exists, **merge** into it: keep everything I already had, show me what you will add, and never delete existing content.
- Some actions need me in a **second terminal window** (logins that ask questions on screen, installers). When that happens, give me the exact line to type there and wait until I say it worked.

---

## STEP 0: WHO I AM & WHAT WE'LL BUILD (LIVE INTERVIEW)

Before touching any files, get to know me and help me pick my first real project — **the case**. Do this conversationally, ONE question at a time. Don't dump all the questions at once, and don't move on until I've answered.

**1. My identity.** First, check whether my Git identity is already set:

```bash
git config --global user.name
git config --global user.email
```

- If both print a value, confirm them with me: "I have you as `<name>` `<<email>>` — is that right for your Git commits?"
- If either is missing, ask me for my full name and the email I want on my commits. Mention that I can use my GitHub "no-reply" address (GitHub → Settings → Emails) if I'd rather not put my real email in commit history.

Hold my name and email — you'll use them in Git setup (Step 4), the vault CLAUDE.md (Step 2), the templates, and the briefs.

**2. My work.** Ask me: what do I do? My role, my organization or team, and the kind of work I'm responsible for day to day. Listen for the areas of my work life — these become my vault's areas of responsibility in Step 1.

**3. My problems.** Ask me to describe **1–3 real work problems** I'd like Claude to help with — the repetitive, manual, or slow tasks that eat my time. (I was asked to bring these to the session.) For each one, dig one level deeper: what data or tools are involved, how often it happens, and what "solved" would look like. Remind me that for today's first exercise we use **sample or non-sensitive data** — a made-up extract, an anonymized copy, or a public file with the same shape. Real business data can come later, once I know where everything goes.

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

## VAULT LOCATION CHECK — before Step 1

The vault is the folder where all my notes live. Claude Code works best when it is **started from
inside that folder**: the folder you launch from is Claude's working folder. Check where we are:

```bash
pwd -W
ls -a
```

(`pwd -W` prints the `C:/Users/...` form, which is the one to use everywhere. Plain `pwd` prints
`/c/Users/...`, which Windows tools and the router can't use.)

**Case A — we are already inside my vault** (a pre-flight check created it, or I made it before):
the listing shows a `.obsidian` folder, or I confirm this is my vault. Keep going with the hard rule below.

**Case B — there is no vault yet.** Create it, with these rules:

- **Name it permanently** — something like `AIAC-Vault`, my name, or my company. Not "Test",
  "Vault2" or "Draft". I will use it for years.
- **Default location:** `~/AIAC-Vault` in Git Bash, which is `C:/Users/YOUR-USER/AIAC-Vault` in File
  Explorer. A folder directly in my user folder is the safest choice.
- Create it with `mkdir -p ~/AIAC-Vault` (or the name I chose), then tell me to open **Obsidian** and
  choose **"Open folder as vault"** (on the start screen, or **Manage vaults** in the bottom-left vault
  switcher) and pick **exactly that folder**. **Never "Create new vault"** — that makes a second,
  different folder, and then Obsidian and Claude are looking at two different places.
- When I say it's open, check that Obsidian marked it: `ls -a ~/AIAC-Vault` must list a `.obsidian`
  folder. If it doesn't, Obsidian opened a different folder — **STOP** and help me fix that first.
- Then tell me to type `/exit`, `cd` into the vault, start `claude` again, and say
  `Read the file <path> and continue from Step 1.` From then on, Claude's working folder is the vault.

**⚠️ HARD RULE (both cases): the vault must NOT live inside a cloud-sync folder** — OneDrive, Dropbox,
Google Drive (`Google Drive`, `GoogleDrive`, `My Drive`) or iCloud (`iCloud`, `Mobile Documents`). Sync
clients fight Obsidian and git and corrupt files. If the path contains any of those, **STOP** and help
me move the vault to `~/AIAC-Vault` before anything else.

- `Documents` and `Desktop` are often silently redirected into OneDrive even when the path
  doesn't say so. If the vault is under `Documents` or `Desktop`, ask me whether OneDrive is backing up
  those folders (OneDrive icon → Settings → Backup); if yes or unsure, use `C:/Users/YOUR-USER/AIAC-Vault`.
- Also avoid `Downloads` and anything that gets cleaned up automatically.

Once the vault path is settled, tell me the full path you will use throughout the setup (from `pwd -W`, forward slashes).

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

**First, back up what already exists.** The merge script below backs up `settings.json` itself, before it changes anything: a private copy (only you can read it) of the file's current contents — of the real file, if `settings.json` is a link to one. An earlier backup is never overwritten: the first copy is `~/.claude/settings.json.bak`, later ones go to the next free name (`settings.json.bak.1`, `.bak.2`, …), and the script names the file it wrote on its `backup of your previous settings` line. For the router file, run this (on a brand-new machine it does nothing, which is fine; an existing backup is kept):

```bash
mkdir -p ~/.claude
[ -e ~/.claude/CLAUDE.md.bak ] || [ -L ~/.claude/CLAUDE.md.bak ] || cp -pL ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.bak 2>/dev/null
```

**Then merge — never overwrite, and never display what is already there.** `~/.claude/settings.json`
can hold API keys and tokens (for example in its `env` block), so **do not open, read or print the
existing file** — not even to show me what will change. The merge happens locally, with a small script
that prints only the kit's own entries and the *names* of the keys I already had:

1. Show me the block below (it holds only the kit's entries) and tell me which `Stop` line you'll use
   (see the note after the block).
2. Save the merge script further down as `~/.claude/aiac-merge-settings.py`, exactly as written.
3. Run it with the block on standard input (running Python isn't pre-approved, so Claude Code should ask first — approve it, but never with "don't ask again"), and show
   me its output. Its last line must start with `Verified:`. If it starts with `STOP:`, nothing was
   changed: show me the message and we fix it together (if an earlier run printed a `backup of your previous settings` line, my backup is the file named there).

   ```bash
   py ~/.claude/aiac-merge-settings.py - <<'JSON'
   <the JSON block below, with the Stop line for my OS>
   JSON
   ```

**If Python isn't available** (it's a Doc 01 prerequisite, so this shouldn't happen): if
`~/.claude/settings.json` does **not** exist yet, create it with exactly the block below; if it
**does** exist, **STOP** and help me install Python first. Never fall back to reading the file.

On Windows the Python command is `py` (the launcher from Doc 01); if `py` isn't found, use
`python`. Never `python3` — on Windows it opens the Microsoft Store.

The kit's block:

```json
{
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Bash(git status --short)",
      "Bash(git diff)",
      "Bash(git log --oneline)",
      "Bash(git remote -v)",
      "Bash(ls *)",
      "Bash(wc *)"
    ],
    "ask": [
      "Bash(cat *)",
      "Bash(head *)",
      "Bash(tail *)",
      "Bash(grep *)",
      "Bash(diff *)",
      "Bash(sed *)",
      "Bash(sort *)",
      "Bash(git show *)",
      "Bash(git -C *)",
      "Bash(git -c *)",
      "Bash(git add *)",
      "Bash(git commit *)",
      "Bash(git push *)",
      "Bash(gh repo create *)"
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

**The merge script** — save it as `~/.claude/aiac-merge-settings.py`. It adds each kit entry that is
missing, keeps every key, `allow`, `ask` and `deny` rule I already have, refuses to touch a file that
isn't valid JSON, first checks that the kit block has exactly the kit's shape (it stops on anything
else, even for a key my settings don't have yet), saves the private backup described above, writes
through a symlinked `settings.json` to the file it points at, keeps the file's access permissions,
re-reads the result to verify it, and prints nothing from my existing settings except key names:

```python
# aiac-merge-settings.py - merges the AIAC kit's entries into ~/.claude/settings.json.
# It never prints existing values: only the kit entries it added and the names
# of keys you already had. Usage: python3 aiac-merge-settings.py [--replace KEY] - < block
import json
import os
import re
import shutil
import sys

TARGET = os.path.expanduser("~/.claude/settings.json")
BACKUP = TARGET + ".bak"
DEEP = ("permissions", "hooks", "env")  # top-level objects merged key by key
HOOK_EVENTS = ("Stop", "UserPromptSubmit", "PreCompact")


def stop(message):
    sys.exit("STOP: " + message + " Nothing was changed.")


def number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0


def hook_groups(v):
    return isinstance(v, list) and all(
        isinstance(g, dict) and set(g) <= {"matcher", "hooks"}
        and isinstance(g.get("matcher", ""), str)
        and isinstance(g.get("hooks"), list) and len(g["hooks"]) > 0
        and all(isinstance(h, dict) and set(h) <= {"type", "command", "timeout"}
                and h.get("type") == "command"
                and isinstance(h.get("command"), str) and h["command"] != ""
                and ("timeout" not in h or number(h["timeout"]))
                for h in g["hooks"])
        for g in v)


# The only shapes a kit block may have. Checked before anything is merged,
# whether or not your settings already have the key.
SCHEMA = {
    "permissions": lambda v: isinstance(v, dict) and set(v) <= {"allow", "ask", "deny"}
    and all(isinstance(x, list) and all(isinstance(r, str) for r in x) for x in v.values()),
    "hooks": lambda v: isinstance(v, dict) and set(v) <= set(HOOK_EVENTS)
    and all(hook_groups(x) for x in v.values()),
    "env": lambda v: isinstance(v, dict) and all(isinstance(x, str) for x in v.values()),
    "statusLine": lambda v: isinstance(v, dict) and set(v) <= {"type", "command", "padding"}
    and v.get("type") == "command" and isinstance(v.get("command"), str) and v["command"] != ""
    and ("padding" not in v or (isinstance(v["padding"], int) and not isinstance(v["padding"], bool))),
}


def check_block(block):
    for key, val in block.items():
        name = key if re.match(r"^[A-Za-z][A-Za-z0-9_]{0,40}$", key) else "a key"
        if key not in SCHEMA:
            stop("the kit block has an entry the kit never uses (" + name + "); check it was copied whole.")
        if not SCHEMA[key](val):
            stop("the kit block's " + name + " entry has the wrong shape; check it was copied whole.")


def merge(dst, new, path, added, kept):
    for key, val in new.items():
        name = ".".join(path + [key])
        deep = isinstance(val, dict) and (path or key in DEEP)
        if key not in dst:
            dst[key] = val
            added.append(name)
        elif (isinstance(val, list) or deep) and type(dst[key]) is not type(val):
            stop(name + " in your settings is not a JSON " +
                 ("list" if isinstance(val, list) else "object") + ", so the kit entries can't be added.")
        elif isinstance(val, list):
            for item in val:
                if item not in dst[key]:
                    dst[key].append(item)
                    added.append(name + ": " + (item if isinstance(item, str) else "1 entry"))
        elif deep:
            merge(dst[key], val, path + [key], added, kept)
        elif dst[key] != val:
            kept.append(name)


def missing(dst, new, path, kept):
    gaps = []
    for key, val in new.items():
        name = ".".join(path + [key])
        if name in kept:
            continue
        if key not in dst:
            gaps.append(name)
        elif isinstance(val, list) and isinstance(dst[key], list):
            gaps += [name for item in val if item not in dst[key]]
        elif isinstance(val, dict) and isinstance(dst[key], dict) and (path or key in DEEP):
            gaps += missing(dst[key], val, path + [key], kept)
    return gaps


def replace(dst, new, dotted):
    keys = dotted.split(".")
    for key in keys[:-1]:
        new = new[key]
        if not isinstance(dst.get(key), dict):
            dst[key] = {}
        dst = dst[key]
    dst[keys[-1]] = new[keys[-1]]


def backup(real):
    """A private copy (0600) of the file's current bytes - the file a symlink
    points at, never the link - made once per run, before the change. An
    earlier backup is never overwritten: the copy goes to the first free name
    (settings.json.bak, then settings.json.bak.1, .bak.2, ...), printed below."""
    name, n = BACKUP, 0
    while os.path.lexists(name):
        n += 1
        name = BACKUP + "." + str(n)
    with open(real, "rb") as f:
        data = f.read()
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    return name


def main():
    args, to_replace = sys.argv[1:], []
    while len(args) >= 2 and args[0] == "--replace":
        to_replace.append(args[1])
        args = args[2:]
    try:
        if args and args[0] != "-":
            with open(args[0], encoding="utf-8") as f:
                block = json.load(f)
        else:
            block = json.load(sys.stdin)
    except (OSError, ValueError):
        stop("the kit block could not be read as JSON (check it was copied whole).")
    if not isinstance(block, dict):
        stop("the kit block is not a JSON object.")
    check_block(block)
    # Write through a symlinked settings.json to the file it points at.
    real = os.path.realpath(TARGET)
    current = {}
    if os.path.exists(real):
        try:
            with open(real, encoding="utf-8") as f:
                current = json.load(f)
        except ValueError:
            stop("~/.claude/settings.json is not valid JSON.")
        if not isinstance(current, dict):
            stop("~/.claude/settings.json is not a JSON object.")
    added, kept = [], []
    for dotted in to_replace:
        try:
            replace(current, block, dotted)
        except (KeyError, TypeError):
            stop(dotted + " is not in the kit block.")
        added.append(dotted + " (replaced, as you asked)")
    merge(current, block, [], added, kept)
    kept = [k for k in kept if not any(r.startswith(k + ".") for r in to_replace)]
    saved = None
    if added or not os.path.exists(real):
        os.makedirs(os.path.dirname(real), exist_ok=True)
        if os.path.exists(real):
            try:
                saved = backup(real)
            except OSError:
                stop("could not save a backup of ~/.claude/settings.json first.")
        tmp = real + ".aiac-tmp"
        if os.path.lexists(tmp):
            os.unlink(tmp)
        # Created private (0600) from the start, never briefly readable by others.
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2, ensure_ascii=False)
            f.write("\n")
        if os.path.exists(real):
            shutil.copymode(real, tmp)
        os.replace(tmp, real)
    if saved:
        print("backup of your previous settings (private): ~/.claude/" + os.path.basename(saved))
    for name in added:
        print("added: " + name)
    for name in kept:
        print("kept your existing value (not shown): " + name)
    with open(real, encoding="utf-8") as f:
        gaps = missing(json.load(f), block, [], kept)
    if gaps:
        sys.exit("STOP: still missing after the merge: " + ", ".join(gaps))
    print("Verified: settings.json parses and has every kit entry (%d added)." % len(added))


main()
```

> **What Claude Code already does without asking, and what these rules change.** Two defaults matter
> ([Claude Code permissions](https://code.claude.com/docs/en/permissions)): Claude's file tools (Read,
> Glob, Grep) work inside the folder you launched it from — your vault — without a prompt and ask before
> reading anywhere else; and a built-in set of read-only shell commands — `ls`, `cat`, `head`, `tail`,
> `grep`, `find`, `wc`, `diff`, `stat` and read-only `git` among them — runs **without a prompt, anywhere
> on your disk**.
> That set can't be switched off; the documented way to get a prompt for one of them is an `ask` (or
> `deny`) rule. So:
>
> - **`allow` holds only read-only commands:** five exact git commands (`git status`,
>   `git status --short`, `git diff`, `git log --oneline`, `git remote -v`) plus `ls` and `wc`. Nothing
>   in it writes, publishes or runs a program — not even `mkdir`: creating a folder isn't pre-approved either.
> - **`ask` turns the promised confirmations into rules.** `cat`, `head`, `tail`, `grep`, `diff`, `sed`,
>   `sort` and `git show` can print a file's contents, so they ask every time (inside the vault Claude
>   reads with its Read tool, which needs no prompt there). `git add`, `git commit`, `git push` and
>   `gh repo create` ask every time too, and so does any git command written as `git -C <folder> …` or
>   `git -c <setting> …` — forms that would otherwise slip past the `git push` rule. An `ask` rule wins
>   over any `allow` rule — including one saved by answering "Yes, and don't ask again" — and it still
>   asks in auto mode and in the sandbox's auto-allow mode (Doc 02-S). These fourteen rules are the
>   **only** commands guaranteed to ask every time. That is also why there is no `ask` rule for all of `git log` or `git diff`: it
>   would make the allowed `git log --oneline` and `git diff` ask too.
> - **Left out on purpose:**
>   - **Any git wildcard in `allow`.** Options such as `--output`, `--ext-diff` or `--template` can
>     write files, run programs or plant git hooks, and a `git diff *` allow rule would approve them
>     silently. (In `ask`, a wildcard can only add prompts.)
>   - **Python, Node and other interpreters, and `pip install`.** A script can read and write any file
>     as a subprocess, which permission rules cannot see. Pre-approving an interpreter would make any
>     `deny` rule you add later decorative. Without an allow rule, Claude Code normally asks before
>     running one — but not always: an approval you saved earlier ("Yes, and don't ask again"), a
>     permission mode that skips prompts, or the sandbox's auto-allow mode (Doc 02-S) can let a script run
>     without asking, because interpreters are not in the `ask` list. Approve each one when asked, never
>     with "don't ask again".
>   - **Bare tool names — `Read`, `Write`, `Edit`, `Glob`, `Grep`.** Listed without a path, a tool name
>     pre-approves that tool **anywhere on your disk**, which overrides Claude Code's default of working
>     in the folder you launched it from. Glob and Grep already search the vault without a prompt.
>
> **What this does and doesn't give you:** your vault is Claude's working folder. Claude's file tools
> ask before reading or writing outside it, and the `ask` rules cover the usual commands that print
> files or publish. They can't cover everything: the built-in read-only set is longer than this list and
> can't be switched off, so some read-only commands still run without asking anywhere on your disk —
> `ls`, `find`, `stat` and `wc` list names, sizes and line counts, and read-only `git` forms such as
> `git log -p` (or `git diff` with extra options) can print file contents. A script you approve can open
> any file. These rules match the command as Claude writes it: they are prompts, not a wall. If you want
> a hard, verifiable boundary, that is Doc 02-S (the opt-in sandbox).

**What this does:**
- **Permissions:** Pre-approves a few read-only, everyday commands so Claude doesn't ask every time, and makes the commands that print files, commit or publish ask every time. Everything else follows Claude Code's defaults. You can add more later, one rule at a time.
- **Sound hook:** Plays a sound when Claude finishes a task. Essential when you walk away and come back.

### Global Router — `~/.claude/CLAUDE.md`

Now create the **global router** at `~/.claude/CLAUDE.md`. This is the file that makes Claude Code load your vault rules at the start of EVERY session, no matter which folder you launch from. Two parts matter: the TOP is an **imperative router** (LOAD the vault CLAUDE.md at startup); the BOTTOM is your **profile** (who you are, what you're building).

Emit the file with this exact structure, filling `Who I Am`, the project brief path, and the repo path from the Step 0 interview and the case we chose. **If `~/.claude/CLAUDE.md` already exists** (it was backed up above), show it to me first: put this router block at the top and keep my existing content below it, unless I tell you otherwise.

```markdown
# CLAUDE.md — Global Router

## Default Workspace

All Claude Code sessions must load and follow the instructions in:

**`<VAULT_PATH>/CLAUDE.md`**

## Rules

1. At session start, read the vault CLAUDE.md above and follow its routing logic.
2. Default working directory is `<VAULT_PATH>/` unless I explicitly specify another.
3. **Code repositories live in `~/dev/<repo-name>` — never inside the vault.**
   (On Windows, `~/dev` in Git Bash is the same folder as `C:/Users/YOUR-USER/dev` in File Explorer — that is where to look for it later.)
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

Verify before moving on: read back the first 25 lines of `~/.claude/CLAUDE.md`, then run:

```bash
# This MUST print 0. Any other number means a backslash path got written into the router,
# which breaks it silently and looks like an unrelated bug.
grep -c '\\' ~/.claude/CLAUDE.md
```

Confirm: (0) the `grep` printed `0`, (1) the first section is `## Default Workspace` (not `## Who I Am`), and (2) no literal `<VAULT_PATH>` remains. The full outside-the-vault routing test runs later at the final validation gate.

Confirm. Move to Step 3.5.

---

## STEP 3.5: CONTEXT MONITORING (STATUSLINE + AUTO-COMPACT GUARDRAILS)

> **Why this step exists.** Claude Code has a limited context window. When it fills past its default threshold it **auto-compacts** — it summarizes and drops detail, and that is where sessions silently lose work. This step gives you a **visible bar** showing how full context is, an **audible warning at 50%**, and a hook that **turns automatic compaction off** so YOU decide when to compact (with `/session-close`, which preserves plans and tasks to disk before you `/clear`) instead of being surprised. When context reaches 75% the bar turns red and Claude Code skips the automatic compaction and carries on; if you keep going past the red bar, a later request can fail, and then you run `/compact` yourself. Four small layers — install one at a time and pipe-test each before moving on.

**OS:** Windows, Git Bash (declared at the top). The sound lines below already use the Windows beep.

**Then check for `jq`** (a small JSON tool that Layers 2 and 3 use): run `jq --version`.
- If it prints a version, continue.
- If it's missing (it is **not** included with Git for Windows): the install line is
  `winget install jqlang.jq`. Give me the line to run in a **second terminal window**, then have me close and reopen the
  terminal and resume from Step 3.5.
- **If `jq` can't be installed today** (no admin rights, no package manager): do Layers 1 and 4 only,
  skip Layers 2 and 3, and note it as a Week-1 item. The settings checks below don't need `jq`:
  the merge script from Step 3 verifies the file itself.

### Layer 1 — Raise the auto-compact threshold to 75% (all OS, do this even if you skip the rest)

Merge it into `~/.claude/settings.json` with the script from Step 3 (same rule: never open the file):

```bash
py ~/.claude/aiac-merge-settings.py - <<'JSON'
{ "env": { "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "75" } }
JSON
```

Validate: the script's last line starts with `Verified:`. If it reports
`env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` on a `kept your existing value` line, I already had a different value: tell me, and only
if I say so, run it again with `--replace env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` before the `-`.
This layer is OS-independent and is the single most important safety setting.

### Layer 2 — Visible statusline bar with a 50% warning

The statusline is the ONLY place that can see context %. Merge it with the script from Step 3:

```bash
py ~/.claude/aiac-merge-settings.py - <<'JSON'
{ "statusLine": { "type": "command", "command": "~/.claude/statusline.sh", "padding": 2 } }
JSON
```

If it reports `statusLine` on a `kept your existing value` line, I already have a status line: tell me and let me decide —
replace it (`--replace statusLine` before the `-`) or keep mine and skip the rest of this layer.

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
> 3. Try an absolute path for the status line script: run the merge script with
>    `--replace statusLine` before the `-`, and the full block
>    `{ "statusLine": { "type": "command", "command": "/c/Users/YOUR-USER/.claude/statusline.sh", "padding": 2 } }`.
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
{"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "⚠ CONTEXT ≥50%. Automatic compaction is off, so nothing compacts for you. Consider running /session-close then /clear to preserve plans/tasks before context runs out."}}
EOF
fi
```

`chmod +x ~/.claude/hooks/context-warn-prompt.sh`. **Pipe-test:**
```bash
touch /tmp/claude-ctx-warn-test
echo '{"session_id":"test"}' | bash ~/.claude/hooks/context-warn-prompt.sh | jq -e .
rm -f /tmp/claude-ctx-warn-test
```

### Layer 4 — Turn automatic compaction off (PreCompact hook)

Write `~/.claude/hooks/context-warn-precompact.sh`:

```bash
#!/bin/bash
cat <<'EOF'
{"decision": "block", "reason": "Automatic compaction is off (your context monitor blocks it). Run /session-close to preserve plans/tasks to disk (then /clear), or run /compact yourself."}
EOF
```

`chmod +x ~/.claude/hooks/context-warn-precompact.sh`. **Pipe-test:** `echo '{}' | bash ~/.claude/hooks/context-warn-precompact.sh | jq -e '.decision == "block"'`

> **What the hook does** ([hooks reference, PreCompact](https://code.claude.com/docs/en/hooks#precompact)): a PreCompact hook blocks compaction
> by printing `"decision": "block"` (or by exiting with code 2); the `continue` field is ignored on this event. The hook is
> wired to the `auto` trigger only, so in practice it **turns automatic compaction off**: when Claude Code tries to compact
> on its own (at 75%, from Layer 1), the attempt is skipped and the conversation continues. A `/compact` you type yourself
> still runs. The red bar is your signal: if you ignore it and keep working until context is completely full, a request can
> fail — run `/session-close` or `/compact` yourself at that point.

### Wire both hooks into settings.json + verify

**Merge** them with the script from Step 3 — it adds both entries next to any hooks I already have:

```bash
py ~/.claude/aiac-merge-settings.py - <<'JSON'
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command", "command": "bash ~/.claude/hooks/context-warn-prompt.sh", "timeout": 3 } ] }
    ],
    "PreCompact": [
      { "matcher": "auto", "hooks": [ { "type": "command", "command": "bash ~/.claude/hooks/context-warn-precompact.sh", "timeout": 3 } ] }
    ]
  }
}
JSON
```

Validate: the script's last line starts with `Verified:` — it re-reads the file, confirms it parses
and that every entry from Layers 1, 2 and these hooks is present, without printing anything else
from it. (Re-run it with the Layer 1 and Layer 2 blocks if you want them re-checked.)

Tell me: which files were created/modified, whether existing hooks/env had to be merged, any OS sound swap made, and that the new statusline and hooks take effect in my **next** Claude Code session (or after opening `/hooks` once). End with: "Context monitoring is on. Next session, when context crosses 50% you'll see a yellow ⚠ in the status bar, hear one alert, and get a reminder each turn until you compact."

Confirm. Move to Step 4.

---

## STEP 4: GIT SETUP

Check if Git is installed:

```bash
git --version
```

- If installed: tell me the version and move on.
- If not: tell me to install **Git for Windows** — in a second terminal window `winget install --id Git.Git -e`, or the installer from https://git-scm.com/download/win (accept the default options, and make sure **Git Bash** is included) — then close and reopen the terminal, and wait for me to confirm. Do NOT suggest `xcode-select` — that is macOS only.

Configure my Git identity using the name and email from Step 0 (if it was already set and I confirmed it, you can skip this; otherwise set it now):

```bash
git config --global user.name "<my full name>"
git config --global user.email "<my email>"
```

Confirm. Move to Step 5.

---

## STEP 5: GITHUB ACCOUNT AND `gh`

Ask me: **"Do you have a GitHub account? If yes, what's your username?"**

- If yes: note my username and move on.
- If no: walk me through creating one at https://github.com (just the signup). Then ask for my username.

`gh` is GitHub's command-line tool. It's part of the prerequisites (Doc 01), and we use it in
Step 12 to create my repo as **Private** and check it. Check it:

```bash
gh --version
gh auth status
```

- **`gh` isn't installed:** give me `winget install --id GitHub.cli -e` to run in a second terminal
  window, then have me close and reopen Git Bash and resume from Step 5.
- **`gh` is installed but not logged in:** don't run the login yourself — it asks questions on screen
  that you can't answer from here. Tell me to run this in a **second terminal window**, follow the
  browser, and tell you when it's done:

  ```
  gh auth login --hostname github.com --git-protocol https --web
  ```

  Then run `gh auth status` again, and connect git to that login so pushes don't ask for a password:

  ```bash
  gh auth setup-git
  ```

- **Check the account:** `gh api user --jq .login` must print the username I gave you. If it prints a
  different account, tell me and let me decide which one to use — don't decide for me.
- **`gh` isn't installed and can't be installed today** (for example, a work laptop without admin
  rights): note it, and we use the browser path in Step 12. **Git Credential Manager** (included with
  Git for Windows) opens a browser sign-in on the first push. **Never create a classic
  personal access token** for this — browser sign-in is safer and is all Phase 0 needs.

Move to Step 6.

---

## STEP 6: CREATE THE REPO — IN `~/dev`

**Critical:** the repo lives in `~/dev/<repo-name>`, NOT inside the Obsidian vault. Use the repo name we chose in Step 0.

Two workspaces, one rule to tell them apart: **if it has its own `.git/`, it belongs in `~/dev/`.** Knowledge (notes, briefs, project management) lives in the vault. Code repositories live in `~/dev/`. A git repo nested inside the vault fights Obsidian — Obsidian rewrites files just by displaying them, `.git` internals churn through sync, and data folders bloat the vault.

(This does NOT mean "code can't live in the vault." Small scripts that operate on the vault itself — hooks, helpers, one-off analysis — stay in the vault under `05 AI/`. They have no `.git` of their own. The rule is about *repositories*, not about *code*.)

> **⚠️ Windows:** `~/dev` works as written in **Git Bash**. In File Explorer the same folder is `C:/Users/YOUR-USER/dev`.

Because we're starting a brand-new project, there's nothing to clone yet — we create a fresh local repo, in a folder that **must not exist yet**:

```bash
mkdir -p ~/dev
if [ -e ~/dev/<repo-name> ]; then
  echo "STOP: ~/dev/<repo-name> already exists - not touched"
else
  mkdir ~/dev/<repo-name> && cd ~/dev/<repo-name> && git init -b main
fi
```

**If it prints `STOP`, stop.** An existing folder may already have its own history or an `origin` that
points somewhere else, and Step 12 would push from it. Don't reuse it on your own: show me what is
there (`ls -la ~/dev/<repo-name>`, and if it's a git repo, `git -C ~/dev/<repo-name> remote -v` and
`git -C ~/dev/<repo-name> log --oneline -5`) and let me choose. The default is a new repo name. Only if
I explicitly say this folder is mine and should be reused do we treat it as a recovery: we go through
its remotes and its history together, and I decide about each one before Step 7.

**Verify the repo landed in `~/dev` — DO NOT SKIP:**

```bash
cd ~/dev/<repo-name> && test "$(cd "$(git rev-parse --show-toplevel)" && pwd -P)" = "$(cd ~/dev/<repo-name> && pwd -P)" \
  && echo "OK — repo is at ~/dev/<repo-name>" \
  || echo "WRONG LOCATION: $(git rev-parse --show-toplevel)"
```

On Windows, git prints paths as `C:/Users/…` and Git Bash as `/c/Users/…`, so the check normalises
both sides with `cd … && pwd -P` before comparing. Without that, a correctly placed repo would show a
false `WRONG LOCATION`.

That one check asserts both that the repo IS at `~/dev/<repo-name>` and that it is NOT inside the vault. If it prints `WRONG LOCATION`, **STOP** — do not continue with the repo in the wrong place. Show me the path it printed and we'll fix it before Step 7.

Show me the output of the verify command.

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
data/processed/  — clean, final datasets (gitignored by default — see below)
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
data/processed/
```

All three `data/` folders are gitignored on purpose: the repo is private, but GitHub is still a
third party, and the first exercise uses sample data anyway. Later, remove the `data/processed/` line
only for files you are sure are safe to put on GitHub.

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

Work in the `<repo-name>` repo (in `~/dev` — see Step 6). **Start every command in this step with
`cd ~/dev/<repo-name> &&`, exactly as written below.** Claude Code moves its shell back to the vault
after any command that ends outside it, so a `git commit` or `git push` on a line of its own would run
in the wrong folder. Don't rewrite them as `git -C <path> …` either. (A `cd` followed by `git` asks for
approval every time — git could run that folder's hooks — so expect a prompt for each block: read it,
then approve.) Stage everything:

```bash
cd ~/dev/<repo-name> && git add -A && git status --short
```

**Show me the list of staged files and wait for my OK.** Point out anything that looks like it
shouldn't go to GitHub — a `.env` file, passwords or keys, real customer or business data, large
exports. If I'm unsure about a file, take it out of the commit and add it to `.gitignore`. Before the
first commit there is no `HEAD` yet, so `git restore --staged` doesn't work here — use this instead
(it only unstages; the file stays on disk), then show me the revised list:

```bash
cd ~/dev/<repo-name> && git rm --cached -- <file> && git status --short
```

Only after I confirm the list, commit:

```bash
cd ~/dev/<repo-name> && git commit -m "Initial project setup: CLAUDE.md, folder structure, README, .gitignore"
```

**Now put it on GitHub — as a Private repo under the right account.** Before creating anything,
confirm three things with me and wait for my "yes":

1. **Owner:** the account it will be created under — my username from Step 5, or, with `gh`:

   ```bash
   cd ~/dev/<repo-name> && gh api --hostname github.com user --jq .login
   ```

2. **Visibility: Private.**
3. **Name:** `<repo-name>`.

**With `gh`** (the default path):

```bash
cd ~/dev/<repo-name> && gh repo create <owner>/<repo-name> --private --source . --remote origin
```

**If it prints any error, STOP.** The name may be taken, an `origin` may already exist, or the login
may have failed. In every case: don't push, don't retry with other options, and don't run
`git remote add` or `git remote set-url` on your own. Show me the error and let me decide.

**Without `gh`** (browser path): walk me through https://github.com/new — **Owner** = my account,
**Repository name** = `<repo-name>`, select **Private**, and leave README, .gitignore and license
unticked. When I've created it, have me confirm the repo page shows the **Private** label. Then connect
it:

```bash
cd ~/dev/<repo-name> && git remote add origin https://github.com/<owner>/<repo-name>.git
```

If it prints any error (for example `remote origin already exists`), **STOP** the same way: don't push,
don't change the remote, show me the error.

**Before pushing, check where the push would really go — both paths, DO NOT SKIP:**

```bash
cd ~/dev/<repo-name> && git remote get-url --push --all origin && git log --oneline
```

1. **Destination.** The first command prints the address git will actually push to, after any rewrite
   rules in my git configuration. It must print **exactly one line**, and that line must be
   `https://github.com/<owner>/<repo-name>.git` (or, if I use SSH, GitHub's SSH form of that
   address) with the owner and name I confirmed. A different owner, a different name, another host or more than one line
   means **STOP** — don't push.
2. **Visibility.** With `gh`, ask GitHub itself about the exact host, owner and name from check 1:

   ```bash
   cd ~/dev/<repo-name> && gh repo view github.com/<owner>/<repo-name> --json nameWithOwner,visibility
   ```

   It must print my `nameWithOwner` **and `"visibility": "PRIVATE"`**. Without `gh`, I confirm the
   **Private** label on the repo page. If it isn't private, **STOP** and help me fix it first (repo
   **Settings → General → Danger Zone → Change visibility**).
3. **What will be sent.** A first push sends the **whole history**, not just today's files.
   `git log --oneline` lists every commit that will go up, and it must show only the commit we made
   today. Anything I don't recognize means **STOP**.

Show me all three results and wait for my "yes". Only then push. It asks for my approval every time: the
`ask` rule from Step 3 matches `git push` written exactly like this (and the `git -C` / `git -c`
forms), which is one more reason not to rewrite the command:

```bash
cd ~/dev/<repo-name> && git push -u origin main
```

**If the push asks for credentials or fails auth:** with `gh`, connect git to `gh`'s GitHub sign-in, then
run the exact push block above again (same command, same approval):

```bash
cd ~/dev/<repo-name> && gh auth setup-git --hostname github.com
```

Without `gh`, Git Credential Manager (included with Git for Windows) opens a browser sign-in — sign in
and authorize there. **Do not create a classic personal access token.** If it still fails, **STOP** and
show me the error so I can share it with my facilitator.

**Then verify the push really arrived** — ask GitHub, don't assume. Ask the exact address confirmed in
check 1 (write `<push-url>` as that one line, for example `https://github.com/<owner>/<repo-name>.git`),
not `origin`: a remote's fetch address can differ from the address git pushes to.

```bash
cd ~/dev/<repo-name> && git rev-parse HEAD && git ls-remote <push-url> refs/heads/main
```

Both must show the same commit ID: the second one comes from GitHub itself. With `gh`, confirm again
that the repo is still `PRIVATE`:

```bash
cd ~/dev/<repo-name> && gh repo view github.com/<owner>/<repo-name> --json nameWithOwner,visibility
```

If we can't connect to GitHub right now, a local-only commit is fine for today — say so clearly in the
summary, and we connect later.

Confirm. Move to Step 12.5.

---

## STEP 12.5: AIAC CHEAT SHEET — GUARANTEED INBOX LOCATION

Create a single, predictable cheat-sheet file I can always find. **Exact path — do not vary:**

```
00 HUB/00 INBOX/AIAC Cheat Sheet.md
```

Save it to `00 HUB/00 INBOX/` — the vault's INBOX folder, created in Step 1. Do NOT route this to `05 AI/`, `CLAUDE CODE RESOURCES/`, or any "Cloud Code Resources" folder — those are floating locations I will not remember.

Fill in the repo name, project name, and my first name. Content (the outer 4-backtick fence below is only there so the nested triple-backtick blocks display correctly; write the file without it):

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
3. Claude Code global settings, merged into what was already there without displaying it (a short list of read-only permissions, and `ask` rules so printing files, committing and publishing always ask — nothing that writes, publishes or runs scripts is pre-approved — plus sound notification + **context monitoring** — visible statusline bar, yellow ⚠ at 50% with a sound, 75% auto-compact threshold, and automatic compaction turned off so you decide when to `/session-close` or `/compact`)
4. Git configured with my identity
5. My case code repository at `~/dev/<repo-name>` — outside the vault — with CLAUDE.md (full project context + a pointer back to the vault brief), pushed to GitHub as a **Private** repo (or local-only for now, if we couldn't connect)
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

1. **Open Claude Code daily** (even 10 minutes). In the `<repo-name>` folder, drop a sample (or non-sensitive) data file into `data/raw/` and ask Claude to analyze it.
2. **Gather your initial data** and save it in `<repo-name>/data/raw/` (gitignored — it stays on your machine)
3. **Run this prompt** in the `<repo-name>` folder:

```
Read the CLAUDE.md and look at the files in the repo.
Create an inventory document mapping what data we have, what's missing,
and how each piece connects to the project goals.
```

**End with:** "You're set up. Every time you open Claude Code in your `<repo-name>` folder, it already knows your entire project. Just tell it what you need."
