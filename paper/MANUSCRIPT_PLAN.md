# Manuscript Plan

**Status:** CORE SECTIONS 1--8 WRITTEN IN LATEX  
**Target length:** 22--23 pages; hard maximum 25 pages.

## Working title candidates

Current preferred:

**Multibasin Reachable Present-State Fibers in an Autonomous Caputo System**

Alternatives:

- **Reachable Present-State Fibers Crossing Extinction and Coexistence Basins in an Autonomous Caputo System**
- **Same Present, Different Basins in an Autonomous Caputo System: A Certified Extinction--Coexistence Split**

The final title must avoid “first” and foreground the basin theorem rather than the ecological model alone.

## Core theorem statement

For the exact B215 system
[
{}^CD^{17/20}x=x(1-x)(x-1/2)-\tfrac12xy,
\qquad
{}^CD^{17/20}y=y(x-4/5),
]
with
[
p=(277/100,467/1000),
]
the exact standard trajectory enters the cold-start extinction strip throughout a nondegenerate certified time interval while the inherited trajectory converges to
[
E^*=(4/5,3/25).
]

Thus, for every certified entry time (t_*), the inherited continuation state and canonical cold start at the identical reached present (X(t_*;p)) lie in distinct asymptotic basins.

## Section architecture

1. Introduction and precise contribution.
2. Caputo continuation states and present-state fibers.
3. Scalar purity contrast.
4. Strong-Allee model and analytic basin certificates.
5. Certified multibasin fiber theorem.
6. Computer-assisted validation.
7. Geometry and interpretation.
8. Discussion and limitations.
9. References/declarations.

All Sections 1--8 now exist in `paper/sections/`.

## Figure plan

Target 8 figure environments / approximately 12--16 panels:

1. continuation-state fiber geometry;
2. B215 physical excursion and extinction strip;
3. certified threshold crossing in time;
4. inherited continuation versus cold-start future from the same present;
5. CAP tube;
6. sign-aware versus absolute-value amplification;
7. adaptive mesh and defect localization;
8. memory-tail budget and independent certificate comparison.

See `paper/FIGURE_SPECIFICATIONS.md`.

## Tables

Keep to 2--3 compact tables:
- theorem/certificate constants;
- closest-prior comparison;
- evidence hierarchy or redundancy summary.

## Precision lock

The manuscript states a nondegenerate **time interval** on which every reached present value has a multibasin fiber.

Injectivity of
[
t\mapsto X(t;p)
]
on (I_*) is not currently certified, so do not claim a topological arc of distinct fibers.

## Remaining editorial steps

1. theorem-level figures;
2. page-budget compression;
3. TASK-0007 arithmetic update;
4. final title/abstract freeze;
5. journal-template conversion.
