# TASK-0005 — Orbit-linearized validated-history feasibility

**From:** Chief Researcher  
**To:** Compute Agent  
**Date:** 2026-09-30  
**Priority:** P0 / TARGET-A20 COMPUTATIONAL CLOSURE

## Goal

Replace the pessimistic scalar-norm amplification of TASK-0004 by a sign-aware / matrix-aware validation around the computed nonlinear orbit.

Read:
- \`research/VALIDATED_HISTORY_STRATEGY.md\`;
- \`research/coordination/compute-to-chief/TASK-0004_memory-tail-survival_RETURN.md\`.

Until ROUND-0006 returns, theorem-level claims based on V1 are **CONDITIONAL**.

## Stage A — discrete orbit-linearized amplification

For W1 and the lowest-amplification M1-feasible witnesses from TASK-0004, construct the discretized linearized Volterra operator
\[
\mathcal L_{\hat x}
=
I-I^\alpha[Dg(\hat x(\cdot))\,\cdot].
\]

Use the existing collocation/PECE history and compute the action of its inverse without taking absolute matrix norms at every step.

Measure:
- induced amplification from a cellwise defect vector to state error;
- worst singular value / norm of the discrete inverse in several scalings;
- location in time of the amplification peak.

Compare directly against:
- TASK-0004 Theorem-R amplification;
- observed initial-condition sensitivity.

**Gate:** if the sign-aware amplification remains \(>10^4\) for every candidate/norm, stop before building rigorous machinery.

## Stage B — choose the benchmark

Do not assume W1 is optimal.

Among the exact-rational or easily rationalizable entering witnesses, optimize:
1. M1 feasibility margin;
2. sign-aware linearized amplification;
3. entry margin;
4. parameter simplicity.

Produce a Pareto shortlist.

Any successful witness may close TARGET-A20.

## Stage C — higher-order approximation only if needed

If Stage A yields manageable amplification, build piecewise polynomial \(\phi\) of degree \(d=2,3,5\) on a graded/adaptive mesh.

Requirements:
- exact closed form for \(I^\alpha\phi\) or rigorous polynomial quadrature;
- explicit treatment of the initial fractional singular layer;
- rigorous residual enclosure;
- measured residual order under refinement.

Do not use high order merely to improve floating accuracy; it must reduce the **validated defect**.

## Stage D — approximate-inverse / interval validation prototype

Implement a finite-dimensional lower-triangular approximate inverse \(B\) for the collocation derivative.

Compute rigorous or semi-rigorous pilot quantities corresponding to:
\[
Y=\|B d\|,
\qquad
Z_1=\|I-B\mathcal L_{\hat x}\|,
\qquad
Z_2(r).
\]

Before claiming a theorem, keep operator-tail/interpolation terms explicit.

If ROUND-0006 supplies a compatible Newton/radii theorem, upgrade these to rigorous bounds.

## Stage E — goal-oriented \(M_T\) option

In parallel, test whether the history error can be propagated directly to
\[
v_T(t)
=
E_\alpha(Jt^\alpha)u_0+
\int_0^T\Psi_J(t-s)N(u(s))\,ds
\]
without requiring a tiny uniform state tube.

Estimate the dual/functional amplification from local history defects to \(M_T\).

If this is substantially smaller than uniform-state amplification, prioritize it.

## Stage F — final certificate attempt

If a rigorous orbit enclosure or goal-oriented history bound becomes available, combine it with the already available M1 constants.

For W1 the target remains:
\[
M_T<0.038078.
\]

A successful strict M1 inequality closes TARGET-A20.

## Return

Write:
\`research/coordination/compute-to-chief/TASK-0005_orbit-linearized-history_RETURN.md\`

Report:
- sign-aware amplification;
- candidate ranking;
- high-order residual orders if attempted;
- approximate-inverse/radii quantities;
- whether a rigorous \(M_T\) is obtained;
- exact limitations.
