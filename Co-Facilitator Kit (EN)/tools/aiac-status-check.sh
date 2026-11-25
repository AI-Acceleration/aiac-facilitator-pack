#!/bin/bash
# ---------------------------------------------------------------------------
# ORIGIN: contributed by Mangan (github.com/dibkorma), co-facilitator, 2026-08-18.
# Built while running a 10-student cohort; adopted into the kit 2026-08-19.
# Its first real run flipped a wrong diagnosis: a student everyone believed was
# 19 days behind was actually finished and waiting on us to schedule.
#
# FACILITATOR NOTE: ship this to the participant as the .sh.txt twin - WhatsApp
# and Gmail block .sh attachments. The twin is byte-identical and runs the same.
# Keep this file 100% ASCII so it survives copy-paste through any chat app.
# ---------------------------------------------------------------------------
# AI Acceleration Club - Phase 0 Status Check
#
# WHAT THIS IS: a read-only report of how far your Phase 0 setup got.
# It writes nothing, changes nothing, installs nothing, and sends nothing.
# It only looks at files that already exist on your machine and prints a summary.
# Works on macOS, Windows (Git Bash or WSL) and Linux.
#
# HOW TO RUN - use the exact filename you received (.sh or .sh.txt both work):
#   bash ~/Downloads/aiac-status-check.sh.txt
# You can run it in a terminal window (Git Bash on Windows) or ask Claude Code
# to run that same command for you.
#
# WHAT TO SHARE: ONLY the block at the very end, from the line
#   ----- AIAC STATUS (safe to share) -----
# down to the line
#   ----- END -----
# That block holds nothing but check names, DONE / NOT DONE / SKIPPED, your
# operating system and one verdict line. Everything printed above it is for
# your own eyes: it is already trimmed (no email, no full paths, no repo URL),
# but it describes your machine, so keep it to yourself.
#
# OPTIONS:
#   bash aiac-status-check.sh.txt "/path/to/your/vault"   check this vault
#   bash aiac-status-check.sh.txt --sandbox    also check the opt-in sandbox (Doc 02-S)
#   bash aiac-status-check.sh.txt --details    more local detail - do NOT share it
# ---------------------------------------------------------------------------

VERSION="2.0"

DETAILS=0
FORCE_SANDBOX=0
VAULT_ARG=""
for arg in "$@"; do
  case "$arg" in
    --details) DETAILS=1 ;;
    --sandbox) FORCE_SANDBOX=1 ;;
    -h|--help)
      printf '%s\n' "Usage: bash aiac-status-check.sh [--sandbox] [--details] [\"/path/to/vault\"]"
      printf '%s\n' "Read-only. Share ONLY the block between '----- AIAC STATUS (safe to share) -----'"
      printf '%s\n' "and '----- END -----' at the end of the output."
      exit 0
      ;;
    -*) printf '%s\n' "Unknown option: $arg (try --help)"; exit 2 ;;
    *) VAULT_ARG="$arg" ;;
  esac
done

# Never take a lock or refresh an index in any repository we look at.
GIT_OPTIONAL_LOCKS=0
export GIT_OPTIONAL_LOCKS

NL='
'
TAB=$(printf '\t')

# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
line() { printf '%s\n' "---------------------------------------------------------------"; }
head1() { printf '\n'; line; printf '%s\n' "$1"; line; }
info() { printf '%s %-44s %s\n' "[info]" "$1" "$2"; }
warn() { printf '%s %-44s %s\n' "[WARN]" "$1" "$2"; }

have_one() {
  if [ "$1" = "jq" ] && [ "${AIAC_STATUS_FORCE_NO_JQ:-0}" = "1" ]; then
    return 1
  fi
  command -v "$1" >/dev/null 2>&1
}

# On WSL, Windows tools are reachable as name.exe.
have() {
  have_one "$1" && return 0
  case "$PLATFORM" in Windows*) have_one "$1.exe" && return 0 ;; esac
  return 1
}

cmd_name() {
  if have_one "$1"; then printf '%s' "$1"; else printf '%s' "$1.exe"; fi
}

# Replace the home folder with ~ so the report never spells out your user name.
tildify() {
  case "$1" in
    "$HOME") printf '%s' "~" ;;
    "$HOME"/*) printf '%s' "~/${1#"$HOME"/}" ;;
    *) printf '%s' "$1" ;;
  esac
}

# Paths that may contain a client, company or personal name are only shown
# with --details.
show_path() {
  if [ "$DETAILS" = "1" ]; then tildify "$1"; else printf '%s' "(hidden - re-run with --details to see it)"; fi
}

lower() { printf '%s' "$1" | tr 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 'abcdefghijklmnopqrstuvwxyz'; }

# Convert ~, $HOME and Windows drive paths (C:\Users\...) to this shell's form.
to_unix_path() {
  p=$1
  case "$p" in
    "~") p=$HOME ;;
    "~/"*) p="$HOME/${p#\~/}" ;;
    '$HOME') p=$HOME ;;
    '$HOME/'*) p="$HOME/${p#\$HOME/}" ;;
    [A-Za-z]:|[A-Za-z]:[\\/]*)
      conv=""
      if have_one cygpath; then
        conv=$(cygpath -u "$p" 2>/dev/null)
      elif have_one wslpath; then
        conv=$(wslpath -u "$p" 2>/dev/null)
      fi
      if [ -n "$conv" ]; then
        p=$conv
      else
        drive=$(lower "${p%%:*}")
        rest=$(printf '%s' "${p#?:}" | tr '\\' '/' | sed 's|//*|/|g')
        if [ "$PLATFORM" = "Windows (WSL)" ]; then
          p="${AIAC_STATUS_WSL_MNT:-/mnt}/$drive$rest"
        else
          p="/$drive$rest"
        fi
      fi
      ;;
  esac
  case "$p" in
    */) [ "$p" != "/" ] && p=${p%/} ;;
  esac
  printf '%s' "$p"
}

same_dir() {
  [ -d "$1" ] && [ -d "$2" ] || return 1
  a=$(cd "$1" 2>/dev/null && pwd -P)
  b=$(cd "$2" 2>/dev/null && pwd -P)
  [ -n "$a" ] && [ "$a" = "$b" ]
}

json_valid() { have jq && [ -f "$1" ] && jq -e . "$1" >/dev/null 2>&1; }
jtest() { json_valid "$1" && jq -e "$2" "$1" >/dev/null 2>&1; }

# Which cloud-sync service, if any, a path lives in.
cloud_kind() {
  l=$(lower "$1")
  case "$l" in
    *onedrive*) printf '%s' "OneDrive" ;;
    *dropbox*) printf '%s' "Dropbox" ;;
    *"google drive"*|*googledrive*|*"my drive"*) printf '%s' "Google Drive" ;;
    *icloud*|*"mobile documents"*|*clouddocs*) printf '%s' "iCloud" ;;
    */library/cloudstorage/*) printf '%s' "a cloud storage provider" ;;
    *) printf '%s' "" ;;
  esac
}

# ---------------------------------------------------------------------------
# Check bookkeeping. Every check is recorded once, printed as a detail line now
# and repeated as a bare status in the safe-to-share block at the end.
#   check GROUP STATUS LABEL DETAIL
#   GROUP:  home = before the session, sess = built live in the session,
#           sbxh / sbxs = the same two, for the opt-in sandbox (Doc 02-S)
#   STATUS: done | notdone | skip   (skip = optional, never counts against you)
# ---------------------------------------------------------------------------
PRE_SESSION=0
N=0
check() {
  N=$((N+1))
  C_GROUP[$N]=$1
  C_STATUS[$N]=$2
  C_LABEL[$N]=$3
  case "$2" in
    done) tag="[ OK ]" ;;
    skip) tag="[skip]" ;;
    *)
      tag="[ -- ]"
      if [ "$PRE_SESSION" = "1" ]; then
        case "$1" in sess|sbxs) tag="[sess]" ;; esac
      fi
      ;;
  esac
  if [ -n "$4" ] && [ "${#3}" -gt 44 ]; then
    printf '%s %s\n' "$tag" "$3"
    printf '       %-44s %s\n' "" "$4"
  elif [ -n "$4" ]; then
    printf '%s %-44s %s\n' "$tag" "$3" "$4"
  else
    printf '%s %s\n' "$tag" "$3"
  fi
}

# ---------------------------------------------------------------------------
# Platform
# ---------------------------------------------------------------------------
UNAME_SYSTEM=$(uname -s 2>/dev/null || printf 'unknown')
case "$UNAME_SYSTEM" in
  Darwin) PLATFORM="macOS" ;;
  MINGW*|MSYS*|CYGWIN*) PLATFORM="Windows" ;;
  Linux)
    if [ -n "${WSL_DISTRO_NAME:-}" ] || grep -qi microsoft /proc/version 2>/dev/null; then
      PLATFORM="Windows (WSL)"
    else
      PLATFORM="Linux"
    fi
    ;;
  *) PLATFORM="unsupported" ;;
esac
WSL_C="${AIAC_STATUS_WSL_MNT:-/mnt}/c"

printf '===============================================================\n'
printf ' AI ACCELERATION CLUB - PHASE 0 STATUS CHECK  (v%s)\n' "$VERSION"
printf ' Generated: %s\n' "$(date '+%Y-%m-%d %H:%M')"
printf ' Read-only. Nothing was created, modified or deleted.\n'
printf '\n'
printf ' The DETAILS below are for your eyes only.\n'
printf ' To share your status, copy ONLY the block at the very end that is\n'
printf ' marked "safe to share" - nothing else.\n'
if [ "$DETAILS" = "1" ]; then
  printf '\n'
  printf ' *** --details is ON: this output shows local paths and names. ***\n'
  printf ' *** Do NOT share it. Share only the safe-to-share block.      ***\n'
fi
printf '===============================================================\n'

# ---------------------------------------------------------------------------
# STAGE 0 - Machine and prerequisites (Doc 01)
# ---------------------------------------------------------------------------
head1 "STAGE 0 - MACHINE AND PREREQUISITES  (Doc 01)"

info "Operating system" "$PLATFORM"
if [ "$PLATFORM" = "macOS" ]; then
  info "macOS version" "$(sw_vers -productVersion 2>/dev/null || echo 'unknown')"
  mem=$(sysctl -n hw.memsize 2>/dev/null || /usr/sbin/sysctl -n hw.memsize 2>/dev/null || echo 0)
  info "Memory (GB)" "$(( ${mem:-0} / 1073741824 ))"
fi
info "Chip / architecture" "$(uname -m 2>/dev/null)"

# tool_version COMMAND -> first line of --version, or empty
tool_version() {
  c=$(cmd_name "$1")
  "$c" --version 2>&1 | head -1
}

tool_check() {  # tool_check COMMAND LABEL
  if have "$1"; then
    where=""
    [ "$DETAILS" = "1" ] && where="   ($(tildify "$(command -v "$(cmd_name "$1")")"))"
    check home done "$2" "$(tool_version "$1")$where"
  else
    check home notdone "$2" "not found on PATH (a new terminal window may be needed after installing)"
  fi
}

tool_check git "Doc 01 - Git installed"
tool_check gh "Doc 01 - GitHub CLI (gh) installed"

# gh sign-in: read the gh config file, never the token, never the account name.
GH_SIGNED=0
if [ -n "${GH_TOKEN:-}" ] || [ -n "${GITHUB_TOKEN:-}" ]; then
  GH_SIGNED=1
else
  gh_dirs=""
  [ -n "${GH_CONFIG_DIR:-}" ] && gh_dirs="$gh_dirs$NL$(to_unix_path "$GH_CONFIG_DIR")"
  gh_dirs="$gh_dirs$NL${XDG_CONFIG_HOME:-$HOME/.config}/gh"
  [ -n "${APPDATA:-}" ] && gh_dirs="$gh_dirs$NL$(to_unix_path "$APPDATA")/GitHub CLI"
  OLDIFS=$IFS; IFS=$NL; set -f
  for d in $gh_dirs; do
    [ -n "$d" ] || continue
    if grep -q '^github\.com:' "$d/hosts.yml" 2>/dev/null; then GH_SIGNED=1; break; fi
  done
  IFS=$OLDIFS; set +f
fi
if [ "$GH_SIGNED" = "1" ]; then
  check home done "Doc 01 - GitHub CLI signed in" "signed in to github.com (account name not shown)"
else
  check home notdone "Doc 01 - GitHub CLI signed in" "no github.com sign-in found - run gh auth login in a separate terminal window"
fi

tool_check claude "Doc 01 - Claude Code installed"
if have claude; then
  cp_path=$(command -v "$(cmd_name claude)")
  case "$cp_path" in
    *"/.local/bin/"*) info "  install method" "native installer (self-updating)" ;;
    *"/homebrew/"*|*"/usr/local/bin/"*) info "  install method" "likely Homebrew (does NOT auto-update)" ;;
    *) info "  install method" "other $([ "$DETAILS" = "1" ] && printf '(%s)' "$(tildify "$cp_path")")" ;;
  esac
fi
tool_check jq "Doc 01 - jq installed"

# Python 3: python3, python or the Windows py launcher. The Microsoft Store
# stub prints "Python was not found", so only a real "Python 3.x" counts.
PY_VER=""
for py in python3 python py; do
  have "$py" || continue
  c=$(cmd_name "$py")
  if [ "$py" = "py" ]; then v=$("$c" -3 --version 2>&1 | head -1); else v=$("$c" --version 2>&1 | head -1); fi
  case "$v" in "Python 3"*) PY_VER="$v ($py)"; break ;; esac
done
if [ -n "$PY_VER" ]; then
  check home done "Doc 01 - Python 3 installed" "$PY_VER"
else
  check home notdone "Doc 01 - Python 3 installed" "no working python3 / python / py found"
fi

# Obsidian, per platform. Never require a macOS path on another OS.
OBSIDIAN_FOUND=""
case "$PLATFORM" in
  macOS)
    mac_obsidian="${AIAC_STATUS_OBSIDIAN_APP:-/Applications/Obsidian.app}"
    if [ -e "$mac_obsidian" ]; then OBSIDIAN_FOUND="Applications folder"
    elif [ -e "$HOME/Applications/Obsidian.app" ]; then OBSIDIAN_FOUND="your Applications folder"; fi
    ;;
  Windows*)
    for base in "${LOCALAPPDATA:-}" "${PROGRAMFILES:-}"; do
      [ -n "$base" ] || continue
      b=$(to_unix_path "$base")
      for exe in "$b/Programs/Obsidian/Obsidian.exe" "$b/Obsidian/Obsidian.exe"; do
        if [ -e "$exe" ]; then OBSIDIAN_FOUND="Windows install"; break 2; fi
      done
    done
    if [ -z "$OBSIDIAN_FOUND" ] && [ "$PLATFORM" = "Windows (WSL)" ]; then
      for exe in "$WSL_C"/Users/*/AppData/Local/Programs/Obsidian/Obsidian.exe \
                 "$WSL_C"/Users/*/AppData/Local/Obsidian/Obsidian.exe \
                 "$WSL_C/Program Files/Obsidian/Obsidian.exe"; do
        if [ -e "$exe" ]; then OBSIDIAN_FOUND="Windows install"; break; fi
      done
    fi
    ;;
  Linux)
    if have obsidian; then OBSIDIAN_FOUND="on PATH"
    elif have flatpak && flatpak info md.obsidian.Obsidian >/dev/null 2>&1; then OBSIDIAN_FOUND="Flatpak"
    elif ls "$HOME"/Applications/Obsidian*.AppImage >/dev/null 2>&1 || ls "$HOME"/Obsidian*.AppImage >/dev/null 2>&1; then OBSIDIAN_FOUND="AppImage"
    fi
    ;;
esac
if [ -n "$OBSIDIAN_FOUND" ]; then
  check home done "Doc 01 - Obsidian installed" "found ($OBSIDIAN_FOUND)"
elif [ "$PLATFORM" = "unsupported" ]; then
  check home notdone "Doc 01 - Obsidian installed" "this operating system cannot be checked by this script"
else
  check home notdone "Doc 01 - Obsidian installed" "not found in the usual install locations for $PLATFORM"
fi

# Optional tools: never a NOT DONE.
if [ "$PLATFORM" = "macOS" ]; then
  if [ -e "/Applications/Ghostty.app" ] || [ -e "$HOME/Applications/Ghostty.app" ]; then
    check home done "Doc 01 - Ghostty terminal" "found"
  else
    check home skip "Doc 01 - Ghostty terminal" "not found - optional, the built-in Terminal works too"
  fi
fi
GRANOLA=0
case "$PLATFORM" in
  macOS) { [ -e "/Applications/Granola.app" ] || [ -e "$HOME/Applications/Granola.app" ]; } && GRANOLA=1 ;;
  Windows*)
    if [ -n "${LOCALAPPDATA:-}" ]; then
      b=$(to_unix_path "$LOCALAPPDATA")
      { [ -e "$b/Programs/Granola/Granola.exe" ] || [ -e "$b/Granola/Granola.exe" ]; } && GRANOLA=1
    fi
    ;;
esac
if [ "$GRANOLA" = "1" ]; then
  check home done "Doc 01 - Granola or other transcription tool" "Granola found"
else
  check home skip "Doc 01 - Granola or other transcription tool" "Granola not found - optional: any transcription tool, or a pasted transcript, works"
fi

# ---------------------------------------------------------------------------
# Locate the vault. The vault that counts is the one Claude Code uses: the one
# your global router (~/.claude/CLAUDE.md) names. Before the session there is
# no router yet, so we fall back to Obsidian's own vault list, then to disk.
# ---------------------------------------------------------------------------
head1 "VAULT  (pre-flight + Doc 02)"

ROUTER="$HOME/.claude/CLAUDE.md"
[ -f "$ROUTER" ] || PRE_SESSION=1

ROUTER_VAULT=""
if [ -f "$ROUTER" ]; then
  cands=$( { grep -o '`[^`]*CLAUDE\.md`' "$ROUTER" 2>/dev/null | tr -d '`'
             grep -oE '(~|/|[A-Za-z]:)[^`*"<>|]*CLAUDE\.md' "$ROUTER" 2>/dev/null; } )
  OLDIFS=$IFS; IFS=$NL; set -f
  for c in $cands; do
    p=$(to_unix_path "$c")
    d=${p%/CLAUDE.md}
    [ "$d" != "$p" ] || continue
    [ -d "$d" ] || continue
    same_dir "$d" "$HOME/.claude" && continue
    ROUTER_VAULT=$d
    break
  done
  IFS=$OLDIFS; set +f
fi

VAULT=""
VAULT_SRC=""
if [ -n "$VAULT_ARG" ]; then
  VAULT=$(to_unix_path "$VAULT_ARG"); VAULT_SRC="the path you passed in"
elif [ -n "$ROUTER_VAULT" ]; then
  VAULT=$ROUTER_VAULT; VAULT_SRC="your global router (~/.claude/CLAUDE.md)"
fi

# Obsidian's own vault list, per platform.
if [ -z "$VAULT" ]; then
  obs_files="$HOME/Library/Application Support/obsidian/obsidian.json$NL$HOME/.config/obsidian/obsidian.json$NL$HOME/.var/app/md.obsidian.Obsidian/config/obsidian/obsidian.json"
  [ -n "${APPDATA:-}" ] && obs_files="$obs_files$NL$(to_unix_path "$APPDATA")/obsidian/obsidian.json"
  if [ "$PLATFORM" = "Windows (WSL)" ]; then
    for f in "$WSL_C"/Users/*/AppData/Roaming/obsidian/obsidian.json; do
      [ -f "$f" ] && obs_files="$obs_files$NL$f"
    done
  fi
  vault_list=""
  OLDIFS=$IFS; IFS=$NL; set -f
  for f in $obs_files; do
    [ -f "$f" ] || continue
    if have jq; then
      vault_list="$vault_list$NL$(jq -r '.vaults[]?.path // empty' "$f" 2>/dev/null)"
    else
      vault_list="$vault_list$NL$(grep -o '"path"[[:space:]]*:[[:space:]]*"[^"]*"' "$f" 2>/dev/null \
        | sed 's/.*"path"[[:space:]]*:[[:space:]]*"//; s/"$//')"
    fi
  done
  n=0
  for c in $vault_list; do
    p=$(to_unix_path "$c")
    [ -n "$p" ] && [ -d "$p" ] || continue
    n=$((n+1))
    if [ "$n" = "1" ]; then VAULT=$p; VAULT_SRC="Obsidian's own vault list"; fi
    [ "$DETAILS" = "1" ] && info "  vault registered in Obsidian" "$(tildify "$p")"
  done
  IFS=$OLDIFS; set +f
  if [ "$n" -gt 1 ]; then
    warn "More than one vault registered" "$n vaults; using the first - re-run with the right path if wrong"
  fi
fi

# Last resort: look on disk in the usual places.
if [ -z "$VAULT" ]; then
  for base in "$HOME/AIAC-Vault" "$HOME/Desktop" "$HOME/Documents" "$HOME" "$HOME/obsidian" \
              "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents"; do
    [ -d "$base" ] || continue
    found=$(find "$base" -maxdepth 2 -type d -name ".obsidian" 2>/dev/null | head -5)
    if [ -n "$found" ]; then
      VAULT=$(printf '%s\n' "$found" | head -1 | sed 's|/\.obsidian$||')
      VAULT_SRC="found on disk"
      others=$(printf '%s\n' "$found" | wc -l | tr -d ' ')
      [ "$others" -gt 1 ] && warn "More than one vault found on disk" "using the first - re-run with the right path if wrong"
      break
    fi
  done
fi

HAS_VAULT=0
[ -n "$VAULT" ] && [ -d "$VAULT" ] && HAS_VAULT=1

if [ "$HAS_VAULT" = "1" ]; then
  check home done "Pre-flight - vault folder exists" "$(show_path "$VAULT")"
  info "  how it was located" "$VAULT_SRC"
else
  check home notdone "Pre-flight - vault folder exists" "no vault found - the pre-flight prompt creates it"
  printf '       %s\n' "If you DO have a vault somewhere unusual, re-run with its path:"
  printf '       bash %s "/path/to/your/vault"\n' "$(tildify "$0")"
fi

# The vault must live in a plain local folder. Sync clients (OneDrive, Dropbox,
# Google Drive, iCloud) rewrite files under Claude and Obsidian and can lock them.
if [ "$HAS_VAULT" = "1" ]; then
  real_vault=$(cd "$VAULT" 2>/dev/null && pwd -P)
  ck=$(cloud_kind "$VAULT")
  [ -z "$ck" ] && ck=$(cloud_kind "$real_vault")
  if [ -n "$ck" ]; then
    check home notdone "Pre-flight - vault not in a cloud-synced folder" "the vault is inside $ck - move it to a plain local folder such as ~/AIAC-Vault"
  else
    check home done "Pre-flight - vault not in a cloud-synced folder" "local folder"
  fi
  if [ -d "$VAULT/.obsidian" ]; then
    check home done "Pre-flight - vault opened in Obsidian" ".obsidian folder present"
  else
    check home notdone "Pre-flight - vault opened in Obsidian" "no .obsidian folder - in Obsidian use 'Open folder as vault' on THIS folder (never 'Create new vault')"
  fi
else
  check home notdone "Pre-flight - vault not in a cloud-synced folder" "no vault yet"
  check home notdone "Pre-flight - vault opened in Obsidian" "no vault yet"
fi

if [ "$PRE_SESSION" = "1" ]; then
  printf '\n%s %s\n' "[info]" "READING: you look PRE-SESSION (no ~/.claude/CLAUDE.md yet). Everything"
  printf '%s %s\n'   "      " "from Doc 02 onward is built live with your facilitator, so items"
  printf '%s %s\n'   "      " "marked [sess] are not things you missed - they are the session agenda."
fi

# Broad, lasting approvals the kit never grants. Any git rule with a wildcard
# counts (git options can write files, run programs or plant hooks); the five
# exact read-only git rules and "ls *", "mkdir *", "wc *" are fine.
BROAD_FILTER='
  [ ((.permissions.allow // []) | if type == "array" then .[] else empty end
      | select(type == "string")
      | select(. == "Bash" or . == "Bash(*)" or . == "Bash(:*)" or
               . == "Read" or . == "Write" or . == "Edit" or
               (test("^Bash\\(git[ :)]") and test("[*]")) or
               test("^Bash\\((cat|head|gws)( \\*|:\\*|\\*)\\)$") or
               test("^Bash\\((python3?|py|node|npx|pip3?|ruby|perl|deno|bun|bash|sh|zsh|pwsh|powershell)(\\.exe)?([ :].*)?\\)$"))),
    (if .permissions.defaultMode == "bypassPermissions" then "defaultMode: bypassPermissions" else empty end),
    (if ([.. | objects | has("additionalDirectories")] | any) then "additionalDirectories" else empty end)
  ] | .[]'

# ---------------------------------------------------------------------------
# Sandbox (Doc 02-S) - opt-in. Shown only when a sandbox config exists or when
# you pass --sandbox.
# ---------------------------------------------------------------------------
VS="$VAULT/.claude/settings.json"
GS="$HOME/.claude/settings.json"

SANDBOX=0
[ "$FORCE_SANDBOX" = "1" ] && SANDBOX=1
if [ "$HAS_VAULT" = "1" ] && [ -f "$VS" ] && grep -q '"sandbox"' "$VS" 2>/dev/null; then SANDBOX=1; fi
grep -q '"sandbox"' "$GS" 2>/dev/null && SANDBOX=1

# Doc 02-S Part 3b: the Doc 02 allow list plus the targeted deny list. The
# Stop (sound) hook is optional - 02-S says to delete it if unsure - but an
# empty Stop block fails on every turn, so a present one must hold a hook.
valid_global_security() {
  jtest "$1" '
    type == "object" and
    (.permissions | type == "object") and
    (.permissions.allow | type == "array") and
    (.permissions.deny | type == "array") and
    any(.permissions.deny[]; type == "string" and . == "Read(~/.ssh/**)") and
    all(.permissions.allow[]; type == "string") and
    ([ '"$BROAD_FILTER"' ] | length == 0) and
    ((.hooks.Stop // null) as $stop |
      $stop == null or ($stop | type == "array" and length > 0 and
        all(.[]; (.hooks | type == "array" and length > 0))))
  '
}

# Doc 02-S Part 3a: deny reads of the whole home folder, re-allow only the
# vault (".") and ~/.claude; write nothing extra. Part 3c option B may add one
# named repo, ~/dev/<repo-name>, to allowRead and allowWrite. Nothing broader.
valid_project_security() {
  jtest "$1" '
    .sandbox.enabled == true and
    .sandbox.failIfUnavailable == true and
    .sandbox.allowUnsandboxedCommands == false and
    (.sandbox.filesystem.denyRead | type == "array" and
      any(.[]; type == "string" and (. == "~/" or . == "~" or . == "~/**"))) and
    (.sandbox.filesystem.allowRead | type == "array" and
      all(.[]; type == "string") and
      any(.[]; . == "." or . == "./") and
      any(.[]; . == "~/.claude" or . == "~/.claude/" or . == "~/.claude/**") and
      all(.[]; test("^([.]/?|~/[.]claude(/|/[*][*])?|~/dev/[^/*]+(/|/[*][*])?)$"))) and
    ((.sandbox.filesystem.allowWrite // []) | type == "array" and
      all(.[]; type == "string") and
      all(.[]; test("^([.]/?|~/dev/[^/*]+(/|/[*][*])?)$"))) and
    (.sandbox.network.allowedDomains | type == "array" and
      all(.[]; type == "string" and . != "*")) and
    ([.. | objects | has("additionalDirectories")] | any | not)
  '
}

if [ "$SANDBOX" = "1" ]; then
  head1 "OPT-IN SANDBOX  (Doc 02-S)"
  if valid_global_security "$GS"; then
    check sbxh done "Doc 02-S - hardened global settings (Part 3b)" "credential deny list, no blanket approvals"
  elif ! have jq; then
    check sbxh notdone "Doc 02-S - hardened global settings (Part 3b)" "cannot check without jq"
  else
    check sbxh notdone "Doc 02-S - hardened global settings (Part 3b)" "needs Read(~/.ssh/**) in permissions.deny, no blanket or interpreter approvals, no additionalDirectories"
  fi
  if [ "$HAS_VAULT" = "1" ] && valid_project_security "$VS"; then
    check sbxs done "Doc 02-S - sandbox config in the vault (Part 3a)" ""
  elif [ "$HAS_VAULT" = "0" ]; then
    check sbxs notdone "Doc 02-S - sandbox config in the vault (Part 3a)" "no vault yet - created in the session"
  elif [ ! -f "$VS" ]; then
    check sbxs notdone "Doc 02-S - sandbox config in the vault (Part 3a)" "missing: <vault>/.claude/settings.json"
  elif ! have jq; then
    check sbxs notdone "Doc 02-S - sandbox config in the vault (Part 3a)" "cannot check without jq"
  else
    check sbxs notdone "Doc 02-S - sandbox config in the vault (Part 3a)" "present but not the 02-S Part 3a values"
  fi
  if [ "$HAS_VAULT" = "1" ] && json_valid "$VS"; then
    for k in enabled failIfUnavailable allowUnsandboxedCommands; do
      info "  sandbox.$k" "$(jq -c ".sandbox.$k" "$VS" 2>/dev/null)"
    done
    info "  allowedDomains (count)" "$(jq -c '.sandbox.network.allowedDomains // [] | length' "$VS" 2>/dev/null)"
    if [ "$DETAILS" = "1" ]; then
      for k in denyRead allowRead allowWrite; do
        info "  filesystem.$k" "$(jq -c ".sandbox.filesystem.$k // empty" "$VS" 2>/dev/null)"
      done
    fi
  fi
fi

# ---------------------------------------------------------------------------
# STAGE 2 - Global Claude Code config (Doc 02 STEP 3 / 3.5)
# ---------------------------------------------------------------------------
head1 "STAGE 2 - GLOBAL CLAUDE CODE CONFIG  (Doc 02 STEP 3 / 3.5)"

# Settings values are never printed: settings.json can hold API keys in "env".
if [ ! -f "$GS" ]; then
  check sess notdone "Doc 02 - global settings file is valid" "missing: ~/.claude/settings.json"
elif json_valid "$GS"; then
  check sess done "Doc 02 - global settings file is valid" "~/.claude/settings.json parses"
elif ! have jq; then
  check sess notdone "Doc 02 - global settings file is valid" "cannot check without jq"
else
  check sess notdone "Doc 02 - global settings file is valid" "MALFORMED JSON - none of its settings load"
fi

if json_valid "$GS"; then
  broad=$(jq -r "$BROAD_FILTER" "$GS" 2>/dev/null)
  if [ -z "$broad" ]; then
    check sess done "Doc 02 - no blanket approvals in settings" "no blanket git/cat/head/interpreter rules"
  else
    nb=$(printf '%s\n' "$broad" | wc -l | tr -d ' ')
    check sess notdone "Doc 02 - no blanket approvals in settings" "$nb broad rule(s) found - remove them (--details lists them)"
    if [ "$DETAILS" = "1" ]; then
      printf '%s\n' "$broad" | sed 's/^/         broad rule: /'
    fi
  fi
else
  check sess notdone "Doc 02 - no blanket approvals in settings" "cannot check (settings missing, malformed, or no jq)"
fi

if [ -f "$ROUTER" ]; then
  if [ -n "$ROUTER_VAULT" ] && [ "$HAS_VAULT" = "1" ] && same_dir "$ROUTER_VAULT" "$VAULT"; then
    check sess done "Doc 02 - global router points at the vault" ""
  elif [ -n "$ROUTER_VAULT" ]; then
    check sess notdone "Doc 02 - global router points at the vault" "the router names a different folder than the vault checked here"
  else
    check sess notdone "Doc 02 - global router points at the vault" "~/.claude/CLAUDE.md names no existing <vault>/CLAUDE.md"
  fi
else
  check sess notdone "Doc 02 - global router points at the vault" "missing: ~/.claude/CLAUDE.md"
fi

CTX_OK=0
ctx_why=""
if json_valid "$GS"; then
  if ! jtest "$GS" '(.env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE | tostring) == "75"'; then
    ctx_why="auto-compact threshold is not 75"
  elif ! jtest "$GS" '.statusLine.type == "command" and (.statusLine.command | type == "string" and length > 0)'; then
    ctx_why="statusLine is not configured"
  elif jtest "$GS" '.statusLine.command | contains("statusline.sh")' && [ ! -f "$HOME/.claude/statusline.sh" ]; then
    ctx_why="statusLine points at ~/.claude/statusline.sh, which is missing"
  else
    CTX_OK=1
  fi
else
  ctx_why="cannot check (settings missing, malformed, or no jq)"
fi
if [ "$CTX_OK" = "1" ]; then
  check sess done "Doc 02 - context monitoring (auto-compact 75 + statusline)" ""
  if [ -f "$HOME/.claude/statusline.sh" ] && [ ! -x "$HOME/.claude/statusline.sh" ] && \
     ! jtest "$GS" '.statusLine.command | test("^(bash|sh) ")'; then
    warn "  statusline.sh" "present but not executable (ask Claude to chmod +x it)"
  fi
  if ! jtest "$GS" '(.hooks.UserPromptSubmit | type == "array") and (.hooks.PreCompact | type == "array")'; then
    warn "  context hooks" "UserPromptSubmit / PreCompact hooks not found (Doc 02 Step 3.5 Layers 3-4)"
  fi
else
  check sess notdone "Doc 02 - context monitoring (auto-compact 75 + statusline)" "$ctx_why"
fi

# ---------------------------------------------------------------------------
# STAGE 3 - Vault build (Doc 02)
# ---------------------------------------------------------------------------
head1 "STAGE 3 - VAULT BUILD  (Doc 02)"

inbox=""
missing_folders=""
if [ "$HAS_VAULT" = "1" ]; then
  if [ -d "$VAULT/00 HUB/00 INBOX" ]; then
    inbox="$VAULT/00 HUB/00 INBOX"
  elif [ -d "$VAULT/00 INBOX" ]; then
    inbox="$VAULT/00 INBOX"
  else
    inbox=$(find "$VAULT" -maxdepth 2 -type d -iname "*INBOX" 2>/dev/null | sort | head -1)
  fi
  [ -n "$inbox" ] || missing_folders="INBOX"
  for d in "01 PROJECTS" "02 AREAS" "03 REFERENCE" "04 ARCHIVES" "05 AI/CLAUDE CODE/workspace" "05 AI/CLAUDE CODE/resources" "Templates"; do
    [ -d "$VAULT/$d" ] || missing_folders="${missing_folders:+$missing_folders, }$d"
  done
  if [ -z "$missing_folders" ]; then
    check sess done "Doc 02 - vault folders" "all PARA folders present"
  else
    check sess notdone "Doc 02 - vault folders" "missing: $missing_folders"
  fi

  if [ -f "$VAULT/CLAUDE.md" ]; then
    check sess done "Doc 02 - vault CLAUDE.md" ""
  else
    check sess notdone "Doc 02 - vault CLAUDE.md" "missing"
  fi

  APP="$VAULT/.obsidian/app.json"
  if json_valid "$APP"; then
    off=""
    jtest "$APP" '.newFileLocation == "folder" and ((.newFileFolderPath // "") | test("INBOX"; "i"))' || off="new notes go to INBOX"
    jtest "$APP" '.useMarkdownLinks != true' || off="${off:+$off, }wikilinks"
    jtest "$APP" '.showUnsupportedFiles == true' || off="${off:+$off, }detect all file extensions"
    jtest "$APP" '.alwaysUpdateLinks == true' || off="${off:+$off, }auto-update links"
    if [ -z "$off" ]; then
      check sess done "Doc 02 - Obsidian settings (Files and links)" ""
    else
      check sess notdone "Doc 02 - Obsidian settings (Files and links)" "not set: $off"
    fi
  elif [ -f "$APP" ] && have jq; then
    check sess notdone "Doc 02 - Obsidian settings (Files and links)" "app.json is malformed"
  elif [ -f "$APP" ]; then
    check sess notdone "Doc 02 - Obsidian settings (Files and links)" "cannot check without jq"
  else
    check sess notdone "Doc 02 - Obsidian settings (Files and links)" "not set yet (Doc 02 Step 1.5)"
  fi

  n_proj=$(ls -1 "$VAULT/01 PROJECTS" 2>/dev/null | wc -l | tr -d ' ')
  n_area=$(ls -1 "$VAULT/02 AREAS" 2>/dev/null | wc -l | tr -d ' ')
  info "  items in 01 PROJECTS" "$n_proj"
  info "  items in 02 AREAS" "$n_area"

  jrn=$(find "$VAULT" -maxdepth 4 -iname "*Journey*.md" -not -path "*/.obsidian/*" 2>/dev/null | head -1)
  if [ -n "$jrn" ]; then check sess done "Doc 02 - AIAC Journey brief" ""; else check sess notdone "Doc 02 - AIAC Journey brief" "not found (Step 11.5)"; fi
  cs=$(find "$VAULT" -maxdepth 4 -iname "*Cheat*Sheet*.md" -not -path "*/.obsidian/*" 2>/dev/null | head -1)
  if [ -n "$cs" ]; then check sess done "Doc 02 - AIAC cheat sheet" ""; else check sess notdone "Doc 02 - AIAC cheat sheet" "not found (Step 12.5)"; fi
else
  for l in "Doc 02 - vault folders" "Doc 02 - vault CLAUDE.md" "Doc 02 - Obsidian settings (Files and links)" \
           "Doc 02 - AIAC Journey brief" "Doc 02 - AIAC cheat sheet"; do
    check sess notdone "$l" "no vault yet"
  done
fi

# git identity: never print the name or the address. Only --details shows the
# email domain.
printf '\n'
gn=$(git config --global user.name 2>/dev/null)
ge=$(git config --global user.email 2>/dev/null)
if [ -n "$gn" ] && [ -n "$ge" ]; then
  case "$ge" in
    *users.noreply.github.com) dom="email is a GitHub no-reply address" ;;
    *@*) if [ "$DETAILS" = "1" ]; then dom="email at ...@${ge##*@}"; else dom="email set (not shown)"; fi ;;
    *) dom="email set (not shown)" ;;
  esac
  check sess done "Doc 02 - git identity set" "name set (not shown), $dom"
else
  check sess notdone "Doc 02 - git identity set" "git user.name / user.email not set"
fi

# The code repo: ONLY a repo that the global router names (~/dev/<name>).
# Nothing else in ~/dev is ever looked at.
REPO=""
if [ -f "$ROUTER" ]; then
  names=$(grep -oE '[\\/]dev[\\/][A-Za-z0-9._-]+' "$ROUTER" 2>/dev/null | sed 's|^.dev.||')
  OLDIFS=$IFS; IFS=$NL; set -f
  for nm in $names; do
    case "$nm" in .|..) continue ;; esac
    for cand in "$HOME/dev/$nm" ${VAULT:+"$VAULT/dev/$nm"}; do
      if [ -e "$cand/.git" ]; then REPO=$cand; break 2; fi
    done
  done
  IFS=$OLDIFS; set +f
fi

redact_remote() {
  r=$1
  if [ -z "$r" ]; then printf '%s' "no remote"; return; fi
  # Only recognized network remotes may expose a host. Credentials, user
  # names, ports, paths, queries and fragments are never printed.
  url_remote='^[a-zA-Z][a-zA-Z0-9+.-]*://([^/?#]*@)?(\[[0-9a-fA-F:.]+\]|[a-zA-Z0-9._-]+)(:[0-9]+)?([/?#]|$)'
  scp_remote='^[^/@:[:space:]]+@(\[[0-9a-fA-F:.]+\]|[a-zA-Z0-9._-]+):.+'
  case "$r" in
    [fF][iI][lL][eE]://*) printf '%s' "present (local/unrecognized)"; return ;;
  esac
  if [[ "$r" =~ $url_remote ]]; then
    printf '%s' "present (${BASH_REMATCH[2]})"
  elif [[ "$r" =~ $scp_remote ]]; then
    printf '%s' "present (${BASH_REMATCH[1]})"
  else
    printf '%s' "present (local/unrecognized)"
  fi
}

if [ -n "$REPO" ]; then
  check sess done "Doc 02 - code repo in ~/dev (named in router)" "$(show_path "$REPO")"
  case "$REPO" in
    "$VAULT"/*) warn "  repo location" "inside the vault - Doc 02 puts repos in ~/dev" ;;
  esac
  nc=$(git -C "$REPO" rev-list --count HEAD 2>/dev/null || echo 0)
  rm_raw=$(git -C "$REPO" remote get-url origin 2>/dev/null || true)
  rm_=$(redact_remote "$rm_raw")
  rm_raw=""
  info "  commits" "$nc"
  info "  origin" "$rm_"
  if [ -f "$REPO/CLAUDE.md" ]; then check sess done "Doc 02 - repo CLAUDE.md" ""; else check sess notdone "Doc 02 - repo CLAUDE.md" "missing (Step 8)"; fi
  if [ "${nc:-0}" -gt 0 ] 2>/dev/null; then check sess done "Doc 02 - repo has a first commit" ""; else check sess notdone "Doc 02 - repo has a first commit" "no commits yet (Step 12)"; fi
  case "$rm_" in
    "present (local/unrecognized)"|"no remote") check sess notdone "Doc 02 - repo connected to GitHub" "origin: $rm_" ;;
    *) check sess done "Doc 02 - repo connected to GitHub" "origin: $rm_" ;;
  esac
else
  if [ -f "$ROUTER" ]; then why="the router names no existing ~/dev/<repo> with a .git folder"; else why="no router yet"; fi
  check sess notdone "Doc 02 - code repo in ~/dev (named in router)" "$why"
  check sess notdone "Doc 02 - repo CLAUDE.md" "no repo"
  check sess notdone "Doc 02 - repo has a first commit" "no repo"
  check sess notdone "Doc 02 - repo connected to GitHub" "no repo"
fi

# ---------------------------------------------------------------------------
# STAGE 4 - Skills and plugins (Doc 03)
# ---------------------------------------------------------------------------
head1 "STAGE 4 - SKILLS AND PLUGINS  (Doc 03)"

SKILLS="project-create inbox-clear retro session-close skill-create meeting-minutes"
missing_skills=""
for s in $SKILLS; do
  if [ -f "$HOME/.claude/skills/$s/SKILL.md" ]; then
    info "  skill /$s" "present"
  else
    info "  skill /$s" "missing"
    missing_skills="${missing_skills:+$missing_skills, }/$s"
  fi
done
if [ -z "$missing_skills" ]; then
  check sess done "Doc 03 - starter skills (all 6)" ""
else
  check sess notdone "Doc 03 - starter skills (all 6)" "missing: $missing_skills"
fi

# A plugin counts only if the plugin registry lists an install whose folder
# exists AND settings.json enables it. Marketplace files alone prove nothing.
plugin_ready() {
  registry="$HOME/.claude/plugins/installed_plugins.json"
  json_valid "$registry" && json_valid "$GS" || return 1
  rows=$(jq -r --arg plugin "$1" '
    .plugins | to_entries[]? |
    select(.key | startswith($plugin + "@")) |
    select(.value | type == "array" and length > 0) |
    [.key, (.value[0].installPath // "")] | @tsv' "$registry" 2>/dev/null)
  OLDIFS=$IFS; IFS=$NL; set -f
  for row in $rows; do
    key=${row%%"$TAB"*}
    ipath=${row#*"$TAB"}
    ipath=$(to_unix_path "$ipath")
    if [ -n "$key" ] && [ -d "$ipath" ] && \
       jq -e --arg key "$key" '.enabledPlugins[$key] == true' "$GS" >/dev/null 2>&1; then
      IFS=$OLDIFS; set +f; return 0
    fi
  done
  IFS=$OLDIFS; set +f
  return 1
}

missing_plugins=""
for p in compound-engineering superpowers playground; do
  if plugin_ready "$p"; then
    info "  plugin $p" "installed and enabled"
  else
    info "  plugin $p" "not installed and enabled"
    missing_plugins="${missing_plugins:+$missing_plugins, }$p"
  fi
done
if [ -z "$missing_plugins" ]; then
  check sess done "Doc 03 - plugins (compound-engineering, superpowers, playground)" ""
elif ! have jq; then
  check sess notdone "Doc 03 - plugins (compound-engineering, superpowers, playground)" "cannot check without jq"
else
  check sess notdone "Doc 03 - plugins (compound-engineering, superpowers, playground)" "missing: $missing_plugins (verify with: claude plugin list)"
fi

if [ "$HAS_VAULT" = "1" ] && [ -f "$VAULT/05 AI/CLAUDE CODE/resources/lessons.md" ]; then
  check sess done "Doc 03 - lessons.md" ""
else
  check sess notdone "Doc 03 - lessons.md" "missing (Doc 03 Step 3)"
fi

# ---------------------------------------------------------------------------
# Not checkable from files
# ---------------------------------------------------------------------------
head1 "NOT CHECKED HERE (needs a human)"
printf '    - Your Claude plan is active (Pro is enough to start)\n'
printf '    - Your transcription tool (if any) has microphone / screen permission\n'
printf '    - The repo exists on GitHub and is Private (your facilitator checks this)\n'
printf '    - On a Mac: if the vault is on Desktop or in Documents, iCloud\n'
printf '      "Desktop & Documents Folders" sync is off\n'
[ "$SANDBOX" = "1" ] && printf '    - The /sandbox Config tab shows the rules as RESOLVED\n'
printf '    - The fresh-window router test (a new Claude Code window finds your brief)\n'

# ---------------------------------------------------------------------------
# Verdict - computed only from required checks (optional ones never count).
# ---------------------------------------------------------------------------
home_open=0; sess_open=0; req=0
i=1
while [ "$i" -le "$N" ]; do
  if [ "${C_STATUS[$i]}" != "skip" ]; then
    req=$((req+1))
    if [ "${C_STATUS[$i]}" = "notdone" ]; then
      case "${C_GROUP[$i]}" in
        home|sbxh) home_open=$((home_open+1)) ;;
        *) sess_open=$((sess_open+1)) ;;
      esac
    fi
  fi
  i=$((i+1))
done

if [ "$PLATFORM" = "unsupported" ]; then
  VERDICT="VERDICT: UNSUPPORTED OPERATING SYSTEM - check by hand with your facilitator"
elif [ "$PRE_SESSION" = "1" ]; then
  if [ "$home_open" = "0" ]; then
    VERDICT="VERDICT: PRE-SESSION - homework complete, ready for the session"
  else
    VERDICT="VERDICT: PRE-SESSION - homework not complete ($home_open item(s) NOT DONE)"
  fi
elif [ $((home_open+sess_open)) = "0" ]; then
  VERDICT="VERDICT: PHASE 0 SETUP COMPLETE - all $req required checks DONE"
else
  VERDICT="VERDICT: IN PROGRESS - $((home_open+sess_open)) of $req required checks NOT DONE"
fi

status_word() {
  case "$1" in
    done) printf '%s' "DONE" ;;
    skip) printf '%s' "SKIPPED (optional)" ;;
    *) printf '%s' "NOT DONE" ;;
  esac
}

print_group() {  # print_group GROUP_A GROUP_B
  i=1
  while [ "$i" -le "$N" ]; do
    case "${C_GROUP[$i]}" in
      "$1"|"$2") printf '%s: %s\n' "${C_LABEL[$i]}" "$(status_word "${C_STATUS[$i]}")" ;;
    esac
    i=$((i+1))
  done
}

# The safe-to-share block. Only fixed check names, statuses, the OS and the
# verdict are printed here - never a path, name, address, URL or setting value.
printf '\n'
printf '%s\n' "Share ONLY the block below. Copy every line from the first ----- line to the last."
printf '\n'
printf '%s\n' "----- AIAC STATUS (safe to share) -----"
printf 'Status check: v%s\n' "$VERSION"
printf 'OS: %s\n' "$PLATFORM"
printf '%s\n' "BEFORE THE SESSION:"
print_group home sbxh
printf '%s\n' "BUILT IN THE SESSION:"
print_group sess sbxs
printf '%s\n' "$VERDICT"
printf '%s\n' "----- END -----"
if [ "$DETAILS" = "1" ]; then
  printf '\n%s\n' "*** --details was ON: do NOT share the details above. Share only the block. ***"
fi
exit 0
