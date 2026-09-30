# Status

**Phase:** ACTIVE — M1 FEASIBLE; VALIDATED-HISTORY METHOD IS THE BOTTLENECK

## TASK-0004 assimilated — 2026-09-30

Branch:
\`compute/task-0004\`

Verified HEAD:
\`b57774734379640861f4cb48ae2620ee0abe4100\`

Merged:
PR #4 -> main at \`37258073f91a177882d615381fd67e576fd59a86\`.

## What TASK-0004 established

For W1, the memory-tail theorem M1 is numerically feasible from late cut times.

The adapted norm gives substantially better kernel constants than Euclidean norm.

The failure is the finite-history validation:
the current normwise a-posteriori recursion loses huge cancellation during the nonlinear excursion.

No rigorous \(M_T\) was obtained.

Therefore:
\[
\boxed{\text{TARGET-A20 remains OPEN}.}
\]

## Methodological change

Do not push the existing second-order verifier to vastly larger \(N\).

Next:
- preserve the time-dependent matrix linearization along the orbit;
- construct/approximate the inverse Volterra operator;
- measure sign-aware amplification;
- add higher-order polynomial residuals only if amplification is manageable.

## Active

- ROUND-0006 — rigorous orbit-linearized Volterra validation audit.
- TASK-0005 — sign-aware approximate-inverse feasibility/certification.

## Paper

NOT STARTED.
