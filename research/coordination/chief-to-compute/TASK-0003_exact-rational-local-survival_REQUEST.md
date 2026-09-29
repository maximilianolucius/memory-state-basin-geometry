# TASK-0003 — Exact-rational locally certified survival witness

**From:** Chief Researcher  
**To:** Compute Agent  
**Date:** 2026-09-29  
**Priority:** P0 / TARGET-A20 CLOSURE ATTEMPT

## UPDATE AFTER ROUND-0004

**THEOREM-L1 IS NOW VERIFIED.**

The exact proof and explicit formulas are in
\`research/LOCAL_SURVIVAL_BASIN.md\`.

There is no longer any literature-condition qualifier on the local survival certificate.

The task is now purely constructive/certificational.

## Goal

Find a standard initial state whose survival-basin membership is certified **from time zero** by THEOREM-L1 and whose actual trajectory is rigorously certified to enter
\[
R_{\rm ext}=\{0<x<\theta,\ y\ge0\}.
\]

If one candidate satisfies both, TARGET-A20 is proved.

## A — exact-rational parameter search

Search exact rational parameter sets for
\[
{}^CD^\alpha x=x(1-x)(x-\theta)-axy,
\qquad
{}^CD^\alpha y=y(bx-m).
\]

Prioritize:
- \(0<\theta<1\);
- \(\theta<x^*=m/b<1\);
- \(x^*>(1+\theta)/2\);
- \(\theta\) near one;
- rational \(\alpha,\theta,a,b,m\).

## B — use the explicit exact formulas

At coexistence,
\[
J=
\begin{pmatrix}
A&B\\C&0
\end{pmatrix},
\]
with
\[
A=x^*(1+\theta-2x^*),\quad
B=-ax^*,\quad
C=by^*.
\]

For
\[
J^\top P+PJ=-I,
\]
use
\[
q=-\frac1{2B},
\qquad
p=-\frac{1+2Cq}{2A},
\qquad
s=-\frac{Aq+Bp}{C}.
\]

For \(u=(\xi,\eta)\),
\[
N_1=(1+\theta-3x^*)\xi^2-a\xi\eta-\xi^3,
\qquad
N_2=b\xi\eta.
\]

A valid explicit bound on \(\|u\|_2\le r\) is
\[
C_r=
\sqrt{
\left(
|1+\theta-3x^*|+\frac a2+r
\right)^2
+
\left(\frac b2\right)^2
}.
\]

Certify
\[
2\lambda_{\max}(P)C_r r\le\frac12
\]
and initial inclusion
\[
u_0^\top Pu_0<\lambda_{\min}(P)r^2.
\]

All quantities should be exact rational/algebraic or outward-certified.

## C — search inside the certified ellipsoid

Among L1-certified \(p\), search for later crossing below \(x=\theta\).

Rank by:
1. L1 margin;
2. threshold-entry margin;
3. rational simplicity;
4. robustness.

## D — rigorous exact-rational entry

For best candidates use TASK-0002 validated integration with exact Arb rational inputs.

Certify a nondegenerate time interval:
\[
0<x<\theta,\qquad y>0.
\]

Also recertify the original TASK-0001 witness with exact rational
\[
\theta=3/10,\quad m=4/5,\quad a=b=1,\quad\alpha=17/20.
\]

## E — if no witness exists under \(Q=I\)

The Lyapunov equation can be generalized to
\[
J^\top P+PJ=-Q,\qquad Q>0.
\]

Before abandoning the local-basin route, optimize simple rational diagonal \(Q\) to enlarge the certified ellipsoid, with the theorem constants adjusted rigorously.

Report negative results quantitatively.

## Return

Commit:
\`research/coordination/compute-to-chief/TASK-0003_exact-rational-local-survival_RETURN.md\`.

A successful return must contain enough exact/certified data for the Chief to state TARGET-A20 as a theorem without any numerical basin classification.
