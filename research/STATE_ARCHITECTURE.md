# State Architecture and Current Theorem Program

**Owner:** Chief Researcher  
**Date:** 2026-09-30  
**Status:** PRINCIPAL ARCHITECTURE CLOSED / TARGET-A20 PROVED

## 1. Continuation-state architecture

For
\[
{}^CD^\alpha x=g(x),
\qquad0<\alpha<1,
\]
use
\[
\mathfrak C=C(\mathbb R_+,\mathbb R^d)
\]
with the compact-open topology and the Doan--Kloeden continuation-state semidynamical system \(T_t\).

Define
\[
\iota(z)(\tau)\equiv z,
\qquad
e_0(f)=f(0),
\]
\[
\mathcal R_\alpha
=
\{T_t\iota(p):t\ge0,\ p\in X_{\rm phys}\},
\]
and
\[
\mathcal F_z=e_0^{-1}(z)\cap\mathcal R_\alpha.
\]

## 2. Structural mechanism

E1 proves that if:
- cold starts in \(U_-\) belong to basin \(A_-\);
- a standard initial state \(p\) belongs to a distinct basin \(A_+\);
- its physical orbit reaches \(z\in U_-\);

then
\[
T_{t_*}\iota(p),\ \iota(z)\in\mathcal F_z
\]
belong to distinct basins.

E3 proves that physical convergence of a standard IVP to an equilibrium lifts to compact-open convergence of its continuation state.

## 3. Closed B215 realization

For
\[
\alpha=17/20,\quad
\theta=1/2,\quad
a=1/2,\quad
b=1,\quad
m=4/5,
\]
\[
p=(277/100,467/1000),
\]
TASK-0006 certifies:
- entry into
  \[
  R_{\rm ext}=\{0<x<1/2,y>0\}
  \]
  for every time in
  \[
  I_*=[5.8576774143,13.7275388580];
  \]
- convergence of the original standard trajectory to
  \[
  E^*=(4/5,3/25).
  \]

X1 classifies every cold start in \(R_{\rm ext}\) as extinction-bound.

Hence, for every \(t_*\in I_*\),
\[
\mathcal F_{x(t_*;p)}
\]
intersects both extinction and coexistence basins.

## 4. Principal status

\[
\boxed{\text{TARGET-A20 PROVED}}
\]

by certified computation under the TASK-0006 arithmetic model.

ROUND-0007 finds no direct published theorem match and returns:
\[
\boxed{\text{NOVELTY SURVIVES WITH CLAIM NARROWING}}.
\]

## 5. Manuscript precision

The certified result is indexed by a nondegenerate **time interval**.

Injectivity of
\[
t\mapsto x(t;p)
\]
on that interval has not been separately certified.  Therefore manuscript text should avoid claiming a topological arc of distinct fibers unless such injectivity is later proved.
