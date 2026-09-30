# Compute Backlog

## Completed

TASK-0001 through TASK-0006 complete.

TASK-0006 proves B215 survival and closes TARGET-A20 under the declared arithmetic model.

## Active

### TASK-0007 — publication arithmetic hardening

Request:
\`research/coordination/chief-to-compute/TASK-0007_publication-arithmetic-hardening_REQUEST.md\`

Goal:
remove the few-ulp libm assumption from the primary \(T=300,N=12000\) certificate where practical, and audit remaining binary64/BLAS roundoff assumptions.

This is not a novelty gate.

## After TASK-0007

No further compute work is mandatory for the first manuscript unless referee-style internal audit exposes a gap.
