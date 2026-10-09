---
title: "Next Steps Brief (Participant) — AIAC Phase 0 Co-Facilitator Kit (EN)"
created: 2026-07-14
category: reference
status: draft
tags: [aiac, phase0, co-facilitator, next-steps, english]
---

*Given to the participant at session end (Block 5) as their homework roadmap.*

# Next Steps Brief — Claude Code Mastery

> **What this is:** Your roadmap from setup to productive daily use. Organized in priority order — do Week 1 first, then expand.
> Each section has exact prompts you can paste. No thinking required — just copy, paste, go.

---

## PART 0: INSTALL ESSENTIAL PLUGINS (Do First)

> **This brief is prompt-driven.** Wherever Claude can run a command for you, you get a **paste-ready prompt** instead of a list of commands to type yourself — paste it into Claude Code and Claude does the work, you confirm. The raw commands stay as a fallback. (The same principle runs through the rest of this brief: when you see a prompt block, paste it; when you see a terminal command, that's either the fallback or a step Claude genuinely can't do for you — like clicking an app's settings or a browser OAuth.)

**Paste this into Claude Code:**

```
Install these plugins for me, one by one, then run `claude plugins list` to confirm they
all landed. If one fails, tell me which one and the error, and we'll fix it before moving
on:

- explanatory-output-style  (Claude explains its reasoning while it works)
- commit-commands           (smart git commits via /commit)
- skill-creator             (create your own custom commands)
- claude-md-management      (keep your CLAUDE.md healthy)
- context7                  (up-to-date docs for any library)
- code-review               (code quality review)
- firecrawl                 (web research, scraping, reading documentation)
- playground                (interactive HTML visualizations)
```

Claude installs each (via `claude plugin install <name>@claude-plugins-official`) and reports the final `claude plugin list`.

<details><summary><b>Fallback — run them yourself in a terminal</b></summary>

Open your regular terminal (not inside Claude Code) and run:

```bash
claude plugin marketplace add anthropics/claude-plugins-official   # only if not already configured
claude plugin install explanatory-output-style@claude-plugins-official
claude plugin install commit-commands@claude-plugins-official
claude plugin install skill-creator@claude-plugins-official
claude plugin install claude-md-management@claude-plugins-official
claude plugin install context7@claude-plugins-official
claude plugin install code-review@claude-plugins-official
claude plugin install firecrawl@claude-plugins-official
claude plugin install playground@claude-plugins-official
```

`claude /install-plugin` and `claude plugins add` do not exist — a plugin is always `<plugin>@<marketplace>` (corrected 2026-09-23).
</details>

**You should already have from earlier in today's session:** Compound Engineering, Superpowers (installed during your Skills & Config step, Doc 3).

> **On Claude Pro?** Watch your usage caps — space heavy sessions out across the day rather than burning them back-to-back. On Max, you can ignore this.

---

## PART 0.7: CONCEPTS & INSTALLED STACK — READ THIS FIRST

> **Why this section exists:** During your Phase 0 session we moved fast through a lot of plumbing. This is the "theory + inventory" page — the reference you come back to when you want to understand *why* something is wired the way it is, or *what exactly got installed on your machine*. Read it once end-to-end before Week 1 starts. Then skim it weekly for the first month.

### The 4 Core Concepts

You only need to grok 4 concepts to be productive with Claude Code. Everything else flows from these.

#### 1. CLAUDE.md — The System's Brain

There isn't ONE `CLAUDE.md`. There's a **chain** of them that Claude reads automatically at session start:

| Location | Purpose | When Claude reads it |
|----------|---------|---------------------|
| `~/.claude/CLAUDE.md` | **Global router + your profile.** Tells Claude where your vault is, who you are, your defaults. | Every session, regardless of starting directory |
| `[vault]/CLAUDE.md` | **Vault rules.** How to handle notes, PARA structure, safety, language. | Every session started inside the vault |
| `[repo]/CLAUDE.md` | **Project rules.** Schema, domain principle, data sources, stack, validation rules. | Every session started inside that repo |

**Key mental model:** CLAUDE.md is how the system **improves over time**. Every time you correct Claude, add the rule to the appropriate CLAUDE.md. Next session, the correction sticks. After a month, Claude genuinely works better for YOU because the rules accumulate.

**Location-by-specificity rule:** Add a correction to the MOST SPECIFIC CLAUDE.md that applies. If the rule is project-specific, it goes in the repo's CLAUDE.md. If it's about how you take notes in general, it goes in the vault's CLAUDE.md. If it's about your defaults across ALL projects (e.g., "always use English"), it goes in `~/.claude/CLAUDE.md`.

#### 2. Context Window — Your Working Memory

Claude's context window is limited (~200K tokens). As you work in a session, it fills up with conversation history, files Claude reads, tool outputs, etc. When it fills past a certain point, **quality degrades** — this is called **context rot**.

**The thresholds that matter:**
- **Compact IDEALLY before 50%** — best quality, zero degradation, clean state carry-over. This is the target.
- **Compact CERTAINLY before 70%** — past 70%, output quality falls off a cliff. Hitting this threshold mid-task is expensive because a forced reactive compact is much messier than a proactive one.
- **After 50% context rot starts to kick in** — not catastrophic, but Claude starts forgetting earlier context, making inconsistent references, and confusing details. Quality degrades gradually from 50% → hard wall near 70%.

**The compact options at the threshold:**
- Run `/session-close` then `/clear` to start fresh (cleanest — fully preserves state in project brief's Continuation Prompt, then resets).
- Or run `/compact` to summarize in place and keep the same session going mid-task (faster, but lossy — it drops detail, so prefer the option above at a natural break point).

**How to see your usage:** Your context % shows as a live bar in the status line at the bottom of the terminal — set up during your Main Setup Prompt session (Doc 2), the four-layer context monitor. The bar turns **yellow ⚠ at 50%** (with a one-shot sound) and **red 🚨 at 75%**, and auto-compaction is **hard-stopped at 75%** so you get a chance to run `/session-close` (which preserves plans/tasks to your project brief) before context is compressed. If the bar isn't visible, type `/context` to see the current state, or ask Claude to re-run the statusline + hook setup from Doc 2.

**Why this exists:** LLMs have a hard limit on how much text they can "think about" at once. Unlike human short-term memory, it doesn't gracefully degrade all the way — it starts gradually (at ~50%) and then hits a wall (~70%). Proactive compaction beats reactive cap-hit every time.

#### 3. Skills — Reusable Procedures

A "skill" is a structured prompt + workflow stored at `~/.claude/skills/{name}/SKILL.md` that Claude can invoke via `/{name}`. You already have `/session-close` installed from earlier in today's session (Doc 3).

**How to invoke a skill:** Type `/` in Claude Code and pick from the autocomplete, OR type the skill name explicitly (e.g., `/session-close`).

**When to create a new skill:** If you find yourself giving Claude the same instructions 3+ times, it's skill-worthy. Run `/skill-create` — Claude walks you through defining the skill interactively.

**Why skills matter:** They turn ad-hoc patterns into durable infrastructure. A skill you write in Week 2 still works in Month 6 without you remembering the details.

#### 3.5. Multi-Session Workflow — Vault and Repo Are Two Different Places

You'll often have **two Claude Code sessions open at once** — one in your vault (notes, planning, briefs) and one in your project's repo at `~/dev/[your-repo-name]` (code, data, scripts). This is normal, not an edge case — it's how the router + CLAUDE.md chain is designed to work.

**Why the split matters:**

1. **Skill loading is new-session-only.** When a skill gets installed (like `/session-close` earlier in today's session), it doesn't retrofit the session that's already running. It shows as "installed" but isn't "active" until you open a new Claude Code window. Tonight, that's exactly why you'll use the Manual Close Prompt (see APPENDIX) instead of `/session-close` — from your next session onward, `/session-close` works normally.
2. **Each project has its own CLAUDE.md + its own state.** Running your case analysis inside a vault-planning session mixes two different logs together. Keep vault work and repo work in separate windows.
3. **The router resolves you into the right project.** From any cwd, typing "let's work on my [case name]" opens your case project in a fresh session with its Continuation Prompt loaded — no `cd`, no clarifying questions.

**Day-to-day pattern:** when you switch projects, open a new terminal → `claude` → say "let's work on my [X]." You don't need to close the old one first if you're coming back to it.

#### 4. MCPs — External System Connectors

MCP = "Model Context Protocol". It's how Claude Code talks to external systems (Google Workspace, Granola, GitHub, databases, etc.) beyond just your filesystem.

**In today's session you got:**
- **Claude.ai Google Workspace connectors** (activated during your Skills & Config session, Doc 3) — let Claude read your Drive / Docs / Sheets / Gmail drafts / Calendar from the Claude.ai chat UI
- **Granola MCP** (activated during your Skills & Config session, Doc 3) — lets Claude fetch your meeting transcripts + AI summaries

**How to add more later:** Edit `~/.claude/settings.json` and add entries under `mcpServers`. Common ones worth adding when needed: Playwright (browser automation), Supabase/Postgres (database queries), Slack (team messaging), SQL Server (corporate DB).

**When to add an MCP vs. a CLI:** MCPs are "structured connectors" — Claude gets typed tools with defined inputs/outputs. CLIs are "raw commands" — Claude types shell commands. MCPs are cleaner for frequent operations; CLIs are better for one-off or OS-level tasks. For Google Workspace CLI operations from Claude Code (not the chat UI), install the `gws` CLI later when a workflow specifically needs it (see PART 0.9).

### Best Practices — The Core Loop

These are the 7 habits that separate productive Claude Code users from the rest. Internalize all 7 by Week 4.

1. **Always `/session-close` before ending.** No exceptions. This is the habit that makes the system compound.
2. **Plan before building.** Any task that touches 2+ files: `Shift+Tab` twice for Plan Mode. Big/new projects: `/ce:plan`.
3. **Correct Claude out loud, then persist the correction.** When Claude does something wrong, say "that's not right because X. Now update the CLAUDE.md so it doesn't happen again." This IS the self-improvement loop.
4. **Monitor context window proactively.** At ~50%, compact or close. Never let it hit the hard cap mid-task.
5. **Capture lessons.** Any surprising behavior, gotcha, or workaround → append one line to a lessons log at end of session.
6. **Open Claude Code daily, even 10 min.** The habit is more important than the output in Week 1.
7. **Trust the CLAUDE.md chain.** If Claude is confused, it's usually because a CLAUDE.md is missing or wrong — not because Claude is broken. Fix the CLAUDE.md.

### What Got Installed On Your Machine Today

Full inventory, in case you need to audit, replicate, or troubleshoot later.

**Global files:**

| Path | What it is | Edit when... |
|------|-----------|--------------|
| `~/.claude/CLAUDE.md` | Global router + your profile | Your vault moves, your role changes, you want to add global defaults |
| `~/.claude/settings.json` | Permissions (pre-approved commands) + hooks (session-end sound, etc.) | You want Claude to ask permission less often, or to fire events on session lifecycle |
| `~/.claude/skills/session-close/SKILL.md` | The `/session-close` skill | You want to change how sessions are closed (rare) |

**Vault files created:**

| Path | What it is |
|------|-----------|
| `[vault]/CLAUDE.md` | Vault-level rules (PARA, language, safety) |
| `[vault]/Templates/Project Brief Template.md` | Reusable template for new projects |
| `[vault]/01 PROJECTS/[project name]/[project name].md` | Your case project brief |
| `[vault]/01 PROJECTS/AI Acceleration Club — [your name].md` | Tracks your progression through the program |
| A lessons log in your vault | Where you log one-liner lessons after each session |
| `[vault]/00 HUB/00 INBOX/AIAC Cheat Sheet.md` | Quick reference card |

**Repo files:**

| Path | What it is |
|------|-----------|
| `~/dev/[your-repo-name]/CLAUDE.md` | Project-level rules (schema, principles, data sources, stack) + pointer to the vault brief |
| `~/dev/[your-repo-name]/README.md` | Human-facing intro to the project |
| `~/dev/[your-repo-name]/.gitignore` | Prevents uploading data/secrets to GitHub |
| `~/dev/[your-repo-name]/data/{raw,working,processed}/` | Data zones (raw = gitignored, processed = committed) |

**Plugins installed today (Doc 3 + Part 0 above):**

| Plugin | Main commands | What it does |
|--------|--------------|--------------|
| Compound Engineering | `/ce:plan`, `/ce:work`, `/ce:brainstorm`, `/ce:review` | Plan → research → build workflow |
| Superpowers | `/brainstorm`, `/systematic-debugging`, `/test-driven-development`, `/verification-before-completion` | Structured thinking + debugging |
| Explanatory Output Style | (automatic) | Claude explains its reasoning as it works |
| Commit Commands | `/commit`, `/commit-push-pr` | Smart git commits with auto messages |
| Skill Creator | `/skill-create` | Interactive skill creation |
| Claude MD Management | `/claude-md-improver` | Audit and improve CLAUDE.md files |
| Context7 | (automatic) | Up-to-date library docs when you reference them |
| Code Review | `/code-review` | Bug / security / quality review |
| Firecrawl | (replaces web search) | Web research + scraping |
| Playground | `/playground` | Interactive HTML visualizations |

**MCP connectors:**

| Connector | What it exposes |
|-----------|-----------------|
| Claude.ai Google Workspace | Drive, Docs, Sheets (read + write), Gmail (draft only), Calendar (full CRUD) — from Claude.ai chat |
| Granola | Meeting transcripts + AI summaries |

> **If a claude.ai connector (Gmail / Drive / Calendar / Granola) didn't finish authorizing during the session:**
>
> Go back to claude.ai → Settings → Connectors, find the connector, and complete the OAuth flow. Verify it worked with a quick test prompt in Claude Code, e.g. *"List my 3 most recent emails."* If it still won't authorize, flag it to your facilitator with the exact error you see on the OAuth screen.

**Hooks:**

| Event | Hook | What happens |
|-------|------|--------------|
| `Stop` (session end) | Sound beep | Audible notification when Claude finishes a task |

### How to Troubleshoot When Something Feels Off

Quick decision tree:

- **Claude doesn't know about my project** → `~/.claude/CLAUDE.md` router may be broken. Re-run the fresh-window test from Phase 0 Block 7.
- **Claude is making the same mistake repeatedly** → the correction didn't get persisted. Open the relevant CLAUDE.md and verify the rule is there.
- **Session feels slow or Claude is forgetting things** → context window is full. Run `/session-close` then `/clear`.
- **A plugin command isn't found** → plugin may not be installed. Run `claude plugins list` to see what's loaded.
- **A skill command isn't found** → skill may be in a plugin, not global. Check `~/.claude/skills/` vs `~/.claude/plugins/*/skills/`.
- **Something errors in the terminal** → copy the error, paste it back to Claude, ask "what is this error?" (this is the universal fallback).

---

## PART 0.8: OPTIONAL — LEVEL UP YOUR OBSIDIAN

> **Optional, not required.** Phase 0 already set the four load-bearing Obsidian settings
> (new notes → `00 HUB/00 INBOX`, wikilinks, show all file types, auto-update links). Everything
> below is *amplification* — community plugins and deeper settings that make your vault
> more powerful. Add them when you want the capability, not because you have to. Each entry
> says **what it's for** and **how to set it up**.

### Community plugins worth installing

Install path is the same for all of them: **Settings → Community plugins → Turn on
community plugins → Browse → search the name → Install → Enable (toggle ON)**. Install one,
try it, then come back for the next — don't bulk-install five plugins you won't touch.

| Plugin | What it's useful for | How to set it up |
|--------|----------------------|------------------|
| **Dataview** | Live queries over your notes' frontmatter — the engine behind any compiled dashboard or "show me all active projects" view. The single highest-leverage plugin for a PARA vault. | Install + enable. Then in its settings turn **ON**: "Enable inline queries", "Enable JavaScript queries", "Enable inline JavaScript queries". Test in a note: a fenced ```` ```dataview LIST FROM "" LIMIT 5 ``` ```` block should render a list of files. |
| **Tasks** | Real task management on top of `- [ ]` checkboxes — due dates, priorities, recurrence, and queries like "everything due this week across the whole vault". | Install + enable. In its settings turn ON "Set done date on every completed task". Test: type `- [ ] Test 📅 2026-12-31` — it gets a date pill. |
| **Templater** | Placeholder substitution in templates (`{{title}}`, `{{date}}`, dynamic snippets) — turns your Project Brief Template into a fill-itself-in scaffold. | Install + enable. Point its "Template folder location" at `Templates/`. |
| **Calendar** | A sidebar mini-calendar tied to daily notes — click a day to open/create that day's note. Pairs with Periodic Notes. | Install + enable. No config needed to start. |
| **Periodic Notes** | Daily / weekly / monthly note creation with templates — the backbone of a journaling or daily-log habit. | Install + enable. Turn on "Daily Notes", set its template + folder. |

### Deeper settings (optional)

A couple of settings beyond the Phase 0 four, for when you want them:

- **Attachments in one folder.** Settings → Files and links → **Default location for new
  attachments** → "In the folder specified below" → e.g. `assets`. Keeps pasted images
  and PDFs out of your note folders.
- **Shortest link format.** Settings → Files and links → **New link format** → "Shortest
  path when possible". Cleaner `[[Note]]` links instead of full paths.

### Power-user route: write the settings files directly

Everything above can also be set by editing the JSON files in the hidden `.obsidian/`
folder inside your vault (faster than clicking, and scriptable). Only do this if you're
comfortable — and **restart Obsidian afterward**. Ask Claude Code:

```
Open the .obsidian/ folder in my vault and show me app.json. I want to set:
attachments → "assets", new link format → shortest, and confirm new notes go to 00 HUB/00 INBOX.
Then walk me through enabling Dataview inline queries via its data.json.
```

---

## PART 0.9: OPTIONAL — gws CLI FOR DEEPER GOOGLE WORKSPACE INTEGRATION

> **Optional enrichment, Google-stack only.** Today's session wired the **claude.ai Connectors** (Gmail / Drive / Calendar / Granola) — that covers ~90% of what you'll need and is the right default. Add the **gws CLI** later only when you outgrow the Connectors and need to **drive Google Workspace programmatically from scripts** — especially **writing to Google Sheets** (formulas, batch range updates, schema), which the Connectors don't do. Skip entirely if you're on Microsoft 365 / Outlook or you don't script against Sheets.

**What it unlocks beyond Connectors:** the full Google Workspace API surface in one binary — Sheets *writes*, Apps Script, advanced Drive/Calendar — callable from Python/bash so Claude can build real automations (a nightly report that writes to a Sheet, a form-driven pipeline, etc.).

**When to bother:** your project needs Claude to *edit* a spreadsheet, not just read it; or you're building a scripted automation around Google Workspace.

**How** — same install path as the optional gws CLI section covered in your Skills & Config session (Doc 3), if you touched it there; otherwise budget ~1.5h end to end (gcloud + the `gws` binary + OAuth). To set it up now, paste into Claude Code:

```
I want to install the gws CLI so I can write to Google Sheets from Claude Code. Walk me
through it step by step: check whether I have gcloud, install the gws binary to ~/bin,
run the OAuth authentication, test a read command, and add a "Google Workspace Tools"
rule to my vault's CLAUDE.md. If anything fails, we'll troubleshoot it together.
```

Claude runs the install with you. (Heads-up it knows: gws ranges containing `!` need Python `subprocess`, not raw bash.)

---

## PART 0.10: OPTIONAL — SELF-GUIDED COURSES FROM YOUR VAULT

> ⚠ **Not installed by this kit.** `/notebooklm` is a custom skill, not part of the starter-pack or any plugin above — the prompt below has nothing to call until you build it (`/skill-create`) or your facilitator shares theirs. Treat this section as a pattern to build toward, not a command to run today.

> **Optional enrichment.** Turn your own vault material — a project brief, a cluster of notes, a wiki, a set of meeting minutes — into a **self-guided course**: a NotebookLM notebook with study decks, a narrated overview, and a Q&A you can interrogate. Great for going deeper on a topic you're building in, or onboarding yourself (or your team) to a body of knowledge you've accumulated.

**What it does:** `/notebooklm` takes the vault sources you point it at and produces a structured study set — outline → decks → narrated overview — so you *learn* the material instead of just storing it. The compounding move: your second brain doesn't just hold knowledge, it teaches it back to you.

**When to use:** you've accumulated enough on a topic (a project, an area MOC, a wiki) that a guided walkthrough beats re-reading raw notes.

**How** — paste into Claude Code:

```
I want to turn [name your project / folder / wiki] into a self-guided course with
/notebooklm. Build the course outline from those notes and generate the study decks.
Before generating, tell me which sources you'll use.
```

Claude scopes the sources with you, then runs `/notebooklm` to build the course.

---

## PART 0.11: GENERATE YOUR CONSOLIDATED USER GUIDE

> **Do this once, after the rest of setup is done.** You now have a vault, a repo, plugins, skills, and a context monitor spread across a few places. This generates a single **`User Guide — [your name].md`** at your vault root — the one map of *what you have and how it fits*. It complements (doesn't replace) your **AIAC Cheat Sheet** (quick command reference) and the homework below. (Generated in one pass from your real setup — robust to whatever order you installed things in.)

**Paste this into Claude Code:**

```
Generate my consolidated User Guide at `User Guide — [your name].md` at the root of my
vault. Read what's ACTUALLY installed and configured on my system — don't guess. Three
short, navigable sections:

- Section A — My Vault: the PARA structure, the CLAUDE.md chain (global → vault → repo),
  the 4 Obsidian settings, and where everything lives (vault vs. repo).
- Section B — Claude Code: the plugins and skills I have installed, the context monitor
  (the 50/75% bar), and Plan Mode. For the command quick-ref, point to my AIAC Cheat
  Sheet instead of duplicating it.
- Section C — My case workflows ([your project name]): the 2-3 concrete workflows for
  my project and their starter prompts.

It's a map, not a manual — keep it short.
```

Claude reads your real setup and writes the guide. Re-run it any time your system grows.

---

## PART 1: POST-SESSION HOMEWORK — TONIGHT, THIS WEEK, CHEAT SHEET, STUCK

> **Goal:** Get real data into the repo, build your first analysis, start the self-improvement loop. Structured in 4 layers so nothing falls through.

### 1. Tonight (3 mini-actions, before bed)

These three are tiny. Do them tonight while the session is still fresh.

- [ ] **Open your vault.** `cd "[vault path]" && claude` — confirm the session starts and the router loads. If `~/.claude/CLAUDE.md` doesn't pick up your vault → flag it to your facilitator.
- [ ] **Run the Manual Close Prompt (see APPENDIX).** `/session-close` isn't active in this session yet (it was installed today — skills only activate in a fresh session). This logs today's Phase 0 work into your project brief and writes the Continuation Prompt. The habit starts tonight, not next week.
- [ ] **Write tomorrow's project intention** into the case brief's Next Actions section — one line: "Tomorrow I want to ___." This anchors Day 1.

### 2. This Week (5 things to try, in order)

Sequenced ramp into real usage. Don't skip ahead — each step builds on the previous one. (This is a general pattern — your specific version of each step lives in PART 3, "Your Project's Next Workflows," which you fill in at the end of today's session.)

1. Drop the first real data file you brought to today's session into `data/raw/` in your repo and ask Claude to inventory it — what's in it, what's missing, what questions it could answer.
2. Run your first real analysis using the prompt you and your facilitator drafted together in PART 3.
3. Turn that first analysis into a saved output — a report, a script, or a note in your project brief — so it's not just left sitting in chat history.
4. Automate the most annoying manual step in your workflow — the one thing you do by hand every week. Ask Claude to script or template it.
5. Correct Claude at least once out loud, then say "update the CLAUDE.md so this doesn't happen again." This is your first rep of the self-improvement loop (PART 7).

> **For your NEXT project (NOT today's case — a brand-new one):** run `/project-create` and let the skill guide you with questions. **Don't ask for another Setup Prompt** — from here on, the flow is self-serve via `/project-create`. The Setup Prompt is only for Phase 0; after that, you have the skill installed.

### 3. Cheat Sheet — Always In The Same Place

Your cheat sheet lives at exactly this path:

```
00 HUB/00 INBOX/AIAC Cheat Sheet.md
```

That's the canonical location — not scattered in `03 REFERENCE/`, not floating somewhere else. Pin this file in Obsidian.

The cheat sheet was created during your Main Setup Prompt session (Doc 2). If you can't find it: open Obsidian, navigate to `00 HUB/00 INBOX/`, and look for `AIAC Cheat Sheet.md`. If missing → flag it to your facilitator, or ask Claude to re-run Doc 2's cheat-sheet step to regenerate it.

The cheat sheet contains: session-start commands, the router prompt, essential commands, context-window thresholds, file anchors. Everything you need in one screen.

### 4. Stuck? — Where To Get Help

You're not on your own after the session. Help is **tiered** — start at the top and only escalate when you need to:

1. **Claude first (most issues).** Paste errors back into Claude, try `/systematic-debugging`, check the CLAUDE.md chain. Give it ~24h of solo debugging before escalating — most things resolve right here.
2. **Your support channel: [SET: your support channel].** For day-to-day doubts, installer/setup problems, or a quick "is this normal?" — ask here. Don't sit stuck in silence — a shared question resolves faster, and helping each other is part of how a cohort levels up.
3. **Your facilitator — for infra blockers.** Reach out immediately if you're blocked on: a tool install failure, an auth/login issue, an MCP config that won't connect, or a router test failure. Don't burn a day on infra plumbing — that's the kind of thing your facilitator can usually unblock in minutes.

**When you ask for help (any tier):** include the prompt you ran, the exact error output, and what you already tried. "It's broken" is not a debug message.

### 5. End of Week 1 — Close Properly

```
/session-close
```

---

## PART 2: WEEK 2 — BUILD YOUR DAILY HABITS

### Morning: Start Your Day

```
Read my project brief at 01 PROJECTS/[project name].md.
What are my open next actions? What's the most important thing to work on today?
If there's a Continuation Prompt, summarize where I left off.
```

### During Work: Use Plan Mode

For any non-trivial task, enter **Plan Mode** first:
- Press `Shift+Tab` twice
- Describe what you want
- Review the plan
- Approve and execute

### Before Ending: Always Close

```
/session-close
```

This updates your project brief, logs what you did, and creates a continuation prompt. **This is the single most important habit.** Every session makes the next one better.

### Weekly: Review Progress

```
Read 01 PROJECTS/[project name].md.

Give me a weekly progress report:
1. What milestones have been completed?
2. What's in progress?
3. What's blocked and by whom?
4. What should I focus on next week?
5. Are we on track for the milestone targets?
```

---

## PART 3: YOUR PROJECT'S NEXT WORKFLOWS

Unlike a pre-configured cohort, your case wasn't picked in advance — you and your facilitator chose it live, during today's session, from the 1-3 problems you brought in. So this section starts blank on purpose. Fill it in before you leave (Block 5), while the session is still fresh — it becomes your personal version of PART 1's "This Week" ramp and PART 8's progression map.

**How to fill this in.** Ask Claude directly:

```
Based on everything we built and discussed today for [your project name], help me draft
3-5 workflows I'll actually run again — recurring reports, analyses, or documents specific
to my work. For each one, give me:
1. A short name
2. When I'd use it
3. A paste-ready prompt with real file paths from my repo

Save this list into my project brief's Next Actions, and also write it out below so I
have it in this brief too.
```

Then write each one out here, following the same shape as PART 4's general prompts below — a short name, a one-line description of when you'd use it, and the exact paste-ready prompt.

### Workflow 1: _______________________________
```
[paste-ready prompt — fill in during/after today's session]
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

> **Want a more structured day-by-day Week 1 plan instead of just a workflow list?** Ask Claude: *"Help me turn the workflows above into a day-by-day Week 1 schedule."*

---

## PART 4: GENERAL PRODUCTIVITY PROMPTS

### Research Any Topic

```
/deep-research [topic]

Example:
/deep-research best practices for [relevant topic to your domain]
```

### Create a New Project

Open Claude Code in your vault, then:

```
I need to create a new project. Help me fill out a Project Brief.

Project name: [NAME]
What I want to achieve: [DESCRIBE THE OUTCOME]

Use the Project Brief Template in Templates/ and save the brief in 01 PROJECTS/.
```

### Make a Decision

```
I need to make a decision about: [DESCRIBE THE DECISION]

Help me think through this structured:
1. What are the options? (at least 3)
2. What are the pros and cons of each?
3. What's the risk if we pick wrong?
4. What information am I missing?
5. What's your recommendation and why?

Save this as a decision memo in 00 HUB/00 INBOX/.
```

### Analyze a Spreadsheet

```
Read the file [FILENAME] in data/.
Tell me:
1. What's in this data? (columns, row count, date range)
2. Summary statistics for the numerical columns
3. Any patterns, trends, or anomalies
4. 3 questions this data could answer
5. What other data would I need to combine with this for a complete picture?
```

### Create a Custom Skill

When you find yourself doing something repeatedly:

```
/skill-create

I keep doing [DESCRIBE THE REPEATED TASK].
Help me create a skill that automates this.
```

### Git Workflow

```
# After finishing work:
/commit

# If you want to push too:
/commit-push-pr
```

---

## PART 5: SKILLS CATALOGUE — PRIORITIZED

> 🚀 **SHORTCUT — Install the starter-pack first.** The program maintains a curated public repo with all 8 Tier 1 skills pre-configured and ready to install in one go:
>
> **[wildbuffaloman/cc-starter-pack](https://github.com/wildbuffaloman/cc-starter-pack)** — public
>
> ```bash
> # Clone + install Tier 1 skills with one command:
> git clone https://github.com/wildbuffaloman/cc-starter-pack.git
> cd cc-starter-pack
> ./install.sh                # copies into ~/.claude/skills/ (default)
> ./install.sh symlink        # symlinks instead — keep updated via `git pull`
> ```
>
> All 8 skills ship with canonical `## Dependencies` sections declaring exactly what each needs. Only `/session-close` has external CLI requirements (`jq` + `git`); the rest work with Claude Code's built-in tools out of the box.
>
> **After running `./install.sh`: restart Claude Code, then test with `/context`** — if it runs, you're set.
>
> **Why a starter-pack instead of building from scratch?** The skills below took months to refine. The pack ships that expertise so you start productive on day 1 instead of reinventing patterns. Tier 2+ skills (below) you'll build or request individually as your needs emerge.
>
> If you prefer copying a single skill manually: each SKILL.md in the repo is self-contained — copy into `~/.claude/skills/[skill-name]/SKILL.md`. Skills marked with a prompt in the tables below can be tested immediately even without installation — just paste the prompt.

### TIER 1 — ESSENTIAL (Install Week 1 — all 8 are in the starter-pack above)

These are the skills you'll use in almost every session. Install all 8 at once via the starter-pack, or individually.

| # | Skill | What it does | How to use | In starter-pack? |
|---|-------|-------------|-----------|------------------|
| 1 | **session-close** | Closes session properly — updates brief, logs work, creates continuation prompt, code review, retro | `/session-close` | ✅ |
| 2 | **context** | Shows current context window usage and session info | `/context` | ✅ |
| 3 | **permissions** | Display current permission settings | `/permissions` | ✅ |
| 4 | **retro** | Run a retrospective — what worked, what didn't, what to change | `/retro` | ✅ |
| 5 | **extract** | Smart content extraction from any note or URL — structured 6-section output | `/extract [note or URL]` | ✅ |
| 6 | **skill-create** | Create new custom skills interactively | `/skill-create` | ✅ |
| 7 | **project-create** | Create a project brief through interactive Q&A | `/project-create` | ✅ |
| 8 | **deep-research** | Two-phase deep research — broad sweep then synthesis into structured brief with sources | `/deep-research [topic]` | ✅ |

### TIER 2 — DAILY PRODUCTIVITY (Install Week 2)

These are Tier B candidates from the starter-pack initiative — they'll ship as a second pack after Tier 1 proves out. For now, your facilitator can point you to them individually, or you can rebuild from the pattern.

| # | Skill | What it does | How to use |
|---|-------|-------------|-----------|
| 9 | **startup-day** | Morning command center — aggregates tasks, calendar, follow-ups into prioritized action plan | `/startup-day` |
| 10 | **close-day** | End-of-day close — scan all systems, update briefs, sync tasks, tomorrow preview | `/close-day` |
| 11 | **last30days** | Search Reddit, X, YouTube, HN, etc. for what's happening right now (⚠ requires paid ScrapeCreators API key + `yt-dlp`) | `/last30days [topic]` |
| 12 | **library** | Create a Library index note for a topic, pre-populated with linked vault notes | `/library [topic]` |

### TIER 3 — WEEKLY WORKFLOWS (Install Week 2-3)

| # | Skill | What it does | How to use |
|---|-------|-------------|-----------|
| 13 | **weekly-review** | Full GTD weekly review — vault scan, calendar, inbox clear, task sync, next-week planning | `/weekly-review` |
| 14 | **weekly-prep** | Plan next week's calendar — deep work scheduling, routine events, meeting agendas | `/weekly-prep` |
| 15 | **monthly-review** | Monthly strategic review — priority recalibration, project health, personal finance, reflections | `/monthly-review` |
| 16 | **inbox-clear** | GTD inbox clearing — classify every note, propose actions, execute after approval | `/inbox-clear` |
| 17 | **read-review** | Review READ_REVIEW items — structured summaries, key takeaways, action items | `/read-review` |
| 18 | **meeting-agenda** | Create/update meeting agendas with calendar + vault + external context | `/meeting-agenda [meeting name]` |
| 19 | **meeting-minutes** | Generate meeting minutes from Granola recordings | `/meeting-minutes` |
| 20 | **followup** | Scan project briefs for Waiting For items, classify by eligibility, send follow-ups | `/followup` |

### TIER 4 — BUSINESS ANALYSIS (Install Week 3-4)

| # | Skill | What it does | How to use |
|---|-------|-------------|-----------|
| 21 | **decision-memo** | Structured decision document — context, 3+ alternatives, analysis, recommendation | `/decision-memo` |
| 22 | **strategy-brief** | Strategic analysis for a business decision, market move, or initiative | `/strategy-brief` |
| 23 | **scenario-model** | Build 3+ scenarios with probability-weighted outcomes and sensitivity analysis | `/scenario-model` |
| 24 | **okr-update** | Update OKR scorecard — review progress, flag off-track items | `/okr-update` |
| 25 | **okr-cascade** | Review OKR alignment — cascade from company to team/individual, identify gaps | `/okr-cascade` |
| 26 | **blind-spot-scan** | Socratic blind-spot analysis — surface unknown unknowns through probing questions | `/blind-spot-scan` |
| 27 | **learning-program** | Create a structured learning program on any topic with AI skill deconstruction | `/learning-program [topic]` |
| 28 | **contact-card** | Create a rich Contact Card — combines vault data, web research, relationship context | `/contact-card [name]` |

### TIER 5 — NEGOTIATION & SALES (Install When Needed)

| # | Skill | What it does | How to use |
|---|-------|-------------|-----------|
| 29 | **negotiation-prep** | Full negotiation preparation — counterparty research, BATNA, stakeholder mapping, playbook | `/negotiation-prep` |
| 30 | **negotiation-coach** | Live negotiation coaching — routes to prep, live, or debrief mode | `/negotiation-coach` |
| 31 | **batna-analysis** | Focused BATNA modeling — identify, evaluate, rank alternatives for a specific deal | `/batna-analysis` |
| 32 | **concession-framework** | Design a structured concession sequence — tradeable items, sequencing, reciprocal asks | `/concession-framework` |
| 33 | **objection-tree** | Navigate objection decision trees with Voss/Black Swan/Gap tactics | `/objection-tree` |
| 34 | **stakeholder-map** | Map counterparty decision architecture — 6 stakeholder types with engagement strategy | `/stakeholder-map` |

### TIER 6 — VAULT MANAGEMENT (Learn Later)

| # | Skill | What it does | How to use |
|---|-------|-------------|-----------|
| 35 | **clean-areas** | Audit 02 AREAS/ — fix MOC drift, enforce templates, detect orphans | `/clean-areas` |
| 36 | **clean-projects** | Audit 01 PROJECTS/ — template compliance, staleness detection | `/clean-projects` |
| 37 | **clean-reference** | Audit 03 REFERENCE/ — detect misrouted files, enforce structure | `/clean-reference` |
| 38 | **vault-link-scan** | Zettelkasten link scan — discover connections, insert wikilinks, fix broken links | `/vault-link-scan` |

### TIER 7 — META / TOOLING (Advanced)

| # | Skill | What it does |
|---|-------|-------------|
| 39 | **bible-sync** | Monthly sync of Claude Code Bible against live setup |
| 40 | **skills-audit** | Scan skill directories, cross-reference configs |
| 41 | **skill-health-report** | Generate health report for all skills |
| 42 | **push-skills** | Push updated skills to GitHub repos |

---

## PART 6: PLUGIN REFERENCE

### Installed (from your Phase 0 session + Part 0 above)

| Plugin | Key Commands | What it does |
|--------|-------------|-------------|
| **Compound Engineering** | `/ce:plan`, `/ce:work`, `/ce:brainstorm`, `/ce:review` | Plan-first development workflow with parallel research agents |
| **Superpowers** | `/brainstorm`, `/systematic-debugging`, `/test-driven-development`, `/verification-before-completion` | Structured workflows for debugging, brainstorming, TDD |
| **Explanatory Output Style** | (automatic) | Claude explains its reasoning as it works — great for learning how it thinks |
| **Commit Commands** | `/commit`, `/commit-push-pr` | Smart git commits with auto-generated messages |
| **Skill Creator** | `/skill-create` | Interactive skill creation wizard (the `skill-creator` *plugin* from PART 0 provides the same thing — you only need one) |
| **Claude MD Management** | `/claude-md-improver` | Audit and improve CLAUDE.md files |
| **Context7** | (automatic) | Pulls up-to-date docs for libraries when you reference them |
| **Code Review** | `/code-review` | Review code for bugs, security, quality |
| **Firecrawl** | (replaces web search) | Web research, scraping, reading docs — superior to built-in web tools |
| **Playground** | `/playground` | Create interactive HTML visualizations for exploring ideas |

### Optional Plugins (Install Later)

| Plugin | What it does | When to install |
|--------|-------------|----------------|
| **Feature Dev** | Guided feature development with codebase analysis | When building larger features |
| **PR Review Toolkit** | Comprehensive PR code review | When doing code reviews |
| **Frontend Design** | High-quality frontend interface generation | When building UIs/dashboards |
| **Playwright** | Browser automation for testing | When testing web apps |
| **Hookify** | Create hooks to prevent unwanted behaviors | When you want to automate rules |
| **GitHub** | GitHub integration | When using GitHub more heavily |

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

Corrections are domain-specific — they'll come from real mistakes Claude makes on **your** project, not a generic list. Here's the pattern, plus space to log your own as they happen this week:

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
- [ ] Plugins installed (Part 0)
- [ ] Real project data dropped into `data/raw/` (or equivalent) in your repo
- [ ] First analysis pass run and saved (not just left in chat)
- [ ] At least 3 Claude Code sessions completed
- [ ] `/session-close` run at the end of every session
- [ ] First workflow from PART 3 tested end-to-end

### Week 2: Daily Habits
- [ ] Daily morning check-in with your project brief
- [ ] Plan Mode used at least twice
- [ ] First automated/repeatable output generated (a report, script, or template)
- [ ] At least 2 corrections added to your CLAUDE.md (self-improvement loop, PART 7)
- [ ] A `weekly-review` skill **built** with `/skill-create` (it is not in the starter-pack — you build it; see Tier 3) and run once

### Week 3: Operational Workflows
- [ ] 2-3 of your PART 3 workflows tested and refined
- [ ] A custom skill created for a workflow you've repeated 3+ times (`/skill-create`)
- [ ] GitHub repo pushed at least twice
- [ ] Tier 2-3 skills installed (see PART 5)

### Week 4: Autonomy
- [ ] Your top workflow runs on a single paste-ready prompt, no rework
- [ ] CLAUDE.md has 5+ accumulated rules from the self-improvement loop
- [ ] Using Claude Code for 30+ real minutes a day
- [ ] Ready to take on a second project (`/project-create`)

### Month 2: Expansion
- [ ] A second project or case started with `/project-create`
- [ ] Tier 3-4 skills installed and in regular use
- [ ] At least one workflow fully automated end-to-end

### Month 3: Mastery
- [ ] Claude Code is a default part of your daily work, not a novelty
- [ ] You've created 2+ custom skills of your own
- [ ] You're comfortable correcting Claude and updating CLAUDE.md without being prompted to do it

---

## APPENDIX: QUICK REFERENCE CARD

### Start Working

> **Two places, two purposes.** Your vault (notes, planning, briefs) and your project repo (`~/dev/[your-repo-name]`, code + data) are separate folders — the router (`~/.claude/CLAUDE.md`) makes sure Claude reads the right CLAUDE.md chain no matter which one you're in.

```bash
# Notes, projects, thinking (vault root):
cd "[vault path]" && claude

# Code and data (your repo, in ~/dev/):
cd ~/dev/[your-repo-name] && claude
```

### Essential Session Flow
```
1. Start: claude reads CLAUDE.md automatically
2. Check continuation: "Read my project brief. Where did I leave off?"
3. Plan: Shift+Tab twice -> describe task -> review plan -> approve
4. Work: Execute the plan
5. Close: /session-close
```

### When Stuck
```
/systematic-debugging

I'm stuck on: [describe the problem]
What I've tried: [what you already tried]
What I expected: [what should have happened]
```

### When Starting Something New
```
/ce:plan [describe what you want to build]
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

> **When to use:** `/session-close` was installed earlier in this SAME session — skills only activate in sessions opened AFTER they're installed. So tonight, right after today's session ends, use this manual close prompt instead. From tomorrow's session onward, `/session-close` works normally.

```
Please close this session:
1. At the top of my case project brief's Next Actions section, add or replace the
   ### Continuation Prompt block with:
   - Today's date
   - Mode: Vault Management
   - Context summary: what we did in this Phase 0 session (vault scaffolding, project
     brief created, GitHub repo pushed, case file scaffolded, skills installed, router
     test passed)
   - Resume-from: next actions for Week 1 homework
   - Files touched in this session
2. Append a Log entry: "Phase 0 session completed — vault scaffolded, case brief created,
   GitHub repo pushed, skills installed, router validated."
3. Do not invoke /session-close — it's installed but not yet active in this session
   (skills load on new sessions only). Perform the updates directly via Edit.
```

---

## GATE 5.5 — SAVE THIS BRIEF INTO YOUR VAULT (FINAL CONFIRMATION)

> **Run this at session end — before you stand up from the desk.** Prevents the "where did that homework list go?" friction.

Do this NOW, in front of your facilitator if it's a live session:

1. Save this document into your vault at `00 HUB/00 INBOX/Next Steps Brief.md` (copy the content your facilitator shared, or ask Claude to save it there for you).
2. Open Obsidian and confirm you can find it at `00 HUB/00 INBOX/`.
3. Confirm your `AIAC Cheat Sheet.md` (created during your Main Setup Prompt session, Doc 2) is sitting right next to it in the same folder.
4. Say out loud: "I found both files in `00 HUB/00 INBOX/`."

If you can't find one or both files → they haven't landed yet. Re-run Doc 2's cheat-sheet step for the Cheat Sheet, and manually save this brief's content into INBOX. Do NOT close the session until both files are visible from `00 HUB/00 INBOX/` in Obsidian.

**Why this gate exists:** it's easy to leave a session with the homework roadmap floating in a chat window, a Drive link, or an email — and lose track of it within 48 hours. INBOX is the one folder every participant knows how to find. Both files live there, always.

---

> *Part of the AI Acceleration Club Phase 0 program — this roadmap distills patterns refined over months of daily Claude Code use into a step-by-step ramp for your first month.*
