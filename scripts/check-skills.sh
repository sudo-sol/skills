#!/usr/bin/env bash
# Offline package validation; does not test live agent behavior.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 scripts/check_skills.py
