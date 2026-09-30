# Memory-Tail Survival Theorem

**Owner:** Chief Researcher  
**Date:** 2026-09-30  
**Status:** PROVED AND INSTANTIATED FOR B215

## Setup

Let
\[
{}^CD^\alpha u=Ju+N(u),
\qquad0<\alpha<1,
\]
where \(J\) satisfies the Matignon sector condition.

Define
\[
\Psi_J(t)=t^{\alpha-1}E_{\alpha,\alpha}(Jt^\alpha)
\]
and
\[
K_J=\int_0^\infty\|\Psi_J(s)\|\,ds<\infty.
\]

For a standard trajectory with \(u_0=p-E^*\), define at any finite cut \(T\)
\[
v_T(t)
=
E_\alpha(Jt^\alpha)u_0
+
\int_0^T\Psi_J(t-s)N(u(s))\,ds,
\qquad t\ge T.
\]

The exact continuation is
\[
u(t)
=
v_T(t)
+
\int_T^t\Psi_J(t-s)N(u(s))\,ds.
\]

This is not a restart at \(T\): \(v_T\) contains the entire pre-\(T\) history.

## THEOREM M1

Suppose
\[
\|N(u)\|\le C_r\|u\|^2
\qquad(\|u\|\le r),
\]
and
\[
M_T:=\sup_{t\ge T}\|v_T(t)\|.
\]

If
\[
M_T+K_JC_rr^2<r,
\]
then the full inherited-memory trajectory remains in the radius-\(r\) ball for every \(t\ge T\) and
\[
u(t)\to0.
\]

### Proof

A first-exit time \(t_e\) would satisfy
\[
\|u(t_e)\|
\le
M_T+K_JC_rr^2<r,
\]
a contradiction.

Inside the invariant ball,
\[
\|N(u)\|\le C_rr\|u\|,
\]
and strict invariance gives
\[
K_JC_rr<1.
\]

Since \(v_T(t)\to0\), the \(L^1\)-kernel limsup argument yields
\[
L:=\limsup_{t\to\infty}\|u(t)\|
\le
K_JC_rrL.
\]
Therefore \(L=0\). \(\square\)

## B215 instantiation

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
\quad
E^*=(4/5,3/25),
\]
TASK-0006 certifies at \(T=300\):
\[
K_J\le11.3499043,
\]
\[
M_T\le0.043232414,
\]
\[
C_r\le0.3695518+0.1627353r,
\]
with
\[
r=2221/20000
\]
and
\[
r-K_JC_rr^2-M_T\ge0.0135626>0.
\]

Hence
\[
X(t;p)\to E^*.
\]

An independent \(T=1000\) certificate also closes with margin
\[
\ge0.0413364.
\]

## Evidence

The theorem is analytic from published resolvent/Mittag--Leffler theory.

The B215 constants are certified computation under the TASK-0006 arithmetic model; TASK-0007 is hardening the remaining elementary-function assumptions for publication.
