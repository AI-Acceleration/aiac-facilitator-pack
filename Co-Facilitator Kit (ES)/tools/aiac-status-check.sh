#!/bin/bash
# ---------------------------------------------------------------------------
# ORIGIN: contributed by Mangan (github.com/dibkorma), co-facilitator, 2026-08-18.
# Built while running a 10-student cohort; adopted into the kit 2026-08-19.
# Its first real run flipped a wrong diagnosis: a student everyone believed was
# 19 days behind was actually finished and waiting on us to schedule.
#
# FACILITATOR NOTE: ship this to the student as a .sh.txt twin - WhatsApp and
# Gmail block .sh attachments. The twin is byte-identical and runs the same.
# Keep this file 100% ASCII so it survives copy-paste through any chat app.
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# AI Acceleration Club - Phase 0 Status Check
#
# WHAT THIS IS: a read-only report of how far your Phase 0 setup got.
# It writes nothing, changes nothing, installs nothing, and sends nothing.
# It only looks at files that already exist on your machine and prints a summary.
#
# HOW TO RUN:
#   1. Open your terminal (Ghostty, or the built-in Terminal app).
#   2. Run:   bash ~/Downloads/aiac-status-check.sh
#      (or drag the file into the terminal window after typing "bash ")
#   3. Copy the whole output and send it back.
#
# If your vault is not auto-detected, pass it in:
#   bash ~/Downloads/aiac-status-check.sh "/path/to/your/vault"
#
# WHAT IT PRINTS ABOUT YOU: your vault path, your git name/email, your GitHub
# remote (if any), and which tools are installed. No file contents, no notes,
# no keys. Read the output before you send it if you want to check.
# ---------------------------------------------------------------------------

VERSION="1.1"

OK="[ OK ]"
NO="[ -- ]"
WARN="[WARN]"

pass_count=0
fail_count=0

line() { printf '%s\n' "---------------------------------------------------------------"; }
head1() { printf '\n'; line; printf '%s\n' "$1"; line; }

# say STATUS LABEL [DETAIL]
say() {
  if [ -n "$3" ]; then
    printf '%s %-42s %s\n' "$1" "$2" "$3"
  else
    printf '%s %s\n' "$1" "$2"
  fi
  if [ "$1" = "$OK" ]; then pass_count=$((pass_count+1)); fi
  if [ "$1" = "$NO" ]; then fail_count=$((fail_count+1)); fi
}

have() { command -v "$1" >/dev/null 2>&1; }

# Work that only happens LIVE in the session is not a failure when it is missing
# before the session. PRE_SESSION is set once the vault has been looked for.
SESS="[sess]"
PRE_SESSION=0
# say_sess PRESENT(1/0) LABEL DETAIL_IF_MISSING
say_sess() {
  if [ "$1" = "1" ]; then
    say "$OK" "$2" ""
  elif [ "$PRE_SESSION" = "1" ]; then
    printf '%s %-42s %s\n' "$SESS" "$2" "not yet - this happens live in your session"
  else
    say "$NO" "$2" "$3"
  fi
}

# chk_cmd COMMAND LABEL
chk_cmd() {
  if have "$1"; then
    v=$("$1" --version 2>&1 | head -1)
    w=$(command -v "$1")
    say "$OK" "$2" "$v   ($w)"
  else
    say "$NO" "$2" "not found on PATH"
  fi
}

# chk_path PATH LABEL   (file or directory)
chk_path() {
  if [ -e "$1" ]; then say "$OK" "$2" "$1"; else say "$NO" "$2" "missing: $1"; fi
}

# jread FILE JQ_FILTER  -> prints value or empty
jread() {
  [ -f "$1" ] || return 1
  if have jq; then
    jq -c "$2" "$1" 2>/dev/null | sed 's/^null$//'
  else
    printf 'jq-not-installed'
  fi
}

# grep_json FILE PATTERN -> yes/no, works without jq
in_file() { [ -f "$1" ] && grep -q -- "$2" "$1" 2>/dev/null; }

printf '===============================================================\n'
printf ' AI ACCELERATION CLUB - PHASE 0 STATUS CHECK  (v%s)\n' "$VERSION"
printf ' Generated: %s\n' "$(date '+%Y-%m-%d %H:%M')"
printf ' Read-only. Nothing was created, modified or deleted.\n'
printf '===============================================================\n'

# ---------------------------------------------------------------------------
# STAGE 0 - Machine and prerequisites (Doc 01)
# ---------------------------------------------------------------------------
head1 "STAGE 0 - MACHINE AND PREREQUISITES  (Doc 01)"

printf '%s %-42s %s\n' "[info]" "macOS version" "$(sw_vers -productVersion 2>/dev/null || echo 'not macOS')"
printf '%s %-42s %s\n' "[info]" "Chip / architecture" "$(uname -m)"
printf '%s %-42s %s\n' "[info]" "Memory (GB)" "$(( $(sysctl -n hw.memsize 2>/dev/null || echo 0) / 1073741824 ))"

chk_cmd git "git"
chk_cmd claude "Claude Code"
chk_cmd jq "jq"

if have claude; then
  cp_path=$(command -v claude)
  case "$cp_path" in
    *"/.local/bin/"*)   printf '%s %-42s %s\n' "[info]" "Claude Code install method" "native installer (self-updating)" ;;
    *"/homebrew/"*|*"/usr/local/bin/"*) printf '%s %-42s %s\n' "[info]" "Claude Code install method" "likely Homebrew (does NOT auto-update)" ;;
    *) printf '%s %-42s %s\n' "[info]" "Claude Code install method" "unknown ($cp_path)" ;;
  esac
fi

if have brew; then
  printf '%s %-42s %s\n' "[info]" "Homebrew" "installed ($(brew --version 2>/dev/null | head -1))"
else
  printf '%s %-42s %s\n' "[info]" "Homebrew" "not installed (fine - native install path)"
fi

chk_path "/Applications/Obsidian.app" "Obsidian app"
chk_path "/Applications/Ghostty.app" "Ghostty app"
if [ -e "/Applications/Granola.app" ]; then
  say "$OK" "Granola app" "/Applications/Granola.app"
else
  printf '%s %-42s %s\n' "$WARN" "Granola app" "not in /Applications (check manually)"
fi

# ---------------------------------------------------------------------------
# Locate the vault
# ---------------------------------------------------------------------------
head1 "VAULT"

VAULT="$1"
VAULT_SRC=""

# 1) Obsidian's own vault list is the authoritative answer - it knows about
#    vaults anywhere on disk, including iCloud and external drives.
OBS_JSON="$HOME/Library/Application Support/obsidian/obsidian.json"
if [ -z "$VAULT" ] && [ -f "$OBS_JSON" ]; then
  if have jq; then
    cands=$(jq -r '.vaults[]?.path // empty' "$OBS_JSON" 2>/dev/null)
  else
    cands=$(grep -o '"path"[[:space:]]*:[[:space:]]*"[^"]*"' "$OBS_JSON" 2>/dev/null \
            | sed 's/.*"path"[[:space:]]*:[[:space:]]*"//; s/"$//')
  fi
  n=0
  while IFS= read -r p; do
    [ -n "$p" ] && [ -d "$p" ] || continue
    n=$((n+1))
    if [ "$n" = "1" ]; then VAULT="$p"; VAULT_SRC="Obsidian's own vault list"; fi
  done <<EOF
$cands
EOF
  if [ "$n" -gt 1 ]; then
    printf '%s %-42s %s\n' "$WARN" "More than one vault registered" "using the first; re-run with the path if wrong"
    printf '%s\n' "$cands" | sed 's/^/       /'
  fi
fi

# 2) Fallback: look on disk.
if [ -z "$VAULT" ]; then
  for base in "$HOME/Documents" "$HOME" "$HOME/Desktop" "$HOME/obsidian" \
              "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents" \
              "$HOME/Library/Mobile Documents/com~apple~CloudDocs"; do
    [ -d "$base" ] || continue
    found=$(find "$base" -maxdepth 3 -type d -name ".obsidian" 2>/dev/null | head -5)
    if [ -n "$found" ]; then
      VAULT=$(printf '%s\n' "$found" | head -1 | sed 's|/\.obsidian$||')
      VAULT_SRC="found on disk"
      others=$(printf '%s\n' "$found" | wc -l | tr -d ' ')
      if [ "$others" -gt 1 ]; then
        printf '%s %-42s %s\n' "$WARN" "More than one vault found" "using the first; re-run with the path if wrong"
        printf '%s\n' "$found" | sed 's|/\.obsidian$||' | sed 's/^/       /'
      fi
      break
    fi
  done
fi

HAS_VAULT=0
if [ -n "$VAULT" ] && [ -d "$VAULT" ]; then
  HAS_VAULT=1
  say "$OK" "Obsidian vault found" "$VAULT"
  [ -n "$VAULT_SRC" ] && printf '%s %-42s %s\n' "[info]" "  how it was located" "$VAULT_SRC"
else
  # NOT a failure. Doc 01 Step 2 explicitly says: "Don't create any vault yet -
  # I'll do that with my facilitator during the session."
  printf '%s %-42s %s\n' "[info]" "Obsidian vault" "none yet - EXPECTED before your session"
  printf '       %s\n' "Doc 01 Step 2 says: \"Don't create any vault yet - I'll do that"
  printf '       %s\n' "with my facilitator during the session.\" So this is correct, not missing."
  if [ -f "$OBS_JSON" ]; then
    printf '       %s\n' "(Obsidian has been opened at least once; it lists no vault.)"
  else
    printf '       %s\n' "(Obsidian has no vault list yet - it may never have been opened.)"
  fi
  printf '       %s\n' "If you DO have a vault somewhere unusual, re-run with its path:"
  printf '       bash %s "/Users/you/Documents/My Vault"\n' "$0"
fi

# No vault AND no global router == the session has not happened yet.
if [ "$HAS_VAULT" = "0" ] && [ ! -f "$HOME/.claude/CLAUDE.md" ]; then
  PRE_SESSION=1
  printf '\n%s %s\n' "[info]" "READING: you look PRE-SESSION. Everything from Doc 02 onward is"
  printf '%s %s\n'   "      " "built live with your facilitator, so items marked [sess] below are"
  printf '%s %s\n'   "      " "not things you missed - they are the agenda for session day."
fi

# ---------------------------------------------------------------------------
# STAGE 1 - Sandbox setup (Doc 02-S)  <-- only for participants who opted into the sandbox
# ---------------------------------------------------------------------------
head1 "STAGE 1 - SANDBOX SETUP  (Doc 02-S)"

VS="$VAULT/.claude/settings.json"
GS="$HOME/.claude/settings.json"

if [ "$HAS_VAULT" = "0" ]; then
  printf '%s %-42s %s\n' "[info]" "Sandbox config in the vault" "CANNOT CHECK YET - there is no vault"
  printf '       %s\n' "02-S Part 2a lives at <vault>/.claude/settings.json, so it cannot exist"
  printf '       %s\n' "before the vault does. It gets created live in the session, by design."
  printf '       %s\n' "The GLOBAL half of 02-S (Part 2b) IS checkable - see Stage 2 below."
elif [ -f "$VS" ]; then
  say "$OK" "Project settings (in vault)" "$VS"

  if have jq; then
    if jq -e . "$VS" >/dev/null 2>&1; then
      say "$OK" "Project settings is valid JSON" ""
    else
      say "$NO" "Project settings is valid JSON" "MALFORMED - the sandbox never loads"
    fi
    en=$(jread "$VS" '.sandbox.enabled')
    fi_=$(jread "$VS" '.sandbox.failIfUnavailable')
    un=$(jread "$VS" '.sandbox.allowUnsandboxedCommands')
    dr=$(jread "$VS" '.sandbox.filesystem.denyRead')
    ar=$(jread "$VS" '.sandbox.filesystem.allowRead')
    aw=$(jread "$VS" '.sandbox.filesystem.allowWrite')
    dom=$(jread "$VS" '.sandbox.network.allowedDomains | length')

    [ "$en" = "true" ]  && say "$OK" "sandbox.enabled" "true"                || say "$NO" "sandbox.enabled" "${en:-absent}"
    [ "$fi_" = "true" ] && say "$OK" "sandbox.failIfUnavailable" "true"      || say "$NO" "sandbox.failIfUnavailable" "${fi_:-absent}  <- without this there is no guarantee"
    [ "$un" = "false" ] && say "$OK" "sandbox.allowUnsandboxedCommands" "false (strict)" || say "$NO" "sandbox.allowUnsandboxedCommands" "${un:-absent}"
    printf '%s %-42s %s\n' "[info]" "filesystem.denyRead"  "${dr:-absent}"
    printf '%s %-42s %s\n' "[info]" "filesystem.allowRead" "${ar:-absent}"
    printf '%s %-42s %s\n' "[info]" "filesystem.allowWrite" "${aw:-absent}"
    printf '%s %-42s %s\n' "[info]" "network.allowedDomains (count)" "${dom:-0}"

    # THE load-bearing question: which 02-S did she run?
    case "$ar" in
      *'.claude'*) say "$OK" "02-S version" "PATCHED (~/.claude allowed) - Doc 03 will work" ;;
      "") printf '%s %-42s %s\n' "$WARN" "02-S version" "allowRead absent - cannot tell" ;;
      *)  say "$NO" "02-S version" "GENERIC (no ~/.claude) - Doc 03 breaks on ~12 commands" ;;
    esac
    case "$aw" in
      *'.claude'*) : ;;
      *) printf '%s %-42s %s\n' "$WARN" "allowWrite" "no ~/.claude - skill installs in Doc 03 will be blocked" ;;
    esac
  else
    # Never print the file itself: settings.json can carry API keys in its
    # "env" block, and this report is sent to the facilitator.
    printf '%s %-42s %s\n' "$WARN" "Cannot parse settings" "jq is not installed - sandbox keys not checked (install jq and re-run)"
  fi
else
  say "$NO" "Project settings (in vault)" "missing: $VS  <- the sandbox is NOT configured"
fi

# ---------------------------------------------------------------------------
# STAGE 2 - Global config (Doc 02-S part 2b / Doc 02 STEP 3 + 3.5)
# ---------------------------------------------------------------------------
head1 "STAGE 2 - GLOBAL CLAUDE CODE CONFIG  (Doc 02 STEP 3 / 3.5)"

if [ -f "$GS" ]; then
  say "$OK" "Global settings" "$GS"
  if have jq && ! jq -e . "$GS" >/dev/null 2>&1; then
    say "$NO" "Global settings is valid JSON" "MALFORMED"
  fi

  if in_file "$GS" 'python3'; then
    printf '%s %-42s %s\n' "$WARN" "permissions.allow" "contains Bash(python3 *) -> the STANDARD Doc 02 block is in effect, not the 02-S hardened one"
  else
    say "$OK" "permissions.allow" "no blanket python3 (02-S hardened block)"
  fi

  if in_file "$GS" '"Read(~/.ssh/'; then
    say "$OK" "permissions.deny" "credential deny list present"
  else
    say "$NO" "permissions.deny" "credential deny list NOT found"
  fi

  if in_file "$GS" 'additionalDirectories'; then
    printf '%s %-42s %s\n' "$WARN" "additionalDirectories" "PRESENT - widens Claude's scope beyond the vault"
  else
    say "$OK" "additionalDirectories" "absent (correct)"
  fi

  # The hooks block ships inside 02-S Part 2b, so on the sandboxed variant this
  # is the participant's own homework, not session work.
  if in_file "$GS" '"hooks"'; then
    say "$OK" "hooks block present" "(ships in 02-S Part 2b)"
  else
    say "$NO" "hooks block present" "not set"
  fi

  # --- Step 3.5 - session work ---
  ac=$(jread "$GS" '.env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE')
  if [ -n "$ac" ] && [ "$ac" != "jq-not-installed" ]; then
    say "$OK" "Auto-compact threshold (Layer 1)" "$ac"
  else
    say_sess 0 "Auto-compact threshold (Layer 1)" "not set - Step 3.5 did not run"
  fi

  if in_file "$GS" 'statusLine'; then
    say_sess 1 "statusLine configured (Layer 2)" ""
  else
    say_sess 0 "statusLine configured (Layer 2)" "not set"
  fi
else
  say "$NO" "Global settings" "missing: $GS"
fi

if [ -f "$HOME/.claude/statusline.sh" ]; then
  if [ -x "$HOME/.claude/statusline.sh" ]; then
    say "$OK" "statusline.sh" "present and executable"
  else
    printf '%s %-42s %s\n' "$WARN" "statusline.sh" "present but NOT executable (chmod +x)"
  fi
else
  say_sess 0 "statusline.sh" "missing: ~/.claude/statusline.sh"
fi

if [ -f "$HOME/.claude/CLAUDE.md" ]; then
  say "$OK" "Global router (~/.claude/CLAUDE.md)" ""
  if [ -n "$VAULT" ] && grep -qF "$VAULT" "$HOME/.claude/CLAUDE.md" 2>/dev/null; then
    say "$OK" "Router points at the vault" ""
  else
    printf '%s %-42s %s\n' "$WARN" "Router points at the vault" "vault path not found inside the router file"
  fi
else
  say_sess 0 "Global router (~/.claude/CLAUDE.md)" "missing - Doc 02 STEP 3 did not finish"
fi

# ---------------------------------------------------------------------------
# STAGE 3 - Vault build (Doc 02 STEP 1 - 12.5)
# ---------------------------------------------------------------------------
head1 "STAGE 3 - VAULT BUILD  (Doc 02)"

if [ -n "$VAULT" ] && [ -d "$VAULT" ]; then
  # INBOX may be at the root (kit default) or nested under a hub folder
  if [ -d "$VAULT/00 INBOX" ]; then
    inbox="$VAULT/00 INBOX"
  else
    inbox=$(find "$VAULT" -maxdepth 2 -type d -iname "*INBOX" 2>/dev/null | sort | head -1)
  fi
  if [ -n "$inbox" ]; then
    say "$OK" "folder: INBOX" "${inbox#$VAULT/}"
  else
    say "$NO" "folder: INBOX" "missing"
  fi

  for d in "01 PROJECTS" "02 AREAS" "03 REFERENCE" "04 ARCHIVES" "05 AI/CLAUDE CODE/workspace" "05 AI/CLAUDE CODE/resources" "Templates"; do
    if [ -d "$VAULT/$d" ]; then say "$OK" "folder: $d" ""; else say "$NO" "folder: $d" "missing"; fi
  done

  chk_path "$VAULT/CLAUDE.md" "Vault CLAUDE.md (Doc 02 STEP 2)"

  if [ -f "$VAULT/.obsidian/app.json" ]; then
    say "$OK" "Obsidian app.json (STEP 1.5)" ""
    printf '%s %-42s %s\n' "[info]" "  app.json contents" "$(tr -d '\n ' < "$VAULT/.obsidian/app.json")"
  else
    say "$NO" "Obsidian app.json (STEP 1.5)" "missing - Files and links settings not applied"
  fi

  n_proj=$(ls -1 "$VAULT/01 PROJECTS" 2>/dev/null | wc -l | tr -d ' ')
  n_tpl=$(ls -1 "$VAULT/Templates" 2>/dev/null | wc -l | tr -d ' ')
  n_area=$(ls -1 "$VAULT/02 AREAS" 2>/dev/null | wc -l | tr -d ' ')
  printf '%s %-42s %s\n' "[info]" "items in 01 PROJECTS" "$n_proj"
  printf '%s %-42s %s\n' "[info]" "items in 02 AREAS" "$n_area"
  printf '%s %-42s %s\n' "[info]" "items in Templates" "$n_tpl"

  jrn=$(find "$VAULT" -maxdepth 4 -iname "*Journey*.md" 2>/dev/null | head -1)
  if [ -n "$jrn" ]; then say "$OK" "AIAC Journey brief (STEP 11.5)" "$(basename "$jrn")"; else say "$NO" "AIAC Journey brief (STEP 11.5)" "not found"; fi

  cs=$(find "$VAULT" -maxdepth 4 -iname "*Cheat*Sheet*.md" 2>/dev/null | head -1)
  if [ -n "$cs" ]; then say "$OK" "AIAC cheat sheet (STEP 12.5)" "$(basename "$cs")"; else say "$NO" "AIAC cheat sheet (STEP 12.5)" "not found"; fi
fi

# git identity + repo
printf '\n'
gn=$(git config --global user.name 2>/dev/null)
ge=$(git config --global user.email 2>/dev/null)
if [ -n "$gn" ] && [ -n "$ge" ]; then say "$OK" "git identity (STEP 4)" "$gn <$ge>"; else say "$NO" "git identity (STEP 4)" "user.name / user.email not set"; fi

REPO=""
for cand in "$VAULT"/dev/* "$HOME"/dev/*; do
  [ -d "$cand/.git" ] || continue
  REPO="$cand"; break
done
# fall back to any git repo living anywhere inside the vault
if [ -z "$REPO" ] && [ -n "$VAULT" ] && [ -d "$VAULT" ]; then
  g=$(find "$VAULT" -maxdepth 4 -type d -name ".git" -not -path "*/.obsidian/*" 2>/dev/null | head -1)
  [ -n "$g" ] && REPO="${g%/.git}"
fi
if [ -n "$REPO" ]; then
  say "$OK" "Code repo (STEP 6)" "$REPO"
  case "$REPO" in
    "$VAULT"/*) printf '%s %-42s %s\n' "[info]" "  repo location choice" "(A) inside the vault" ;;
    *)          printf '%s %-42s %s\n' "[info]" "  repo location choice" "(B) ~/dev - needs a named sandbox path" ;;
  esac
  nc=$(git -C "$REPO" rev-list --count HEAD 2>/dev/null || echo 0)
  rm_=$(git -C "$REPO" remote get-url origin 2>/dev/null || echo "no remote")
  printf '%s %-42s %s\n' "[info]" "  commits" "$nc"
  printf '%s %-42s %s\n' "[info]" "  origin" "$rm_"
  if [ -f "$REPO/CLAUDE.md" ]; then say "$OK" "Repo CLAUDE.md (STEP 8)" ""; else say "$NO" "Repo CLAUDE.md (STEP 8)" "missing"; fi
else
  say_sess 0 "Code repo (STEP 6)" "no git repo found in <vault>/dev or ~/dev"
fi

# ---------------------------------------------------------------------------
# STAGE 4 - Skills and plugins (Doc 03)
# ---------------------------------------------------------------------------
head1 "STAGE 4 - SKILLS AND PLUGINS  (Doc 03)"

for s in project-create inbox-clear retro session-close skill-create meeting-minutes; do
  if [ -f "$HOME/.claude/skills/$s/SKILL.md" ]; then
    say "$OK" "skill: /$s" ""
  else
    say_sess 0 "skill: /$s" "missing"
  fi
done

if [ -d "$HOME/.claude/plugins" ]; then
  say "$OK" "plugins directory" "$HOME/.claude/plugins"
  pl=$(ls -1 "$HOME/.claude/plugins/marketplaces" 2>/dev/null | tr '\n' ' ')
  printf '%s %-42s %s\n' "[info]" "  marketplaces" "${pl:-none}"
  for p in superpowers playground; do
    if find "$HOME/.claude/plugins" -maxdepth 5 -iname "*$p*" 2>/dev/null | head -1 | grep -q .; then
      say "$OK" "plugin: $p" ""
    else
      say_sess 0 "plugin: $p" "not found"
    fi
  done
else
  say_sess 0 "plugins directory" "missing - Doc 03 STEP 2 did not run"
fi

if [ -n "$VAULT" ] && [ -f "$VAULT/05 AI/CLAUDE CODE/resources/lessons.md" ]; then
  say "$OK" "lessons.md (Doc 03 STEP 3)" ""
else
  say_sess 0 "lessons.md (Doc 03 STEP 3)" "missing"
fi

# ---------------------------------------------------------------------------
# VERDICT
# ---------------------------------------------------------------------------
head1 "WHERE THINGS STAND"

stage0=0; stage1g=0; stage1p=0; stage2=0; stage3=0; stage4=0
have git && have claude && have jq && [ -d "/Applications/Obsidian.app" ] && stage0=1
# 02-S global half (Part 2b): the credential deny list is present AND there is no
# blanket python3 - that combination is the hardened block, not the standard one.
[ -f "$GS" ] && in_file "$GS" '"Read(~/.ssh/' && ! in_file "$GS" 'python3' && stage1g=1
# 02-S project half (Part 2a) needs the vault to exist, so it is session-time.
[ "$HAS_VAULT" = "1" ] && [ -f "$VS" ] && in_file "$VS" 'sandbox' && stage1p=1
[ -f "$HOME/.claude/CLAUDE.md" ] && stage2=1
[ -n "$VAULT" ] && [ -f "$VAULT/CLAUDE.md" ] && [ -d "$VAULT/01 PROJECTS" ] && stage3=1
[ -f "$HOME/.claude/skills/session-close/SKILL.md" ] && stage4=1

mark()  { [ "$1" = "1" ] && printf 'DONE      ' || printf 'NOT DONE  '; }
marks() {
  if [ "$1" = "1" ]; then printf 'DONE      '
  elif [ "$PRE_SESSION" = "1" ]; then printf 'SESSION   '
  else printf 'NOT DONE  '; fi
}

printf '  YOURS - to have ready before session day\n'
printf '  %s Doc 01   - prerequisites installed\n'              "$(mark $stage0)"
printf '  %s Doc 02-S - global settings, Part 2b\n'             "$(mark $stage1g)"
printf '\n  BUILT LIVE IN THE SESSION - not homework\n'
printf '  %s Doc 02-S - sandbox config in the vault, Part 2a\n' "$(marks $stage1p)"
printf '  %s Doc 02   - global config + router\n'               "$(marks $stage2)"
printf '  %s Doc 02   - vault built (folders + CLAUDE.md)\n'    "$(marks $stage3)"
printf '  %s Doc 03   - skills and plugins\n'                   "$(marks $stage4)"

if [ "$PRE_SESSION" = "1" ]; then
  printf '\n  >> READING: everything marked SESSION is the agenda for session day,\n'
  printf '     not something you missed.\n'
  if [ "$stage0" = "1" ] && [ "$stage1g" = "1" ]; then
    printf '  >> YOUR HOMEWORK IS COMPLETE. You are waiting on a session date.\n'
  fi
fi

printf '\n  Checks passed: %s   Checks failed: %s   (session work is not counted as failed)\n' "$pass_count" "$fail_count"

printf '\n  NOT CHECKED HERE (needs a human):\n'
printf '    - Claude Pro / Max subscription is active\n'
printf '    - Granola has screen + microphone permission\n'
printf '    - The /sandbox Config tab shows the rules as RESOLVED\n'
printf '    - The fresh-window router test (Block 7)\n'

printf '\n===============================================================\n'
printf ' END OF REPORT - copy everything above and send it back.\n'
printf '===============================================================\n'
