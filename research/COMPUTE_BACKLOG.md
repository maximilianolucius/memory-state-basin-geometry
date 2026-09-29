# Compute Backlog

## Dispatch status

**TASK-0001 dispatched 2026-09-29:**  
`research/coordination/chief-to-compute/TASK-0001_validated-collision-search_REQUEST.md`

TASK-0001 stages C-A001, C-A002, C-A010, C-A020 and C-A021 in that order, with C-A022 attempted only when a robust refined candidate exists.

## P0 — infrastructure

### C-A001 — Caputo solver validation
status: DISPATCHED / TASK-0001  
Build two independent history-retaining solvers and validate on known Mittag-Leffler solutions.

Acceptance:
- convergence test;
- long-horizon test;
- reproducible environment;
- regression tests.

### C-A002 — Cong–Tuan intersection reproduction
status: DISPATCHED / TASK-0001  
Reproduce the published higher-dimensional intersection construction numerically/high precision.

Purpose: validate noninjective present-state observation and exercise collision-detection machinery. This is not new mathematics.

## P1 — application baseline

### C-A010 — Double-Allee reproduction
status: DISPATCHED / TASK-0001, conditional on C-A001/C-A002 PASS  
Reproduce equilibria, local stability and multistable/basin regime for one published fractional Double-Allee model, preferably Mondal et al. 2025.

Acceptance:
- parameter provenance;
- two-solver cross-check;
- mesh/horizon sensitivity;
- raw data saved.

## P1 — multibasin discovery

### C-A020 — near-collision search
status: DISPATCHED / TASK-0001, conditional on validated baseline  
Search pairs of standard physical IVPs producing same/near-same current physical state and different conservative long-run outcomes.

Search both same-age and cross-age collisions.

### C-A021 — root refinement
status: DISPATCHED / TASK-0001 after robust near-collision  
Formulate candidate physical-state collisions as nonlinear root problems and refine at arbitrary precision.

Also estimate rank/singular values of the collision Jacobian for candidate theorem M2.

### C-A022 — interval certification
status: QUEUED  
Certify candidate collision/transversality conditions with interval arithmetic when feasible.

## P2 — structural atlases

### C-A030 — alpha/parameter atlas
Map candidate behavior over a declared parameter/order family.

### C-A031 — monotonicity stress tests
Test sign classes where comparison theory predicts purity.

## P3 — publication figures
Only after theorem hypotheses are known:
- theorem-region atlas;
- memory-fiber/basin schematic;
- certified collision panel;
- robustness/open-set panel;
- solver convergence;
- horizon sensitivity;
- multiple initial histories.

Every figure must answer a theorem-level question.
