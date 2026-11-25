---
title: "Next Steps Brief (Participant) — AIAC Phase 0 Co-Facilitator Kit (EN)"
created: 2026-07-14
category: reference
tags: [aiac, phase0, co-facilitator, next-steps, english]
---

*Given to the participant at session end (Block 5) as their homework roadmap, together with Doc 06 — Pro Plan Survival Kit.*

# Next Steps Brief — Claude Code Mastery

> **What this is:** your roadmap from setup to productive daily use, in priority order. **Part 0 first** (close Phase 0 properly, this week), then Week 1, then the rest. Every section has ready prompts.

## How to Use This Brief

- **Short prompts** (the blocks in this document): copy them and paste them into Claude Code. On Windows, paste with right-click (or `Shift+Insert`), not Ctrl+V.
- **Long prompts or whole files:** don't paste them; terminals can cut long pastes. In Obsidian, right-click the file → **Copy path** (the full system path), then in Claude Code type `Read the file <path> and follow its instructions.` It's the same way you loaded the setup prompts.
- **Wherever Claude can run something for you, you get a prompt**, not a list of commands. Terminal commands appear only where Claude genuinely can't do the step (an interactive login, a click in an app).
- **Next to this brief** you have **Doc 06 — Pro Plan Survival Kit** (read it if you're on Pro) and **Doc 07 — Vocabulary** (every term on one page).

> **Plan note.** Claude **Pro** is the default and is enough to start. All plans have usage limits that reset every few hours and every week. Doc 06 explains how to spread heavy sessions out and make Pro last. Upgrade to Max only if you keep hitting the limits ([claude.com/pricing](https://claude.com/pricing)).

---

## PART 0: CLOSE PHASE 0 FIRST (THIS WEEK)

### 0.1 Check what the setup left

Open a session in your vault (`cd "<your vault path>"`, then `claude`) and paste:

```
Check what my Phase 0 setup left in place. Don't change anything: only look, and give me READY or MISSING for each point.
1. ~/.claude/CLAUDE.md (the global router) and the CLAUDE.md at the root of my vault.
2. ~/.claude/settings.json is valid JSON and has CLAUDE_AUTOCOMPACT_PCT_OVERRIDE at 75:
   jq -e '.env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE' ~/.claude/settings.json
3. The cheat sheet: 00 HUB/00 INBOX/AIAC Cheat Sheet.md
4. The template: Templates/Project Brief Template.md
5. My area map: a <Area>.md file inside 02 AREAS/<Area>/
6. My journey brief: 01 PROJECTS/AI Acceleration/<My Name>/AI Acceleration Club - <My Name> Journey.md
7. My case project brief: 01 PROJECTS/<Project Name>/<Project Name>.md
8. My repo, outside the vault and on GitHub, private:
   ls ~/dev/<repo-name> and gh repo view <owner>/<repo-name> --json nameWithOwner,visibility
   (visibility must be PRIVATE)
9. The folder 05 AI/CLAUDE CODE/resources/ (lessons.md appears there with my first lesson;
   if it doesn't exist yet, that's not MISSING).
10. My skills and plugins: list the folders in ~/.claude/skills/ and run claude plugin list.
If something is missing, tell me which step of the Main Setup Prompt or the Skills & Config
Setup Prompt creates it. Don't redo it on your own.
```

If something from the setup is missing, load that setup file by path and ask for only that step: `Read the file <path to the setup prompt> and run only STEP N.` If the repo is **not** private, fix that first (on GitHub: Settings → General → Danger Zone → Change visibility → Private).

### 0.2 Your case project brief, with `/project-create` (only if it's missing)

The Main Setup Prompt normally creates your case brief. **If 0.1 says it exists, skip this**; don't create a second one. If it's missing, create it with the `/project-create` skill, which interviews you. It's the same path you'll follow every time you start something new.

1. **Open a NEW Claude Code window** in your vault. Skills load in new sessions only.
2. **Type exactly:**

   ```
   /project-create
   ```

   If it doesn't show up in the list when you type `/`, it isn't installed: ask for help at [SET: your support channel]. Typing just the project name does **not** call the skill.
3. Use your case name as the project name. Answer from what you discussed in the session.
4. **If Claude starts writing code or asks you to install something, you're not in the skill.** Press `Esc` and go back to step 2.
5. When it finishes, check where the brief landed. It belongs in its own folder: `01 PROJECTS/<Project Name>/<Project Name>.md`. If it's somewhere else, tell Claude: `Move it into 01 PROJECTS/ in its own folder, with the same name.`
6. Open the brief in Obsidian and read it all. If your repo isn't listed under `## Key Resources`, ask Claude to add `~/dev/<repo-name>`.

### 0.3 Close the setup session by hand

`/session-close` was installed **during** your setup session. Skills only load in sessions started after they're installed, so in that same session it doesn't work yet. Close it with the **APPENDIX: MANUAL CLOSE PROMPT** at the end of this brief. From your next session on, `/session-close` works normally.

When you've finished Part 0, close with `/session-close`.

---

## PART 0.5: CONCEPTS & INSTALLED STACK — READ THIS ONCE

> **Why this section exists:** during your Phase 0 session we moved fast through a lot of plumbing. This is the "theory + inventory" page: the reference you come back to when you want to understand *why* something is wired the way it is, or *what exactly got installed*. Read it once end-to-end before Week 1. Then skim it weekly for the first month.

### The 4 Core Concepts

#### 1. CLAUDE.md — The System's Brain

There isn't ONE `CLAUDE.md`. There's a **chain** of them that Claude reads automatically at session start:

| Location | Purpose | When Claude reads it |
|----------|---------|---------------------|
| `~/.claude/CLAUDE.md` | **Global router + your profile.** Tells Claude where your vault is, who you are, your defaults. | Every session, regardless of starting directory |
| `[vault]/CLAUDE.md` | **Vault rules.** How to handle notes, PARA structure, safety, language. | Every session started inside the vault |
| `[repo]/CLAUDE.md` | **Project rules.** Domain principles, data sources, what may be touched, and the bridge back to your brief. | Every session started inside that repo |

**Key mental model:** `CLAUDE.md` is how the system **improves over time**. Every time you correct Claude, add the rule to the right `CLAUDE.md`. Next session, the correction sticks. After a month, Claude genuinely works better for YOU because the rules accumulate.

**Location-by-specificity rule:** add a correction to the MOST SPECIFIC `CLAUDE.md` that applies. Project-specific → the repo's `CLAUDE.md`. How you take notes in general → the vault's `CLAUDE.md`. Defaults across ALL projects (e.g., "always answer in English") → `~/.claude/CLAUDE.md`.

#### 2. Context Window — Your Working Memory

Claude's context window is limited. As you work in a session, it fills with conversation history, files Claude reads, tool outputs, etc. Past a certain point, **quality degrades**: this is called **context rot**.

**The thresholds that matter:**
- **Compact IDEALLY before 50%:** best quality, clean state carry-over. This is the target.
- **After 50% context rot starts:** not catastrophic, but Claude starts forgetting earlier context and confusing details.
- **Compact CERTAINLY before 70%:** past 70%, quality falls off a cliff. A forced reactive compact is much messier than a proactive one.

**The compact options at the threshold:**
- Run `/session-close`, then `/clear` to start fresh (cleanest: state is saved in your project brief's Continuation Prompt, then reset).
- Or run `/compact` to summarize in place and keep going mid-task (faster, but lossy: prefer the option above at a natural break point).

**How to see your usage:** your context % shows as a live bar at the bottom of the terminal, the context monitor set up by your Main Setup Prompt. The bar turns **yellow ⚠ at 50%** (with a one-time warning), and auto-compaction is **stopped just before 75%** so you get a chance to run `/session-close` before context is compressed. If the bar isn't visible, open a new session; if it's still missing, type `/context` to see the current state and ask Claude to re-run STEP 3.5 of your Main Setup Prompt (don't use `/statusline-setup`: it replaces the custom bar and removes the 50% warning).

#### 3. Skills — Reusable Procedures

A "skill" is a structured prompt + workflow stored at `~/.claude/skills/{name}/SKILL.md` (or inside a plugin) that Claude runs when you type `/{name}`. You already have `/session-close` and the other starter skills from your Skills & Config step.

**How to invoke a skill:** type `/` in Claude Code and pick from the autocomplete (part of the name is enough, e.g. `/session`).

**When to create a new skill:** if you find yourself giving Claude the same instructions 3+ times, it's skill-worthy. Run `/skill-create` and Claude walks you through defining it.

**Why skills matter:** they turn ad-hoc patterns into durable infrastructure. A skill you write in Week 2 still works in Month 6 without you remembering the details.

#### 4. MCP and Connectors — External Systems

MCP ("Model Context Protocol") is how Claude Code talks to systems beyond your files: email, calendars, documents, transcription tools, databases.

**What you set up in your Skills & Config step** depends on your stack:
- **Google:** the claude.ai connectors for Gmail, Google Drive and Google Calendar.
- **Microsoft 365:** the claude.ai Microsoft 365 connector (Outlook mail and calendar, OneDrive, SharePoint), if your account allows it.
- **Meetings:** `/meeting-minutes` reads from your transcription tool's connector, or from a transcript you paste.
- **Team or Enterprise account:** your organization's admin decides which connectors you can see.

> **If a claude.ai connector didn't finish authorizing during the session:** go to claude.ai → Settings → Connectors, open it and complete the authorization. Then, in a **new** Claude Code session, test it with a quick prompt (e.g. *"List my 3 most recent emails."*). If it still won't authorize, send your facilitator the exact error.

**Adding more later:** ask Claude to help you add an MCP server when a workflow needs one, and check with your facilitator first if it touches work data. Database access: read-only by default. New connectors and MCP servers show up in **new** sessions.

**MCP vs. CLI:** MCPs are structured connectors (Claude gets typed tools with defined inputs and outputs). CLIs are raw commands Claude types in the shell. MCPs are cleaner for frequent operations; CLIs are fine for one-off or OS-level tasks.

### Two Places, Two Kinds of Session

You'll often have **two Claude Code sessions open at once**: one in your vault (notes, planning, briefs) and one in your project's repo at `~/dev/[your-repo-name]` (code, data, scripts). That's normal; it's how the router + `CLAUDE.md` chain is designed to work.

1. **Skills and plugins load in new sessions only.** Something installed during a session shows as installed but isn't active until you open a new Claude Code window.
2. **Each project has its own `CLAUDE.md` and its own state.** Running your case analysis inside a vault-planning session mixes two logs together. Keep vault work and repo work in separate windows.
3. **The router resolves you into the right project.** From any folder, in a new window, say *"let's work on my [case name]"*: Claude opens your project with its Continuation Prompt, no `cd` needed.

The rule for where things live: **knowledge** (notes, briefs, project management) in the vault; **code repositories** in `~/dev/`. If a folder has its own `.git/`, it belongs in `~/dev/`.

### Working in the Claude Desktop App

You set everything up in the terminal, and that's where installs and settings changes happen. Claude Desktop's **Code** tab reads the same `~/.claude` folder (your skills, settings and `CLAUDE.md` files), so you can do day-to-day work there if you prefer a window to a terminal. Commands such as `claude plugin …` and `claude mcp add …` still need the terminal.

### Portability — Your System Isn't Locked In

Everything you built is plain Markdown files, Git and standard tools. Claude Code is the recommended harness today, but your vault, briefs and `CLAUDE.md` rules are just text: another AI tool could read them tomorrow. Nothing in your second brain depends on a single vendor.

### Best Practices — The Core Loop

These are the 7 habits that separate productive Claude Code users from the rest. Internalize all 7 by Week 4.

1. **Always `/session-close` before ending.** No exceptions. This is the habit that makes the system compound.
2. **Plan before building.** Any task that touches 2+ files: press `Shift+Tab` until the bottom bar says *plan*. Big or new projects: a planning skill (see Part 5).
3. **Correct Claude out loud, then persist the correction.** "That's not right because X. Now update the CLAUDE.md so it doesn't happen again." This IS the self-improvement loop.
4. **Watch the context bar.** At ~50%, compact or close. Never let it hit the limit mid-task.
5. **Capture lessons.** Any surprise, gotcha or workaround → one line in `05 AI/CLAUDE CODE/resources/lessons.md`.
6. **Open Claude Code daily, even 10 min.** In Week 1 the habit matters more than the output.
7. **Trust the CLAUDE.md chain.** If Claude is confused, it's usually because a `CLAUDE.md` is missing or wrong, not because Claude is broken.

### What Got Installed On Your Machine

Full inventory, in case you need to audit, replicate or troubleshoot later.

**Global files:**

| Path | What it is | Edit when... |
|------|-----------|--------------|
| `~/.claude/CLAUDE.md` | Global router + your profile | Your vault moves, your role changes, you want to add global defaults |
| `~/.claude/settings.json` | Permissions (a short list of pre-approved, read-mostly commands), hooks (session-end sound, context warnings), auto-compact at 75%, status bar | You want Claude to ask less often for a specific safe command, or to change a hook |
| `~/.claude/statusline.sh` and `~/.claude/hooks/` | The context bar and the 50% / pre-compact warnings | Rarely |
| `~/.claude/skills/` | Your starter skills (`/session-close`, `/project-create`, …) | You add or update skills |

> **Permissions are deliberately narrow.** Setup never pre-approves blanket commands (all of `git`, `cat`, Python, …). Claude asks before pushing, deleting or running scripts, and that's your safety net. When you add a permission, add one specific command, never a wildcard.

**Vault files created:**

| Path | What it is |
|------|-----------|
| `[vault]/CLAUDE.md` | Vault-level rules (PARA, language, safety) |
| `[vault]/Templates/Project Brief Template.md` | Reusable template for new projects |
| `[vault]/01 PROJECTS/[project name]/[project name].md` | Your case project brief |
| `[vault]/01 PROJECTS/AI Acceleration/[your name]/AI Acceleration Club - [your name] Journey.md` | Tracks your progress through the program |
| `[vault]/02 AREAS/[area]/[area].md` | Your area map (MOC) |
| `[vault]/05 AI/CLAUDE CODE/resources/` | Lessons folder; `lessons.md` appears with your first lesson |
| `[vault]/00 HUB/00 INBOX/AIAC Cheat Sheet.md` | Quick reference card |

**Repo files** (in `~/dev/[your-repo-name]/`, outside the vault, pushed to a **private** GitHub repo):

| Path | What it is |
|------|-----------|
| `CLAUDE.md` | Project-level rules + the bridge back to your vault brief |
| `README.md` | Human-facing intro to the project |
| `.gitignore` | Keeps raw data and secrets out of GitHub |
| `data/raw/` · `data/working/` · `data/processed/` | Data zones: raw and working are **never** uploaded; processed results are |

**Plugins:** run `claude plugin list` in the terminal to see exactly what's installed and enabled (Part 6 explains the main ones).

**Hooks:**

| Event | Hook | What happens |
|-------|------|--------------|
| `Stop` | Sound | Audible notification when Claude finishes a task |
| `UserPromptSubmit` | Context warning | A one-time reminder once you pass 50% |
| `PreCompact` | Stop before auto-compact | Gives you the chance to `/session-close` first |

### How to Troubleshoot When Something Feels Off

- **Claude doesn't know about my project** → the router in `~/.claude/CLAUDE.md` may be broken. In a new window, from `cd ~`, ask what's in your vault INBOX. If it can't find it, ask for help.
- **Claude repeats the same mistake** → the correction didn't get saved. Open the relevant `CLAUDE.md` and check the rule is there.
- **Session feels slow or Claude forgets things** → context is full. `/session-close`, then `/clear`.
- **A skill or plugin command isn't found** → open a **new** window first (they load in new sessions). Then run `claude plugin list` in the terminal, and check `~/.claude/skills/`. On a Team/Enterprise account, a plugin you installed by hand with the same name as one your organization provides can hide the organization's copy: keep the organization's.
- **Something errors in the terminal** → copy the error (check it doesn't contain a password or token), paste it to Claude and ask *"what is this error?"*.

---

## PART 0.6: KEEPING PLUGINS UP TO DATE

Plugins come from **marketplaces** (catalogs). To update, in Claude Code:

1. `/plugin marketplace update` (refreshes the catalogs)
2. `/plugin update <plugin>@<marketplace>` for the plugin you want to update
3. **Start a new session** so the new version loads.

Check the result with `claude plugin list` in the terminal. On a **Team or Enterprise** account, plugins your organization provides are updated by your organization; you may only need step 3.

---

## PART 0.7: OPTIONAL — MORE PLUGINS

Your Skills & Config step installed the core plugins. These are worth adding when you want them. **Paste into Claude Code:**

```
Install these plugins from the official marketplace (claude-plugins-official), one by one, asking me
before each install. If a plugin is already installed, skip it. When you're done, run
claude plugin list and show me the result. If one fails, tell me which one and the error.

- explanatory-output-style  (Claude explains its reasoning while it works)
- commit-commands           (git commits with good messages, via /commit)
- claude-md-management      (keep your CLAUDE.md files healthy)
- context7                  (up-to-date docs for any library)
- code-review               (code quality review)
- playground                (interactive HTML visualizations)
```

Then **start a new session** so they load.

<details><summary><b>Fallback — run them yourself in a terminal</b></summary>

A plugin is always `<plugin>@<marketplace>`:

```bash
claude plugin marketplace add anthropics/claude-plugins-official   # only if not already configured
claude plugin install explanatory-output-style@claude-plugins-official
claude plugin install commit-commands@claude-plugins-official
claude plugin install claude-md-management@claude-plugins-official
claude plugin install context7@claude-plugins-official
claude plugin install code-review@claude-plugins-official
claude plugin install playground@claude-plugins-official
claude plugin list
```

`claude /install-plugin` and `claude plugins add` do **not** exist. If an old guide shows them, ignore it.
</details>

---

## PART 0.8: OPTIONAL — LEVEL UP YOUR OBSIDIAN

> **Optional, not required.** Phase 0 already set the four load-bearing Obsidian settings
> (new notes → `00 HUB/00 INBOX`, wikilinks, show all file types, auto-update links). Everything
> below is *amplification*. Add it when you want the capability, not because you have to.

### Community plugins worth installing

Install path is the same for all of them: **Settings → Community plugins → Turn on
community plugins → Browse → search the name → Install → Enable (toggle ON)**. Install one,
try it, then come back for the next.

| Plugin | What it's useful for | How to set it up |
|--------|----------------------|------------------|
| **Dataview** | Live queries over your notes' frontmatter: "show me all active projects" in a table. The highest-leverage plugin for a PARA vault. | Install + enable. Test in a note: a fenced ```` ```dataview LIST FROM "" LIMIT 5 ``` ```` block should render a list of files. Turn on JavaScript queries only if you understand what they run. |
| **Tasks** | Real task management on top of `- [ ]` checkboxes: due dates, priorities, recurrence, and queries like "everything due this week". | Install + enable. In its settings turn ON "Set done date on every completed task". |
| **Templater** | Templates that fill themselves in (`{{title}}`, `{{date}}`). | Install + enable. Point its "Template folder location" at `Templates/`. |
| **Calendar** + **Periodic Notes** | Daily / weekly notes with templates, from a sidebar calendar. | Install + enable both; in Periodic Notes turn on "Daily Notes" and set its template + folder. |

### Deeper settings (optional)

- **Attachments in one folder.** Settings → Files and links → **Default location for new
  attachments** → "In the folder specified below" → e.g. `assets`.
- **Shortest link format.** Settings → Files and links → **New link format** → "Shortest
  path when possible".

---

## PART 0.9: OPTIONAL — gws CLI FOR DEEPER GOOGLE WORKSPACE INTEGRATION

> **Optional, Google-stack only, and not for Week 1.** The claude.ai connectors cover most of what you need. Add the **gws CLI** later only if your project needs Claude to **write to Google Sheets** or drive Google Workspace from scripts. Skip it entirely on Microsoft 365. If it's a **work** Google account, ask your IT or facilitator first.

Ground rules: sign in with **only the scopes you need** (for example Sheets, not everything), and **don't add a permission rule that pre-approves all `gws` commands**: let Claude ask each time. Budget about an hour and a half end to end.

```
I want to install the gws CLI so Claude Code can write to Google Sheets. Walk me through it step by step.
Ask me which Google services I actually need and request only those scopes when I log in.
Do not add any permission rule that pre-approves gws commands. Test one read command, then add a
short "Google Workspace Tools" note to my vault's CLAUDE.md. If anything fails, we'll fix it together.
```

---

## PART 0.10: GENERATE YOUR CONSOLIDATED USER GUIDE

> **Do this once, after Part 0.** It generates a single **`User Guide — [your name].md`** at your vault root: the one map of *what you have and how it fits*. It complements (doesn't replace) your **AIAC Cheat Sheet**.

**Paste this into Claude Code, in your vault:**

```
Generate my consolidated User Guide at `User Guide — [your name].md` at the root of my
vault. Read what's ACTUALLY installed and configured on my system — don't guess. Three
short, navigable sections:

- Section A — My Vault: the PARA structure, the CLAUDE.md chain (global → vault → repo),
  and where everything lives (vault = knowledge, ~/dev/ = code repositories).
- Section B — Claude Code: the plugins and skills I have installed (claude plugin list and
  ~/.claude/skills/), the context monitor (the 50/75% bar), and Plan Mode. For the command
  quick-ref, point to my AIAC Cheat Sheet instead of duplicating it.
- Section C — My case workflows ([your project name]): the 2-3 concrete workflows for
  my project and their starter prompts.

It's a map, not a manual — keep it short.
```

Re-run it any time your system grows.

---

## PART 1: AFTER THE SESSION — TONIGHT, THIS WEEK, CHEAT SHEET, HELP

> **Goal:** get real data into the repo, build your first analysis, start the self-improvement loop.

### 1. Tonight (3 mini-actions)

- [ ] **Test the router.** Open a new terminal, `cd ~`, run `claude` and ask *"What files are in my vault INBOX?"*. If it answers without you giving the path, the router works. If not → ask for help at [SET: your support channel].
- [ ] **Close the setup session by hand** with the APPENDIX: MANUAL CLOSE PROMPT (Part 0.3). The closing habit starts tonight.
- [ ] **Write tomorrow's intention** in your case brief's `## Next Actions`, one line: "Tomorrow I want to ___."

### 2. This Week (5 things to try, in order)

A ramp into real use. Don't skip ahead: each step builds on the previous one. (Your project-specific version of each step lives in PART 3, which you fill in at the end of today's session.)

1. Drop the first real (or sample) data file into `data/raw/` in your repo and ask Claude to inventory it: what's in it, what's missing, what questions it could answer.
2. Run your first real analysis using a prompt from PART 3.
3. Turn that analysis into a saved output (a report, a script, or a note in your project brief) so it doesn't just sit in chat history.
4. Automate the most annoying manual step in your workflow: ask Claude to script or template it.
5. Correct Claude at least once out loud, then say "update the CLAUDE.md so this doesn't happen again." Your first rep of the self-improvement loop (PART 7).

> **Using real business data?** Only once your company has approved using Claude with it. Raw data stays in `data/raw/`, which is never uploaded to GitHub.

> **For your NEXT project** (a brand-new one, not today's case): open a **new** Claude Code window in your vault and run `/project-create`. **Don't ask for another Setup Prompt**: from here on, the flow is yours.

### 3. Cheat Sheet — Always In The Same Place

Your cheat sheet lives at exactly this path:

```
00 HUB/00 INBOX/AIAC Cheat Sheet.md
```

Pin it in Obsidian. The Main Setup Prompt created it; if it's missing, load that setup file by path and ask for only the cheat-sheet step. It has the session-start commands, the router prompt, the essential commands, the context thresholds and your file anchors.

**Add two things to it now.** Paste into Claude Code, in your vault:

```
Add two short sections to 00 HUB/00 INBOX/AIAC Cheat Sheet.md, at the end, without changing the rest:
1. "Several sessions at once — claude agents": the key points from section 4 of PART 1 of my Next Steps Brief.
2. "Asking for something big — the task contract": the four-line template from section 5 of PART 1.
Show me the diff before saving.
```

### 4. Several Sessions at Once — `claude agents`

You'll often have two or more sessions open (one in the vault, one in the repo). `claude agents` shows them all and lets you jump between them:

- Type `claude agents` in the terminal: the list of your sessions appears.
- `↑` `↓` to choose one; `→` to enter it.
- `←` goes back to the list, **only when the text field is empty**. If you've typed something, delete it first.
- Not sure which session you're in? Go back with `←` and look at the list. To come back another day: `claude agents`.

Prefer something simpler? One terminal tab (on Windows, one Git Bash window) per session, with `claude` in each. Both work; what matters is not mixing vault work and repo work in the same session.

### 5. Asking for Something Big — The Task Contract

For anything bigger than a quick question, give Claude a goal it can verify. Copy and fill in:

```
Goal: {what you want, in one sentence}
Done when: {how we'll both know it worked — a file I can open, a command that passes, a number that matches}
Only touch: {the files it may change}
Ask me first if: {it would send something, delete something, spend money or touch real data}
```

Vague words are fine *if* you add: "turn 'professional' into 3 checkable criteria and confirm them with me before you start."

### 6. Stuck? — Where To Get Help

Help is **tiered**. Start at the top and only escalate when you need to:

1. **Claude first (most issues).** Paste the error, try `/systematic-debugging`, check the `CLAUDE.md` chain. Most things resolve right here.
2. **Your support channel: [SET: your support channel].** For day-to-day doubts, setup problems or a quick "is this normal?". Don't sit stuck in silence; a shared question resolves faster.
3. **Your facilitator, for infrastructure blockers.** A failed install, a login problem, a connector that won't connect, a router test failure: reach out right away. Don't burn a day on plumbing.

**When you ask for help (any tier):** include the prompt you ran, the exact error output (without passwords or tokens) and what you already tried. "It's broken" is not a debug message.

### 7. End of Week 1 — Close Properly

```
/session-close
```

---

## PART 2: WEEK 2 — BUILD YOUR DAILY HABITS

### Morning: Start Your Day

In a new window, from any folder:

```
Let's work on my [project name]. What are my open next actions, and what's the most important thing to work on today?
If there's a Continuation Prompt, summarize where I left off.
```

### During Work: Use Plan Mode

For any non-trivial task:
- Press `Shift+Tab` until the bottom bar says *plan*
- Describe what you want
- Review the plan
- Approve and execute

### Before Ending: Always Close

```
/session-close
```

This updates your project brief, logs what you did and creates a continuation prompt. **This is the single most important habit.**

### Weekly: Review Progress

```
Read my [project name] project brief.

Give me a weekly progress report:
1. What milestones have been completed?
2. What's in progress?
3. What's blocked and by whom?
4. What should I focus on next week?
5. Are we on track for the milestone targets?
```

---

## PART 3: YOUR PROJECT'S NEXT WORKFLOWS

Your case wasn't picked in advance: you and your facilitator chose it live. So this section starts blank on purpose. Fill it in before you leave (Block 5), while the session is fresh. It becomes your personal version of PART 1's "This Week" ramp and PART 8's progression map.

**How to fill this in.** Ask Claude:

```
Based on everything we built and discussed today for [your project name], help me draft
3-5 workflows I'll actually run again — recurring reports, analyses, or documents specific
to my work. For each one, give me:
1. A short name
2. When I'd use it
3. A ready prompt with real file paths from my repo

Save this list into my project brief's Next Actions, and also write it out below so I
have it in this brief too.
```

### Workflow 1: _______________________________
```
[ready prompt — fill in during/after today's session]
```

### Workflow 2: _______________________________
```

```

### Workflow 3: _______________________________
```

```

### Workflow 4: _______________________________
```

```

### Workflow 5: _______________________________
```

```

> **Want a day-by-day Week 1 plan instead of a workflow list?** Ask Claude: *"Help me turn the workflows above into a day-by-day Week 1 schedule."*

---

## PART 4: GENERAL PRODUCTIVITY PROMPTS

### Research Any Topic

```
/deep-research [topic]
```

### Create a New Project

In a **new** Claude Code window in your vault:

```
/project-create
```

### Make a Decision

```
I need to make a decision about: [DESCRIBE THE DECISION]

Help me think it through:
1. What are the options? (at least 3)
2. What are the pros and cons of each?
3. What's the risk if I pick wrong?
4. What information am I missing?
5. What's your recommendation and why?

Save this as a decision memo in 00 HUB/00 INBOX/.
```

### Analyze a Spreadsheet

In a repo session (`cd ~/dev/[your-repo-name]` and `claude`), with the file copied into `data/raw/`:

```
Read the file [FILENAME] in data/raw/. Don't modify it: work on a copy. Tell me:
1. What's in this data? (columns, row count, date range)
2. Summary statistics for the numerical columns
3. Any patterns, trends, or anomalies
4. 3 questions this data could answer
5. What other data would I need to combine with this for a complete picture?
```

### Save Your Work to GitHub

In a repo session, when you finish:

```
Commit my changes with a clear message and push them to GitHub. First show me which files
are included, confirm the repository is still private, and confirm nothing from data/raw/ or
data/working/ is being uploaded.
```

### Create a Custom Skill

```
/skill-create

I keep doing [DESCRIBE THE REPEATED TASK].
Help me create a skill that automates this.
```

---

## PART 5: THE SKILLS YOU HAVE — AND WHAT TO BUILD NEXT

> To see everything you have: type `/` in Claude Code and scroll the list. Names can vary slightly between plugin versions.

### Starter skills (installed in your Skills & Config step)

They come from the public **[AI-Acceleration/cc-starter-pack](https://github.com/AI-Acceleration/cc-starter-pack)** repository, pinned at release **`v1.0.0`** so everyone gets the same reviewed version.

| Skill | What it does | How to use |
|-------|-------------|-----------|
| **session-close** | Closes a session properly: updates the brief, logs work, writes the continuation prompt | `/session-close` |
| **project-create** | Creates a project brief through guided questions | `/project-create` |
| **inbox-clear** | Clears your INBOX with the GTD decision tree; acts only on your approval | `/inbox-clear` |
| **retro** | A retrospective: what worked, what didn't, what to change | `/retro` |
| **skill-create** | Create your own skills through a guided conversation | `/skill-create` |
| **deep-research** | Multi-phase research: broad sweep → deep dive → synthesis, with sources | `/deep-research [topic]` |
| **deep-planning** | Planning pipeline (brainstorm → plan) before you build | `/deep-planning` |
| **extract** | Structured extraction from a note or a URL | `/extract [note or URL]` |
| **fermi-decomposition** | Break "unmeasurable" numbers into estimable factors | `/fermi-decomposition` |
| **context** | How much context you've used | `/context` |
| **permissions** | Shows your current permission settings | `/permissions` |

Plus **`/meeting-minutes`**, set up for your transcription tool (or for pasted transcripts).

**Reinstalling or updating the starter skills.** Ask Claude to do it, pinned to a release tag:

```
Reinstall my starter skills from the AI-Acceleration/cc-starter-pack repository at tag v1.0.0:
git clone --depth 1 --branch v1.0.0 https://github.com/AI-Acceleration/cc-starter-pack.git into a
temporary folder, show me what install.sh will do, run it after I approve, then delete the temporary folder.
```

Then start a **new** session. Use a newer tag only when your facilitator announces one.

### Plugin skills (from your plugins)

| Skill | What it does |
|-------|-------------|
| **Compound Engineering** planning skills (e.g. `/ce-plan`, `/ce-work`, `/ce-brainstorm`; older versions use `/ce:plan`) | Plan with research first, then execute step by step |
| **Superpowers** (e.g. `/systematic-debugging`, `/verification-before-completion`, `/brainstorming`) | Structured debugging, brainstorming and verification |

### Ideas to build next (not installed — build them with `/skill-create`)

These are patterns that work well once your basics are solid. None of them is installed by the kit; when one would save you time, build your own version with `/skill-create`:

| Idea | What it would do |
|------|------------------|
| **weekly-review** | GTD weekly review: scan your projects, clear the INBOX, plan next week |
| **startup-day** / **close-day** | A morning plan from your tasks and calendar; an end-of-day wrap-up |
| **meeting-agenda** | Build an agenda from the calendar, your notes and past minutes |
| **decision-memo** | A structured decision document: context, alternatives, recommendation |
| **followup** | Scan your briefs for "Waiting For" items and draft follow-ups (you approve every send) |

---

## PART 6: PLUGIN REFERENCE

**What you have:** run `claude plugin list` in the terminal. Your Skills & Config step installed at least **Compound Engineering** and **Superpowers**; Part 0.7 adds more.

| Plugin | What it does |
|--------|-------------|
| **Compound Engineering** | Plan-first development workflow with research agents |
| **Superpowers** | Structured workflows for debugging, brainstorming, TDD and verification |
| **Explanatory Output Style** | Claude explains its reasoning as it works |
| **Commit Commands** | Git commits with good messages |
| **Claude MD Management** | Audit and improve `CLAUDE.md` files |
| **Context7** | Up-to-date docs for libraries when you reference them |
| **Code Review** | Review code for bugs, security and quality |
| **Playground** | Interactive HTML visualizations |

### Optional Plugins (Install Later)

| Plugin | What it does | When to install |
|--------|-------------|----------------|
| **Feature Dev** | Guided feature development with codebase analysis | When building larger features |
| **PR Review Toolkit** | Thorough pull-request review | When doing code reviews |
| **Frontend Design** | High-quality interface generation | When building UIs or dashboards |
| **Playwright** | Browser automation for testing | When testing web apps |
| **Hookify** | Create hooks that prevent unwanted behaviors | When you want to automate rules |

---

## PART 7: THE SELF-IMPROVEMENT LOOP

This is the most important concept. It's what separates productive Claude Code users from everyone else.

### The Loop

```
1. Work with Claude Code
2. Claude makes a mistake -> correct it
3. Tell Claude: "Update the CLAUDE.md so this doesn't happen again"
4. Next session reads the updated CLAUDE.md
5. Mistake doesn't happen again
6. Repeat for weeks -> CLAUDE.md accumulates intelligence
7. After a month, Claude genuinely works better for YOU
```

### Prompt to Start the Loop

Whenever Claude does something wrong:

```
That's not right. [Explain what was wrong and what the correct approach is.]
Now update the CLAUDE.md to add a rule that prevents this mistake in the future.
```

### Your Corrections

Corrections come from real mistakes Claude makes on **your** project. Here's the pattern, plus space to log your own as they happen this week:

**Pattern:**
> "[What Claude did wrong] isn't right — [why, and what the correct approach is]. Add this rule to the CLAUDE.md so it doesn't happen again."

**Log yours here as they happen:**

1. Correction — ___________________________:
   > "..."

2. Correction — ___________________________:
   > "..."

3. Correction — ___________________________:
   > "..."

---

## PART 8: PROGRESSION MAP

### Week 1: Setup + First Real Use
- [ ] Part 0 done (setup checked, setup session closed by hand)
- [ ] Real or sample project data in `data/raw/` in your repo
- [ ] First analysis pass run and saved (not just left in chat)
- [ ] At least 3 Claude Code sessions completed
- [ ] `/session-close` run at the end of every session
- [ ] First workflow from PART 3 tested end-to-end

### Week 2: Daily Habits
- [ ] Daily morning check-in with your project brief
- [ ] Plan Mode used at least twice
- [ ] First automated or repeatable output (a report, script or template)
- [ ] At least 2 corrections added to your `CLAUDE.md` (PART 7)
- [ ] A `weekly-review` skill **built** with `/skill-create` (it is not installed by the kit; see Part 5) and run once

### Week 3: Operational Workflows
- [ ] 2-3 of your PART 3 workflows tested and refined
- [ ] A custom skill created for a workflow you've repeated 3+ times (`/skill-create`)
- [ ] Changes pushed to your private GitHub repo at least twice
- [ ] Optional plugins from Part 0.7 installed if you want them

### Week 4: Autonomy
- [ ] Your top workflow runs on a single ready prompt, no rework
- [ ] `CLAUDE.md` has 5+ accumulated rules from the self-improvement loop
- [ ] Using Claude Code for 30+ real minutes a day
- [ ] Ready to take on a second project (`/project-create`)

### Month 2: Expansion
- [ ] A second project started with `/project-create`
- [ ] At least one workflow fully automated end-to-end

### Month 3: Mastery
- [ ] Claude Code is a default part of your daily work, not a novelty
- [ ] You've created 2+ custom skills of your own
- [ ] You correct Claude and update `CLAUDE.md` without being prompted to

---

## APPENDIX: QUICK REFERENCE CARD

### Start Working

> **Two places, one rule.** **Knowledge** (notes, briefs, project management) lives in your vault. **Code** lives in `~/dev/[your-repo-name]`, **outside** the vault. The test is mechanical: if it has its own `.git/`, it goes in `~/dev/`.

```bash
cd "[vault path]" && claude          # notes, projects, thinking
cd ~/dev/[your-repo-name] && claude   # code and data
```

On Windows (Git Bash), run each as two lines (`cd …`, then `claude`). In File Explorer the repo folder is `C:\Users\YOUR-USER\dev\[your-repo-name]`.

Or, from any folder in a new window: *"Let's work on my [project name]."*

### Essential Session Flow
```
1. Start: Claude reads the CLAUDE.md files automatically
2. Resume: "Let's work on my [project name]. Where did I leave off?"
3. Plan: Shift+Tab until the bar says plan -> describe the task -> review the plan -> approve
4. Work: execute the plan
5. Close: /session-close
```

### Several Sessions
```
claude agents        (↑ ↓ choose · → enter · ← back to the list, with the text field empty)
```

### Asking for Something Big
```
Goal: … · Done when: … · Only touch: … · Ask me first if: …
```

### When Stuck
```
/systematic-debugging

I'm stuck on: [describe the problem]
What I've tried: [what you already tried]
What I expected: [what should have happened]
```

### When You Need Research
```
/deep-research [topic]
```

### When Ending
```
/session-close
```

---

## APPENDIX: MANUAL CLOSE PROMPT

> **When to use:** in the session where you ran the setup. `/session-close` was installed in that SAME session, and skills only load in sessions opened AFTER they're installed, so that session is closed by hand. From your next session on, `/session-close` works normally. Paste this **in that same session**:

```
Please close this session by hand. Don't invoke /session-close: it's installed but not loaded
in this session yet. Make the changes directly:
1. At the top of my case project brief's ## Next Actions section, add or replace the
   ### Continuation Prompt block with:
   - Today's date
   - Mode: Vault Management
   - Context summary: what we did in this Phase 0 session (vault scaffolding, project
     brief created, private GitHub repo pushed, skills installed, router test passed)
   - Resume-from: Part 0 of my Next Steps Brief, then the Week 1 homework
   - Files touched in this session
2. Append a Log entry: "Phase 0 session completed — vault scaffolded, case brief created,
   private GitHub repo pushed, skills installed, router validated."
3. Show me the block and the log entry before saving.
```

---

## LAST STEP — SAVE THIS BRIEF WHERE YOU'LL FIND IT

> **Do this as soon as you receive this document**, in front of your facilitator if it's a live session.

1. Save this document into your vault at `00 HUB/00 INBOX/Next Steps Brief.md`, and Doc 06 next to it. If they're in your Downloads folder, ask Claude to move them there.
2. In Obsidian, open `00 HUB/00 INBOX/` and confirm you see `Next Steps Brief.md`, Doc 06 and `AIAC Cheat Sheet.md` in the same folder.
3. Pin the brief and the cheat sheet.

If the cheat sheet isn't there, regenerate it with the cheat-sheet step of your Main Setup Prompt (load the file by path and ask for that step only).

**Why this matters:** it's easy to leave a session with the homework roadmap floating in a chat window, a download folder or an email, and lose track of it within 48 hours. INBOX is the one folder you always know how to find.

---

> *Part of the AI Acceleration Club Phase 0 program. This roadmap distills patterns refined over months of daily Claude Code use into a step-by-step ramp for your first month.*
