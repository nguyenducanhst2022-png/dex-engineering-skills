#!/usr/bin/env bash
# ==============================================================================
# DEX Polyglot Script Engine v7.0 / v8.0 — Unix Shell Wrapper
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
DEX_PY="${REPO_ROOT}/scripts/polyglot/dex.py"

if [ ! -f "${DEX_PY}" ]; then
    echo "[ERROR] Cannot locate dex.py at ${DEX_PY}" >&2
    exit 1
fi

PYTHON_CMD=""
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "[ERROR] Python 3 is required but not found in PATH." >&2
    exit 127
fi

exec "${PYTHON_CMD}" "${DEX_PY}" "$@"
