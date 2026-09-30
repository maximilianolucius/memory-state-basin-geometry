# Claim Registry

**Status:** TARGET-A20 PROVED; FINAL NOVELTY AUDIT ACTIVE.

## Principal result

### TARGET-A20 — multibasin reachable present-state fibers

**Status:** PROVED BY CERTIFIED COMPUTATION UNDER THE DECLARED ARITHMETIC MODEL.

Exact system:
\[
{}^CD^{17/20}x
=
x(1-x)(x-1/2)-\frac12xy,
\]
\[
{}^CD^{17/20}y=y(x-4/5).
\]

Initial state:
\[
p=(277/100,467/1000).
\]

The exact standard orbit:
- enters \(R_{\rm ext}=\{0<x<1/2,y>0\}\) on a certified nondegenerate interval;
- converges to \(E^*=(4/5,3/25)\).

For every certified entry time \(t_*\), the continuation state \(T_{t_*}\iota(p)\) and the cold start \(\iota(x(t_*;p))\) share the same present value but lie in coexistence and extinction basins respectively.

## Supporting results

X1, E1–E4, M1: PROVED.

Finite-history B215 CAP: CERTIFIED COMPUTATION under declared arithmetic model.

Independent full certificates exist at:
- \(T=300,N=12000\);
- \(T=1000,N=20000\).

## Evidence boundary

Not end-to-end interval arithmetic.

The theorem promotion is explicitly conditional on the stated IEEE/libm arithmetic model used to prove the binary64 upper bounds.

## Current gate

ROUND-0007 final hostile novelty audit.
