# ROUND-0017 — CHIEF DECISION

**From:** CHIEF RESEARCHER  
**Date:** 2026-09-28  
**Evaluates:** `research/coordination/web-to-chief/ROUND-0017_shortlist-final-killer-audit_RETURN.md`  
**Disposition:** ACCEPT — GAP-DISCOVERY PHASE COMPLETE

## 1. Final outcome

The final killer audit leaves one candidate that survives in a clean, genuinely theorem-level form and two candidates that survive only after substantial reformulation.

### PRIMARY RECOMMENDATION

> **Deterministic reachable memory-state basin geometry in positive multidimensional Caputo systems, with a preferred realization in strong/Double-Allee dynamics.**

Core question:

[
mathcal F_x
=
e_0^{-1}(x)capmathcal R_alpha.
]

Can one physically reachable current-state fiber satisfy

[
mathcal F_xcapmathcal B(A_{m ext})
eqarnothing,
qquad
mathcal F_xcapmathcal B(A_{m surv})
eqarnothing?
]

Equivalently:

> can the same currently observed population vector correspond to different asymptotic outcomes solely because the reachable Caputo memory state differs?

This is the strongest research opportunity identified by the project.

## 2. Why Family A is recommended

### 2.1 Novelty boundary is clean

Direct prior already establishes:
- finite-terminal Caputo dynamics is non-Markovian in the physical state;
- in (dge2), distinct solution trajectories can meet in physical state;
- history-state/Volterra representations exist;
- hereditary systems have genuine history-space basin geometry;
- fractional Double-Allee models with multistability and basin diagrams already exist.

But no searched theorem resolves the specific **reachable-fiber basin organization**:

[
e_0^{-1}(x)capmathcal R_alpha
]

across distinct asymptotic basins.

That residual survived repeated hostile searches through:
- Volterra systems;
- hereditary systems;
- delay equations;
- factor maps;
- partial observation;
- output equivalence;
- stable-set fibers;
- monotone/competitive Caputo systems.

### 2.2 Fractional structure is essential

The candidate is not an ODE theorem with (D^alpha) inserted.

Its core object exists because current physical state is not a sufficient Markov state for multidimensional Caputo dynamics.

The question disappears in an ordinary autonomous finite-dimensional ODE, where current state uniquely determines the future.

### 2.3 Double Allee is direct rather than decorative

Mondal et al. 2025, DOI `10.1016/j.cjph.2025.09.020`, provides a natural positive fractional predator–prey realization containing:
- Double Allee effect;
- strong-Allee extinction;
- alternative asymptotic states;
- multistability;
- basin calculations;
- incommensurate orders.

The proposed mathematical question is therefore naturally exposed by an existing Double-Allee system class rather than reverse-engineered into one.

### 2.4 The problem has theorem-family scale

The opportunity is not merely to find one counterexample.

A future theorem program could distinguish:

1. **impossibility classes**
   - scalar systems;
   - triangular systems;
   - selected monotone/comparison-dominated classes;

2. **existence classes**
   - sufficient conditions for multibasin fibers;

3. **fiber geometry**
   - topology;
   - regularity;
   - multiplicity;
   - local/global structure;

4. **fractional-order dependence**
   - how fiberwise basin intersections change with (alpha) or (oldsymbolalpha);

5. **observable sufficiency**
   - when current population is or is not sufficient to infer asymptotic fate;

6. **ecological specialization**
   - extinction versus persistence/coexistence in strong/Double-Allee systems.

This is plausibly large enough for a future high-level mathematical project if the first constructive/existence step succeeds.

## 3. Main risk of the recommended direction

The remaining technical risk is **constructive realizability**.

The literature audit shows a natural multistable Double-Allee class, but the project has not proved that this exact class contains a current-state fiber crossing two basins.

A future research project must first establish one of two outcomes:

- a natural positive class where multibasin fibers actually occur; or
- a structural theorem showing when they are impossible.

Either outcome can be mathematically valuable, but the first is preferable for the intended ecological interpretation.

This project does not perform that proof.

## 4. Secondary opportunity — Family B

### Reformulated title

> **Robust multibasin threshold geometry under parameter and fractional-order/kernel perturbations.**

The broad “robust fractional persistence” formulation is rejected.

Strong prior already exists for:
- robust persistence of semidynamical systems;
- robust persistence in delay/structured population models;
- viability and differential inclusions;
- discriminating kernels;
- robust invariant/capture sets.

The residual is narrower:

- persistence of the strong-Allee multibasin decomposition;
- sharp/common survival and extinction regions;
- separator enclosures;
- preservation/loss of bistability under ((	heta,alpha,	ext{kernel})) perturbations.

### Status

**SECONDARY OPPORTUNITY — DEFENSIBLE, BUT HIGHER SUBSUMPTION AND CONSERVATISM RISK.**

It becomes especially attractive if linked to Family A's memory-state basin geometry.

## 5. Tertiary/high-risk opportunity — Family C

### Reformulated title

> **Rare extinction and basin-exit theory for positive multistable stochastic fractional-memory systems.**

The broad stochastic-persistence formulation is rejected as primary novelty.

Strong prior already exists for:
- stochastic Volterra Markovian lifts;
- infinite-dimensional stochastic persistence;
- stochastic-delay quasipotential/exit theory;
- stochastic Volterra path LDP;
- long-memory regime switching.

The residual is the singular fractional-memory implementation:

- quasipotential/action on the appropriate memory lift;
- uniform-in-initial-memory exit theory;
- extinction-time asymptotics;
- most-likely extinction paths;
- dependence on (alpha);
- strong/Double-Allee basin geometry.

### Status

**HIGH-POTENTIAL / HIGH-NOVELTY-DECAY-RISK.**

The 2026 literature is moving quickly, so novelty could erode faster than for Family A.

## 6. Final project recommendation

The project should report the following opportunity as its principal discovery:

> **Observable insufficiency and basin ambiguity induced by fractional memory: characterize the physically reachable memory-state fibers associated with a fixed current population state, determine when such fibers are basin-pure or multibasin, and specialize the theory to extinction versus survival in positive strong/Double-Allee systems.**

A concise mathematical formulation is:

[
oxed{
	ext{Characterize }
mathcal F_x=e_0^{-1}(x)capmathcal R_alpha
	ext{ relative to the basin partition of the Caputo memory-state semiflow.}
}
]

The strongest biologically interpretable event is:

[
oxed{
exists phi,psiinmathcal F_x:
quad
omega(phi)=A_{m extinction},
qquad
omega(psi)=A_{m survival}.
}
]

## 7. Project boundary

The goal of this repository was:
- map the state of knowledge;
- identify frontiers;
- falsify candidate gaps;
- recommend fertile opportunities.

That task is now complete.

The following belong to a **new project**, not this one:
- constructing/proving the first multibasin-fiber theorem;
- selecting a concrete Double-Allee model for proof;
- numerical experiments designed to discover the theorem;
- writing a new original-research paper from the result.

A review/state-of-the-art paper based on the completed cartography remains an admissible continuation of this repository.

## 8. Final disposition

- **Family A:** RECOMMENDED PRIMARY RESEARCH OPPORTUNITY.
- **Family B:** RETAIN AS SECONDARY / POSSIBLE EXTENSION.
- **Family C:** RETAIN AS HIGH-RISK FUTURE OPPORTUNITY.
- **All other candidate branches:** survey/domain-map/supporting material only, or merged as previously recorded.

**Gap-discovery phase: COMPLETE.**
