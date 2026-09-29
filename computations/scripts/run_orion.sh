#!/usr/bin/env bash
# Launch a stage script on ORION, detached, single-threaded BLAS per worker, niced.
# Usage: run_orion.sh <script.py> [args...]
set -euo pipefail
SCRIPT="$1"; shift || true
NAME="$(basename "$SCRIPT" .py)"
ssh -o BatchMode=yes orion "cd ~/msbg/computations && \
  env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  setsid nice -n 15 ../venv/bin/python -u $SCRIPT $* > /tmp/${NAME}.log 2>&1 < /dev/null &
  sleep 3; echo launched ${NAME}"
