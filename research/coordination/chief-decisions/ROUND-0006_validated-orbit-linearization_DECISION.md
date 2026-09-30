# ROUND-0006 — CHIEF DECISION

**Date:** 2026-09-30  
**Disposition:** ACCEPT — ORBIT-LINEARIZED APPROXIMATE-INVERSE CAP IS THE PRIMARY ROUTE

## 1. Verdict

ROUND-0006 supports both:
1. orbit-linearized approximate-inverse / radii-polynomial validation;
2. high-order weakly singular collocation.

The ordering is fixed:

\[
\boxed{\text{control amplification first; reduce residual second}.}
\]

The load-bearing CAP theorem is Church & Queirolo (2023/2024 publication), with Becker (2011) providing weakly singular nonautonomous Volterra resolvent theory.

## 2. Required correction accepted

A bounded approximate inverse \(B\) must be injective, or equivalently an actual inverse condition must be proved.

The project specialization below supplies something stronger: \(B\) is explicitly bijective once the discrete nodal operator is invertible.

## 3. Functional setting chosen by Chief

Use a mesh-weighted oscillation Banach norm, not the plain sup norm.

For a finite mesh \(C_n=[t_n,t_{n+1}]\), positive weights \(\vartheta_n>0\), and a fixed vector norm \(|\cdot|_*\), define

\[
\|f\|_{X_\vartheta}
=
\max\left\{
\|f\|_\infty,\,
\max_n
\frac{\operatorname{osc}_{C_n}(f)}{\vartheta_n}
\right\}.
\]

Because the mesh is finite and all \(\vartheta_n>0\),

\[
\|f\|_\infty
\le
\|f\|_{X_\vartheta}
\le
\max\left(1,\frac{2}{\min_n\vartheta_n}\right)\|f\|_\infty.
\]

Therefore \(X_\vartheta=C([0,T],\mathbb R^2)\) as a set, with an equivalent Banach norm.

No external Hölder regularity assumption is introduced.

## 4. Interpolation projection

Let \(\pi\) be nodal piecewise-linear interpolation.

Then
\[
\|\pi f\|_{X_\vartheta}\le \|f\|_{X_\vartheta},
\]
because on each cell
\[
\operatorname{osc}_{C_n}(\pi f)
\le
\operatorname{osc}_{C_n}(f).
\]

Also
\[
\|(I-\pi)f\|_{X_\vartheta}\le2\|f\|_{X_\vartheta}.
\]

Thus the off-grid component is a bounded operator in this same Banach space.

## 5. Source-space formulation

For a numerical approximation \(\hat x\), define
\[
\rho=\phi-g(\hat x),
\qquad
e=I^\alpha f.
\]

The exact source equation is
\[
\mathcal H(f)
=
f-
\left[g(\hat x+I^\alpha f)-g(\hat x)\right]
+\rho
=0.
\]

Its derivative at \(0\) is
\[
D\mathcal H(0)=I-K,
\qquad
(Kf)(t)=A(t)I^\alpha f(t),
\quad
A(t)=Dg(\hat x(t)).
\]

This is the formulation to use for the rigorous radii polynomial.

## 6. Important discrete correction

For source variables, the nodal discrete operator is

\[
\boxed{
L_h^{(f)}=I-AW,
}
\]

not \(I-WA\).

TASK-0005 Stage A used \(I-WA\) correctly for **state-error amplification**.

TASK-0005 Stage D then wrote the \(Z_1\) identity in source space but reused the state-space inverse. That mixing must be corrected before any rigorous \(Z_1\) claim.

The small sign-aware amplification result remains strong evidence; the radii implementation must now be rebuilt with \(I-AW\).

## 7. Exact approximate inverse

Let \(P_h=\operatorname{range}\pi\), and define
\[
K_h=\pi K\pi.
\]

On \(P_h\),
\[
L_h=I-K_h.
\]

Assume \(L_h\) is invertible and define
\[
\boxed{
B=L_h^{-1}\pi+(I-\pi).
}
\]

Then
\[
\boxed{
B^{-1}=L_h\pi+(I-\pi).
}
\]

Hence \(B\) is bounded and bijective.

This supplies the injectivity condition required by the published radii-polynomial theorem.

## 8. Exact inverse-defect identity

With \(D\mathcal H(0)=I-K\),

\[
\boxed{
I-B(I-K)
=
L_h^{-1}\pi K(I-\pi)
+
(I-\pi)K.
}
\]

Now the TASK-0005 “oscillation assumption” becomes a norm statement:
if \(\|f\|_{X_\vartheta}\le1\), then automatically
\[
\operatorname{osc}_{C_n}(f)\le\vartheta_n.
\]

Thus \(Z_1\) can be rigorously bounded in \(X_\vartheta\) without assuming the unknown exact solution has the empirical oscillation profile.

## 9. CAP theorem specialization

Use
\[
A^\dagger=B^{-1}.
\]

Then
\[
Z_0=\|I-BA^\dagger\|=0
\]
exactly.

Compute:
\[
Y_0=\|B\mathcal H(0)\|_{X_\vartheta},
\]
\[
Z_1=
\|I-BD\mathcal H(0)\|_{X_\vartheta},
\]
and a rigorous derivative-Lipschitz bound \(Z_2(r)\).

If the Church–Queirolo radii polynomial is strictly negative, the exact source \(f\) exists uniquely in the validated ball, and
\[
x=\hat x+I^\alpha f
\]
is the true Caputo trajectory.

## 10. Next action

No more generic web search.

TASK-0006 should implement this exact source-space CAP for B215, including:
- rigorous \(I-AW\) inverse;
- rigorous \(X_\vartheta\) operator bounds;
- rigorous entry;
- rigorous goal-oriented \(M_T\).

If successful, TARGET-A20 closes.
