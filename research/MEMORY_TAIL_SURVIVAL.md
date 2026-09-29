# Memory-Tail Survival Theorem

**Owner:** Chief Researcher  
**Date:** 2026-09-29  
**Status:** PROVED FROM PUBLISHED RESOLVENT THEORY / COMPUTATIONAL INSTANTIATION PENDING

## 1. Setup

Let
\[
{}^CD^\alpha u=Ju+N(u),
\qquad
0<\alpha<1,
\]
where \(J\) satisfies the Matignon sector condition
\[
\sigma(J)
\subset
\left\{
\lambda\ne0:
|\arg\lambda|>\frac{\alpha\pi}{2}
\right\}.
\]

Define
\[
\Psi_J(t)
=
t^{\alpha-1}E_{\alpha,\alpha}(Jt^\alpha).
\]

Published stable Mittag-Leffler estimates give
\[
\Psi_J(t)=O(t^{-\alpha-1})
\]
as \(t\to\infty\), while near zero
\[
\Psi_J(t)
=
\frac{t^{\alpha-1}}{\Gamma(\alpha)}I
+
O(t^{2\alpha-1}).
\]

Hence, in every induced finite-dimensional norm,
\[
\boxed{
K_J
=
\int_0^\infty
\|\Psi_J(s)\|\,ds
<\infty.
}
\]

Also
\[
\boxed{
\int_0^\infty\Psi_J(s)\,ds=-J^{-1}.
}
\]

## 2. Exact memory split at time \(T\)

For a standard trajectory generated from \(u_0=p-E^*\), the global variation-of-constants formula is
\[
u(t)
=
E_\alpha(Jt^\alpha)u_0
+
\int_0^t
\Psi_J(t-s)N(u(s))\,ds.
\]

For any \(T>0\) and \(t\ge T\), define the inherited linear-memory response
\[
\boxed{
v_T(t)
=
E_\alpha(Jt^\alpha)u_0
+
\int_0^T
\Psi_J(t-s)N(u(s))\,ds.
}
\]

Then exactly
\[
\boxed{
u(t)
=
v_T(t)
+
\int_T^t
\Psi_J(t-s)N(u(s))\,ds.
}
\]

This is the preferred computational form.

It is algebraically equivalent to splitting the original Volterra equation as
\[
u(t)
=
h_T(t)
+
I^\alpha_T[Ju+N(u)](t),
\]
where
\[
h_T(t)
=
p-E^*
+
\frac1{\Gamma(\alpha)}
\int_0^T
(t-s)^{\alpha-1}F(x(s))\,ds.
\]

The second formulation makes inherited history explicit; the first avoids cancellation in numerical certification.

## 3. Decay of the inherited linear response

For fixed finite \(T\),

\[
E_\alpha(Jt^\alpha)u_0\to0.
\]

Also, on \([0,T]\), \(N(u(s))\) is bounded. Since for each fixed \(s\)
\[
\Psi_J(t-s)\to0
\]
and the history interval is finite,
\[
\int_0^T
\Psi_J(t-s)N(u(s))\,ds
\to0.
\]

Therefore
\[
\boxed{
v_T(t)\to0.
}
\]

Equivalently, in the \(h_T\) formulation, \(h_T(t)\to p-E^*\) and the resolvent identity
\[
\int_0^\infty\Psi_J=-J^{-1}
\]
cancels this constant tail.

## 4. THEOREM M1 — memory-tail survival criterion

Fix an induced norm.

Suppose that, for some \(r>0\),
\[
\|N(u)\|
\le
C_r\|u\|^2
\qquad
(\|u\|\le r).
\]

Define
\[
M_T
=
\sup_{t\ge T}
\|v_T(t)\|.
\]

If
\[
\boxed{
M_T+K_JC_rr^2<r,
}
\]
then the full inherited-memory trajectory satisfies
\[
\|u(t)\|<r
\qquad
(t\ge T)
\]
and
\[
\boxed{
u(t)\to0.
}
\]

### Proof

At \(t=T\),
\[
u(T)=v_T(T),
\]
hence
\[
\|u(T)\|\le M_T<r.
\]

If \(t_e\) were the first exit time from the radius-\(r\) ball, then for \(T\le s\le t_e\),
\[
\|N(u(s))\|\le C_rr^2.
\]

Thus
\[
\|u(t_e)\|
\le
M_T+
\int_T^{t_e}
\|\Psi_J(t_e-s)\|C_rr^2\,ds
\le
M_T+K_JC_rr^2
<r,
\]
contradiction.

So the tail remains in the ball.

Within the ball,
\[
\|N(u)\|\le C_rr\|u\|.
\]

Let
\[
L=\limsup_{t\to\infty}\|u(t)\|.
\]

The strict invariance inequality implies
\[
K_JC_rr<1.
\]

Split the nonlinear convolution at a large fixed time \(S\):
the contribution from \([T,S]\) tends to zero because \(\Psi_J(t-s)\to0\);
the remaining contribution is bounded asymptotically by
\[
K_JC_rr(L+\varepsilon).
\]

Since \(v_T(t)\to0\),
\[
L\le K_JC_rr(L+\varepsilon).
\]

Letting \(\varepsilon\downarrow0\),
\[
L\le K_JC_rrL.
\]

Hence \(L=0\). \(\square\)

## 5. Computational sanity checks

Any certified \(K_J\) must satisfy
\[
\boxed{
K_J\ge\|J^{-1}\|
}
\]
because
\[
\int_0^\infty\Psi_J=-J^{-1}.
\]

This is a mandatory validation check for TASK-0004.

## 6. Relation to O1/O2

O1 does not apply because M1 certifies a continuation state using its complete inherited history, not the cold start at \(x(T)\).

O2 does not apply because the large early excursion is absorbed exactly into \(v_T\); the radius-\(r\) nonlinear estimate is imposed only after the late cut time.

## 7. TARGET-A20 closure

For exact-rational W1, if TASK-0004 certifies M1 at any finite \(T\), then survival is rigorous.

Together with:
- exact-rational certified entry;
- X1 cold-start extinction;
- E1 basin-entry geometry;

this proves TARGET-A20.
