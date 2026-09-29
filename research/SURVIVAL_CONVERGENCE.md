# Survival-Convergence Program

**Owner:** Chief Researcher  
**Date:** 2026-09-29  
**Status:** ACTIVE / PRINCIPAL THEOREM BOTTLENECK

## 1. Exact remaining problem

For the Caputo system
\[
{}^C D^\alpha x=x(1-x)(x-\theta)-axy,
\]
\[
{}^C D^\alpha y=y(bx-m),
\]
with coexistence equilibrium
\[
x^*=\frac mb,\qquad
y^*=\frac{(1-x^*)(x^*-\theta)}a,
\]
prove for at least one standard initial state \(p\) that
\[
(x(t;p),y(t;p))\to(x^*,y^*),
\]
while its finite-time physical orbit enters
\[
R_{\rm ext}=\{0<x<\theta,\ y\ge0\}.
\]

By E3 + X1 + E1 this alone closes the principal multibasin-fiber existence theorem.

## 2. What is not enough

The following are insufficient by themselves:

- local Matignon stability of \(E^*\);
- a late physical near-hit to \(E^*\);
- finite-horizon numerical convergence;
- an ODE-style restart at a late time;
- a basin plot.

The proof must classify the original standard IVP from time zero.

## 3. Candidate entropy Lyapunov structure

Let
\[
h(x)=(1-x)(x-\theta).
\]

At coexistence,
\[
h(x^*)=ay^*,\qquad bx^*=m.
\]

Consider the Volterra-type entropy candidate
\[
V(x,y)
=
x-x^*-x^*\log\frac{x}{x^*}
+
\frac ab
\left(
y-y^*-y^*\log\frac{y}{y^*}
\right).
\]

If the standard fractional convex-chain inequality can be applied,
\[
{}^CD^\alpha V
\le
\left(1-\frac{x^*}{x}\right){}^CD^\alpha x
+
\frac ab
\left(1-\frac{y^*}{y}\right){}^CD^\alpha y.
\]

The right side simplifies exactly to
\[
(x-x^*)[h(x)-h(x^*)].
\]

Since
\[
h(x)-h(x^*)
=
(x-x^*)[(1+\theta)-(x+x^*)],
\]
we obtain the formal estimate
\[
{}^CD^\alpha V
\le
-(x-x^*)^2
\left[x+x^*-(1+\theta)\right].
\]

Thus the entropy is dissipative wherever
\[
x>1+\theta-x^*.
\]

### Important limitation

For the TASK-0001 witness
\[
\theta=0.3,\qquad x^*=0.8,
\]
the sign-guaranteed region is
\[
x>0.5,
\]
whereas the witness deliberately falls below \(0.3\).

Therefore this Lyapunov estimate does **not** directly prove convergence of the existing witness from time zero.

It may still be valuable for:
- parameter regimes with \(\theta\) close to \(1\);
- a future global argument;
- constructing rigorous local survival sets;
- interpreting TASK-0002 near-equilibrium candidates.

No theorem is claimed from this calculation yet.

## 4. Candidate proof routes

Priority order:

1. **validated asymptotic/tail proof** for a specific standard IVP;
2. **Lyapunov/LaSalle proof** covering a region large enough to contain a witness;
3. **published-model theorem** with an already rigorous survival basin and a verified threshold-entry orbit;
4. analytic separatrix/basin-boundary argument.

## 5. Relation to TASK-0002

TASK-0002 should be interpreted as searching for a witness optimized for proof, not merely for penetration depth.

The ideal candidate minimizes:
- distance to a rigorously certifiable survival set,
while retaining
- strict entry margin into \(R_{\rm ext}\).

The strongest numerical witness need not be the easiest theorem witness.
