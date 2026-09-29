#!/usr/bin/env bash
# Launch a stage script on AUREUS, detached and niced.
# Usage: THREADS=8 run_aureus.sh <script.py> [args...]
# THREADS defaults to 1 (right for multi-process stages); raise it for
# single-process stages so BLAS can use the machine.
# The local git SHA is exported so the remote manifest records which commit the
# rsync'd tree corresponds to (the remote copy is not a checkout).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPT="$1"; shift || true
NAME="$(basename "$SCRIPT" .py)"
TH="${THREADS:-1}"
GC="$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
GB="$(git -C "$ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
GD="$(git -C "$ROOT" status --porcelain 2>/dev/null | head -c1 | wc -c)"
ssh -o BatchMode=yes aureus "cd ~/msbg/computations && env \
  MSBG_GIT_COMMIT='$GC' MSBG_GIT_BRANCH='$GB' MSBG_GIT_DIRTY='$GD' \
  OMP_NUM_THREADS=$TH OPENBLAS_NUM_THREADS=$TH MKL_NUM_THREADS=$TH NUMEXPR_NUM_THREADS=$TH \
  setsid nice -n 10 ../venv/bin/python -u $SCRIPT $* > /tmp/${NAME}.log 2>&1 < /dev/null & \
  sleep 3; echo launched ${NAME} on AUREUS with $TH thread\(s\)"
