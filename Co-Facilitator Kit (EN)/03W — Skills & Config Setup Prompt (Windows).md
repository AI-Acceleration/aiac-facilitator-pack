---
title: "Skills & Config Setup Prompt (Participant, WINDOWS) — AI Acceleration Club Phase 0"
created: 2026-07-14
category: reference
status: draft
tags: [aiac, phase0, co-facilitator-kit, participant, skills, config, setup-prompt, windows]
---

**Supports:** Block 3 of your live Phase 0 session. Paste the block below into Claude Code when your facilitator tells you to.

# Phase 0 — Skills & Config Setup Prompt (WINDOWS)

> ## Same three Windows rules as Doc 02
>
> 1. **Right-click to paste**, not Ctrl+V.
> 2. **Git Bash**, not PowerShell and not CMD.
> 3. **Forward slashes `/` in every path.** An unquoted `\` is silently stripped in Git Bash and the
>    command fails with no visible error.
>
> **If you started a new Claude Code session since Doc 02, paste this first:**
>
> ```
> Environment: Windows, Git Bash. Forward slashes in all paths. Do not offer me macOS commands
> (afplay, xcode-select, brew, open) or macOS paths (~/Library/...). Take the Windows branch
> without asking.
> ```

This is the **second** prompt you'll paste into Claude Code during the session. It comes right after the Main Setup Prompt (Doc 2) has finished scaffolding your vault and your project. Paste everything below the line into Claude Code and let it walk you through each step, one at a time.

---

## PASTE EVERYTHING BELOW INTO CLAUDE CODE

---

We just finished setting up my vault and project. Now I need you to install the essential plugins, create key skills, and configure a few more things. Walk me through each step one at a time. Confirm each step before moving on.

---

## STEP 1: VERIFY GLOBAL CLAUDE.md ROUTER + ROUTING TEST

My global router `~/.claude/CLAUDE.md` was already created in the **Main Setup prompt (Doc 2)** — the "Global Router" step. Here we just confirm it's in place and run the live routing test before installing skills.

Verify the file:

```bash
head -25 ~/.claude/CLAUDE.md

# Third check, Windows-specific. This MUST print 0.
# Any other number means a backslash path is in the router, which breaks it silently.
grep -c '\\' ~/.claude/CLAUDE.md
```

Confirm that:
1. The first section is `## Default Workspace` (the imperative router), NOT `## Who I Am`.
2. The vault path is resolved (no literal placeholder remains in the file).

Then run the **outside-the-vault routing test** — critical for catching the "profile-only, not router" failure mode:

```bash
cd ~
claude
```

Once Claude Code starts, ask: *"What files are in my vault INBOX?"* If Claude reads my vault's `00 HUB/00 INBOX/` without me giving it the path, the router is working. If it says "I don't know where your vault is", the router was generated as a profile doc, not a router — go back to the Main Setup prompt's "Global Router" step and recreate `~/.claude/CLAUDE.md` with the `## Default Workspace` block at the TOP.

Confirm both checks pass. Move to Step 2.

---

## STEP 2: INSTALL PLUGINS

Run these commands to install essential plugins:

```bash
# Compound Engineering — the Plan -> Build workflow
# Creates structured plans before building, uses parallel research agents
claude plugin marketplace add EveryInc/compound-engineering-plugin
claude plugin install compound-engineering@compound-engineering-plugin
```

```bash
# Superpowers — debugging, brainstorming, TDD, code review
claude plugin install superpowers@claude-plugins-official
```

If `superpowers` or `playground` says the marketplace is unknown, first run `claude plugin marketplace add anthropics/claude-plugins-official`. (`claude /install-plugin` and `claude plugins add` do not exist — corrected 2026-09-23.)

If none of those work, tell me what error you got and we'll troubleshoot.

**After installing, briefly explain what each plugin does:**

- **Compound Engineering:** Gives you `/ce:plan` (create a structured plan with research) and `/ce:work` (execute a plan step by step). The core idea: "unless it's a one-line change, there's always a plan first."
- **Superpowers:** Gives you structured workflows for debugging (`/systematic-debugging`), brainstorming (`/brainstorm`), code review (`/requesting-code-review`), and test-driven development (`/test-driven-development`).

Confirm both are installed. Move to Step 2.5.

---

## STEP 2.5: EMAIL / WORKSPACE INTEGRATION (branches by your work email stack)

First, tell me which email/calendar stack you use for work — this decides which path we follow:

- **Google Workspace / Gmail** → follow **Path A** below
- **Microsoft 365 / Outlook** → follow **Path B**
- **Something else** (Fastmail, Zoho, Proton, etc.) → follow **Path C**

Once I tell you, walk me through **only** the matching path — ignore the other two.

### Path A — Google Workspace / Gmail (claude.ai Connectors, default)

For Gmail, Drive, Calendar, and Granola, the **default install path is claude.ai Connectors** — first-party OAuth integrations managed by Anthropic that work from Claude desktop and Claude Code without any CLI install. This covers ~90% of integration needs and takes about 5 minutes total.

Walk me through:

1. Open the Claude desktop app (or https://claude.ai in the browser).
2. Go to **Settings → Connectors → Explore**.
3. Install these four connectors one by one, accepting the OAuth consent on each:
   - **Gmail** (read/send/search)
   - **Google Drive** (search/read/create files)
   - **Google Calendar** (list events, create events, respond to invites)
   - **Granola** (meeting transcripts + AI summaries)
4. For each connector, the browser opens a Google consent screen. **If the browser tab doesn't open automatically, copy the URL Claude shows and paste it into your browser manually** — this is the most common friction point, not a failure.
5. After installing, the connectors are available in any Claude Code session as `mcp__claude_ai_<connector>__*` tools — no further config needed.

**Verification:** in this Claude Code session, ask: *"List my 3 most recent Gmail messages."* and *"List my upcoming calendar events for today."* If both return real data, the connectors are wired.

### Path B — Microsoft 365 / Outlook

Email/calendar integration is **deferred to Phase 1** — there is no first-party Connector for Outlook yet and the MCP options are under evaluation. **Skip the Google Connectors above entirely** (they don't touch an Outlook mailbox). If you need Outlook data during Phase 0, export/import manually; we'll wire a proper integration in Phase 1. *(Granola is standalone — if you use it for meetings, install just that one Connector.)*

### Path C — Other / unknown stack

Skip email integration for Phase 0 and defer to Phase 1. Tell me what you use (Fastmail, Zoho, Proton, etc.) and we'll evaluate options later. Nothing here blocks the rest of setup.

Once verified (Google) or skipped (Microsoft / other) per your path, move to Step 2.5b.

---

### STEP 2.5b: ADVANCED — gws CLI (OPTIONAL, DEFER TO PHASE 0.5 — Google stack only)

> **Decide:** install gws CLI only if you need to **edit Google Sheets programmatically from Claude Code** (write formulas, batch-update ranges, manage spreadsheet schema). The Connectors above already cover Sheets *read*, plus all Gmail / Drive / Calendar operations. If your project doesn't write to Sheets from terminal scripts, skip this step entirely — you can always come back later in Phase 0.5.

For projects that need it, `gws` is the command-line tool that wraps the full Google Workspace API surface (Sheets writes included) into one binary. **On Windows** get the `windows-amd64` build, save it as `~/bin/gws.exe`, and add `export PATH="$HOME/bin:$PATH"` to `~/.bashrc` — the macOS instructions (`chmod +x ~/bin/gws`, editing a zsh profile) do not apply. Install adds ~1.5h (gcloud install + OAuth client setup + scope grants).

Walk me through the install step by step:

1. Check if gcloud CLI is installed: `gcloud --version`
   - If not, go to https://cloud.google.com/sdk/docs/install and guide me through install
   - After install: `gcloud auth login` (opens browser)

2. Download the gws binary from https://github.com/googleworkspace/cli/releases
   - Pick the binary for my OS/architecture
   - Place at `~/bin/gws` (create `~/bin/` if needed)
   - `chmod +x ~/bin/gws`
   - Add `~/bin` to my PATH if not already (check my shell profile)
   - Verify: `~/bin/gws --version`

3. OAuth setup: `~/bin/gws auth setup` — creates an OAuth client, enables needed Google APIs.

4. Authenticate: `~/bin/gws auth login` — browser OAuth consent, grant all scopes.

5. Test: `~/bin/gws drive files list --params '{"pageSize": 3}'` and `~/bin/gws calendar events list --params '{"calendarId": "primary", "maxResults": 3}'`.

6. Add `"Bash(~/bin/gws *)"` to the `allow` array in `~/.claude/settings.json` so Claude Code doesn't prompt every time.

7. Append a "Google Workspace Tools" section to the vault CLAUDE.md with these rules:
   - Primary tool: `gws` CLI at `~/bin/gws`
   - Syntax: `gws <service> <resource> [sub-resource] <method> --params <JSON>`
   - Two flags: `--params` = URL/query parameters, `--json` = request body
   - Important: the `!` character in Sheets ranges (e.g., `Sheet1!A1:Z10`) gets mangled by bash. When working with ranges, always use Python `subprocess.run()` to call gws — never raw bash.

If any step fails, help me troubleshoot before moving on.

Confirm Connectors are working (and optionally gws if installed). Move to Step 2.6.

---

## STEP 2.6: MEETING TRANSCRIPTS + /meeting-minutes SKILL

My meeting-transcription tool is **[TOOL]** *(the facilitator fills this in before the session: `Granola` (default) · `SpeakUp` · `Otter` · `Plaud` · `none / pasted transcript`)*. Install the `/meeting-minutes` skill against **that** source — do not assume Granola.

**Branch by tool:**
- **Granola** → In Step 2.5 I installed the **Granola Connector** via claude.ai. Verify it: ask *"List my 3 most recent Granola meetings."* If it returns real meetings it works; if not, re-install the connector and **if the browser tab didn't open during OAuth, copy the URL and paste it manually**. The skill reads via the `mcp__claude_ai_Granola__*` tools.
- **SpeakUp / Otter / Plaud / other** → If the tool publishes an MCP server or connector, install it now (SpeakUp has one — 2026-09-10) and verify by listing recent recordings. If it has none, the skill's input is **a transcript I paste or export to a file**; do not try to wire a Granola connector.
- **None** → The skill accepts a pasted transcript; skip any connector work.

**Prerequisite:** the tool's app is installed and I have at least one test recording. If not, do that first (see the Pre-Session Setup Instructions, Doc 1) and come back.

Walk me through:

1. **Verify the transcript source** per the branch above.

2. **Install the `/meeting-minutes` skill** — create `~/.claude/skills/meeting-minutes/SKILL.md` that:
   - Takes a meeting ID from [TOOL] (or prompts for latest), **or** a pasted / file transcript when there is no connector
   - Fetches transcript + AI summary via the tool's MCP/connector when one exists (Granola: `mcp__claude_ai_Granola__*`)
   - Generates a structured Meeting Minutes note in `03 REFERENCE/<area>/`. If `Templates/Meeting Minutes Template.md` does not exist yet, create it first (attendees, date, agenda, decisions, action items with owners, next steps) — Doc 02 only ships a Project Brief template
   - Extracts Decisions, Action Items, and Next Actions as wikilinks

3. **Verification:** Record a 30-second test meeting in [TOOL] (or paste any short transcript), then run `/meeting-minutes latest`. Claude should fetch/read the transcript, generate a minutes file, and show me the path.

Confirm the transcript source + `/meeting-minutes` skill are working. Move to Step 2.7.

---

### STEP 2.6b: ADVANCED — Granola MCP via CLI (OPTIONAL, DEFER TO PHASE 0.5)

> **Decide:** install the CLI-based Granola MCP only if you want vault-side automation that runs **outside a Claude Code session** (e.g., a cron job that processes new meetings every morning). The Connector above already covers in-session use — running `/meeting-minutes` live during or after a session. Skip this entirely unless you have a concrete automation need.

For projects that need it, Granola exposes a REST API that a local wrapper can call directly. If/when needed, walk me through:

1. Read the auth token from Granola's app-data folder. **On Windows that is `%APPDATA%\Granola\`
   (in Git Bash: `~/AppData/Roaming/Granola/`), NOT the macOS `~/Library/Application Support/` path.**
   Confirm the real filenames on disk first (`ls ~/AppData/Roaming/Granola/`) — do not assume the
   Mac layout carries over. Look for the nested `workos_tokens.access_token`.
2. Use the meeting cache in that same folder to list IDs/titles/dates (again: confirm the actual filename rather than assuming `cache-v6.json`).
3. Build a small Python helper at `~/bin/granola-fetch` that accepts `--meeting-id` or `--latest` and prints transcript + AI summary as JSON. API endpoints: `https://api.granola.ai/v1/get-document-transcript` and `https://api.granola.ai/v1/get-document-panels`.
4. Wire the helper into **Windows Task Scheduler** for unattended processing (launchd and cron are macOS/Linux only).

Confirm the CLI helper works (only if you chose to install it). Move to Step 2.7.

---

## STEP 2.7: INSTALL THE PHASE E CORE SKILLS

Beyond `/session-close` (Step 4) and `/meeting-minutes` (Step 2.6), five more skills are part of the Phase E required install set — these came out of repeated friction in Phase 0 sessions where members had to invent flows from scratch instead of using a battle-tested skill:

- **`/project-create`** — used in the demo flow ("always start with a plan"); creates Project / Program briefs via guided Q&A
- **`/inbox-clear`** — daily INBOX processing; classify each note, propose actions, execute after approval
- **`/retro`** — session retrospectives; routes to the right protocol per session mode
- **`/playground`** — interactive HTML playgrounds for exploring concepts visually
- **`/skill-create`** — build new skills from a guided conversation; used for the Week-1 weekly-review skill and called by `/retro` when it proposes codifying a recurring workflow.

### 2.7a — Install `/project-create` (curl one-liner)

The `/project-create` skill ships in the public AIAC starter-pack repo. Install via a single curl:

```bash
mkdir -p ~/.claude/skills/project-create/ && curl -fsSL https://raw.githubusercontent.com/wildbuffaloman/cc-starter-pack/main/project-create/SKILL.md -o ~/.claude/skills/project-create/SKILL.md
```

Verify:
```bash
head -5 ~/.claude/skills/project-create/SKILL.md
```

You should see the YAML frontmatter (`name: project-create`, `version: ...`, etc.).

### 2.7b — Install `/playground` (official Anthropic plugin)

`/playground` is part of the official Anthropic plugin marketplace — install it as a plugin, not a standalone skill:

```bash
claude plugin install playground@claude-plugins-official
```

Verify by running `/playground` in this session — Claude should describe the playground builder workflow.

### 2.7c — Install `/inbox-clear` (inline-paste)

The `/inbox-clear` skill repo is currently private (will go public in a future cohort). For now, create the file from this paste-ready content. Create `~/.claude/skills/inbox-clear/SKILL.md` with:

```markdown
---
name: inbox-clear
description: GTD-based inbox clearing — classify every note in 00 HUB/00 INBOX/, propose actions in a clearance manifest, execute after user approval.
user-invocable: true
argument-hint: "optional: single note path, or 'batch' to process all"
---

Clear `00 HUB/00 INBOX/` using a GTD-style classify-then-execute flow. Never delete or move silently — always propose first.

## Phase 1: Audit

For each note in `00 HUB/00 INBOX/`:

1. Read the note (full content if <500 chars, otherwise frontmatter + first/last sections).
2. Classify into one of:
   - **PROJECT** — actionable, multi-step → route to `01 PROJECTS/<Brief>/` or create a new project via `/project-create`
   - **REFERENCE** — durable knowledge → route to `03 REFERENCE/<area>/`
   - **READ_REVIEW** — needs deeper read before disposition → route to `03 REFERENCE/READ_REVIEW/`
   - **TASK** — single action → append to the Next Actions section of the relevant project brief, then archive the note. (If you have a task manager wired up, offer to add it there too — don't assume one.)
   - **DAILY_NOTE** — date-tagged daily content → route to `03 REFERENCE/DAILY NOTES/`
   - **ARCHIVE** — historical / completed → route to `04 ARCHIVES/`
   - **DELETE** — duplicate / accidental / no value → propose deletion
   - **KEEP_IN_INBOX** — needs human triage that AI can't make
3. For tasks: propose Eisenhower priority (Q1🔺 / Q2⏫ / Q3🔼 / Q4 none) based on urgency + leverage.

## Phase 2: Clearance Manifest

Write the manifest to `00 HUB/00 INBOX/_inbox-clear-manifest-YYYY-MM-DD.md`:

| Note | Classification | Proposed Action | Target Path | Priority |
|------|----------------|-----------------|-------------|----------|
| ... | PROJECT | Route to existing brief | 01 PROJECTS/Foo/Foo.md | — |

Present the manifest to the user. Wait for approval (or per-row overrides) before Phase 3.

## Phase 3: Execute

Only after user approves:
1. Move each note to its target.
2. Append TASK rows to the Next Actions section of the relevant project brief (and to a task manager only if the user has one set up).
3. Run `/project-create` for any new PROJECT rows.
4. Update the manifest with `✓` per executed row.
5. Surface anything that failed for re-decision.

## Rules

- Never bulk-move without approval.
- Tasks dedup against existing Apple Reminders before creating (search by title).
- Preserve original filename when moving — don't rename silently.
- If a note has wikilinks to others in INBOX, process the cluster together so cross-refs stay valid.
- Surface anything truly ambiguous as KEEP_IN_INBOX — better to leave it than mis-route.
```

Verify:
```bash
head -5 ~/.claude/skills/inbox-clear/SKILL.md
```

Should show the `name: inbox-clear` frontmatter.

### 2.7d — Install `/retro` (inline-paste)

The `/retro` skill repo is currently private. Create `~/.claude/skills/retro/SKILL.md` with this simplified version:

```markdown
---
name: retro
description: Run a retrospective on the current session or project — surface what worked, what didn't, and what to change so the next session is better.
user-invocable: true
argument-hint: "optional: scope — session, project, weekly, monthly"
---

Run a retrospective and update CLAUDE.md / project briefs with lessons learned.

## When to Run

- After a milestone or significant session
- When something broke or pivoted unexpectedly
- At a regular cadence (weekly = recommended, monthly = strategic)
- When the user says "retro", "let's reflect", "what did we learn"

## Steps

### 1 — Scope

Determine the scope:
- **session** (default) — just this session
- **project** — entire project arc (read its brief, look at Log section)
- **weekly** — last 7 days across all projects
- **monthly** — last 30 days strategic view

If no scope arg, ask: "Retro on this session, the current project, or a longer review?"

### 2 — Surface the Material

Pull the relevant material:
- For session: current conversation
- For project: the brief's Log + last 5 entries in Next Actions + Continuation Prompts history
- For weekly/monthly: scan all project briefs touched in that window

### 3 — The Three Questions

Ask the user (or work through these yourself, then confirm):

1. **What went well?** (2-3 items — celebrate wins, identify what to keep doing)
2. **What went wrong / friction?** (2-3 items — be specific, name the moment)
3. **What to change?** (1-2 concrete actions — these become CLAUDE.md updates or new rules)

### 4 — Codify

For each "change" item:
- If it's a behavior rule → update `~/.claude/CLAUDE.md` or the relevant project CLAUDE.md
- If it's a recurring workflow → propose codifying as a skill via `/skill-create` (don't auto-create — ask first)
- If it's a one-off lesson → append a line to `05 AI/CLAUDE CODE/resources/lessons.md`

### 5 — Log

Append a Retro entry to the relevant Log section (project brief Log, or lessons.md for session-scope retros):

| Date | Type | Description |
|------|------|-------------|
| YYYY-MM-DD | Retro | <one-line summary of the 3 questions> |

## Rules

- Never auto-edit CLAUDE.md without user approval — present the proposed diff first
- Keep it short — 3 wins, 3 frictions, 1-2 changes is the target. Don't write essays
- If the user says "no retro needed", respect that — don't push
- Lessons learned in retro should be **specific** ("when X happens, do Y"), not vague ("be more careful")
```

Verify:
```bash
head -5 ~/.claude/skills/retro/SKILL.md
```

Should show the `name: retro` frontmatter.

### 2.7e — Install `/skill-create` (curl one-liner)

`/skill-create` builds new skills from a guided conversation — you'll use it for your Week-1 weekly-review skill, and `/retro` calls it when it proposes codifying a recurring workflow. Install it from the public AIAC starter-pack with a single curl:

```bash
mkdir -p ~/.claude/skills/skill-create/ && curl -fsSL https://raw.githubusercontent.com/wildbuffaloman/cc-starter-pack/main/skill-create/SKILL.md -o ~/.claude/skills/skill-create/SKILL.md
```

Verify:
```bash
head -5 ~/.claude/skills/skill-create/SKILL.md
```

You should see `name: skill-create` in the frontmatter.

### 2.7f — Final Verification

Run all skills in a single check:

```bash
for skill in meeting-minutes project-create inbox-clear retro skill-create; do
  if [ -f ~/.claude/skills/$skill/SKILL.md ]; then
    echo "✓ $skill"
  else
    echo "✗ $skill MISSING"
  fi
done
```

For `/playground` (which is a plugin, not a standalone skill):
```bash
ls ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/playground 2>/dev/null && echo "✓ playground plugin" || echo "✗ playground plugin MISSING"
```

If anything is missing, fix it before moving to Step 3.

---

## STEP 3: LESSONS FOLDER

Create a lessons file in my vault at `05 AI/CLAUDE CODE/resources/lessons.md` for capturing lessons learned.

Seed it with this Windows rule as the first entry, so every future session re-reads it:

> **Always use forward slashes `/` in paths on this machine.** In Git Bash an unquoted backslash is
> silently stripped and the command fails with no visible error — and the symptom mimics an
> unrelated bug. Get Windows paths with `pwd -W`, never plain `pwd`.

Content:

```markdown
# Lessons Learned — Claude Code

> One line per lesson. Date + what happened + what to do differently.
> This file grows over time. Claude reads it to avoid repeating mistakes.

## Lessons

| Date | Lesson |
|------|--------|
| YYYY-MM-DD | Setup complete. First session. |
```

Use today's date in the first row. Confirm. Move to Step 4.

---

## STEP 4: SESSION-CLOSE SKILL

Create the file `~/.claude/skills/session-close/SKILL.md` with this content:

```markdown
---
name: session-close
description: Close the current session — update the project brief, log the work done, and leave a Continuation Prompt for the next session.
user-invocable: true
argument-hint: "optional: project name"
---

Close the current session by updating all relevant artifacts.

## When to Run

Run when:
- The user says "close session", "wrap up", "done for today", "save the state", or similar
- Context is running low (~50% used)
- An important task was completed
- The session is ending for any reason

## Step 1 — Identify the Project Brief

Every work session corresponds to a project. Find the matching brief:

1. Look in `01 PROJECTS/` (in the Obsidian vault) for a .md file that matches this session's work.
2. If no brief exists, create a new one in `00 HUB/00 INBOX/` using the Project Brief Template.
3. If the session was purely exploratory with no specific project, still create a minimal brief.

## Step 2 — Update the Project Brief

### Continuation Prompt (THE MOST IMPORTANT PART)

At the top of the `## Next Actions` section, add or REPLACE a `### Continuation Prompt` block. Only the most recent one is kept — it's overwritten each session.

Format:

### Continuation Prompt
> **Date:** YYYY-MM-DD
> **Context:** <1-2 sentences — which project, what we were doing>
>
> **Resume from:** <specific step, file, or location to continue from>
> **Key decisions:** <decisions made that affect the next steps>
> **Blockers/questions:** <anything unresolved>
> **Files touched:** <important files modified this session>

This block is designed to be copied and pasted into a new Claude Code session to resume the work without friction.

### Next Actions

Update the task list:
- Mark completed tasks as done
- Add new tasks discovered during the session

### Log

Add dated entries for the work performed:

| Date | Type | Description |
|------|------|-------------|
| YYYY-MM-DD | Task | Summary of the work |

Log rules:
- One item per row
- Label as "Task" or "Milestone"

### Waiting For

Only items that depend on OTHER people. Never put your own tasks here.

## Step 3 — Code Verification (only if code was written)

If the session involved writing or modifying code:

### 3a. Run and Verify
- Run the scripts that were created/modified
- Verify the output is correct
- If there are tests, run them

### 3b. Quality Review
Review the code for:
- **Security:** SQL injection? Hardcoded credentials?
- **Common errors:** Division by zero? Unclosed connections?
- **Readability:** Clear variable names? Comments where needed?

If you find problems, fix them (with the user's confirmation).

### 3c. Commit (if applicable)
If the work is in a git repo:
- Ask: "Do you want to commit the changes?"
- If yes, commit with a descriptive message
- Never push without explicit confirmation

## Step 4 — Lessons Learned

If the session produced reusable learnings:
- Add a line to `05 AI/CLAUDE CODE/resources/lessons.md` (in the vault)

## Step 5 — Report to the User

When finished, show:
- What was updated (and where)
- A summary of the Continuation Prompt
- Recommended next steps

## Step 6 — Retrospective Evaluation

Evaluate whether a quick retro is worthwhile. Indicators (1 point each):

1. **Milestone completed** — a milestone was reached
2. **Failure or pivot** — something broke or the plan changed
3. **New pattern** — a reusable workflow emerged
4. **Rule gap** — a hole in CLAUDE.md
5. **Repeated friction** — permission issues, repeated clarifications

Decision:
- **0-1 points:** No retro.
- **2-3 points:** Suggest a retro.
- **4+ points:** Strongly recommend one.

If the user agrees: **invoke the `/retro` skill** — it runs the retrospective (what went well / what went wrong / what to change) and updates CLAUDE.md / the briefs with the learnings. **Don't run the retro inline here** — `/retro` (installed in Step 2.7d) owns that flow; running it inline would duplicate the logic in two places.

## Rules

- The Continuation Prompt is MANDATORY on every close. No exceptions.
- Never invent data.
- If multiple projects were touched, update all their briefs.
- The Log is historical — only append, never modify previous entries.
- Respond in English.
```

After creating, verify the file exists by reading it. Then move to Step 5.

---

## STEP 5: PLAN MODE TRAINING

Explain Plan Mode to me. Show me:

1. **What it is:** A special mode where Claude Code creates a detailed plan BEFORE making any changes. No code gets written until the plan is approved.

2. **How to activate it:** Type `Shift+Tab` twice in the terminal input area. The prompt changes to show you're in plan mode.

3. **When to use it:**
   - Before any task that touches more than 1-2 files
   - Before building something new
   - When you're not sure of the approach
   - Rule of thumb: "If you're not sure, plan first."

4. **The workflow:**
   - Enter plan mode (Shift+Tab twice)
   - Describe what you want to build
   - Claude creates a structured plan (files to touch, approach, risks)
   - Review the plan, ask questions, adjust
   - Approve -> Claude executes the plan step by step

5. **Example:** Ask me to try it right now. Have me enter plan mode and type a simple prompt relevant to my project so I can see what the plan looks like. Then exit plan mode without executing (this is just practice).

Move to Step 6.

---

## STEP 6: KEY CONCEPTS CHEAT SHEET

Create a file in my vault at `00 HUB/00 INBOX/Claude Code Cheat Sheet.md`:

````markdown
# Claude Code — Cheat Sheet

## Windows notes (the four things you'll forget by next week)

| Thing | Remember |
|---|---|
| Which window | **Git Bash** for everything in this kit. PowerShell only for installing Claude Code. |
| Paths | Forward slashes `/` always. `pwd -W` gives the `C:/...` form. |
| Paste | Right-click, not Ctrl+V. |
| Something's broken | `claude doctor` — it checks the install and reports what's wrong. |

## Essential Commands

| Command | What it does |
|---------|-------------|
| `claude` | Start a session in current folder |
| `/exit` | End session |
| `/clear` | Clear context, start fresh |
| `/help` | See all commands |
| `/session-close` | Close session properly (updates project brief, logs work, creates continuation prompt) |
| `Ctrl+C` | Cancel current operation |
| `Escape` | Cancel current input |
| `Shift+Tab` (x2) | Enter/exit Plan Mode |
| `/project-create` | Create a Project/Program brief via guided Q&A (Phase E skill) |
| `/inbox-clear` | Classify and route 00 HUB/00 INBOX notes (Phase E skill) |
| `/meeting-minutes` | Turn a Granola recording into a structured note (Phase E skill) |
| `/retro` | Run a retrospective on a session, project, or week (Phase E skill) |
| `/playground` | Build an interactive HTML playground (Phase E plugin) |

## Plugin Commands

| Command | Plugin | What it does |
|---------|--------|-------------|
| `/ce:plan` | Compound Engineering | Create a structured plan with parallel research |
| `/ce:work` | Compound Engineering | Execute a plan step by step |
| `/brainstorm` | Superpowers | Explore ideas before building |
| `/systematic-debugging` | Superpowers | Debug systematically instead of guessing |

## Key Concepts

### CLAUDE.md = The Brain
Every folder can have a CLAUDE.md. Claude reads it automatically at session start. It tells Claude who you are, what the project is, and how to behave. **Update it after every correction.**

### Context Window = Your Working Memory
Claude has a limited context window (~200K tokens). As you work, it fills up.
- **At ~50%:** Save state and consider starting fresh (`/session-close` then `/clear`)
- **Never work past 70%** — quality degrades
- **Never accept "Resume from summary"** when Claude Code offers to compact — choose **"Resume full session"** or run `/session-close` first. The auto-summary is lossy (it silently drops detail).
- Starting a new session is cheap. Losing context is expensive.

### Plan First, Build Second
Unless it's a one-line change, always plan before building.
- Quick tasks: just describe what you want
- Medium tasks: use Plan Mode (Shift+Tab twice)
- Big tasks: use `/ce:plan` for full research + planning

### Two Workspaces — Vault (Knowledge) + Repo (Code)
The router (`~/.claude/CLAUDE.md`) makes Claude default to your vault no matter which folder you're in. Your notes live in the vault; your code lives in a git repo under `~/dev/`. Repos live OUTSIDE the vault — the mechanical test: if it has its own `.git/`, it belongs in `~/dev/`.
- **Notes / projects / thinking:** `cd [your vault path] && claude` (vault root)
- **Code / data:** `cd ~/dev/[your repo] && claude` (the repo folder)

**How it syncs:** the repo is git-managed — you `git push`/`git pull` to move code, and the GitHub remote works exactly as usual. Obsidian Sync handles only the `.md` knowledge (notes, briefs). The code itself (`.py`, `.sh`, etc.) does NOT sync via Obsidian — Obsidian Sync excludes those files by default. That's expected and fine: the `.md` travels over Obsidian Sync, the code travels over git. Two channels, two workspaces, linked by a pointer in your project brief.

### Session Close = Compound Learning
Always run `/session-close` before ending. It:
1. Updates your project brief with what you did
2. Creates a Continuation Prompt so the next session picks up exactly where you left off
3. Logs lessons learned
4. Reviews code quality
5. Suggests improvements to CLAUDE.md

**This is what makes Claude Code get smarter over time.** The more you close sessions properly, the better the instructions get.

### The Self-Improvement Loop
1. Work with Claude Code
2. When it makes a mistake, correct it
3. Claude updates CLAUDE.md with the new rule
4. Next session, the mistake doesn't happen again
5. After a few weeks, Claude genuinely gets better — not because the model changes, but because the instructions accumulate.

## Starter Prompts

> Tailor these to your own project — the case you set up in the Main Setup session.

**In the vault — morning check-in:**
```
Read my project brief in 01 PROJECTS/. What are my pending next actions?
What's the most important thing today? If there's a Continuation Prompt, summarize where I left off.
```

**In the repo — first automation:**
```
Read the CLAUDE.md, then look at the files and data in this repo.
For each one, tell me what it contains and how it maps to the project.
Then suggest the first automated report or tool we should build.
```
````

After creating the file, replace the two starter prompts above with 2-3 prompts tailored to my specific project (the case we set up in the Main Setup session), covering both the repo and the vault. Confirm the file was created. Move to Step 7.

---

## STEP 7: FIRST TEST

Let's do a quick test to make sure everything works. Run this simple exercise:

1. Check that the CLAUDE.md in this vault is readable — read it and tell me the first line.
2. Check that `~/.claude/CLAUDE.md` exists and has the correct vault path.
3. Check that `~/.claude/settings.json` has the permissions we set up earlier.
4. Check that all 6 standalone skills exist at `~/.claude/skills/<skill>/SKILL.md`: `meeting-minutes`, `project-create`, `inbox-clear`, `retro`, `skill-create` (the loop from Step 2.7f), plus `session-close` (created later, in Step 4).
5. Check that the `/playground` plugin is installed under `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/playground/`.
6. Verify the claude.ai Connectors respond — ask: "List my 3 most recent Gmail messages" and "List my upcoming calendar events for today." (Skip this check if you're on Microsoft 365 / other and deferred email integration to Phase 1.)
7. **Find out which Python command exists on this machine before using one.** On Windows the
   command is usually `python` or `py` — **bare `python3` normally does NOT exist, and typing it
   opens the Microsoft Store**, which looks like a crash. Run this first:

   ```bash
   for c in python py python3; do command -v $c >/dev/null 2>&1 && echo "FOUND: $c"; done
   ```

   - **If one is found:** create a simple script at `05 AI/CLAUDE CODE/workspace/hello.py` that
     prints a personalized greeting with the vault and repo paths, run it with the command that
     actually exists, and show me the output. Add that real command to my `permissions.allow`
     array (e.g. `Bash(python *)`), not the macOS `python3` form.
   - **If none is found: that is NOT a blocker, and we do NOT install Python now.** Nothing else in
     Phase 0 needs it. Note it as a Week-1 item and skip to the next check. Do not let this stop
     the session — it is the last verification step, not a prerequisite.

8. Validate that the settings file wasn't corrupted by the merges in Doc 02:

   ```bash
   jq . ~/.claude/settings.json > /dev/null && echo "settings.json is valid JSON"
   ```

9. Run `claude doctor` and show me the output.

If everything works, move to Step 8.

---

## STEP 8: SETUP COMPLETE

Give me a final summary of everything in this session:

**What was configured:**
1. `~/.claude/CLAUDE.md` — Global pointer to my vault (Claude always knows where my notes are)
2. Compound Engineering plugin — Plan -> Build workflow
3. Superpowers plugin — Debugging, brainstorming, code review
4. claude.ai Connectors — Gmail / Drive / Calendar / Granola (default integration path for Google Workspace; deferred to Phase 1 for Microsoft 365 / other; gws CLI deferred to Phase 0.5 if needed)
5. Phase E core skills (6) — `/session-close`, `/meeting-minutes`, `/project-create`, `/inbox-clear`, `/retro`, `/playground`
6. Lessons file — `05 AI/CLAUDE CODE/resources/lessons.md`
7. Plan Mode — Learned how to plan before building
8. Cheat Sheet — Quick reference at `00 HUB/00 INBOX/`

**The three most important habits:**
1. **Always `/session-close` before ending** — this is what makes you smarter over time
2. **Plan before building** — Shift+Tab twice, or `/ce:plan` for big tasks
3. **Correct Claude and let it update CLAUDE.md** — the self-improvement loop

End with: "Your Claude Code setup is complete. You have the same foundation as the most productive Claude Code users. The key now is to use it daily — even 10 minutes. Every session makes the next one better."
