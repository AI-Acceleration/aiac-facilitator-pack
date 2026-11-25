# AIAC Phase 0 Co-Facilitator Kit (EN)

[← Back to the repo front page](../README.md) · [Kit en español](../Co-Facilitator%20Kit%20(ES)/README%20%E2%80%94%20Kit%20Index%20%26%20How%20to%20Use.md)

This is a self-contained, **docs-only** kit in English for running a **Phase 0
onboarding session** with anyone. Nothing needs to be configured in advance
and there is no intake form. The participant **builds their own project live
during the session** through a guided interview. It is built for 1-on-1
sessions; small groups work, but they need more time.

## How it works in one paragraph

You (the facilitator) send the participant **Doc 01** (and **Doc 07**, the
vocabulary) a few days before. They install everything on their own and finish
with a short pre-flight check whose one-line result they send you. On session
day you run the 8-block flow in **Doc 05 (the manual)**. The participant gives
**Doc 02** to Claude Code **by file**: they save it, then tell Claude "Read
the file <path> and follow its instructions". Claude interviews them, picks
their first real case, and builds their own vault and project. Then they
load **Doc 03** the same way to install skills and config. At the end you hand
them **Doc 04** (the homework roadmap) and **Doc 06** (how to make the Pro plan
last). The session *kicks off* their first project, and the Week-1 homework
finishes it. Timing: about 90 minutes when everything goes well. Plan 2–3
hours for your first sessions.

## The documents (read in this order)

| # | Document | Audience | When |
|---|----------|----------|------|
| **05** | [**Facilitator Manual — How to Run a Phase 0 Session**](05%20%E2%80%94%20Facilitator%20Manual%20%E2%80%94%20How%20to%20Run%20a%20Phase%200%20Session.md) | You (facilitator) | **Read this first.** Run-of-show, talking points, gates. |
| 01 | [Pre-Session Setup Instructions](01%20%E2%80%94%20Pre-Session%20Setup%20Instructions%20(Participant).md) | Participant | Sent a few days before the session. |
| 07 | [Vocabulary](07%20%E2%80%94%20Vocabulary%20(Participant).md) | Participant | Sent with Doc 01. Five minutes of reading, about a day before the session. |
| 02 | [Main Setup Prompt](02%20%E2%80%94%20Main%20Setup%20Prompt%20(Participant).md) | Participant | Loaded into Claude Code by file during **Block 2** (contains the live interview). |
| 03 | [Skills & Config Setup Prompt](03%20%E2%80%94%20Skills%20%26%20Config%20Setup%20Prompt%20(Participant).md) | Participant | Loaded into Claude Code by file during **Block 3**. |
| 04 | [Next Steps Brief](04%20%E2%80%94%20Next%20Steps%20Brief%20(Participant).md) | Participant | Handed over at **Block 5** as the homework roadmap. |
| 06 | [Pro Plan Survival Kit](06%20%E2%80%94%20Pro%20Plan%20Survival%20Kit%20(Participant).md) | Participant | Handed over with Doc 04, to read before starting real work. How usage limits work and how to make Pro last. |
| **02-S** | [**Sandbox Setup**](02-S%20%E2%80%94%20Sandbox%20Setup%20(Participant,%20opt-in).md) *(opt-in)* | Participant | **Only for participants who ask that Claude be confined to their vault.** Runs after Doc 01 and **before** Doc 02, and replaces Doc 02's STEP 3 permissions block. Not part of the default flow. Mac/Linux only. |
| **02W** | [**Main Setup Prompt (Windows)**](02W%20%E2%80%94%20Main%20Setup%20Prompt%20(Windows).md) | Participant | **Send instead of Doc 02 to a Windows participant.** |
| **03W** | [**Skills & Config Setup Prompt (Windows)**](03W%20%E2%80%94%20Skills%20%26%20Config%20Setup%20Prompt%20(Windows).md) | Participant | **Send instead of Doc 03 to a Windows participant.** |
| **00W** | [**Windows Edition Diff Tables**](00W%20%E2%80%94%20Windows%20Edition%20Diff%20Tables%20(FACILITATOR%20ONLY).md) | Maintainer | 🚨 **Facilitator only, never send.** The auditable record of every Windows deviation. |

## Which edition to send

| Participant | Send |
|---|---|
| **Mac** | 01 · 07 before the session; 02 · 03 during it; 04 · 06 at the end |
| **Windows** | 01 · 07 before; **02W** · **03W** during; 04 · 06 at the end. Docs 01, 04, 06 and 07 are shared and need no variant |
| **Wants Claude confined to their vault** (Mac/Linux) | 01 · 07 · **02-S** · 02 · 03 · 04 · 06, in that order |

Windows is a **variant, not a fork**: `02W`/`03W` are the EN docs plus a listed
set of changes, recorded in `00W — Windows Edition Diff Tables`. When you change
Doc 02 or 03, check whether the change belongs in the W variant too, and update
the diff table either way.

**Never available on Windows:** the `02-S` sandbox module. Native Windows has no
sandbox (WSL2 required), so a Windows participant who asks for scoping needs a
different answer.

**Plan:** Claude **Pro** is the default and is enough to start. Upgrade to Max
only when the limits keep getting in the way. Doc 06 explains how to tell.

## Before your first session: the TWO things to fill in

Everything else in the kit is generic. These two placeholders are yours:

1. **`[SET: your support channel]`** in **Doc 04**. Replace it with the channel
   your participants use to reach you (a WhatsApp group, a Slack channel, your
   email).
2. **`[TOOL]`** in **Docs 03 and 03W**. Replace it with the participant's
   meeting-transcription tool: Granola, another transcription tool, or
   `none / pasted transcript`. Recording is optional: always ask everyone in
   the meeting first, and a pasted transcript works just as well.

## Delivery rules: how these docs travel (read before sending anything)

We learned these the hard way in the field. When you break one, nothing
warns you: the participant gets a file that *looks* right and then fails
mid-session.

**1. Send the docs as Markdown (`.md`), never through Word or PDF.**
Docs 01–04 contain prompts and commands. Word curls the quotes, and a curly
quote inside JSON or a shell command **fails live, mid-session**. Docs 06 and 07
are plain reading and are safe to convert if you need to.

> If you ever generate a `.docx`, verify it before sending: check that no
> `Courier New` run contains `' ' " "`, then actually **look** at the rendered
> file. Text checks miss layout bugs.

**2. Long prompts are loaded by file, not pasted.**
Terminals, the Windows one especially, can cut off a long paste without any
warning. The participant saves the doc, copies its path, and tells Claude
"Read the file <path> and follow its instructions". Only short prompts of a
few lines get pasted.

**3. `.sh` attachments are blocked by WhatsApp and Gmail.**
Send the byte-identical `.sh.txt` twin of the status check (it runs the same).
The participant runs the **exact filename they received**, e.g.
`bash ~/Downloads/aiac-status-check.sh.txt`, and sends you **only** the block
between `----- AIAC STATUS (safe to share) -----` and `----- END -----`.
Everything above that block is for their eyes only. Keep any script you send
**100% ASCII** so it survives copy-paste through chat apps.

**4. Private per-participant delivery repos work well.**
One private repo per participant (`aiac-phase0-<name>`), with the docs
hash-verified against the kit after you push. Making it private keeps the
participant's name and your notes to them out of public view. The kit itself
is CC BY 4.0, so you may also republish or adapt it openly, as long as you
credit it. Tell the participant plainly: *don't run Claude Code inside the
clone*. Doc 02 builds the vault wherever Claude Code is running.

**5. Facilitator material never rides along.**
Anything written *about* a participant (tracking notes, diff tables, defect
discussions) lives outside the shareable folder. Keep one `Send to <Name>/`
subfolder that is the only place you ever share from.

## Tools

- **`tools/aiac-status-check.sh`** (send the `.sh.txt` twin): a read-only
  pre-session check the participant runs in their own terminal on macOS,
  Windows (Git Bash or WSL) or Linux. It writes nothing. It prints details for
  the participant first, then a short **safe-to-share block** with only check
  names and `DONE` / `NOT DONE` / `SKIPPED (optional)`, the operating system
  and an overall verdict. The first `NOT DONE` is where to resume.
  `--details` shows more local detail and warns not to share it. Contributed
  by Mangan.

## Where the starter skills come from

Docs 03/03W and 04 install the starter skills from the public
[`AI-Acceleration/cc-starter-pack`](https://github.com/AI-Acceleration/cc-starter-pack)
repo, **pinned to tag `v1.0.0`**, so every participant gets the same reviewed
version. A new version means a new tag and an update to the docs.

## Not locked to one AI tool

The method is plain files (Markdown notes, a few instruction files) plus
standard tools like Git and GitHub. Claude Code is the recommended tool today
and every prompt here is written for it, but the vault and the habits carry
over to other AI tools.

## Scope

- **In:** English, docs-only, participant self-setup live; 1-on-1 by design,
  small groups with extra time.
- **Out:** an installable plugin version of the kit.
