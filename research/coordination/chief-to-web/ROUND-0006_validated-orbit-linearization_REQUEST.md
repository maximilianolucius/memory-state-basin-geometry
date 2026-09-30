# ROUND-0006 — Rigorous orbit-linearized Volterra validation audit

**From:** Chief Researcher  
**To:** Deep Web Search Agent  
**Date:** 2026-09-30  
**Priority:** P0 / VALIDATED-NUMERICS GATE

## Context

TASK-0004 established that THEOREM-M1 is numerically feasible, but the current normwise a-posteriori verifier loses \(10^6\)–\(10^{16}\) through absolute-value amplification during the nonlinear excursion.

The project now needs rigorous validation around the computed orbit rather than around the equilibrium Jacobian.

Read:
- \`research/VALIDATED_HISTORY_STRATEGY.md\`;
- \`research/coordination/compute-to-chief/TASK-0004_memory-tail-survival_RETURN.md\`.

## Q1 — high-order a-posteriori Volterra methods

Search formally published work on:
- high-order collocation for weakly singular Volterra equations;
- residual-based a-posteriori estimates;
- adaptive collocation/DG for kernels \((t-s)^{\alpha-1}\);
- rigorous error estimators that avoid a crude global Gronwall constant.

Priority leads to inspect:
- adaptive collocation for weakly singular Volterra equations;
- 2026 residual-based DG a-posteriori Volterra work;
- published high-order fractional convolution/product-integration methods.

Extract theorem statements and whether they can yield **computer-assisted enclosures**, not only asymptotic convergence rates.

## Q2 — Newton–Kantorovich / approximate inverse

Search published rigorous-numerics literature for nonlinear Volterra integral equations using:
- Newton–Kantorovich;
- interval Newton;
- radii polynomials;
- approximate inverse of the Fréchet derivative;
- computer-assisted proof of integral equations.

Determine whether a theorem directly supports:

\[
\mathcal F(x)=0,\quad
\mathcal L=D\mathcal F(\hat x),
\]
with an approximate inverse \(B\), and bounds \(Y,Z_1,Z_2(r)\) such that a radii inequality proves a true nearby solution.

Generic Banach-space Newton theorems are acceptable if the project can verify all operator bounds.

## Q3 — nonautonomous Volterra resolvent

For
\[
e(t)
=
f(t)
+
\frac1{\Gamma(\alpha)}
\int_0^t
(t-s)^{\alpha-1}A(s)e(s)\,ds,
\]
with continuous matrix \(A(s)\), find published theory for:
- two-variable resolvent kernels;
- variation of constants;
- norm estimates;
- numerical approximation of the resolvent.

The purpose is to preserve sign/rotation cancellation along the actual orbit.

## Q4 — fractional initial singularity and high order

Audit published methods that explicitly handle the \(t^\alpha\)-type initial layer:
- graded meshes;
- fractional-power expansions;
- corrected convolution quadrature;
- high-order product integration.

Identify which methods remain high-order for \(0<\alpha<1\) without assuming classical smoothness at \(t=0\).

## Q5 — exact current-prior pressure

Search 2025–2026 published work on validated/certified numerical solutions of Caputo systems or nonlinear weakly singular Volterra equations.

The project must not claim novelty for validated numerics if a direct method already exists.

## Required verdict

Return a ranked recommendation:

1. **ORBIT-LINEARIZED APPROXIMATE-INVERSE ROUTE SUPPORTED**
2. **HIGH-ORDER RESIDUAL ROUTE SUPPORTED**
3. **BOTH**
4. **NO PRACTICAL PUBLISHED ROUTE FOUND**

For each recommended route, provide the exact theorem/source chain needed for a computer-assisted proof.

Deliver:
\`research/coordination/web-to-chief/ROUND-0006_validated-orbit-linearization_RETURN.md\`
and a substantive report under \`research/web-search/\`.

Final-paper bibliography remains formally published only.
