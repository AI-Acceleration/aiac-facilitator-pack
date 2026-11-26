#!/usr/bin/env bash
# Fails when a change touches the gate surface: .githooks/, bin/, .github/
# and CODEOWNERS (which decides who must review the rest).
#
#   bash bin/gate_surface_pin.sh <base-commit> <head-commit>
#
# Compares <head-commit> with its merge base with <base-commit>, so only the
# change's own edits count (a branch that is merely behind main passes).
# Exit codes: 0 = surface untouched   1 = surface changed   3 = could not run
#
# CI logs are public, and a file NAME can carry an address or other private
# text. So this script never prints a file name: it prints a fixed message
# and a count, and discards git's own error output (which can quote a path
# or ref name) in favour of a fixed message. To list the files, run locally:
#   git diff --name-only <base-commit>...<head-commit> -- .githooks bin .github \
#       CODEOWNERS docs/CODEOWNERS
set -uo pipefail

# CODEOWNERS: GitHub reads .github/CODEOWNERS (covered above), then
# /CODEOWNERS, then docs/CODEOWNERS. Pinning all three means a pull request
# cannot drop or reroute the security-owner review of this surface.
# tests/ is deliberately NOT pinned: tests never run in the gate job (CI
# runs main's scanner on the pull request's objects), so a test edit cannot
# change what the gate sees; it only changes the pull request's own test run.
SURFACE=(.githooks bin .github CODEOWNERS docs/CODEOWNERS)

die() {
  echo "GATE ERROR: $1" >&2
  echo "Refusing to certify: a check that cannot run never reports clean." >&2
  exit 3
}

[ "$#" -eq 2 ] || die "usage: gate_surface_pin.sh <base-commit> <head-commit>"

base=$(git rev-parse --verify --quiet "$1^{commit}" 2>/dev/null) \
  || die "cannot resolve the base commit."
head=$(git rev-parse --verify --quiet "$2^{commit}" 2>/dev/null) \
  || die "cannot resolve the head commit."
merge_base=$(git merge-base "$base" "$head" 2>/dev/null) \
  || die "the head commit shares no history with the base commit."

tmp=$(mktemp -d) || die "cannot create a temporary directory."
trap 'rm -rf "$tmp"' EXIT

# NUL-separated, written to a file: names are counted, never echoed, and a
# name holding a space or newline still counts once.
git diff --name-only -z --no-renames "$merge_base" "$head" -- "${SURFACE[@]}" \
  > "$tmp/names" 2>/dev/null || die "git diff failed (its message is not printed: CI logs are public)."
count=$(tr -cd '\000' < "$tmp/names" | wc -c | tr -d ' ')

if [ "$count" -ne 0 ]; then
  echo "BLOCKED: this change edits the gate surface ($count path(s) under"
  echo ".githooks/, bin/, .github/ or CODEOWNERS). File names are not printed:"
  echo "CI logs are public. Those paths decide what the gate can see and who"
  echo "reviews it, so a change to them is a security review: maintainer"
  echo "review, then an admin merge."
  echo "See CONTRIBUTING.md, \"Changing the gate itself\"."
  exit 1
fi
echo "gate surface pin: .githooks/ bin/ .github/ CODEOWNERS unchanged since ${merge_base:0:12}."
exit 0
