# Survival-Convergence Program

**Owner:** Chief Researcher  
**Date:** 2026-09-30  
**Status:** CLOSED FOR B215 / PRINCIPAL TARGET PROVED

## 1. Closed benchmark

For
\[
\theta=\frac12,\quad
a=\frac12,\quad
b=1,\quad
m=\frac45,\quad
\alpha=\frac{17}{20},
\]
with
\[
p=(277/100,467/1000),
\]
TASK-0006 certifies the standard physical trajectory on \([0,300]\) and proves the memory-tail inequality M1.

The positive coexistence equilibrium is
\[
E^*=(4/5,3/25).
\]

At the primary cut
\[
T=300,
\]
the certified constants satisfy
\[
K_J\le11.3499043,
\qquad
M_T\le0.043232414,
\]
\[
C_r\le0.3695518+0.1627353r,
\qquad
r=2221/20000,
\]
and
\[
r-K_JC_rr^2-M_T\ge0.0135626>0.
\]

Therefore
\[
x(t;p)\to E^*.
\]

## 2. Certified extinction-strip excursion

The same exact trajectory satisfies
\[
0<x(t)<1/2,\qquad y(t)>0
\]
for every
\[
t\in[5.8576774143,13.7275388580].
\]

Thus the standard trajectory enters the cold-start extinction strip while remaining survival-bound through its inherited continuation state.

## 3. Consequence

X1 + E3 + E1 yield TARGET-A20:

for every certified entry time \(t_*\), the continuation state
\[
T_{t_*}\iota(p)
\]
and the canonical cold start
\[
\iota(x(t_*;p))
\]
have the same present physical value and lie in distinct coexistence/extinction basins.

## 4. Evidence boundary

The current certificate is rigorous under the arithmetic model declared in TASK-0006.

TASK-0007 is publication hardening only; it does not reopen the survival theorem unless it discovers a numerical-proof defect.
