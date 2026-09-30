# TASK-0006 — CHIEF DECISION

**Date:** 2026-09-30  
**Branch:** \`compute/task-0006\`  
**Verified HEAD:** \`0e0905cf968fee852fc4c85ca42f88b8215dbc02\`  
**Certificate code SHA:** \`c9bc2f80788e0834ecb74e69e89aab59e50c741d\`  
**Integration:** main fast-forwarded to TASK-0006 HEAD  
**Disposition:** ACCEPT — B215 SURVIVAL CERTIFIED; TARGET-A20 PROMOTED

## 1. Evidence class

The result is accepted as:

> **COMPUTER-ASSISTED THEOREM / CERTIFIED COMPUTATION UNDER THE DECLARED ARITHMETIC MODEL.**

The mathematical fixed-point argument is rigorous.

The numerical upper bounds use:
- Arb ball arithmetic for the core analytic envelopes and exact-rational model data;
- binary64 operations with explicit rounding bounds/slack in the \(O(N^2)\) layers;
- a stated assumption on IEEE-754 arithmetic and few-ulp behavior of the listed libm functions.

This is not yet an end-to-end interval-arithmetic certificate. That distinction must remain explicit in the manuscript and audit trail.

## 2. Exact benchmark

\[
\alpha=\frac{17}{20},\qquad
\theta=\frac12,\qquad
a=\frac12,\qquad
b=1,\qquad
m=\frac45,
\]
\[
p=
\left(
\frac{277}{100},
\frac{467}{1000}
\right).
\]

The system is

\[
{}^CD^{17/20}x
=
x(1-x)\left(x-\frac12\right)
-\frac12xy,
\]

\[
{}^CD^{17/20}y
=
y\left(x-\frac45\right).
\]

The coexistence equilibrium is

\[
E^*=
\left(
\frac45,\frac3{25}
\right).
\]

## 3. Finite-history CAP

TASK-0006 validates the exact Caputo orbit on \([0,T]\) by a cellwise positive-operator fixed-point argument.

The successful proof does **not** use the failed scalar radii polynomial.

Instead it proves:

1. a componentwise self-map inequality
   \[
   F(b)<b
   \]
   for cellwise source sup/oscillation/bubble bounds;

2. a contraction in a strictly positive Perron-weighted norm.

At \(T=300,\ N=12000\):

\[
\kappa\le0.083612,
\]

and the exact orbit lies within

\[
\|x-\hat x\|_{\rm adapted}
\le4.8661\times10^{-4},
\]

hence physical state error

\[
\|x-\hat x\|_2
\le2.2193\times10^{-4}.
\]

An independent complete certificate also closes at \(T=1000,\ N=20000\), with

\[
\kappa\le0.187495.
\]

## 4. Why the vector certificate is valid

Let \(S_b\) be the set of continuous source functions satisfying the certified cellwise inequalities for:
- cell sup;
- cell oscillation;
- interpolation bubble.

These constraints define a closed subset of \(C([0,T],\mathbb R^2)\).

The contraction norm uses strictly positive weights \(q\) on a finite mesh:
\[
\|h\|_q
=
\max_{c,n}
\frac{\mathcal M_{c,n}(h)}{q_{c,n}},
\]
where \(\mathcal M\) denotes the three cellwise seminorm components.

Because the sup component is present and all weights are finite and positive, this is equivalent to the sup norm on the relevant continuous-function space.

Thus \(S_b\) is complete in the contraction norm.

The code verifies
\[
T(S_b)\subset S_b
\]
strictly and
\[
\operatorname{Lip}(T|_{S_b})\le\kappa<1.
\]

Banach therefore yields a unique fixed point.

The verified inverse is injective, so the fixed point solves the exact Volterra/Caputo equation.

## 5. Certified threshold excursion

For the exact-rational B215 orbit, the \(T=300\) certificate proves

\[
0<x(t)<\frac12,\qquad y(t)>0
\]

on the complete nondegenerate interval

\[
\boxed{
t\in[5.8576774143,\ 13.7275388580].
}
\]

A representative best cell is

\[
t\in[8.9839195370,\ 8.9927932624],
\]

with

\[
x\in[0.468938793,\ 0.469058899],
\]

\[
y\ge0.248262346,
\]

and threshold margin

\[
\eta
=
\frac12-x_{\max}
\ge0.0309411007.
\]

## 6. Certified survival

For \(T=300\),

\[
K_J\le11.3499043,
\]

\[
C_r\le0.3695518+0.1627353\,r,
\]

\[
M_T\le0.043232414.
\]

At

\[
r=\frac{2221}{20000},
\]

TASK-0006 certifies

\[
\boxed{
r-K_JC_rr^2-M_T
\ge
0.0135626>0,
}
\]

and

\[
K_JC_rr\le0.48857<1.
\]

Therefore THEOREM-M1 applies and

\[
\boxed{
x(t;p)\to E^*
\quad(t\to\infty).
}
\]

The independent \(T=1000\) proof gives the larger M1 margin

\[
\ge0.0413364.
\]

## 7. TARGET-A20 theorem

Let \(x(t;p)\) denote the exact standard B215 Caputo trajectory.

For every

\[
t_*
\in
[5.8576774143,\ 13.7275388580],
\]

define

\[
z=x(t_*;p).
\]

Then

\[
z\in R_{\rm ext}
=
\left\{
0<x<\frac12,\ y>0
\right\}.
\]

The inherited continuation state is

\[
\Phi=T_{t_*}\iota(p).
\]

Its present physical value is

\[
e_0(\Phi)=z.
\]

Since the full standard orbit converges to \(E^*\), E3 and semigroup invariance give

\[
\Phi\in\mathcal B(\iota(E^*)).
\]

But X1 gives

\[
\iota(z)\in\mathcal B(\iota(0,0)).
\]

And

\[
e_0(\iota(z))=z.
\]

Therefore

\[
\Phi,\iota(z)\in F_z
\]

but they belong to distinct asymptotic basins.

Hence

\[
\boxed{
F_z
\text{ is multibasin.}
}
\]

This holds for every \(t_*\) in the certified entry interval.

Thus the result is stronger than one isolated fiber:

\[
\boxed{
\text{a certified physical excursion carries an interval of multibasin reachable fibers.}
}
\]

## 8. Promotion

\[
\boxed{
\text{TARGET-A20 — PROVED BY CERTIFIED COMPUTATION UNDER THE DECLARED ARITHMETIC MODEL.}
}
\]

The principal scientific gate is closed.

## 9. Remaining publication gates

1. final theorem-specific hostile novelty audit;
2. optionally harden the binary64/libm layers to end-to-end Arb for maximum referee robustness;
3. manuscript only after novelty audit passes.
