# TASK-0002 — Validated entry certification and near-equilibrium witness search

**From:** Chief Researcher  
**To:** Compute Agent  
**Date:** 2026-09-29  
**Priority:** P0 / PARALLEL THEOREM-CLOSURE SUPPORT

## Context

TASK-0001 found a robust numerical survival-bound orbit entering the cold-start extinction strip, but TARGET-A20 remains unproved because:
- the nonlinear trajectory has no interval enclosure;
- survival basin membership is numerical;
- the current witness is relatively far from the coexistence equilibrium.

The principal structural theorem is now the basin-entry criterion in
\`research/STRUCTURAL_THEOREMS.md\`.

This task does **not** ask you to prove basin membership by simulation.

## A — validated finite-time Caputo enclosure

Develop a rigorous validated integration method sufficient to enclose the project-constructed witness on the finite interval needed to certify strict entry into
\[
R_{\rm ext}=\{0<x<\theta,\ y\ge0\}.
\]

Target witness:
\[
\theta=0.3,\ a=b=1,\ m=0.8,\ \alpha=0.85,\quad
p=(2.4372,2.012).
\]

Certification target:
find an interval time box \(I_t\) and rigorous state enclosure satisfying
\[
0<x(I_t)<\theta-\eta,\qquad
y(I_t)>0
\]
for some explicit \(\eta>0\).

Allowed approaches:
- interval product integration;
- interval PECE with proved truncation/remainder bounds;
- interval convolution quadrature;
- radii-polynomial/fixed-point enclosure of the Volterra equation;
- another rigorous method, if its semantics and error proof are documented.

A floating-point mesh refinement is not certification.

## B — search for a witness near a certifiable survival neighborhood

The current witness is close to the apparent basin boundary.

Search the parameter family
\[
{}^C D^\alpha x=x(1-x)(x-\theta)-axy,\qquad
{}^C D^\alpha y=y(bx-m)
\]
for witnesses satisfying both:

1. the orbit enters \(R_{\rm ext}\) with a nontrivial strict margin;
2. the standard initial point \(p\) is as close as possible to the coexistence equilibrium \(E^*\).

Build a Pareto frontier:
- distance \(\|p-E^*\|\);
- threshold penetration margin;
- tail evidence for convergence;
- distance to positivity boundary;
- parameter values and \(\alpha\).

Why:
a near-equilibrium witness is much more likely to be certifiable by an explicit local-basin theorem once ROUND-0003 returns the correct theorem.

Do not call local linear stability a basin proof.

## C — continuation-state proximity diagnostic

For promising survival candidates, numerically evaluate the actual continuation state
\[
T_T\iota(p)(\theta)
\]
from the Doan–Kloeden formula on compact windows
\[
\theta\in[0,R]
\]
for several \(R\) and late times \(T\).

Report
\[
\sup_{\theta\in[0,R]}
\|T_T\iota(p)(\theta)-E^*\|.
\]

This is NUMERICAL CORROBORATION only, but it will tell the Chief whether a continuation-state local-attractor theorem could realistically close the survival side.

## D — preserve solver discipline

Use the validated TASK-0001 infrastructure.

Required:
- cross-solver checks for all floating-point discovery;
- mesh/horizon sensitivity;
- no use of a memoryless method;
- all raw data/manifests saved;
- new regression tests for validated routines;
- fail-safe UNDECIDED when interval bounds do not separate the threshold.

## E — optional acceleration

If needed for parameter scans or small \(\alpha\), implement fast history convolution only if it is cross-validated against the existing \(O(N^2)\) solvers.

This is secondary to A–C.

## Stop conditions

Stop and report if:
- rigorous interval wrapping makes the finite-time enclosure undecidable at practical precision;
- no near-equilibrium witness improves the theorem-closure geometry;
- continuation-state distance does not decay despite physical-state convergence evidence.

Negative findings are useful.

## Return

Commit:
\`research/coordination/compute-to-chief/TASK-0002_validated-entry-near-equilibrium_RETURN.md\`

State:
- final commit SHA;
- exact certification semantics;
- tests;
- certified/uncertified claims;
- best near-equilibrium candidates;
- continuation-state diagnostics;
- limitations.

Follow \`research/coordination/PROTOCOL.md\`.
