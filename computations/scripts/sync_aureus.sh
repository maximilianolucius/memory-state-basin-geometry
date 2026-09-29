#!/usr/bin/env bash
# Push computations/ to AUREUS and pull generated artifacts back.
# Key-based auth (ssh alias "aureus" in ~/.ssh/config); no credentials in this file.
set -euo pipefail
LOCAL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE="aureus:~/msbg/computations"
case "${1:-push}" in
  push) rsync -az --delete --exclude='__pycache__' --exclude='.pytest_cache' \
             --exclude='data/' --exclude='figures/' --exclude='manifests/' "$LOCAL/" "$REMOTE/" ;;
  pull) for d in data figures manifests; do rsync -az "$REMOTE/$d/" "$LOCAL/$d/" 2>/dev/null || true; done ;;
  *) echo "usage: $0 push|pull" >&2; exit 2;;
esac
