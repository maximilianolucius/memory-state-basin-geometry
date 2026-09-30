# Validated History Strategy

**Owner:** Chief Researcher  
**Date:** 2026-09-30  
**Status:** ACTIVE — ORBIT-LINEARIZED A-POSTERIORI VALIDATION

## 1. Problem

THEOREM-M1 can certify survival once
\[
M_T<0.038078
\]
is rigorously available for W1 in the current adapted norm.

Numerically:
\[
M_{1000}\approx0.014.
\]

The missing step is a rigorous history enclosure on \([0,T]\).

The current normwise verifier fails because it pays a huge amplification during the excursion.

## 2. Nonlinear Volterra operator

Define on \([0,T]\)
\[
\mathcal F(x)
=
x-p-I^\alpha[g(x)].
\]

For a numerical approximation \(\hat x\), set
\[
A(t)=Dg(\hat x(t)).
\]

The Fréchet derivative is
\[
D\mathcal F(\hat x)e
=
e-I^\alpha[A(\cdot)e].
\]

Write
\[
\mathcal L_{\hat x}
=
I-I^\alpha A(\cdot).
\]

For the error
\[
e=x-\hat x,
\]
\[
\mathcal L_{\hat x}e
=
-d+
I^\alpha R_{\hat x}(e),
\]
where
\[
d=\mathcal F(\hat x)
\]
and
\[
R_{\hat x}(e)
=
g(\hat x+e)-g(\hat x)-A e
\]
is quadratic in \(e\).

## 3. Candidate validation principle V1

Suppose a bounded operator \(B\) approximates
\[
\mathcal L_{\hat x}^{-1}.
\]

Let
\[
Y=\|B d\|,
\]
and rigorously bound
\[
Z_1=\|I-B\mathcal L_{\hat x}\|,
\]
and for \(\|e\|\le r\),
\[
\|B I^\alpha R_{\hat x}(e)\|
\le Z_2(r).
\]

If the associated Newton/radii inequality
\[
\boxed{
Y+Z_1r+Z_2(r)<r
}
\]
holds, then a true solution exists in the radius-\(r\) neighborhood of \(\hat x\).

The exact fixed-point formulation and uniqueness hypotheses are to be audited by ROUND-0006.

## 4. Implementation preference

The Volterra structure makes the discretized derivative block lower triangular.

Preferred implementation:
1. piecewise polynomial/collocation representation of \(\hat x\);
2. exact fractional integration of polynomial basis functions;
3. numerical inversion of the discrete block-lower-triangular linearized operator;
4. interval enclosure of that inverse/action;
5. explicit off-grid/interpolation remainder;
6. radii-polynomial or Newton–Kantorovich closure.

This retains matrix signs/rotations instead of replacing them by \(\|Dg-J\|\).

## 5. Two-stage escalation

### Stage I — amplification test
Before rigorous implementation, compute the discrete inverse response of
\[
\mathcal L_{\hat x}
\]
to defects concentrated on each cell.

Measure a true/discrete operator amplification surrogate.

If it remains \(\gg10^4\), this route is unlikely to close.

If it is \(O(1)\)–\(O(10^2)\), proceed.

### Stage II — residual order
Only then improve the approximation:
- degree 2/3/5 piecewise polynomial;
- graded mesh near the initial singular layer;
- exact \(I^\alpha\) polynomial moments;
- rigorous residual bounds.

## 6. Goal-oriented alternative

The final theorem only needs \(M_T\), not a publication-quality uniform enclosure of every state value.

If possible, certify directly the functional
\[
v_T(t)
=
E_\alpha(Jt^\alpha)u_0
+
\int_0^T\Psi_J(t-s)N(u(s))\,ds.
\]

A goal-oriented bound may use the orbit error only through the weighted history functional above and can be substantially tighter than
\[
\sup_{[0,T]}\|x-\hat x\|.
\]

This should be tested in parallel.

## 7. Success criterion

A history-validation method is successful if it rigorously implies
\[
M_T<0.038078
\]
for W1, or an analogous M1 threshold for another exact-rational entering witness.

Then M1 + X1 + E1 close TARGET-A20.
