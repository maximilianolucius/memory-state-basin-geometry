# TASK-0002 — CHIEF DECISION

**Date:** 2026-09-29  
**Branch:** \`compute/task-0002\`  
**Verified HEAD:** \`ba05c6c82051bd0477708982d47282c880c49bf9\`  
**Merged to main:** PR #2, merge commit \`0771917f7691024b21c7f847e4458e6e1b4bef6b\`  
**Disposition:** ACCEPT ENTRY CERTIFICATION / SURVIVAL STILL OPEN / CHANGE PROOF STRATEGY

## 1. Accepted as CERTIFIED COMPUTATION

The TASK-0001 witness is rigorously certified to enter the verified extinction strip.

For the exact binary64 inputs used by the verifier,
\[
\theta=0.3,\quad a=b=1,\quad m=0.8,\quad \alpha=0.85,\quad p=(2.4372,2.012),
\]
a validated Volterra a-posteriori enclosure proves, for example,
\[
t\in[3.387705,3.389048],
\]
\[
x(t)\in[0.195165,0.201521],
\qquad
y(t)\ge0.655495,
\]
hence
\[
x(t)<\theta-0.098479.
\]

The same solution is certified inside \(R_{\rm ext}\) over a nondegenerate contiguous time interval.

Evidence class: **CERTIFIED COMPUTATION**.

## 2. A-posteriori verifier — Chief audit

The theorem used by the verifier is accepted as an internal rigorous computational lemma.

Its essential ingredients are:
- exact Volterra defect identity;
- rigorous cellwise defect bounds;
- rigorous Jacobian/Lipschitz bounds on a bootstrap tube;
- a cellwise Volterra-Gronwall recursion;
- first-exit bootstrap;
- fail-safe UNDECIDED semantics.

The collocation approximation is not trusted; it only supplies a candidate \(\phi\). The certificate encloses an actual solution independently of the floating solver accuracy.

The tests against an exact planar Mittag-Leffler solution directly exercise the enclosure semantics.

### Publication correction required

The current certificates are for the exact IEEE-754 numbers nearest the printed decimals.

Before manuscript use, every load-bearing certificate must be rerun with **exact rational Arb inputs**, e.g.
\[
\theta=3/10,\quad m=4/5,\quad\alpha=17/20,
\]
and exact rational coordinates whenever the witness is chosen rationally or with explicitly enclosed parameter boxes.

## 3. Near-equilibrium search

Accepted as NUMERICAL CORROBORATION.

TASK-0002 found 237 cross-solver/mesh-confirmed witnesses and two near-equilibrium candidates with certified entry.

This is useful, but neither candidate has rigorous survival-basin membership.

The closest candidate is still not close enough to assume that a generic local-stability theorem captures it.

## 4. Continuation-state topology — exact consequence

TASK-0002 proves an important structural fact.

For a bounded standard orbit and fixed \(T\),
\[
(T_T\iota(p))(\tau)-p
=
\frac1{\Gamma(\alpha)}
\int_0^T
(T+\tau-s)^{\alpha-1}g(x(s))\,ds,
\]
so
\[
\|(T_T\iota(p))(\tau)-p\|
\to0
\qquad(\tau\to\infty).
\]

Thus, unless \(p=E^*\),
\[
\sup_{\tau\ge0}
\|(T_T\iota(p))(\tau)-E^*\|
\ge
\|p-E^*\|.
\]

Therefore convergence of continuation states to the equilibrium lift cannot hold in the unweighted global sup norm. The project's compact-open topology is essential.

This is promoted as STRUCTURAL-E4.

## 5. Principal gap after TASK-0002

Finite-time entry is no longer a gap.

For the TASK-0001 witness:
- cold-start extinction: PROVED (X1);
- entry into extinction strip: CERTIFIED COMPUTATION;
- survival convergence: **OPEN**.

Hence TARGET-A20 is now missing only a rigorous survival classification.

## 6. Strategy change

Do not spend the next compute cycle merely pushing the same far witness to longer horizons.

Instead seek a witness that is survival-classified **from time zero** by an explicit local Lyapunov basin theorem.

The target regime should satisfy ordinary Hurwitz stability of the coexistence Jacobian, so a quadratic Lyapunov function is available.

If a standard initial point lies in a rigorously certified local basin and its Caputo trajectory is also certified to enter \(R_{\rm ext}\), then X1 + E1 close TARGET-A20 without any long-time numerical inference.

## 7. Next actions

- ROUND-0004: audit the exact quadratic fractional Lyapunov theorem needed for the local survival basin.
- TASK-0003: search for an exact-rational, locally certified survival witness that also has certified entry into \(R_{\rm ext}\).

Manuscript mode remains blocked.
