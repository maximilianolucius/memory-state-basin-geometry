# TASK-0003 — Exact-rational locally certified survival witness

**From:** Chief Researcher  
**To:** Compute Agent  
**Date:** 2026-09-29  
**Priority:** P0 / TARGET-A20 CLOSURE ATTEMPT

## Goal

Find a witness whose survival-basin membership can be certified **from time zero** by CANDIDATE-L1 in
\`research/LOCAL_SURVIVAL_BASIN.md\`, and whose finite-time entry into
\[
R_{\rm ext}=\{0<x<\theta,\ y\ge0\}
\]
is certified by the TASK-0002 validated integrator.

This is a theorem-oriented search, not a deepest-dip search.

## A — exact-rational parameter search

Search exact rational parameter sets for
\[
{}^CD^\alpha x=x(1-x)(x-\theta)-axy,
\qquad
{}^CD^\alpha y=y(bx-m).
\]

Prioritize:
- \(0<\theta<1\);
- \(\theta<x^*=m/b<1\);
- \(x^*>(1+\theta)/2\) so \(J\) is Hurwitz;
- \(\theta\) near one to reduce the threshold gap;
- rational \(\alpha,\theta,a,b,m\).

Do not use binary64 approximations as the formal parameter definition.

## B — rigorous local basin certificate

For each candidate:

1. compute \(E^*\) exactly/rationally where possible;
2. certify \(J\) Hurwitz;
3. solve
   \[
   J^\top P+PJ=-I
   \]
   and rigorously enclose \(P\), \(\lambda_{\min}(P)\), \(\|P\|_2\);
4. rigorously bound
   \[
   \|N(u)\|_2\le C_r\|u\|_2^2
   \]
   on a ball;
5. maximize a certified radius \(r\) satisfying the current L1 sufficient inequality;
6. search initial states \(p\) inside the resulting certified ellipsoid.

Until ROUND-0004 returns, label this **L1-CONDITIONAL**, not proved survival.

## C — search inside the certified local basin

Among \(p\) satisfying the local-basin certificate, integrate with the validated numerical stack and find those whose trajectory crosses below \(x=\theta\).

Rank by:
1. certified local-basin margin;
2. threshold-entry margin;
3. simplicity of rational parameter values;
4. robustness.

If none exist, this is a valuable negative result; map how close trajectories approach the threshold.

## D — rigorous entry with exact rational inputs

For the best candidates, rerun the TASK-0002 a-posteriori verifier with:
- Arb rational parameters, not float conversions;
- exact rational \(\alpha\);
- exact rational \(p\) if feasible, otherwise an explicit small rational/interval box for \(p\).

Certify a nondegenerate time interval with
\[
0<x<\theta,\qquad y>0.
\]

Also recertify the original TASK-0001 witness with exact rational
\[
\theta=3/10,\quad m=4/5,\quad a=b=1,\quad\alpha=17/20
\]
for archival publication-grade evidence.

## E — optional direct survival certificate

If the L1 search fails, investigate a rigorous infinite-horizon a-posteriori contraction in a weighted norm around \(E^*\), but do not replace a theorem with a long finite-horizon simulation.

## Return

Commit:
\`research/coordination/compute-to-chief/TASK-0003_exact-rational-local-survival_RETURN.md\`

Report:
- exact parameter definitions;
- L1 certificate constants;
- whether any certified-local-basin trajectory enters \(R_{\rm ext}\);
- validated entry boxes;
- exact-rational recertification of the original witness;
- negative results and limitations.
