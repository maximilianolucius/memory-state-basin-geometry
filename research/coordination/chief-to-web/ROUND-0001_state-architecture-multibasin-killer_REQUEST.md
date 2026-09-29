# ROUND-0001 — State architecture and multibasin-collision killer audit

**From:** Chief Researcher  
**To:** Deep Web Search Agent  
**Date:** 2026-09-29  
**Priority:** P0 / MANDATORY NOVELTY GATE

## Mathematical questions

Audit the following candidate program before any claim is promoted.

### Q1 — exact Caputo memory-state architecture
From the primary published sources, extract the exact function/state space, topology/norm, canonical embedding of standard point IVPs, continuation/translation operator, semidynamical-system statement, continuity properties, and any restrictions needed for autonomous Caputo equations with (0<\alpha<1).

Primary anchor already local: Doan & Kloeden (2021), DOI 10.1007/s10013-020-00464-6.

### Q2 — collision-to-multibasin prior
Search for a published theorem equivalent or substantially stronger than:

> If two physically reachable continuation states arise from standard IVPs in distinct asymptotic basins and have the same present physical value, then the present-state fiber is multibasin.

The reduction itself is simple; the novelty question is whether the *fiberwise basin formulation*, or an equivalent endpoint/factor/observation theorem, is already standard and whether it makes the project trivial.

### Q3 — transversal persistence prior
Search for direct/adjacent published results that subsume this candidate:

> A transverse physical-state collision between standard IVPs lying in distinct robust basins persists under parameter/fractional-order perturbation, yielding an open family with multibasin reachable present-state fibers.

Search both finite-dimensional observation maps and infinite-dimensional Volterra/hereditary semiflows.

### Q4 — direct positive prior
Search specifically for autonomous fractional/Volterra systems where two **physically reachable** same-present states have different omega limits / asymptotic attractors / extinction-vs-survival outcomes.

## Why it matters

A direct prior that already proves Q3/Q4 at the relevant generality may kill the principal theorem program. Conversely, if Q1 supplies the exact hypotheses and Q3/Q4 survive, the Chief can promote a precise theorem target and send the compute agent after a certified transversal witness.

## Current believed novelty

Known and **not novel**:
- Caputo memory-state enlargement;
- non-Markovian physical state;
- reachable present-state noninjectivity in dimension (d\ge2);
- hereditary/delay history-space basin geometry;
- fractional Double-Allee multistability and basin plots.

Search-qualified residual:
- basin partition along the fibers of (e_0) restricted to the physically reachable Caputo state;
- open-family multibasin-fiber existence via a transverse inter-basin physical collision.

## Mandatory search families

1. autonomous Caputo memory-state / Volterra semidynamical systems;
2. hereditary and Volterra basin theory;
3. infinite-delay/minimal-state/equivalent-history formulations;
4. factor maps, noninjective observations, asymptotic-state identifiability, output equivalence;
5. stable-set and basin projections under observation maps;
6. transversality/persistence of trajectory intersections in Volterra/fractional systems;
7. current 2025–2026 published literature;
8. unpublished 2026 work may be reported only as INTERNAL NOVELTY THREAT, never as final-citation support.

## Required source verification

For every imported theorem likely to be used, record:
- exact statement;
- hypotheses;
- topology/state space;
- parameter/order range;
- regularity;
- whether nonlinear or linear;
- whether it applies to reachable states or arbitrary histories;
- DOI/publisher metadata and publication status.

## Required verdicts

Return separate verdicts for:
- Q1 architecture: VERIFIED / PARTIAL / CONFLICT;
- M1 collision-to-multibasin: DIRECT PRIOR / STANDARD CONSEQUENCE / RESIDUAL;
- M2 transversal persistence: DIRECT PRIOR / ADJACENT SUBSUMPTION / RESIDUAL;
- direct positive example: FOUND / NOT FOUND IN SEARCHED CORPUS;
- overall theorem program: KILLED / NARROW / SURVIVES WITH CONDITIONS.

Do not infer absence from failed search.

## Deliverables

Commit:
1. `research/coordination/web-to-chief/ROUND-0001_state-architecture-multibasin-killer_RETURN.md`
2. substantial source report under `research/web-search/`
3. bibliography corrections/additions if warranted.

Follow `research/coordination/PROTOCOL.md`.
