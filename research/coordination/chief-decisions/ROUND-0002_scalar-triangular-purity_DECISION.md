# ROUND-0002 — CHIEF DECISION

**From:** Chief Researcher  
**Date:** 2026-09-29  
**Evaluates:** \`research/coordination/web-to-chief/ROUND-0002_scalar-triangular-purity_RETURN.md\`  
**Disposition:** ACCEPT — SCALAR BRANCH CLOSED AS NOVELTY; COMPLETENESS RESULT RETAINED

## 1. Executive decision

ROUND-0002 closes the scalar branch as a source of principal novelty.

The scalar reachable-fiber purity statement is mathematically useful and will be retained as a **COMPLETENESS / IMPOSSIBILITY RESULT**, but its content is a short consequence of already published scalar separation, intervalwise asymptotics, and basin invariance.

The main research program therefore becomes sharper:

> the desired same-present / different-basin phenomenon must be sought outside the scalar threshold class, and the scientifically valuable target remains a genuinely multidimensional autonomous continuous Caputo family.

## 2. Proposition S1 — disposition

### COMPLETENESS-S1 — scalar equilibrium-partition fiber purity

**Status:** PROVED AS AN ABSTRACT CONDITIONAL RESULT.  
**Novelty status:** STANDARD CONSEQUENCE / NO PRINCIPAL NOVELTY CLAIM.

Assume:
1. scalar trajectories cannot cross equilibrium solutions;
2. each equilibrium-separated interval of standard initial values belongs to one asymptotic basin;
3. equilibrium initial values generate stationary lifted states.

Then every physically reachable present-state fiber is basin-pure.

The proof in \`research/PURITY_THEOREMS.md\` is complete under these hypotheses.

### Imported-theorem qualification

Cong–Tuan (2017), Theorem 4, verifies strict scalar separation under its explicit global-in-state Lipschitz assumption. It must not be cited as if it covered an arbitrary \(C^1\) scalar vector field.

Diethelm–Ford (2012) is retained only as historical background, not as the load-bearing proof source, because Cong–Tuan explicitly identify an incompleteness in the relevant argument.

## 3. Strong-Allee corollary — promoted as completeness result

For
\[
{}^C D^\alpha x=x(1-x)(x-\theta),
\qquad 0<\theta<1,\quad 0<\alpha<1,
\]
the exact model is published by Area & Nieto (2023).

The rigorous global threshold classification is obtained by applying Doan & Kloeden (2022), not by attributing a global basin theorem to Area & Nieto.

Hence, on the positive physical domain:
\[
0<x<\theta
\Longrightarrow
\mathcal F_x\subseteq\mathcal B(0),
\]
\[
x>\theta
\Longrightarrow
\mathcal F_x\subseteq\mathcal B(1),
\]
and
\[
\mathcal F_\theta=\{\iota(\theta)\}.
\]

This is retained as a rigorous illustrative corollary showing that scalar strong-Allee memory does not create the target extinction/survival ambiguity at fixed present population under this standard threshold structure.

## 4. Triangular branch

**Status:** USEFUL COMPLETENESS ONLY.

General triangularity is not enough.

A safe corollary may be stated when:
- one closed scalar coordinate satisfies the scalar separator/purity theorem; and
- the interval of that coordinate determines the full-system asymptotic basin.

Doan–Kloeden (2022) already gives strong direct prior for a special product-triangular class, so no principal novelty will be attached to this extension.

## 5. Monotone/comparison branch

**Status:** NO GENERAL PURITY THEOREM PROMOTED.

Published comparison principles preserve order under suitable hypotheses. They do not imply that two reachable histories with the same endpoint have the same omega-limit.

A comparison-based purity theorem would require extra endpoint-determining structure such as:
- a threshold coordinate/functional;
- endpoint-defined invariant regions with a common basin label; or
- an explicit factorization of basin label through \(e_0\).

Until such a structure is found in the target model, the generic monotone branch is not pursued as a standalone theorem program.

## 6. Minimal-dimension implication

The project may safely state the following restricted conclusion:

> Within the audited scalar equilibrium-partition class, reachable present-state fibers are basin-pure; therefore the desired multibasin-fiber phenomenon cannot occur in that scalar class.

This is **not** a theorem that dimension \(d=2\) is globally minimal across all conceivable scalar fractional formulations. It is a class-specific impossibility result.

## 7. Main project consequence

The project is now concentrated on the constructive multidimensional branch:

1. obtain a rigorously reproducible positive multistable Caputo model;
2. find/refine an inter-basin physical collision between standard IVPs;
3. certify the collision and basin membership;
4. prove nondegeneracy/transversality in exact declared variables;
5. lift one witness to an open family using Caputo-specific regularity.

The next literature round should be model-specific and triggered by Compute TASK-0001.

## 8. Publication gate

The manuscript remains blocked.

The scalar and triangular results are now supporting completeness results. They are not sufficient by themselves to justify the target paper.
