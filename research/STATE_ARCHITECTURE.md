# State Architecture and First Theorem Program

**Owner:** Chief Researcher  
**Date:** 2026-09-29  
**Status:** VERIFIED BASELINE / TARGET-MODEL ADMISSIBILITY STILL OPEN

## 1. Governing Caputo IVP

Work initially with
\[
{}^C D_{0+}^{\alpha}x(t)=g(x(t);\theta),\qquad 0<\alpha<1,
\]
with standard point initial data \(x(0)=x_0\).

For the globally Lipschitz baseline, Doan & Kloeden (2021) give the equivalent Volterra formulation and the semidynamical-system architecture used below.

For the eventual ecological model, global Lipschitz need not be imposed artificially. Instead, the project must prove the admissibility/global-continuation conditions required for the generalized Volterra problem.

No ODE semiflow is assumed on the physical state \(X_{\rm phys}\).

## 2. Verified memory-state architecture

Adopt
\[
\mathfrak C=C(\mathbb R_+,\mathbb R^d)
\]
with the compact-open topology induced by
\[
\rho(f,h)=\sum_{n=1}^{\infty}2^{-n}
\frac{\sup_{t\in[0,n]}\|f(t)-h(t)\|}
{1+\sup_{t\in[0,n]}\|f(t)-h(t)\|}.
\]

Terminology discipline: treat this as a continuous-function state space with compact-open topology; do not rely on an unverified global Banach-norm structure.

For the generalized Volterra equation, the continuation operator is
\[
(T_\tau f)(\theta)
=
f(\tau+\theta)
+
\int_0^\tau
\frac{(\tau+\theta-s)^{\alpha-1}}{\Gamma(\alpha)}
g(x_f(s))\,ds.
\]

Under the audited Doan–Kloeden hypotheses,
\[
T_{\sigma+\tau}=T_\sigma T_\tau
\]
and each \(T_\tau\) is continuous.

The canonical physical embedding and present-state evaluation are
\[
\iota(x_0)(t)\equiv x_0,\qquad e_0(f)=f(0),
\]
with
\[
x(t;x_0)=e_0(T_t\iota(x_0)).
\]

Define
\[
\mathcal R_\alpha=
\{T_t\iota(x_0):t\ge0,\ x_0\in X_{\rm phys}\},
\]
and
\[
\mathcal F_x=e_0^{-1}(x)\cap\mathcal R_\alpha.
\]

### Closure policy

Principal claims are to be made on \(\mathcal R_\alpha\), not on arbitrary ambient histories.

The closure \(\overline{\mathcal R_\alpha}\) may be introduced only when genuinely required by compactness/attractor/stable-set arguments. A witness existing only in the closure does not establish physical reachability.

## 3. Basin definition and invariance

For an invariant asymptotic state/attractor \(A\subset\mathfrak C\), define
\[
\mathcal B(A)=
\{\phi\in\mathfrak C:
\operatorname{dist}(T_t\phi,A)\to0
\text{ as }t\to\infty\},
\]
with distance interpreted in the chosen compatible metric/topology.

By the semigroup property, basins are positively invariant:
\[
\phi\in\mathcal B(A)
\Longrightarrow
T_r\phi\in\mathcal B(A),\qquad r\ge0.
\]

A reachable fiber is **basin-pure** if all basin-classified members belong to one basin, and **multibasin** if it contains members of at least two distinct basins.

## 4. REDUCTION-M1 — inter-basin physical collision

Define
\[
P_{\alpha,\theta}(x_0,t)
=
e_0(T_t\iota(x_0))
=
x(t;x_0,\alpha,\theta).
\]

If
\[
\iota(p)\in\mathcal B(A_1),\qquad
\iota(q)\in\mathcal B(A_2),\qquad A_1\neq A_2,
\]
and there exist \(t,s\ge0\) such that
\[
P(p,t)=P(q,s)=x,
\]
then
\[
T_t\iota(p),T_s\iota(q)\in\mathcal F_x
\]
and positive invariance gives
\[
T_t\iota(p)\in\mathcal B(A_1),\qquad
T_s\iota(q)\in\mathcal B(A_2).
\]

Hence \(\mathcal F_x\) is multibasin.

**Status:** PROVED / STANDARD CONSEQUENCE.  
**Novelty:** none claimed.  
**Role:** finite-dimensional discovery reduction.

ROUND-0001 explicitly determined that this implication is not theorem-level novelty.

## 5. CANDIDATE-M2 — Caputo-specific persistence

Let
\[
H(p,q,t,s;\mu)=P_\mu(p,t)-P_\mu(q,s).
\]

The generic parameterized implicit-function step is standard. A publishable persistence theorem must therefore verify the nonstandard burden in the actual Caputo setting.

At a candidate zero
\[
H(p_*,q_*,t_*,s_*;\mu_*)=0,
\]
the project will seek:

1. robust trapping/basin membership of the two standard IVPs;
2. a nonsingular \(d\times d\) derivative minor with respect to explicitly declared solved variables;
3. \(C^1\) regularity in those solved variables;
4. continuity of the relevant derivatives under model-parameter perturbation;
5. correct fixed-lower-terminal memory treatment;
6. additional order regularity if \(\alpha\) itself is varied.

If these are proved, the collision can potentially be promoted from one witness to an open parameter family.

**Status:** OPEN / NARROWED.  
**Novelty burden:** not the IFT mechanism itself, but the Caputo-specific realization and open-family reachable multibasin geometry.

## 6. Purity / impossibility track

The scalar theorem program is now separated into
\`research/PURITY_THEOREMS.md\`.

The key draft result is an equilibrium-partition purity theorem: scalar nonintersection against equilibrium solutions prevents crossing equilibrium separators; if basin outcome is constant on the resulting intervals, every reachable present-state fiber is pure.

The same logic may extend to triangular systems only when a closed scalar coordinate is basin-determining for the full system.

Order preservation alone is not assumed to imply fiber purity because equal endpoint does not imply ordered histories.

## 7. Constructive positive target

The preferred example remains a natural nontriangular positive strong/Double-Allee Caputo system with:

- extinction and survival/coexistence attractors;
- standard physical IVPs rigorously placed in both basins;
- an exact/certified inter-basin physical collision;
- a nondegenerate collision Jacobian;
- positivity and global continuation;
- persistence beyond one benchmark.

A numerical near-collision is only a conjecture generator.

## 8. Novelty boundary after ROUND-0001

Not new:
- memory-state enlargement;
- current-state non-Markovianity;
- reachable trajectory intersection;
- history-space basin geometry;
- headpoint/projected basin calculations in hereditary systems;
- overlapping projected attractors in fractional maps;
- M1 as an abstract implication;
- the generic implicit-function mechanism.

Search-qualified residual:
\[
\exists\phi,\psi\in\mathcal R_\alpha:
\quad e_0(\phi)=e_0(\psi),\qquad
\phi\in\mathcal B(A_1),\quad
\psi\in\mathcal B(A_2),\quad A_1\neq A_2,
\]
for physically reachable states of an autonomous continuous Caputo system with \(0<\alpha<1\), preferably extinction versus survival in a natural positive model, plus an open-family structural result.

## 9. Active gates

- ROUND-0001: assimilated.
- ROUND-0002: scalar/triangular purity audit dispatched.
- TASK-0001: validated collision-search compute task outstanding.
- manuscript mode: blocked.
