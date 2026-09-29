#!/usr/bin/env bash
# Launch a stage script on ORION, detached and niced.
# Usage: THREADS=8 run_orion.sh <script.py> [args...]
# THREADS defaults to 1: ORION is a shared host and the multi-process stages
# must not oversubscribe it with nested BLAS threads.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPT="$1"; shift || true
NAME="$(basename "$SCRIPT" .py)"
TH="${THREADS:-1}"
GC="$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
GB="$(git -C "$ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
GD="$(git -C "$ROOT" status --porcelain 2>/dev/null | head -c1 | wc -c)"
ssh -o BatchMode=yes orion "cd ~/msbg/computations && env \
  MSBG_GIT_COMMIT='$GC' MSBG_GIT_BRANCH='$GB' MSBG_GIT_DIRTY='$GD' \
  OMP_NUM_THREADS=$TH OPENBLAS_NUM_THREADS=$TH MKL_NUM_THREADS=$TH NUMEXPR_NUM_THREADS=$TH \
  setsid nice -n 15 ../venv/bin/python -u $SCRIPT $* > /tmp/${NAME}.log 2>&1 < /dev/null & \
  sleep 3; echo launched ${NAME} on ORION with $TH thread\(s\)"
