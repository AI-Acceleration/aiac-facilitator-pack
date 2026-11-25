# Vocabulary

**For:** participants, before the Phase 0 session. Read it once, about a day before. It takes five minutes.

> **Why:** the session moves fast and you'll hear a handful of technical words. If you already know them, everything flows. You don't need to memorize anything. Read the list once, and anything that still isn't clear we'll cover live.

---

## The map first: how the 3 pieces fit together

Before the individual terms, here is the whole picture. Everything we use comes down to **3 pieces**, and each one has **one** job. Most of the confusion at the start doesn't come from not knowing what a word means. It comes from not seeing how the tools connect. Once you have this picture, the rest of the words fall into place.

```
  +------------------+    +------------------+    +------------------+
  |   CLAUDE CODE    |    |  OBSIDIAN/VAULT  |    |   GIT + GITHUB   |
  |  the one that    |    |  where your      |    |  HISTORY +       |
  |  ACTS            |    |  knowledge LIVES |    |  BACKUP          |
  +------------------+    +------------------+    +------------------+
  | The AI in your   |    | Your notes,      |    | Keeps every      |
  | terminal: reads, |    | projects and     |    | version of your  |
  | writes and runs  |    | briefs. The      |    | code (in ~/dev)  |
  | things on your   |    | source of truth. |    | and backs it up. |
  | files.           |    |                  |    |                  |
  +------------------+    +------------------+    +------------------+
     you work WITH   ->   ...what you know   ->   ...and CODE lives
     Claude Code...       lives in the vault      in ~/dev, with Git
```

**In one sentence:** you work **with** Claude Code. What you know and decide lives in your **vault** (Obsidian). **Code** lives separately, in `~/dev/`, where **Git** keeps its history and **GitHub** backs it up in the cloud. Claude *acts*, the vault *keeps the knowledge*, and Git and GitHub are the *safety net* for code.

**Two places, one rule:** if a folder has its own `.git/`, it's a repo and it goes in `~/dev/`. The repo for your first project will live in `~/dev/<your-project>`, outside the vault, with a link to it from your project brief.

---

## Glossary: the terms, one by one

### Working with Claude

| Term | What it is, in one line |
|---|---|
| **Claude Code** | Claude running in your terminal with access to your files. It reads, writes, runs commands and builds things instead of only chatting. |
| **Prompt** | What you tell Claude: a question, an instruction, or a whole document of instructions. In this kit, long prompts are **loaded by file**: you save the document and tell Claude "Read the file <path> and follow its instructions". |
| **Harness** | The program that runs the AI model and gives it tools (reading files, running commands). Claude Code is a harness. The method in this kit is plain files, so it also works with other harnesses. Claude Code is simply the one we recommend today. |
| **Slash command** | Something you type inside Claude Code starting with `/` to run a skill or a built-in action, like `/session-close` or `/context`. |
| **Plan mode** | A mode where Claude first proposes a plan and waits for your OK before touching anything. Press **Shift+Tab** to switch modes. Use it for any task that isn't trivial. |
| **Context window** | Claude's "working memory" within one session. It's limited: when it fills up, it's time to save and start fresh. A bar at the bottom shows the percentage. |
| **Usage limit** | How much of your Claude plan you've used, measured over a rolling 5-hour window and per week. It's separate from the context window. See Doc 06. |

### Your knowledge system

| Term | What it is, in one line |
|---|---|
| **Vault** | Your Obsidian folder, your "second brain": notes, projects, knowledge. It's the source of truth for what you know and what you're working on. |
| **Obsidian** | The free app you use to read and browse your vault. The notes are plain text files, so they stay yours. |
| **PARA** | How the vault is organized: **P**rojects (things with a finish line), **A**reas (ongoing responsibilities), **R**eference (useful material), **A**rchives (finished or inactive). |
| **GTD** | *Getting Things Done*: a method for capturing everything in one place (your **INBOX**) and then deciding what each item is and what the next action is. |
| **Brief** | The note for one project in your vault: what you want to achieve, the next actions, what you're waiting on from others, and a log. Claude reads it first every time you return to that project. |
| **CLAUDE.md** | The **instructions** file Claude reads automatically when it starts: who you are, how you work and the project's rules. Each correction you make gets saved here, which is how it improves over time. |
| **Router** | The CLAUDE.md in your home folder (`~/.claude/CLAUDE.md`). It sends every new session to your vault's rules, whichever folder you start from, so that "let's work on my project" just works. |

### Extending Claude

| Term | What it is, in one line |
|---|---|
| **Skill** / **SKILL.md** | A packaged procedure Claude follows step by step (for example, closing a session properly). Its file is `SKILL.md`. CLAUDE.md holds rules; a SKILL.md holds one procedure. |
| **Plugin** | A bundle of skills (and sometimes other tools) that you install in one go. Check what's installed by asking Claude to run `claude plugin list`. |
| **Connector** / **MCP** | The standard "plug" that connects Claude to outside services such as email, calendar or a meeting recorder so it can use them. MCP (*Model Context Protocol*) is the technical name. |

### Terminal and code

| Term | What it is, in one line |
|---|---|
| **Terminal** (or console) | The window where you type text commands instead of clicking. On Mac it's "Terminal"; on Windows, Git Bash or PowerShell. |
| **Shell** | The program that interprets what you type in the terminal (bash, zsh and PowerShell are shells). "Terminal" and "shell" are used almost interchangeably. |
| **CLI** | *Command-Line Interface*: a tool you use by typing commands in the terminal. Claude Code is a CLI, and so is `gh`. |
| **Repo** (repository) | A folder of **code** with Git history. It lives in `~/dev/`, **outside** the vault, and the project brief in the vault points to it. Vault = knowledge; repo = code. |
| **Git** | The system that keeps the history of changes to your code, like an unlimited "undo". |
| **GitHub** | The cloud service where Git repos are backed up and shared. Your repos there are **Private** unless you choose otherwise. |
| **`gh`** | GitHub's program for the terminal. Claude uses it to create your repo on GitHub. |
| **commit** | Saving a "snapshot" of your changes in Git's history, with a message saying what you changed. |
| **push** | Uploading your commits to GitHub. **pull** is the reverse: downloading changes from the cloud to your computer. |
| **branch** / **PR** | A *branch* is a parallel line of work, and a *PR* (pull request) proposes merging that branch into the main one. You'll barely touch these in Phase 0. They're here so the words don't sound strange. |

> That's it. Anything that still isn't clear, we'll cover live.
