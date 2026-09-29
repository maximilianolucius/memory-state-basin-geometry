# Purity / Impossibility Theorem Program

**Owner:** Chief Researcher  
**Date:** 2026-09-29  
**Status:** ACTIVE — proof drafts pending exact imported-theorem audit

## 1. Purpose

A positive multibasin-fiber theorem can only be scientifically interpreted if important impossibility classes are separated first.

The scalar case is the first target because published Caputo nonintersection results allow equilibrium solutions to act as barriers.

These results are intended primarily as completeness/minimal-dimension results, not as the principal novelty.

## 2. Scalar equilibrium-partition theorem

Consider the scalar autonomous Caputo IVP
[
{}^C D_{0+}^{alpha}x(t)=g(x(t)),qquad 0<alpha<1,
]
with standard point initial data and a well-defined continuation-state semigroup.

Let
[
c_1<cdots<c_m
]
be equilibrium values, and define the open intervals
[
I_0=(-infty,c_1),quad
I_j=(c_j,c_{j+1}),quad
I_m=(c_m,infty),
]
intersected with the physical domain as needed.

### PROPOSITION S1 — equilibrium-partition fiber purity

Assume:

**S1-H1.** Scalar nonintersection with equilibrium solutions holds:
for every (x_0
eq c_k),
[
x(t;x_0)
eq c_kqquad orall t>0, orall k.
]

**S1-H2.** For each interval (I_j), there exists an asymptotic state/attractor (A_{sigma(j)}) such that every standard physical initial condition (x_0in I_j) has canonical lift
[
iota(x_0)inmathcal B(A_{sigma(j)}).
]

**S1-H3.** Each equilibrium (c_k) has its stationary lifted state (iota(c_k)), and no non-equilibrium standard trajectory reaches (c_k) at positive time.

Then every physically reachable present-state fiber is basin-pure:
- if (xin I_j), then
[
mathcal F_xsubseteqmathcal B(A_{sigma(j)});
]
- if (x=c_k), then
[
mathcal F_x={iota(c_k)}.
]

Consequently, no reachable scalar present-state fiber can intersect two distinct basins under S1-H1--S1-H3.

### Proof draft

Take any
[
phi=T_tiota(x_0)inmathcal F_x.
]
If (xin I_j), S1-H1 applied against each equilibrium solution implies the standard trajectory cannot cross any (c_k); therefore (x_0) and (x) lie in the same connected component (I_j). By S1-H2,
[
iota(x_0)inmathcal B(A_{sigma(j)}).
]
Positive invariance of basins under the memory-state semigroup gives
[
T_tiota(x_0)inmathcal B(A_{sigma(j)}).
]
Because (phiinmathcal F_x) was arbitrary,
[
mathcal F_xsubseteqmathcal B(A_{sigma(j)}).
]

If (x=c_k), any representation
[
T_tiota(x_0)inmathcal F_{c_k}
]
has
[
x(t;x_0)=c_k.
]
By S1-H3, this forces (x_0=c_k). Since the equilibrium lift is stationary,
[
T_tiota(c_k)=iota(c_k),
]
so
[
mathcal F_{c_k}={iota(c_k)}.
]
QED, conditional on the imported nonintersection theorem and exact state-space hypotheses.

## 3. Strong-Allee corollary target

For a scalar strong-Allee equation with equilibria
[
0<a_u<K
]
and basin dichotomy
[
x_0<a_uRightarrow 	ext{extinction},qquad
x_0>a_uRightarrow 	ext{survival/positive attractor},
]
S1 implies:
[
x<a_uRightarrow mathcal F_xsubseteqmathcal B(A_{m ext}),
]
[
x>a_uRightarrow mathcal F_xsubseteqmathcal B(A_{m surv}),
]
with the separator fiber at (a_u) stationary under the standard equilibrium assumptions.

This formalizes why a scalar Double/Strong-Allee model cannot provide the desired same-present extinction/survival ambiguity when the usual threshold classification holds.

## 4. Dimension implication

If S1 is fully audited and the positive target requires two distinct basins separated as above, then the desired multibasin-fiber phenomenon requires leaving this scalar class.

This does **not** prove that every multidimensional system admits multibasin fibers.

## 5. Triangular extension target

Consider
[
{}^C D^alpha x_1=f_1(x_1),qquad
{}^C D^alpha x_{2:d}=F(x_1,ldots,x_d),
]
or a more general triangular cascade.

A safe theorem requires more than triangularity:

- the first coordinate must obey an audited scalar separator theorem;
- the full-system asymptotic basin label must be determined by the separator interval of (x_1).

Under those conditions, equality of the full present state forces equality of (x_1), so S1 determines the full basin and the fiber is pure.

This is currently a candidate completeness result.

## 6. Monotone/comparison caution

Order preservation by itself is insufficient for the desired conclusion because two memory states with equal present endpoint need not be ordered as histories.

Any monotone-system purity theorem must identify an additional endpoint-determining separator/invariant functional or a theorem that makes basin membership factor through (e_0).

No such claim is presently made.

## 7. Evidence status

- proof logic for S1: analytic and complete modulo imported theorem hypotheses;
- scalar nonintersection source: published prior, exact hypothesis audit pending ROUND-0002;
- novelty: not claimed;
- manuscript eligibility: no, until source audit and final scope decision.
