#!/usr/bin/env bash
# The required privacy check for a pull request, run by CI from the BASE
# checkout. The pull request is only DATA here: its commits are git objects
# this script reads with git and bin/gate_scan.py. Nothing from the pull
# request is checked out, imported or executed, and the scanner and pattern
# lists are this checkout's (the base's), so a pull request cannot loosen the
# gate that judges it.
#
#   bash bin/gate_pr_check.sh <base-commit> <head-commit>
#
# <head-commit> must already be in the object store and reachable from a ref
# (CI fetches it into refs/gate/pr-head), so --history walks it.
# Runs all three checks even when one fails, then exits with the worst code:
# 0 = clean   1 = blocked   3 = a check could not run (never reported clean)
set -uo pipefail

die() {
  echo "GATE ERROR: $1" >&2
  echo "Refusing to certify: a check that cannot run never reports clean." >&2
  exit 3
}

[ "$#" -eq 2 ] || die "usage: gate_pr_check.sh <base-commit> <head-commit>"

here=$(cd "$(dirname "$0")" && pwd) || die "cannot locate bin/."
top=$(git rev-parse --show-toplevel) || die "not inside a git repository."
cd "$top" || die "cannot enter the repository."

base=$(git rev-parse --verify --quiet "$1^{commit}") \
  || die "cannot resolve the base commit."
head=$(git rev-parse --verify --quiet "$2^{commit}") \
  || die "cannot resolve the head commit."
reachable=$(git for-each-ref --contains "$head" --count=1 --format=x) \
  || die "git for-each-ref failed."
[ -n "$reachable" ] \
  || die "the head commit is not reachable from any ref, so --history would skip it."

tmp=$(mktemp -d) || die "cannot create a temporary directory."
trap 'rm -rf "$tmp"' EXIT

worst=0
record() {
  if [ "$1" -eq 3 ] || { [ "$1" -ne 0 ] && [ "$1" -ne 1 ]; }; then
    worst=3
  elif [ "$1" -eq 1 ] && [ "$worst" -eq 0 ]; then
    worst=1
  fi
}

echo "== gate surface pin"
bash "$here/gate_surface_pin.sh" "$base" "$head"
record $?

# The pull request's files, read from a throwaway index built from its tree.
# read-tree only writes index entries: no checkout, no filters, no hooks.
echo "== private-data gate: files in the pull request"
if GIT_INDEX_FILE="$tmp/index" git read-tree "$head"; then
  GIT_INDEX_FILE="$tmp/index" python3 "$here/gate_scan.py" --tree
  record $?
else
  echo "GATE ERROR: cannot read the pull request's tree." >&2
  record 3
fi

echo "== private-data gate: full history, including the pull request's commits"
python3 "$here/gate_scan.py" --history
record $?

exit "$worst"
