# AIAC Facilitator Pack

Everything you need to run a **Phase 0 onboarding session** for someone else:
in a few hours a participant goes from zero to working with Claude Code on
their own real case, inside a personal knowledge vault. English and Spanish.

This is the method the AI Acceleration Club uses for its own onboarding,
released free and open source so anyone can run it for their team.

| Folder | What it is |
|---|---|
| `Co-Facilitator Kit (EN)/` · `(ES)/` | The session materials. `05 — Facilitator Manual` is the core; read it first. |
| `Co-Facilitator Kit (…)/tools/` | `aiac-status-check.sh`, a read-only pre-session diagnostic that reports DONE / NOT DONE per document. |
| `bin/` · `.githooks/` · `tests/` | The private-data gate that keeps participant data out of this repo (see Contributing). |

**Start here:** `Co-Facilitator Kit (<your edition>)/README — Kit Index & How to Use.md`,
then `05 — Facilitator Manual — How to Run a Phase 0 Session.md`.

## Which edition to send

Choose per **participant**, never per facilitator: one facilitator can run
sessions in two languages and two registers. Spanish defaults to Venezuelan
*tuteo*; Argentine *voseo* differences live in `00V` as a diff table, not a fork.
Windows participants get the `W` editions of Docs 02 and 03.

## Delivery rules

- Send **Markdown**, never Word or PDF. A curly quote inside a JSON block or a
  shell command fails live, mid-session.
- Send `tools/aiac-status-check.sh.txt`, not the `.sh`: WhatsApp and Gmail
  block `.sh` attachments. The two files are byte-identical by design.
- Run it as `bash aiac-status-check.sh`; it is not marked executable, matching
  every instruction in the Kit.

## Contributing

Corrections from real sessions are the most valuable contribution: a command
that failed on someone's machine, a step that confused a participant, a
translation that reads wrong. See `CONTRIBUTING.md`. The first thing to run
after cloning:

```bash
bash bin/install-hooks.sh
```

`.git/hooks` is not copied by `git clone`; this turns on the private-data gate
for your commits. CI runs the same gate on every PR.

## Credits

Created by the AI Acceleration Club. Field-tested and extended by
**Mangan** ([@dibkorma](https://github.com/dibkorma)), who ran the kit
independently with ten students: the Windows editions, the opt-in sandbox
(`02-S`), the pre-session status check and the delivery rules all came out of
his field report.

## License

- **Content** (everything in the Kit folders except `tools/`):
  [Creative Commons Attribution 4.0](LICENSE). Use it, translate it, adapt it,
  run it commercially; credit "AIAC Facilitator Pack, AI Acceleration Club".
- **Code** (`tools/`, `bin/`, `.githooks/`, `tests/`): [MIT](LICENSE-CODE).

Neither license covers the **AI Acceleration Club** name. You are welcome to
say your session uses the AIAC Facilitator Pack; please don't present yourself
as an AIAC-certified facilitator unless you are one.
