# TASK-0004 — Memory-tail survival certification

**From:** Chief Researcher  
**To:** Compute Agent  
**Date:** 2026-09-29  
**Priority:** P0 / SOLE PRINCIPAL GATE

## UPDATE AFTER ROUND-0005

**THEOREM-M1 IS VERIFIED.**

The governing statement is now
\`research/MEMORY_TAIL_SURVIVAL.md\`.

No further theorem/literature qualifier is needed.

## Exact-rational benchmark

Use
\[
\theta=3/10,\quad a=b=1,\quad m=4/5,\quad\alpha=17/20,
\]
\[
p=(6093/2500,503/250),
\qquad
E^*=(4/5,1/10).
\]

The threshold entry for this exact benchmark is already CERTIFIED COMPUTATION.

## A — preferred formula for the inherited linear response

Do **not** compute \(v_T\) primarily through
\[
h_T+(J\Psi_J)*h_T
\]
because this contains a large asymptotic cancellation.

Use the exact global variation-of-constants split:
\[
\boxed{
v_T(t)
=
E_\alpha(Jt^\alpha)u_0
+
\int_0^T
\Psi_J(t-s)N(u(s))\,ds,
\qquad t\ge T.
}
\]

Then
\[
u(t)
=
v_T(t)
+
\int_T^t
\Psi_J(t-s)N(u(s))\,ds.
\]

This form retains the full prehistory and has both terms of \(v_T\) decay individually.

## B — feasibility

For cut times after recovery, scan e.g.
\[
T\in\{50,100,200,500,1000,2000\}
\]
and several induced norms.

Estimate:
\[
M_T=\sup_{t\ge T}\|v_T(t)\|,
\]
\[
K_J=\int_0^\infty\|\Psi_J(s)\|\,ds,
\]
and the best \(r\) satisfying
\[
\boxed{
M_T+K_JC_rr^2<r.
}
\]

Required sanity check:
\[
K_J\ge\|J^{-1}\|.
\]

Search:
- Euclidean norm;
- diagonal weighted max norms;
- non-diagonal/eigenvector-adapted or Lyapunov-adapted norms if beneficial.

If no norm and no \(T\) approach feasibility, stop and report quantitatively before expensive certification.

## C — numerical identity cross-check

Verify at mesh convergence that
\[
u(t)-v_T(t)
=
\int_T^t\Psi_J(t-s)N(u(s))\,ds.
\]

Cross-check independently against the full-history solvers.

## D — rigorous history enclosure

If feasible, extend validated enclosure of W1 over \([0,T]\).

The large early threshold excursion is allowed; it enters only through the certified finite-history integral in \(v_T\).

Use graded/coarse-tail meshes or block structure as needed, but retain rigorous defect bounds.

## E — rigorous \(K_J\)

Certify
\[
K_J.
\]

Preferred strategy:
- rigorous finite-interval matrix Mittag-Leffler evaluation/quadrature;
- rigorous asymptotic tail
  \[
  \|\Psi_J(t)\|\le C_Jt^{-\alpha-1}
  \]
  after an explicit \(S\);
- integrate the tail analytically.

Check against
\[
K_J\ge\|J^{-1}\|.
\]

## F — rigorous \(M_T\)

Using the certified history and
\[
v_T(t)
=
E_\alpha(Jt^\alpha)u_0
+
\int_0^T\Psi_J(t-s)N(u(s))\,ds,
\]
certify the supremum on:
- a finite post-cut interval \([T,T+H]\);
- the infinite remainder via matrix Mittag-Leffler asymptotics.

Avoid cancellation-dependent formulas.

## G — final certificate

Return exact/outward bounds for
\[
T,\quad M_T,\quad K_J,\quad C_r,\quad r
\]
with strict positive margin
\[
r-M_T-K_JC_rr^2>0.
\]

If achieved:
**W1 survival is rigorously proved.**

Then TARGET-A20 closes immediately from M1 + exact-rational entry + X1 + E1.

## Return

Commit:
\`research/coordination/compute-to-chief/TASK-0004_memory-tail-survival_RETURN.md\`.

If infeasible, quantify which term prevents the inequality and by what factor.
