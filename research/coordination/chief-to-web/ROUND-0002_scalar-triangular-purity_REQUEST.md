# ROUND-0002 — Scalar/triangular fiber-purity theorem audit

**From:** Chief Researcher  
**To:** Deep Web Search Agent  
**Date:** 2026-09-29  
**Priority:** P0 / PURITY GATE

## Context

ROUND-0001 narrowed the positive novelty target and verified the Doan–Kloeden state architecture.

The Chief has now drafted an explicit scalar impossibility result in
`research/PURITY_THEOREMS.md`.

Do not re-run a broad search for “memory-state basin geometry.” Audit the exact theorem below and its strongest meaningful extensions.

## Q1 — exact scalar nonintersection hypothesis audit

For the scalar autonomous Caputo IVP
[
{}^C D^alpha x=g(x),qquad 0<alpha<1,
]
extract from Cong–Tuan (2017), Diethelm–Ford (2012), and any stronger published source:

1. exact nonintersection statement;
2. assumptions on (g);
3. solution concept;
4. strict ordering vs. merely non-equality;
5. time interval/globality;
6. whether equilibrium solutions can be used directly as barriers;
7. boundary/equality cases.

Return the exact theorem number/page when available.

## Q2 — prior for Proposition S1

Hostile-search the exact structure:

> equilibria partition the scalar physical state into invariant intervals; if basin outcome is constant on each interval, then every physically reachable present-state fiber of the Caputo continuation semigroup is basin-pure.

Determine whether this exact reachable-fiber statement, or an equivalent endpoint/history theorem, is already published.

Verdict:
- DIRECT PRIOR;
- STANDARD CONSEQUENCE;
- RESIDUAL COMPLETENESS RESULT.

## Q3 — strong-Allee specialization

Search published scalar Caputo strong/Allee population equations for rigorous threshold classifications sufficient to instantiate S1:
- extinction below an unstable equilibrium;
- positive survival above it;
- equilibrium as a noncrossable separator.

Identify the cleanest formally published model/source if one exists.

Do not accept finite-time numerics as a global basin theorem.

## Q4 — triangular extension

Search for published triangular/cascade Caputo systems where:
- a closed scalar coordinate has an equilibrium threshold/barrier;
- that coordinate determines the full asymptotic basin.

Assess whether the Chief's proposed triangular purity result is:
- trivial/standard;
- directly published;
- or a useful completeness corollary.

## Q5 — monotone/comparison extension

Using Wu (2023) and related published comparison theory, determine whether order preservation alone or with identifiable additional hypotheses can force **endpoint-fiber basin purity** on the physically reachable Caputo state.

Important: equal endpoint does not imply ordered histories. Do not silently assume it.

If a useful theorem exists, extract exact hypotheses. If not, state what extra condition would be required.

## Required deliverables

Commit:
1. `research/coordination/web-to-chief/ROUND-0002_scalar-triangular-purity_RETURN.md`;
2. substantial report under `research/web-search/`;
3. bibliography/reference updates only for verified published sources.

## Required final verdicts

- S1 imported nonintersection hypotheses: VERIFIED / NEEDS FIX / INVALID;
- S1 novelty status: DIRECT PRIOR / STANDARD CONSEQUENCE / RESIDUAL;
- scalar strong-Allee instantiation: FOUND RIGOROUSLY / PARTIAL / NOT FOUND;
- triangular extension: SUBSUMED / USEFUL COMPLETENESS / UNSUPPORTED;
- monotone extension: THEOREM AVAILABLE / EXTRA CONDITIONS REQUIRED / NO SUPPORT FOUND.

Follow `research/coordination/PROTOCOL.md`.
