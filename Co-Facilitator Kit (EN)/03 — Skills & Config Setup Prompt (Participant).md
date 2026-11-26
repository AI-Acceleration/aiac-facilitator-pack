---
title: "Skills & Config Setup Prompt (Participant) — AI Acceleration Club Phase 0"
created: 2026-07-14
category: reference
tags: [aiac, phase0, co-facilitator-kit, participant, skills, config, setup-prompt]
---

**Supports:** Block 3 of your live Phase 0 session. You give this file to Claude Code by its path when your facilitator tells you to; you do not paste it.

# Phase 0 — Skills & Config Setup Prompt

This is the **second** prompt of the session. It comes right after the Main Setup Prompt (Doc 2) has finished scaffolding your vault and your project. Claude reads it and walks you through each step, one at a time.

## How to give this file to Claude

Same as Doc 02 — **don't paste it**, hand Claude the file:

1. Save this file on your computer and copy its full path (macOS: Finder → right-click, hold
   **Option** → **Copy "…" as Pathname** · Windows: File Explorer → **Shift**+right-click → **Copy as
   path** · Linux: **Copy path**, or drag the file into the terminal).
2. In the terminal, `cd` into your vault and start `claude` (or keep the session from Doc 02 open).
3. Type this, paste the path where it says `<path>`, and press Enter:

   ```
   Read the file <path> and follow its instructions, starting at "FOR CLAUDE — START HERE".
   ```

4. If you have to stop midway: start Claude again in your vault and type
   `Read the file <path> and continue from Step N.`

> **Two things to know before you start**
>
> - **Plugins, skills and connectors you install during a session load in the *next* session.** They
>   won't show up in the session that installed them. Step 8 ends with a check in a fresh session.
> - **Work or school Claude account (Team / Enterprise)?** Your organization's admin controls which
>   connectors you can turn on, and may already give you plugins. Step 2 checks this first.

---

## FOR CLAUDE — START HERE

---

We just finished setting up my vault and project. Now I need you to install the essential plugins, install the starter skills, and configure a few more things. Walk me through each step one at a time. Confirm each step before moving on.

**Rules for this part:** don't add blanket or lasting permissions for me; merge into existing settings files, never overwrite them; anything that needs a login with questions on screen goes in a **second terminal window** (give me the exact line and wait); when a step says **STOP**, really stop and wait for me.

---

## STEP 1: VERIFY GLOBAL CLAUDE.md ROUTER + ROUTING TEST

My global router `~/.claude/CLAUDE.md` was already created in the **Main Setup prompt (Doc 2)** — the "Global Router" step. Here we just confirm it's in place and run the live routing test before installing skills.

Verify the file — read back its first 20 lines and confirm that:
1. The first section is `## Default Workspace` (the imperative router), NOT `## Who I Am`.
2. The vault path is resolved (no literal placeholder remains in the file).

Then the **outside-the-vault routing test** — critical for catching the "profile-only, not router" failure mode. I do this myself, in a **second terminal window**, so this session stays open:

```
cd ~/dev
claude
```

(If Claude Code asks whether to trust `~/dev`, answer **Yes** — that is where my repos live.) Once it starts, I ask: *"What files are in my vault INBOX?"* If Claude reads my vault's `00 HUB/00 INBOX/` without me giving it the path, the router is working. If it says "I don't know where your vault is", the router was generated as a profile doc, not a router — go back to the Main Setup prompt's "Global Router" step and recreate `~/.claude/CLAUDE.md` with the `## Default Workspace` block at the TOP. Either way, I type `/exit` in that second window and come back here to tell you the result.

Confirm both checks pass. Move to Step 2.

---

## STEP 2: INSTALL PLUGINS

**First, check what kind of Claude account I'm on:**

```bash
grep -o '"organizationType": *"[^"]*"' ~/.claude.json
claude plugin list
```

- **No output, or a personal type** → personal account (Pro or Max). Install the plugins below.
- **A team or enterprise type** → an organization account. Its admin controls connectors and may
  already distribute plugins to me. **Use the organization's plugins first:** if `claude plugin list`
  already shows a plugin below, don't install it again. Install manually **only as a fallback** for one
  the organization doesn't provide — and tell me, because a manually installed copy with the same name
  can shadow (hide) the organization's copy. (Whether that shadowing happens the same way on Windows is
  unverified; check with `claude plugin list` either way.)

Then install what's missing:

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

If `superpowers` or `playground` says the marketplace is unknown, first run `claude plugin marketplace add anthropics/claude-plugins-official`.

If none of those work, tell me what error you got and we'll troubleshoot.

**After installing, briefly explain what each plugin does:**

- **Compound Engineering:** Gives you `/ce:plan` (create a structured plan with research) and `/ce:work` (execute a plan step by step). The core idea: "unless it's a one-line change, there's always a plan first."
- **Superpowers:** Gives you structured workflows for debugging (`/systematic-debugging`), brainstorming (`/brainstorm`), code review (`/requesting-code-review`), and test-driven development (`/test-driven-development`).

Confirm both are installed: run `claude plugin list` (the plain text view) and show me the lines for both. They become usable in my **next** session — don't expect `/ce:plan` to work in this one. Move to Step 2.5.

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
2. Go to **Connectors** (under **Settings** or **Customize**, depending on the app version) → **Browse / Explore**. On a work account, if a connector isn't listed, your organization's admin has to enable it first — note it and move on.
3. Install these connectors one by one, accepting the OAuth consent on each:
   - **Gmail** (read/send/search)
   - **Google Drive** (search/read/create files)
   - **Google Calendar** (list events, create events, respond to invites)
   - **Granola** (meeting transcripts + AI summaries) — only if Granola is my meeting tool (Step 2.6)
4. For each connector, the browser opens a Google consent screen. **If the browser tab doesn't open automatically, copy the URL Claude shows and paste it into your browser manually** — this is the most common friction point, not a failure.
5. After installing, the connectors are available in Claude Code sessions as `mcp__claude_ai_<connector>__*` tools — no further config needed. Like plugins, they show up reliably in a **new** session.

**Verification:** at the end of this setup, in a fresh session (Step 8), ask: *"List my 3 most recent Gmail messages."* and *"List my upcoming calendar events for today."* If both return real data, the connectors are wired.

### Path B — Microsoft 365 / Outlook

There is a first-party **Microsoft 365 connector** (Outlook mail and calendar, OneDrive, SharePoint, Teams). **Skip the Google connectors above** — they don't touch an Outlook mailbox.

1. In the Claude desktop app or https://claude.ai, go to **Connectors** → find **Microsoft 365** → **Connect**, and sign in with my Microsoft account.
2. **Work or school Microsoft account:** a Microsoft administrator must approve the connector once for the whole organization, and on a Claude Team/Enterprise plan the Claude organization owner must enable it too. If the sign-in says approval is needed, **don't fight it today** — note "ask IT to approve the Microsoft 365 connector" as a Week-1 item and move on. A personal Microsoft account needs no admin.
3. By default the connector is **read-only** (it can read mail, events and files, not send or change them). That is the right setting for Phase 0.
4. Verification (in a fresh session, Step 8): *"List my 3 most recent emails"* and *"What's on my calendar today?"*

*(Granola is standalone — if you use it for meetings, install just that one connector.)*

### Path C — Other / unknown stack

Skip email integration for Phase 0 and defer to Phase 1. Tell me what you use (Fastmail, Zoho, Proton, etc.) and we'll evaluate options later. Nothing here blocks the rest of setup.

Once connected (Google or Microsoft) or skipped (other) per your path, move to Step 2.5b.

---

### STEP 2.5b: GOOGLE WORKSPACE CLI (`gws`) — NOT TODAY

Skip this today. The connectors above already cover reading Gmail, Drive, Calendar and Sheets. The `gws` command-line tool is only for **writing to Google Sheets from scripts**, and setting it up takes over an hour (a Google Cloud OAuth client, API enablement, scope grants).

If a later project needs it, set it up in a dedicated session with your facilitator, and keep it narrow:

- **Log in with only the scopes the project needs** (for example Sheets only), not "grant all scopes".
- **No blanket permission rule** for it (no `gws` wildcard in `allow`). Approve its commands one at a time, or add an exact rule for one specific read-only command you run often.

Tell me "noted" and move to Step 2.6.

---

## STEP 2.6: MEETING TRANSCRIPTS + /meeting-minutes SKILL

My meeting-transcription tool is **[TOOL]** *(FACILITATOR PLACEHOLDER — replace before sending: `Granola` · another transcription tool by name · `none / pasted transcript`. If it still says [TOOL], ask me which one I use)*. Install the `/meeting-minutes` skill against **that** source — do not assume Granola. **Recording is optional:** a pasted transcript works just as well. Whatever the tool, **everyone in a meeting is asked before it is recorded.**

**Branch by tool:**
- **Granola** → In Step 2.5 I installed the **Granola Connector** via claude.ai. Verify it: ask *"List my 3 most recent Granola meetings."* If it returns real meetings it works; if not, re-install the connector and **if the browser tab didn't open during OAuth, copy the URL and paste it manually**. The skill reads via the `mcp__claude_ai_Granola__*` tools.
- **Any other tool (SpeakUp, Otter, Plaud…)** → If the tool publishes an MCP server or connector, install it now and verify by listing recent recordings. If it has none, the skill's input is **a transcript I paste or export to a file**; do not try to wire a Granola connector.
- **None** → The skill accepts a pasted transcript; skip any connector work.

**For the test, no real meeting is needed:** a 30-second recording of just me, or a short made-up transcript pasted in, is enough. Don't use a real client or internal meeting for the first test.

Walk me through:

1. **Verify the transcript source** per the branch above.

2. **Install the `/meeting-minutes` skill** — create `~/.claude/skills/meeting-minutes/SKILL.md` that:
   - Takes a meeting ID from [TOOL] (or prompts for latest), **or** a pasted / file transcript when there is no connector
   - Fetches transcript + AI summary via the tool's MCP/connector when one exists (Granola: `mcp__claude_ai_Granola__*`)
   - Generates a structured Meeting Minutes note in `03 REFERENCE/<area>/`. If `Templates/Meeting Minutes Template.md` does not exist yet, create it first (attendees, date, agenda, decisions, action items with owners, next steps) — Doc 02 only ships a Project Brief template
   - Extracts Decisions, Action Items, and Next Actions as wikilinks

3. **Verification:** the skill becomes available in my **next** session. In the fresh session at the end (Step 8), record a 30-second test in [TOOL] (or paste a short made-up transcript), then run `/meeting-minutes latest` (or `/meeting-minutes` and paste). Claude should read the transcript, generate a minutes file, and show me the path.

Confirm the transcript source and that `~/.claude/skills/meeting-minutes/SKILL.md` exists. Move to Step 2.7.

---

## STEP 2.7: INSTALL THE STARTER SKILLS (ONE PACK, ONE CLONE)

The starter skills come from one public, reviewed pack: **`AI-Acceleration/cc-starter-pack`, pinned at tag `v1.0.1`** (a fixed version, so every fresh install gets exactly the same files; a skill you already have under the same name is skipped and keeps your version — see 2.7a). It contains nine skills, including the ones this kit uses every day:

- **`/session-close`** — close a session: update the brief, log the work, leave a Continuation Prompt (Step 4)
- **`/project-create`** — create a Project / Program brief through guided Q&A
- **`/inbox-clear`** — process `00 HUB/00 INBOX/`: classify each note, propose moves, act only after approval
- **`/retro`** — session retrospectives that turn friction into CLAUDE.md rules
- **`/skill-create`** — build new skills from a guided conversation (your Week-1 weekly-review skill)
- plus `/load-context`, `/deep-research`, `/deep-planning`, `/fermi-decomposition`

Several skills ship helper files next to their `SKILL.md`, so install the whole pack, not single files. Nothing
of the pack is kept afterwards: it is cloned into a brand-new temporary folder that is deleted at the end, so a
leftover or changed copy can never be installed by mistake.

### 2.7a — Clone the pack at `v1.0.1` into a temporary folder and run its installer

Every install — the first one, a retry after an error, or a reinstall later (Doc 04) — uses this same block.
Run it as **one** command:

```bash
PACK_TMP="$(mktemp -d)" || PACK_TMP=""
if [ -z "$PACK_TMP" ]; then
  echo "STOP: could not create a temporary folder - not installed"
elif ! git clone --depth 1 --branch v1.0.1 https://github.com/AI-Acceleration/cc-starter-pack.git "$PACK_TMP/cc-starter-pack"; then
  echo "STOP: the clone failed - not installed"
elif [ "$(cd "$PACK_TMP/cc-starter-pack" && git rev-parse HEAD)" != "a85d906849f1fbd200d0e44a59b0d1f24b450135" ]; then
  echo "STOP: v1.0.1 is not the reviewed commit a85d906 - not installed"
else
  (cd "$PACK_TMP/cc-starter-pack" && bash ./install.sh)
fi
[ -n "$PACK_TMP" ] && rm -rf "$PACK_TMP"
```

It runs the installer **only** when all three hold: the temporary folder was created, the clone succeeded,
and the clone sits on commit `a85d906849f1fbd200d0e44a59b0d1f24b450135` — the exact `v1.0.1` this kit was reviewed against (a tag can be moved
after the fact, a commit can't). The parentheses keep this session's working folder on the vault. Any
`STOP:` line means nothing was installed: show me, and don't work around it. **Never run `install.sh` from
any other folder** — not from a copy left by an earlier attempt, and not from an older `~/.aiac/cc-starter-pack`
from a previous version of this kit (you can delete that one).

- `install.sh` copies each skill folder into `~/.claude/skills/<skill>/`. It **skips** any skill I already have with the same name and prints `SKIP: …` for it — that skill keeps my version, not the `v1.0.1` one. If you see a `SKIP`, show me the list and ask me what to do — never overwrite one of my skills without my OK (`bash ./install.sh force` overwrites).
- A `NOTE: …` line means a skill from an older version of the pack (`context`, `permissions` or `extract`) is still in `~/.claude/skills/`. The installer leaves it in place: show me the line and delete that folder only if I say so (`/context` and `/permissions` are also built-in Claude Code commands, so the old copies are not needed).
- It ends with "Restart Claude Code": **don't restart now.** The skills load in my next session.

### 2.7b — Install `/playground` (official Anthropic plugin)

`/playground` is a plugin from the official marketplace, not a standalone skill (on an organization account, check `claude plugin list` first, as in Step 2):

```bash
claude plugin install playground@claude-plugins-official
```

### 2.7c — Verify

```bash
for skill in session-close project-create inbox-clear retro skill-create meeting-minutes; do
  if [ -f ~/.claude/skills/$skill/SKILL.md ]; then echo "OK      $skill"; else echo "MISSING $skill"; fi
done
claude plugin list
```

All six skills must print `OK`, and `claude plugin list` must list `playground`, `compound-engineering` and `superpowers`. If anything is missing, **STOP** and fix it (show me the error) before Step 3. Using them is tested in a fresh session at the end (Step 8).

---

## STEP 3: LESSONS FOLDER

Create a lessons file in my vault at `05 AI/CLAUDE CODE/resources/lessons.md` for capturing lessons learned.

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

## STEP 4: SESSION-CLOSE — THE ONE HABIT THAT MATTERS

`/session-close` was installed with the starter pack in Step 2.7 (`~/.claude/skills/session-close/`). Don't write your own version — read the installed `SKILL.md` and explain to me in plain words, in five lines or fewer:

1. **When** to run it: whenever I'm done for now, when context passes ~50%, or after finishing something important.
2. **What it updates:** the project brief's Next Actions and Log, and a **Continuation Prompt** at the top of Next Actions — the block the next session reads to pick up exactly where I left off.
3. **What it never does on its own:** push code, delete notes, or invent data. If it offers to commit, it asks first.
4. **Retro:** when a session had a milestone, a failure or repeated friction, it suggests running `/retro`.

Then move to Step 5.

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
| `Shift+Tab` | Switch mode (default → accept edits → Plan Mode); press until the bottom bar shows the one you want |
| `/project-create` | Create a Project/Program brief via guided Q&A (starter pack) |
| `/inbox-clear` | Classify and route 00 HUB/00 INBOX notes (starter pack) |
| `/meeting-minutes` | Turn a meeting transcript into a structured note |
| `/retro` | Run a retrospective on a session, project, or week (starter pack) |
| `/skill-create` | Build a new skill from a guided conversation (starter pack) |
| `/playground` | Build an interactive HTML playground (plugin) |

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
3. Check the permissions **without opening or printing any settings file** (they can hold keys). Run
   this check — it reads `~/.claude/settings.json` and `settings.local.json`, the same two files in this
   vault's `.claude/` folder (where "Yes, and don't ask again" answers are saved) and in my repo's, and it
   prints only counts and categories, never a rule's text. Put my repo name in place of `<repo-name>`:

   ```bash
   python3 - <<'PY'
   import json, os, re
   KIT = ["Bash(git status)", "Bash(git status --short)", "Bash(git diff)", "Bash(git log --oneline)",
          "Bash(git remote -v)", "Bash(ls *)", "Bash(wc *)"]
   NEED = ["cat", "head", "tail", "grep", "diff", "sed", "sort", "git show", "git -C", "git -c",
           "git add", "git commit", "git push", "gh repo create"]
   INTERP = re.compile(r"^(Bash|PowerShell)\((\S*/)?(python[0-9.]*|py|node|npx|pip[0-9.]*|uv|uvx|ruby|perl|deno|bun|bash|sh|zsh|fish|pwsh|powershell|osascript|sudo|env|xargs|eval)(\.exe)?([ :)]|$)")
   def kind(r):  # the same categories as the status check; the rule text is never printed
       if r in KIT:
           return None
       if "(" not in r:
           ok = (re.match(r"mcp__.+__.+", r) and "*" not in r) or r == "WebSearch"
           return None if ok else "bare tool"
       if INTERP.search(r):
           return "interpreter or shell"
       if re.match(r"(Read|Edit|Write|MultiEdit|NotebookEdit|Glob|Grep)\(", r):
           return "file-tool rule"
       if "*" in r:
           if re.match(r"Bash\(git[ :]", r):
               return "git wildcard"
           return "command wildcard" if re.match(r"(Bash|PowerShell)\(", r) else "other wildcard"
       return None
   def has_extra_dirs(x):
       if isinstance(x, dict):
           return "additionalDirectories" in x or any(has_extra_dirs(v) for v in x.values())
       return isinstance(x, list) and any(has_extra_dirs(v) for v in x)
   FILES = [("global", "~/.claude/settings.json"), ("global local", "~/.claude/settings.local.json"),
            ("vault", ".claude/settings.json"), ("vault local", ".claude/settings.local.json"),
            ("repo", "~/dev/<repo-name>/.claude/settings.json"),
            ("repo local", "~/dev/<repo-name>/.claude/settings.local.json")]
   found, ask, extra = {}, [], False
   for label, path in FILES:
       path = os.path.expanduser(path)
       if not os.path.isfile(path):
           continue
       try:
           s = json.load(open(path, encoding="utf-8"))
       except ValueError:
           found[label + ": not valid JSON"] = 1
           continue
       p = s.get("permissions") if isinstance(s, dict) else None
       p = p if isinstance(p, dict) else {}
       allow = p.get("allow") if isinstance(p.get("allow"), list) else []
       for k in [kind(r) for r in allow if isinstance(r, str)]:
           if k:
               found[label + ": " + k] = found.get(label + ": " + k, 0) + 1
       if p.get("defaultMode") not in (None, "default", "manual", "plan"):
           found[label + ": defaultMode"] = 1
       extra = extra or has_extra_dirs(s)
       if label == "global" and isinstance(p.get("ask"), list):
           ask = [r for r in p["ask"] if isinstance(r, str)]
   print("broad allow rules:", "%d (%s)" % (sum(found.values()), ", ".join(
       "%s x%d" % (k, n) for k, n in sorted(found.items()))) if found else "none")
   print("missing ask rules:", ", ".join(c for c in NEED if "Bash(%s *)" % c not in ask) or "none")
   print("additionalDirectories:", "present" if extra else "absent")
   PY
   ```

   PASS = `broad allow rules: none`, `missing ask rules: none`, `additionalDirectories: absent`. If
   anything else shows up, show me the line and ask me before changing anything — it names the file and
   the kind of rule; I open that file myself in a text editor and remove the rule, or tell you to re-run
   the Doc 02 merge for a missing one.
4. Check that the six skills exist at `~/.claude/skills/<skill>/SKILL.md` (the loop from Step 2.7c): `session-close`, `project-create`, `inbox-clear`, `retro`, `skill-create`, `meeting-minutes`.
5. Check with `claude plugin list` that `playground`, `compound-engineering` and `superpowers` are installed.
6. Create a simple Python script at `05 AI/CLAUDE CODE/workspace/hello.py` that prints a personalized greeting with the vault and repo paths.
7. Run it once (I approve the prompt — **do not** add Python to `permissions.allow`) and show me the output. If `python3` isn't found, something is off: Python is a prerequisite (Doc 01's pre-flight checks it, and Doc 02 Step 3 used it). Tell me, give me the Doc 01 install line to run in a **second terminal window**, and check again. If it can't be installed today, note it for my facilitator and go on with the rest of this list.

If everything works, move to Step 8.

---

## STEP 8: SETUP COMPLETE

Give me a final summary of everything in this session:

**What was configured:**
1. `~/.claude/CLAUDE.md` — Global pointer to my vault (Claude always knows where my notes are)
2. Compound Engineering plugin — Plan -> Build workflow
3. Superpowers plugin — Debugging, brainstorming, code review
4. Connectors — Google (Gmail / Drive / Calendar) or Microsoft 365, plus Granola if that's my meeting tool (other stacks deferred; `gws` CLI not today)
5. Starter skills from `AI-Acceleration/cc-starter-pack` `v1.0.1` (`/session-close`, `/project-create`, `/inbox-clear`, `/retro`, `/skill-create` and more), plus `/meeting-minutes` and the `/playground` plugin
6. Lessons file — `05 AI/CLAUDE CODE/resources/lessons.md`
7. Plan Mode — Learned how to plan before building
8. Cheat Sheet — Quick reference at `00 HUB/00 INBOX/`

**The three most important habits:**
1. **Always `/session-close` before ending** — this is what makes you smarter over time
2. **Plan before building** — Shift+Tab until Plan Mode, or `/ce:plan` for big tasks
3. **Correct Claude and let it update CLAUDE.md** — the self-improvement loop

**Last check — in a fresh session.** Everything installed today loads in a new session, so tell me to: type `/exit`, start `claude` again in my vault, and then:

- type `/` and confirm I see `/session-close`, `/project-create`, `/inbox-clear`, `/retro`, `/meeting-minutes`;
- ask *"Which plugins are active?"* (or run `/plugin`) and confirm Compound Engineering, Superpowers and Playground;
- if I set up connectors: run the Gmail/Calendar (or Microsoft 365) verification questions from Step 2.5, and the `/meeting-minutes` test from Step 2.6.

If something is missing there, restart Claude Code once more; if it's still missing, note it for my facilitator.

End with: "Your Claude Code setup is complete. You have the same foundation as the most productive Claude Code users. The key now is to use it daily — even 10 minutes. Every session makes the next one better."
