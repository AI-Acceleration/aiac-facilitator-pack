---
title: "Pre-Session Setup Instructions (Participant) — AI Acceleration Club Phase 0"
created: 2026-07-14
category: reference
tags: [aiac, phase0, co-facilitator-kit, participant, pre-session, setup]
---

**Supports:** Before the session. You get this about a week ahead: start as soon as you can, not the night before, and finish every step, including the **pre-flight** at the end, before your facilitator's cutoff date.

# Pre-Session Setup — AI Acceleration Club Phase 0

Welcome to Phase 0 of the AI Acceleration Club. Before your live session you'll install a handful of tools. Each one has a specific job in the system we'll build together. For every step you'll find a one-line explanation of *why* you need it, plus a ready-to-paste prompt for Claude (at claude.ai). The prompt walks you through the install and helps if something goes wrong.

The last step is the **pre-flight**. Claude Code creates your vault, checks every tool and ends with one line that you send to your facilitator. That line is how your facilitator knows you're ready. **The pre-flight is required.**

**Where to send things:** [SET: your support channel]

**New words?** Your facilitator sends **Doc 07 — Vocabulary** together with this document: every term in the kit (vault, skill, plugin, brief, router…) on one page. Keep it at hand.

> **If you get stuck on a command:** copy the command you typed and the error message, and paste them into the same Claude conversation. Claude reads them and gives you the next step until it works. You're the eyes and hands; Claude is the brain.
> **Before you paste, glance over it.** Never paste a password, a token (long random strings, often starting with `ghp_`, `gho_` or `sk-`), a private key or a recovery code into any chat. If an error message contains one, delete it first.

> **Download only from the official sites named in each step.** For those official downloads, a warning such as "unidentified developer" (macOS Gatekeeper) or "Windows protected your PC" (SmartScreen) is common and expected. On a Mac: right-click the app → **Open**, or allow it in **System Settings → Privacy & Security**. On Windows: **More info → Run anyway**. If a warning appears for something you did **not** download from the official site, or it mentions a virus, stop and ask your facilitator.

## Before You Start — Your Machine

**Use a device you're allowed to use for this work.** On a company laptop, ask IT **before the session** for:

1. **Permission and admin rights.** Installing Git, Claude Code and the other tools needs administrator rights. Most IT teams can grant them temporarily for an install window. Ask now, not on the day.
2. **Claude Code allowed.** The official installers (`claude.ai/install.sh` on Mac/Linux, `claude.ai/install.ps1` on Windows) must not be blocked, and nothing (a firewall or data-loss-prevention policy) may block `claude.ai` or `api.anthropic.com`.
3. **GitHub allowed.** `github.com`, including `git push` over HTTPS, must not be blocked.

If your company doesn't allow this on its machines, talk to your facilitator. Don't move work data to a personal computer against your company's policy. The first exercise works with **sample data**, so a personal machine is fine as long as no confidential data goes on it.

**Is your machine ready?** Old or very slow machines make the session painful. Check now: an operating system that still gets updates, at least 8 GB of memory, and a few GB of free disk space. If you're unsure, ask your facilitator. They may give you a **cutoff date** by which your machine and your pre-flight must be ready.

**VPN.** In countries or regions where Claude is not available, a VPN has to stay **ON** for the whole setup and every time you use Claude afterward. Turning it off midway breaks logins and downloads. If a *company* VPN blocks `claude.ai`, `github.com` or `obsidian.md`, ask IT to allow those three domains. Don't switch a company VPN off against policy.

## Windows Only — Read Before You Start

If you're on a Mac or Linux, skip to the table below. On Windows, read **all** of these first. Each one has cost a real participant real time.

> **This section is prose, not commands.** Read it; don't paste it into a terminal. (Pasting prose
> into PowerShell produces a `ParserError` and can leave you stuck at a `>>` continuation prompt.
> An apostrophe in a word like *you're* opens a quote that never closes. If that happens, press
> **Ctrl+C** and carry on.)

**0. Claude Code does not run on the free Claude plan.** This is gate zero and it blocks everything
else. Anthropic's docs are explicit: *"The free Claude.ai plan does not include Claude Code access."*
Do Step 1 **before** you try to install anything. It self-resolves: if `claude` opens and you're
logged in, the upgrade worked. A participant in another cohort was stuck for weeks on exactly this.

**0.5. Know which window you're typing in. This is the #1 Windows confusion.** Windows gives you
three, and they are not interchangeable:

| Window | Use it for |
|---|---|
| **PowerShell** | Only for installing Claude Code (the `irm ... \| iex` command in Step 4) |
| **Git Bash** | **Everything else in this kit.** It comes with Git for Windows (Step 2). Open it from the Start menu. |
| **CMD** (the black `C:\>` box) | Nothing here. If your error messages start with `C:\>`, you're in the wrong window. |

Also normal and **not** a failed install: `where bash` returns nothing. Git for Windows installs
Git Bash but doesn't put `bash.exe` on your PATH. Launch Git Bash from the Start menu instead.

**1. Paste with right-click.** In Git Bash, PowerShell and Windows Terminal, Ctrl+V often doesn't work. Use **right-click** (or the mouse scroll-wheel click, or `Shift+Insert`).

**2. Long texts get cut when pasted.** The Windows terminal can silently truncate a long paste. That's why, from the pre-flight on, long prompts are never pasted: you'll give Claude the **path** of the file and tell it to read the file. The pre-flight practises this with you.

**3. Always use forward slashes `/` in file paths, never backslashes `\`.**
Write `C:/Users/YOUR-USER/AIAC-Vault`, not `C:\Users\YOUR-USER\AIAC-Vault`. This one matters more
than it looks: in Git Bash an unquoted `\` is silently stripped and **the command fails without any
visible error**. The resulting breakage looks identical to an unrelated bug, so you'd spend the
session debugging the wrong thing. To see a path in the right form, Claude uses `pwd -W` (which
prints `C:/Users/...`), not plain `pwd` (which prints `/c/Users/...`).

**4. The PATH step after installing Claude Code.** The Claude Code installer can finish successfully and still say, in its own output, that it did **not** add `C:\Users\YOUR-USER\.local\bin` to your PATH. Then `claude` is "not recognized". The fix: Start → "Edit the system environment variables" → **Environment Variables** → select **Path** under **System variables** (or under User variables if you don't have admin rights) → **New** → paste that folder → OK, then open a **new** window. Step 4's prompt walks you through it.

**5. "Do you trust the files in this folder?"** The first time you run `claude` in a folder, Claude Code asks this. For your own home folder and, later, your vault, choose **Yes**. The default answer is No, and No simply exits.

---

## What Each Tool Is For

| Tool | Why you need it |
|---|---|
| **Claude** (paid plan) | The AI assistant. It's the brain behind everything else. The free plan does not include Claude Code. |
| **Git** | Tracks every change to your project files, so you never lose work and can go back. |
| **GitHub account** | The cloud backup for that work. Your project repository lives there, **private**. |
| **Ghostty** (Mac, optional) | A modern terminal app. The Mac's built-in Terminal works too. |
| **Claude Code** | Claude in your terminal: it reads your files, writes code, builds reports and automates tasks. |
| **`gh`** (GitHub CLI) | GitHub's terminal tool. Claude uses it to create your private repository during the session. You sign in once through your browser. |
| **Python 3** | Several skills use it behind the scenes to process files. You won't program in Python. |
| **`jq`** | A tiny tool for reading JSON. The context bar you set up in the session depends on it: without `jq` the bar never appears, and there's no error message. |
| **Obsidian** | Your "second brain": the app where your notes, projects and everything you make with AI live, linked together. |
| **Transcription tool** (optional) | Captures meetings as text so Claude can turn them into minutes. Any tool works, or none. |

---

## Step 1 — Your Claude Plan (Pro is enough to start)

Claude is the AI assistant you'll use for everything. **Claude Code needs a paid plan.** The default is **Claude Pro** (about $20/month), which includes Claude Code and is enough to start. Upgrade to Max only if you keep hitting the usage limits. Current prices and limits: [claude.com/pricing](https://claude.com/pricing). Every plan has usage limits that reset every few hours and every week. **Doc 06 — Pro Plan Survival Kit** explains how to make Pro last.

This step is manual:

1. Go to claude.ai and sign in (or create your account).
2. **Settings → Billing** → choose **Pro**.
3. Complete the payment.

> If your company gives you Claude through a **Team or Enterprise** account, use that account instead and skip the payment. Tell your facilitator. The pre-flight detects this too.

## Step 2 — Your GitHub Account and Git

Two things that go together but aren't the same:

- **Git** is a program on your computer. It tracks every change to your project files.
- **GitHub** is a free cloud account (github.com). Your project gets backed up there, in a **private** repository that only you can see.

**FIRST, create your GitHub account** (manual, 2 minutes):

1. Go to https://github.com
2. Click **Sign up** and create your account (it's free).
3. Confirm your email and note your GitHub **username**. You'll send it to your facilitator.

**THEN, install Git.** Paste the prompt for your system into claude.ai.

**Mac:**

```
I need to install Git on my Mac. Walk me through it step by step:
1. First tell me how to check whether I already have it (git --version in the Terminal).
2. If I don't, the command is: xcode-select --install
   (Apple's command line tools: they bring Git and also Python 3).
3. Verify with git --version.
If anything fails, help me fix it.
```

**Windows:**

```
I need to install Git on my Windows PC. Walk me through it step by step:
1. First tell me how to check whether I already have it (git --version).
2. If I don't, the command is: winget install --id Git.Git -e
   If winget doesn't work, tell me how to use the installer from https://git-scm.com/download/win
   Keep the default options: they install Git Bash, which I'll use for everything.
3. Open a NEW Git Bash window from the Start menu and verify with git --version.
If anything fails, help me fix it.
```

**Linux:** install `git` with your package manager (for example `sudo apt install git`) and check `git --version`.

## Step 3 — Your Terminal

The terminal is the window where you'll work with Claude Code.

- **Mac:** the built-in **Terminal** app works. If you'd like a nicer one, install **Ghostty** (optional) by pasting this into claude.ai:

  ```
  I want to install Ghostty, a terminal app, on my Mac. Walk me through it:
  1. Download it from ghostty.org.
  2. Install it like any other Mac app.
  3. Open it and check that it works.
  If anything fails, help me fix it.
  ```

  From here on, "terminal" means Terminal or Ghostty, whichever you chose.
- **Windows:** your terminal is **Git Bash** (from Step 2). PowerShell is used only for Step 4.
- **Linux:** your usual terminal.

## Step 4 — Claude Code

Claude Code is the version of Claude that runs in your terminal. It reads your files, writes code, builds reports and automates tasks. This is where the real work happens.

**Mac or Linux:** open your terminal and paste this into claude.ai:

```
I need to install Claude Code (Anthropic's terminal tool). Walk me through it step by step:
1. Use Anthropic's native installer: curl -fsSL https://claude.ai/install.sh | bash
   (No Homebrew, no sudo, and it keeps itself updated.)
2. Verify with: claude --version
   If the command isn't found, help me make sure ~/.local/bin is on my PATH.
3. Walk me through logging in with my Claude account.
If anything fails, help me diagnose it.
```

> **Why the native installer:** it's what Anthropic's own setup docs recommend, and it keeps
> itself current. A Homebrew install does **not** update itself, so you'd silently drift onto an
> old version.

**Windows:** Claude Code is installed from **PowerShell** (not Git Bash, not CMD). Git for Windows (Step 2) must already be installed. Paste this into claude.ai:

```
I need to install Claude Code (Anthropic's terminal tool) on Windows. Walk me through it step by step:
1. In PowerShell, the command is: irm https://claude.ai/install.ps1 | iex
2. IMPORTANT: read the installer's output with me before I close the window. It can finish
   successfully and still say it did NOT add C:\Users\YOUR-USER\.local\bin to my PATH.
   If it says that, walk me through adding that folder to Path in Environment Variables
   (System variables, or User variables if I don't have admin rights). Don't use setx.
   Then I open a NEW window.
3. Open a NEW Git Bash window and verify with: claude --version
   If I get "'claude' is not recognized", it's almost certainly the PATH step above: fix that first.
4. Walk me through logging in with my Claude account.
If anything fails, help me diagnose it.
```

**Verify with Claude.** From now on Claude Code can check its own work. In your terminal (Git Bash on Windows), type `claude`, answer **Yes** if it asks whether you trust the folder, and paste:

```
Run git --version and claude --version. Tell me READY or MISSING for each, nothing else.
```

> **From here on you can choose where to paste the install prompts:** in claude.ai (you run the
> commands yourself) or in Claude Code (Claude runs them and asks before each one). One exception:
> **logins** (`gh auth login`, the Claude login) ask questions on screen that Claude can't answer, so you
> run those yourself, in a separate terminal window.

## Step 5 — `gh` and Your GitHub Login

**Required.** During the session Claude uses `gh` to create your **private** repository on GitHub. You sign in through your browser. There's no token to copy or store.

**Mac:**

```
I need to install the GitHub CLI (gh) on my Mac and sign in. Walk me through it step by step:
1. If I have Homebrew (brew --version answers), the command is: brew install gh
   If I don't, tell me how to use the macOS installer (.pkg) from https://cli.github.com
2. Verify with: gh --version
3. Sign in with: gh auth login --hostname github.com --git-protocol https --web
   It shows a one-time code and opens the browser: tell me where to enter the code and what I'm authorizing.
4. Verify with: gh auth status
   It must say I'm logged in to github.com with my username.
If anything fails, help me fix it.
```

**Windows:**

```
I need to install the GitHub CLI (gh) on Windows and sign in. Walk me through it step by step:
1. The command is: winget install --id GitHub.cli -e
   If winget doesn't work, tell me how to use the .msi installer from https://cli.github.com
2. Open a NEW Git Bash window and verify with: gh --version
3. Sign in with: gh auth login --hostname github.com --git-protocol https --web
   It shows a one-time code and opens the browser: tell me where to enter the code and what I'm authorizing.
4. Verify with: gh auth status
   It must say I'm logged in to github.com with my username.
If anything fails, help me fix it.
```

**Linux:** install `gh` (https://github.com/cli/cli/blob/trunk/docs/install_linux.md), then `gh auth login --hostname github.com --git-protocol https --web` and check `gh auth status`.

If `gh` can't be installed on your machine (for example a locked-down company laptop), tell your facilitator **before** the session. There's a browser-only path, but it takes longer and your facilitator needs to know in advance. Do **not** create a "personal access token" as a workaround.

**Verify with Claude:**

```
Run gh --version and gh auth status. Tell me READY if I'm logged in to github.com, MISSING if not.
Don't run the login yourself.
```

## Step 6 — Python 3

**Mac:** it usually came with Step 2. Paste into claude.ai (or Claude Code):

```
I need to check that I have Python 3 on my Mac. Walk me through it:
1. In the terminal: python3 --version
2. If it answers with a 3.x version, I'm done.
3. If it doesn't answer, or offers to install the developer tools, accept. If it's still missing,
   install it with brew install python (if I have Homebrew) or the installer from https://www.python.org/downloads/
4. Verify again with python3 --version
If anything fails, help me fix it.
```

**Windows:**

```
I need to install Python 3 on Windows. Walk me through it step by step:
1. First check whether I already have it: in Git Bash, py --version
2. If I don't, the command is: winget install --id Python.Python.3.12 -e
3. Open a NEW window and verify with: py --version
   On Windows, Python is called with py. If python3 opens the Microsoft Store, ignore it: that's a Windows shortcut, not Python.
If anything fails, help me fix it.
```

**Linux:** `sudo apt install python3` (or your package manager), then `python3 --version`.

**Verify with Claude:**

```
Run python3 --version (on Windows: py --version). Tell me READY if it's version 3.x, MISSING if not.
```

## Step 7 — jq (small, but the session depends on it)

macOS 15 and later include `jq`; older macOS and Windows don't, and Git for Windows doesn't include it either. Check with `jq --version` and install it now if it's missing.

**Mac:**

```
I need to install jq (a small command-line JSON tool) on my Mac. Walk me through it step by step:
1. If I have Homebrew (brew --version answers), the command is: brew install jq
2. If I don't: tell me which chip I have (uname -m: arm64 = Apple Silicon, x86_64 = Intel),
   create ~/.local/bin if it doesn't exist, download the matching file from
   https://github.com/jqlang/jq/releases/latest (jq-macos-arm64 or jq-macos-amd64) to ~/.local/bin/jq,
   make it executable (chmod +x) and make sure ~/.local/bin is on my PATH permanently.
3. Verify with: jq --version
If anything fails, help me fix it.
```

**Windows:**

```
I need to install jq (a small command-line JSON tool) on Windows. Walk me through it step by step:
1. The command is: winget install --id jqlang.jq -e
2. Open a NEW Git Bash window so the PATH refreshes.
3. Verify with: jq --version
If anything fails, help me fix it.
```

**Linux:** `sudo apt install jq`, then `jq --version`.

**Verify with Claude:**

```
Run jq --version. Tell me READY or MISSING.
```

## Step 8 — Obsidian

Obsidian is a note-taking app that becomes your "second brain": the place where your projects, ideas and everything you create with AI live and link to each other.

Paste this into claude.ai:

```
I need to install Obsidian on my computer. Ask me which operating system I use if you need to.
Walk me through it step by step:
1. Tell me which page to download it from (obsidian.md).
2. Explain how to install it on my system.
3. Once it's installed, just check that it opens.
4. Do NOT create a vault: the pre-flight creates it in the last step.
If anything fails, help me fix it.
```

**Verify:** Obsidian opens. If it shows a welcome screen offering to create a vault, close it. **Don't create a vault yourself.**

## Step 9 — Meeting Transcription (optional, any tool)

After the session you can turn meetings into minutes with Claude. You need the meeting as text, and any of these works:

- **Granola** (granola.ai), an AI meeting recorder. Any email works. At the login screen use **Continue with Google** (or Microsoft), not the **SSO** button, which is for enterprise accounts only.
- **Another transcription tool** you already use (Zoom, Teams, Meet, Otter and others).
- **No tool at all.** You paste a transcript into Claude by hand.

Tell your facilitator which one you'll use. Nothing here blocks the session.

> **Recording needs consent.** Only record a meeting when everyone in it has agreed. Your facilitator will ask you before recording your session, and you can say no.

If you choose Granola, this prompt walks you through it (paste into claude.ai):

```
I need to install Granola (granola.ai), an AI meeting recorder. Walk me through it step by step:
1. Tell me which page to go to and how to install it on my computer.
2. Help me create the account with "Continue with Google" or Microsoft (not SSO).
3. Connect my calendar and check that my meetings show up.
4. Let's record 30 seconds of me talking and confirm it creates a transcript and a summary.
If anything fails, help me diagnose it.
```

---

## Step 10 — The Pre-Flight (required)

The pre-flight gets your computer ready for the session in about 10 minutes. Claude Code:

- creates your vault in a safe place (never inside a cloud-synced folder such as OneDrive, Dropbox, Google Drive or iCloud),
- has you open it in Obsidian and checks that Obsidian opened **that same folder**,
- moves your kit files into the vault and practises loading a prompt **by file**,
- checks every tool and your GitHub login,
- ends with **one line** that you send to your facilitator.

**Before you start:** Steps 1 to 8 are done. Your facilitator has sent you these kit files: this document, the **Main Setup Prompt** and the **Skills & Config Setup Prompt** (on Windows, their Windows editions `02W` and `03W`), and Doc 07 — Vocabulary. Save them all in your **Downloads** folder and don't rename, open or move them. The pre-flight moves them.

**How to run it.** You don't paste the long prompt below. You tell Claude to read it from this file:

1. Open your terminal (on Windows: **Git Bash**) and type `claude`. If it asks whether you trust the folder, choose **Yes**.
2. Paste this short prompt (on Windows: right-click to paste) and press Enter:

   ```
   Read the file in my Downloads folder whose name contains "Pre-Session Setup Instructions". Find the section "PRE-FLIGHT PROMPT" and follow only the instructions inside its code block.
   ```

3. Answer Claude's questions. Claude's **last line** says `PREFLIGHT: READY …` or `PREFLIGHT: MISSING …`.

If Claude can't find the file (for example, you saved it somewhere else), drag the file into the terminal window. That pastes its path. Then type `Read this file, find the section "PRE-FLIGHT PROMPT" and follow only the instructions inside its code block.` As a last resort on Mac or Linux, copy the block below and paste it.

### PRE-FLIGHT PROMPT

```
PRE-FLIGHT — AI Acceleration Club Phase 0

Hi Claude. I'm getting ready for my Claude Code onboarding session. Let's run a pre-flight: set up my Obsidian vault and check my tools. Go in order, one point at a time, and wait for me when a point needs me. Don't install anything or change any setting without asking me first. Never read, print or ask me for a password, token or key.

0. MY COMPUTER
   - Tell me which system you detect: macOS, Windows (Git Bash), WSL or Linux.
   - On Windows: run commands in Git Bash, write paths with forward slashes (C:/Users/...), never backslashes, and show me paths with pwd -W instead of pwd.

1. MY VAULT (the folder that becomes my second brain)
   - Ask me whether I already have an Obsidian vault I want to use. If yes, ask for its full path and use that folder: don't create another one.
   - If not, create it as AIAC-Vault directly inside my home folder: $HOME/AIAC-Vault (on Windows that is C:/Users/YOUR-USER/AIAC-Vault). Ask me only whether I want a different name; a name without spaces is easiest.
   - HARD RULE: the vault must never live inside a cloud-synced folder. If the full path contains OneDrive, Dropbox, Google Drive, GoogleDrive, My Drive, iCloud or Mobile Documents, don't use it: tell me why and propose $HOME/AIAC-Vault instead. Don't put it in Documents or Desktop either: on Windows they are often redirected into OneDrive, and on a Mac they may be synced to iCloud.
   - Create only the vault folder and, inside it, "00 HUB/00 INBOX". Nothing else: the Main Setup Prompt builds the rest during the session. If a folder already exists, leave it as it is.
       mkdir -p "$HOME/AIAC-Vault/00 HUB/00 INBOX" && cd "$HOME/AIAC-Vault" && pwd
     (On Windows use pwd -W. If I chose another path or name, use that one.)
   - Show me the full vault path. I'll need it in the session.

2. OBSIDIAN OPENS THE SAME FOLDER
   - Tell me to open Obsidian and choose "Open folder as vault", then select the folder from point 1. If Obsidian already has a vault open, it's under the vault icon at the bottom left: "Manage vaults" then "Open folder as vault". NEVER "Create new vault": that makes a second vault somewhere else.
   - Wait until I say "done". Then check that the hidden folder .obsidian now exists inside the vault folder (ls -a). If it doesn't, Obsidian opened a different folder: let's repeat point 2.

3. MY KIT FILES AND LOADING A PROMPT BY FILE
   - Look in my Downloads folder for the kit files my facilitator sent me: names containing "Pre-Session Setup Instructions", "Main Setup Prompt", "Skills & Config Setup Prompt" or "Vocabulary". If there is more than one copy of a file (for example with "(1)" in the name), take the newest and tell me which one you took.
   - Move them into "00 HUB/00 INBOX" in the vault, removing any "(1)" from the name. If the Main Setup Prompt or the Skills & Config Setup Prompt isn't there, carry on and note "setup files" as missing.
   - Show me what is now in "00 HUB/00 INBOX".
   - Now let's practise how long prompts are loaded in the session. Tell me to open "00 HUB/00 INBOX" in Obsidian, right-click the Main Setup Prompt file (or this Pre-Session file if the setup file is missing), choose "Copy path" and then the full system path (not the "Obsidian URL"), and paste it here. Check that the path points to the file (test -f). On Windows, change any \ to / before testing. Do NOT run that file now: we're only checking that the path works.

4. MY TOOLS
   Run these and show me what each one printed:
     git --version
     gh --version
     gh auth status
     python3 --version     (on Windows: py --version)
     jq --version
     claude --version
   - gh auth status must say I'm logged in to github.com. If it doesn't, do NOT run the login yourself: it asks questions on screen that you can't answer from here. Tell me to run this in a SECOND terminal window, follow the browser, and tell you when I'm done:
       gh auth login --hostname github.com --git-protocol https --web
     Then run gh auth status again.
   - Once I'm logged in, run gh api user --jq .login and show me my GitHub username. I'll send it to my facilitator.
   - On Windows, Python is called with py. If python3 opens the Microsoft Store, ignore it: that's a Windows shortcut, not Python.
   - If something isn't installed, tell me which step of my Pre-Session Setup Instructions installs it and wait. When I say I'm done, check again; a fresh install sometimes needs a new terminal window. If it's still missing, note it as missing.
   - My Claude account type. Run this; it shows only the account type, nothing else:
       grep -o '"organizationType": *"[^"]*"' "$HOME/.claude.json"
     claude_team or claude_enterprise means a team account: my organization's admin decides which connectors I see and may hand out plugins. Anything else, or no output, means a personal account. Neither one is a problem.

5. MEETING TRANSCRIPTION (never a blocker)
   - Ask me how I'll capture meetings after the session: Granola, another transcription tool, or pasting transcripts by hand. Any answer is fine. Just note it.

6. SUMMARY
   - Give me a table with each point and READY or MISSING: vault (not in a synced folder), Obsidian opened the same folder (.obsidian found), setup files in the INBOX, "Copy path" works, git, gh, gh logged in, Python 3, jq, Claude Code. Add a row "Claude account" (personal or team), a row "GitHub username" and a row "transcription" with my answer.
   - Under the table, the line I'll use in the session to enter my vault: cd "<full vault path>"
   - End with ONE exact line and nothing after it:
       PREFLIGHT: READY · ACCOUNT: personal
     if everything is ready, or
       PREFLIGHT: MISSING <what is missing, comma-separated> · ACCOUNT: personal
     for example: PREFLIGHT: MISSING jq, gh login · ACCOUNT: team
     Write team instead of personal for a Team or Enterprise account.
```

### After the Pre-Flight

- **Send the last line** (`PREFLIGHT: READY …` or `PREFLIGHT: MISSING …`) and your **GitHub username** to your facilitator at [SET: your support channel]. If it says `MISSING`, ask for help right away, **before** the session. Missing pieces take minutes to fix now and half an hour live.
- **Keep the `cd "…"` line** Claude gave you. In the session you use it to enter your vault.
- **Don't create another vault.** If Obsidian doesn't show yours, open it again with **Open folder as vault**.
- In the session, long prompts are **loaded by file**, exactly as you just practised: in Obsidian, right-click the file → **Copy path**; in Claude Code, `Read the file <path> and follow its instructions.`

### If Your Facilitator Asks for the Status Check

Your facilitator may also send you `aiac-status-check.sh` (often as `aiac-status-check.sh.txt`, because chat apps and email block `.sh` files). It's a small **read-only** script: it installs nothing, changes nothing and sends nothing. It only looks and prints a report. Save it in Downloads and tell Claude, using the **exact file name you received**:

```
Run `bash ~/Downloads/aiac-status-check.sh.txt --share` and show me its output exactly as printed.
```

(If your file is called `aiac-status-check.sh`, use that name instead; both work.) **`--share` matters:** with it the script prints only the block that starts with `----- AIAC STATUS (safe to share) -----` and ends with `----- END -----`, so nothing else about your machine enters the conversation with Claude. That block contains check names and `DONE` / `NOT DONE` / `SKIPPED (optional)` plus a verdict line, nothing personal, and it is the only thing you share. The first `NOT DONE` is where you pick up.

Want the full report, with the details behind each line? Run it **yourself in a terminal window** (Git Bash on Windows), not through Claude: `bash ~/Downloads/aiac-status-check.sh.txt`. Those details are for your eyes only; never paste them to Claude or anyone else, and never share output from `--details`. If Claude Code isn't working yet, run that same command in your terminal and copy only the block between the two `-----` lines.

---

## Come Ready With One Concrete Project

You don't fill out a form. Instead, come to your session with **one concrete project from your real work** that you'd like Claude to help with. If you're torn, bring two or three candidates and we'll pick one together.

"Concrete" means you can name three things:

- **The input:** a file, an export or a report you already have (a spreadsheet, PDFs, a system export).
- **The output you want:** a report, a summary, a cleaned table, a draft, an analysis.
- **Why it matters:** the time it costs you today, or the decision it would help.

Examples of the kind of thing that works well:

- "I build the same report by hand every month and it takes me hours."
- "I have data in one system that I can't easily cross-reference with another."
- "I need to analyze something but don't have the right tools for it."
- "My team coordinates a process, and information keeps falling through the cracks."

"Learn AI" or "be more productive" is not a project yet. Narrow it down to one task you'd actually run again.

**Bring sample data, not confidential data.** For the first exercise, use a copy with names and amounts removed, a small slice, or made-up rows that look like the real thing. Use real business data only once your company has approved using Claude with it.
