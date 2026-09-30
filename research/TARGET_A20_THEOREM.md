# TARGET-A20 — Certified Multibasin Reachable-Fiber Theorem

**Status:** PROVED BY CERTIFIED COMPUTATION UNDER THE DECLARED ARITHMETIC MODEL  
**Date:** 2026-09-30

## System

Consider

\[
{}^CD^{17/20}x
=
x(1-x)\left(x-\frac12\right)
-\frac12xy,
\]

\[
{}^CD^{17/20}y
=
y\left(x-\frac45\right),
\]

with standard initial state

\[
p=
\left(
\frac{277}{100},
\frac{467}{1000}
\right).
\]

Its positive coexistence equilibrium is

\[
E^*=
\left(
\frac45,\frac3{25}
\right).
\]

## Certified facts

The exact standard trajectory \(x(t;p)\):

1. is validated on \([0,300]\) by a cellwise computer-assisted fixed-point proof;

2. satisfies
   \[
   0<x(t)<\frac12,\qquad y(t)>0
   \]
   for every
   \[
   t\in I_*:=
   [5.8576774143,\ 13.7275388580];
   \]

3. converges to
   \[
   E^*
   \]
   by THEOREM-M1 with rigorous memory-tail constants.

## Reachable-fiber conclusion

For any \(t_*\in I_*\), define

\[
z=x(t_*;p),
\qquad
\Phi=T_{t_*}\iota(p).
\]

Then

\[
e_0(\Phi)=z=e_0(\iota(z)).
\]

Therefore

\[
\Phi,\iota(z)\in F_z.
\]

The inherited continuation state satisfies

\[
\Phi\in\mathcal B(\iota(E^*)),
\]

while THEOREM-X1 gives

\[
\iota(z)\in\mathcal B(\iota(0,0)).
\]

Consequently

\[
\boxed{
F_z\cap\mathcal B(\iota(E^*))\ne\varnothing,
\qquad
F_z\cap\mathcal B(\iota(0,0))\ne\varnothing.
}
\]

Thus \(F_z\) is a multibasin reachable present-state fiber.

Because the statement holds for every \(t_*\in I_*\), the certified excursion generates a nondegenerate time interval of such fibers.

## Evidence boundary

The analytic theorem chain is exact.

The finite-orbit and tail inequalities are computer-assisted and certified under the arithmetic model declared in TASK-0006:
- Arb for exact-rational/interval analytic layers;
- binary64 with explicit roundoff bounds/slack for selected \(O(N^2)\) positive-sum and inverse layers;
- stated libm few-ulp assumption.

Do not describe this as end-to-end interval arithmetic unless the publication-hardening rerun is completed.
