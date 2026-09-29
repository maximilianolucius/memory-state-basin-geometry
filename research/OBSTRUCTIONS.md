# Structural Obstructions to Present-State Survival Certificates

**Owner:** Chief Researcher  
**Date:** 2026-09-29  
**Status:** O1 PROVED / O2 PROVED FOR DECLARED CERTIFICATE CLASS

## 1. O1 — forward-invariant physical survival-set obstruction

Let
\[
S\subset X_{\rm phys}
\]
be a set such that
\[
\iota(S)\subseteq\mathcal B(A_{\rm surv}).
\]

Let
\[
R_{\rm ext}\subset X_{\rm phys}
\]
satisfy
\[
\iota(R_{\rm ext})\subseteq\mathcal B(A_{\rm ext}),
\qquad
A_{\rm surv}\ne A_{\rm ext}.
\]

Then
\[
S\cap R_{\rm ext}=\varnothing.
\]

If, in addition, a standard physical orbit starting at \(p\in S\) satisfies
\[
x(t;p)\in S
\qquad\forall t\ge0,
\]
then that orbit cannot enter \(R_{\rm ext}\).

### Proof

A point \(z\in S\cap R_{\rm ext}\) would make the same canonical state
\[
\iota(z)
\]
belong to two distinct asymptotic basins, impossible.

Forward invariance of the physical orbit inside \(S\) then prevents entry into \(R_{\rm ext}\). \(\square\)

## 2. Consequence for THEOREM-L1

The L1 ellipsoid
\[
\Omega
=
\left\{
z:
(z-E^*)^\top P(z-E^*)
<
\lambda_{\min}(P)r^2
\right\}
\]
has:
\[
\iota(\Omega)\subseteq\mathcal B(E^*)
\]
and L1 keeps any standard orbit starting in \(\Omega\) inside a smaller Lyapunov sublevel, hence inside \(\Omega\).

Therefore
\[
\Omega\cap R_{\rm ext}=\varnothing
\]
and no L1-certified initial state can generate the threshold-entry event.

This conclusion is independent of the sharpness of \(C_r\), \(P\), or \(r\).

## 3. Interpretation

O1 is a structural statement about proof methods.

The desired phenomenon is precisely that the basin label is **not** determined by present physical state.

Therefore a proof that certifies survival by trapping the trajectory inside a physical-state set all of whose cold starts survive is fundamentally incompatible with the desired threshold entry.

The survival certificate must depend on:
- the continuation state/history;
- a nonlocal functional of the past; or
- a tail equation in which inherited memory appears explicitly.

## 4. O2 — global diagonal weighted-max resolvent obstruction

For the Hurwitz coexistence Jacobian and the specific certificate class studied in TASK-0003 Stage E, define
\[
g=x^*-\theta,
\qquad
c_2=3x^*-1-\theta.
\]

A necessary condition for a global weighted-max ball certificate to both:
- contain enough overshoot to reach the threshold; and
- satisfy the nonlinear contraction smallness condition,

implies
\[
\frac{4gc_2}{x^*(1-x^*)}<1.
\]

Hurwitz stability gives
\[
x^*>\frac{1+\theta}{2},
\]
hence
\[
g>\frac{1-\theta}{2},
\qquad
c_2>\frac{1+\theta}{2},
\]
and because \(x^*>1/2\),
\[
x^*(1-x^*)<
\frac{1-\theta^2}{4}.
\]

Therefore
\[
\frac{4gc_2}{x^*(1-x^*)}>4,
\]
contradiction.

### Scope

O2 excludes only the declared certificate class:
- one global tail radius from time zero;
- diagonal weighted max norm;
- kernel \(L^1\) bound \(K\);
- crude global quadratic remainder bound.

It does **not** exclude:
- memory-tail certificates after a finite validated excursion;
- non-diagonal adapted norms;
- time-weighted norms;
- a posteriori bounds around a computed nonlinear tail;
- non-Hurwitz fractional-stable regimes.
