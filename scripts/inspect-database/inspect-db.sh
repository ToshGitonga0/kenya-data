#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON="python3"
[ -x "${REPO_ROOT}/.venv/bin/python3" ] && PYTHON="${REPO_ROOT}/.venv/bin/python3"
"${PYTHON}" "${REPO_ROOT}/database/scripts/inspect_db.py" "$@"
