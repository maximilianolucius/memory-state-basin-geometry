# TASK-0007 — Publication arithmetic hardening

**From:** Chief Researcher  
**To:** Compute Agent  
**Date:** 2026-09-30  
**Priority:** P0 FOR SUBMISSION ROBUSTNESS / NOT A NOVELTY GATE

## Objective

Remove the principal arithmetic-referee vulnerability from the successful TASK-0006 \(T=300,N=12000\) certificate.

The mathematical theorem and CAP architecture are already accepted.

Do not redesign the proof unless hardening exposes an actual error.

## Primary target

B215 primary certificate:

\[
T=300,\qquad N=12000.
\]

Preserve the exact rational benchmark and the same adaptive mesh unless a verified arithmetic implementation requires a mechanically equivalent representation.

## A — inventory every load-bearing floating operation

From \`computations/msbg/cap.py\` and the Stage-E pipeline, classify every quantity as:

1. Arb/interval already rigorous;
2. binary64 algebra with a proved Higham-style roundoff bound;
3. binary64 transcendental/libm evaluation covered only by the current few-ulp assumption;
4. corroborative/non-load-bearing.

Return a machine-readable inventory.

## B — eliminate category 3

Replace every load-bearing use of:
- \`pow\`;
- \`expm1\`;
- \`log1p\`;
- \`gamma\`;
- any other elementary function whose proof currently uses a few-ulp assumption,

with one of:
- Arb ball evaluation;
- MPFR/directed interval enclosure;
- another explicitly verified enclosure.

For \(O(N^2)\) kernels, hybridize if necessary:
compute rigorous interval endpoints/constants once per geometric pattern or in vectorized/block form while preserving an actual upper bound.

## C — audit category 2

The float dense inverse may remain if its residual and all product/sum rounding errors are rigorously enclosed without an unsupported libm assumption.

Re-derive/check:
- \(\gamma_n\) constants;
- BLAS/dot-product assumptions;
- possible fused-multiply-add behavior;
- OpenBLAS threading/reduction order;
- conversion of Arb mid/radius to floats;
- all uses of fixed relative slack such as \(10^{-13}\).

If any bound depends on an undocumented BLAS reduction model, replace that computation by a reproducible verified accumulation or add a valid operation-count bound independent of ordering.

## D — regenerate the primary certificate

Recompute the full \(T=300,N=12000\) proof.

Required final items:
- verified inverse residual;
- componentwise \(F(b)<b\);
- Perron contraction \(\kappa<1\);
- state tube;
- certified entry;
- \(K_J,C_r,M_T\);
- positive M1 margin.

Compare all final constants against TASK-0006.

## E — evidence label

Best outcome:

\[
\boxed{\text{END-TO-END VERIFIED ELEMENTARY-FUNCTION ENCLOSURES}}
\]

with any remaining standard IEEE arithmetic assumptions explicitly listed.

Do not use the phrase “fully interval” unless every load-bearing arithmetic layer actually is interval/set-valued.

## F — redundancy

Do not rerun \(T=1000,N=20000\) unless:
- the \(T=300\) hardening fails;
- or the implementation change reveals a systematic issue that must be checked independently.

The existing \(T=1000\) result remains secondary redundancy.

## Return

Write:
\`research/coordination/compute-to-chief/TASK-0007_publication-arithmetic-hardening_RETURN.md\`.

No theorem promotion is needed if the hardening reproduces TASK-0006; report it as publication robustness.
