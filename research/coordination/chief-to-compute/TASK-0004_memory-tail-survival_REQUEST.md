# TASK-0004 — Memory-tail survival feasibility and certification

**From:** Chief Researcher  
**To:** Compute Agent  
**Date:** 2026-09-29  
**Priority:** P0 / TARGET-A20 SURVIVAL CLOSURE

## Context

TASK-0003 proved that physical-state invariant basin certificates cannot close the target.

Use the memory-dependent candidate theorem in:
\`research/MEMORY_TAIL_SURVIVAL.md\`.

Until ROUND-0005 returns, label M1-dependent conclusions **CONDITIONAL**.

## A — feasibility first

Use the exact-rational W1 model:
\[
\theta=3/10,\quad a=b=1,\quad m=4/5,\quad\alpha=17/20,
\]
\[
p=(6093/2500,503/250).
\]

For cut times after recovery, e.g.
\[
T\in\{50,100,200,500,1000\},
\]
numerically estimate in several norms:

1. the inherited input \(h_T\);
2. the exact linear response \(v_T=\mathcal L_Jh_T\);
3. 
   \[
   M_T=\sup_{t\ge T}\|v_T(t)\|;
   \]
4. 
   \[
   K_J=\int_0^\infty\|\Psi_J(s)\|\,ds;
   \]
5. best radius \(r\) for
   \[
   M_T+K_JC_rr^2<r.
   \]

Use:
- Euclidean norm;
- diagonal weighted max norms;
- if useful, a non-diagonal eigenvector/Lyapunov-adapted norm.

This stage is NUMERICAL EXPLORATION only.

Stop early if the inequality misses by orders of magnitude for every reasonable \(T\).

## B — verify the resolvent numerically

Cross-check:
\[
u(t)
=
v_T(t)
+
\int_T^t\Psi_J(t-s)N(u(s))\,ds
\]
against the existing full-history solvers.

The identity should agree at mesh convergence order.

## C — rigorous finite-history input

If Stage A is feasible, extend the TASK-0002 validated trajectory enclosure from \([0,4]\) to a useful cut time \(T\).

Use graded/coarse-tail meshes or block acceleration while retaining rigorous defect bounds.

From the certified history, build rigorous enclosures of \(h_T(t)\) needed by the linear response calculation.

Do not restart the Caputo IVP at \(T\).

## D — rigorous kernel and linear-response bounds

Develop certified bounds for:
\[
K_J
\]
and
\[
M_T.
\]

Allowed:
- matrix diagonalization with interval eigenvector enclosures;
- scalar Mittag-Leffler sector bounds;
- direct Arb quadrature on a finite interval plus analytic asymptotic tail;
- contour/asymptotic bounds justified by ROUND-0005 sources.

All tail estimates must be rigorous.

## E — certificate

If ROUND-0005 validates M1 and the strict inequality
\[
M_T+K_JC_rr^2<r
\]
is rigorously separated, return:
- exact \(T\);
- norm;
- \(M_T,K_J,C_r,r\);
- numerical margins;
- full provenance.

Then survival of W1 is certified.

Combined with the existing exact-rational threshold-entry certificate, X1 and E1, this would prove TARGET-A20.

## Negative result

If M1 is infeasible even after norm optimization, quantify the obstruction rather than extending horizon blindly.

## Return

Commit:
\`research/coordination/compute-to-chief/TASK-0004_memory-tail-survival_RETURN.md\`.
