# Cold-Start Extinction Strip

**Owner:** Chief Researcher  
**Date:** 2026-09-29  
**Status:** PROVED FROM PUBLISHED HYPOTHESES / SUPPORTING THEOREM

## 1. Model

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

Define
\[
R_{\rm ext}
=
\{(x,y):0<x<\theta,\ y\ge0\}.
\]

## 2. THEOREM X1 — cold-start extinction strip

If
\[
\theta<\frac{m}{b},
\]
then every standard physical initial condition
\[
(x_0,y_0)\in R_{\rm ext}
\]
has a global nonnegative solution satisfying
\[
(x(t),y(t))\to(0,0).
\]

Equivalently,
\[
\iota(R_{\rm ext})\subseteq\mathcal B(\iota(0,0)).
\]

## 3. Proof

### Step 1 — positivity

The vector field is locally Lipschitz and quasi-positive on the coordinate axes:
\[
F_1(0,y)=0,\qquad F_2(x,0)=0.
\]

Published Caputo viability theory for closed positive sets (Girejko–Mozyrska–Wyrwas, 2011) supplies forward invariance of the nonnegative cone under the present hypotheses; Caputo extremum results of Al-Refai (2012) provide the corresponding first-contact mechanism.

Thus
\[
x(t)\ge0,\qquad y(t)\ge0.
\]

### Step 2 — prey comparison

Let \(u\) solve
\[
{}^C D^\alpha u
=
u(1-u)(u-\theta),
\qquad
u(0)=x_0.
\]

Since \(y(t)\ge0\),
\[
{}^C D^\alpha x
=
x(1-x)(x-\theta)-axy
\le
x(1-x)(x-\theta).
\]

Wu (2020), Theorem 3.2, gives the scalar comparison
\[
0\le x(t)\le u(t)
\]
on the common maximal interval.

From the already audited scalar strong-Allee result,
\[
0<x_0<\theta
\Longrightarrow
0<u(t)<\theta,\qquad u(t)\to0.
\]

Therefore
\[
0\le x(t)\le u(t)<\theta,
\qquad
x(t)\to0.
\]

### Step 3 — predator comparison

Set
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

Compare with
\[
{}^C D^\alpha v=-\delta v,
\qquad v(0)=y_0,
\]
whose exact solution is
\[
v(t)=y_0E_\alpha(-\delta t^\alpha).
\]

Hence
\[
0\le y(t)\le v(t)\to0.
\]

### Step 4 — global continuation

The estimates give
\[
0\le x(t)\le\theta,\qquad
0\le y(t)\le y_0
\]
on every finite interval.

Wu & Liu (2020) give the maximal continuation / blow-up alternative for Caputo systems. Boundedness excludes finite-time termination.

Thus the solution is global and
\[
(x(t),y(t))\to(0,0).
\]
\(\square\)

## 4. Evidence classification

- theorem status: **PROVED FROM PUBLISHED HYPOTHESES**;
- novelty status: supporting theorem, not principal novelty;
- ROUND-0003 verdict: X1 VERIFIED.

## 5. Interpretation

X1 classifies only the canonical **cold start**
\[
\iota(z),\qquad z\in R_{\rm ext}.
\]

It does not classify every reachable continuation state whose present evaluation lies in \(R_{\rm ext}\).

That distinction is the core of the principal theorem program.
