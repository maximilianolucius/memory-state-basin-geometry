# INITIAL THEOREM PROGRAM — CHIEF DECISION

**Date:** 2026-09-29  
**Disposition:** START FEASIBILITY / FALSIFICATION; MANUSCRIPT REMAINS BLOCKED

## Decision

The project will pursue two theorem tracks in parallel:

1. **Purity track:** prove endpoint/present-state basin purity under explicit barrier, triangular, or comparison-dominated hypotheses. No claim that generic monotonicity or triangularity alone suffices.
2. **Existence track:** reduce multibasin-fiber existence to a physical collision between standard IVPs from distinct basins, then seek an open-family theorem from a transverse collision plus robust basin trapping.

## Immediate structural insight

The constructive search does not need arbitrary ambient history states.

If two standard IVPs start in distinct basins and their physical trajectories meet at possibly different ages, the two continuation states are physically reachable, share the same present value, and retain distinct asymptotic basin membership by forward invariance. This is recorded as candidate lemma M1 in `research/STATE_ARCHITECTURE.md`.

The stronger candidate M2 is:

> transverse inter-basin physical collision + robust basin trapping + sufficient parameter regularity implies persistence of multibasin reachable fibers on an open parameter/order neighborhood.

M2 is **OPEN** and must survive the literature/source audit before promotion.

## Why this direction

It directly addresses the inherited critical risk that a positive example might otherwise require artificial histories. It also gives a route from one discovered collision to an open-family theorem, satisfying the publication directive against benchmark-only results.

## Delegation

- Deep Web Search: ROUND-0001 state architecture / collision-persistence killer audit.
- Compute: TASK-0001 validated Caputo solver + published intersection reproduction + Double-Allee baseline + inter-basin collision discovery.

## Gate

No manuscript drafting. No TARGET claim is promoted until the web-search return, exact theorem hypotheses, and independent compute validation are assimilated.
