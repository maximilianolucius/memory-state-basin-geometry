# Oscillation-Banach Computer-Assisted Proof Framework

**Owner:** Chief Researcher  
**Date:** 2026-09-30  
**Status:** THEORETICAL FRAMEWORK CLOSED / NUMERICAL BOUNDS PENDING

## 1. Source equation

Let
\[
\hat x=p+I^\alpha\phi
\]
be the numerical Volterra approximation and
\[
\rho=\phi-g(\hat x).
\]

Write
\[
x=\hat x+e,
\qquad
e=I^\alpha f.
\]

Then the exact Caputo IVP is equivalent to
\[
\boxed{
\mathcal H(f)=0,
}
\]
where
\[
\mathcal H(f)
=
f-
\left[g(\hat x+I^\alpha f)-g(\hat x)\right]
+\rho.
\]

At \(f=0\),
\[
\mathcal H(0)=\rho.
\]

Set
\[
A(t)=Dg(\hat x(t)).
\]

Then
\[
D\mathcal H(0)=I-K,
\qquad
(Kf)(t)=A(t)I^\alpha f(t).
\]

## 2. Mesh-weighted oscillation Banach space

Let
\[
0=t_0<\cdots<t_N=T,
\qquad
C_n=[t_n,t_{n+1}],
\]
and choose fixed positive weights
\[
\vartheta_n>0.
\]

In a fixed vector norm \(|\cdot|_*\), define
\[
\operatorname{osc}_{C_n}(f)
=
\sup_{s,t\in C_n}|f(t)-f(s)|_*,
\]
and
\[
\boxed{
\|f\|_\vartheta
=
\max\left\{
\sup_{0\le t\le T}|f(t)|_*,
\max_n
\frac{\operatorname{osc}_{C_n}(f)}{\vartheta_n}
\right\}.
}
\]

Because the mesh is finite and every \(\vartheta_n>0\),
\[
\|f\|_\infty
\le
\|f\|_\vartheta
\le
\max\left(1,\frac{2}{\min_n\vartheta_n}\right)\|f\|_\infty.
\]

Hence this is an equivalent Banach norm on
\[
C([0,T],\mathbb R^2).
\]

The weights are part of the proof design and may be optimized.

## 3. Piecewise-linear projection

Let \(\pi\) be nodal PL interpolation.

Then:
\[
\pi^2=\pi,
\]
\[
\|\pi\|_{X_\vartheta\to X_\vartheta}\le1,
\]
and
\[
\|I-\pi\|_{X_\vartheta\to X_\vartheta}\le2.
\]

The key implication is:
\[
\|f\|_\vartheta\le r
\quad\Longrightarrow\quad
\operatorname{osc}_{C_n}(f)\le r\vartheta_n.
\]

Thus off-grid oscillation control is intrinsic to the norm and requires no guessed regularity of the exact source.

## 4. Source-space discrete derivative

For \(f\in\operatorname{range}\pi\),
\[
I^\alpha f(t_n)
=
\sum_jW_{nj}f(t_j).
\]

Therefore
\[
(\pi K\pi f)(t_n)
=
A_n\sum_jW_{nj}f_j.
\]

Hence the exact nodal matrix is
\[
\boxed{
K_h=AW,
\qquad
L_h=I-AW.
}
\]

This differs from the state-error discretization
\[
I-WA.
\]

Both are legitimate for their own variables; they must not be mixed.

## 5. Approximate inverse

Assume \(L_h\) is invertible on the PL subspace.

Define
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

Proof:
decompose
\[
f=\pi f+(I-\pi)f.
\]
The two components lie in complementary invariant subspaces for \(B\), on which \(B\) acts as \(L_h^{-1}\) and \(I\), respectively.

Thus \(B\) is bounded and bijective.

## 6. Exact inverse-defect identity

Because
\[
D\mathcal H(0)=I-K
\]
and
\[
L_h=I-\pi K\pi,
\]
direct algebra gives
\[
\boxed{
I-B(I-K)
=
L_h^{-1}\pi K(I-\pi)
+
(I-\pi)K.
}
\]

This is the rigorous target for \(Z_1\).

Both terms are controlled by cell oscillation rather than only global amplitude.

## 7. Radii-polynomial specialization

Take
\[
A^\dagger=B^{-1}.
\]

Then
\[
Z_0=
\|I-BA^\dagger\|
=0.
\]

Let
\[
Y_0
\ge
\|B\mathcal H(0)\|_\vartheta,
\]
\[
Z_1
\ge
\|I-BD\mathcal H(0)\|_\vartheta,
\]
and
\[
Z_2(r)
\ge
\sup_{\|f\|_\vartheta\le r}
\|B(D\mathcal H(f)-D\mathcal H(0))\|_\vartheta.
\]

Apply the published Banach-space radii-polynomial theorem of Church & Queirolo.

A strict negative radii polynomial proves a unique exact source \(f\) in the ball.

Then
\[
x=\hat x+I^\alpha f
\]
is the exact Caputo solution.

## 8. Goal-oriented functional

The final basin theorem needs a rigorous memory-tail response, not only a uniform trajectory enclosure.

For the cut time \(T\), define the functional producing
\[
v_T(t)
=
E_\alpha(Jt^\alpha)u_0
+
\int_0^T
\Psi_J(t-s)N(u(s))\,ds.
\]

Once \(f\) is enclosed in the radii ball, propagate that ball directly through the Fréchet derivative of this history functional plus a quadratic remainder.

This can yield a much smaller error than converting a uniform state radius into \(M_T\).

## 9. Evidence status

The Banach-space construction, boundedness/bijectivity of \(B\), and operator identity are analytic.

The actual constants
\[
Y_0,Z_1,Z_2(r)
\]
for B215 remain to be rigorously computed.
