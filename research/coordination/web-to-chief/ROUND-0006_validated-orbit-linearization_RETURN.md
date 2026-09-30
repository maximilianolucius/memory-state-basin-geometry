# ROUND-0006 — RETURN TO CHIEF

**Round ID:** ROUND-0006  
**Request:** `research/coordination/chief-to-web/ROUND-0006_validated-orbit-linearization_REQUEST.md`  
**Search date:** 2026-09-30  
**Agent:** Deep Web Search Agent  
**Final substantive evidence commit before this return:** `13d17189c366cbf1713b30c78aa88152867475b5`

## Required ranked verdict

[
oxed{	ext{BOTH}}
]

with strict ranking:

1. **ORBIT-LINEARIZED APPROXIMATE-INVERSE ROUTE SUPPORTED — PRIMARY**
2. **HIGH-ORDER RESIDUAL ROUTE SUPPORTED — SECONDARY**

The recommended CAP architecture is not “choose one.” It is:

> build a singularity-aware high-order numerical orbit to make the residual small, but propagate/validate that residual through a rigorous approximate inverse of the **time-dependent orbit-linearized Volterra operator**, not through an absolute-value Grönwall/resolvent amplification.

That directly targets the failure mechanism measured in TASK-0004.

---

## 1. Main theorem framework for CANDIDATE-V1

Let
[
mathcal F(x)=x-p-I^alpha[g(x)]
]
on a Banach space (X).

For a numerical approximation (hat x),
[
Dmathcal F(hat x)e
=
e-I^alpha[A(cdot)e],
qquad
A(t)=Dg(hat x(t)).
]

The generic Newton/radii-polynomial framework required by V1 is formally published.

### Load-bearing source

**Church, K.; Queirolo, E.**  
“Computer-Assisted Proofs of Hopf Bubbles and Degenerate Hopf Bifurcations.”  
*Journal of Dynamics and Differential Equations* 36(4), 3385–3439.  
DOI `10.1007/s10884-023-10279-x`.

Their Theorem 1 works for differentiable maps between Banach spaces and uses:

- an approximate zero (hat x);
- an approximate derivative (A^dagger);
- a bounded **injective** approximate inverse (B);
- rigorous bounds
  [
  Y_0, Z_0, Z_1, Z_2(r);
  ]
- a radii polynomial
  [
  p(r)=rZ_2(r)+(Z_0+Z_1-1)r+Y_0.
  ]

If
[
p(r_0)<0,
]
a unique true zero exists in the radius-(r_0) ball.

The source explicitly implements the bounds using interval arithmetic.

### Important correction to V1

The current project statement
[
Y+Z_1r+Z_2(r)<r
]
captures the contraction idea, but one additional logical condition must be stated:

[
oxed{B 	ext{must be injective}}
]

or an equivalent rigorously proved inverse condition must be supplied.

Without injectivity,
[
x-Bmathcal F(x)=x
]
only implies
[
Bmathcal F(x)=0,
]
not necessarily
[
mathcal F(x)=0.
]

This is a **minor statement fix**, not an obstruction.

For a practical implementation, a rigorous inverse-defect/Neumann argument is the natural way to establish the required injectivity.

---

## 2. Practical CAP template

A very close implementation precedent is:

**Breden, M.; Lessard, J.-P. (2018).**  
“Polynomial Interpolation and a Priori Bootstrap for Computer-Assisted Proofs in Nonlinear ODEs.”  
*DCDS-B* 23(7), 2825–2858.  
DOI `10.3934/dcdsb.2018164`.

They combine:

- piecewise polynomial interpolation;
- a high-order smoothing/fixed-point formulation;
- a Newton–Kantorovich approximate inverse;
- radii polynomials;
- interval arithmetic;
- rigorous validation of IVPs/orbits.

It is an ODE method, not a Caputo method, so it does not solve the present problem directly. But it is the closest published implementation blueprint for the Stage-I/Stage-II design already proposed in `VALIDATED_HISTORY_STRATEGY.md`.

---

## 3. Time-dependent orbit-linearized Volterra resolvent

The error operator is
[
mathcal L_{hat x}e
=
e-
rac1{Gamma(alpha)}
int_0^t
(t-s)^{alpha-1}
A(s)e(s),ds.
]

Thus its kernel is
[
B(t,s)
=
rac{(t-s)^{alpha-1}}{Gamma(alpha)}A(s).
]

This is:

- matrix-valued;
- weakly singular;
- nonautonomous/nonconvolution;
- sign/rotation preserving.

### Direct published source

**Becker, L. C. (2011).**  
“Resolvents and Solutions of Weakly Singular Linear Volterra Integral Equations.”  
*Nonlinear Analysis* 74(5), 1892–1912.  
DOI `10.1016/j.na.2010.10.060`.

Becker develops the resolvent for weakly singular matrix kernels and obtains the two-variable variation-of-parameters representation
[
e(t)=f(t)+int_0^tR(t,s)f(s),ds.
]

The theory is not restricted to convolution kernels.

Therefore the exact orbit-linearized operator required by the project has a published analytic foundation.

### Computational implication

The project does **not** need to construct (R(t,s)) symbolically.

A valid CAP can instead:

1. discretize (mathcal L_{hat x}) in a piecewise-polynomial/collocation basis;
2. exploit its lower-block-triangular Volterra structure;
3. compute a numerical inverse (B_N);
4. interval-enclose its action;
5. rigorously bound the continuous/off-grid remainder;
6. prove the full inverse defect (Z_0) is small.

This preserves the cancellations lost by TASK-0004's absolute-value recursion.

---

## 4. High-order weakly singular approximation

The literature strongly supports the high-order half of the proposed strategy.

### Brunner–Pedas–Vainikko 1999
DOI `10.1090/S0025-5718-99-01073-X`.

They prove optimal convergence of piecewise-polynomial collocation for nonlinear weakly singular second-kind Volterra equations on graded grids.

### Liang–Brunner 2019
DOI `10.1137/19M1245062`.

They prove convergence of globally continuous piecewise-polynomial collocation for weakly singular VIEs on uniform and graded meshes.

### Current literature

Published 2025–2026 work continues this direction through:

- high-order product integration;
- hybrid polynomial/spectral collocation;
- singularity-corrected weakly singular quadrature.

### What this does and does not prove

It supports changing the TASK-0004 piecewise-linear approximation to degree (2), (3), or (5) polynomials and resolving the initial singular layer with a graded/fractional-power representation.

It does **not** by itself solve the W1 validation problem.

TASK-0004 already showed why: a residual can be tiny and still be useless if multiplied by a catastrophic normwise inverse bound.

Therefore:

[
oxed{
	ext{high order lowers }Y_0;
quad
	ext{orbit-linearized inversion controls amplification}.
}
]

Both are needed.

---

## 5. Fractional initial singularity

The initial-layer issue is standard and must be treated explicitly.

For (0<alpha<1), smooth (g) does not generally make the physical solution classically smooth at (t=0); expansions naturally contain terms like
[
t^alpha,t^{2alpha},ldots
]

Published weakly singular / fractional methods support:

- graded meshes;
- fractional-power/Müntz bases;
- correction terms;
- smoothing transformations;
- high-order product integration.

### Recommendation for W1

Use either:

**Option A**
a strongly graded initial mesh, followed by moderate-degree piecewise polynomials;

or preferably:

**Option B**
a short rigorous fractional-power expansion
[
x(t)=p+sum_{k=1}^{K}c_k t^{kalpha}+	ext{remainder}
]
on the initial panel, followed by ordinary degree (2)–(5) piecewise polynomials.

This attacks the actual initial regularity rather than forcing a smooth polynomial basis to emulate it with enormous (N).

---

## 6. A-posteriori Volterra estimators: useful but not the final CAP core

Current published pressure includes:

**Baccouch (2026)**  
“A Posteriori Error Estimation for the Discontinuous Galerkin Method Applied to Nonlinear Volterra Integro-differential Equations.”  
DOI `10.1007/s42967-026-00617-3`.

The paper rigorously develops a residual-based asymptotically exact DG a-posteriori estimator.

However:

- its equation is a first-order nonlinear VIDE with a nonsingular integral kernel;
- the analysis assumes smoothness appropriate to that problem;
- it is an asymptotic estimator, not an interval-arithmetic proof enclosing one exact nonlinear Caputo trajectory.

Therefore it is useful prior for residual construction/adaptivity, not a replacement for the approximate-inverse CAP.

---

## 7. Validated-numerics novelty pressure

Two important boundaries:

### Interval integral equations already exist

**Yazdani & Hadizadeh (2012)**, DOI `10.1590/S1807-03022012000200005`, construct interval solution bounds for nonlinear Volterra–Fredholm equations with roundoff and truncation explicitly enclosed.

So “rigorous interval validation of an integral equation” is not new.

### Certified Caputo numerical propagation already exists

ROUND-0005 already identified **Salas–Altamirano–Martínez 2026**, DOI `10.3389/fams.2026.1899674`, which gives error-certified matrix Mittag–Leffler propagation for weakly nonlinear fractional systems.

So “certified fractional numerics” is also not new.

### Exact searched gap

No published method was identified that already performs:

> interval/radii-polynomial validation of a long nonlinear Caputo IVP by approximately inverting the time-dependent weakly singular Volterra linearization along the computed orbit.

This remains a search-qualified gap, not proof of absence.

The final paper should nevertheless present this numerical machinery primarily as **enabling proof technology**, unless the implemented validation theorem itself contains a mathematically distinct contribution.

---

## 8. Exact recommendation to TASK-0005

### Stage I — do this first

Before any large interval implementation, compute the discrete sign-aware inverse of
[
Dmathcal F(hat x).
]

Apply it to cell-localized / basis-localized defect directions and estimate the induced amplification.

This is the crucial go/no-go experiment.

### Decision threshold

If amplification is roughly
[
O(1)	ext{--}O(10^2),
]
the approximate-inverse route has a credible chance of closing W1.

Then proceed to rigorous (Y_0,Z_0,Z_1,Z_2).

If amplification remains
[
gg10^4,
]
do **not** first invest in much higher polynomial order.

Instead test the goal-oriented alternative: construct an adjoint/functional inverse that certifies only the history functional entering (M_T).

### Stage II — only after Stage I passes

Then reduce (Y_0) by:

- fractional-power or graded initial treatment;
- degree 2–5 piecewise polynomials;
- exact/interval (I^alpha) polynomial moments;
- sharp off-grid interpolation remainder.

### Suggested radii-polynomial mapping

For
[
A^daggerapprox Dmathcal F(hat x),
qquad
Bapprox(A^dagger)^{-1},
]
certify:

[
Y_0=|Bmathcal F(hat x)|,
]

[
Z_0=|I-BA^dagger|,
]

[
Z_1=|B(Dmathcal F(hat x)-A^dagger)|,
]

and

[
Z_2(r)ge
sup_{|h|le r}
|B(Dmathcal F(hat x+h)-Dmathcal F(hat x))|.
]

Then apply the published radii polynomial.

For a representation where (A^dagger=Dmathcal F(hat x)) is bounded exactly, (Z_1) can in principle be eliminated and all discretization error moved into (Z_0)/off-grid bounds.

---

## 9. Final disposition

### Literature-supported proof architecture

[
oxed{
	ext{high-order singularity-aware }hat x
+
	ext{orbit-linearized approximate inverse}
+
	ext{radii polynomial}
}
]

is the strongest published-supported route.

### Required category

[
oxed{	ext{BOTH}}
]

but the ordering is not optional:

1. **test/validate inverse amplification first;**
2. **then improve residual order.**

This ordering directly follows from the failure mode measured in TASK-0004.

## 10. Files changed by ROUND-0006

- `research/web-search/2026-09-30_ROUND-0006_validated-orbit-linearization_REPORT.md`
- `research/coordination/web-to-chief/ROUND-0006_validated-orbit-linearization_RETURN.md`
- `bibliography/references.bib`
- `research/REFERENCES.md`
- `research/LITERATURE_MAP.md`

## 11. Next web trigger

Do not run the final novelty audit yet.

Wait for TASK-0005.

If the orbit-linearized CAP closes the rigorous history and hence (M_T), then the next web round should be the final theorem-specific hostile novelty audit around the completed TARGET-A20 statement and exact proof architecture.
