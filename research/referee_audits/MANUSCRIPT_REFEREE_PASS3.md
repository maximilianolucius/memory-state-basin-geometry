# Referee Audit Pass 3 — Hardened Arithmetic and Final Evidence Boundary

**Date:** 2026-09-30  
**Role:** hostile internal referee  
**Scope:** TASK-0007 arithmetic hardening, manuscript numerical constants, and evidence language  
**Verdict:** PASS

## 1. Principal certificate regeneration

PASS.

The primary exact-rational B215 certificate was regenerated at
\[
T=300,\qquad N=12000
\]
with the same mesh and with the hardened arithmetic layer.

All theorem verdicts reproduce:
- Banach self-map: PASS;
- Perron contraction: PASS;
- extinction-strip entry: CERTIFIED;
- M1 inequality: SEPARATED.

## 2. Legacy arithmetic defects

PASS AFTER CORRECTION.

TASK-0007 identified six TASK-0006 bookkeeping defects:
1. fixed \(10^{-13}\) slacks used on long reductions where the actual Higham \(\gamma_n\) is larger;
2. missing rounding enclosure on Abel cumulative sums;
3. omitted float-conversion radius for \(A_n\);
4. omitted final residual/inverse-product roundings;
5. omitted weight-data radii in the mean-kernel blocks;
6. non-directed floating-point threshold comparisons in Stage E.

Two of these meant that the TASK-0006 expressions were not valid upper bounds as written at \(N=12000\). TASK-0007 repairs all six and reruns the complete principal certificate. No theorem verdict changes.

## 3. Elementary functions

PASS.

All load-bearing elementary-function evaluations are now enclosed using Arb or exact/closed-form constructions. The arithmetic inventory contains zero category-3 (few-ulp libm) quantities.

Approved evidence label:
\[
\boxed{\text{END-TO-END VERIFIED ELEMENTARY-FUNCTION ENCLOSURES}}.
\]

## 4. Remaining binary64 layer

PASS WITH EXPLICIT BOUNDARY.

The dense approximate inverse and large positive algebraic reductions are still evaluated in binary64, but every load-bearing reduction carries an explicit length-dependent Higham error bound. This is a rigorous a-posteriori floating-point enclosure strategy, not set-valued interval arithmetic throughout.

Therefore the manuscript must not say ``fully interval arithmetic'' or equivalent.

## 5. Hardened margins

PASS.

Principal margins remain comfortably strict:
\[
\|E\|_\infty\le2.09096\times10^{-10},
\]
\[
\min\operatorname{slack}(F(b)<b)\ge6.0254\times10^{-4},
\]
\[
\kappa\le0.0861986<1,
\]
\[
\|X-\widehat X\|_2\le2.22282\times10^{-4},
\]
\[
\eta\ge0.0309410164,
\]
\[
r-K_JC_rr^2-M_T\ge0.0135623350>0.
\]

No conclusion depends on a numerically marginal sign decision.

## 6. Redundant cut

PASS.

The \(T=1000,N=20000\) computation is not load-bearing and was not rerun. It may remain in the paper only if explicitly identified as secondary TASK-0006 redundancy under the earlier arithmetic model.

## 7. Manuscript consistency

PASS subject to CI.

The principal theorem, CAP section, certified-entry figure, M1 budget figure, and reproducibility statement have been updated to TASK-0007 constants. A repository search finds no old principal TASK-0006 values in `paper/`.

## Referee-3 disposition

\[
\boxed{\text{PASS}}
\]

The arithmetic-hardening gate is closed. No further computation is required for first submission unless journal review specifically requests a hardened rerun of the redundant \(T=1000\) cut.
