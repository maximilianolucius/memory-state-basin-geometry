# TASK-0001 — Validated Caputo collision-search infrastructure

**From:** Chief Researcher  
**To:** Compute Agent  
**Date:** 2026-09-29  
**Priority:** P0

## Scientific objective

Build a trustworthy discovery pipeline for the following finite-dimensional condition:

[
H(p,q,t,s)=x(t;p)-x(s;q)=0,
]

where (p,q) are standard physical initial states of the **same autonomous Caputo system**, and ultimately (p,q) must lie in distinct robust asymptotic basins.

A successful inter-basin collision will be lifted by the Chief to a multibasin reachable present-state fiber. Your output is computational evidence only unless a rigorous certificate is explicitly produced.

## Stage A — solver validation (mandatory before discovery)

Implement or select **two independent history-retaining Caputo solvers**.

Required:
- known Mittag–Leffler linear test(s);
- mesh refinement / observed convergence;
- long-horizon stability test;
- deterministic reproducibility;
- regression tests;
- explicit dependency/environment versions.

Reject memoryless one-step surrogates as primary solvers.

## Stage B — published intersection reproduction

Reproduce a published multidimensional Caputo physical-state intersection example from Cong–Tuan (2017) or another verified published source.

Purpose:
- validate same-present collision detection;
- exercise root refinement;
- confirm that distinct continuation states can share the same physical endpoint.

This is **not** a novelty claim.

## Stage C — Double-Allee baseline

Reproduce one published fractional Double-Allee multistable model, preferably Mondal et al. (2025), using parameter values traceable to the paper/local bibliography.

Required:
- equilibria and local-stability sanity checks;
- positivity checks over tested trajectories;
- at least two long-run outcome classes if the published regime supports them;
- two-solver cross-check;
- mesh and horizon sensitivity;
- raw machine-readable data.

If exact equations/parameters cannot be recovered from the locally available sources, stop Stage C and report the missing information rather than guessing.

## Stage D — inter-basin collision discovery

Only after A–C pass, search for
[
x(t;p)\approx x(s;q)
]
with (p,q) drawn from distinct **conservatively classified** outcome sets.

Search both:
- same-age (t=s);
- cross-age (t\ne s).

Use near-collisions only to seed nonlinear root refinement. Save every candidate with full provenance.

For a refined root, estimate the rank/singular values of the Jacobian of (H) with respect to a declared set of free variables. This is to test the Chief's candidate transversality theorem.

## Evidence classes

- floating point search: NUMERICAL CORROBORATION / CONJECTURE GENERATOR;
- high precision root: still numerical unless certified;
- interval/Krawczyk/radii-polynomial style inclusion: CERTIFIED COMPUTATION if all assumptions and arithmetic semantics are documented.

Do **not** call finite-horizon labels basin proofs.

## Stop conditions

Stop and report cleanly if:
- the two solvers disagree beyond convergence expectations;
- the published baseline cannot be faithfully reconstructed;
- collision candidates vanish under mesh/horizon refinement;
- only boundary/ambiguous outcomes are found;
- the candidate Jacobian is rank-deficient at all robust roots.

Negative search is not an impossibility theorem.

## Expected artifacts

- `computations/` code, tests, environment lock/spec;
- raw and processed data;
- `research/coordination/compute-to-chief/TASK-0001_validated-collision-search_RETURN.md`;
- exact reproduction commands;
- branch/final commit SHA;
- evidence labels and caveats.

Follow `research/coordination/PROTOCOL.md`.
