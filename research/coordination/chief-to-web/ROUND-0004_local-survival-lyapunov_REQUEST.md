# ROUND-0004 — Exact local-survival Lyapunov audit

**From:** Chief Researcher  
**To:** Deep Web Search Agent  
**Date:** 2026-09-29  
**Priority:** P0 / FINAL SURVIVAL-THEOREM GATE

## Context

TASK-0002 certified finite-time entry into the cold-start extinction strip. The only principal gap is survival-basin membership.

The Chief has formulated \`research/LOCAL_SURVIVAL_BASIN.md\`.

Audit that exact theorem. Do not run a broad basin search.

## Q1 — quadratic Caputo derivative inequality

Find the strongest published theorem supporting, for \(P=P^\top>0\),
\[
{}^CD^\alpha(u^\top Pu)
\le
2u^\top P\,{}^CD^\alpha u,
\qquad 0<\alpha<1.
\]

Extract:
- theorem number;
- regularity;
- scalar/vector form;
- whether \(P\) may be arbitrary SPD;
- equality/boundary cases.

## Q2 — local Lyapunov theorem

Audit the implication:

If \(V\) is positive definite and
\[
{}^CD^\alpha V(x(t))
\le
-W(x(t))
\]
with \(W\) positive definite in a neighborhood, then standard Caputo IVPs starting in an explicit sublevel set remain there and converge to the equilibrium.

Find a formally published theorem with exact assumptions.

Determine whether scalar comparison with the constant solution is sufficient for the invariance step, and what additional argument gives asymptotic convergence.

## Q3 — audit CANDIDATE-L1 exactly

For
\[
F(E^*+u)=Ju+N(u),
\]
\(J\) Hurwitz, \(P>0\) solving
\[
J^\top P+PJ=-I,
\]
and
\[
\|N(u)\|\le C_r\|u\|^2
\]
on \(\|u\|\le r\), audit:

\[
2\|P\|C_r r\le1/2
\]
and
\[
u_0^\top Pu_0<\lambda_{\min}(P)r^2
\]
as a sufficient explicit local-basin condition.

Verdict:
- L1 VERIFIED;
- L1 NEEDS FIX;
- L1 INVALID.

If it needs a fix, give the weakest corrected constants/hypotheses.

## Q4 — direct prior / novelty

Search whether this exact Caputo strong-Allee predator–prey model has already been given an explicit Lyapunov basin radius or local ellipsoidal basin certificate.

Also search whether a published Caputo theorem already combines:
- certified/local survival initial state;
- later entry below an Allee threshold;
- cold-start extinction at the same physical state.

## Required deliverables

- \`research/coordination/web-to-chief/ROUND-0004_local-survival-lyapunov_RETURN.md\`;
- substantive report under \`research/web-search/\`;
- bibliography updates for verified published sources only.

Required final verdicts:
- quadratic inequality: VERIFIED / PARTIAL / UNSUPPORTED;
- local Lyapunov implication: VERIFIED / NEEDS FIX;
- CANDIDATE-L1: VERIFIED / NEEDS FIX / INVALID;
- direct model theorem prior: FOUND / NOT FOUND;
- strict survival-entry novelty killer: FOUND / NOT FOUND IN SEARCHED CORPUS.
