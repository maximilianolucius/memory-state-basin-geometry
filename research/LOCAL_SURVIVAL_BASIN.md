# Local Survival Basin Program

**Owner:** Chief Researcher  
**Date:** 2026-09-29  
**Status:** CANDIDATE THEOREM / EXACT SOURCE AUDIT + COMPUTE SEARCH ACTIVE

## 1. Model and coexistence equilibrium

Consider
\[
{}^C D^\alpha z=F(z),
\qquad z=(x,y),
\]
with
\[
F_1=x(1-x)(x-\theta)-axy,
\qquad
F_2=y(bx-m).
\]

For
\[
x^*=\frac mb,\qquad
y^*=\frac{(1-x^*)(x^*-\theta)}a,
\]
assume
\[
\theta<x^*<1.
\]

Let \(u=z-E^*\) and
\[
J=DF(E^*).
\]

## 2. Candidate theorem L1 — explicit local survival basin

Assume \(J\) is Hurwitz.

Let \(P=P^\top>0\) solve
\[
J^\top P+PJ=-I.
\]

Write
\[
F(E^*+u)=Ju+N(u).
\]

For \(r>0\), let \(C_r\) satisfy
\[
\|N(u)\|_2\le C_r\|u\|_2^2
\qquad
(\|u\|_2\le r).
\]

Assume the standard Caputo quadratic inequality
\[
{}^CD^\alpha(u^\top Pu)
\le
2u^\top P\,{}^CD^\alpha u
\]
and the audited fractional Lyapunov theorem.

Then inside \(\|u\|_2\le r\),
\[
{}^CD^\alpha V
\le
-\|u\|_2^2
+
2\|P\|_2C_r\|u\|_2^3.
\]

If
\[
2\|P\|_2C_r r\le\frac12,
\]
then
\[
{}^CD^\alpha V
\le
-\frac12\|u\|_2^2.
\]

Consequently every standard initial state satisfying
\[
V(u_0)<\lambda_{\min}(P)r^2
\]
should remain in the ball and converge to \(E^*\).

### Status

This is a **candidate theorem** until ROUND-0004 verifies:
- the exact quadratic Caputo chain inequality;
- the scalar comparison/stability step that keeps \(V\) below its initial value;
- the asymptotic-convergence conclusion from the negative-definite fractional Lyapunov derivative;
- regularity hypotheses.

## 3. Why this route is attractive

If Compute finds \(p\) satisfying the local certificate from time zero and also certifies
\[
x(t_*;p)<\theta,
\]
then:
- L1 gives \(p\in\mathcal B(E^*)\);
- X1 gives the cold start at the reached state is in the extinction basin;
- E1 gives a rigorous multibasin present-state fiber.

No long-time basin inference is needed.

## 4. Search geometry

Hurwitz stability of \(J\) is deliberately stronger than Caputo/Matignon stability.

This excludes the weakly damped B2/B3 fractional-stabilization regime, but buys an explicit classical quadratic Lyapunov matrix.

A useful search should emphasize:
- \(\theta\) near one;
- \(x^*>(1+\theta)/2\), so the coexistence Jacobian has negative trace;
- exact rational parameters;
- a threshold gap small enough that a locally stable trajectory can still undershoot \(x=\theta\).

## 5. Certification burden

For a candidate parameter set, certify:
1. exact rational equilibrium;
2. Hurwitz \(J\);
3. rigorous \(P>0\);
4. rigorous \(C_r\);
5. the L1 inequalities;
6. initial-point inclusion in the certified ellipsoid;
7. finite-time entry into \(R_{\rm ext}\) using the TASK-0002 validated integrator.

If all seven hold after ROUND-0004 validates the theorem, TARGET-A20 is closed.
