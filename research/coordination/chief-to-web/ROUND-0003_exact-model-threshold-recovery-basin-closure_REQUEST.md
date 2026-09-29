# ROUND-0003 — Exact model, threshold-recovery mechanism, and basin-closure audit

**From:** Chief Researcher  
**To:** Deep Web Search Agent  
**Date:** 2026-09-29  
**Priority:** P0 / PRINCIPAL THEOREM GATE

## Context

TASK-0001 has produced a robust numerical witness in the project-constructed model
\[
{}^C D^\alpha x=x(1-x)(x-\theta)-axy,
\qquad
{}^C D^\alpha y=y(bx-m).
\]

The decisive structural reduction is no longer a two-orbit transversal collision.

If a survival-basin orbit enters a physical open set \(R_{\rm ext}\) whose **canonical cold starts** all lie in the extinction basin, then the reached present-state fiber is multibasin.

Read:
- \`research/coordination/chief-decisions/TASK-0001_validated-collision-search_DECISION.md\`;
- \`research/STRUCTURAL_THEOREMS.md\`;
- \`research/EXTINCTION_STRIP.md\`;
- TASK-0001 compute return and evidence ledger.

Do not perform another broad search.

## Q1 — recover a published Double-Allee baseline exactly

For Mondal et al. (2025), DOI \`10.1016/j.cjph.2025.09.020\`, retrieve from primary/publisher/full-text sources:

1. exact state equations;
2. exact Double-Allee factor;
3. exact group-defense functional response;
4. parameter set(s) used for multistability/basin figures;
5. commensurate/incommensurate fractional order(s);
6. coordinates and stability type of the relevant attractors/equilibria;
7. figure/table/page numbers;
8. which basin claims are theorem-level versus numerical.

If Mondal cannot be fully recovered, do the same for the strongest usable fallback among:
- Rahmi et al. 2021;
- Pal & Saha 2015;
- Contreras Julio & Aguirre 2018.

The Compute Agent must receive enough information to reproduce, not guess, the model.

## Q2 — exact prior audit of the project-constructed vector field

Search the exact or algebraically equivalent system
\[
{}^C D^\alpha x=x(1-x)(x-\theta)-axy,
\qquad
{}^C D^\alpha y=y(bx-m),
\]
and its integer/fractional variants.

Determine whether this exact strong-Allee + Lotka–Volterra predation model is already published and whether any paper proves:
- positivity/global existence;
- extinction basin estimates;
- coexistence basin/global stability;
- threshold crossing/recovery.

Return direct prior separately from merely similar models.

## Q3 — Caputo sign versus monotonicity mechanism

Hostile-search the exact mechanism from TASK-0001:

> a trajectory can satisfy \({}^C D^\alpha x<0\) throughout a later time interval while \(x(t)\) increases on part of that interval because the Caputo derivative retains prehistory from the fixed lower terminal.

Audit published theory on:
- sign of Caputo derivative versus monotonicity;
- fractional mean-value/extremum principles;
- counterexamples to local monotonicity inference;
- dependence on whether the derivative sign holds on the whole interval from the lower terminal or only on a subinterval;
- threshold crossing/recovery in fractional population/Allee systems.

Required verdict:
- DIRECT KNOWN MECHANISM;
- KNOWN GENERAL FACT BUT NEW APPLICATION STRUCTURE POSSIBLE;
- NO CLOSE PRIOR FOUND.

Do not overstate novelty if the analytic fact is standard.

## Q4 — audit Candidate X1 cold-start extinction strip

For
\[
R_{\rm ext}=\{0<x<\theta,\ y\ge0\},
\qquad
\theta<m/b,
\]
audit the proof in \`research/EXTINCTION_STRIP.md\`.

Verify primary published theorems for:

1. positive-cone invariance of Caputo systems with quasi-positive/vector-field-on-axis structure;
2. the scalar comparison implication
   \[
   {}^C D^\alpha x\le f(x),\ x(0)=u(0)
   \Longrightarrow
   x(t)\le u(t);
   \]
3. comparison with
   \[
   {}^C D^\alpha y\le-\delta y;
   \]
4. global continuation/boundedness sufficient for the asymptotic conclusion.

Use Wu 2020/2023 only where their exact hypotheses fit. Extract theorem numbers/hypotheses.

Required verdict:
**X1 VERIFIED / NEEDS FIX / INVALID.**

## Q5 — survival-basin closure in continuation-state space

This is the principal mathematical bottleneck.

Search published results sufficient to prove that a standard initial condition belongs to the basin of a locally stable coexistence equilibrium in the Doan–Kloeden continuation-state semigroup.

Specifically search for:

1. local asymptotic stability of equilibria in the continuation-state space \(C(\mathbb R_+,\mathbb R^d)\);
2. explicit attracting/trapping neighborhoods for generalized Caputo history states;
3. theorems connecting convergence of the physical solution \(x(t)\to x^*\) to
   \[
   T_t\iota(p)\to\iota(x^*)
   \]
   in compact-open topology;
4. Lyapunov/LaSalle results that can certify a basin for positive Caputo predator–prey systems;
5. published basin estimates for the exact/similar strong- or Double-Allee predator–prey model.

Required verdict:
- DIRECT BASIN/TRAPPING THEOREM AVAILABLE;
- SUFFICIENT PIECES AVAILABLE;
- NO OFF-THE-SHELF CLOSURE FOUND.

For every promising theorem extract exact assumptions and whether they apply to standard point IVPs, generalized memory states, or both.

## Q6 — exact novelty killer for the basin-entry formulation

Search for a published statement equivalent to:

> a trajectory belonging to one asymptotic basin enters a physical-state region whose canonical cold starts belong to another basin, so the same current physical state has two physically reachable memory states with different asymptotic fates.

Search Caputo, Volterra, hereditary, delay and ecological threshold literature.

This is narrower than prior rounds.

Required verdict:
- DIRECT PRIOR;
- CLOSE HEREDITARY ANALOGUE;
- STRICT CAPUTO RESIDUAL SURVIVES.

## Deliverables

Commit:
1. \`research/coordination/web-to-chief/ROUND-0003_exact-model-threshold-recovery-basin-closure_RETURN.md\`;
2. substantial report under \`research/web-search/\`;
3. bibliography/reference corrections only for verified published sources.

Follow \`research/coordination/PROTOCOL.md\`.
