# Structural Theorems — Basin Entry Geometry

**Owner:** Chief Researcher  
**Date:** 2026-09-29  
**Status:** E1/E2/E3/E4 PROVED; MODEL-SPECIFIC SURVIVAL BASIN OPEN

## E1 — basin-entry criterion

If
\[
\iota(U_-)\subseteq\mathcal B(A_-),
\quad
\iota(p)\in\mathcal B(A_+),
\quad A_-\ne A_+,
\]
and
\[
z=P(p,t_*)\in U_-,
\]
then
\[
T_{t_*}\iota(p),\ \iota(z)\in\mathcal F_z
\]
belong to different basins.

Hence \(\mathcal F_z\) is multibasin.

## E1-A — arc criterion

If the same orbit remains in \(U_-\) over a nondegenerate time interval, every reached present state along that interval has a multibasin reachable fiber.

## E2 — open persistence

Strict entry persists by continuity. Open-family persistence of the full phenomenon additionally requires persistence of both basin memberships.

No transversality/IFT is required for basic existence.

## E3 — physical convergence lifts to compact-open continuation convergence

If a standard physical IVP satisfies
\[
x(t;p)\to x^*,\qquad g(x^*)=0,
\]
then
\[
T_t\iota(p)\to\iota(x^*)
\]
in the compact-open topology.

For each fixed \(N\),
\[
\sup_{0\le\eta\le N}
\|(T_t\iota(p))(\eta)-x^*\|\to0.
\]

## E4 — tail anchoring of finite-time continuation states

Assume the physical orbit is bounded on \([0,T]\). For fixed \(T>0\),
\[
(T_T\iota(p))(\tau)
=
p+
\frac1{\Gamma(\alpha)}
\int_0^T
(T+\tau-s)^{\alpha-1}g(x(s))\,ds.
\]

Thus
\[
\|(T_T\iota(p))(\tau)-p\|
\le
\frac{M}{\Gamma(\alpha+1)}
\left[(T+\tau)^\alpha-\tau^\alpha\right],
\]
where
\[
M=\sup_{0\le s\le T}\|g(x(s))\|.
\]

Since \(0<\alpha<1\),
\[
(T+\tau)^\alpha-\tau^\alpha\to0
\qquad(\tau\to\infty).
\]

Therefore
\[
(T_T\iota(p))(\tau)\to p
\qquad(\tau\to\infty).
\]

### Consequence

If \(p\ne x^*\),
\[
\sup_{\tau\ge0}
\|(T_T\iota(p))(\tau)-x^*\|
\ge
\|p-x^*\|.
\]

Hence convergence in E3 cannot generally be strengthened to the unweighted global sup norm on \(C(\mathbb R_+,\mathbb R^d)\).

The compact-open topology is structurally essential.

## Current model-specific route

X1 already proves
\[
\iota(R_{\rm ext})\subseteq\mathcal B(0).
\]

TASK-0002 certifies that several standard orbits enter \(R_{\rm ext}\).

The remaining problem is to certify one such initial state as belonging to the survival basin.

The preferred route is now CANDIDATE-L1 in
\`research/LOCAL_SURVIVAL_BASIN.md\`.
