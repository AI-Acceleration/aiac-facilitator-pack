---
title: "Sandbox Setup (Participant) — AI Acceleration Club Phase 0"
created: 2026-07-15
category: reference
status: draft
tags: [aiac, phase0, co-facilitator-kit, participant, sandbox, security]
---

**Supports:** Run this BEFORE Doc 02. Replaces Doc 02's STEP 3 permissions block.

# Sandbox Setup — Confining Claude Code to Your Vault

This document is for a participant who wants a **verifiable** boundary around Claude Code, not a promise of one. It is written for someone technical. It does not simplify, and it does not oversell.

Read Part 1 before you run anything. It tells you what you are actually getting — including what you are **not** getting. If Part 1's guarantees aren't strong enough for you, Part 6 tells you what to do instead.

---

## Part 1 — What this actually guarantees

The honest claim first, because the marketing version of this is wrong.

**Claude Code does not run "inside a sandbox."** There is no single boundary around the process. There are two different enforcement mechanisms covering two different sets of tools, and they have very different strengths:

| What runs | Enforced by | Strength |
|---|---|---|
| **Bash commands + every child process they spawn** (including `python`, `node`, `git`, any script) | The OS kernel — Seatbelt on macOS, bubblewrap on Linux/WSL2 | **Hard.** Enforced on the running process. Holds regardless of what the model decided to run, and even if an allowed command does more than its name suggests. |
| **Claude's built-in file tools** — Read, Edit, Write, Glob, Grep | Claude Code's permission system, in-process, evaluated *before* the tool runs | **Application-level.** Deny rules are absolute (first match wins, no exceptions possible), but this is Claude Code enforcing rules on itself, not the kernel enforcing them on a process. |

From the official docs, verbatim:

> "Sandboxing provides OS-level enforcement that restricts what Bash commands can access at the filesystem and network level. **It applies only to Bash commands and their child processes.**"

and

> "**Built-in file tools**: Read, Edit, and Write use the permission system directly rather than running through the sandbox."

So the accurate sentence is: **everything Claude can execute is kernel-confined to your vault; everything Claude reads or writes directly is confined to your vault by permission rules that it evaluates before acting.** Both layers are configured below. Neither is decorative.

### Why the Bash layer is the one that matters

This is the part worth understanding, because it's the reason the standard AIAC config is not sufficient for you.

Permission rules like `Read(~/.ssh/**)` in a deny list work on Claude's own file tools and on file commands Claude Code recognizes in Bash (`cat`, `head`, `tail`, `sed`). They **do not** work on arbitrary subprocesses. Docs, verbatim:

> "They don't apply to arbitrary subprocesses that read or write files indirectly, like a Python or Node script that opens files itself. For OS-level enforcement that blocks all processes from accessing a path, enable the sandbox."

The standard Phase 0 config pre-approves `Bash(python3 *)` and has an **empty deny list**. That combination means a one-line Python script reads anything on the machine, and no permission rule can stop it. Any deny list you add on top of it is theater. The sandbox is what closes that hole — and it closes it at the kernel, which is why it holds even if the model is confused, wrong, or manipulated by something it read.

### What this does NOT protect against

Stated plainly so you can decide for yourself:

- **The network layer does not inspect TLS.** The built-in proxy allows or blocks by the hostname the client claims. Docs warn that broad allowlists "can create paths for data exfiltration" via domain fronting. Our config allowlists narrowly.
- **Hooks.** The sandbox docs enumerate what falls outside the sandbox (built-in file tools, computer use, environment variables, subagents) and **do not mention hooks either way**. I am not going to guess. Treat hooks as unsandboxed. They matter here because Doc 02 Step 3.5 installs two of them — they are shell commands *you* install and can read in full before they ever run, so they are inside your trust boundary by inspection, not by enforcement.
- **MCP servers**, if you add any later (Phase 3). Permission rules apply to them; the sandbox does not.
- **Environment variables.** Sandboxed commands inherit your shell's environment, including any secrets in it. Part 3 handles this.
- **This is not a VM.** Docs: "Sandboxing reduces risk but is not a complete isolation boundary." If your threat model needs one kernel boundary around the entire Claude Code process, see Part 6.

---

## Part 2 — Availability gate (do this first)

**The sandbox runs on macOS, Linux, and WSL2. Native Windows is not supported.**

- **macOS** — nothing to install. Uses the built-in Seatbelt framework. You're ready.
- **Windows** — you must run Claude Code **inside a WSL2 distribution**. WSL1 does not work (bubblewrap needs kernel features only WSL2 has). Check with `wsl -l -v` in PowerShell. Inside the distro: `sudo apt-get install bubblewrap socat`.
- **Linux** — `sudo apt-get install bubblewrap socat` (or `sudo dnf install bubblewrap socat`).

> **On Ubuntu 24.04+ (including under WSL2):** run `sysctl kernel.apparmor_restrict_unprivileged_userns`. If it returns `1`, AppArmor blocks bubblewrap from creating user namespaces and you need an AppArmor profile for `bwrap` — the sandboxing docs have the exact profile. If the key doesn't exist or returns `0`, skip this.

**If you are on native Windows without WSL2, stop here.** There is no sandbox, and the rest of this document cannot give you what you're asking for. Tell the facilitator before the session — the options are WSL2, a container/VM, or running Phase 0 without the guarantee.

Verify availability before you trust anything: start Claude Code and run `/sandbox`. If the panel shows **only a Dependencies tab**, something is missing — install it, restart Claude Code (the dependency check runs at startup), and re-run.

---

## Part 3 — The configuration

Two files. Create both **before** you paste Doc 02 into Claude Code, by hand, so that Claude is confined from its very first tool call rather than after it has already built half your vault.

### 3a — Project settings: `<YOUR_VAULT>/.claude/settings.json`

**This file must live in your vault**, not in `~/.claude/`. That is load-bearing, not stylistic. The `.` path resolves to the project root **only** when the config lives in project settings. Docs, verbatim:

> "The `.` in `allowRead` resolves to the project root because this configuration lives in project settings. If you placed the same configuration in `~/.claude/settings.json`, `.` would resolve to `~/.claude` instead, and project files would remain blocked by the `denyRead` rule."

```json
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false,
    "filesystem": {
      "denyRead": ["~/"],
      "allowRead": [".", "~/.claude"],
      "allowWrite": []
    },
    "network": {
      "allowedDomains": [
        "github.com",
        "api.github.com",
        "codeload.github.com",
        "registry.npmjs.org",
        "pypi.org",
        "files.pythonhosted.org"
      ]
    }
  }
}
```

Line by line, because you should not accept any of these on my word:

- **`denyRead: ["~/"]` + `allowRead: ["."]`** — the default sandbox read policy is **read access to your entire computer**. Enabling the sandbox alone does *not* restrict reads. This pair is the documented pattern for inverting that to deny-by-default: block all of `$HOME`, then re-allow the project root. Note the asymmetry with permission rules — sandbox `allowRead` **can** re-allow inside a `denyRead` region; permission deny rules **cannot** carry exceptions. Different systems, different semantics.
- **`allowRead` includes `~/.claude`** — **this line is required, and it was found the hard way.** With `denyRead: ["~/"]` + `allowRead: ["."]` alone, `~/.claude/` is blocked — and **Doc 03 lives there**. Roughly **12 commands fail**: the `curl -o ~/.claude/skills/...` installs, five `head` verifications, the router test, the plugins `ls`. Without this entry the sandbox looks like it works right up until Block 3, then breaks the whole skills install. Verified safe: Claude Code **auto-denies writes to `settings.json` at every scope**, so a sandboxed command still cannot rewrite its own policy even with this read allowance.
- **`allowWrite: []`** — writes already default to the working directory + the session temp dir. Empty means we add nothing to that.
- **`failIfUnavailable: true`** — **this is the setting your request actually depends on.** By default, if the sandbox can't start (missing dependency, unsupported platform), Claude Code *prints a warning and runs your commands unsandboxed anyway*. That's a silent downgrade from "confined" to "not confined." This makes it a hard failure instead. Without this line, none of the above is a guarantee.
- **`allowUnsandboxedCommands: false`** — the "strict sandbox mode" toggle. By default, when a command fails on a sandbox restriction, Claude may retry it with `dangerouslyDisableSandbox`, which runs it outside the boundary (subject to a permission prompt). This makes that parameter **completely ignored**. Note the tradeoff: some tools genuinely don't work sandboxed (`docker`, `watchman`/`jest`, and Go-based CLIs like `gh` can fail TLS verification under Seatbelt on macOS). With this off, they fail instead of escaping. That is the trade you're asking for. If `gh` breaks, use HTTPS + a PAT — Phase 0 already treats `gh` as optional with fallbacks.
- **`network.allowedDomains`** — no domains are pre-allowed by default; the first hit on a new domain prompts you. This list pre-approves only what Phase 0 needs (GitHub, npm, PyPI) so you aren't click-fatigued into approving something you didn't read. Everything else still prompts. Keep it narrow — a broad entry here is the exfiltration path the docs warn about.

Two things you get for free, worth knowing: the sandbox **automatically denies writes to Claude Code's own `settings.json` at every scope**, so a sandboxed command cannot rewrite its own policy. And **subagents inherit the parent session's sandbox config** — they run in the same process, so there's no bypass there.

> **`sandbox.credentials` (optional, needs Claude Code v2.1.187+).** Check with `claude --version`. This block explicitly denies credential files and unsets secret env vars for sandboxed commands. Our `denyRead: ["~/"]` already covers files under `$HOME`, and this adds the environment-variable half:
> ```json
> "credentials": {
>   "files": [
>     { "path": "~/.aws/credentials", "mode": "deny" },
>     { "path": "~/.ssh", "mode": "deny" }
>   ],
>   "envVars": [
>     { "name": "GITHUB_TOKEN", "mode": "deny" },
>     { "name": "AWS_SECRET_ACCESS_KEY", "mode": "deny" }
>   ]
> }
> ```
> There is no built-in credential deny list — only what you list is restricted.

### 3b — Global settings: `~/.claude/settings.json`

This covers the built-in file tools, which the sandbox does not. **This replaces the permissions block in Doc 02's STEP 3 — do not also apply that one.**

> **Note (2026-08-19):** Doc 02's STEP 3 has since been hardened to the same `allow` list you see
> below, so the two no longer disagree on that half. What this block still adds on top is the
> **targeted `deny` list** (crown-jewel paths) — that part is unique to the sandbox variant.

```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(ls *)",
      "Bash(mkdir *)",
      "Bash(cat *)",
      "Bash(head *)",
      "Bash(wc *)",
      "Glob",
      "Grep"
    ],
    "deny": [
      "Read(~/.ssh/**)",
      "Read(~/.aws/**)",
      "Read(~/.gnupg/**)",
      "Read(~/.config/gh/**)",
      "Read(~/Library/Keychains/**)",
      "Read(**/.env)",
      "Read(**/*.pem)",
      "Read(**/*.key)"
    ]
  },
  "hooks": {
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "afplay /System/Library/Sounds/Blow.aiff" }
        ]
      }
    ]
  }
}
```

What changed from the standard Phase 0 config, and why each change is deliberate:

- **`Bash(python3 *)` and `Bash(pip install *)` removed from `allow`.** This is the single most important edit. Pre-approving Python means pre-approving "read or write any file, unconstrained by any permission rule." With the sandbox on, Python is kernel-confined to your vault anyway — but there is no reason to *also* hand it a blanket pre-approval, and if the sandbox ever fails to load you want the prompt. (`failIfUnavailable: true` should make that impossible. Belt and braces.)
- **Bare `Read`, `Write`, `Edit` removed from `allow`.** A bare tool name in `allow` pre-approves that tool for **any** input — including paths outside your vault. Removing them restores the real default: *"By default, Claude has access to files in the directory where you launched it."* Launch from the vault, and the vault is the scope. This is a case where deleting three lines buys more than adding ten.
- **Targeted `deny` entries, not a broad one.** Note what is deliberately **absent**: there is no `Read(~/Documents/**)` or `Read(//**)`. Your vault lives under `~/Documents`, and permission deny rules take precedence over allow rules with **no possible exception** — a broad deny like that would silently lock Claude out of the very vault you're trying to give it. These entries are narrow on purpose. The broad boundary is the sandbox's job; this list is for the built-in tools' crown jewels.
- **Sound hook is macOS-only.** On Windows Git Bash/WSL use `powershell.exe -c "[console]::beep(1000,400)"`; on Linux `paplay /usr/share/sounds/freedesktop/stereo/bell.oga`. If unsure, delete the whole `"Stop"` block — it's a convenience, and a wrong command here fails on every single turn.

**Also check `additionalDirectories`.** If that key exists in any settings file, whatever it lists is added to Claude's built-in-tool scope. It should be absent or empty. Same for the `--add-dir` flag and the `/add-dir` command — don't use them.

### 3c — Where the code repo goes (decide before Step 6)

Phase 0 as designed puts your git repo in **`~/dev/<repo-name>`, outside the vault**, on the reasoning that a nested `.git` fights Obsidian sync. That collides with a vault-only boundary: with `allowRead: ["."]`, Bash cannot see `~/dev` at all, and `git` won't work there.

Pick one before the session:

- **(A) Repo inside the vault** — e.g. `<vault>/dev/<repo-name>/`. One boundary, nothing to widen, the config above works unchanged. Cost: you should add `dev/` to Obsidian's *Settings → Files and links → Excluded files* so it stays out of search and sync.
- **(B) Repo in `~/dev`, named explicitly** — keep Phase 0's layout and add exactly one path to the sandbox:
  ```json
  "filesystem": {
    "denyRead": ["~/"],
    "allowRead": [".", "~/dev/<repo-name>"],
    "allowWrite": ["~/dev/<repo-name>"]
  }
  ```
  Two boundaries instead of one, but both are named, auditable, and still exclude the rest of the machine.

Either satisfies "not my whole computer." **(A) is the stricter reading of your request and the one I'd default to**; (B) preserves the kit's layout. Your call — tell the facilitator which, at the start of the session.

---

## Part 4 — Verify it yourself

Do not take Part 1 on faith. These are the tests that distinguish a real boundary from a config file that looks reassuring. Run them **before** pasting Doc 02.

**1. Confirm the sandbox actually loaded.** In Claude Code, run `/sandbox` and open the **Config** tab. It shows the *resolved* settings — what's actually in effect after all scopes merge, not what you typed. Confirm `enabled: true` and your filesystem rules are there. Confirm the panel is not showing a Dependencies tab.

**2. Plant a canary outside the vault.** In a normal terminal, not through Claude:

```bash
mkdir -p ~/canary && echo "CANARY-SHOULD-NEVER-BE-READ" > ~/canary/secret.txt
```

**3. The test that matters.** Ask Claude, in the vault session:

> Run this exact command and show me the raw output, including any error: `python3 -c "print(open('/Users/YOURNAME/canary/secret.txt').read())"`

**This is the whole ballgame.** It must fail with a filesystem/permission error from the OS. If it prints `CANARY-SHOULD-NEVER-BE-READ`, your sandbox is not active — stop and fix it before continuing. This test is specifically constructed to bypass permission rules (it's a subprocess doing its own file I/O), so **only** a working kernel sandbox stops it. A config that passes step 1 but fails this one is the exact failure mode this document exists to prevent.

**4. Test the built-in tool layer.** Ask Claude:

> Read the file ~/canary/secret.txt

It should not silently read it. Then ask it to read `~/.ssh/id_rsa` (whether or not it exists) — the deny rule should block that outright.

**5. Test the network boundary.** Ask Claude:

> Run: `curl -sS -o /dev/null -w "%{http_code}" https://example.com`

Not in `allowedDomains`, so it should be blocked or prompt — never silently succeed.

**6. Confirm the write boundary.** Ask Claude:

> Run: `touch ~/canary/written-by-claude.txt`

Must fail. Writes are confined to the working directory and the session temp dir.

**7. Clean up.** `rm -rf ~/canary`

If any of 3, 5, or 6 succeeds, the boundary is not what you think it is. Say so out loud in the session rather than proceeding — a config that silently didn't apply is worse than no config, because you'd be trusting it.

---

## Part 4.5 — git under the sandbox (read this before session day)

**Expect this, it is not a misconfiguration:** under the sandbox, **Claude cannot run `git` for you.**
The harness pattern-protects `.git/` state files — `config`, `HEAD`, `refs` — because git hooks and
`git config` are a documented escape vector (a hook is just a script git will run for you). This was
verified with isolated probes on a real machine during a live session. `Bash(git *)` sitting in your
`allow` list does not change it: the sandbox is a kernel-level boundary, and the permission list is a
different system that cannot override it.

**What to do about it — and why the workaround is better than the thing it replaces:**

> **Claude creates and edits the files. You run git yourself.**
>
> ```bash
> git add -A && git commit -m "..."     # you type this
> ```
>
> This came out of a live session, and it turned into better pedagogy than the original design:
> **the commit becomes your act of approval.** Nothing enters your history that you didn't look at
> and sign off on. For a participant who asked for a sandbox in the first place, that is the whole
> point rather than a tax.

**If the friction outweighs the benefit** (you're committing constantly and it's breaking your flow),
the escape hatch is the sandbox's **Excluded Commands** setting for `git`, which drops git back to
ordinary permission prompts instead of a hard block. That is a real loosening of the boundary — make
it a deliberate Week-1 decision, not a session-day reflex.

**One honest note on the PAT path.** If you authenticate with a Personal Access Token, it ends up in
plaintext under `~/.claude`. That is true with or without the sandbox; it is worth knowing, and it is
your call. If it bothers you, use Git Credential Manager instead, which stores it in the OS keychain.

---

## Part 5 — What changes in Doc 02

Run Doc 02 normally, with these overrides:

| Doc 02 step | Change |
|---|---|
| **Before pasting** | `cd` into your vault. Confirm with `pwd`. The working directory *is* the boundary — if you launch Claude from anywhere else, the built-in-tool scope follows you there and `.` resolves somewhere else entirely. |
| **STEP 3 — permissions block** | **Skip it.** Already done in Part 3b, deliberately different. Do not let Claude overwrite it. |
| **STEP 3 — global router** | Run normally. If you chose option (A) in Part 3c, tell Claude to change router rule 3 to point at `<vault>/dev/` instead of `~/dev/`. |
| **STEP 3.5 — hooks** | Run normally, but read both hook commands before they're written. They're the part of the setup that isn't sandbox-constrained. `jq` must be installed (Doc 01 Step 5.5). |
| **STEP 6 — create the repo** | Use whichever location you picked in Part 3c. |
| **If `gh` fails** | Likely the Seatbelt/TLS issue with Go-based CLIs. Expected under strict mode. Use HTTPS + a PAT — Phase 0 treats `gh` as optional with documented fallbacks. |

**On "you feed in the content":** worth being precise about what that does and doesn't mean. Copying a file into your vault brings it fully inside the boundary — Claude reads it, and so does anything Bash runs. The boundary is a *perimeter*, not a per-file policy: there is no "Claude may see this file but not that one" inside the vault. So the vault is your review gate. If something shouldn't be seen, it doesn't go in the folder. That's the whole model, and it's a good one *because* it's simple enough to hold in your head.

---

## Part 6 — If this isn't strong enough

Everything above is honest about being two mechanisms rather than one, and about the built-in file tools being application-enforced rather than kernel-enforced. If that gap matters to you, the built-in sandbox is the wrong tool and you want a boundary around the **entire Claude Code process**:

- **Dev container / container** — Claude Code runs inside; the container is the boundary; every tool including Read/Edit/Write is confined by it. See the official `devcontainer` docs.
- **VM** — strongest, heaviest.
- **`@anthropic-ai/sandbox-runtime`** — the same OS primitives as a standalone package, used to wrap the whole process.

For Phase 0 specifically, the config in Part 3 is the right proportion: it closes the real hole (arbitrary subprocesses reading your whole disk), it's verifiable in five minutes with Part 4, and it doesn't turn a 90-minute onboarding into an infrastructure project. Worth knowing the ladder exists, though, and where you are on it.

---

## Sources

Every quote and setting above is from the official Claude Code documentation, retrieved 2026-07-15:

- `https://code.claude.com/docs/en/sandboxing.md` — sandbox scope, filesystem/network config, platform support, limitations
- `https://code.claude.com/docs/en/permissions.md` — rule precedence, path patterns, the subprocess caveat, working-directory default
- `https://code.claude.com/docs/en/settings.md` — full settings reference

Where the docs don't state something (hook sandboxing), this document says so rather than guessing.
