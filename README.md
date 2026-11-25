# AIAC Facilitator Pack

**English** · [Español](LEEME.md)

This is a free kit for getting the people in your business started with
**Claude Code**, an AI assistant that works on the files on your computer
instead of just chatting with you. In one live session, each person goes from
never having used it to doing a real task from their own job. They don't type
code: they give Claude prompts that are already written for them. They also
leave with their own "second brain", a folder of plain notes on their computer
that the AI reads and keeps up to date.

- **Who it's for:** a business owner, or someone on your team you choose to
  run it (the *facilitator*), plus the people they bring on board (the
  *participants*). Neither side needs a technical background.
- **What it costs:** the kit itself is free. Each participant needs their own
  Claude plan. **Claude Pro** (about $20/month; see
  [claude.com/pricing](https://claude.com/pricing)) is enough to start, and you
  only upgrade if you keep hitting its limits.
- **How long it takes:** participants do the installs on their own before the
  session, then have one live session, alone or in a small group. That session
  takes about 90 minutes when everything goes well. Plan 2–3 hours for your
  first few, and more for groups.
- **Editions:** English and Spanish, Mac and Windows.

**Start here:**

- **I'm running a session** → [Facilitator Manual (Doc 05)](Co-Facilitator%20Kit%20(EN)/05%20%E2%80%94%20Facilitator%20Manual%20%E2%80%94%20How%20to%20Run%20a%20Phase%200%20Session.md)
- **I'm a participant** → [Before your session (Doc 01)](Co-Facilitator%20Kit%20(EN)/01%20%E2%80%94%20Pre-Session%20Setup%20Instructions%20(Participant).md)
- **I want to see everything** → [Full kit index](Co-Facilitator%20Kit%20(EN)/README%20%E2%80%94%20Kit%20Index%20%26%20How%20to%20Use.md)

---

## What's in this repo

| Folder | What it is |
|---|---|
| [`Co-Facilitator Kit (EN)/`](Co-Facilitator%20Kit%20(EN)/) · [`(ES)/`](Co-Facilitator%20Kit%20(ES)/) | The session materials. The facilitator manual (Doc 05) is the core; read it first. The kit index lists every document and who gets it. |
| `Co-Facilitator Kit (…)/tools/` | `aiac-status-check.sh`, a read-only check the participant runs before the session. It ends with a short block of `DONE` / `NOT DONE` lines that is safe to share; the participant sends **only that block**. |
| `bin/` · `.githooks/` · `tests/` | The private-data gate that keeps participant data out of this repo (see Contributing). |

This is the method the AI Acceleration Club uses for its own onboarding,
released free and open source so anyone can run it with their team.

## Not locked to one AI tool

The method is plain text files (Markdown notes, a few instruction files) plus
standard tools such as Git and GitHub. Your notes and projects stay readable
in any editor and belong to you. **Claude Code is the tool we recommend
today**, and every prompt in the kit is written for it, but the vault, the
project briefs and the habits carry over if you switch to a different AI tool
later.

## Which edition to send

Choose per **participant**, never per facilitator: one facilitator can run
sessions in two languages and two registers. The Spanish edition is neutral
Latin-American Spanish with *tú* (tuteo). Argentine *voseo* differences live
in `00V` as a diff table, not a fork. Windows participants get the `W`
editions of Docs 02 and 03. The [kit index](Co-Facilitator%20Kit%20(EN)/README%20%E2%80%94%20Kit%20Index%20%26%20How%20to%20Use.md)
has the full send list.

## Delivery rules

- Send **Markdown**, never Word or PDF. A curly quote inside a JSON block or a
  shell command fails live, mid-session.
- Long prompts are **loaded by file, not pasted**: the participant saves the
  document and tells Claude "Read the file <path> and follow its
  instructions". Terminals, the Windows one especially, can cut off a long
  paste.
- Send `tools/aiac-status-check.sh.txt`, not the `.sh`, because WhatsApp and
  Gmail block `.sh` attachments. The two files are byte-identical by design.
  The participant runs the exact filename they received, for example
  `bash ~/Downloads/aiac-status-check.sh.txt`, and shares only the block
  between `----- AIAC STATUS (safe to share) -----` and `----- END -----`.

## Contributing

Corrections from real sessions are the most valuable contribution: a command
that failed on someone's machine, a step that confused a participant, a
translation that reads wrong. See [`CONTRIBUTING.md`](CONTRIBUTING.md). The
first thing to run after cloning:

```bash
bash bin/install-hooks.sh
```

`.git/hooks` is not copied by `git clone`, so this command turns on the
private-data gate for your commits. CI runs the same gate on every PR.

**What the gate does and doesn't catch:** it blocks email addresses that are
not on the allowlist, and internal files that are deliberately kept out of
the public pack. It does **not** detect names, phone numbers or secrets
automatically. Human review catches those, so never put participant data in
an issue or a PR.

## Security

To report a security or privacy problem (for example, the status check
printing something it shouldn't, a hole in the gate, or a setup prompt that
grants broader permissions than it says), see [`SECURITY.md`](SECURITY.md).
Please report it privately and don't open a public issue.

## Credits

Created by the AI Acceleration Club. Field-tested and extended by
**Mangan** ([@dibkorma](https://github.com/dibkorma)), who ran the kit
independently with ten students. The Windows editions, the opt-in sandbox
(`02-S`), the pre-session status check and the delivery rules all came out of
his field report.

## License

- **Content** (everything in the Kit folders except `tools/`):
  [Creative Commons Attribution 4.0](LICENSE). Use it, translate it, adapt it,
  republish it, run it commercially; credit "AIAC Facilitator Pack, AI
  Acceleration Club".
- **Code** (`tools/`, `bin/`, `.githooks/`, `tests/`): [MIT](LICENSE-CODE).

Neither license covers the **AI Acceleration Club** name. You are welcome to
say your session uses the AIAC Facilitator Pack, but please don't present
yourself as an AIAC-certified facilitator unless you are one.
