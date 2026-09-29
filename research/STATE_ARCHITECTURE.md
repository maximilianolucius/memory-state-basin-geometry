# State Architecture and First Theorem Program

**Owner:** Chief Researcher  
**Date:** 2026-09-29  
**Status:** ACTIVE / PROVISIONAL PENDING PRIMARY-SOURCE HYPOTHESIS AUDIT

## 1. Governing Caputo IVP

Work initially with a commensurate autonomous Caputo system
[
{}^C D_{0+}^{\alpha}x(t)=g(x(t);\theta),\qquad 0<\alpha<1,
]
on a physical domain (X_{\rm phys}\subseteq\mathbb R^d), with standard point initial data (x(0)=x_0).

The equivalent Volterra form is
[
x(t)=x_0+\frac1{\Gamma(\alpha)}
\int_0^t (t-s)^{\alpha-1}g(x(s);\theta)\,ds.
]

Exact regularity, existence, uniqueness, continuation and parameter-dependence hypotheses will be imported only after primary-source audit. No ODE semiflow assumption is permitted on (X_{\rm phys}).

## 2. Memory-state architecture

Let (mathcal H_\alpha) denote the function/history state space on which the audited Caputo/Volterra continuation operator defines a semidynamical system (T_t). Let
[
\iota:X_{\rm phys}\to\mathcal H_\alpha
]
be the canonical embedding of a standard physical IVP and
[
e_0:\mathcal H_\alpha\to X_{\rm phys}
]
the present-state evaluation map.

The physically reachable memory-state set is
[
\mathcal R_\alpha
=
\{T_t\iota(x_0):t\ge0,\ x_0\in X_{\rm phys}\}.
]

For (x\in X_{\rm phys}), define the reachable present-state fiber
[
\mathcal F_x=e_0^{-1}(x)\cap\mathcal R_\alpha.
]

### Closure policy

The principal existence/nonexistence statements should be made on (mathcal R_\alpha), not on arbitrary ambient histories.

The closure (overline{\mathcal R_\alpha}) may be introduced only when a theorem genuinely requires topological closure (for example, compactness, stable-manifold arguments, or attractor theory). Any theorem proved only on the closure must separately state whether its witnesses are actually reachable.

## 3. Basin definition

Let (A\subset\mathcal H_\alpha) be an invariant asymptotic state/attractor for the memory-state semidynamical system. Define
[
\mathcal B(A)
=
\{\phi\in\mathcal H_\alpha:
\operatorname{dist}(T_t\phi,A)\to0\text{ as }t\to\infty\},
]
subject to the exact topology/metric fixed by the source audit.

For a physical equilibrium (a\in X_{\rm phys}) with (g(a)=0), the associated memory-state equilibrium is expected to be the canonical stationary lift; this identification must be checked against the chosen representation.

A reachable fiber is **basin-pure** relative to a specified attractor family if all of its basin-classified members belong to one basin. It is **multibasin** if it contains members of at least two distinct basins.

## 4. Key reduction: inter-basin physical collision

Define the present observation of a standard IVP at age (t):
[
P_{\alpha,\theta}(x_0,t)
=
e_0(T_t\iota(x_0))
=
x(t;x_0,\alpha,\theta).
]

### CANDIDATE STRUCTURAL LEMMA M1 — collision-to-multibasin lift

Assume (iota(p)\in\mathcal B(A_1)) and (iota(q)\in\mathcal B(A_2)) with (A_1\neq A_2). If there exist (t,s\ge0) such that
[
P(p,t)=P(q,s)=x,
]
then
[
T_t\iota(p),\ T_s\iota(q)\in\mathcal F_x
]
and, by forward invariance of basins,
[
T_t\iota(p)\in\mathcal B(A_1),\qquad
T_s\iota(q)\in\mathcal B(A_2).
]
Hence (mathcal F_x) is multibasin.

**Evidence status:** analytic reduction / proof sketch complete, but not promoted until the exact semidynamical/basin hypotheses are audited.

**Importance:** this converts the constructive problem from an infinite-dimensional history search into a finite-dimensional search for a physical-state collision between trajectories whose lifted initial states have different asymptotic outcomes.

## 5. Candidate robustness theorem

Let
[
H(p,q,t,s;\mu)
=
P_\mu(p,t)-P_\mu(q,s),
]
where (mu) collects model parameters and fractional order(s).

### CANDIDATE STRUCTURAL THEOREM M2 — transversal collision persistence

At a base point ((p_*,q_*,t_*,s_*;\mu_*)), suppose:

1. (H=0);
2. the two lifted initial states lie in distinct basins with robust trapping neighborhoods;
3. a (d\times d) minor of the derivative of (H) with respect to selected free variables is nonsingular;
4. the Caputo solution map has the differentiability/parameter-continuity required by the implicit-function theorem.

Then the inter-basin collision, and therefore a multibasin reachable fiber, persists for parameters (mu) in a neighborhood of (mu_*).

**Status:** OPEN / candidate theorem. Hypotheses 3–4 and the correct Banach/finite-dimensional formulation require source and proof audit.

**Publication value if valid:** turns one certified collision into an open-family result and prevents benchmark-only novelty.

## 6. Purity/impossibility program

### P0 — one global basin
If every reachable standard IVP converges to the same attractor, every reachable fiber is trivially basin-pure. This is completeness/background, not principal novelty.

### P1 — scalar strong-Allee barrier
Do **not** infer purity merely from same-time scalar nonintersection. Because (mathcal R_\alpha) contains states of different ages, equal present values can in principle arise at different times.

Instead target a barrier theorem: under scalar comparison/separation hypotheses, an unstable Allee equilibrium (a_u) separates extinction and survival outcomes, and the sign of (x-a_u) cannot change along a standard IVP. Then basin label is determined by the current scalar state and every reachable present-state fiber away from the separator is pure.

**Status:** OPEN pending exact comparison theorem audit.

### P2 — triangular observable-determining coordinate
For triangular systems, seek hypotheses under which one scalar coordinate obeys a closed threshold equation and determines the asymptotic basin of the full system. If that coordinate is a basin-complete observable, same-present fibers are pure.

**Status:** OPEN; general triangularity alone is not asserted to suffice.

### P3 — monotone/comparison-dominated classes
Do not claim that order preservation alone implies fiber purity: two histories with the same endpoint need not be ordered in memory state. Search for extra hypotheses that make basin membership a function of an order interval, threshold functional, or endpoint-determined invariant region.

**Status:** OPEN / hostile literature audit required.

## 7. Constructive target

The preferred positive example is a natural nontriangular fractional strong/Double-Allee model with:

- a rigorously identified extinction attractor;
- a rigorously identified survival/coexistence attractor;
- standard physical IVPs in both basins;
- an inter-basin physical collision (P(p,t)=P(q,s));
- a transversality condition suitable for M2;
- positivity and global continuation proved independently of the collision search.

A numerical near-collision is only a conjecture generator. Basin labels must ultimately be supported by analytic trapping, exact inequalities, or rigorous certification.

## 8. Immediate gates

Before promoting M1/M2/P1/P2/P3:

1. verify the exact Doan–Kloeden state space, topology, continuation operator and canonical embedding;
2. verify basin forward-invariance assumptions in that setting;
3. hostile-search M1/M2 language and synonyms in Volterra/hereditary/factor/observation theory;
4. verify scalar and monotone comparison hypotheses from primary published sources;
5. independently reproduce the numerical infrastructure before any discovery claim.

## 9. Current Chief assessment

The most promising route is not “find two exotic histories.” It is:

> find two ordinary standard physical IVPs in distinct robust basins whose physical trajectories collide, then lift that collision to the reachable memory state and prove persistence by transversality.

This route is finite-dimensional at the discovery layer, physically reachable by construction, and has a plausible path from one example to an open-family theorem.
