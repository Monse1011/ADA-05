#!/usr/bin/env bash
# Single verification entry point for this repository (local and CI).
# Usage: scripts/verify_repo.sh            (uses $PYTHON, else .venv/bin/python, else python3)
#        PYTHON=~/.venv/bin/python scripts/verify_repo.sh
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ -z "${PYTHON:-}" ]]; then
  if [[ -x .venv/bin/python ]]; then PYTHON=.venv/bin/python; else PYTHON=python3; fi
fi
echo "==> Python: $("$PYTHON" --version 2>&1) ($PYTHON)"

# pyproject.toml declares requires-python >=3.10. Warn (not fail): the accepted ADA-08
# BEFORE/AFTER environment is Python 3.9.6 (see AGENTS.md, "Environment").
if ! "$PYTHON" -c 'import sys; sys.exit(sys.version_info < (3, 10))'; then
  echo "WARNING: pyproject.toml requires Python >=3.10; results on this interpreter are not authoritative."
fi

if ! "$PYTHON" -c 'import pytest' 2>/dev/null; then
  echo "ERROR: pytest is not installed for $PYTHON."
  echo "       Install dev dependencies:  $PYTHON -m pip install -e '.[dev]'"
  exit 2
fi

echo "==> Repository contract"
"$PYTHON" scripts/check_repo_contract.py

echo "==> Tests"
"$PYTHON" -m pytest -v -p no:cacheprovider

echo "==> verify_repo: OK"
