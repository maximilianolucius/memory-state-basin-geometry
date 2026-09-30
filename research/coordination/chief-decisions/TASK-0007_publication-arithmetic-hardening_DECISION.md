# Chief Decision — TASK-0007 Publication Arithmetic Hardening

**Date:** 2026-09-30
**Disposition:** ACCEPT / PROMOTE TO PRINCIPAL COMPUTATIONAL BASELINE

## Evidence label

\[
\boxed{\text{END-TO-END VERIFIED ELEMENTARY-FUNCTION ENCLOSURES}}
\]

This label applies to the principal \(T=300,N=12000\) B215 certificate.

It does **not** mean fully interval arithmetic. Load-bearing elementary functions are enclosed with Arb; the dense approximate inverse and large nonnegative bound-operator reductions use binary64 algebra with explicit a-posteriori Higham roundoff bounds.

## Hardened principal constants

- \(\|E\|_\infty\le2.09096\times10^{-10}\);
- componentwise self-map minimum relative slack \(\ge6.0254\times10^{-4}\);
- Perron contraction \(\kappa\le0.0861986<1\);
- adapted state tube \(\le4.87385\times10^{-4}\);
- physical state tube \(\le2.22282\times10^{-4}\);
- certified entry remains 836 cells on \([5.8576774143,13.7275388580]\);
- representative threshold margin \(\eta\ge0.0309410164\);
- \(K_J\le11.3499042225\);
- \(M_T\le0.0432327049\);
- M1 margin \(\ge0.0135623350\);
- \(K_JC_rr\le0.488563351<1\).

## Audit significance

TASK-0007 removed every load-bearing few-ulp libm assumption and corrected six TASK-0006 bookkeeping/roundoff defects. Two legacy fixed-slack constructions were not valid upper bounds at the actual reduction lengths. The hardened rerun repairs them and reproduces every theorem verdict.

Therefore all principal manuscript computational claims must cite TASK-0007 values. TASK-0006 remains provenance and the \(T=1000,N=20000\) redundancy certificate.

## Redundant cut

The \(T=1000\) run is not rerun. It is not load-bearing and remains explicitly labeled as TASK-0006 redundancy under the earlier arithmetic model.

## Scientific consequence

No theorem statement or novelty claim changes. TARGET-A20 remains proved; the computational evidence language is strengthened.
