# Structural Theorems — Basin Entry Geometry

**Owner:** Chief Researcher  
**Date:** 2026-09-30  
**Status:** E1/E2/E3/E4 PROVED / E1 REALIZED BY B215

## E1 — basin-entry criterion

If
\[
\iota(U_-)\subseteq\mathcal B(A_-),
\quad
\iota(p)\in\mathcal B(A_+),
\quad
A_-\ne A_+,
\]
and
\[
z=X(t_*;p)\in U_-,
\]
then
\[
T_{t_*}\iota(p),\ \iota(z)\in\mathcal F_z
\]
belong to different basins.

Hence \(\mathcal F_z\) is multibasin.

## E1-A — time-interval criterion

If the same orbit remains in \(U_-\) for every \(t\) in a nondegenerate time interval \(I\), then
\[
\mathcal F_{X(t;p)}
\]
is multibasin for every \(t\in I\).

No injectivity of \(t\mapsto X(t;p)\) is assumed or claimed.

## E2 — open persistence

Strict physical entry persists by continuity.  Open-parameter persistence of the full basin-splitting phenomenon additionally requires persistence of the two basin memberships.

This has not been quantified for the final B215 theorem and is not a current manuscript claim.

## E3 — physical convergence lifts to compact-open continuation convergence

If
\[
X(t;p)\to X^*,\qquad g(X^*)=0,
\]
then
\[
T_t\iota(p)\to\iota(X^*)
\]
in the compact-open topology.

For every fixed \(N\),
\[
\sup_{0\le\eta\le N}
\|(T_t\iota(p))(\eta)-X^*\|\to0.
\]

## E4 — tail anchoring

For fixed \(T>0\),
\[
(T_T\iota(p))(\tau)
=
p+
\frac1{\Gamma(\alpha)}
\int_0^T(T+\tau-s)^{\alpha-1}g(X(s;p))\,ds.
\]

If the physical orbit is bounded on \([0,T]\), then
\[
(T_T\iota(p))(\tau)\to p
\qquad(\tau\to\infty).
\]

Thus compact-open topology is essential; finite-time continuation states need not be globally close to the equilibrium in the unweighted sup norm.

## Final B215 realization

TASK-0006 certifies:
\[
X(t;p)\in R_{\rm ext}
\]
for every
\[
t\in[5.8576774143,13.7275388580],
\]
while
\[
X(t;p)\to E^*=(4/5,3/25).
\]

X1 classifies the canonical cold start from every reached point in that interval as extinction-bound.

Hence E1-A is realized:
\[
\mathcal F_{X(t;p)}
\]
is multibasin for every certified entry time.

This is TARGET-A20.
