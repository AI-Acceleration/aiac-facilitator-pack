# Pro Plan Survival Kit

**For:** participants, after the Phase 0 session. Read it once before you start real work. It takes five minutes.

> **Why this matters.** On the Claude **Pro** plan, your usage is measured in a **rolling 5-hour window**, and there is also a **weekly** cap. Used with a little discipline, that limit works in your favour, because it pushes you to work in batches instead of marathons. Without discipline, you hit the cap and lose hours waiting.
>
> On **Max**, or if your organization gives you Claude with different limits, keep this anyway. The same rules help the day you work with big files.

**Check your usage at any time:** type `/usage` in Claude Code, or open **Settings → Usage** on claude.ai. Plans and prices change, so see [claude.com/pricing](https://claude.com/pricing) for the current ones.

---

## The 3 rules

**Rule 1: heavy work goes in batches, not in one long marathon.**

Every expensive operation, such as processing files, reading large spreadsheets or generating data-heavy reports, uses up part of your Pro usage window. That window is **not** the same as `/context`: `/context` only measures how full the *current conversation* is, not how much of your plan you've used. After each batch, check whether Claude Code is showing a usage-limit warning. No warning means keep going. When one appears, stop and do something else: manual work, reviewing what came out, a coffee. Waiting costs nothing, while hitting the cap leaves you without Claude Code for hours.

**Rule 2: do heavy work on Sunday or early Monday.**

The window rolls, so if you worked hard on Friday afternoon, you start Saturday morning with part of it already used. Sunday and early Monday are usually the cleanest moments. (The weekly cap resets on its own schedule; `/usage` shows when.) Save them for:

- Processing a lot of data at once (many files, large folders)
- Anything that touches more than 20 files in one go
- Long research

**Rule 3: deep research only when it's the only heavy thing that day.**

A deep research run (several sources plus a synthesis, like `/deep-research` if you have it installed) can use up your whole window in one go. For anything lighter:

- Ask Claude to read **one** specific page and summarize it
- Search 1 or 2 specific sources, not "everything out there"

Keep deep research for big decisions, not for "let's see what's out there".

---

## A week that fits in Pro

Use this as your mental model for the first few months:

| Day | Kind of work | Priority |
|-----|--------------|----------|
| Monday | Heavy work (batches, big analyses) | High: clean window |
| Tuesday | Medium work (scripts, iterating) | Medium |
| Wednesday | Reports and dashboards | Medium |
| Thursday | Medium work + adjustments | Medium |
| Friday | Close the week: review your project brief and run `/session-close` | Low: the window may already be loaded |

Leave room for day-to-day work, and for one deep research run a week if you really need it.

---

## If you hit the cap in the middle of a task

Relax. The limit resets by itself and nothing is lost, because your files are on your computer.

1. **As soon as you see the usage warning, run `/session-close`.** It saves where you are into your project brief, with a resume point. If you're already cut off, run it first thing when the limit resets.
2. Close Claude Code and leave it for at least 1–2 hours. Claude Code tells you when the limit resets.
3. When you come back, check `/usage`. If you're under the limit, carry on, and if not, wait longer.
4. If you can't wait, do by hand the work you were going to delegate. There is always useful work that doesn't need AI.

---

## When to move up to Max

Upgrade when you actually feel the ceiling, **not before**. At the time of writing, Max starts at **$100/month for about 5× Pro's usage**; check [claude.com/pricing](https://claude.com/pricing) for current plans. These are the concrete signs:

- You process a lot of data all the time, not just in an occasional batch
- The 5-hour window stops you at least twice a week, or you hit the weekly cap
- You want to run heavy skills without thinking about the cap
- Your daily work with Claude Code regularly runs past 2–3 hours straight

If several of these become routine, Max costs about $100 a month against hours of frustration. Until then, Pro used with discipline will carry you comfortably through the first months, so earn the move to Max with real usage data.
