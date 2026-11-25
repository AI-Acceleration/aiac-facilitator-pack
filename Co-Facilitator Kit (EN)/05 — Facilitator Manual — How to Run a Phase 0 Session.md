---
title: "Facilitator Manual — How to Run a Phase 0 Session"
created: 2026-07-14
category: reference
tags: [aiac, phase0, co-facilitator, facilitator-manual, english]
---

# Facilitator Manual — How to Run a Phase 0 Session

> **This is the centerpiece of the AIAC Phase 0 Co-Facilitator Kit (EN).** It is written for **you, the facilitator**, the person running the session, not for the participant. Read it start to finish before your first session, then keep it open beside you (second monitor, second tab, or printed) while you run one. It is your conductor's score.

## What this kit is

This kit packages the AI Acceleration Club's **Phase 0** onboarding so you can run it for anyone, **1-on-1**: a live, hands-on session where the participant walks out with a working second brain, a real private code repository, their first project, and a Claude Code setup that ties it all together.

**How long it really takes.** About **90 minutes is the best case**: a 1-on-1 session with prerequisites and pre-flight done, a facilitator who has run it before, and a participant comfortable with a terminal. **Budget 2–3 hours for your first runs.** Groups need more: plan at least 3 hours for a small group, with one helper for every two or three participants.

Two things make this kit different from the internal pipeline it derives from:

- **Docs-only.** There is no plugin to install and nothing to pre-generate. You drive the session; the participant gives Claude Code plain Markdown prompts. Long prompts are **loaded by file** ("Read the file <path> and follow its instructions"), never pasted, because terminals (especially on Windows) can silently truncate a long paste.
- **Live self-setup.** The participant does **not** fill out an intake form and does **not** receive files pre-built for their case. During the session Claude interviews them about their work, helps pick their first real project, and generates their project files on the spot. The participant also creates **their own private** GitHub repository under **their own** account. There is no central repo and no collaborator invite to chase.

> **Model-agnostic by design.** The method is plain Markdown files, Git and standard command-line tools. Claude Code is the recommended harness today, but the vault, the briefs and the habits carry over to another AI tool if you ever switch.

### The five core documents, plus variants

| Doc | For whom | When it's used |
|---|---|---|
| **01 — Pre-Session Setup Instructions** | Participant | Sent a week ahead. They install the prerequisites, run the **pre-flight** and send you its one-line result. |
| **02 — Main Setup Prompt** | Participant | Loaded by file into Claude Code in **Block 2**. Builds the vault structure, the private repo and, through a live interview, their first case. |
| **03 — Skills & Config Setup Prompt** | Participant | Loaded by file in **Block 3**. Installs the global router, plugins and core skills. |
| **04 — Next Steps Brief** | Participant | Handed over in **Block 5**. Their roadmap for the weeks after. |
| **05 — Facilitator Manual** (this doc) | You | Your run-of-show for the whole session. |

**Variants and companions:**

| File | What it is |
|---|---|
| **02W / 03W** | Windows editions of 02 and 03. Send these instead of 02/03 to Windows participants. |
| **02-S** | Opt-in sandbox setup, for participants who want Claude confined to their vault (Mac/Linux). |
| **06 — Pro Plan Survival Kit** | How to make Claude Pro last. Handed over with Doc 04. |
| **07 — Vocabulary** | Every term on one page. Sent with Doc 01. |
| **00W / 00E / 00V** | Facilitator-only diff tables (Windows edition, Spanish edition, Argentine voseo). Never send these to participants. |
| **`tools/aiac-status-check.sh`** (+ `.sh.txt` twin) | A read-only diagnostic the participant runs; they share only its safe-to-share block. |

Docs 02 and 03 **are** the prompts. Preserve them exactly: a changed command or JSON block breaks the participant's environment. **Never hand-adapt them for a participant without a step-by-step diff against the original** (see Pre-Session § 1).

### Terminal first, not the Desktop app

Run the setup in a **terminal**. Claude Desktop's Code tab reads the same `~/.claude` folder (the same skills, settings and `CLAUDE.md` files), so participants can work there afterward. But `claude plugin …` and `claude mcp add …` need the terminal, and the setup prompts assume one.

---

## PHILOSOPHY — read this before your first session

### What Phase 0 achieves

By the end of a Phase 0 session the participant has, and has *tested*, four things working together:

1. **A second brain:** an Obsidian vault with a PARA structure (Projects / Areas / Resources / Archives).
2. **A real repository:** a Git repo in `~/dev`, pushed to a **private** GitHub repository under their own account, for their first case.
3. **Their first case:** a real work problem, chosen live, with a project brief and a project `CLAUDE.md` that gives Claude the domain context.
4. **The router:** a global `~/.claude/CLAUDE.md` that points Claude to their vault from *any* directory, so they never have to explain where things live.

That's the whole deliverable: not a finished piece of work, but a *working system the participant can pick up again tomorrow.*

### "Kickoff, not finish"

This is the single most important principle for pacing the session, and the one new facilitators break most often.

**Block 4 kicks off the first exercise. It does not finish it.** The session's job is to get the participant *running* on their real problem with Claude Code, not to produce a polished deliverable live. Completing the first workflow is **Week-1 homework** (Doc 04).

Why hold back:

- Finishing live pushes the session even longer, exhausts the participant's attention and burns their Claude usage limit (on Pro this matters, see Doc 06).
- It robs them of the agency-building "I did this myself" moment in Week 1, which is the point of the whole program.

So when the first exercise starts producing output, your instinct will be to keep going until it's "done." Resist it. Produce a partial result, leave a clear breadcrumb for where to continue, and move on. Say it out loud so the participant isn't confused: *"We're not finishing this now. That's the homework, and it's the good part."*

### The peer-level demo

Your opening demo (Block 1) is not a product pitch. It's you showing your **own** working system doing something real, ideally something that mirrors the participant's world. The message is *"this is a normal way for a person like you to work,"* not *"look what the tool can do."* Keep it peer-level: real files, real corrections, a real close-out. Three or four minutes is plenty.

---

## PRE-SESSION

Do these in the week before the session.

### 1. Dry-run the material (before your first session, and after every kit update)

Run Docs 01 → 02 → 03 yourself, end to end, on a **clean machine or a fresh user account**, exactly as a participant would. Tools change; a prompt that worked last month can break on a new Claude Code release. The dry run is where you find out, not the participant.

**Never hand-adapt the prompts without a step-by-step diff.** If you tailor Doc 02 or 03 for a participant or a cohort, compare your version against the original **step by step** and make sure every step is still there, or carries an explicit "removed on purpose because …" line. In one cohort a hand-adapted setup prompt silently lost three steps (the project-brief template, the area map, and part of the brief structure). Nobody noticed in prep because the check compared document *names*, not their content. The session ran an hour over.

### 2. Pre-session checklist

- [ ] **Placeholders filled.** `[SET: your support channel]` appears in **Doc 01** and **Doc 04**. Replace it with the channel your participants use to reach you (a WhatsApp number, an email, a Slack channel). `[TOOL]` appears in **Doc 03 / 03W**: replace it with the participant's transcription tool (`Granola`, another tool, or `none / pasted transcript`). These are the only values you fill in; everything else the participant generates live.
- [ ] **Right editions picked.** Windows participant → **02W / 03W**. Spanish → the ES kit (tú); Argentine participant → apply the `00V` voseo table to the participant docs.
- [ ] **Screen sharing tested** on the call tool you'll use.
- [ ] **A dated cutoff set** for the pre-flight (see § 4).
- [ ] **Concrete project confirmed** (see § 6).
- [ ] **Recording decided:** optional, and only with consent (see § 8).

### 3. Send the material a week ahead

Send, together, about a week before the session:

- **Doc 01** — Pre-Session Setup Instructions
- **Doc 02 and Doc 03** (Windows: **02W and 03W**). The participant needs them on disk: the pre-flight moves them into the vault and practises loading one by file.
- **Doc 07** — Vocabulary
- Optionally `tools/aiac-status-check.sh.txt` (the `.txt` twin, because chat apps and email block `.sh`).

Tell them to save everything in **Downloads** without renaming it. Doc 01 is self-service: each prerequisite comes with a ready prompt for claude.ai, and a "Verify with Claude" check once Claude Code is installed.

### 4. The pre-flight gate, with a dated cutoff

Doc 01 ends with a **mandatory pre-flight**: a prompt the participant loads into Claude Code by file. It creates the vault (never in a cloud-synced folder), has them open it in Obsidian with **Open folder as vault**, checks that Obsidian opened that exact folder, moves the kit files into `00 HUB/00 INBOX/`, practises **Copy path** → load by file, checks every tool and their GitHub login, and ends with exactly one line:

```
PREFLIGHT: READY · ACCOUNT: personal
PREFLIGHT: MISSING jq, gh login · ACCOUNT: team
```

Ask for that line **and their GitHub username** by a **dated cutoff**, for example three working days before the session, and say the date explicitly when you send the docs. Use the same cutoff for **machine readiness**: an old, slow or locked-down machine discovered on the day costs the session.

- **Silence is "not done."** In the field, self-reports did not arrive on their own. Ask again 24 hours before the cutoff.
- **`MISSING …`** → fix it before the session, by message or in a short call.
- **No line by the cutoff** → book a prework call (§ 5) or reschedule. Don't start a session blind.
- **`ACCOUNT: team`** → a Team/Enterprise account. The organization's admin controls which claude.ai connectors exist and may distribute plugins. Doc 03 handles this (org plugins first, manual install only as a fallback), but know it before you start.

"They told me it's done" is a report, not a state. One session started blind; another was scheduled on "everything's installed" and then stalled twice, a week apart, on a missing PATH entry. The pre-flight line exists to replace the report with a check.

### 5. Prework with a helper

For non-technical participants, and for any group, **pair each participant with a helper before the session**: you in a 20–30 minute call, or a colleague or past participant acting as a mentor. Together they work through Doc 01 and the pre-flight. The installs and logins (the most fragile part) then happen calmly, not live, and the pre-flight line arrives because someone was there to send it.

### 6. A concrete, executable project (required)

The participant must arrive with **one concrete project**: an input they can bring (a file, an export), an output they want (a report, a summary, a cleaned table) and a reason it matters. "Learn AI" or "be more productive" is not a project. If what you get is vague, narrow it with them by message before the session. Block 2's interview goes from "what do you do?" to a usable case much faster when the candidate already exists.

**Sample data for the first exercise.** Ask them to bring a copy with names and amounts removed, a small slice, or made-up rows. Real business data comes later, once their company has approved using Claude with it, and it never goes into Git: the repo keeps `data/raw/` and `data/working/` out of history.

### 7. The status check (backup, not the gate)

`tools/aiac-status-check.sh` is a read-only script (it installs, changes and sends nothing) that reports how far a setup got. Use it when a pre-flight line is unclear or a participant is stuck between sessions.

- Tell them to run **the exact filename they received**, for example `bash ~/Downloads/aiac-status-check.sh.txt` (Claude can run it for them; Doc 01 has the prompt).
- Ask them to share **only** the block between `----- AIAC STATUS (safe to share) -----` and `----- END -----`. It holds check names, `DONE` / `NOT DONE` / `SKIPPED (optional)`, the OS and an overall verdict. **Never ask for the details above it**, and never ask for `--details` output: that part is for the participant's own eyes.
- The first `NOT DONE` is the resume point. `SKIPPED (optional)` is not homework. Before the session, a complete setup reads `VERDICT: PRE-SESSION - homework complete, ready for the session`; after it, `VERDICT: PHASE 0 SETUP COMPLETE - …`. The script reports only what it can see on the machine — for example "GitHub CLI credentials present", "Obsidian config found in this folder", "repo origin points at GitHub" — and its "NOT CHECKED HERE" list names what it cannot prove: that the `gh` credentials still work (`gh auth status`), that Obsidian has this exact folder open, and that the repo exists on GitHub, is Private and holds the commit. You verify those yourself: the folder on their shared screen, and the repo server-side (Gate 6).
- If the participant has already set up the 02-S sandbox, they run it in a plain terminal rather than inside Claude Code, where sandboxed commands can't see `~/.claude`.

### 8. Recording: optional, with consent

Recording the session is **optional**. If you'd like to record, ask the participant first and accept a no. Use whatever they're comfortable with: Granola, any other transcription tool, or no recording at all (you can write a short summary afterward, or they can paste a transcript into Claude later). If you do record, **say results out loud** (for example "router test: PASSED"), because the recording is only useful if the outcome is in it.

### 9. Participants who want the sandbox (02-S)

If the participant asks that Claude only touch the folder they give it, send **`02-S — Sandbox Setup`** as well, to run after the pre-flight and *before* Doc 02. Roughly one in ten asks for this unprompted, and it is the objection that otherwise blocks anyone on an employer machine. Before you agree to run it:

- Doc 02's **STEP 3 permissions block is skipped**: 02-S replaces it deliberately.
- Read 02-S's own statement of the boundary with the participant: the sandbox confines Claude's shell commands, but it is not an all-purpose wall (02-S lists what stays outside it). Don't promise more than it states.
- **Claude may not be able to run `git` or `gh`** under the sandbox. The participant runs those themselves, and the commit becomes their act of approval. Say this up front so it doesn't read as a failure mid-session. If `gh` fails, use the browser path in § 10 (no tokens).
- Mac and Linux only. Native Windows has no sandbox (WSL2 required).

### 10. GitHub access (this kit's version)

The participant creates **their own private** repo under **their own** GitHub account, live, in Block 2. There is no collaborator invite and no central repo. What you need before the session:

> **Claude Code running + a GitHub account + `gh` logged in (browser login).**

The pre-flight line already confirms this (`gh login` would be listed as missing). Before the **first push**, Doc 02 has Claude stop and confirm three things with the participant: the **owner** (their account), the visibility (**Private**) and the **list of files** about to be uploaded. Make sure that check happens; don't let anyone click through it.

**If `gh` can't be installed** (a locked-down company laptop): the participant creates the repository in the browser at `github.com/new`, with **their account as owner, visibility Private, and no README**, and Git signs in through **Git Credential Manager** (a browser window on the first push; it ships with Git for Windows). **No classic personal access tokens.** Gate 6 (Block 6) has a `gh`-free check for this path.

**Facilitator-owned repo (accepted variant).** If, for a reason of your own, the repo lives under your account, add the participant as a collaborator well ahead of time and confirm they **accepted** the invitation before the session. A pending invitation blocks everything, and invitations expire after 7 days.

---

## THE RUN-OF-SHOW

Nine blocks. The minutes are the **nominal** best case (~90 min). On a first run, expect each block to take longer, and budget 2–3 hours in total. Keep this bar visible while you run:

```
[ ] Block 0:   Start check: screen share + pre-flight line   5 min  ← before anything else
[ ] Block 0.5: Kickoff + consent to record                   5 min
[ ] Block 1:   Demo (peer-level, 3 key messages)           10 min
[ ] Block 1.5: Obsidian walkthrough                         5 min
[ ] Block 2:   Main Setup Prompt (Doc 02) + interview      30 min  ← capture the VAULT PATH
[ ] Block 3:   Skills & Config (Doc 03) + router test      10 min
[ ] Block 3.5: Status line + context protocol               5 min  ← load-bearing
[ ] Block 4:   First exercise: KICKOFF NOT FINISH          10 min
[ ] Block 5:   Orientation (cheat sheet + Docs 04 and 06) 5–10 min
[ ] Block 6:   Quality gates + Gate 6 (GitHub, server-side) 5 min
[ ] Block 7:   Close-out: fresh-window router test          5 min  ← the real end
```

For every block below: **what you do**, **what the participant does**, **teaching talking points**, **common errors + fixes**, **Expected** (what you should see before moving on) and **timing**. Each block also links a Google Slides deck as **optional support**: screen-share it if it helps, skip it if not. This manual's narrative is enough to run without slides.

---

### Block 0 — Start Check (5 min)

**What you do:**
- **Check screen sharing first.** Ask the participant to share their screen and confirm you can read their terminal. Everything after this depends on seeing it. Have them enlarge the terminal font if needed.
- **Read the pre-flight line.** You should already have it from before the session. Ask them to show it (it's the last line of the pre-flight in their Claude Code history) or read it to you. Also look at their status-check safe-to-share block if you asked for one. **You don't run the script live; you read results.**
- **`PREFLIGHT: READY`** → move on. **`PREFLIGHT: MISSING …`** → fix only the listed items now, with the same fixes as Doc 01. **No line at all** → have them run the pre-flight now (Doc 01, Step 10). It takes about 10 minutes and replaces guesswork.
- **Check their `cd` line.** The pre-flight gave them a `cd "<vault path>"` line. Make sure they have it, and **write the vault path down** yourself.

**What the participant does:** shares their screen, shows the pre-flight line, has the `cd` line ready.

**Common errors + fixes:**
- They can't find the line → open Claude Code and ask it to show the pre-flight summary from their last session, or rerun the pre-flight.
- The line says `ACCOUNT: team` and you didn't know → fine; Doc 03 follows the org path. Expect connectors and plugins to be admin-controlled.
- Obsidian shows a different vault than the pre-flight created → have them use **Open folder as vault** on the pre-flight's folder. Never "Create new vault".

**Expected:** screen visible, `PREFLIGHT: READY` (or the gaps just fixed), vault path written down.

**Timing:** 5 min. Don't skip it because "they told me it's ready." That's precisely the report the field data says not to trust.

### Block 0.5 — Kickoff + Consent to Record (5 min)

**What you do:**
- Welcome the participant warmly. This is their first hands-on experience; set a calm, "we've got time" tone.
- **Ask before recording.** If you'd like to record or transcribe, ask now and accept a no. If they agree, start the recording and confirm it is actually running.
- Confirm the first-exercise data is **sample data**, not confidential data.

**What the participant does:** answers the consent question; confirms what data they brought.

**Teaching talking points** *(the "why we're here" framing; support: [Deck 1 — Why AI Acceleration Club](https://docs.google.com/presentation/d/1mDNUeBUvxDDso_qUf_ZFeFzcIPBw8OnmT2rt5pnc0iU/edit), 5 slides)*:
- **The program arc.** "Today is Phase 0, the setup. After this you work on your own for a couple of weeks, then we reconvene. Phase 0 is the foundation everything else stands on."
- **What you'll walk out with.** "Today you'll have four things, all wired together: a second brain in Obsidian, a private code repository, your first actual project, and a setup that lets Claude find all of it automatically. And we'll *test* that it works before we finish."
- **Peer framing.** "This is just how I work every day. Nothing here is exotic. By the end you'll be doing it too."

**Common errors + fixes:**
- Recording tool has no permission → on a Mac, grant screen and microphone permission in System Settings and restart the tool. If it takes more than a minute, skip recording and take notes instead.

**Expected:** consent answered (recording running, or not recording by choice); sample data confirmed.

**Timing:** 5 min. Don't let a green setup tempt you to linger. Move to the demo.

---

### Block 1 — Demo (10 min)

**What you do:**
- Show **your own** system doing something real, ideally mirroring the participant's world. Pick from what you actually use:
  - *Finance / family business* → a report compiled from source data, with the commentary written for you.
  - *Time-pressed exec / GM* → your morning command center: one command that reconstructs the day across your calendars, tasks and follow-ups into a prioritized plan.
  - *Operations / supply chain* → messy export → clean structured data → an actual decision (a reorder point, a forecast), with Claude catching the data-quality edge cases.
  - *Creative / brand* → building a small interactive tool live from a one-line idea.
  - *Knowledge worker / unsure* → the second-brain + correction loop: make a correction and watch it get written into a `CLAUDE.md` so it sticks.
- Keep it to 3–4 minutes of doing, then recap. Use non-confidential material on screen.

**What the participant does:** watches. That's it; this is your block.

**Teaching talking points** *(the 3 key messages + the mental-model map; support: [Deck 2 — Demo Framing](https://docs.google.com/presentation/d/1WitxhK3dvXZiYm_a9Hm0zE6JpQwJTxqCJgBligQmVqM/edit), 3 slides, only if the demo is slow to start)*:

Open with the **30-second mental-model map**. The #1 friction for newcomers is not vocabulary; it's not seeing how the pieces fit (Doc 07 has the vocabulary). Say:

> "There are three pieces, each with one job. **Claude Code** is the AI in your terminal: it *acts*. Your **vault** in Obsidian is where your knowledge lives: it *stores*. **Git and GitHub** are the history and the private backup for your code. You work *with* Claude, *inside* your vault; Git protects the code part."

Then, during the demo, land the **three key messages**:

1. **"Claude reads the `CLAUDE.md` automatically. It already knows the project context."** (The `CLAUDE.md` is the system's brain.)
2. **"Every correction I make gets saved, so it gets smarter over time."** (Corrections compound into permanent behavior.)
3. **"I close every session with `/session-close`. That's what preserves the state."** (Discipline is what makes the system reliable.)

Close with a **"what you just saw"** recap: name the three things Claude did on its own (read the context, produced the artifact and, if you showed it, saved a correction).

**Common errors + fixes:**
- The demo lands flat / feels like a tool showcase → pull it back to *their* world and *your* real files. The emotional beat is "a person like me works this way."
- You start improvising and it runs long → pick one tight thing you can do in 3 minutes. Longer is worse.

**Expected:** the participant can repeat the three-piece map in their own words.

**Timing:** 10 min including the recap.

---

### Block 1.5 — Obsidian Walkthrough (5 min)

**What you do:**
- Before running any setup, walk the participant through Obsidian so the PARA structure that's about to be generated makes visual sense. (Doing this *first* prevents the mid-setup hand-holding that used to slow Block 2 down.)
- Have them open Obsidian on **the vault the pre-flight created**. It contains only `00 HUB/00 INBOX/` with their kit files. That's expected.

**What the participant does** (in Obsidian):
1. **Left panel, the file tree.** "Each folder here becomes a section of your second brain."
2. **Create a new note (Cmd/Ctrl+N).** "Notes are just Markdown files: plain text with formatting."
3. **Wikilinks: type `[[Test]]` in the note.** "This is how notes connect, like Wikipedia's internal links."
4. **Graph view (left sidebar icon).** "This is where your knowledge becomes a network."
5. **Command palette (Cmd/Ctrl+P).** "Anything Obsidian can do, you can find here."
6. **Right-click a file → Copy path.** "This is how you'll hand long prompts to Claude all day today." (They practised it in the pre-flight.)

Then have them delete the test note.

**Teaching talking points** *(support: [Deck 3 — Obsidian + PARA + GTD](https://docs.google.com/presentation/d/1SrDJ-RjJgkr1XrAFkg2BqFGddu-YQP9ijlW4QJIqp_s/edit), 8 slides)*:
- **Your second brain, yours forever.** "It's plain-text Markdown on your own disk, with no vendor lock-in. If Obsidian disappeared tomorrow, your notes are still just files you own."
- **PARA.** "Four buckets: **Projects** (active, with an end), **Areas** (ongoing responsibilities), **Resources** (reference material), **Archives** (done). Everything has a home."
- **GTD in one line.** "Capture → Clarify → Organize → Engage. Get it out of your head, decide what it is, put it where it belongs, then do it."
- **Where Claude Code fits.** "The `CLAUDE.md` files are the *rules*; the folders are the *data*. Claude reads the rules and works over the data."

Then point at the nearly empty vault and set the cliffhanger:

> "Right now this is almost empty. In the next half hour, Claude Code is going to fill it: the PARA structure, a project brief for your case, an area map, and your AI Acceleration Club journey brief. Watch the left panel populate as we go."

**Common errors + fixes:**
- Obsidian opens a different, older vault → vault switcher (bottom left) → **Open folder as vault** → the pre-flight's folder. Never "Create new vault": a second vault is the most common way the setup and Obsidian end up looking at different folders.
- Graph view is empty and confusing → that's expected on an empty vault; it fills in as notes and links appear.

**Expected:** Obsidian shows the pre-flight's vault (`00 HUB/00 INBOX/` with the kit files), and the participant can do Copy path.

**Timing:** 5 min. This is orientation, not a tutorial. Keep it moving.

---

### Block 2 — Main Setup Prompt + Live Interview (30 min)

This is the biggest block and the heart of the setup. **Doc 02** (Windows: **02W**) is the prompt.

**What you do:**
- Have the participant open a terminal (Windows: Git Bash), run the `cd "<vault path>"` line from the pre-flight, then `claude`. If Claude asks whether they trust the folder, the answer is **Yes**.
- Have them **load Doc 02 by file**: in Obsidian, right-click the Main Setup Prompt in `00 HUB/00 INBOX/` → **Copy path** (full system path), then in Claude Code: `Read the file <path> and follow its instructions, starting at "FOR CLAUDE — START HERE".` On Windows, the path's `\` become `/`.
- Watch for errors, explain what each step does as it happens, and **confirm the vault path** Claude uses matches the one you wrote down in Block 0.
- During the **live interview**, help the participant articulate their work problem and steer toward a first case that's a good fit (see below).
- **Before the first push**, make sure Claude stops and confirms the owner, **Private** visibility and the staged file list with the participant.

**What the participant does:**
1. Enters the vault and starts Claude Code.
2. Loads Doc 02 by file and works through it interactively, answering the interview.
3. Confirms owner, Private and the file list before the first push.

**The live interview, the key difference in this kit.** Where the internal pipeline pre-builds the participant's project files from a form, Doc 02 has Claude run the interview *live*. Claude will:
- Ask what they do and their role.
- Ask about the concrete project they brought (Doc 01 asked for one, with an input and an output).
- Ask 1–2 light calibration questions (terminal / Git comfort) to set pacing.
- Recommend the **best first case** and, on the participant's confirmation, generate their project `CLAUDE.md` and project brief on the spot.

Your job during the interview is to be the human co-pilot: help them pick the case with **sample data they can actually bring** and a **first prototype that fits in 10–15 minutes** of Week-1 work. If they're torn between two problems, steer toward the more concrete, more painful one. Claude derives the repo name from the chosen case; you don't fill anything in.

**What the Main Setup Prompt builds:**
- PARA folder structure + the `05 AI/CLAUDE CODE/` workspace.
- The vault `CLAUDE.md` (behavioral rules) and the global router `~/.claude/CLAUDE.md`.
- `~/.claude/settings.json`: narrow permissions, **merged** into whatever was there (never overwritten, never blanket approvals), the sound hook and the context monitor (status bar + auto-compact guardrails).
- Git configured, GitHub connected, and a repo in `~/dev`, pushed to a **private** GitHub repository under the participant's own account.
- The repo `CLAUDE.md` (case-specific domain context, from the interview), with a bridge back to the vault brief.
- The project-brief template, the project brief in `01 PROJECTS/`, the Area MOC and the AI Acceleration Club journey brief.
- The first commit and the AIAC Cheat Sheet.

**Teaching talking points** *(support: [Deck 5 — Main Setup Prompt](https://docs.google.com/presentation/d/1lHx2L90fW5wFSPXCiMoyrSVelWxrH5lJCKQA_tegAqE/edit), 3 slides · [Deck 4 — Git + GitHub 101](https://docs.google.com/presentation/d/17r_FGB_Pff8gPagk1bSIf6svrXrPMsZfO0ElP1ND1Aw/edit), 11 slides; do not run them all)*:
- **What the prompt does.** "This one prompt builds your whole environment in a single interactive run. You're watching a system assemble itself."
- **The `CLAUDE.md` chain.** "There are three levels, from general to specific: the **global router** (`~/.claude/CLAUDE.md`) points to your vault from anywhere; the **vault `CLAUDE.md`** holds your general working rules; the **repo `CLAUDE.md`** holds the domain knowledge for this one project. Claude reads the most specific one that applies."
- **Two briefs, not one.** "You get two briefs: a **case brief** for the project itself, and a **journey brief** that tracks your progress through the program."
- **Git/GitHub in plain terms** (say these as the Git steps run):
  - "Version control is a time machine for your files."
  - "A repository is just a folder that remembers its whole history."
  - "A commit is a save-state you can always come back to."
  - "GitHub is the remote copy: your private backup and, later, how you collaborate."
  - "`.gitignore` is the list of things we *never* save to history: secrets, big or confidential data files."
- **Private by default.** "Your repo is private: only you can see it. We check that before the first push, every time."
- **Knowledge vs. code.** "Notice the repo lives in `~/dev`, **not** inside the vault. Knowledge in the vault, code in `~/dev`. Keep them separate."

**Common errors + fixes:**
- **The paste got cut off** → they pasted instead of loading by file. Stop, and load Doc 02 by path.
- **Vault path with spaces** → a raw `cd` fails on an unquoted space. The pre-flight's `cd "…"` line is quoted; use it as-is. Launching `claude` from inside the vault avoids the problem entirely.
- **Git not installed** → Doc 01 Step 2 (`xcode-select --install` on Mac, Git for Windows on Windows).
- **Repo creation fails** → `gh auth status` must show a logged-in user; if not, the participant runs `gh auth login --hostname github.com --git-protocol https --web` in a **second terminal window** (Claude can't answer its prompts). No `gh` at all → the browser path from Pre-Session § 10.
- **Claude Code login expired** → `/login`, or exit and run `claude` again.
- **Blocked country** → the VPN must stay **on** for the whole session; network steps fail the moment it drops.
- **Claude blocks a settings edit and mentions the mode** → press **Shift+Tab** to switch to the default mode, make the edit, then switch back.
- **The interview stalls, participant can't name a problem** → fall back to the project they brought per Doc 01; if still stuck, pick a concrete, recurring task from their described role and name it yourself. A decent first case beats a perfect one.

**Expected:** PARA folders visible in Obsidian; the repo at `~/dev/<repo-name>` (not inside the vault); the first push done after the owner/Private/files check; the vault path confirmed.

**Timing:** 30 min nominal, often 45+ on a first run. **Confirm the vault path before you leave this block.**

---

### Block 3 — Skills & Config + Router Test (10 min)

**Doc 03** (Windows: **03W**) is the prompt. The participant should still be in Claude Code, in the vault.

**What you do:**
- Have them **load Doc 03 by file**, the same way as Doc 02 (Copy path → `Read the file <path> and follow its instructions, starting at "FOR CLAUDE — START HERE".`).
- When Doc 03 asks which **email stack** they use (Google / Microsoft / other), help them answer; the prompt follows the matching path live.
- On a **team account** (`ACCOUNT: team`), expect the org path: org-distributed plugins first, manual install only as a fallback.
- After it runs, run the **mandatory outside-the-vault routing test** (below). Do not skip it.

**What the participant does:** loads Doc 03 and works through it. It installs the router-first global `CLAUDE.md`, the plugins, the starter skills (including `/session-close`), `/meeting-minutes` for their transcription tool, and walks them through Plan Mode.

**The mandatory router test** (a real gate, caught too late in past sessions):
1. Type `/exit` to leave Claude Code.
2. `cd ~`
3. Run `claude`
4. Ask: **"What files are in my vault INBOX?"**

If Claude reads the vault INBOX **without being given the path**, the router works. If it says "I don't know where your vault is," the global `CLAUDE.md` was generated as a *profile* doc instead of a *router*. Fix it now (re-run Doc 03's router step), then re-run the test until it passes.

**Teaching talking points** *(support: [Deck 6 — Skills + Plugins](https://docs.google.com/presentation/d/1v-JuXDTYHxv2mPoApT5lk9Qp0G5THCio6EusolrT8uo/edit), 3 slides)*:
- **What a skill is.** "A skill is a reusable procedure you invoke with `/name`. Think of it as a saved playbook Claude already knows how to run."
- **The plugins.** "Plugins bundle many of these playbooks. You got a starter set today."
- **Skills and plugins load in new sessions only.** "Anything you install now shows up the *next* time you start Claude Code, not in this session. That's why we check in a fresh window."
- **Why the router matters** (say it out loud): "`~/.claude/CLAUDE.md` is why Claude always knows where your vault is, from any folder on your computer."
- **The sound hook.** "The sound means you can walk away and come back when Claude's done."
- **The one habit.** "`/session-close` is the single most important habit. It's what makes the system smarter over time."

**Common errors + fixes:**
- **Router generated as a profile doc** (the classic bug) → the outside-the-vault test catches it; re-run the router step, then re-test.
- **A plugin or skill "isn't there"** → check in a **new** session; then `claude plugin list` in the terminal (text view) shows what's installed and enabled. On team accounts, a manually installed copy with the same name as an org plugin can shadow it; prefer the org copy.
- **Plan Mode confusion** → have them press **Shift+Tab** until the bottom bar says *plan*, type a real prompt, review the plan, then exit. It's just practice.
- **Email-stack branch picked wrong** → re-run that step with the correct stack.

**Expected:** the router test passes from `cd ~`; `claude plugin list` shows compound-engineering, superpowers and playground; `/session-close` appears when they type `/` in a **new** session.

**Timing:** 10 min nominal, including the routing test.

---

### Block 3.5 — Status Line + Context Protocol (5 min)

This is short but **load-bearing.** The context window is one of the two most important mental models (the other is `CLAUDE.md`). Members who understand it from day one avoid the "my session got worse the longer I worked" failure mode.

**What you do, part 1: confirm the status bar (2 min).**
- Doc 02 (STEP 3.5) already installed the context monitor: a status bar with the context %, a warning at 50% and an auto-compact guardrail at 75%. Have the participant look at the bottom of their terminal for the context percentage. If they don't see it, open a **new** session: status-line changes show up after a restart.
- **Don't run `/statusline-setup`.** It replaces the custom bar from Doc 02 and removes the 50% warning. If the bar is still missing after a restart, re-run Doc 02's STEP 3.5 only (Windows: 02W has a documented fallback).

**What you do, part 2: teach the protocol (3 min).** Say these thresholds out loud; they *are* the protocol:

- **Compact ideally before 50%.** Best quality. Plan sessions to hit natural break points before 50%, then `/session-close` + `/clear`.
- **After 50%, context rot starts.** Not catastrophic, but Claude starts forgetting earlier context and making inconsistent references. The bar turns yellow and warns once.
- **Compact certainly before 70%.** Past 70%, quality falls off a cliff. Auto-compaction is set to 75%, with a stop just before it so you decide, not the tool.

The two ways to compact at the threshold:
- **A. `/session-close` + `/clear`**: cleanest. State is saved to the brief's Continuation Prompt, then reset. Best for task transitions.
- **B. `/compact`**: Claude Code's built-in in-session compaction; keeps you going mid-task. Lossy by design, so A is the better habit.

**Teaching talking points** *(support: [Deck 7 — Context Window + Status Line](https://docs.google.com/presentation/d/1DwvVL_MVjRjfnDWT5RhNC4YER6UffsKzI1MQFroSpiM/edit), 4 slides)*. Say the "why" out loud:

> "If you take one protocol from today, it's this one. Watching the context bar is the single habit that separates members who improve over time from members whose sessions get worse the longer they work. You *can* work past 50%, but now you're on notice. Past 70% is where you pay for it."

**What the participant does:** finds the context % in the bar and repeats the three thresholds back to you.

**Common errors + fixes:**
- Bar not visible → new session first; then check `jq --version` (the bar depends on `jq`); then re-run Doc 02 STEP 3.5.
- On Windows the bar misbehaves → follow 02W's fallback and stop after 3 minutes; the bar is display only, the auto-compact guardrail works without it.

**Expected:** a context % visible in the bar (or the 02W fallback applied); the participant can state 50% / 70% / 75%.

**Timing:** 5 min. Don't cut this to save time; it's the highest-leverage 5 minutes in the session.

---

### Block 4 — First Exercise: KICKOFF NOT FINISH (10 min)

Re-read the **"Kickoff, not finish"** principle above before you run this. This block gets the participant *running* on their real problem. It does **not** complete a deliverable.

**What you do:**
- Have them open a **new** terminal window and start a session **in the repo** (not the vault): `cd ~/dev/<repo-name>` and then `claude`.
- Choose the path by whether they brought sample data.

  **Path A — they brought sample data.** They give Claude a prompt like:

  > "Copy the file <path to my sample file> into data/raw/ in this repo. Don't modify the original. Then read the CLAUDE.md and tell me, for each file in data/raw/, what's in it, how many rows, what period it covers and how it maps to the project in the CLAUDE.md. Leave a note at the end saying where we continue in Week 1."

  Cap it at 2–3 files. The point is to show the flow, not ingest everything.

  **Path B — no data yet.**

  > "Read the CLAUDE.md. Create a data inventory template at docs/data-inventory.md that I can fill in over the next week."

**What the participant does:** runs the kickoff prompt and sees Claude working on *their* real problem.

**Teaching talking points** *(support: [Deck 8 — First Exercise + Homework](https://docs.google.com/presentation/d/1xz_91oO93udpz6ss_grLQh1CwljvFxPfY56sHtEbeVs/edit), 4 slides)*:
- **Path A vs Path B.** "If you brought data, we point Claude at it. If not, we build the checklist for gathering it. Either way you leave with momentum."
- **Kickoff not finish.** Say it explicitly: *"We're not finishing this right now. You'll keep going this week on your own; that's the whole point. My job today is to get you into the flow where you KNOW you can pick this up tomorrow."*
- **Raw data stays out of Git.** "`data/raw/` and `data/working/` are in `.gitignore`. Only processed results get committed."
- **When stuck, come back.** "This week, if you get stuck, that's normal and there's no shame in it. Reach out and we'll unstick you." (This sets up the support model in Doc 04.)

**Common errors + fixes:**
- **You're tempted to finish it** → don't. Partial output + a breadcrumb is the *correct* outcome.
- **They brought confidential data** → don't load it. Switch to Path B, or make a scrubbed copy together first.
- **No data and no clear inventory** → the `docs/data-inventory.md` template is the deliverable; it's a perfectly good Week-1 starting point.

**Expected:** one real prompt run in the repo session; a partial result or the inventory template; a breadcrumb for Week 1.

**Timing:** 10 min. Stop even if the output is partial, *especially* if it's partial.

---

### Block 5 — Orientation (5–10 min)

**What you do:**
- Walk through the **AIAC Cheat Sheet** (created by Doc 02, in `00 HUB/00 INBOX/`).
- Hand over **Doc 04 — Next Steps Brief** (their homework and roadmap) and **Doc 06 — Pro Plan Survival Kit** (how to make Pro last). Have them save both into `00 HUB/00 INBOX/` now.

**What the participant does:** follows along on the cheat sheet; saves Docs 04 and 06 into the vault.

**Teaching talking points.** Emphasize five things:
1. **Two workspaces:** vault (notes, thinking) vs. repo (code, data).
2. **The self-improvement loop:** correct Claude → the correction gets written into a `CLAUDE.md` → it doesn't repeat the mistake.
3. **Always `/session-close`** before ending. It's the compound-learning mechanism.
4. **Plan before building:** Shift+Tab to Plan Mode for medium tasks; a planning skill for big ones.
5. **Homework** (Doc 04 Part 0 first): close Phase 0 properly, open Claude Code daily (even 10 minutes), collect the data for the case, and complete the first workflow.

**Doc 04 note:** Doc 04 has a section the participant fills in themselves (Part 3, "your project's next workflows"), because their case was chosen live. Encourage them to jot 2–3 next steps for their project while it's fresh.

**Common errors + fixes:**
- Participant treats homework as optional → frame it as the part where the value actually lands; the session was just the setup.

**Expected:** Docs 04 and 06 saved in `00 HUB/00 INBOX/`, next to the Cheat Sheet.

**Timing:** 5–10 min.

---

### Block 6 — Quality Gates + Gate 6 (5 min)

Run through this with the participant. **Every gate needs evidence you can see on their screen**, not their word. If a gate fails, fix it **now**, before the close-out.

```
QUALITY GATES — Phase 0
━━━━━━━━━━━━━━━━━━━━━━━

- [ ] Obsidian shows the vault Claude built (PARA folders + vault CLAUDE.md),
      and .obsidian/ is inside that same folder
- [ ] Claude Code running: claude --version works
- [ ] ~/.claude/CLAUDE.md is a ROUTER (first section = "Default Workspace"
      with an imperative load instruction, NOT a profile-first doc)
- [ ] Outside-the-vault routing test PASSED (cd ~ && claude, then
      "list my vault INBOX" works without giving the path)
- [ ] ~/.claude/settings.json: narrow permissions merged in (no blanket
      git/cat/interpreter approvals), sound hook, context monitor
- [ ] Status line shows a context % (or the 02W fallback applied)
- [ ] Participant can state the context thresholds (50% / 70% / 75%)
- [ ] Gate 6 PASSED: private GitHub repo verified on the server (below)
- [ ] Project brief in the vault, linked to the repo
- [ ] /session-close shows up in a NEW session
- [ ] claude plugin list shows the plugins Doc 03 installed
      (compound-engineering, superpowers, playground)
- [ ] Ran at least one real prompt on their case (Path A or Path B)
- [ ] Can articulate what they'll work on this week
```

#### Gate 6 — GitHub, verified server-side (run before they leave)

GitHub is the step that keeps passing in the room and failing on disk. `git remote -v` only proves that a URL was typed: it prints happily for a repository that doesn't exist. The participant's word and a recording summary can't prove it either. **Ask GitHub directly.**

**With `gh` (default).** In the repo session, the participant gives Claude this prompt (replace owner and repo):

> "Run `gh repo view <owner>/<repo> --json nameWithOwner,visibility`, then `gh api repos/<owner>/<repo>/commits --jq '.[0].sha[0:7]'` and `git log --oneline -1`. Show me the raw output of all three."

**PASS** = `nameWithOwner` is their repo, `visibility` is **`PRIVATE`**, and the commit SHA from GitHub matches the first 7 characters of the local `git log` line. A `gh` error, an empty answer, a public repo or a mismatched SHA is a **FAIL**, whatever the terminal showed ten minutes ago.

**Without `gh`.** The participant asks Claude to run `git remote get-url --push --all origin`, `git ls-remote origin HEAD` and `git rev-parse --short HEAD`. The first must print exactly one line, `https://github.com/<owner>/<repo>.git` (or the same address in GitHub's SSH form), with their owner and repo name; the second asks GitHub for its latest commit, and its first 7 characters must match the third. Then they open the repo page in the browser while sharing their screen, and you confirm the **Private** label next to the repository name.

**Facilitator-owned variant.** Membership alone proves nothing about privacy or the push, so you run all three checks on your own machine:

1. `gh api repos/<owner>/<repo>/collaborators --jq '.[].login'` — their username is listed. A **pending invitation is a FAIL**: have them accept it now at `https://github.com/<owner>/<repo>/invitations`.
2. `gh repo view <owner>/<repo> --json nameWithOwner,visibility` — `visibility` is **`PRIVATE`**.
3. `gh api repos/<owner>/<repo>/commits --jq '.[0].sha[0:7]'` — matches the first 7 characters of the `git log --oneline -1` line that the participant's Claude shows on their screen.

PASS = all three. Any one missing is a **FAIL**.

**If the repo turns out public**, fix it before anything else: on GitHub, Settings → General → Danger Zone → Change visibility → Private. Then check what was pushed.

**Expected:** every box ticked with evidence; Gate 6 PASS stated out loud.

**Timing:** usually 3–5 min if everything held.

---

### Block 7 — Close-Out: Fresh-Window Router Test (5 min) — THE REAL END

The session does **not** end at the quality gates. It ends when the participant has **two Claude Code windows open**: one still working in the repo, and one freshly opened from *outside* the vault that proves the whole stack (router + project brief) works end to end. Without this last test, they walk away "set up but untested"; with it, they walk away "ready to work."

**What you do, part 1: leave the current window open.**
- The participant should **not** close the Claude Code session running in the repo. No `/exit`, no closing the tab.

**What you do, part 2: open a second window and test.**
- Have the participant:
  1. Open a **new** terminal window or tab (separate from the repo window).
  2. `cd ~` (home directory, **not** the vault).
  3. `claude` (a fresh session).
  4. Type this exact prompt:

     > **"Open my case project brief and give me a 3-bullet summary of what I'm building."**

**Expected behavior:**
- Claude reads `~/.claude/CLAUDE.md` at session start.
- It finds the vault path from the router block.
- It opens the project brief in `01 PROJECTS/…`.
- It returns a 3-bullet summary **without** the participant giving any path.

**If it passes:** they now have proof the whole stack works end to end. Say:

> "That's it. We just tested the full loop. Tomorrow you open Claude Code, tell it to pick up where you left off, and it does."

**If it fails — common modes + fixes:**
- "I don't know where your vault is" → the router block wasn't generated correctly; re-apply Doc 03's router step and re-run the test.
- Finds the vault but not the brief → the brief path is wrong or the file wasn't created; check `01 PROJECTS/` for the actual filename and correct the path in the vault `CLAUDE.md`.
- Reads everything but the summary is garbled → likely a minor frontmatter issue; rare. Note it as a Week-1 fix and move on.

**Do not declare the session complete until this test passes.** This is the true end, not Block 6.

**Say the result out loud and write it down**, *"router test: PASSED"* or *"router test: FAILED because X"*, in your own notes. If you recorded, the recording is only useful when the outcome is spoken. One session ended on *"I need to know whether it worked"*, and afterward nobody could confirm it had.

**Expected:** "router test: PASSED" said and written down.

**Timing:** 5 min (+ buffer if you troubleshoot).

---

## POST-SESSION

Do these the same day, while it's fresh.

### Exit checklist: every line needs evidence

Don't report the session as complete with an empty line. For each item, write the evidence next to it (a path, a command's output, a SHA) or "skipped because …":

```
EXIT CHECKLIST — <participant>, <date>
- [ ] Pre-flight line received before the session ............ <the line>
- [ ] Vault path ............................................. <path>
- [ ] Repo + Gate 6 .......................................... <owner/repo, PRIVATE, SHA>
- [ ] Router test (Block 7) .................................. PASSED / FAILED because …
- [ ] Case project brief ..................................... <path under 01 PROJECTS/>
- [ ] Docs 04 + 06 saved in the vault INBOX .................. yes / no
- [ ] Recording .............................................. consented + where it is / not recorded
- [ ] Open issues + who fixes them ........................... <list, or "none">
- [ ] Follow-up date ......................................... <date>
```

Fill the checklist from **what happened**, never from the plan. A plan line copied as a result ("plugins synced") is exactly how a past close reported something that never happened.

### Then

- **Confirm the homework is clear.** In your follow-up note, restate Doc 04's first steps: Part 0 (close Phase 0: check what the setup left, close the setup session manually), open Claude Code daily (even 10 min), collect the case data, complete the first workflow. Remind them the first exercise was a *kickoff*; finishing it this week is the point.
- **Lead with any failed gate.** If Gate 6 or the router test failed, the follow-up opens with that, with the fix and a date.
- **How to follow up.** Check back after 1–2 weeks of self-directed work. If they go quiet, a single low-pressure nudge ("how's the case going — anything stuck?") is usually enough. Keep the support model no-shame: getting stuck is expected, not a failure.
- **Recording.** If you recorded (with consent), the transcript is your source for follow-up notes. Store it as carefully as anything else with the participant's work in it, and delete it when you no longer need it.
- **Improve the kit.** Note any friction (a step that failed, a confusing prompt) and fix the kit, or report it upstream, before the next session.

---

## FACILITATOR'S OWN ONE-TIME SETUP

Do this **once**, before you run your first session. It's not per-participant.

1. **Fill the placeholders.** `[SET: your support channel]` in **Docs 01 and 04**; `[TOOL]` in **Docs 03 / 03W** (per participant, if transcription tools differ). These are the only values you fill in.
2. **Dry-run the kit** on a clean machine or fresh user account (Pre-Session § 1).
3. **Keep your copy current.** Work from the published kit and check for an updated release before each session; prompts change as Claude Code changes.
4. **Remember the format.** This kit is written for **one-on-one** sessions. This manual's narrative is your script; **the decks linked in each block are optional support**. Screen-share them if they help, skip them if not.

---

## OUT OF SCOPE (for now)

Noted so you know they're deliberate omissions, not gaps:

- **Group / cohort format.** This kit is written 1-on-1. It can run with small groups, but budget at least 3 hours, give every two or three participants a helper who runs Gate 6 with them before they leave, and fill in a shared gate grid live. With a dozen people, one facilitator can't also be the scribe.
- **Installable plugin / skill pack for facilitators.** There's no facilitator plugin in this kit by design. It's docs-only, so it works for anyone with no shared infrastructure.
