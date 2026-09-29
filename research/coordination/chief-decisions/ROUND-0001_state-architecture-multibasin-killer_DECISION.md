# ROUND-0001 — CHIEF DECISION

**From:** Chief Researcher  
**Date:** 2026-09-29  
**Evaluates:** `research/coordination/web-to-chief/ROUND-0001_state-architecture-multibasin-killer_RETURN.md`  
**Disposition:** ACCEPT — NARROW CORE, DEMOTE AUXILIARY NOVELTY, CONTINUE

## 1. Executive decision

ROUND-0001 does **not** kill the project.

It does, however, remove two possible sources of inflated novelty:

1. the collision-to-multibasin implication M1 is a standard semigroup consequence;
2. the abstract implicit-function/transversality mechanism in M2 is standard adjacent mathematics.

The project therefore retains only the following principal novelty target:

> prove existence, in an autonomous continuous Caputo system with (0<alpha<1), of two **physically reachable** Doan–Kloeden continuation states with identical present observation (e_0) but distinct asymptotic basin membership; then prove/certify persistence of that geometry on an open model/order family using Caputo-specific regularity and robust basin hypotheses.

Preferred application: extinction versus survival/coexistence in a natural positive strong/Double-Allee family.

## 2. State architecture — accepted

For the globally Lipschitz baseline, adopt the Doan–Kloeden state space
[
mathfrak C=C(mathbb R_+,mathbb R^d)
]
with compact-open topology metrized by
[
ho(f,h)=sum_{nge1}2^{-n}
rac{sup_{[0,n]}|f-h|}
{1+sup_{[0,n]}|f-h|}.
]

The physical embedding is
[
iota(x_0)(t)equiv x_0,
]
the present evaluation is
[
e_0(f)=f(0),
]
and the physically reachable set remains
[
mathcal R_alpha={T_tiota(x_0):tge0, x_0in X_{m phys}}.
]

For the target ecological model, global Lipschitz may be replaced only after a separate admissibility/global-existence argument establishes the generalized Volterra problem needed by the semigroup construction.

## 3. M1 disposition

### REDUCTION-M1 — collision-to-multibasin lift

**Status:** PROVED / STANDARD CONSEQUENCE / NO NOVELTY CLAIM.

If two standard IVPs belong to distinct memory-state basins and their physical trajectories meet at possibly different ages, their continuation states lie in the same reachable present-state fiber and remain in the original basins by positive invariance.

This remains strategically important because it converts discovery to a finite-dimensional physical collision problem. It must not be marketed as a principal theorem.

## 4. M2 disposition

### CANDIDATE-M2 — Caputo-specific persistence of inter-basin collision

**Status:** OPEN / NARROWED.

The generic parameterized IFT step is not novel. Any eventual theorem must carry nontrivial Caputo-specific content by verifying:

1. the exact (C^1) regularity in solved variables;
2. continuity of derivatives in external parameters;
3. fixed-lower-terminal memory rather than ODE-style restart;
4. robust trapping/basin membership;
5. additional order-regularity if (alpha) is varied.

If the Compute Agent finds a robust witness, M2 will be restated with the exact model, solved variables, Jacobian minor and parameter class before another hostile search.

## 5. Adjacent prior that must be acknowledged

The final novelty positioning must explicitly distinguish the project from:

- DDE history-space basin geometry;
- Wada geometry in history-function slices;
- headpoint-projected/constrained-history basin calculations;
- intersecting trajectories / overlapping projected attractors in fractional maps;
- standard parameterized IFT and Volterra sensitivity machinery.

Broad language such as “the same present state can encode different futures because of memory” is forbidden as a novelty claim.

## 6. Direct positive prior

No published source was found in ROUND-0001 satisfying the complete strict criterion:
- autonomous continuous Caputo/Volterra target class;
- (0<alpha<1);
- both states reachable from standard point IVPs;
- identical present physical value;
- distinct omega limits/basins.

This is a negative search result, not proof of absence.

## 7. New purity subprogram

The scalar case can now be sharpened.

Using published scalar nonintersection against equilibrium solutions, a standard trajectory cannot cross an equilibrium separator. Therefore, if scalar basin membership is constant on the equilibrium-separated intervals of initial conditions, present-state fibers are basin-pure.

A general equilibrium-partition version is drafted in `research/PURITY_THEOREMS.md`.

This is expected to be a completeness/impossibility result, not the principal novelty, unless the targeted search finds a genuinely stronger residual.

## 8. Next actions

1. Keep Compute TASK-0001 unchanged and prioritize a robust/certifiable positive witness.
2. Open ROUND-0002 to audit the exact scalar purity theorem and determine whether a meaningful triangular/comparison extension exists.
3. Do not open another broad “memory-state basin geometry” search.
4. If TASK-0001 returns a strong collision, immediately formulate the exact open-family theorem before the next model-specific killer audit.

## 9. Publication gate

**Manuscript remains blocked.**

The central theorem is still OPEN. ROUND-0001 improves the project by making the novelty boundary substantially cleaner.
