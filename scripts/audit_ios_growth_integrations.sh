#!/usr/bin/env bash
# Backward-compatible entry point; never print source lines or config values.
set -euo pipefail
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3.9+ is required. Run the .py helper with your interpreter." >&2
  exit 2
fi
exec python3 "$SCRIPT_DIR/audit_ios_growth_integrations.py" "$@"
