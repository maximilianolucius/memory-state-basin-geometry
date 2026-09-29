# Cold-Start Extinction Strip — Theorem Draft

**Owner:** Chief Researcher  
**Date:** 2026-09-29  
**Status:** ANALYTIC PROOF DRAFT / POSITIVITY + COMPARISON SOURCE AUDIT PENDING

## 1. Model class

Consider
\[
{}^C D^\alpha x
=
x(1-x)(x-\theta)-a x y,
\]
\[
{}^C D^\alpha y
=
y(bx-m),
\qquad
0<\alpha<1,
\]
with
\[
a,b,m>0,\qquad 0<\theta<1.
\]

Assume the positive cone is invariant and the scalar Caputo comparison theorem applies in the form used below.

## 2. Candidate theorem X1 — cold-start extinction strip

If
\[
\theta<\frac{m}{b},
\]
then every standard physical initial condition
\[
0<x_0<\theta,\qquad y_0\ge0
\]
converges to
\[
(0,0).
\]

Equivalently, with
\[
R_{\rm ext}
=
\{(x,y):0<x<\theta,\ y\ge0\},
\]
we have
\[
\iota(R_{\rm ext})\subseteq\mathcal B((0,0)).
\]

## 3. Proof draft

Let \(u\) solve the scalar strong-Allee Caputo equation
\[
{}^C D^\alpha u
=
u(1-u)(u-\theta),
\qquad
u(0)=x_0.
\]

Because \(y(t)\ge0\),
\[
{}^C D^\alpha x
=
x(1-x)(x-\theta)-axy
\le
x(1-x)(x-\theta).
\]

Under the audited scalar comparison theorem and equal initial data,
\[
0\le x(t)\le u(t).
\]

By COROLLARY-S1A,
\[
0<x_0<\theta
\Longrightarrow
u(t)\to0
\]
and \(u(t)<\theta\) for all positive time.

Hence
\[
0\le x(t)\le u(t)<\theta,
\qquad
x(t)\to0.
\]

Now set
\[
\delta=m-b\theta>0.
\]

Since \(x(t)<\theta\),
\[
{}^C D^\alpha y
=
y(bx-m)
\le
-\delta y.
\]

Comparison with
\[
{}^C D^\alpha v=-\delta v,
\qquad
v(0)=y_0,
\]
gives
\[
0\le y(t)
\le
y_0E_\alpha(-\delta t^\alpha)
\to0.
\]

Therefore
\[
(x(t),y(t))\to(0,0).
\]
\(\square\)

## 4. What still requires audit

Before promotion to PROVED FROM PUBLISHED HYPOTHESES, verify:

1. positive-cone invariance for this Caputo system under the exact solution regularity available;
2. the exact scalar comparison theorem hypotheses for
   \[
   {}^C D^\alpha x\le f(x),\quad x(0)=u(0);
   \]
3. applicability to the polynomial vector field on the positively invariant/bounded region;
4. global continuation needed for the asymptotic conclusion;
5. whether the linear comparison
   \[
   {}^C D^\alpha y\le-\delta y
   \]
   requires any additional regularity.

ROUND-0003 owns this source/hypothesis audit.

## 5. Structural interpretation

This theorem concerns **cold starts**:
\[
\iota(z),\qquad z\in R_{\rm ext}.
\]

It does not say that every continuation state whose present evaluation lies in \(R_{\rm ext}\) is in the extinction basin.

TASK-0001 numerically exhibits exactly that distinction:
a continuation state \(T_t\iota(p)\) can satisfy
\[
e_0(T_t\iota(p))\in R_{\rm ext}
\]
while retaining enough prehistory to recover.

That difference between the constant physical slice and the full reachable memory-state fiber is the central project mechanism.
