# ROUND-0006 — Rigorous orbit-linearized Volterra validation audit

**Agent:** Deep Web Search Agent  
**Search date:** 2026-09-30  
**Request:** `research/coordination/chief-to-web/ROUND-0006_validated-orbit-linearization_REQUEST.md`  
**Priority:** P0 / VALIDATED-NUMERICS GATE

## Executive verdict

### Required ranked recommendation

1. **ORBIT-LINEARIZED APPROXIMATE-INVERSE ROUTE SUPPORTED — PRIMARY**
2. **HIGH-ORDER RESIDUAL ROUTE SUPPORTED — SECONDARY / RESIDUAL REDUCTION**
3. Overall required category: **BOTH**

The two routes should not be treated as competitors. The strongest architecture is:

> high-order singularity-aware approximation to make the defect small **plus** a rigorous Newton/radii-polynomial approximate inverse of the orbit-linearized Volterra operator to avoid the catastrophic normwise amplification seen in TASK-0004.

No published source located gives this exact Caputo-IVP computer-assisted proof end-to-end, but every functional-analytic ingredient needed by the proposed V1 strategy has published support.

---

# Q1 — High-order a-posteriori Volterra methods

## 1. Classical weakly singular collocation

### Brunner, Pedas & Vainikko (1999)

**H. Brunner; A. Pedas; G. Vainikko.**  
“The piecewise polynomial collocation method for nonlinear weakly singular Volterra equations.”  
*Mathematics of Computation* 68(227), 1079–1095.  
DOI **10.1090/S0025-5718-99-01073-X**.

This is directly relevant to the project class. It treats nonlinear second-kind Volterra equations with algebraically weakly singular kernels and proves optimal global/local convergence of piecewise polynomial collocation on graded grids.

**Value to project:** supports replacing the piecewise-linear (hat x) by degree-(p) piecewise polynomials without assuming classical smoothness at the initial point, provided the mesh is graded according to the weak singularity.

**Limitation:** convergence theorem, not a computer-assisted enclosure. It does not by itself supply outward-rounded finite constants certifying one computed orbit.

### Liang & Brunner (2019)

**Hui Liang; Hermann Brunner.**  
“The Convergence of Collocation Solutions in Continuous Piecewise Polynomial Spaces for Weakly Singular Volterra Integral Equations.”  
*SIAM Journal on Numerical Analysis* 57(4), 1875–1896.  
DOI **10.1137/19M1245062**.

Establishes uniform convergence for globally continuous piecewise-polynomial collocation solutions on uniform and graded meshes.

**Value:** source support for a continuous piecewise-polynomial representation compatible with a (C([0,T]))-based CAP.

## 2. A-posteriori estimators

### Adaptive collocation, 2007

“Adaptive collocation methods for Volterra integral and integro-differential equations,” *Applied Mathematics and Computation* 191 (2007), 67–78. DOI **10.1016/j.amc.2006.12.087**.

This paper derives residual-based a-posteriori estimates for smooth and weakly singular Volterra equations and uses them for adaptive mesh refinement.

**Important limitation for our use:** the analysis still propagates residual information through discrete/weakly-singular Grönwall-type bounds. It is therefore precisely the style of estimate that can become unusably pessimistic on a rotating/sign-changing nonlinear excursion. It is useful for mesh design, not sufficient as the core W1 certificate.

### Baccouch 2026

**Mahboub Baccouch.**  
“A Posteriori Error Estimation for the Discontinuous Galerkin Method Applied to Nonlinear Volterra Integro-differential Equations.”  
*Communications on Applied Mathematics and Computation* (2026).  
DOI **10.1007/s42967-026-00617-3**.

Theorem 4 proves, for degree (pge1), that the computable DG error estimator (E_u) satisfies
[
|e_u-E_u|le Ch^{p+2},
]
and the global effectivity index tends to one at rate (O(h)).

**Novelty pressure:** this is a current 2026 residual-based a-posteriori Volterra result.

**But not a direct CAP source for W1:** the model in that paper is a first-order VIDE with a nonsingular time integral and smooth solution hypotheses; the bound contains theoretical constants and is an asymptotic estimator, not an outward-rounded interval enclosure of a Caputo weakly singular IVP.

## 3. Current high-order weak-singular methods

### 2025 product integration

“A Nyström method based on product integration for weakly singular Volterra integral equations with variable exponent.”  
*Journal of Computational and Applied Mathematics* 454 (2025), 116164.  
DOI **10.1016/j.cam.2024.116164**.

Uses product integration with piecewise polynomials and graded meshes; proves rigorous convergence/error estimates and superconvergence.

### Ma & Stynes 2026

**Zheng Ma; Martin Stynes.**  
“A hybrid polynomial spectral collocation method for weakly singular Volterra integral equations with variable exponent.”  
*IMA Journal of Numerical Analysis* (2026).  
DOI **10.1093/imanum/draf144**.

Published 6 March 2026. Uses a hybrid polynomial/spectral treatment designed to retain high order for weak endpoint singularities.

### 2026 singularity-corrected product integration

**Masouri et al. (2026).**  
“High-Order Singularity-Corrected Sum-of-Exponentials Product Integration for Second-Kind Fractional Volterra Equations With Modulated Weakly Singular Kernels.”  
*Mathematical Methods in the Applied Sciences*.  
DOI **10.1002/mma.70970**.

Current published pressure for high-order fractional Volterra quadrature with explicit singularity correction.

## Q1 conclusion

**HIGH-ORDER RESIDUAL ROUTE: SUPPORTED, but not sufficient as a standalone rigorous enclosure strategy.**

The literature strongly supports high-order/graded/singularity-aware construction of (hat x). It does **not** remove the need to validate the inverse sensitivity of the nonlinear operator. For W1, the catastrophic (10^6)–(10^{16}) amplification is an inverse-operator problem, not only a residual-order problem.

---

# Q2 — Newton–Kantorovich / approximate inverse / radii polynomials

## 4. Generic Banach-space theorem directly matches V1

A clean published current theorem is:

**Church et al.**  
“Computer-Assisted Proofs of Hopf Bubbles and Degenerate Hopf Bifurcations.”  
*Journal of Dynamics and Differential Equations* (published online 2023).  
DOI **10.1007/s10884-023-10279-x**.

### Theorem 1

Let (F:X_1	o X_2) be differentiable between Banach spaces, (hat x) an approximate zero, (A^dagger:X_1	o X_2) an approximate derivative, and (A:X_2	o X_1) a bounded **injective** approximate inverse.

If one rigorously bounds
[
|AF(hat x)|le Y_0,
]
[
|I-AA^dagger|le Z_0,
]
[
|A(DF(hat x)-A^dagger)|le Z_1,
]
and on the radius-(r) ball
[
|A(DF(hat x+delta)-DF(hat x))|
le Z_2(r),
]
then negativity of
[
p(r)
=
rZ_2(r)+(Z_0+Z_1-1)r+Y_0
]
implies a unique true zero of (F) in the ball.

The paper explicitly states that the bounds are computed rigorously with interval arithmetic.

## 5. Direct relevance to the Chief's V1

The proposed operator is
[
mathcal F(x)=x-p-I^alpha[g(x)]
]
on a suitable Banach space of vector-valued continuous/piecewise-represented functions.

At (hat x),
[
Dmathcal F(hat x)e
=
e-I^alpha[A(cdot)e],
qquad
A(t)=Dg(hat x(t)).
]

This is exactly a nonlinear zero-finding problem in Banach space.

Choose:
- (A^dagger) = rigorous representation of the orbit-linearized Volterra operator (mathcal L_{hat x});
- (A=B) = bounded approximate inverse constructed from the lower-triangular discretization plus an analytically controlled infinite/off-grid remainder.

Then:
[
Y_0=|Bmathcal F(hat x)|,
]
[
Z_0=|I-B A^dagger|,
]
and if (A^dagger=Dmathcal F(hat x)) exactly, one can set (Z_1=0).

The nonlinear remainder supplies (Z_2(r)).

### Critical correction to CANDIDATE-V1

The current simplified statement
[
Y+Z_1r+Z_2(r)<r
]
is valid as a contraction criterion **only if** the preconditioning operator (B) is injective (or an equivalent condition ensuring a fixed point of (x-Bmathcal F(x)) is genuinely a zero of (mathcal F)).

The safe manuscript form is the published radii-polynomial theorem above, with:
- explicit injectivity of (B); or
- (Z_0<1) plus a structural argument proving injectivity, as standard in radii-polynomial implementations.

This is a **minor theorem-statement fix**, not an obstruction.

## 6. Closest practical CAP template

**Breden & Lessard (2018).**  
“Polynomial interpolation and a priori bootstrap for computer-assisted proofs in nonlinear ODEs.”  
*Discrete and Continuous Dynamical Systems - B* 23(7), 2825–2858.  
DOI **10.3934/dcdsb.2018164**.

They:
- use piecewise polynomial interpolation;
- formulate the IVP as a fixed-point/zero problem;
- build a Newton-like approximate inverse;
- rigorously validate with radii polynomials;
- show dramatic gains when higher polynomial degree is used.

This is ODE rather than fractional Volterra, but methodologically it is extremely close to the proposed Stage I/II strategy.

### Q2 verdict

[
oxed{	ext{ORBIT-LINEARIZED APPROXIMATE-INVERSE ROUTE SUPPORTED}}
]

This is the **recommended primary route**.

---

# Q3 — Nonautonomous weakly singular Volterra resolvent

## 7. Exact linearized error equation

The project needs to retain
[
A(s)=Dg(hat x(s))
]
rather than replace it by an absolute scalar amplification.

The linear equation is
[
e(t)
=
f(t)
+
int_0^t
B(t,s)e(s),ds,
]
with
[
B(t,s)
=
rac{(t-s)^{alpha-1}}{Gamma(alpha)}A(s).
]

This is a nonconvolution, weakly singular **matrix Volterra kernel**.

## 8. Becker 2011 directly supplies the resolvent theory

**Leigh C. Becker.**  
“Resolvents and solutions of weakly singular linear Volterra integral equations.”  
*Nonlinear Analysis: Theory, Methods & Applications* 74(5), 1892–1912 (2011).  
DOI **10.1016/j.na.2010.10.060**.

The paper treats weakly singular matrix kernels (B(t,s)), proves existence/structure of the two-variable resolvent (R(t,s)), and derives the variation-of-parameters formula
[
e(t)
=
f(t)+
int_0^t R(t,s)f(s),ds.
]

The paper explicitly includes nonconvolution/nonseparable weakly singular kernels.

Therefore the orbit-linearized kernel
[
B(t,s)=k_alpha(t-s)A(s)
]
falls in exactly the right theoretical category on every finite interval, assuming (A) is continuous—which holds for a continuous numerical orbit approximation and polynomial (g).

## 9. Computational implication

The exact inverse of
[
mathcal L_{hat x}
=
I-I^alpha A(cdot)
]
can be represented by this two-variable resolvent.

But the project does **not** need a closed formula for (R(t,s)).

A practical approximate-inverse CAP may instead:

1. discretize (mathcal L_{hat x}) in a piecewise polynomial basis;
2. invert the finite lower-block-triangular matrix numerically;
3. interval-enclose the finite inverse/action;
4. prove the continuous off-grid/remainder operator is small;
5. validate the total inverse defect (Z_0).

This retains sign and rotation automatically. The general radii theorem only cares about the rigorous operator bounds.

### Q3 verdict

**NONAUTONOMOUS ORBIT RESOLVENT: PUBLISHED THEORY EXISTS AND DIRECTLY SUPPORTS THE STRATEGY.**

No published ready-made interval implementation for this exact weakly singular matrix kernel was located.

---

# Q4 — Fractional initial singularity and preservation of high order

## 10. The issue is real

For (0<alpha<1), even smooth autonomous Caputo equations generally produce a (t^alpha)-type initial layer. Uniform high-order polynomial schemes can suffer order reduction.

## 11. Published routes that do not assume classical smoothness at (t=0)

### Graded piecewise polynomial collocation

Brunner–Pedas–Vainikko 1999 and Liang–Brunner 2019 provide the classical weakly singular Volterra foundation.

On meshes
[
t_n=T(n/N)^q
]
with sufficiently strong grading, optimal polynomial convergence can be recovered despite endpoint singularity.

### Fractional-power / Müntz basis

“A multi-domain spectral collocation method for Volterra integral equations with a weakly singular kernel.”  
*Applied Numerical Mathematics* 167 (2021), 218–236.  
DOI **10.1016/j.apnum.2021.05.006**.

Uses Müntz-polynomial spaces plus graded meshes and proves hp-type rigorous error estimates. This is especially attractive for a (t^{kalpha})-type Caputo initial expansion.

### Caputo-specific graded high order

“A Fast High-Order Predictor–Corrector Method on Graded Meshes for Solving Fractional Differential Equations.”  
*Fractal and Fractional* 6 (2022), 516.  
DOI **10.3390/fractalfract6090516**.

Uses quadratic interpolation on graded meshes specifically for Caputo IVPs and analyzes the weak initial singularity.

### 2025 direct Caputo collocation

“Analysis and implementation of collocation methods for fractional differential equations.”  
*Journal of Scientific Computing* (2025).  
DOI **10.1007/s10915-025-03006-9**.

Explicitly discusses correction terms, smoothing transformations, and graded meshes as the three standard ways to avoid loss of order from the initial singularity.

## 12. Recommended representation for W1

For the computer-assisted proof, the safest design is:

**Initial panel:** either
- a strongly graded mesh; or preferably
- a short fractional-power/Müntz expansion (p+sum c_k t^{kalpha}) with rigorous remainder.

**Regular remainder of interval:** degree 2–5 piecewise polynomials on a much coarser mesh.

Why this is superior to simply increasing (N):
- it resolves the (t^alpha) layer analytically;
- it makes the residual genuinely high order;
- the orbit-linearized inverse—not a Grönwall factor—then handles propagation of that residual.

### Q4 verdict

**HIGH ORDER WITH INITIAL SINGULARITY IS WELL SUPPORTED.**

Do not assume (C^{p+1}) regularity at (t=0). State the graded/fractional-power approximation explicitly.

---

# Q5 — 2025–2026 validated/certified prior pressure

## 13. Closest direct Caputo paper: Salas et al. 2026

**Salas, Altamirano & Martínez (2026).**  
“An error-certified matrix Mittag–Leffler perturbation method for weakly nonlinear fractional systems.”  
*Frontiers in Applied Mathematics and Statistics* 12, 1899674.  
DOI **10.3389/fams.2026.1899674**.

Already audited in ROUND-0005.

It provides:
- exact matrix Mittag-Leffler propagation;
- perturbative nonlinear corrections;
- explicit truncation bounds;
- a posteriori residual-to-solution estimates;
- removal of the endpoint singularity by a power substitution.

This is the strongest current direct novelty pressure on “certified numerical Caputo solutions.”

### Important distinction

The paper's “error-certified” estimates are analytic residual/error bounds. It is not an interval-arithmetic computer-assisted proof of a long nonlinear excursion with all roundoff/discretization uncertainties enclosed, and it does not invert the time-dependent orbit-linearized operator.

## 14. Current 2026 Volterra a-posteriori work

Baccouch 2026 gives rigorous asymptotically exact residual estimators for nonlinear Volterra integro-differential equations, but for smooth-kernel first-order VIDEs rather than the singular Caputo integral equation.

Current 2026 weakly singular collocation papers prove convergence/error estimates, but the search did not identify one that performs a full interval/radii-polynomial enclosure of a nonlinear Caputo IVP.

## 15. Older interval-enclosure prior

**Yazdani & Hadizadeh (2012).**  
“Piecewise constant bounds for the solution of nonlinear Volterra-Fredholm integral equations.”  
*Computational & Applied Mathematics* 31(2), 305–322.  
DOI **10.1590/S1807-03022012000200005**.

This is genuine validated numerics:
- interval enclosures guaranteed to contain the exact solution;
- roundoff and truncation errors included.

It is not tailored to the Caputo weakly singular kernel and does not use orbit-linearized approximate inversion.

### Q5 verdict

No published 2025–2026 method was located that already supplies the exact proposed result:

> interval/radii-polynomial validation of a nonlinear Caputo IVP over a long excursion by approximately inverting the time-dependent weakly singular Volterra linearization.

Therefore the project must **not** claim validated numerics generically as new, but the exact validation architecture appears unsaturated in the searched corpus.

---

# 16. Exact theorem/source chain recommended for TASK-0005

## Route A — PRIMARY: orbit-linearized approximate inverse

### Step A1 — Banach-space zero problem
Work with
[
mathcal F(x)=x-p-I^alpha[g(x)]
]
in a Banach space (X) compatible with the piecewise representation and a sup/weighted norm.

Published basis:
- general Volterra well-posedness already in project bibliography;
- Breden–Lessard 2018 as CAP model.

### Step A2 — exact derivative
[
Dmathcal F(hat x)e
=
e-I^alpha[Dg(hat x(cdot))e].
]

No approximation here.

### Step A3 — approximate inverse
Construct (Bapprox Dmathcal F(hat x)^{-1}) from the lower-block-triangular collocation discretization.

The two-variable resolvent existence is supported by Becker 2011.

### Step A4 — radii bounds
Use Church et al. 2023, Theorem 1:
[
Y_0,quad Z_0,quad Z_1,quad Z_2(r).
]

For (A^dagger=Dmathcal F(hat x)), ideally (Z_1=0), leaving
[
p(r)=rZ_2(r)+(Z_0-1)r+Y_0<0.
]

All finite-dimensional matrix operations and coefficient bounds should be interval/ball arithmetic.

### Step A5 — injectivity
Explicitly verify the injectivity requirement for (B), or use a Neumann argument from a rigorous inverse-defect bound.

### Step A6 — consequence
The theorem returns a unique true Volterra solution in the validated ball around (hat x). This is the exact history enclosure needed to compute rigorous (M_T).

## Route B — SECONDARY: high-order residual construction

Use:
- fractional-power/Müntz initial panel or graded mesh;
- degree 2–5 piecewise polynomial approximation;
- exact/rigorous fractional polynomial moments;
- interval residual and interpolation remainders.

Published basis:
- Brunner–Pedas–Vainikko 1999;
- Liang–Brunner 2019;
- multi-domain Müntz collocation 2021;
- current 2025/2026 high-order product-integration/collocation literature.

Then feed this approximation into Route A.

## Do not use as the final proof core

Do not base the final certificate only on:
- a global fractional Grönwall constant;
- an asymptotically exact estimator with unknown/non-rigorous constants;
- mesh-refinement agreement;
- residual smallness without an inverse bound.

TASK-0004 has already empirically demonstrated why these can be useless on the target excursion.

---

# 17. Practical recommendation to Compute

Before building any high-order interval machinery, execute the Chief's Stage I test:

1. discretize (Dmathcal F(hat x)) along W1 with the existing fine numerical orbit;
2. solve/apply its lower-triangular inverse to localized defect vectors;
3. estimate the induced amplification in the intended coefficient/sup norm;
4. compare with the current (10^6)–(10^{16}) normwise amplification.

Decision:
- if the sign-aware discrete inverse is (O(1))–(O(10^2)), proceed immediately to V1/radii implementation;
- if it remains (gg10^4), test a goal-oriented functional inverse for (M_T) before investing in full uniform validation.

The literature audit strongly supports this ordering.

---

# 18. Final novelty boundary

Not new:
- high-order collocation for weakly singular Volterra equations;
- graded meshes / fractional-power treatment of the initial layer;
- residual-based a-posteriori Volterra estimation;
- Newton–Kantorovich / radii-polynomial CAP;
- two-variable resolvents for nonautonomous weakly singular Volterra equations;
- error-certified Caputo propagation.

Potentially residual:
- adapting an orbit-linearized approximate-inverse CAP to a long nonlinear Caputo excursion specifically to certify the inherited memory needed for a same-present-state / opposite-basin theorem.

The paper should treat the validation method as enabling machinery unless the final implementation itself develops a mathematically distinct theorem beyond the standard radii-polynomial framework.
