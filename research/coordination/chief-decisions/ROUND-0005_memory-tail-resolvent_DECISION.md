# ROUND-0005 — CHIEF DECISION

**Date:** 2026-09-29  
**Evaluates:** \`research/coordination/web-to-chief/ROUND-0005_memory-tail-resolvent_RETURN.md\`  
**Disposition:** ACCEPT — M1 PROMOTED TO PROVED MEMORY-TAIL SURVIVAL CRITERION

## 1. Executive decision

ROUND-0005 closes the imported mathematics needed for a genuinely memory-dependent survival certificate.

Accepted:

1. the matrix fractional resolvent / variation-of-constants identity;
2. \(L^1\)-integrability of
   \[
   \Psi_J(t)=t^{\alpha-1}E_{\alpha,\alpha}(Jt^\alpha)
   \]
   under the Matignon sector condition;
3. exact splitting of a standard Caputo trajectory at a finite cut time without restart;
4. cancellation of the nonzero asymptotic constant of the inherited input by the linear resolvent;
5. the first-exit and limsup arguments in M1.

Therefore CANDIDATE-M1 is promoted to:

> **THEOREM-M1 — memory-tail survival criterion.**

## 2. Important correction in interpretation

For a finite history cut at \(T\),
\[
h_T(t)
=
p-E^*
+
\frac1{\Gamma(\alpha)}
\int_0^T(t-s)^{\alpha-1}F(x(s))\,ds
\]
does **not** tend to zero.

Rather,
\[
h_T(t)\to p-E^*.
\]

The stable linear resolvent cancels that constant:
\[
\int_0^\infty\Psi_J(s)\,ds=-J^{-1},
\]
so
\[
\mathcal L_J h_T(t)\to0.
\]

No Caputo restart is being used.

## 3. Cleaner computational representation

For certification, do not form
\[
v_T=h_T+(J\Psi_J)*h_T
\]
directly because it contains an asymptotic cancellation.

Starting from the global variation-of-constants formula
\[
u(t)
=
E_\alpha(Jt^\alpha)u_0
+
\int_0^t\Psi_J(t-s)N(u(s))\,ds,
\]
split only the nonlinear convolution at \(T\):

\[
\boxed{
v_T(t)
=
E_\alpha(Jt^\alpha)u_0
+
\int_0^T\Psi_J(t-s)N(u(s))\,ds,
\qquad t\ge T.
}
\]

Then
\[
\boxed{
u(t)
=
v_T(t)
+
\int_T^t\Psi_J(t-s)N(u(s))\,ds.
}
\]

This is algebraically equivalent to the inherited-input formulation but is better conditioned for rigorous computation.

It also makes
\[
v_T(t)\to0
\]
transparent:
- the first term decays under Matignon stability;
- the second is convolution over a fixed finite history interval with a kernel that decays to zero.

## 4. THEOREM-M1

Fix an induced norm.

Assume:
\[
K_J=\int_0^\infty\|\Psi_J(s)\|\,ds<\infty,
\]
\[
\|N(u)\|\le C_r\|u\|^2
\quad
(\|u\|\le r),
\]
and define
\[
M_T=\sup_{t\ge T}\|v_T(t)\|.
\]

If
\[
v_T(t)\to0
\]
and
\[
\boxed{
M_T+K_JC_rr^2<r,
}
\]
then the actual inherited continuation tail remains in the radius-\(r\) ball for all \(t\ge T\) and
\[
u(t)\to0.
\]

### Proof

Before a hypothetical first exit,
\[
\|N(u(s))\|\le C_rr^2.
\]

Thus
\[
\|u(t)\|
\le
M_T+K_JC_rr^2<r,
\]
contradicting first exit.

Therefore the tail remains bounded in the ball globally.

Inside it,
\[
\|N(u)\|\le C_rr\|u\|.
\]

The strict invariance inequality implies
\[
K_JC_rr<1.
\]

Using the \(L^1\) kernel and splitting the convolution into a fixed early part and a late part yields
\[
L:=\limsup_{t\to\infty}\|u(t)\|
\le
K_JC_rr\,L.
\]

Hence \(L=0\). \(\square\)

## 5. Source chain

Load-bearing published support:
- Gripenberg–Londen–Staffans (1990), convolution resolvents;
- Cong–Doan–Siegmund–Tuan (2016), stable Mittag-Leffler kernel and Lyapunov–Perron argument;
- Cong–Doan–Tuan (2017), matrix Caputo variation of constants;
- Cong–Tuan–Trinh (2020), asymptotic/Mittag-Leffler stability framework.

Recent Salas–Altamirano–Martínez (2026) is an important novelty-pressure reference for certified matrix Mittag-Leffler propagation, but does not close the project theorem.

## 6. Consequence for TARGET-A20

The theoretical survival route is now closed.

For exact-rational W1, only a rigorous numerical inequality remains:

\[
\boxed{
M_T+K_JC_rr^2<r.
}
\]

If TASK-0004 certifies it at some finite cut \(T\), then:
- M1 proves W1 survives;
- W1 already has exact-rational certified entry into \(R_{\rm ext}\);
- X1 makes the canonical cold start there extinct;
- E1 yields a rigorous multibasin reachable fiber.

## 7. Search posture

No further literature round now.

If TASK-0004 succeeds, immediately launch the final theorem-specific novelty audit before manuscript mode.
