#!/usr/bin/env bash
# Push computations/ to ORION and pull generated data/figures back.
# Usage: sync_orion.sh push | pull
set -euo pipefail
LOCAL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE="orion:~/msbg/computations"
case "${1:-push}" in
  push)
    rsync -az --delete --exclude='__pycache__' --exclude='.pytest_cache' \
          --exclude='data/' --exclude='figures/' --exclude='manifests/' \
          "$LOCAL/" "$REMOTE/"
    ;;
  pull)
    rsync -az "$REMOTE/data/" "$LOCAL/data/" || true
    rsync -az "$REMOTE/figures/" "$LOCAL/figures/" 2>/dev/null || true
    rsync -az "$REMOTE/manifests/" "$LOCAL/manifests/" || true
    ;;
  *) echo "usage: $0 push|pull" >&2; exit 2;;
esac
