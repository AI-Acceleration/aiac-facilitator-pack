---
title: "Facilitator Manual — How to Run a Phase 0 Session"
created: 2026-07-14
category: reference
status: draft
tags: [aiac, phase0, co-facilitator, facilitator-manual, english, mangan]
related: ["[[AIAC Phase 0 Co-Facilitator Kit (EN) — Design Spec]]", "[[AI Acceleration Club - Phase 0 Playbook]]"]
---

# Facilitator Manual — How to Run a Phase 0 Session

> **This is the centerpiece of the AIAC Phase 0 Co-Facilitator Kit (EN).** It is written for **you, the facilitator** — the person running the session — not for the participant. Read it start to finish before your first session, then keep it open beside you (second monitor, second tab, or printed) while you run one. It is your conductor's score.

## What this kit is

This kit packages the AI Acceleration Club's **Phase 0** onboarding so you can run it for anyone, in **English**, **1-on-1**, in about **90 minutes** — a live, hands-on session where the participant walks out with a working second brain, a real code repository, their first project, and a Claude Code setup that ties it all together.

Two things make this kit different from the internal Spanish pipeline it derives from:

- **Docs-only.** There is no plugin to install and nothing to pre-generate. You drive the session manually; the participant pastes plain Markdown prompts into Claude Code. Everything you both need is the five documents in this folder.
- **Live self-setup.** The participant does **not** fill out an intake form beforehand and does **not** receive files pre-built for their case. Instead, during the session, Claude interviews them about their work, helps pick their first real project, and generates their project files on the spot. The participant also creates **their own** GitHub repository under **their own** account — there is no central repo and no collaborator invite to chase.

### The five documents

| Doc | For whom | When it's used |
|---|---|---|
| **01 — Pre-Session Setup Instructions** | Participant | Sent a few days before the session; they install and verify prerequisites, and come with 1–3 work problems. |
| **02 — Main Setup Prompt** | Participant | Pasted into Claude Code during **Block 2**. Builds the vault, the repo, and — via a live interview — their first case. |
| **03 — Skills & Config Setup Prompt** | Participant | Pasted into Claude Code during **Block 3**. Installs the global router, plugins, and core skills. |
| **04 — Next Steps Brief** | Participant | Handed over as homework at **Block 5**; it's their roadmap for the weeks after. |
| **05 — Facilitator Manual** (this doc) | You | Your run-of-show for the whole session. |

Docs 02 and 03 are **paste-ready**: their body *is* the prompt the participant pastes. Preserve them exactly — a changed command or JSON block breaks the participant's environment.

---

## PHILOSOPHY — read this before your first session

### What Phase 0 achieves

By the end of a Phase 0 session the participant has, and has *tested*, four things working together:

1. **A second brain** — an Obsidian vault with a PARA structure (Projects / Areas / Resources / Archives).
2. **A real repository** — a Git + GitHub repo in `~/dev`, under their own account, for their first case.
3. **Their first case** — a real work problem, chosen live, with a project brief and a project `CLAUDE.md` that gives Claude the domain context.
4. **The router** — a global `~/.claude/CLAUDE.md` that points Claude to their vault from *any* directory, so they never have to explain where things live.

That's the whole deliverable: not a finished piece of work, but a *working system the participant can pick up again tomorrow.*

### "Kickoff, not finish"

This is the single most important principle for pacing the session, and the one new facilitators break most often.

**Block 4 kicks off the first exercise. It does not finish it.** The session's job is to get the participant *running* on their real problem with Claude Code — not to produce a polished deliverable live. Completing the first workflow is **Week-1 homework** (Doc 04).

Why hold back:

- Finishing live pushes the session past two hours, exhausts the participant's attention, and burns their Claude usage cap.
- It robs them of the agency-building "I did this myself" moment in Week 1 — which is the point of the whole program.

So when the first exercise starts producing output, your instinct will be to keep going until it's "done." Resist it. Produce a partial result, leave a clear breadcrumb for where to continue, and move on. Say it out loud so the participant isn't confused: *"We're not finishing this now — that's the homework, and it's the good part."*

### The peer-level demo

Your opening demo (Block 1) is not a product pitch. It's you showing your **own** working system doing something real — ideally something that mirrors the participant's world. The message you're transmitting is *"this is a normal way for a person like you to work,"* not *"look what the tool can do."* Keep it peer-level: real files, real corrections, a real close-out. Three or four minutes is plenty.

---

## PRE-SESSION

Do these in the days before the session.

### 1. Send Doc 01 a few days ahead

Send **Doc 01 — Pre-Session Setup Instructions** to the participant several days before you meet — enough runway that they can install everything and message you if something fails. Doc 01 is self-service: each prerequisite comes with a paste-ready prompt they run in claude.ai, so they rarely need you. Doc 01 also asks them to **come with 1–3 real work problems** they'd like Claude's help with — this replaces the old intake form and is what feeds the live interview in Block 2.

### 2. The 24-hour prerequisite-verify gate

The day before (or at least 24 hours ahead), confirm the participant is actually set up. Doc 01 ends with a verification prompt that checks the stack; ask them to run it and send you the result. You are looking for **six confirmed items**:

1. **Claude Pro/Max subscription active** — they can log in to claude.ai and use it.
2. **Obsidian installed** — opened at least once. (They should **not** have created a vault yet — that happens live in Block 2.)
> **The Step-7 summary is the gate — and in the field it never arrived on its own from a single
> student.** Treat silence as "not done," never as "probably fine." Two fixes that work:
>
> 1. **Ask for it explicitly** when you send the docs, and again 24h before.
> 2. **Send `tools/aiac-status-check.sh`** (as a `.sh.txt` twin — WhatsApp and Gmail block `.sh`).
>    It is read-only and reports DONE / NOT DONE per document; the first NOT DONE is the resume
>    point. Have them run it in their **Terminal, not inside Claude Code** — under a sandbox
>    Claude's Bash is confined to the vault, so `~/.claude` checks would fail for the wrong reason.
>
> A third option that works even better for non-technical participants: **run the pre-session
> live with them** (install together, gate impossible to fail silently).
>
> **A fourth option is no longer optional: Block 0 below re-runs the same script live, as the
> first thing you do in the session** — regardless of whether the pre-session send worked. Treat
> a failed pre-session ask as expected, not a scramble; Block 0 is the backstop that catches it.

> **If the participant asks that Claude only touch the vault they give it** — send them
> **`02-S — Sandbox Setup`** as well, to run after Doc 01 and *before* Doc 02. Roughly one in ten
> asks for this unprompted, and it is the objection that otherwise blocks anyone on an employer
> machine. Three things to know before you agree to run it:
>
> - Doc 02's **STEP 3 permissions block is skipped** — 02-S replaces it deliberately.
> - **Claude cannot run `git`** under the sandbox (blocked by design, not misconfiguration). The
>   participant runs git themselves; the commit becomes their act of approval. Say this up front
>   so it doesn't read as a failure mid-session.
> - **`gh` may fail** under strict mode (TLS in Go CLIs under Seatbelt). Use HTTPS + a **classic**
>   PAT; the kit already treats `gh` as optional.
>
> Mac and Linux only — native Windows has no sandbox (WSL2 required). One full Phase 0 has run on
> it end to end, Block 7 passed.
>
> **"They told me it's done" is a report, not a state.** One session started blind; another was
> scheduled on "everything's installed" and then stalled twice, a week apart, on a missing PATH
> entry. Conversely, one student written off as 19 days behind turned out to be *finished* and
> waiting on us — the script is what found that.

3. **Git installed and a GitHub account that exists** — that is the gate. `gh` itself is NOT required (Doc 01 never installs it on Mac and calls it optional on Windows). Run `gh auth status` only to find out which path Step 2 takes: logged in -> `gh` path; not installed or not logged in -> Git Credential Manager or a PAT. Either answer is fine; neither blocks the session.
4. **Claude Code installed and working** — `claude --version` returns a version. (On Mac, a modern terminal such as Ghostty is nice-to-have; the built-in Terminal also works.)
5. **Granola installed** — and screen/microphone permissions granted so it can record the session.
6. **1–3 real work problems ready** — they've thought about what they want to work on.

If any of the six is missing, resolve it **before** the session, not during it. A prerequisite failure discovered live is the most common way a 90-minute session becomes a 2+ hour one.

### 3. Confirm Granola will record

Granola recording is **mandatory** — it's how the session gets transcribed for follow-up. Confirm Granola is installed and permitted at the gate above, and confirm it is actually **recording** at the top of Block 0.5, right after the Block 0 status check, before anything else in the session proper.

### 4. The Block-0 access gate (this kit's version)

The internal Spanish pipeline has facilitators chase a *collaborator invite* to a central repo before the session — because there, the repo is pre-created in a shared org. **This kit does not work that way.** Here the participant creates **their own** repo under **their own** GitHub account, live, during Block 2.

So the access gate for this kit is simpler. All you need confirmed is:

> **The participant has Claude Code running + a GitHub account + `gh` authenticated.**

Verify authentication live at the top of the session with:

```
gh auth status
```

If it reports a logged-in GitHub user, the Block-2 repo-creation step will work. If it errors or shows "not logged in," pause and have them run `gh auth login` (browser flow) before you proceed. There is **no** collaborator invite to accept and **no** central repo — do not go looking for one.

---

## THE 90-MINUTE RUN-OF-SHOW

Nine blocks, ~90 minutes plus a ~5-minute buffer for Block 7. Keep this bar visible while you run:

```
[ ] Block 0:   Pre-session status check (live re-verify)  3 min  ← NEW, before anything else
[ ] Block 0.5: Kickoff + pre-work check                   5 min
[ ] Block 1:   Demo (peer-level, 3 key messages)        10 min
[ ] Block 1.5: Obsidian walkthrough                      5 min
[ ] Block 2:   Main Setup Prompt (Doc 02) + interview   30 min  ← capture the VAULT PATH
[ ] Block 3:   Skills & Config (Doc 03) + router test   10 min
[ ] Block 3.5: Status line + context protocol            5 min  ← load-bearing
[ ] Block 4:   First exercise — KICKOFF NOT FINISH      10 min
[ ] Block 5:   Orientation (cheat sheet + Doc 04)      5–10 min
[ ] Block 6:   Quality gates checklist                   —
[ ] Block 7:   Close-out — fresh-window router test      5 min  ← the real end
```

For every block below: **what you do**, **what the participant does**, **teaching talking points** (the narrative; **each block also links its Google Slides deck as optional support** — since 2026-09-10 the 8 decks are official kit material, in EN and ES), **common errors + fixes**, and **timing**.

---

### Block 0 — Pre-Session Status Check (3 min — NEW)

> **Why this exists (added 2026-08-24).** § "The 24-hour prerequisite-verify gate" above already asks the participant to run `tools/aiac-status-check.sh` and send you the result *before* the session — but in the field that self-report "never arrived on its own from a single student." This block makes the live re-run of that same script the formal, mandatory FIRST thing you do in the session, not an ad hoc fallback you reach for only when the pre-session ask visibly failed. It runs before Granola confirmation and before the Block-0.5 access gate — before anything else.

**What you do:**
- Before saying hello, before confirming Granola: have the participant open their **Terminal (not Claude Code)** and run:

  ```
  bash ~/Downloads/aiac-status-check.sh
  ```

  (It should already be on their machine from the pre-session send — `tools/aiac-status-check.sh.txt`. If they don't have it, screen-share and paste the contents of `tools/aiac-status-check.sh` for them to save and run.)

- Have them paste the FULL output into chat or read you the STAGE 0 line.
- **STAGE 0** items marked `[ -- ] NOT DONE` (git / Claude Code / jq / Obsidian) are real gaps — resolve now, before anything else. This is the actual prerequisite check the self-report was supposed to catch.
- Items marked `[sess]` are expected — they're built live starting Block 2, not something the participant missed. Don't chase these.
- If the report reads "READING: you look PRE-SESSION" and Stage 0 is clean, their homework is genuinely complete — move straight to Block 0.5.

**What the participant does:**
- Runs the script in their own terminal, pastes the output.

**Common errors + fixes:**
- Script reports a genuine Stage 0 gap the pre-session send should have caught → fix it now (same fixes as Doc 01); this is exactly the silent-failure case the script exists to catch.
- Participant never received the script ahead of time → screen-share and paste it live; note the delivery gap in your post-session Friction Log so the pre-session send gets checked next time.

**Timing:** 3 min. Don't skip this because "they told me it's ready" — that's precisely the report the field data says not to trust.

### Block 0.5 — Kickoff + Pre-Work Check (5 min)

**What you do:**
- Welcome the participant warmly. This is their first hands-on experience — set a calm, "we've got time" tone.
- Confirm **Granola is recording**.
- Run the access gate: confirm Git works (`git --version`) and that they have a GitHub account. Then run `gh auth status` purely to route: logged in -> use the `gh` path later; anything else -> plan on Git Credential Manager or a PAT. Do NOT stop the session to install `gh`.
- **PAT note (from the field):** if the delivery repo lives under the facilitator's account, a *fine-grained* PAT will NOT reach it — use a **classic** PAT with `repo` scope. On an employer machine whose keychain already holds work credentials, `git config --global credential.useHttpPath true` scopes credentials per-repo without disturbing them.
- Quickly re-confirm the six prerequisite items still hold (Claude Code opens, Obsidian is installed, etc.).

**What the participant does:**
- Confirms their setup, runs `gh auth status`, and (if needed) authenticates.

**Teaching talking points** *(the "why we're here" framing — support: [Deck 1 — Why AI Acceleration Club](https://docs.google.com/presentation/d/1mDNUeBUvxDDso_qUf_ZFeFzcIPBw8OnmT2rt5pnc0iU/edit), 5 slides)*:
- **The program arc.** "Today is Phase 0 — the setup. After this you work on your own for a couple of weeks, then we reconvene. Phase 0 is the foundation everything else stands on."
- **What you'll walk out with.** "In about 90 minutes you'll have four things, all wired together: a second brain in Obsidian, a real code repository, your first actual project, and a setup that lets Claude find all of it automatically. And we'll *test* that it works before we finish."
- **Peer framing.** "This is just how I work every day. Nothing here is exotic — by the end you'll be doing it too."

**Common errors + fixes:**
- `gh auth status` says not logged in → `gh auth login`, choose GitHub.com + HTTPS + browser; re-run to confirm.
- Granola not recording / no permission → grant screen + mic permission in macOS System Settings and restart Granola; do not proceed until it's live.

**Timing:** 5 min. Don't let a green setup tempt you to linger — move to the demo.

---

### Block 1 — Demo (10 min)

**What you do:**
- Show **your own** system doing something real, ideally mirroring the participant's world. Pick from what you actually use:
  - *Finance / family-business* → a report compiled from source data, with the commentary written for you.
  - *Time-pressed exec / GM* → your morning command center: one command that reconstructs the day across your calendars, tasks, and follow-ups into a prioritized plan.
  - *Operations / supply chain* → messy export → clean structured data → an actual decision (a reorder point, a forecast), with Claude catching the data-quality edge cases.
  - *Creative / brand* → building a small interactive tool live from a one-line idea.
  - *Knowledge worker / unsure* → the second-brain + correction loop: make a correction and watch it get written into a `CLAUDE.md` so it sticks.
- Keep it to 3–4 minutes of doing, then recap.

**What the participant does:**
- Watches. That's it — this is your block.

**Teaching talking points** *(the 3 key messages + the mental-model map — support: [Deck 2 — Demo Framing](https://docs.google.com/presentation/d/1WitxhK3dvXZiYm_a9Hm0zE6JpQwJTxqCJgBligQmVqM/edit), 3 slides, only if the demo is slow to start)*:

Open with the **30-second mental-model map** — the #1 friction for newcomers is not vocabulary, it's not seeing how the pieces fit. Say:

> "There are three pieces, each with one job. **Claude Code** is the AI in your terminal — it *acts*. Your **vault** in Obsidian is where your knowledge lives — it *stores*. **Git and GitHub** are the history and the backup for your code. You work *with* Claude, *inside* your vault; Git protects the code part."

Then, during the demo, land the **three key messages**:

1. **"Claude reads the `CLAUDE.md` automatically — it already knows the project context."** (The `CLAUDE.md` is the system's brain.)
2. **"Every correction I make gets saved — so it gets smarter over time."** (Corrections compound into permanent behavior.)
3. **"I close every session with `/session-close` — that's what preserves the state."** (Discipline is what makes the system reliable.)

Close with a **"what you just saw"** recap: name the three things Claude did on its own (read the context, produced the artifact, and — if you showed it — saved a correction).

**Common errors + fixes:**
- The demo lands flat / feels like a tool showcase → pull it back to *their* world and *your* real files. The emotional beat is "a person like me works this way," not "look what it can do."
- You start improvising and it runs long → pick one tight thing you can do in 3 minutes. Longer is worse.

**Timing:** 10 min including the recap.

---

### Block 1.5 — Obsidian Walkthrough (5 min)

**What you do:**
- Before running any setup, walk the participant through Obsidian so the PARA structure that's about to be generated makes visual sense. (Doing this *first* prevents the mid-setup hand-holding that used to slow Block 2 down.)
- Have them open Obsidian (they installed it in the prereqs but should **not** have created a vault yet).

**What the participant does:**
- Follows along in Obsidian:
  1. **Left panel — the file tree.** "Each folder here becomes a section of your second brain."
  2. **Create a new note (Cmd/Ctrl+N).** "Notes are just Markdown files — plain text with formatting."
  3. **Wikilinks — type `[[Test]]` in the note.** "This is how notes connect — like Wikipedia's internal links."
  4. **Graph view (left sidebar icon).** "This is where your knowledge becomes a network."
  5. **Command palette (Cmd/Ctrl+P).** "Anything Obsidian can do, you can find here."

**Teaching talking points** *(support: [Deck 3 — Obsidian + PARA + GTD](https://docs.google.com/presentation/d/1SrDJ-RjJgkr1XrAFkg2BqFGddu-YQP9ijlW4QJIqp_s/edit), 8 slides)*:
- **Your second brain, yours forever.** "It's plain-text Markdown on your own disk — no vendor lock-in. If Obsidian disappeared tomorrow, your notes are still just files you own."
- **PARA.** "Four buckets: **Projects** (active, with an end), **Areas** (ongoing responsibilities), **Resources** (reference material), **Archives** (done). Everything has a home."
- **GTD in one line.** "Capture → Clarify → Organize → Engage. Get it out of your head, decide what it is, put it where it belongs, then do it."
- **Where Claude Code fits.** "The `CLAUDE.md` files are the *rules*; the folders are the *data*. Claude reads the rules and works over the data."

Then point at the empty vault and set the cliffhanger:

> "Right now this is empty. In the next 30 minutes, Claude Code is going to fill it — the PARA structure, a project brief for your case, an area map, and your AI Acceleration Club journey brief. Watch the left panel populate as we go."

**Common errors + fixes:**
- The participant already created a vault → fine, use it, but make sure it's empty; if it has clutter, create a fresh empty one now.
- Graph view is empty and confusing → that's expected on an empty vault; tell them it fills in as notes and links appear.

**Timing:** 5 min. This is orientation, not a tutorial — keep it moving.

---

### Block 2 — Main Setup Prompt + Live Interview (30 min)

This is the biggest block and the heart of the setup. **Doc 02** is the prompt.

**What you do:**
- Have the participant create a new vault and launch Claude Code inside it (see the Mac path-with-spaces note below).
- Have them paste **Doc 02** into Claude Code.
- Watch for errors, explain what each step does as it happens, and — critically — **note the vault path** when it's created. You need it later, and the participant will be moving fast.
- During the **live interview** portion, help the participant articulate their work problems and steer toward a first case that's a good fit (see below).

**What the participant does:**
1. Creates a new vault in Obsidian (GUI → "Create new vault").
2. Opens a terminal and launches Claude Code from inside that vault (or launches it straight from the Obsidian-created vault folder — see the gotcha).
3. Pastes **Doc 02** and works through it interactively.

**The live interview — the key difference in this kit.** Where the internal pipeline pre-builds the participant's project files from a form, Doc 02 instead has Claude run the interview *live*. Claude will:
- Ask what they do and their role.
- Ask about their 1–3 work problems (the ones Doc 01 told them to bring).
- Ask 1–2 light calibration questions (terminal / Git comfort) to set pacing.
- Recommend the **best first case** — and, on the participant's confirmation, generate their project `CLAUDE.md` and project brief on the spot.

Your job during the interview is to be the human co-pilot: help them pick the case with **data they can actually bring** and a **first prototype that fits in 10–15 minutes** of Week-1 work. If they're torn between two problems, steer toward the one that's more concrete and more painful to them. Claude also asks for their name + email (or reads `git config`) and derives the repo name from the chosen case — you don't fill anything in.

**What the Main Setup Prompt builds:**
- PARA folder structure + the `05 AI/CLAUDE CODE/` workspace.
- The vault `CLAUDE.md` (behavioral rules) and the global router `~/.claude/CLAUDE.md`.
- `settings.json` (permissions + sound hook + the context monitor).
- Git configured, GitHub connected, and a repo in `~/dev` — **under the participant's own account** by default, or a facilitator-owned repo they have been invited to and accepted (see Block 6).
- The repo `CLAUDE.md` (case-specific domain context, from the interview).
- The project brief in `01 PROJECTS/`, the Area MOC, and the AI Acceleration Club journey brief.
- The first commit and the AIAC Cheat Sheet.

**Teaching talking points** *(support: [Deck 5 — Main Setup Prompt](https://docs.google.com/presentation/d/1lHx2L90fW5wFSPXCiMoyrSVelWxrH5lJCKQA_tegAqE/edit), 3 slides · [Deck 4 — Git + GitHub 101](https://docs.google.com/presentation/d/17r_FGB_Pff8gPagk1bSIf6svrXrPMsZfO0ElP1ND1Aw/edit), 11 slides — do not run them all)*:
- **What the prompt does.** "This one prompt builds your whole environment in a single interactive run — you're watching a system assemble itself."
- **The `CLAUDE.md` chain.** "There are three levels, from general to specific: the **global router** (`~/.claude/CLAUDE.md`) points to your vault from anywhere; the **vault `CLAUDE.md`** holds your general working rules; the **repo `CLAUDE.md`** holds the domain knowledge for this one project. Claude reads the most specific one that applies."
- **Two briefs, not one.** "You get two briefs: a **case brief** for the project itself, and a **journey brief** that tracks your progress through the program."
- **Git/GitHub in plain terms** (say these as the Git steps run):
  - "Version control is a time machine for your files."
  - "A repository is just a folder that remembers its whole history."
  - "A commit is a save-state you can always come back to."
  - "GitHub is the remote copy — your backup and, later, how you collaborate."
  - "`.gitignore` is the list of things we *never* save to history — secrets, big data files."
- **Knowledge vs. code.** "Notice the repo lives in `~/dev`, **not** inside the vault. Knowledge in the vault, code in `~/dev`. Keep them separate."

**Common errors + fixes:**
- **Mac vault path with spaces** — if the vault folder name has a space (e.g. "My Vault"), a raw terminal `cd` fails on the unquoted second word. Don't fight it: create/open the vault in Obsidian, then launch `claude` and run the setup from inside Claude Code — it handles spaced paths natively. Pivot to this immediately rather than burning minutes on `cd` syntax.
- **Git not installed** → `xcode-select --install` (Mac) or download from git-scm.com (Windows).
- **Repo creation fails** → confirm the Block-0 `gh auth status` gate actually passed; re-authenticate with `gh auth login` if needed. (There is no clone step and no invite in this kit — the repo is created fresh under their account.)
- **Claude Code auth expired** → re-run `claude` to re-authenticate.
- **Blocked country / needs VPN** → ensure a VPN is active before retrying network steps.
- **The interview stalls — participant can't name a problem** → fall back to the 1–3 problems they brought per Doc 01; if still stuck, pick a concrete, data-backed recurring task from their described role and name it yourself. Don't let this block stall; a decent first case beats a perfect one.

**Timing:** 30 min. **Capture the vault path before you leave this block.**

---

### Block 3 — Skills & Config + Router Test (10 min)

**Doc 03** is the prompt. The participant should still be in Claude Code, in the vault.

**What you do:**
- Have them paste **Doc 03**.
- When Doc 03 asks which **email stack** they use (Google / Microsoft / other), help them answer — the prompt follows the matching path live.
- After it runs, run the **mandatory outside-the-vault routing test** (below). Do not skip it.

**What the participant does:**
- Pastes Doc 03 and works through it. It installs the router-first global `CLAUDE.md`, the Compound Engineering and Superpowers plugins, Granola + `/meeting-minutes`, the core Phase-E skills (`project-create`, `playground`, `inbox-clear`, `retro`, `skill-create`), the inline `/session-close` skill, and walks them through Plan Mode.

**The mandatory router routing test** (this is a real gate, caught too late in past sessions):
1. Type `/exit` to leave Claude Code.
2. `cd ~`
3. Run `claude`
4. Ask: **"What files are in my vault INBOX?"**

If Claude reads the vault INBOX **without being given the path**, the router works. If it says "I don't know where your vault is," the global `CLAUDE.md` was generated as a *profile* doc instead of a *router*. Fix it now (re-run the router step in Doc 03 / apply the router-fix), then re-run the test until it passes.

**Teaching talking points** *(support: [Deck 6 — Skills + Plugins](https://docs.google.com/presentation/d/1v-JuXDTYHxv2mPoApT5lk9Qp0G5THCio6EusolrT8uo/edit), 3 slides)*:
- **What a skill is.** "A skill is a reusable procedure you invoke with `/name`. Think of it as a saved playbook Claude already knows how to run."
- **The plugins.** "**Compound Engineering** and **Superpowers** give you a big library of these playbooks for free."
- **Skills activate in new sessions only.** "Anything you install now shows up the *next* time you start Claude Code — not retroactively in this session. That's why we test in a fresh window later."
- **Why the router matters** (say it out loud): "`~/.claude/CLAUDE.md` is why Claude always knows where your vault is, from any folder on your computer."
- **The sound hook.** "The sound means you can walk away and come back when Claude's done."
- **The one habit.** "`/session-close` is the single most important habit — it's what makes you smarter over time."

**Common errors + fixes:**
- **Router generated as a profile doc** (the classic bug) → the outside-the-vault test catches it; re-run the router step / apply the router-fix, then re-test.
- **Plan Mode confusion** → have them press Shift+Tab twice, type a real prompt, review the plan, then exit. It's just practice — no need to execute.
- **Email-stack branch picked wrong** → re-run that step with the correct stack.

**Timing:** 10 min including the routing test.

---

### Block 3.5 — Status Line + Context Protocol (5 min)

This is short but **load-bearing.** The context window is one of the two most important mental models (the other is `CLAUDE.md`). Members who understand it from day one avoid the "my session got worse the longer I worked" failure mode.

**What you do — Part 1, set up the status line (2 min):**
- With Claude Code running, have the participant type `/statusline-setup` and follow the prompts to enable a context-% display in the terminal.
- If `/statusline-setup` isn't available, fall back to the prompt: *"Please add a status line to my Claude Code setup that displays my current context window usage as a percentage."*
- Confirm they can see something like "43% context" in the bar.

**What you do — Part 2, teach the protocol (3 min):** Say these three thresholds out loud — they *are* the protocol:

- **Compact ideally before 50%.** Best quality. This is the target — plan your sessions to hit natural break points before 50%, then `/session-close` + `/clear`.
- **After 50%, context rot starts.** Not catastrophic, but Claude starts forgetting earlier context and making inconsistent references. Quality degrades gradually from here.
- **Compact certainly before 70%.** Past 70%, output quality falls off a cliff. A reactive auto-compact is much messier than a proactive one. Never work past 70%.

The two ways to compact when you hit the threshold:
- **A. `/session-close` + `/clear`** — cleanest. State saved to the brief's Continuation Prompt, then reset. Best for task transitions.
- **B. `/compact`** — Claude Code's built-in in-session compaction; keeps you going mid-task without restarting. Lossy by design, so A is the better habit.

**Teaching talking points** *(support: [Deck 7 — Context Window + Status Line](https://docs.google.com/presentation/d/1DwvVL_MVjRjfnDWT5RhNC4YER6UffsKzI1MQFroSpiM/edit), 4 slides)* — say the "why" out loud:

> "If you take one protocol from today, it's this one. Watching the context bar is the single habit that separates members who improve over time from members whose sessions get worse the longer they work. You *can* work past 50% — but now you're on notice. Past 70% is where you pay for it."

**What the participant does:**
- Sets up the status line, confirms the % is visible, and can repeat the three thresholds back to you.

**Common errors + fixes:**
- `/statusline-setup` not available → use the fallback prompt; Claude edits `~/.claude/settings.json` and restarts with the bar visible.
- Status line doesn't appear → confirm the session restarted after the edit.

**Timing:** 5 min. Don't cut this to save time — it's the highest-leverage 5 minutes in the session.

---

### Block 4 — First Exercise: KICKOFF NOT FINISH (10 min)

Re-read the **"Kickoff, not finish"** principle above before you run this. This block gets the participant *running* on their real problem — it does **not** complete a deliverable.

**What you do:**
- Set `REPO` once and reuse it. The repo lives in `~/dev`, **not** the vault:

  ```
  REPO="$HOME/dev/<their-repo-name>"
  ```

- Choose the path by whether the participant brought data:

  **Path A — they brought data files:**
  ```
  # copy their files in (cap at 2–3 PDFs / files)
  cp <their-file> "$REPO/data/"
  cd "$REPO" && claude
  ```
  Then run a case-appropriate **kickoff** prompt — one that produces *partial* output and leaves a clear "continue from here in Week 1" breadcrumb. For example: *"Read the CLAUDE.md, then read the files in data/. For each file, tell me what's in it, how many rows, what period it covers, and how it maps to the project structure in the CLAUDE.md."*

  **Path B — no data yet:**
  ```
  cd "$REPO" && claude
  ```
  Then: *"Read the CLAUDE.md. Create a data inventory template at docs/data-inventory.md that I can fill in over the next week."*

**What the participant does:**
- Copies in data (Path A) or generates the inventory template (Path B), runs the kickoff prompt, and sees Claude working on *their* real problem.

**Teaching talking points** *(support: [Deck 8 — First Exercise + Homework](https://docs.google.com/presentation/d/1xz_91oO93udpz6ss_grLQh1CwljvFxPfY56sHtEbeVs/edit), 4 slides)*:
- **Path A vs Path B.** "If you brought data, we point Claude at it. If not, we build the checklist for gathering it. Either way you leave with momentum."
- **Kickoff not finish.** Say it explicitly: *"We're not finishing this right now. You'll keep going this week on your own — that's the whole point. My job today is to get you into the flow where you KNOW you can pick this up tomorrow."*
- **When stuck, come back.** "This week, if you get stuck, that's normal and there's no shame in it — reach out and we'll unstick you." (This sets up the support model in Doc 04.)

**Common errors + fixes:**
- **You're tempted to finish it** → don't. Partial output + a breadcrumb is the *correct* outcome.
- **No data and no clear inventory** → the `docs/data-inventory.md` template is the deliverable; it's a perfectly good Week-1 starting point.
- **Data files are huge / many** → cap at 2–3; the point is to demonstrate the flow, not ingest everything.

**Timing:** 10 min. Stop even if the output is partial — *especially* if it's partial.

---

### Block 5 — Orientation (5–10 min)

**What you do:**
- Walk through the **AIAC Cheat Sheet** (created during Block 2/3, in the vault INBOX).
- Hand over **Doc 04 — Next Steps Brief** as the participant's homework and roadmap.

**What the participant does:**
- Follows along on the cheat sheet; receives Doc 04.

**Teaching talking points** — emphasize five things:
1. **Two workspaces:** vault (notes, thinking) vs. repo (code, data).
2. **The self-improvement loop:** correct Claude → the correction gets written into a `CLAUDE.md` → never repeat the mistake.
3. **Always `/session-close`** before ending — it's the compound-learning mechanism.
4. **Plan before building:** Shift+Tab (twice) for medium tasks, `/ce:plan` for big ones.
5. **Homework** (in Doc 04): open Claude Code daily (even 10 minutes), collect the data for the case, and complete the first workflow.

**Doc 04 note:** Doc 04 contains a section the participant fills in themselves at session end — the "your next workflows" list — because their case was chosen live rather than pre-scripted. Point them at it and encourage them to jot 2–3 next steps for their project while it's fresh.

**Common errors + fixes:**
- Participant treats homework as optional → frame it as the part where the value actually lands; the session was just the setup.

**Timing:** 5–10 min.

---

### Block 6 — Quality Gates Checklist

Run through this with the participant. If any gate fails, troubleshoot **now**, before the close-out.

```
QUALITY GATES — Phase 0
━━━━━━━━━━━━━━━━━━━━━━━

- [ ] Obsidian vault operational with a CLAUDE.md
- [ ] Claude Code running: claude --version works
- [ ] ~/.claude/CLAUDE.md is a ROUTER (first section = "Default Workspace"
      with an imperative load instruction — NOT a profile-first doc)
- [ ] Outside-the-vault routing test PASSED (cd ~ && claude, then
      "list my vault INBOX" works without giving the path)
- [ ] ~/.claude/settings.json has permissions + sound hook
- [ ] Status line visible in the terminal with a context % display
- [ ] Participant can state the 3 context thresholds
      (compact ideally <50%, certainly <70%, rot starts after 50%)
- [ ] GitHub repo exists with a first commit, and the participant can push to it
      - preferred: under the PARTICIPANT'S OWN account
      - accepted variant: under the FACILITATOR'S account, with the participant
        added as a collaborator AND the invitation accepted before the clone.
        If you take this path, re-read the PAT note in Block 0.5 - a
        fine-grained PAT cannot reach a facilitator-owned repo; it needs a
        CLASSIC PAT with `repo` scope. An unaccepted invite blocks the clone.
- [ ] Project brief in the vault, linked to the repo
- [ ] /session-close skill installed
- [ ] At least one plugin installed (Compound Engineering or Superpowers)
- [ ] Ran at least one real prompt on their case (Path A or Path B)
- [ ] Can articulate what they'll work on this week
```

**Timing:** folded into the flow; usually 2–3 min if everything held.

---

### Block 7 — Close-Out: Fresh-Window Router Test (5 min) — THE REAL END

The session does **not** end at the quality gates. It ends when the participant has **two Claude Code windows open**: one still working in the repo, and one freshly opened from *outside* the vault that proves the whole stack — router + project brief — works end-to-end. Without this last test, they walk away "set up but untested"; with it, they walk away "ready to work."

**What you do — Part 1, leave the current window open:**
- The participant should **not** close the Claude Code session running in the repo. That's their sandbox to keep working in. No `/exit`, no closing the tab.

**What you do — Part 2, open a second window and test:**
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
- It returns a 3-bullet summary — **without** the participant giving any path.

**If it passes:** they now have proof the whole stack works end-to-end. Say:

> "That's it — we just tested the full loop. Tomorrow you open Claude Code, tell it to pick up where you left off, and it does."

**If it fails — common modes + fixes:**
- "I don't know where your vault is" → the router block wasn't generated correctly; re-apply the router-fix from Doc 03's router step and re-run the test.
- Finds the vault but not the brief → the brief path is wrong or the file wasn't created; check `01 PROJECTS/` for the actual filename and correct the path in the vault `CLAUDE.md`.
- Reads everything but the summary is garbled → likely a minor frontmatter issue; rare — note it as a Week-1 homework fix and move on.

**Do not declare the session complete until this test passes.** This is the true end — not Block 6.

**Say the result out loud and write it down** — *"router test: PASSED"* or *"router test: FAILED because X"* — and tick the Block 7 box in your agenda. The recording is the only thing the close-out (`/aiac-close`) can read; if nobody states the result, the close cannot confirm graduation. Evidence 2026-09-10: a session ended on *"I need to know whether it worked"* and the close had to mark the test unverified.

**Timing:** 5 min (+ buffer if you troubleshoot).

---

## POST-SESSION

Do these the same day, while it's fresh.

- **Send the reference docs.** Send **Docs 02, 03, and 04** to the participant. Docs 02 and 03 are their re-setup safety net (if they ever need to rebuild the environment); **Doc 04** is their roadmap and homework for the coming weeks.
- **Confirm the homework is clear.** In your follow-up note, restate the three homework items from Doc 04: open Claude Code daily (even 10 min), collect the case data, and complete the first workflow. Remind them the first exercise was a *kickoff* — finishing it this week is the point.
- **How to follow up.** Check back after 1–2 weeks of their self-directed work. If they go quiet, a single low-pressure nudge ("how's the case going — anything stuck?") is usually enough. Keep the support model no-shame: getting stuck is expected, not a failure.
- **Granola.** The session recording is your source for a transcript and any follow-up minutes; retrieve it if you want a written record.

---

## FACILITATOR'S OWN ONE-TIME SETUP

Do this **once**, before you run your first session — it's not per-participant.

1. **Set your support channel in Doc 04.** Doc 04 has a single marked placeholder, `[SET: your support channel]`. Replace it with the actual channel your participants should use to reach you (a WhatsApp number, an email, a Slack channel — whatever you run your group on). This is the **only** value you fill in anywhere in the kit; everything else the participant generates live.
2. **Know where the kit lives.** The maintainer keeps the canonical kit alongside the AI Acceleration Club Phase 0 materials. Keep your own working copy wherever you actually run sessions from, but check back for an updated version before each session.
3. **Remember the format.** This kit is **one-on-one**. This manual's narrative is your script; **the decks linked in each block are optional support** (screen-share them if they help, skip them if not).

---

## FUTURE EXTENSIONS (out of scope for now)

Noted so you know they're deliberate omissions, not gaps:

- **Group / cohort format.** This kit is 1-on-1 only. A group format (multiple participants, a shared live deck, parallel setup) exists in the internal Spanish pipeline but is a separate future project here.
- **English teaching decks.** This manual carries the teaching narrative so you can run without slides. Building English slide decks (the equivalent of the Spanish deck set) is a separate future project.
- **Installable plugin / skill pack.** There's no facilitator plugin in this kit by design — it's docs-only so it works for anyone with no shared infrastructure.
