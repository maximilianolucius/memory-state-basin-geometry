# Computer-Assisted Validation Draft

**Status:** manuscript prose draft v1 — Section 6  
**Date:** 2026-09-30

---

# 6. Computer-assisted validation of the finite memory segment

The proof of the main theorem requires two finite-time facts about one exact rational point IVP: the trajectory must be enclosed tightly enough to certify its entry into the cold-start extinction strip, and the same finite history must be controlled strongly enough to evaluate the inherited memory term in Theorem 4.2.  A direct normwise fractional Grönwall estimate is far too pessimistic for this orbit because it destroys the sign and rotational cancellations of the time-dependent linearization.  We therefore validate the computed trajectory by an orbit-linearized Volterra fixed-point argument.

## 6.1 Source correction equation

Let the numerical center be written in Volterra form as
\[
\widehat X(t)
=
p+I^\alpha\phi(t),
\]
where \(X=(x,y)\) and
\[
(I^\alpha f)(t)
=
\frac1{\Gamma(\alpha)}
\int_0^t(t-s)^{\alpha-1}f(s)\,ds.
\]
Define the source residual
\[
\rho(t)
=
\phi(t)-g(\widehat X(t)).
\]
If the exact solution is represented as
\[
X=\widehat X+I^\alpha f,
\]
then the correction source \(f\) satisfies
\[
\mathcal H(f)=0,
\]
where
\[
\mathcal H(f)
=
f-
\left[g(\widehat X+I^\alpha f)-g(\widehat X)\right]
+\rho.
\]
At \(f=0\),
\[
D\mathcal H(0)=I-K,
\qquad
(Kf)(t)=A(t)I^\alpha f(t),
\]
with
\[
A(t)=Dg(\widehat X(t)).
\]

This formulation is useful because the strongly non-normal finite excursion is retained in the full time-dependent matrix \(A(t)\), rather than being replaced by a scalar absolute-value Lipschitz bound.

## 6.2 Discrete inverse and continuous correction

Let
\[
0=t_0<t_1<\cdots<t_N=T
\]
be the adaptive validation mesh and let \(\pi\) denote continuous piecewise-linear interpolation at the nodes.  The fractional integral of the hat basis gives a lower-triangular block matrix \(W\).  In the source variable, the projected derivative is
\[
L_h=I-AW.
\]
The ordering \(AW\), rather than \(WA\), is essential because \(A\) acts after the fractional integral in
\[
Kf=A I^\alpha f.
\]

A numerical block-lower-triangular inverse \(\widetilde R\) is computed by forward substitution.  Its residual against the exact data is enclosed:
\[
E=I-L_h\widetilde R.
\]
For the primary certificate
\[
T=300,\qquad N=12000,
\]
the verified residual satisfies
\[
\|E\|_\infty\le2.09\times10^{-10}.
\]
The Neumann argument therefore proves invertibility of \(L_h\) and supplies rigorous blockwise bounds for \(L_h^{-1}\).

The continuous approximate inverse is
\[
B=L_h^{-1}\pi+(I-\pi).
\]
Because the piecewise-linear and interpolation-bubble subspaces are complementary,
\[
B^{-1}=L_h\pi+(I-\pi),
\]
so \(B\) is injective.  Consequently a fixed point of
\[
\mathcal T(f)=f-B\mathcal H(f)
\]
is a zero of \(\mathcal H\), not merely a zero of \(B\mathcal H\).

The analytic foundation for weakly singular Volterra resolvents and high-order/collocation approximations is classical; related computer-assisted approximate-inverse constructions appear in rigorous ODE validation.  Our use of these ingredients is enabling proof technology rather than the principal novelty of the paper \cite{Becker2011WeaklySingularResolvents,BrunnerPedasVainikko1999WeaklySingularCollocation,LiangBrunner2019WeaklySingularCollocation,BredenLessard2018PolynomialCAP,ChurchQueirolo2024HopfCAP}.

## 6.3 Cellwise positive bound map

A single weighted sup norm is unnecessarily restrictive for this trajectory: the largest source defect occurs close to the initial fractional singular layer, whereas the largest accumulated state error and nonlinear sensitivity occur much later.  We therefore retain three cellwise components.  For each cell
\[
C_n=[t_n,t_{n+1}],
\]
let
\[
\omega_n
\]
bound
\[
\sup_{t\in C_n}|f(t)|,
\]
let
\[
\vartheta_n
\]
bound
\[
\operatorname{osc}_{C_n}f,
\]
and let
\[
\beta_n
\]
bound the interpolation bubble
\[
\sup_{t\in C_n}|(I-\pi)f(t)|.
\]
Collect these quantities into
\[
b=(\omega,\vartheta,\beta).
\]

The Newton-like map admits a monotone componentwise upper-bound operator
\[
F(b)
=
Y+Mb+Q_2(b),
\]
where:
- \(Y\) bounds the propagated source residual \(B\rho\);
- \(M\) bounds the orbit-linearized interpolation terms;
- \(Q_2\) bounds the nonlinear derivative remainder.

Every entry of these vectors is a nonnegative upper bound.  Thus
\[
F(b)<b
\]
componentwise proves that the closed cellwise set
\[
S_b
=
\left\{
f:
\sup_{C_n}|f|\le\omega_n,\ 
\operatorname{osc}_{C_n}f\le\vartheta_n,\ 
\sup_{C_n}|(I-\pi)f|\le\beta_n
\right\}
\]
is mapped strictly into itself.

For the primary B215 certificate, monotone iteration followed by a \(1\%\) inflation gives
\[
F(b)<b
\]
on all \(3N=36000\) component inequalities, with minimum relative slack
\[
6.036\times10^{-4}.
\]

The conventional one-radius scalar radii inequality does not close for this orbit.  That failure is not used negatively in the theorem: the cellwise vector inequality retains the temporal localization that a single radius discards.

## 6.4 Perron-weighted contraction

Self-mapping alone gives existence only after an additional compactness or fixed-point argument.  Here we prove a genuine contraction.

Let
\[
q=(q^{\rm sup},q^{\rm osc},q^{\rm bub})
\]
be strictly positive weights obtained from the positive derivative-bound operator.  Define
\[
\|h\|_q
=
\max\left\{
\max_n\frac{\sup_{C_n}|h|}{q_n^{\rm sup}},
\max_n\frac{\operatorname{osc}_{C_n}h}{q_n^{\rm osc}},
\max_n\frac{\sup_{C_n}|(I-\pi)h|}{q_n^{\rm bub}}
\right\}.
\]
Because the mesh is finite and every \(q\)-weight is positive, this norm is equivalent to the sup topology on the continuous source space.  Hence the closed set \(S_b\) is complete in \(\|\cdot\|_q\).

The derivative bounds on \(S_b\) give
\[
\operatorname{Lip}_{\|\cdot\|_q}
(\mathcal T|_{S_b})
\le
\kappa,
\]
with the certified value
\[
\kappa\le0.083612.
\]
Banach's fixed-point theorem therefore yields a unique
\[
f^*\in S_b
\]
such that
\[
\mathcal T(f^*)=f^*.
\]
Injectivity of \(B\) implies
\[
\mathcal H(f^*)=0,
\]
and therefore
\[
X(t)=\widehat X(t)+I^\alpha f^*(t)
\]
is the exact Caputo solution on \([0,300]\).

## 6.5 Validated state tube and threshold entry

Propagating the source enclosure through the fractional integral gives
\[
\sup_{0\le t\le300}
\|X(t)-\widehat X(t)\|_{\rm adapted}
\le
4.8661\times10^{-4},
\]
and therefore
\[
\sup_{0\le t\le300}
\|X(t)-\widehat X(t)\|_2
\le
2.2193\times10^{-4}.
\]

Adding this certified pad to the cellwise state enclosures proves
\[
0<x(t)<\frac12,\qquad y(t)>0
\]
for every
\[
t\in
I_*=
[5.8576774143,\ 13.7275388580].
\]
A representative interior cell is
\[
t\in[8.9839195370,\ 8.9927932624],
\]
where
\[
x\in[0.468938793,\ 0.469058899],
\qquad
y\ge0.248262346.
\]
Thus the prey threshold is crossed with a certified margin
\[
\frac12-x_{\max}
\ge0.0309411007.
\]

## 6.6 Memory-tail quantities

The same validated finite history is inserted into the exact memory-tail representation from Theorem 4.2.  For the primary cut \(T=300\), the certified values are
\[
K_J\le11.3499043,
\]
\[
M_T\le0.043232414,
\]
and
\[
C_r\le0.3695518+0.1627353r.
\]
At
\[
r=\frac{2221}{20000},
\]
one obtains
\[
r-K_JC_rr^2-M_T
\ge0.0135626>0.
\]
This closes the infinite-time survival proof.

A completely independent validation cut at
\[
T=1000,\qquad N=20000
\]
also closes, with contraction
\[
\kappa\le0.187495
\]
and the larger tail margin
\[
r-K_JC_rr^2-M_T
\ge0.0413364.
\]
The second calculation is not needed logically; it is retained as redundancy against accidental dependence on the primary cut.

## 6.7 Arithmetic model and reproducibility boundary

The current certificate combines exact-rational model data and Arb ball arithmetic with selected binary64 layers for the large \(O(N^2)\) matrix and positive-sum computations.  The latter are accompanied by explicit operation-count/roundoff bounds and outward slack.  The TASK-0006 certificate also assumes a few-ulp accuracy model for selected elementary \(\mathrm{libm}\) functions used in the large-kernel layer.

Accordingly, the result should presently be described as a

> computer-assisted theorem under the stated IEEE-754/libm arithmetic model,

rather than as an end-to-end interval-arithmetic proof.

The publication-hardening computation replaces the remaining load-bearing elementary-function calls by verified enclosures; if that audit reproduces the primary certificate, the wording of this subsection can be strengthened without changing any mathematical theorem or proof architecture.
