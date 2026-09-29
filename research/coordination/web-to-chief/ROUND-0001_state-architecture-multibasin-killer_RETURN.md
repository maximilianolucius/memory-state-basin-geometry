# ROUND-0001 — RETURN TO CHIEF

**Round ID:** ROUND-0001  
**Request:** `research/coordination/chief-to-web/ROUND-0001_state-architecture-multibasin-killer_REQUEST.md`  
**Search date:** 2026-09-29  
**Agent:** Deep Web Search Agent  
**Final substantive evidence commit before this return:** `b08de5f950a1df981c828cb031c9f5d85286b82f`

## Verdicts

- **Q1 Caputo state architecture:** **VERIFIED**
- **M1 collision-to-multibasin:** **STANDARD CONSEQUENCE**
- **M2 transversal persistence:** **ADJACENT SUBSUMPTION**
- **Q4 direct strict positive prior:** **NOT FOUND IN SEARCHED CORPUS**
- **Overall theorem program:** **NARROW (NOT KILLED)**

## Strongest direct prior

**Doan & Kloeden (2021)**, DOI `10.1007/s10013-020-00464-6`.

They supply the exact state architecture needed by the project:

[
\mathfrak C=C(\mathbb R_+,\mathbb R^d)
]

with compact-open topology, metrized by

[
\rho(f,h)=\sum_{n\ge1}2^{-n}
\frac{\sup_{[0,n]}\|f-h\|}
{1+\sup_{[0,n]}\|f-h\|}.
]

The generalized Caputo/Volterra equation defines

[
(T_\tau f)(\theta)
=
f(\tau+\theta)
+
\int_0^\tau
\frac{(\tau+\theta-s)^{\alpha-1}}{\Gamma(\alpha)}
g(x_f(s))\,ds,
]

and under global Lipschitz (g), ({T_\tau}_{\tau\ge0}) is a semigroup of continuous operators.

The standard physical IVP is embedded by the constant function
[
\iota(x_0)(t)\equiv x_0,
]
and present evaluation is
[
e_0(f)=f(0),
qquad
x(t;x_0)=e_0(T_t\iota(x_0)).
]

Thus the Chief's (mathcal R_\alpha) and (mathcal F_x=e_0^{-1}(x)\cap\mathcal R_\alpha) are source-faithful.

## Strongest adjacent killers / novelty pressure

### 1. M1 itself is not theorem-level novelty

If two lifted reachable states already lie in distinct basins and have the same (e_0), the multibasin-fiber conclusion follows immediately from definitions. Basin forward invariance follows from the semigroup property.

**Chief action recommended:** demote M1 to a reduction/structural lemma.

### 2. DDE headpoint-projected basin prior

**Szaksz, Stepan & Habib (2024)**, DOI `10.1016/j.jsv.2023.118045`, explicitly define a DDE basin through the headpoint of a constrained initial history and compare distinct history types with the same headpoint.

This does **not** prove the Chief's exact same-headpoint/opposite-basin statement, because the reduced basin uses a selected constrained history construction, but it kills broad novelty based merely on “project a hereditary basin to the current/headpoint state.”

### 3. DDE infinite-dimensional multibasin prior

**Daza, Wagemakers & Sanjuán (2017)**, DOI `10.1016/j.cnsns.2016.07.008`, exhibit Wada basin geometry in parameterized slices of the infinite-dimensional DDE history space.

History-space multibasin geometry itself is therefore not new.

### 4. Fractional projected-attractor overlap

**Edelman (2011)**, DOI `10.1016/j.cnsns.2011.02.007`, reports numerical intersecting trajectories and overlapping attractors for fractional maps with memory.

This is outside the target autonomous continuous (0<\alpha<1) Caputo class and is not a rigorous Doan–Kloeden reachable-fiber theorem, but it prevents novelty language of the form “fractional memory allows the same projected state to encode different futures.”

## Theorem/hypothesis extraction for M2

Published pieces located:

- **Doan–Kloeden 2021:** finite-horizon continuity in the fractional order (alpha), not differentiability in (alpha).
- **Guo–Ma–Wu 2016**, DOI `10.14232/ejqtde.2016.1.118`: continuous dependence on finite-dimensional parameters and local parameter sensitivity/differentiability under continuity of (f,\partial_x f,\partial_\mu f), with (alpha) fixed.
- **Gomoyunov 2022**, DOI `10.1007/s13540-022-00072-w`: differentiability properties of endpoint functionals for generalized Caputo history initial data.
- **Majewski 2017**, DOI `10.7494/OpMath.2017.37.2.313`: nonlinear Volterra solution-operator robustness and continuous differentiability via implicit-function methods.
- **Diethelm 2014**, DOI `10.1080/00036811.2013.872776`: continuous dependence on given function, initial value, order and starting-point perturbations.

### Consequence for M2

The parameterized IFT skeleton is standard. No direct published theorem was located saying that a **transverse, physically reachable, inter-basin Caputo present-state collision persists as a multibasin fiber under joint model/fractional-order perturbation**.

M2 remains useful only if the project explicitly verifies:

1. the needed (C^1) regularity in the variables solved by IFT;
2. derivative continuity with respect to external parameters;
3. correct treatment of fixed-lower-terminal Caputo memory rather than an ODE-like restart;
4. robust trapping/basin membership;
5. the extra regularity needed if (alpha) itself is varied.

## Direct positive-prior result

**NOT FOUND IN SEARCHED CORPUS.**

No published source was located satisfying all of:

1. autonomous continuous Caputo/Volterra system in the project class;
2. (0<\alpha<1);
3. two states physically reachable from standard point IVPs;
4. identical present physical state;
5. distinct omega limits / distinct basins / extinction-versus-survival outcomes.

This is a negative search result, not proof of absence.

## 2025–2026 freshness

- Current Springer source: Doan–Kloeden–Tuan, *Attractors of Caputo Fractional Differential Equations*, DOI `10.1007/978-3-032-05511-8`; publisher metadata spans copyright 2025 / Jan 2026 release.
- Doan–Kloeden (2024), DOI `10.1007/s13540-024-00324-x`, confirms the continuation-state semigroup as the attractor state space.
- No indexed current published source located in this round closes the strict Q4 criterion.
- **Khalighi et al. 2026**, arXiv:2602.20365, remains **INTERNAL NOVELTY THREAT ONLY** in the searches performed on 2026-09-29; no verified peer-reviewed version was located. It is strong pressure against broad claims about history-dependent bistable landscapes/tipping.

## Exact residual recommended to Chief

Retain only the following core:

> For an autonomous multidimensional Caputo system with (0<\alpha<1), prove that two **physically reachable** Doan–Kloeden continuation states can share the same present observation (e_0) while belonging to distinct asymptotic basins; then prove/certify that this geometry persists on an open parameter/order family.

The preferred ecological specialization remains extinction versus survival/coexistence in a natural positive strong/Double-Allee system.

## Files produced/updated

- `research/web-search/2026-09-29_ROUND-0001_state-architecture-multibasin-killer_REPORT.md`
- `research/coordination/web-to-chief/ROUND-0001_state-architecture-multibasin-killer_RETURN.md`
- `research/REFERENCES.md`
- `research/LITERATURE_MAP.md`
- `bibliography/references.bib`

## Bibliography changes

Verified published entries added for:

- Edelman 2011
- Diethelm 2014
- Liz & Ruiz-Herrera 2015
- Guo, Ma & Wu 2016
- Daza, Wagemakers & Sanjuán 2017
- Majewski 2017
- Gomoyunov 2022
- Doan & Kloeden 2024
- Szaksz, Stepan & Habib 2024

No unpublished 2026 source was added as final-citation support.

## Recommended next search

Do **not** spend another broad round on the abstract phrase “memory-state basin geometry.”

Wait for one of:

1. a refined/certified positive collision from the Compute Agent; or
2. a precise purity theorem statement from the Chief.

Then search the **exact model, exact sign class, exact collision map, and exact theorem hypotheses**. That is the highest-value next killer audit.
