#!/usr/bin/env bash
# Thin wrapper: builds data/kenya.db from data/approved/kenya_administrative.json
# (see data/approved/README.md for what that data is and where it's from).
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON="python3"
[ -x "${REPO_ROOT}/.venv/bin/python3" ] && PYTHON="${REPO_ROOT}/.venv/bin/python3"
"${PYTHON}" "${REPO_ROOT}/database/seeds/load_approved_data.py" "${REPO_ROOT}/data/kenya.db"
