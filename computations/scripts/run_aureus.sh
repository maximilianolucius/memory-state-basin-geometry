#!/usr/bin/env bash
# Launch a stage script on AUREUS, detached and niced.
# Usage: THREADS=8 run_aureus.sh <script.py> [args...]
# THREADS defaults to 1 (right for multi-process stages); set it higher for
# single-process stages so BLAS can use the machine.
set -euo pipefail
SCRIPT="$1"; shift || true
NAME="$(basename "$SCRIPT" .py)"
TH="${THREADS:-1}"
ssh -o BatchMode=yes aureus "cd ~/msbg/computations && \
  env OMP_NUM_THREADS=$TH OPENBLAS_NUM_THREADS=$TH MKL_NUM_THREADS=$TH NUMEXPR_NUM_THREADS=$TH \
  setsid nice -n 10 ../venv/bin/python -u $SCRIPT $* > /tmp/${NAME}.log 2>&1 < /dev/null &
  sleep 3; echo launched ${NAME} on AUREUS with $TH thread(s)"
