#!/usr/bin/env bash
# .git/hooks is NOT cloned. core.hooksPath is what makes a fresh clone safe.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
git config core.hooksPath .githooks
echo "core.hooksPath = $(git config core.hooksPath)"
