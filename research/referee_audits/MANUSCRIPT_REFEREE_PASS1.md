# Referee Audit Pass 1 — Mathematical Scope and Proof Chain

**Date:** 2026-09-30  
**Role:** hostile internal referee  
**Scope:** manuscript theorem chain, definitions, and certified-computation interface  
**Verdict:** PASS WITH MINOR FIXES / no principal mathematical gap found

## 1. Principal theorem logic

### Claim
For every certified \(t_*\in I_*\), the reachable fiber
\[
\mathcal F_{X(t_*;p)}
\]
contains:
- the inherited continuation state \(T_{t_*}\iota(p)\) in the coexistence basin;
- the canonical cold start \(\iota(X(t_*;p))\) in the extinction basin.

### Audit
PASS.

Dependencies are non-circular:
1. TASK-0006 CAP validates the exact physical orbit and entry into \(R_{\rm ext}\).
2. X1 classifies canonical cold starts in \(R_{\rm ext}\) as extinction-bound.
3. M1 + TASK-0006 tail constants prove the original inherited standard orbit converges to \(E^*\).
4. E3 lifts physical convergence to continuation-state convergence.
5. Basin positive invariance gives the basin label of \(T_{t_*}\iota(p)\).
6. Present evaluation gives the common physical value.
7. E1 yields the multibasin fiber.

No finite-horizon basin label is used as proof.

## 2. State-space definitions

PASS AFTER CHIEF FIXES.

The manuscript now explicitly defines:
- the compatible compact-open metric on \(\mathfrak C\);
- basin \(\mathcal B(A)\) through convergence in that metric;
- physically reachable set \(\mathcal R_\alpha\);
- reachable fiber \(\mathcal F_z\).

The abstract E1 statement was narrowed from merely \(A_-\neq A_+\) to **disjoint basins**, avoiding overgeneralization for arbitrary invariant sets.

## 3. Physical-to-continuation convergence E3

PASS.

The proof controls compact-open convergence on every bounded future window:
\[
\sup_{0\le\eta\le N}\|(T_t\iota(p))(\eta)-X^*\|\to0.
\]

The tail integral is bounded by
\[
N^\alpha \Gamma(\alpha+1)^{-1}
\sup_{s\ge t}\|g(X(s;p))\|,
\]
which tends to zero by continuity of \(g\) and physical convergence.

No global sup-norm convergence is claimed; E4 correctly explains why it generally fails.

## 4. Scalar purity theorem

PASS AS A CONDITIONAL STRUCTURAL RESULT.

The theorem states its barrier, single-basin-component, and finite-time nonattainment hypotheses explicitly.

The strong-Allee scalar specialization relies on published Caputo scalar/attractor results. It is used as a contrast, not as principal novelty.

Recommendation:
keep this section compact; do not broaden the scalar claim beyond the stated hypotheses.

## 5. Cold-start extinction theorem X1

PASS, subject to the cited comparison/viability hypotheses.

Proof chain:
- nonnegative-cone viability;
- prey comparison with scalar strong-Allee equation;
- \(x(t)<\theta\) and \(x(t)\to0\);
- predator inequality
  \[
  {}^CD^\alpha y\le-(m-b\theta)y;
  \]
- Mittag--Leffler decay of \(y\);
- continuation/global-existence theorem.

The strict hypothesis
\[
\theta<m/b
\]
is present.

## 6. Memory-tail theorem M1

PASS.

Exact inherited-memory split:
\[
U(t)=v_T(t)+\int_T^t\Psi_J(t-s)N(U(s))\,ds
\]
is used; no restart at \(T\).

The first-exit argument proves tail invariance.

The limsup argument closes because
\[
K_JC_rr<1
\]
follows strictly from
\[
M_T+K_JC_rr^2<r.
\]

Minor manuscript improvement still advisable:
state explicitly in the generic theorem that the vector norm and its induced matrix norm are fixed throughout, and that the solution/history is known through the finite cut \(T\).

## 7. Exact B215 algebra

PASS.

Independently verified:
\[
E^*=(4/5,3/25),
\]
\[
J=
\begin{pmatrix}
-2/25&-2/5\\
3/25&0
\end{pmatrix},
\]
\[
\lambda_\pm=(-1\pm i\sqrt{29})/25,
\]
\[
N_1=-\xi^3-\frac9{10}\xi^2-\frac12\xi\eta,
\qquad
N_2=\xi\eta.
\]

Adapted norm:
\[
S=
\begin{pmatrix}
-2/5&0\\
1/25&-\sqrt{29}/25
\end{pmatrix},
\quad
\|U\|_S=\|S^{-1}U\|_2,
\]
with exact
\[
S^{-1}JS=
\begin{pmatrix}
-1/25&-\sqrt{29}/25\\
\sqrt{29}/25&-1/25
\end{pmatrix}.
\]

## 8. Finite-history CAP

PASS UNDER TASK-0006 ARITHMETIC MODEL.

The manuscript now states enough mathematics to be logically self-contained:
- source equation \(\mathcal H(f)=0\);
- orbit-linearized \(K=A I^\alpha\);
- source discrete operator \(L_h=I-AW\);
- verified inverse;
- exact inverse-defect identity;
- exact Newton-map decomposition;
- cellwise validation proposition;
- componentwise self-map \(F(b)<b\);
- Perron-weighted contraction.

The final self-map certificate is correctly described as
\[
3N=36000
\]
scalar cellwise inequalities for \(N=12000\), with each cell carrying scalar adapted-norm bounds on sup, oscillation, and interpolation bubble. Internal \(2\times2\) block representations do not change this theorem-level count.

## 9. Evidence margins

PASS; no equality-case fragility.

Primary proof margins:
\[
\kappa\le0.083612,
\]
\[
\min \text{ relative self-map slack}\ge6.036\times10^{-4},
\]
\[
\|X-\widehat X\|_2\le2.2193\times10^{-4},
\]
\[
1/2-x_{\max}\ge0.0309411007
\]
on the representative certified entry cell, and
\[
r-K_JC_rr^2-M_T\ge0.0135626.
\]

Independent \(T=1000\) proof gives a second positive M1 margin
\[
\ge0.0413364.
\]

## 10. Novelty scope

PASS.

The manuscript does not claim novelty for:
- generic Caputo memory;
- continuation-state enlargement;
- fractional trajectory intersections;
- delay/headpoint dependence;
- Allee multistability;
- the ecological vector field;
- generic validated fractional numerics.

Principal wording remains theorem-specific and matches ROUND-0007.

## 11. Open items before submission

Not theorem blockers:
1. TASK-0007 arithmetic hardening.
2. Full LaTeX CI green build and actual page count.
3. Generate data-dependent figures from committed TASK-0006 artifacts.
4. Author/affiliation metadata.
5. Target-journal template conversion.
6. Second and third internal referee passes after TASK-0007 and final figures.

## Referee-1 disposition

\[
\boxed{\text{PASS WITH MINOR FIXES}}
\]

No principal mathematical gap was identified.
