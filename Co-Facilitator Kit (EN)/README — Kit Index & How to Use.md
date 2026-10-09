---
title: "AIAC Phase 0 Co-Facilitator Kit (EN) — README & Index"
created: 2026-07-14
category: reference
status: draft
tags: [aiac, phase0, co-facilitator, kit, english, readme]
related: ["[[AI Acceleration Club - Phase 0 Playbook]]"]
---

# AIAC Phase 0 Co-Facilitator Kit (EN)

A self-contained, English, **docs-only** kit that lets a co-facilitator run a **1-on-1 Phase 0 onboarding session** for anyone — no pre-configured files, no intake form. The participant **builds their own project live during the session** through a guided interview.

## How it works in one paragraph

You (the facilitator) send the participant **Doc 01** a few days before. On session day you run the ~90-minute, 8-block flow in **Doc 05 (the manual)**: the participant pastes **Doc 02** into Claude Code — which interviews them, picks their first real case, and generates their own vault + project — then pastes **Doc 03** to install skills and config. At the end you hand them **Doc 04** as their homework roadmap. The session *kicks off* their first project; Week-1 homework finishes it.

## The documents (read in this order)

| # | Document | Audience | When |
|---|----------|----------|------|
| **05** | **Facilitator Manual — How to Run a Phase 0 Session** | You (facilitator) | **Read this first.** Run-of-show, talking points, gates. |
| 01 | Pre-Session Setup Instructions | Participant | Sent a few days before the session. |
| 02 | Main Setup Prompt | Participant | Pasted into Claude Code during **Block 2** (contains the live interview). |
| 03 | Skills & Config Setup Prompt | Participant | Pasted into Claude Code during **Block 3**. |
| 04 | Next Steps Brief | Participant | Handed over at **Block 5** as the homework roadmap. |
| **02-S** | **Sandbox Setup** *(opt-in)* | Participant | **Only for participants who ask that Claude be confined to their vault.** Runs after Doc 01 and **before** Doc 02, and replaces Doc 02's STEP 3 permissions block. Not part of the default flow. Mac/Linux only. |
| **02W** | **Main Setup Prompt (Windows)** | Participant | **Send instead of Doc 02 to a Windows participant.** |
| **03W** | **Skills & Config Setup Prompt (Windows)** | Participant | **Send instead of Doc 03 to a Windows participant.** |
| **00W** | **Windows Edition Diff Tables** | Maintainer | 🚨 **Facilitator only — never send.** The auditable record of every Windows deviation. |
| 00 | Design Spec | Maintainer | Provenance / how the kit was derived. Not part of the session, and not in the public repo. |

## Which edition to send

| Participant | Send |
|---|---|
| **Mac** | 01 · 02 · 03 · 04 |
| **Windows** | 01 · **02W** · **03W** · 04 — Doc 01 and Doc 04 are shared and need no variant |
| **Wants Claude confined to their vault** (Mac/Linux) | 01 · **02-S** · 02 · 03 · 04, in that order |

Windows is a **variant, not a fork**: `02W`/`03W` are the EN docs plus a listed set of changes,
recorded in `00W — Windows Edition Diff Tables`. When you change Doc 02 or 03, check whether the
change belongs in the W variant too — and update the diff table either way.

**Never available on Windows:** the `02-S` sandbox module. Native Windows has no sandbox (WSL2
required), so a Windows participant who asks for scoping needs a different answer.

## Before your first session — the ONE thing to set

In **Doc 04**, replace `[SET: your support channel]` with your actual support channel (e.g., a WhatsApp group, a Slack channel, your email). It's the only value you fill in; everything else is generic.

## Delivery rules — how these docs travel (read before sending anything)

Learned the hard way in the field. Breaking these is silent: the participant gets a file that
*looks* right and fails when pasted.

**1. Docs 02 and 03 must NEVER travel through Word or PDF.**
Their body *is* the prompt the participant pastes into a terminal. Word curls the quotes, and a
curly quote inside JSON or a shell command **fails live, mid-session**. Send them as `.md` (or in
a private repo). **Docs 01 and 04 are safe to convert** — their blocks paste into claude.ai chat,
which tolerates curly quotes.

> Verify any generated `.docx` before sending: check that no `Courier New` run contains
> `' ' " "`, then actually **look** at the rendered file. Text checks miss layout bugs.

**2. `.sh` attachments are blocked by WhatsApp and Gmail.**
Ship a byte-identical `.sh.txt` twin (it runs the same). Keep any script you send **100% ASCII**
so it survives copy-paste through chat apps.

**3. Private per-student delivery repos work well.**
One private repo per participant (`aiac-phase0-<name>`), docs hash-verified against the kit after
push. Private on purpose: sending your kit to your own participant is its intended use;
publishing it openly is republishing the material. Tell them plainly: *don't run Claude Code
inside the clone* — Doc 02 builds the vault wherever Claude Code is running.

**4. Facilitator material never rides along.**
Anything written *about* a participant (tracking notes, diff tables, defect discussions) lives
outside the shareable folder. Keep one `Send to <Name>/` subfolder that is the only surface you
ever share from.

## Tools

- **`tools/aiac-status-check.sh`** — read-only pre-session diagnostic the participant runs in their
  own Terminal. Reports DONE / NOT DONE per document; the first NOT DONE is the resume point. Send
  the `.sh.txt` twin (WhatsApp and Gmail block `.sh`). Contributed by Mangan, adopted 2026-08-19.

## Scope

- **In:** English, 1-on-1, docs-only, participant self-setup live.
- **Out (future):** group/cohort format, English teaching decks (the manual carries the teaching narrative instead), an installable plugin.

## Notes for the maintainer

- The skills in Docs 03/04 install from the **public** `wildbuffaloman/cc-starter-pack` repo. If that repo's visibility ever changes to private, the participant installs will break — keep it public (or bundle the skill bodies).
- Derived from the live Spanish AIAC pipeline templates. **As of 2026-08-19 the live ES pipeline
  IS kept in sync** — the same defect set had propagated there and was patched in the same pass.
  When you fix something here, check `05 AI/CLAUDE CODE/plugins/aiac-pipeline/` for the twin.
- A pristine pre-patch snapshot lives at `../_kit-snapshots/2026-08-19 pre-mangan-patch (do not edit)/`.
  Diff against it to audit any change. Keep a fresh snapshot before the next round of edits.
