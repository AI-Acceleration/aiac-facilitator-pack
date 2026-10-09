---
title: "Pre-Session Setup Instructions (Participant) — AI Acceleration Club Phase 0"
created: 2026-07-14
category: reference
status: draft
tags: [aiac, phase0, co-facilitator-kit, participant, pre-session, setup]
---

**Supports:** Before the session — read this a few days ahead of your live Phase 0 session, and complete every step before you arrive.

# Pre-Session Setup — AI Acceleration Club Phase 0

Welcome to Phase 0 of the AI Acceleration Club. Before your live session, you'll need to install a handful of tools. Each one plays a specific role in the system we're building together — for every item below, you'll find a one-line explanation of *why* you need it, plus a ready-to-paste prompt you can hand to Claude (at claude.ai) that will walk you through the install and troubleshoot anything that goes wrong.

You'll install 6 things if you're on a Mac, or 5 if you're on Windows (Windows skips the dedicated terminal app — your built-in terminal works fine).

> **When you're running commands in a terminal:** if you get stuck at any point — a command doesn't work, you see an error, you don't know how to respond — copy **everything** from your terminal (the command you typed, the response, the full error) and paste it back into the same Claude conversation. Claude reads your terminal output and guides you to the next command until the step works. That's how you move forward without getting stuck: you're the eyes and hands, Claude is the brain.

> **One more normal thing:** when installing Granola, Obsidian, or a terminal app, your OS or browser may warn you that the download is from an "unverified developer" or flag it as a possible security risk. This is completely normal and expected with these apps — don't be alarmed. Just proceed: on a Mac, right-click → Open on the app, or allow it in System Settings → Privacy & Security. If you're unsure, paste the warning message into Claude and it'll confirm what to do.

## Is Your Work Machine Corporate-Managed?

If your work laptop is managed by your company's IT department, please confirm with IT **before the session** that:

1. **Claude Code CLI can be installed** — `npm i -g @anthropic-ai/claude-code` isn't blocked.
2. **`git push` to github.com is allowed** — some corporate firewalls block HTTPS push to github.com.
3. **No outbound DLP blocking** — no data-loss-prevention policy is blocking outbound HTTPS to `api.anthropic.com`.

If any of these are blocked, use your personal laptop for Phase 0 instead. Your vault and projects are personal anyway — it's not a great idea to build your second brain on a corporate machine that IT can wipe or revoke access to without notice.

## Windows Only — Before You Start

If you're on a Mac, skip to Step 1. If you're on Windows, work through **all** of these first —
each one has cost a real participant real time.

> **This section is prose, not commands.** Read it; don't paste it into a terminal. (Pasting prose
> into PowerShell produces a `ParserError` and can leave you stuck at a `>>` continuation prompt —
> an apostrophe in a word like *you're* opens a quote that never closes. If that happens, press
> **Ctrl+C** and carry on.)

**0. Claude Code does not run on the free Claude plan.** This is gate zero and it blocks everything
else. Anthropic's docs are explicit: *"The free Claude.ai plan does not include Claude Code access."*
Do Step 1 (Pro or Max) **before** you try to install anything. It self-resolves — if `claude` opens
and you're logged in, the upgrade worked. A participant on another cohort was stuck for weeks on
exactly this.

**0.5. Know which window you're typing in — this is the #1 Windows confusion.** Windows gives you
three, and they are not interchangeable:

| Window | Use it for |
|---|---|
| **PowerShell** | Installing Claude Code (the `irm ... \| iex` command) |
| **Git Bash** | **Everything else in this kit.** All the `bash` blocks in Docs 02/03 need it. It comes with Git for Windows (Step 3). |
| **CMD** (the black `C:\>` box) | Nothing here. If your error messages start with `C:\>`, you're in the wrong window. |

Also normal and **not** a failed install: `where bash` returns nothing. Git for Windows installs
Git Bash but doesn't put `bash.exe` on your PATH. Launch Git Bash from the Start menu instead.

**1. GitHub CLI (`gh`) — optional, not required for Phase 0.** `gh` is just a convenience for authenticating with GitHub. Try installing it from https://cli.github.com and verify with `gh --version`. **If the install fails** (corporate Windows, no admin rights, DLP), that's not blocking — use the path below, which needs no admin rights:
   - **Personal Access Token (PAT), 5 min:** github.com → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token (classic) → scopes `repo` + `workflow` → Generate. **Save the token** — it won't be shown again.
   - **Git Credential Manager** (bundled with Git for Windows): your first `git push` opens a browser window to sign in to GitHub and authorize. Manual alternative: when git asks for a username/password, use your GitHub username and paste the PAT as the password.
   If `gh` installs fine, great. If not, the PAT + Credential Manager cover everything — either way you're not blocked for the session.

**2. Administrator rights.** Make sure your Windows account has administrator rights — you'll need them to install Git, Claude Code, and other packages. If you're not sure, right-click PowerShell → "Run as administrator." If it asks for an admin password you don't have, flag it before the session.

**3. VPN — disable it for these URLs during installation:**
   - claude.ai
   - github.com
   - obsidian.md

   Many corporate VPNs block these URLs during OAuth logins and package downloads. If you have a VPN active by default, temporarily disable it for Steps 2–5 below, or ask IT to allowlist these three domains.

**4. How to paste text into the Windows terminal.** In PowerShell and Windows Terminal, Ctrl+V
often doesn't work for long blocks. Use **right-click** (or the mouse scroll-wheel click) instead.
You'll need this at every step below.

**5. Always use forward slashes `/` in file paths — never backslashes `\`.**
Write `C:/Users/you/Documents/Vault`, not `C:\Users\you\Documents\Vault`. This one matters more
than it looks: in Git Bash an unquoted `\` is silently stripped and **the command fails without any
visible error** — and the resulting breakage looks identical to an unrelated bug, so you'd spend the
session debugging the wrong thing. When a doc asks for your vault path, get it with `pwd -W` (which
prints `C:/Users/...`), not plain `pwd` (which prints `/c/Users/...`).

---

## Step 1 — Claude Pro ($20/month minimum; Max recommended)

Claude is the AI assistant you'll use for everything: it thinks, writes, analyzes, and guides you step by step. **What it's for:** it's the brain behind everything else — every step that follows relies on it, which is why it comes first.

The minimum to get started is the **Pro plan ($20/month)**. If you expect to use it heavily, **Max ($100/month)** is recommended — it gives you higher usage limits on the most capable model, so you don't run low mid-session. You can start on Pro and upgrade to Max later if you need to.

This step is manual:

1. Go to claude.ai
2. Settings → Billing → choose "Pro" (minimum) or "Max" (recommended)
3. Complete the payment

> If you're behind a corporate firewall or VPN that blocks claude.ai, temporarily disable it for this step, or ask your IT team to allowlist the domain.

## Step 2 — Obsidian

Obsidian is a note-taking app that becomes your "second brain." **What it's for:** it's where your projects, ideas, and everything you generate with AI will live and connect to each other — all in one place, always at hand.

Once your Claude plan is active, open claude.ai and paste this prompt:

```
I need to install Obsidian on my computer. Ask me what OS I'm on if you need to.
Walk me through it step by step:
1. Tell me which URL to go to for the download
2. Explain how to install it for my OS
3. Once it's installed, just verify that it opens correctly
4. Don't create any vault yet — I'll do that with my facilitator during the session

If anything fails, help me troubleshoot it.
```

## Step 3 — Git + Your GitHub Account

These are two things that go together but aren't the same — worth keeping the distinction clear:

- **Git** is a program you install on your computer. **What it's for:** it tracks every change you make to your files, so you never lose work and can roll back if something breaks.
- **GitHub** is a free cloud account (github.com). **What it's for:** it's where that work gets backed up and lives online — the place Claude Code pushes your projects to keep them safe and shareable. You'll need it either way, so create it now even if you've never used it before.

**FIRST — create your GitHub account** (manual, 2 minutes):

1. Go to https://github.com
2. Click "Sign up" and create your account (it's free)
3. Confirm your email and note your GitHub username — you'll share it with your facilitator before the session

**THEN — install Git.** Paste this prompt into claude.ai:

```
I need to install Git on my computer.
Walk me through it step by step:
1. First check whether I already have it installed (tell me what command to run in the terminal)
2. If it's not installed, walk me through installing it for my OS
3. Verify the install was successful

If anything fails or you see an error, help me resolve it.
```

*(Mac users continue to Step 4. Windows users: skip to Step 5.)*

## Step 4 — Ghostty (Mac only)

The terminal is the window where you'll work with Claude Code: you type, it executes. **What Ghostty is for:** it's a modern, fast, clean terminal app — much better than the one that ships with your Mac by default, and it's where everything below will run.

Paste this prompt into claude.ai:

```
I need to install Ghostty on my Mac. It's a modern terminal application.
Walk me through it step by step:
1. Tell me how to download it (ghostty.org)
2. Install it like any other Mac app
3. Open it and verify that it works

If anything fails, help me troubleshoot it.
```

**Windows users:** skip this step — Windows Terminal or PowerShell will work fine for everything below.

## Step 5 — Claude Code

Claude Code is the version of Claude that runs in your terminal. **What it's for:** it reads your files, writes code, generates reports, and automates tasks — all from text. It's the engine that does the heavy lifting; this is where the real work happens.

**If you're on a Mac** — open Ghostty and paste this prompt into claude.ai:

```
I need to install Claude Code (Anthropic's CLI tool for the terminal).

Walk me through it step by step:
1. On Mac, use Anthropic's native installer: curl -fsSL https://claude.ai/install.sh | bash
   (No Homebrew, no sudo, and it auto-updates itself in the background.)
2. If that fails and I already have Homebrew, the fallback is: brew install --cask claude-code
   Tell me first that Homebrew installs do NOT auto-update, so I'd have to run
   `brew upgrade --cask claude-code` myself from time to time.
3. After installing, verify with: claude --version
   If the command isn't found, help me confirm ~/.local/bin is on my PATH.
4. If it asks for authentication, walk me through the login process

If anything fails, help me diagnose and resolve it.
```

> **Why the native installer:** it's what Anthropic's own setup docs recommend. Homebrew
> installations do **not** auto-update, which means you'd silently drift onto an old version.
> The native install keeps itself current and doesn't require Homebrew at all.

**If you're on Windows** — open your terminal and paste this prompt into claude.ai:

```
I need to install Claude Code (Anthropic's CLI tool for the terminal).

Walk me through it step by step:
1. On Windows the command is: irm https://claude.ai/install.ps1 | iex
   Run it in PowerShell (not CMD, not Git Bash).
2. Walk me through the process in PowerShell
3. IMPORTANT - read the installer's own output before closing the window. It can finish
   successfully and still tell you it did NOT add C:\Users\<me>\.local\bin to my PATH.
   If it says that, walk me through adding it (setx PATH) and then open a NEW window.
4. Open a NEW terminal window and verify with: claude --version
   If I get "'claude' is not recognized", it is almost certainly the PATH step above - fix that
   before anything else.
5. If it asks for authentication, walk me through the login process

If anything fails, help me diagnose and resolve it.
```

## Step 5.5 — jq (small, but the session depends on it)

`jq` is a tiny command-line tool for reading JSON. **What it's for:** the context-monitor
status bar you'll build during the session is written on top of it. It is not optional —
without `jq` the bar silently never appears, and the failure gives you no error message.
Neither macOS nor Windows ships it, so it has to be installed now.

**If you're on a Mac** — paste this prompt into claude.ai:

```
I need to install jq (a small command-line JSON tool) on my Mac, without Homebrew.

Walk me through it step by step:
1. First tell me which chip I have — Apple Silicon or Intel:
   run `uname -m` (arm64 = Apple Silicon, x86_64 = Intel)
2. Make the folder if it doesn't exist: mkdir -p ~/.local/bin
3. Download the matching binary:
   - Apple Silicon: curl -fsSL -o ~/.local/bin/jq https://github.com/jqlang/jq/releases/latest/download/jq-macos-arm64
   - Intel:         curl -fsSL -o ~/.local/bin/jq https://github.com/jqlang/jq/releases/latest/download/jq-macos-amd64
4. Make it executable: chmod +x ~/.local/bin/jq
5. Make sure ~/.local/bin is on my PATH, and help me add it permanently if it isn't
6. Verify with: jq --version

If anything fails, help me diagnose and resolve it.
```

**If you're on Windows** — paste this prompt into claude.ai:

```
I need to install jq (a small command-line JSON tool) on Windows.

Walk me through it step by step:
1. The command is: winget install jqlang.jq
2. Open a NEW terminal window afterward so the PATH refreshes
3. Verify with: jq --version

If anything fails, help me diagnose and resolve it.
```

## Step 6 — Granola

Granola is an AI meeting recorder that connects to your calendar and generates a transcript + summary automatically. **What it's for:** so your Phase 0 session — and every meeting after it — gets captured and ready to process with Claude Code, without you taking notes by hand.

**Important:** install Granola before the session and leave it open during your time together so it records. Afterward, you'll connect the Granola integration to Claude Code and process that recording.

Any email works — personal Gmail, Google Workspace, or a Microsoft account. (An older restriction on free email providers has been lifted; if you read otherwise somewhere, it's out of date.) At the login screen use **"Continue with Google"** — the **SSO** button is an enterprise-only path and dead-ends for most people.

Paste this prompt into claude.ai:

```
I need to install Granola.ai on my computer.
It's an AI meeting recorder.
Walk me through it step by step:
1. Tell me which URL to go to (granola.ai)
2. Download and install it for my OS
3. Create an account for me — any email works (personal Gmail, Google Workspace, or Microsoft). Use "Continue with Google", not the SSO button
4. Connect my calendar (Google Workspace or similar)
5. Verify that my calendar meetings show up
6. Test recording 30 seconds of me talking and confirm it generates a transcript and summary automatically

If anything fails, help me diagnose it.
```

## Step 7 — Final Verification

Once everything above is installed, open your terminal (Ghostty on Mac, or Windows Terminal / PowerShell on Windows), type `claude`, and paste this prompt:

```
Verify that I have everything installed correctly for the AI Acceleration Club:
1. Git installed and working (git --version)
2. Obsidian installed
3. Claude Code working (you're already running here)
4. jq installed and working (jq --version)
Tell me what happened with each check, and give me a short summary I can send
to my facilitator listing each item as DONE or NOT DONE.
```

**Send that summary to your facilitator.** This is the gate — without it we have no way to know
where you got to, and sessions have started blind because it never arrived.

**Stuck, unsure, or just want to double-check?** Ask your facilitator for
`aiac-status-check.sh` — a small read-only script that reports exactly how far your setup got.
It writes nothing, installs nothing, and sends nothing; it only looks at files that already
exist and prints a summary. Run it in your **terminal** (not inside Claude Code):

```bash
bash ~/Downloads/aiac-status-check.sh
```

Copy the whole output back to your facilitator. The first `NOT DONE` is where you pick up.

If you hit a snag on any step, save the terminal output — you can pick the troubleshooting back
up with Claude, or bring it to your facilitator.

---

## Come Ready With Your Problems

You don't need to fill out a form or send anything ahead of time. Instead, come to your session with **1 to 3 real problems from your work** that you'd like Claude to help you solve — problems where better automation, analysis, or speed would make a real difference.

Examples of the kind of thing that works well:

- "I build the same report by hand every month and it takes me hours."
- "I have data in one system that I can't easily cross-reference with another."
- "I need to analyze something but don't have the right tools for it."
- "My team and I coordinate a process, and information keeps falling through the cracks."

It doesn't need to be technical — just describe the problem and why it matters to you. During the session, you and your facilitator will pick the one that's the best fit and build it together as your first real project, live.
