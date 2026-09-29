# Local Survival Basin Theorem

**Owner:** Chief Researcher  
**Date:** 2026-09-29  
**Status:** PROVED FROM PUBLISHED HYPOTHESES

## 1. Model

Consider
\[
{}^CD^\alpha z=F(z),
\qquad z=(x,y),
\]
with
\[
F_1=x(1-x)(x-\theta)-axy,
\qquad
F_2=y(bx-m),
\]
and coexistence equilibrium
\[
x^*=\frac mb,\qquad
y^*=\frac{(1-x^*)(x^*-\theta)}a.
\]

Assume
\[
\theta<x^*<1.
\]

Let
\[
u=z-E^*.
\]

## 2. Jacobian and Hurwitz condition

At \(E^*\),
\[
J=
\begin{pmatrix}
x^*(1+\theta-2x^*) & -ax^*\\
by^* & 0
\end{pmatrix}.
\]

Since
\[
\det J=abx^*y^*>0,
\]
\(J\) is Hurwitz exactly when
\[
\operatorname{tr}J
=
x^*(1+\theta-2x^*)<0,
\]
i.e.
\[
\boxed{
x^*>\frac{1+\theta}{2}.
}
\]

This deliberately uses a stronger condition than Matignon stability.

## 3. Exact Lyapunov matrix

Write
\[
J=
\begin{pmatrix}
A&B\\C&0
\end{pmatrix},
\qquad
A<0,\ B<0,\ C>0.
\]

Let
\[
P=
\begin{pmatrix}
p&q\\q&s
\end{pmatrix}
\]
solve
\[
J^\top P+PJ=-I.
\]

The entries are explicitly
\[
q=-\frac1{2B},
\]
\[
p=-\frac{1+2Cq}{2A},
\]
\[
s=-\frac{Aq+Bp}{C}.
\]

For rational model parameters, \(A,B,C\) and hence \(P\) are rational.

The classical Lyapunov matrix theorem guarantees
\[
P=P^\top>0
\]
because \(J\) is Hurwitz.

Its spectral quantities can be certified exactly through the two eigenvalues
\[
\lambda_{\pm}(P)
=
\frac{\operatorname{tr}P
\pm
\sqrt{(\operatorname{tr}P)^2-4\det P}}2.
\]

Thus
\[
\|P\|_2=\lambda_{\max}(P).
\]

## 4. Exact nonlinear remainder

Write
\[
u=(\xi,\eta).
\]

The shifted system has
\[
F(E^*+u)=Ju+N(u),
\]
with exact remainder
\[
N_1(\xi,\eta)
=
(1+\theta-3x^*)\xi^2
-a\xi\eta
-\xi^3,
\]
\[
N_2(\xi,\eta)
=
b\xi\eta.
\]

If
\[
\|u\|_2\le r,
\]
then
\[
|\xi\eta|\le\frac12\|u\|_2^2,
\qquad
|\xi|^3\le r\|u\|_2^2.
\]

Therefore the explicit valid bound
\[
\boxed{
C_r=
\sqrt{
\left(
|1+\theta-3x^*|+\frac a2+r
\right)^2
+
\left(\frac b2\right)^2
}
}
\]
satisfies
\[
\|N(u)\|_2\le C_r\|u\|_2^2.
\]

This bound is conservative but algebraic and easy to certify.

## 5. THEOREM L1 — explicit local survival basin

Let \(r>0\) satisfy
\[
\boxed{
2\lambda_{\max}(P)C_r r\le\frac12.
}
\]

Define
\[
V(u)=u^\top Pu.
\]

Then every standard initial state \(u_0\) satisfying
\[
\boxed{
V(u_0)<\lambda_{\min}(P)r^2
}
\]
has a unique global solution and
\[
u(t)\to0.
\]

More explicitly,
\[
\boxed{
V(u(t))
\le
V(u_0)
E_\alpha\!\left(
-\frac{t^\alpha}{2\lambda_{\max}(P)}
\right).
}
\]

Consequently,
\[
z(t)\to E^*,
\]
and by STRUCTURAL-E3,
\[
T_t\iota(z_0)\to\iota(E^*)
\]
in compact-open topology.

Thus every such standard initial state lies rigorously in the survival/coexistence basin.

## 6. Proof

Ren & Wu (2019), Lemma 3.1, gives
\[
{}^CD^\alpha V
\le
2u^\top P\,{}^CD^\alpha u.
\]

Hence
\[
{}^CD^\alpha V
\le
2u^\top P(Ju+N(u)).
\]

Because
\[
J^\top P+PJ=-I,
\]
\[
2u^\top PJu=-\|u\|_2^2.
\]

Also
\[
2u^\top PN(u)
\le
2\|P\|_2 C_r\|u\|_2^3.
\]

Inside \(\|u\|_2\le r\),
\[
{}^CD^\alpha V
\le
-\left(1-2\|P\|_2C_r r\right)\|u\|_2^2
\le
-\frac12\|u\|_2^2.
\]

Since
\[
V(u)\le\lambda_{\max}(P)\|u\|_2^2,
\]
\[
{}^CD^\alpha V
\le
-\frac1{2\lambda_{\max}(P)}V.
\]

Wu (2020), Theorem 3.2, gives comparison with
\[
w(t)=V(u_0)
E_\alpha\!\left(
-\frac{t^\alpha}{2\lambda_{\max}(P)}
\right).
\]

If a first exit from \(\|u\|_2<r\) occurred, then before that time
\[
V(u(t))
\le V(u_0)
<
\lambda_{\min}(P)r^2,
\]
whereas at first exit
\[
V(u)\ge\lambda_{\min}(P)r^2,
\]
a contradiction.

Thus the ball is never exited.

Boundedness and Wu & Liu (2020) give global continuation. The comparison bound tends to zero, hence \(u(t)\to0\). \(\square\)

## 7. Evidence / novelty

- theorem status: **PROVED FROM PUBLISHED HYPOTHESES**;
- ROUND-0004 verdict: VERIFIED;
- novelty: supporting basin certificate, not principal novelty;
- direct exact-model explicit ellipsoidal prior: not found in ROUND-0004.

## 8. TARGET-A20 closure criterion

If an initial point satisfying L1 is rigorously certified to later enter
\[
R_{\rm ext}=\{0<x<\theta,\ y\ge0\},
\]
then:
- L1 gives survival;
- X1 gives extinction of the canonical cold start at the reached point;
- E1 gives a rigorous multibasin reachable fiber.

No long-time numerical classifier is required.
