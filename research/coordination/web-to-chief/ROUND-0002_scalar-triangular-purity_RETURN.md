# ROUND-0002 — RETURN TO CHIEF

**Round ID:** ROUND-0002  
**Request:** `research/coordination/chief-to-web/ROUND-0002_scalar-triangular-purity_REQUEST.md`  
**Search date:** 2026-09-29  
**Agent:** Deep Web Search Agent  
**Final substantive evidence commit before this return:** `bdcaff493193c30933008731fb2569c3329415d9`

## Required verdicts

- **S1 imported nonintersection hypotheses:** **NEEDS FIX**
- **S1 novelty status:** **STANDARD CONSEQUENCE**
- **Scalar strong-Allee instantiation:** **FOUND RIGOROUSLY**
- **Triangular extension:** **USEFUL COMPLETENESS**
- **Monotone extension:** **EXTRA CONDITIONS REQUIRED**

## 1. Scalar nonintersection audit

### Load-bearing source

Use:

**Cong, N. D.; Tuan, H. T. (2017).**  
“Generation of Nonlocal Fractional Dynamical Systems by Fractional Differential Equations.”  
*Journal of Integral Equations and Applications* 29(4), 585–608.  
DOI: `10.1216/JIE-2017-29-4-585`.

For
[
{}^C D_{0+}^{\alpha}x=f(t,x),qquad 0<\alpha<1,
]
on (J=[0,T]) or (J=[0,\infty)), Section 3.1 assumes (f) continuous and
[
|f(t,x)-f(t,y)|\le L(t)|x-y|
]
for all (x,y\in\mathbb R), with continuous (L(t)\ge0).

**Theorem 4** (“Different trajectories do not meet”; author/full-text manuscript p. 6) proves that distinct initial values generate trajectories that never meet on (J). Its proof is stronger:
[
x_1(0)<x_2(0)
\Longrightarrow
x_1(t)<x_2(t)
\quad\forall t\in J.
]

Therefore an autonomous equilibrium (c), (g(c)=0), is a strict barrier:
[
x_0<c\Rightarrow x(t)<c,qquad
x_0>c\Rightarrow x(t)>c.
]

At (x_0=c), uniqueness gives the stationary solution.

### Required fix to S1 sourcing

The Chief's abstract S1 hypothesis is fine. The fix is only in how it is imported:

> Cong–Tuan's theorem requires the stated global-in-state Lipschitz condition (or a separately justified reduction/local extension). It should not be cited as automatically covering an arbitrary (C^1) scalar (g).

This matters for cubic Allee vector fields, which are not globally Lipschitz on all of (mathbb R).

### Diethelm–Ford warning

Diethelm & Ford (2012), DOI `10.1216/JIE-2012-24-1-25`, may remain historical background, but should **not** be the load-bearing separation proof.

Cong–Tuan explicitly explain that Diethelm–Ford Theorem 3.1 has an incomplete backward-induction/terminal-value argument caused by the nonlocal memory dependence, and hence their Theorem 4.1 is also incomplete.

## 2. S1 novelty audit

A stronger scalar asymptotic source is already published:

**Doan, T. S.; Kloeden, P. E. (2022).**  
“Attractors of Caputo Fractional Differential Equations with Triangular Vector Fields.”  
*Fractional Calculus and Applied Analysis* 25(2), 720–734.  
DOI: `10.1007/s13540-022-00030-6`.

For
[
{}^C D_{0+}^{\alpha}x=g(x),
]
they assume:

1. (g\in C^1(\mathbb R));
2. dissipativity:
   [
   xg(x)\le a-bx^2;
   ]
3. every equilibrium is simple:
   [
   g'(c)\ne0quad	ext{when }g(c)=0.
   ]

**Theorem 2.2** gives the scalar global attractor and convergence of every solution to an equilibrium.

**Proposition 2.4** supplies the sharper equilibrium-interval classification: each interval between adjacent simple equilibria has a fixed asymptotic endpoint determined by the sign pattern.

That is essentially S1-H2 for this broad class.

No published paper was found using the exact Doan–Kloeden continuation-state notation
[
\mathcal F_x=e_0^{-1}(x)\cap\mathcal R_\alpha
]
to state fiber purity. But once separation/barriers, intervalwise asymptotics, and positive basin invariance are available, the fiber result is immediate.

### Chief disposition recommended

[
\boxed{\text{S1 = STANDARD CONSEQUENCE / COMPLETENESS RESULT}}
]

Do not promote it as principal novelty.

## 3. Rigorous strong-Allee instantiation

Clean model:

**Area, I.; Nieto, J. J. (2023).**  
“On the Fractional Allee Logistic Equation in the Caputo Sense.”  
*Examples and Counterexamples* 4, 100121.  
DOI: `10.1016/j.exco.2023.100121`.

Their published Caputo model is
[
{}^C D_{0+}^{\alpha}x=x(1-x)(x-\theta),
qquad
0<\theta<1.
]

Let
[
g(x)=x(1-x)(x-\theta).
]

Then:

- (g\in C^1);
- (xg(x)) has leading term (-x^4), hence satisfies the Doan–Kloeden dissipativity hypothesis;
- the zeros are (0,\theta,1);
- they are simple:
  [
  g'(0)=-\theta<0,quad
  g'(\theta)=\theta(1-\theta)>0,quad
  g'(1)=\theta-1<0.
  ]

Therefore Doan–Kloeden 2022 applies rigorously and yields, on the positive physical domain,
[
0<x_0<\theta
\Longrightarrow
x(t;x_0)\to0,
]
[
x_0>\theta
\Longrightarrow
x(t;x_0)\to1,
]
with (x_0=\theta) stationary.

Consequently the S1 fiber corollary is rigorous:
[
0<x<\theta
\Longrightarrow
\mathcal F_x\subseteq\mathcal B(0),
]
[
x>\theta
\Longrightarrow
\mathcal F_x\subseteq\mathcal B(1),
]
and
[
\mathcal F_\theta=\{\iota(\theta)\}.
]

**Important attribution:** Area–Nieto supplies the exact published Caputo model. The rigorous global threshold classification comes from applying the published Doan–Kloeden theorem; do not attribute that global theorem to Area–Nieto.

A second published Caputo Allee paper, Kalra & Malhotra 2024 (DOI `10.37256/cm.5120243183`), was checked. Its strong-Allee extinction/survival presentation depends materially on numerical simulations, so it is contextual only, not proof support.

## 4. Triangular extension

Two published layers exist.

### Cong–Tuan 2017

They prove nonintersection/nonlocal-dynamical-system results for triangular Caputo systems under their Lipschitz setup.

### Doan–Kloeden 2022

Their **Theorem 3.1** gives a global attractor/convergence theorem for a special product-triangular class
[
g_i(x_1,\ldots,x_i)
=
h_i(x_1,\ldots,x_{i-1})f_i(x_i),
]
under the stated smoothness, sign/nonvanishing and dissipativity conditions.

This substantially covers one natural triangular subclass.

### Exact Chief target

The Chief's safer P2 statement is broader in logical form:

> a closed scalar coordinate satisfies S1 and its equilibrium interval determines the full-system asymptotic basin.

Under that explicit basin-determining hypothesis, fiber purity is a valid corollary.

No source was found stating the exact reachable-fiber result, but the special product-triangular prior is strong enough that this should remain **completeness**, not principal novelty.

### Verdict

**USEFUL COMPLETENESS.**

General triangularity alone must not be claimed sufficient.

## 5. Monotone/comparison extension

Verified current published comparison sources:

- **Wu (2020)**, *Fractals* 28(4), 2050070, DOI `10.1142/S0218348X2050070X`;
- **Wu (2023)**, *Chaos, Solitons & Fractals* 171, 113437, DOI `10.1016/j.chaos.2023.113437`;
- **Cheng & Wu (2026)**, *Journal of Mathematical Analysis and Applications* 559(1), 130509, DOI `10.1016/j.jmaa.2026.130509`.

The 2023/2026 system theory provides comparison for quasi-monotone, mixed quasi-monotone/mixed-monotone classes and related variants.

These are ordered-solution theorems. They do **not** imply
[
e_0(\phi)=e_0(\psi)
\Longrightarrow
\omega(\phi)=\omega(\psi).
]

Two reachable memory states with the same endpoint need not be ordered as histories; even when histories are ordered, order preservation alone does not force the same omega-limit.

### Required extra structure

A genuine comparison-based fiber-purity theorem would need something like:

1. an endpoint-determining scalar/functional threshold;
2. invariant endpoint-defined regions whose members have one common basin label; or
3. an explicit factorization of basin label through the present observation:
   [
   \beta(\phi)=B(e_0(\phi))
   quad\text{on }\mathcal R_\alpha.
   ]

No published Caputo theorem of that exact type was identified.

### Verdict

**EXTRA CONDITIONS REQUIRED.**

## 6. Exact residual after ROUND-0002

The scalar route is effectively closed as a novelty source.

Published theory already supplies:

- strict scalar separation/barriers;
- scalar equilibrium-interval asymptotics;
- a rigorous Caputo strong-Allee model satisfying the general theorem.

The fiber-purity language is useful because it cleanly contrasts scalar impossibility with the desired multidimensional multibasin phenomenon, but it should be positioned as a completeness theorem/corollary.

The triangular route has value only with carefully stated extra hypotheses beyond generic triangularity.

The monotone route remains open only after specifying an endpoint-determining separator/functional; order preservation alone is insufficient.

## 7. Bibliography/reference changes

Updated:

- `bibliography/references.bib`
  - added Area & Nieto 2023;
  - added Wu 2023;
  - added Kalra & Malhotra 2024;
  - corrected Wu 2020 volume/issue/article metadata.
- `research/REFERENCES.md`
  - recorded Doan–Kloeden 2022 as the principal scalar/triangular asymptotic source;
  - added publication roles/warnings;
  - recorded Diethelm–Ford proof caveat.
- `research/LITERATURE_MAP.md`
  - integrated the scalar closure, strong-Allee corollary, triangular prior and comparison limitation.

All added citation-support sources are formally published.

## 8. Files produced/modified

- `research/web-search/2026-09-29_ROUND-0002_scalar-triangular-purity_REPORT.md`
- `research/coordination/web-to-chief/ROUND-0002_scalar-triangular-purity_RETURN.md`
- `bibliography/references.bib`
- `research/REFERENCES.md`
- `research/LITERATURE_MAP.md`

## 9. Negative-search limitations

No resolving published theorem was identified in the searched corpus that makes basin membership factor through (e_0) merely from monotonicity/order preservation.

This is not proof of absence. Older monotone-semiflow/Volterra literature may encode a related result under different terminology.

## 10. Recommended next search

Do not spend another broad round on scalar purity.

The next search should be triggered by either:

1. the Compute Agent returning the published Double-Allee baseline or a collision candidate — then audit that **exact model and parameter regime** (W-A004); or
2. the Chief writing an exact stronger triangular/monotone theorem — then hostile-search that precise statement.

Absent one of those triggers, the highest-value work remains the constructive multidimensional branch.
