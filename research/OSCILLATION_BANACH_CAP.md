# Oscillation-Banach Computer-Assisted Proof Framework

**Owner:** Chief Researcher  
**Date:** 2026-09-30  
**Status:** REALIZED SUCCESSFULLY FOR B215

## 1. Final lesson

The final B215 proof does not require a scalar radii polynomial.

It uses a strictly stronger cellwise positive-operator formulation.

For each cell \(C_n\), track:
- source sup bound \(\omega_n\);
- source oscillation bound \(\theta_n\);
- interpolation-bubble bound \(\beta_n\).

Collect
\[
b=(\omega,\theta,\beta).
\]

The validated Newton-like map has a computable nonnegative bound map
\[
F(b)=Y+Mb+Q_2(b).
\]

TASK-0006 certifies
\[
F(b)<b
\]
componentwise.

This proves self-mapping of the closed cellwise set \(S_b\).

## 2. Contraction

Let \(q\) be strictly positive Perron-style weights for the derivative bound map on \(S_b\).

Define
\[
\|h\|_q
=
\max\left\{
\max_n\frac{\sup_{C_n}|h|}{q_n^{\rm sup}},
\max_n\frac{\operatorname{osc}_{C_n}h}{q_n^{\rm osc}},
\max_n\frac{\sup_{C_n}|(I-\pi)h|}{q_n^{\rm bub}}
\right\}.
\]

On the finite mesh all \(q\)-weights are positive, so this norm is equivalent to the sup topology.

TASK-0006 certifies
\[
\operatorname{Lip}(T|_{S_b})\le0.083612
\]
for the primary \(T=300\) proof.

Therefore Banach gives the unique fixed point.

## 3. Verified inverse

The source-space nodal derivative is
\[
L_h=I-AW.
\]

TASK-0006 verifies invertibility through a float inverse plus a rigorous residual/Neumann correction.

At \(T=300\):
\[
\|E\|_\infty\le2.09\times10^{-10}.
\]

Thus the approximate inverse is injective and the fixed point solves the exact source equation.

## 4. Primary certificate

B215, \(T=300,N=12000\):

\[
F(b)<b
\]
with relative slack at least
\[
6.036\times10^{-4}.
\]

\[
\kappa\le0.083612.
\]

Adapted state error:
\[
\le4.8661\times10^{-4}.
\]

Physical error:
\[
\le2.2193\times10^{-4}.
\]

## 5. Independent redundancy

A second complete certificate at
\[
T=1000,\ N=20000
\]
also closes:
\[
\kappa\le0.187495.
\]

This is not needed for the theorem but is useful robustness evidence.

## 6. Arithmetic boundary

The CAP is rigorous under the explicit TASK-0006 arithmetic model.

It is not yet an end-to-end Arb computation.

Do not erase that qualifier in manuscript prose.
