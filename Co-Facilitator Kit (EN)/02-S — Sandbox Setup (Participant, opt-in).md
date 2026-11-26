---
title: "Sandbox Setup (Participant) — AI Acceleration Club Phase 0"
created: 2026-07-15
category: reference
tags: [aiac, phase0, co-facilitator-kit, participant, sandbox, security]
---

**Supports:** Run this BEFORE Doc 02. Adds a kernel sandbox and a `deny` list on top of Doc 02's STEP 3 permissions block.

# Sandbox Setup — Confining Claude Code to Your Vault

This document is for a participant who wants a **verifiable** boundary around Claude Code, not a promise of one. It is written for someone technical. It does not simplify, and it does not oversell.

Read Part 1 before you run anything. It tells you what you are actually getting — including what you are **not** getting. If Part 1's guarantees aren't strong enough for you, Part 6 tells you what to do instead.

> **On every permission prompt, choose plain "Yes" (or "No") — never "Yes, and don't ask again".**
> The "don't ask again" option saves a lasting rule in your settings that lets that command run
> without asking from then on, and the status check will then report it.

---

## Part 1 — What this actually guarantees

The honest claim first, because the marketing version of this is wrong.

**Claude Code does not run "inside a sandbox."** There is no single boundary around the process. There are two different enforcement mechanisms covering two different sets of tools, and they have very different strengths:

| What runs | Enforced by | Strength |
|---|---|---|
| **Bash commands + every child process they spawn** (including `python`, `node`, `git`, any script) | The OS kernel — Seatbelt on macOS, bubblewrap on Linux/WSL2 | **Hard.** Enforced on the running process. Holds regardless of what the model decided to run, and even if an allowed command does more than its name suggests. |
| **Claude's built-in file tools** — Read, Edit, Write, Glob, Grep | Claude Code's permission system, in-process, evaluated *before* the tool runs | **Application-level.** Deny rules are absolute (first match wins, no exceptions possible), but this is Claude Code enforcing rules on itself, not the kernel enforcing them on a process. |

From the official docs (quoted from the live pages as of 2026-11-25):

> "The sandbox covers shell commands only. Claude's file tools, MCP servers, and hooks run outside it."

and

> "**Built-in file and web tools**: tools such as Read, Edit, Write, WebFetch, and WebSearch follow permission rules instead. A `denyRead` entry doesn't stop the Read tool, and `allowedDomains` doesn't limit WebFetch"

So the accurate sentence, for the configuration below, is:

- **Everything Claude executes through Bash** (and every child process) is kernel-confined: it can
  **write** only to the working folder (your vault), the session's temp folder and the one code repo you
  name in Part 3c; it can **read** your vault, that repo and `~/.claude` (Claude Code's own config, skills
  and plugins), but **nothing else inside your home folder** — and not Claude Code's login file `~/.claude/.credentials.json` (where Linux and WSL2
  keep your sign-in token), which Part 3a denies again so no command can read it and send it to an
  allowed domain such as `github.com`. Paths outside your home folder (system folders such as `/usr` or `/etc`) stay readable —
  the deny rule covers `~/`, not the whole disk.
- **Everything Claude reads or writes with its built-in file tools** is governed by permission rules
  that Claude Code evaluates before acting: the vault by default, a prompt for anything else, and a hard
  block for the `deny` list.
- **Outside both layers:** hooks and MCP servers (details below).

Both layers are configured below. Neither is decorative, and neither is a VM.

### Why the Bash layer is the one that matters

This is the part worth understanding, because it's the reason the standard AIAC config is not sufficient for you.

Permission rules like `Read(~/.ssh/**)` in a deny list work on Claude's own file tools and on file commands Claude Code recognizes in Bash (`cat`, `head`, `tail`, `sed`). They **do not** work on arbitrary subprocesses. Docs (live page as of 2026-11-25):

> "They also don't apply to arbitrary subprocesses that read or write files indirectly, like a Python or Node script that opens files itself. For OS-level enforcement on sandboxed shell commands, enable the sandbox and turn off the unsandboxed retry."

Earlier versions of the Phase 0 config pre-approved unrestricted Python execution and had an **empty deny list**. With that combination, a one-line Python script reads anything on the machine, and no permission rule can stop it. Doc 02 no longer pre-approves any interpreter, so outside the sandbox Claude has to ask before running one — but once you approve a script, permission rules still can't see what it opens. Any deny list on its own is theater against a subprocess. The sandbox is what closes that hole — and it closes it at the kernel, which is why it holds even if the model is confused, wrong, or manipulated by something it read.

### What this does NOT protect against

Stated plainly so you can decide for yourself:

- **The network layer does not inspect TLS.** The built-in proxy allows or blocks by the hostname the client claims. Docs warn that broad allowlists "can create paths for data exfiltration" via domain fronting. Our config allowlists narrowly.
- **Hooks are not sandboxed.** Treat every hook as running with your full user permissions. They matter here because Doc 02 Step 3.5 installs three (the statusline script and two hooks) — shell commands *you* install and can read in full before they ever run, so they are inside your trust boundary by inspection, not by enforcement.
- **MCP servers and connectors are not sandboxed.** Permission rules apply to their tools; the sandbox does not confine the server process.
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

Two files. Create both **before** you give Doc 02 to Claude Code, by hand, so that Claude is confined from its very first tool call rather than after it has already built half your vault.

### 3a — Project settings: `<YOUR_VAULT>/.claude/settings.json`

**This file must live in your vault**, not in `~/.claude/`. That is load-bearing, not stylistic. The `.` path resolves to the project root **only** when the config lives in project settings. Docs (live page as of 2026-11-25):

> "Place it in your project's `.claude/settings.json`, because the relative path `.` resolves to the project root when the configuration lives in project settings" … "If you placed the same configuration in `~/.claude/settings.json`, `.` would resolve to `~/.claude` instead, and project files would remain blocked by the `denyRead` rule."

```json
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false,
    "filesystem": {
      "denyRead": ["~/", "~/.claude/.credentials.json"],
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
- **`allowRead` includes `~/.claude`** — without it, sandboxed commands can't even read Claude Code's own config (`claude plugin list`, the skills check in Doc 03 Step 2.7c, the router check all fail). Be clear about what it means: **anything Bash runs can read `~/.claude`** — your global `CLAUDE.md`, settings, skills, plugin files, and session transcripts (everything except the login file, next bullet). And it is **read only**: it does **not** make `~/.claude` writable, so installs into `~/.claude` still fail under the sandbox (Part 3d). Claude Code also **auto-denies writes to `settings.json` at every scope**, so a sandboxed command cannot rewrite its own policy.
- **`denyRead` also lists `~/.claude/.credentials.json`** — on Linux and WSL2, Claude Code keeps your sign-in token in that file (on macOS it lives in the Keychain, so the entry simply matches nothing there). `allowRead` re-opens all of `~/.claude`, and `github.com` is an allowed domain; the docs warn: "Allowing broad domains such as `github.com` can create paths for data exfiltration." When read rules overlap, the narrower path wins — docs: "The deny holds inside a wider allow, so a broad allow can't silently re-expose a secret." So this one entry keeps the token away from every sandboxed command, while the rest of `~/.claude` stays readable.
- **`allowWrite: []`** — writes already default to the working directory + the session temp dir. Empty means we add nothing to that.
- **`failIfUnavailable: true`** — **this is the setting your request actually depends on.** By default, if the sandbox can't start (missing dependency, unsupported platform), Claude Code *prints a warning and runs your commands unsandboxed anyway*. That's a silent downgrade from "confined" to "not confined." This makes it a hard failure instead. Without this line, none of the above is a guarantee.
- **`allowUnsandboxedCommands: false`** — the "strict sandbox mode" toggle. By default, when a command fails on a sandbox restriction, Claude may retry it with `dangerouslyDisableSandbox`, which runs it outside the boundary (subject to a permission prompt). This makes that parameter **completely ignored**. Note the tradeoff: some tools genuinely don't work sandboxed (`docker`, `watchman`/`jest`, and Go-based CLIs like `gh` can fail TLS verification under Seatbelt on macOS). With this off, they fail instead of escaping. That is the trade you're asking for. If `gh` breaks, run the `gh` steps yourself in a normal terminal (Part 5) — never fall back to a classic personal access token.
- **`network.allowedDomains`** — no domains are pre-allowed by default; the first hit on a new domain prompts you. This list pre-approves only what Phase 0 needs (GitHub, npm, PyPI) so you aren't click-fatigued into approving something you didn't read. Everything else still prompts. Keep it narrow — a broad entry here is the exfiltration path the docs warn about.

**Keep it exactly like this — in every settings file.** Claude Code merges the sandbox's path and domain
lists from every settings file it loads (your vault's `.claude/settings.json` and `.claude/settings.local.json`,
where `/sandbox` saves its choices, your global `~/.claude/settings.json`, and any policy your organization
installs), and a later file can switch a setting off. So the boundary is only as narrow as all of them
together. The status check (`--sandbox`) reads every one of those files and reports this part `NOT DONE`
— never `DONE` — when, together, they:

- allow a domain that isn't one of the six above (a saved `WebFetch(domain:…)` approval counts too),
  or leave one out;
- make anything readable or writable beyond the vault, `~/.claude` and the one repo from Part 3c — including
  `Read`/`Edit`/`Write` allow rules and `additionalDirectories`, whose paths are added to the sandbox;
- turn one of the three switches above the other way;
- list `excludedCommands` (those run **outside** the sandbox, with your full access);
- set `filesystem.disabled` (it turns filesystem isolation off while keeping the network filter — user and
  managed settings can set it, project settings can't), or any other loosening switch: weaker nested or
  network isolation, Apple Events, nested user namespaces, Unix sockets, Mach lookups, local port binding or
  a custom proxy ([sandboxing docs](https://code.claude.com/docs/en/sandboxing)).

If a settings or policy file exists but can't be read, the check says "unverified" and reports `NOT DONE`.
It can't see settings passed with `--settings` or pushed by an MDM profile: `/sandbox` → **Config** (Part 4,
step 1) shows the resolved result and is the final word.

Two things you get for free, worth knowing: the sandbox **automatically denies writes to Claude Code's own `settings.json` at every scope**, so a sandboxed command cannot rewrite its own policy. And **subagents inherit the parent session's sandbox config** — they run in the same process, so there's no bypass there.

> **`sandbox.credentials` (optional; see the [sandboxing docs](https://code.claude.com/docs/en/sandboxing) for the current details).** This block explicitly denies credential files and unsets secret env vars for sandboxed commands. Our `denyRead: ["~/"]` already covers files under `$HOME`, and this adds the environment-variable half:
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

This covers the built-in file tools, which the sandbox does not. The `allow` and `ask` lists are **the same as Doc 02's STEP 3**; what this block adds is the **targeted `deny` list** (crown-jewel paths, below). Use it instead of Doc 02's block — and like Doc 02, **merge it into your existing `~/.claude/settings.json` without displaying it** (that file can hold API keys): back the file up, save the block, and run the merge script from this section in a **normal terminal**.

```json
{
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Bash(git status --short)",
      "Bash(git diff)",
      "Bash(git log --oneline)",
      "Bash(git remote -v)",
      "Bash(ls *)",
      "Bash(wc *)"
    ],
    "ask": [
      "Bash(cat *)",
      "Bash(head *)",
      "Bash(tail *)",
      "Bash(grep *)",
      "Bash(diff *)",
      "Bash(sed *)",
      "Bash(sort *)",
      "Bash(git show *)",
      "Bash(git -C *)",
      "Bash(git -c *)",
      "Bash(git add *)",
      "Bash(git commit *)",
      "Bash(git push *)",
      "Bash(gh repo create *)"
    ],
    "deny": [
      "Read(~/.ssh/**)",
      "Read(~/.aws/**)",
      "Read(~/.gnupg/**)",
      "Read(~/.config/gh/**)",
      "Read(~/Library/Keychains/**)",
      "Read(~/.claude/.credentials.json)",
      "Read(~/**/.env)",
      "Read(~/**/*.pem)",
      "Read(~/**/*.key)"
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

#### Canonical deny list

This is the complete list. Every entry is required — the status check (`--sandbox`) marks this part
`NOT DONE` if any one of them is missing from `permissions.deny`:

```text
Read(~/.ssh/**)
Read(~/.aws/**)
Read(~/.gnupg/**)
Read(~/.config/gh/**)
Read(~/Library/Keychains/**)
Read(~/.claude/.credentials.json)
Read(~/**/.env)
Read(~/**/*.pem)
Read(~/**/*.key)
```

`Read(~/.claude/.credentials.json)` is the built-in tools' half of the login-file protection in Part 3a
(the sandbox entry covers Bash; this one covers Claude's Read tool).

Every path is anchored at your home folder (`~/`). That is deliberate: in Claude Code's path syntax a
pattern with no prefix, such as `**/*.key`, is relative to the folder Claude was started in, so it would
miss a key file anywhere outside the vault ([path patterns](https://code.claude.com/docs/en/permissions)).
`~/**/*.key` covers your whole home folder, vault included. Deny rules block Claude's file tools and the
file commands Claude Code recognizes in Bash (`cat`, `head`, `tail`, `sed`), not arbitrary scripts —
that part is the sandbox's job.

**Merge it without reading your existing file.** In a normal terminal:

```bash
mkdir -p ~/.claude
```

Then save the JSON block above as `~/.claude/aiac-02s-block.json` (edit the `Stop` line first — see
below), save the script below as `~/.claude/aiac-merge-settings.py` (it is the same script Doc 02 Step 3
uses), and run `python3 ~/.claude/aiac-merge-settings.py ~/.claude/aiac-02s-block.json`. It adds each
missing entry, keeps every key and rule you already had, prints only the kit's entries and the *names*
of keys it left alone, and its last line must start with `Verified:`. Before it changes anything it saves a
private backup of your current file (of the real file, if `settings.json` is a symlink) and prints its
name: `~/.claude/settings.json.bak` the first time, the next free `settings.json.bak.1`, `.bak.2`, … if
an earlier backup exists (an earlier backup is never overwritten). Use the backup file the script names.

```python
# aiac-merge-settings.py - merges the AIAC kit's entries into ~/.claude/settings.json.
# It never prints existing values: only the kit entries it added and the names
# of keys you already had. Usage: python3 aiac-merge-settings.py [--replace KEY] - < block
import json
import os
import re
import shutil
import sys

TARGET = os.path.expanduser("~/.claude/settings.json")
BACKUP = TARGET + ".bak"
DEEP = ("permissions", "hooks", "env")  # top-level objects merged key by key
HOOK_EVENTS = ("Stop", "UserPromptSubmit", "PreCompact")


def stop(message):
    sys.exit("STOP: " + message + " Nothing was changed.")


def number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0


def hook_groups(v):
    return isinstance(v, list) and all(
        isinstance(g, dict) and set(g) <= {"matcher", "hooks"}
        and isinstance(g.get("matcher", ""), str)
        and isinstance(g.get("hooks"), list) and len(g["hooks"]) > 0
        and all(isinstance(h, dict) and set(h) <= {"type", "command", "timeout"}
                and h.get("type") == "command"
                and isinstance(h.get("command"), str) and h["command"] != ""
                and ("timeout" not in h or number(h["timeout"]))
                for h in g["hooks"])
        for g in v)


# The only shapes a kit block may have. Checked before anything is merged,
# whether or not your settings already have the key.
SCHEMA = {
    "permissions": lambda v: isinstance(v, dict) and set(v) <= {"allow", "ask", "deny"}
    and all(isinstance(x, list) and all(isinstance(r, str) for r in x) for x in v.values()),
    "hooks": lambda v: isinstance(v, dict) and set(v) <= set(HOOK_EVENTS)
    and all(hook_groups(x) for x in v.values()),
    "env": lambda v: isinstance(v, dict) and all(isinstance(x, str) for x in v.values()),
    "statusLine": lambda v: isinstance(v, dict) and set(v) <= {"type", "command", "padding"}
    and v.get("type") == "command" and isinstance(v.get("command"), str) and v["command"] != ""
    and ("padding" not in v or (isinstance(v["padding"], int) and not isinstance(v["padding"], bool))),
}


def check_block(block):
    for key, val in block.items():
        name = key if re.match(r"^[A-Za-z][A-Za-z0-9_]{0,40}$", key) else "a key"
        if key not in SCHEMA:
            stop("the kit block has an entry the kit never uses (" + name + "); check it was copied whole.")
        if not SCHEMA[key](val):
            stop("the kit block's " + name + " entry has the wrong shape; check it was copied whole.")


def merge(dst, new, path, added, kept):
    for key, val in new.items():
        name = ".".join(path + [key])
        deep = isinstance(val, dict) and (path or key in DEEP)
        if key not in dst:
            dst[key] = val
            added.append(name)
        elif (isinstance(val, list) or deep) and type(dst[key]) is not type(val):
            stop(name + " in your settings is not a JSON " +
                 ("list" if isinstance(val, list) else "object") + ", so the kit entries can't be added.")
        elif isinstance(val, list):
            for item in val:
                if item not in dst[key]:
                    dst[key].append(item)
                    added.append(name + ": " + (item if isinstance(item, str) else "1 entry"))
        elif deep:
            merge(dst[key], val, path + [key], added, kept)
        elif dst[key] != val:
            kept.append(name)


def missing(dst, new, path, kept):
    gaps = []
    for key, val in new.items():
        name = ".".join(path + [key])
        if name in kept:
            continue
        if key not in dst:
            gaps.append(name)
        elif isinstance(val, list) and isinstance(dst[key], list):
            gaps += [name for item in val if item not in dst[key]]
        elif isinstance(val, dict) and isinstance(dst[key], dict) and (path or key in DEEP):
            gaps += missing(dst[key], val, path + [key], kept)
    return gaps


def replace(dst, new, dotted):
    keys = dotted.split(".")
    for key in keys[:-1]:
        new = new[key]
        if not isinstance(dst.get(key), dict):
            dst[key] = {}
        dst = dst[key]
    dst[keys[-1]] = new[keys[-1]]


def backup(real):
    """A private copy (0600) of the file's current bytes - the file a symlink
    points at, never the link - made once per run, before the change. An
    earlier backup is never overwritten: the copy goes to the first free name
    (settings.json.bak, then settings.json.bak.1, .bak.2, ...), printed below."""
    name, n = BACKUP, 0
    while os.path.lexists(name):
        n += 1
        name = BACKUP + "." + str(n)
    with open(real, "rb") as f:
        data = f.read()
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    return name


def main():
    args, to_replace = sys.argv[1:], []
    while len(args) >= 2 and args[0] == "--replace":
        to_replace.append(args[1])
        args = args[2:]
    try:
        if args and args[0] != "-":
            with open(args[0], encoding="utf-8") as f:
                block = json.load(f)
        else:
            block = json.load(sys.stdin)
    except (OSError, ValueError):
        stop("the kit block could not be read as JSON (check it was copied whole).")
    if not isinstance(block, dict):
        stop("the kit block is not a JSON object.")
    check_block(block)
    # Write through a symlinked settings.json to the file it points at.
    real = os.path.realpath(TARGET)
    current = {}
    if os.path.exists(real):
        try:
            with open(real, encoding="utf-8") as f:
                current = json.load(f)
        except ValueError:
            stop("~/.claude/settings.json is not valid JSON.")
        if not isinstance(current, dict):
            stop("~/.claude/settings.json is not a JSON object.")
    added, kept = [], []
    for dotted in to_replace:
        try:
            replace(current, block, dotted)
        except (KeyError, TypeError):
            stop(dotted + " is not in the kit block.")
        added.append(dotted + " (replaced, as you asked)")
    merge(current, block, [], added, kept)
    kept = [k for k in kept if not any(r.startswith(k + ".") for r in to_replace)]
    saved = None
    if added or not os.path.exists(real):
        os.makedirs(os.path.dirname(real), exist_ok=True)
        if os.path.exists(real):
            try:
                saved = backup(real)
            except OSError:
                stop("could not save a backup of ~/.claude/settings.json first.")
        tmp = real + ".aiac-tmp"
        if os.path.lexists(tmp):
            os.unlink(tmp)
        # Created private (0600) from the start, never briefly readable by others.
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2, ensure_ascii=False)
            f.write("\n")
        if os.path.exists(real):
            shutil.copymode(real, tmp)
        os.replace(tmp, real)
    if saved:
        print("backup of your previous settings (private): ~/.claude/" + os.path.basename(saved))
    for name in added:
        print("added: " + name)
    for name in kept:
        print("kept your existing value (not shown): " + name)
    with open(real, encoding="utf-8") as f:
        gaps = missing(json.load(f), block, [], kept)
    if gaps:
        sys.exit("STOP: still missing after the merge: " + ", ".join(gaps))
    print("Verified: settings.json parses and has every kit entry (%d added)." % len(added))


main()
```

Why the list looks like this, and why each choice is deliberate:

- **No interpreter (`python`, `node`…) and no `pip install` in `allow`.** Pre-approving an interpreter means pre-approving "read or write any file, unconstrained by any permission rule." With the sandbox on, scripts are kernel-confined anyway — and in the sandbox's auto-allow mode they run without a prompt at all — but there is no reason to *also* hand them a blanket pre-approval: if the sandbox ever fails to load, the missing allow rule is what brings the prompt back. (`failIfUnavailable: true` should make that impossible. Belt and braces.)
- **No blanket git, no lasting write grants, and `ask` rules for what prints or publishes.** Same reasons as Doc 02: only exact, read-only git commands plus `ls` and `wc` are pre-approved (no wildcards, because options like `--output`, `--ext-diff` or `--template` write files, run programs or plant hooks). `cat`, `head`, `tail`, `grep`, `diff`, `sed`, `sort` and `git show` can print files and are built-in read-only commands that Claude Code runs without a prompt anywhere on disk unless a rule says otherwise, so they sit in `ask`, together with `git -C` / `git -c`, `git add`, `git commit`, `git push` and `gh repo create`. Other read-only commands (for example `git log -p`) still run without asking — Doc 02 Step 3 explains why; under the sandbox they can't read outside the boundary anyway.
- **No bare `Read`, `Write`, `Edit`, `Glob`, `Grep` in `allow`.** A bare tool name in `allow` pre-approves that tool for **any** input — including paths outside your vault. Leaving them out keeps the real default: *"By default, Claude has access to files in the directory where you launched it."* Launch from the vault, and the vault is the scope.
- **Targeted `deny` entries, not a broad one.** Note what is deliberately **absent**: there is no `Read(~/Documents/**)` or `Read(//**)`. Your vault lives in your home folder (`~/AIAC-Vault` by default), and permission deny rules take precedence over allow rules with **no possible exception** — a broad deny like that would silently lock Claude out of the very vault you're trying to give it. These entries are narrow on purpose. The broad boundary is the sandbox's job; this list is for the built-in tools' crown jewels.
- **Sound hook is macOS-only.** On Windows (WSL2) use `powershell.exe -c "[console]::beep(1000,400)"`; on Linux `paplay /usr/share/sounds/freedesktop/stereo/bell.oga`. If unsure, delete the whole `"Stop"` block — it's a convenience, and a wrong command here fails on every single turn.

**Also check `additionalDirectories`.** If that key exists in any settings file, whatever it lists is added to Claude's built-in-tool scope. It should be absent or empty. Same for the `--add-dir` flag and the `/add-dir` command — don't use them.

### 3c — Name the code repo (decide before Step 6)

Phase 0 puts your git repo in **`~/dev/<repo-name>`, outside the vault** — Doc 02 Step 6 creates it there and
checks that it landed there, the router names it there, and Doc 04 and the status check look for it there.
That collides with a vault-only boundary: with `allowRead: ["."]`, Bash cannot see `~/dev` at all.

So name exactly **one** repo — the name you'll use in Doc 02 Step 0 — and add it to the sandbox. Replace the
`"filesystem"` block from 3a with:

```json
"filesystem": {
  "denyRead": ["~/", "~/.claude/.credentials.json"],
  "allowRead": [".", "~/.claude", "~/dev/<repo-name>"],
  "allowWrite": ["~/dev/<repo-name>"]
}
```

Two boundaries instead of one, but both are named, auditable, and still exclude the rest of the machine,
including the rest of `~/dev`. Use the same `<repo-name>` everywhere afterwards: in Doc 02 (Steps 0, 6 and
the router) and in Doc 04. If you later pick a different name, change this entry to match — the status check
reports Part 3a `NOT DONE` when the sandbox names a repo other than the one your router names, or more than
one.

The folder must exist before the sandbox can open it for writing (on Linux and WSL2 an `allowWrite` entry
for a missing path has no effect), and sandboxed commands can't create it, because they can't write to
`~/dev`. So in Doc 02 Step 6 **you** run the creation block in a normal terminal (Part 5), then restart
Claude Code in your vault.

### 3d — Installs into `~/.claude` happen outside the boundary (by design)

Under this sandbox, Bash can read `~/.claude` but **cannot write to it**. A few setup steps write there with a shell command, and they **will fail** in a sandboxed session:

| Step | Why it fails sandboxed |
|---|---|
| Doc 02 Step 3.5 — `chmod +x` on the statusline and hook scripts | changes files in `~/.claude` |
| Doc 02 Step 3.5 — the three settings merges (`aiac-merge-settings.py`) | writes `~/.claude/settings.json`, which sandboxed commands may never write |
| Doc 03 Step 2 and 2.7b — `claude plugin install …` | writes to `~/.claude/plugins/` |
| Doc 03 Step 2.7a — the starter-pack install | writes to `~/.claude/skills/` |

Do those steps from a Claude Code session started **outside the vault** — for example from `~/dev` — where the vault's sandbox config doesn't apply. That is a deliberate, short step outside the boundary for reviewed installs: read each command before you approve it, then go back to your vault session. The skills come from a pinned, public version (`AI-Acceleration/cc-starter-pack` `v1.0.1`), so you can read every file before installing.

---

## Part 4 — Verify it yourself

Do not take Part 1 on faith. These are the tests that distinguish a real boundary from a config file that looks reassuring. Run them **before** you give Doc 02 to Claude.

**1. Confirm the sandbox actually loaded.** In Claude Code, run `/sandbox` and open the **Config** tab. It shows the *resolved* settings — what's actually in effect after all scopes merge, not what you typed. Confirm `enabled: true` and your filesystem rules are there. Confirm the panel is not showing a Dependencies tab.

**2. Plant canaries outside the vault — synthetic files only.** In a **normal terminal** (not through Claude), create a new, uniquely named folder inside your home folder with fake contents. Never use a real key or a real secret for this test:

```bash
CANARY_DIR="$(mktemp -d "$HOME/aiac-canary.XXXXXX")" &&
printf 'CANARY-SHOULD-NEVER-BE-READ\n' > "$CANARY_DIR/secret.txt" &&
printf 'SYNTHETIC-NOT-A-REAL-KEY\n' > "$CANARY_DIR/test.key" &&
ls -la "$CANARY_DIR" && echo "CANARY_DIR=$CANARY_DIR"
```

- The folder is created **inside `$HOME` on purpose**: the sandbox denies reads under `~/`. A folder in the system temp directory would sit outside that rule and prove nothing.
- `ls -la` must list `secret.txt` and `test.key`. **Confirm both exist before you test anything** — a "denied" result on a file that isn't there proves nothing.
- Keep this terminal open: you need the printed `CANARY_DIR=…` path below (written `<CANARY_DIR>`) and for the clean-up.

**3. The test that matters.** Ask Claude, in the vault session (replace `<CANARY_DIR>` with the printed path):

> Run this exact command and show me the raw output, including any error: `python3 -c "print(open('<CANARY_DIR>/secret.txt').read())"`

**This is the whole ballgame.** It must fail with a filesystem/permission error from the OS. If it prints `CANARY-SHOULD-NEVER-BE-READ`, your sandbox is not active — stop and fix it before continuing. This test is specifically constructed to bypass permission rules (it's a subprocess doing its own file I/O), so **only** a working kernel sandbox stops it. A config that passes step 1 but fails this one is the exact failure mode this document exists to prevent. (Whether Claude asks first depends on the mode you picked in `/sandbox`: in auto-allow mode a sandboxed command runs without a prompt; in regular-permissions mode you approve it once. Either way, the read itself must fail.)

**4. Test the built-in tool layer.** Ask Claude:

> Read the file <CANARY_DIR>/secret.txt

It should not silently read it — it's outside the vault, so you get a permission prompt. Decline it. Then ask:

> Read the file <CANARY_DIR>/test.key

The `Read(~/**/*.key)` deny rule must block that outright, with no prompt — the canary folder is inside your home folder, so the home-anchored rule covers it. (This uses the synthetic key from step 2 — never point this test at a real key.)

**5. Test the network boundary.** Ask Claude:

> Run: `curl -sS -o /dev/null -w "%{http_code}" https://example.com`

Not in `allowedDomains`, so it should be blocked or prompt — never silently succeed.

**6. Confirm the write boundary.** Ask Claude:

> Run: `touch <CANARY_DIR>/written-by-claude.txt`

Must fail. Writes are confined to the working directory and the session temp dir.

**7. Clean up only what the test created.** Back in the normal terminal from step 2:

```bash
rm -f "$CANARY_DIR/secret.txt" "$CANARY_DIR/test.key" && rmdir "$CANARY_DIR"
```

If `rmdir` refuses because the folder isn't empty, something else got written there — look at it (`ls -la "$CANARY_DIR"`): a `written-by-claude.txt` means step 6 did **not** hold.

If any of 3, 5, or 6 succeeds, the boundary is not what you think it is. Say so out loud in the session rather than proceeding — a config that silently didn't apply is worse than no config, because you'd be trusting it.

---

## Part 4.5 — git under the sandbox (read this before session day)

**Expect this, it is not a misconfiguration:** under the sandbox, **Claude cannot run `git` for you.**
The harness pattern-protects `.git/` state files — `config`, `HEAD`, `refs` — because git hooks and
`git config` are a documented escape vector (a hook is just a script git will run for you). This was
verified with isolated probes on a real machine during a live session. Git entries in your `allow`
list do not change it: the sandbox is a kernel-level boundary, and the permission list is a different
system that cannot override it.

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
the escape hatch is the sandbox's `excludedCommands` setting for `git`. Be clear what that does: an
excluded command runs **outside the sandbox, with your full access** — no filesystem limits and no
network filter — and only the ordinary permission prompts stay ([sandboxing docs](https://code.claude.com/docs/en/sandboxing)).
That is a real loosening of the boundary, so the status check then reports Part 3a `NOT DONE` — make it a
deliberate Week-1 decision, not a session-day reflex.

**Authentication.** Use `gh auth login --web` (run in a normal terminal) or Git Credential Manager. Don't
create a classic personal access token for this. Know where the credential ends up: `gh` stores its token
in your operating system's credential store (macOS Keychain, Windows Credential Manager, a Linux keyring)
**when one is available**, and otherwise falls back to a plain-text file, `~/.config/gh/hosts.yml` — common
on Linux and WSL2 without a keyring. `gh auth status` shows which one it used. Either way the sandbox's
`denyRead: ["~/"]` keeps sandboxed commands away from `~/.config/gh`, and the Part 3b deny rule
`Read(~/.config/gh/**)` keeps Claude's Read tool away from it. Git Credential Manager uses the operating
system's credential store.

---

## Part 5 — What changes in Doc 02

Run Doc 02 normally, with these overrides:

| Doc 02 step | Change |
|---|---|
| **Before you start Doc 02** | `cd` into your vault. Confirm with `pwd`. The working directory *is* the boundary — if you launch Claude from anywhere else, the built-in-tool scope follows you there and `.` resolves somewhere else entirely. |
| **STEP 3 — permissions block** | **Already done in Part 3b** — same `allow` and `ask` lists plus the `deny` list, merged with the script. Tell Claude to skip the Step 3 merge: under the sandbox the script can't write `~/.claude/settings.json` anyway (Claude Code always denies sandboxed writes to it). |
| **STEP 3 — global router** | Run normally. It names `~/dev/<repo-name>`, the same repo as Part 3c. |
| **STEP 3.5 — hooks** | Read both hook commands and the statusline script before they're written — they run unsandboxed. The `chmod +x` lines and the three settings merges fail sandboxed (they write in `~/.claude`): run them from a session outside the vault (Part 3d). `jq` must be installed (Doc 01 prerequisites). |
| **STEP 6 — create the repo** | Use the repo name from Part 3c. Claude shows you the creation block; **you** run it in a normal terminal (sandboxed commands can't write to `~/dev` or run git — Part 4.5). Then restart Claude Code in your vault, so the Part 3c entry applies to the new folder, and run the verify command there yourself too. |
| **STEP 12 — first push** | Under the sandbox Claude can't run git (Part 4.5). Claude shows you the staged file list and the commands; you check owner, **Private** visibility and files, and run `gh repo create … --private` and `git push` yourself in a normal terminal. |
| **If `gh` fails** | Likely the Seatbelt/TLS issue with Go-based CLIs. Expected under strict mode. Run `gh` yourself in a normal terminal; don't create a classic personal access token. |
| **Doc 03 — plugins and skills** | Install from a session outside the vault (Part 3d). |

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

Every setting above is from the official Claude Code documentation (first retrieved 2026-07-15). The quotes were re-checked against the live pages on 2026-11-25 and are labelled with that date; the pages change, so check them again before you rely on a quote:

- `https://code.claude.com/docs/en/sandboxing.md` — sandbox scope, filesystem/network config, platform support, limitations
- `https://code.claude.com/docs/en/permissions.md` — rule precedence, path patterns, the subprocess caveat, working-directory default
- `https://code.claude.com/docs/en/settings.md` — full settings reference

Where the docs don't state something (hook sandboxing), this document says so rather than guessing.
