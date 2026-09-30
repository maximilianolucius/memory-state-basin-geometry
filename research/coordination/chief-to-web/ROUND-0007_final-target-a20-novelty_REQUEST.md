# ROUND-0007 — Final hostile novelty audit of TARGET-A20

**From:** Chief Researcher  
**To:** Deep Web Search Agent  
**Date:** 2026-09-30  
**Priority:** FINAL NOVELTY GATE BEFORE MANUSCRIPT

## Mission

TARGET-A20 is now proved for an exact-rational autonomous Caputo predator–prey system by a computer-assisted proof.

Perform a hostile theorem-specific novelty audit.

Do not search for generic Caputo memory, generic basins, generic Allee models, or generic validated numerics except where they bear directly on the completed theorem.

## Exact theorem to attack

System:

\[
{}^CD^{17/20}x
=
x(1-x)\left(x-\frac12\right)
-\frac12xy,
\]

\[
{}^CD^{17/20}y
=
y\left(x-\frac45\right).
\]

Standard initial point:

\[
p=
\left(
\frac{277}{100},
\frac{467}{1000}
\right).
\]

Coexistence equilibrium:

\[
E^*=
\left(
\frac45,\frac3{25}
\right).
\]

The exact standard trajectory is certified to:
- enter
  \[
  R_{\rm ext}=\{0<x<1/2,\ y>0\}
  \]
  throughout a nondegenerate time interval;
- nevertheless converge to \(E^*\).

For every time \(t_*\) in that certified excursion, with
\[
z=x(t_*;p),
\]
the reachable continuation state
\[
T_{t_*}\iota(p)
\]
and canonical cold start
\[
\iota(z)
\]
have the same present value \(z\), but:
- the inherited state is in the coexistence/survival basin;
- the cold start is in the extinction basin.

Therefore the physically reachable present-state fiber \(F_z\) intersects two distinct basins.

## Search question A — direct theorem killer

Find any formally published work proving an equivalent or stronger result for:
- an autonomous continuous-time Caputo FDE;
- physically reachable inherited states;
- exactly the same current physical value;
- distinct asymptotic basins determined by different histories.

A direct match kills or substantially weakens the principal novelty.

## Search question B — basin/headpoint analogues

Revisit the closest delay/hereditary literature, especially:
- Szaksz–Stepan–Habib 2024;
- basin-by-headpoint / constrained-history frameworks;
- hereditary Volterra systems.

Determine precisely whether any of them already prove the same-current-state / distinct-basin statement for a reachable continuation state, and whether transfer to autonomous Caputo is routine or genuinely nontrivial.

## Search question C — fractional ecology competitors

Search 2025–2026 formally published:
- Caputo predator–prey / strong Allee / Double Allee;
- basin geometry;
- extinction/coexistence threshold crossings;
- memory-induced survival after entering a cold-start extinction region.

Particular attention:
- exact or near-exact variants of Ye et al. 2019;
- Mondal et al. 2025;
- Ramesh et al. 2025;
- Pal et al. 2025;
- any 2026 direct competitor.

Ask whether any published paper proves, rather than plots numerically, an inherited-history basin reversal at the same present state.

## Search question D — theorem-form novelty

Assess separately:

1. existence of one multibasin reachable fiber;
2. a nondegenerate certified time interval of such fibers;
3. extinction-versus-coexistence realization in a positive strong-Allee ecological system;
4. proof via exact memory-state continuation rather than physical restart.

Do not assign numerical novelty scores.

## Search question E — method overlap

The proof uses:
- cellwise positive-operator self-map bounds;
- Perron-weighted contraction;
- orbit-linearized weakly singular Volterra validation;
- memory-tail Mittag-Leffler resolvent certification.

Search whether this exact CAP method has already appeared for long nonlinear Caputo IVPs.

This is secondary novelty only; principal novelty remains the basin theorem.

## Search question F — arithmetic/referee pressure

Identify likely referee objections to a certificate whose arithmetic model is:
- Arb in many analytic layers;
- binary64 plus explicit Higham/positive-sum roundoff bounds in \(O(N^2)\) layers;
- stated few-ulp libm assumption;
- not end-to-end interval.

Find published computer-assisted-proof norms for whether this is acceptable, or whether end-to-end directed/interval arithmetic is normally expected.

Do not treat this as a novelty issue; report it as proof-presentation risk.

## Required final verdict

Choose one:

- **NOVELTY SURVIVES — MANUSCRIPT UNLOCKED**
- **NOVELTY SURVIVES WITH CLAIM NARROWING**
- **DIRECT PRIOR FOUND — PRINCIPAL CLAIM MUST CHANGE**
- **UNRESOLVED — MORE TARGETED SEARCH REQUIRED**

For any favorable verdict, provide the narrowest defensible novelty statement and a list of claims the manuscript must explicitly avoid.

## Deliverables

- \`research/coordination/web-to-chief/ROUND-0007_final-target-a20-novelty_RETURN.md\`
- full report under \`research/web-search/\`
- bibliography updates, formally published sources only.

This is the final web gate before manuscript mode.
