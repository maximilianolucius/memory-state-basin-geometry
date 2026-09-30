# Referee-Facing Positioning Summary

**Internal document — not manuscript prose.**

## The mathematical question

Does basin membership of a physically reachable autonomous Caputo state factor through the current physical value?

The paper answers **no** by constructing and certifying a reachable fiber containing:
- an inherited state in the coexistence basin;
- a canonical cold start at the identical current value in the extinction basin.

## Exact principal theorem

For
\[
{}^CD^{17/20}x=x(1-x)(x-1/2)-\tfrac12xy,
\qquad
{}^CD^{17/20}y=y(x-4/5),
\]
with
\[
p=(277/100,467/1000),
\]
the exact standard trajectory satisfies
\[
0<x(t)<1/2,\qquad y(t)>0
\]
for every
\[
t\in[5.8576774143,13.7275388580],
\]
while
\[
X(t;p)\to(4/5,3/25).
\]

Therefore, for every such \(t_*\),
\[
\iota(X(t_*;p))
\in\mathcal B(\iota(0,0)),
\]
but
\[
T_{t_*}\iota(p)
\in\mathcal B(\iota(4/5,3/25)),
\]
with identical present evaluation.

## Why this is not a restart artifact

The survival proof never restarts the Caputo system at a late physical point.

The exact decomposition
\[
U(t)=v_T(t)+\int_T^t\Psi_J(t-s)N(U(s))\,ds
\]
retains the complete pre-\(T\) history through \(v_T\).

This distinction should be emphasized whenever a referee asks why physical proximity to \(E^*\) is meaningful.

## Why the ecological threshold does not contradict survival

The theorem
\[
z\in R_{\rm ext}
\Longrightarrow
\iota(z)\in\mathcal B(\iota(0,0))
\]
classifies the canonical cold start only.

It does not assert
\[
e_0^{-1}(R_{\rm ext})
\subset
\mathcal B(\iota(0,0)).
\]

The principal theorem proves precisely that the stronger statement is false.

## What is analytically proved

- continuation-state basin-entry criterion;
- physical-to-continuation convergence;
- scalar fiber purity under equilibrium-partition hypotheses;
- cold-start extinction strip;
- memory-tail survival theorem;
- exact B215 equilibrium/Jacobian/remainder algebra.

## What is computer-assisted

- finite B215 trajectory enclosure;
- certified threshold-entry interval;
- source-space inverse bounds;
- cellwise self-map;
- Perron contraction;
- \(K_J,C_r,M_T\) bounds needed by M1.

## Primary numerical proof margins

\[
\kappa\le0.083612,
\]
\[
F(b)<b
\quad\text{with relative slack }\ge6.036\times10^{-4},
\]
\[
\|X-\widehat X\|_2\le2.2193\times10^{-4},
\]
\[
r-K_JC_rr^2-M_T\ge0.0135626.
\]

The threshold penetration margin at the representative cell is
\[
1/2-x_{\max}\ge0.0309411007.
\]

Thus the proof is not numerically balanced on equality cases.

## Independent redundancy

A second complete validation at
\[
T=1000,\quad N=20000
\]
also closes, with
\[
\kappa\le0.187495
\]
and M1 margin
\[
\ge0.0413364.
\]

This is evidence of robustness, not a second theorem requirement.

## Closest literature and exact boundary

Doan--Kloeden:
continuation-state architecture — prior.

Deshpande et al.:
fractional trajectory intersections — prior.

Szaksz--Stepan--Habib:
same-headpoint history sensitivity in delay systems — closest conceptual analogue, but no opposite-basin theorem.

Fractional Allee ecological literature:
multistability, basin plots, extinction/coexistence — prior.

The manuscript novelty is only the rigorous same-present physically reachable Caputo basin split.

## Claims a referee should not find in the paper

The manuscript must not claim:
- first memory-dependent future;
- first trajectory intersection;
- first fractional ecological basin;
- first extinction/coexistence multistability;
- novelty of the vector field;
- novelty of generic validated numerics;
- parameter-open persistence;
- a topological arc of distinct fibers;
- end-to-end interval arithmetic unless TASK-0007 explicitly establishes it.
