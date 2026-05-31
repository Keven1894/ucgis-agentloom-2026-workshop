#!/usr/bin/env bash
# Build attendee-facing workshop repo. Wrapper for build_workshop_snapshot.py.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python scripts/build_workshop_snapshot.py "$@"
