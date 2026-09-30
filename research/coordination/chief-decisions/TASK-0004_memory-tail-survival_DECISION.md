# TASK-0004 — CHIEF DECISION

**Date:** 2026-09-30  
**Branch:** \`compute/task-0004\`  
**Verified HEAD:** \`b57774734379640861f4cb48ae2620ee0abe4100\`  
**Merged to main:** PR #4, merge commit \`37258073f91a177882d615381fd67e576fd59a86\`  
**Disposition:** ACCEPT — M1 IS NUMERICALLY FEASIBLE; GLOBAL HISTORY ENCLOSURE IS THE BOTTLENECK

## 1. Main conclusion

TASK-0004 does not certify survival and therefore does not close TARGET-A20.

However it sharply localizes the remaining difficulty.

For W1, THEOREM-M1 is numerically feasible from late cut times:
\[
T\ge500
\]
in an adapted norm, with comfortable margin by \(T=1000\).

The failure is not the M1 inequality. It is the inability of the current a-posteriori history verifier to enclose the nonlinear excursion tightly enough.

## 2. Accepted results

### 2.1 M1 feasibility
NUMERICAL CORROBORATION:
- adapted norm feasible at \(T=500,1000,2000\);
- at \(T=1000\), the M1 margin is positive by roughly a factor \(2.8\) relative to the observed \(M_T\).

### 2.2 Resolvent identity
NUMERICAL CORROBORATION:
the PECE residual decreases at the expected mesh order.

### 2.3 THEOREM R
Promoted to **PROVED A-POSTERIORI REDUCTION**, now that ROUND-0005 has verified the needed variation-of-constants identity.

The theorem itself is correct; its present normwise implementation is too pessimistic during the excursion.

### 2.4 Kernel/nonlinearity constants
The adapted-norm computations give the benchmark values
\[
K_J\lesssim5.803469,
\]
\[
C_r\lesssim1.078088+0.706762\,r,
\]
with optimal M1 admissible linear-response threshold about
\[
M_T<0.038078.
\]

These are accepted as **CERTIFIED COMPUTATION conditional on the specific contour/integral representation implemented in \`kernel_bound.py\`**. ROUND-0005 verified the general Mittag-Leffler theory and decay but did not independently source-check every algebraic detail of that implementation's Hankel-collapse formula. This conditional tag is retained until the next audit.

## 3. Quantified obstruction

The current verifier replaces the time-dependent linearized dynamics along the orbit by a norm bound relative to the equilibrium Jacobian.

This creates enormous artificial amplification:
- W1: about \(10^{15.8}\) in exploratory adapted-norm profiling;
- best M1-feasible witnesses found: at least \(10^{5.4}\);
- B54 rigorous attempt: about \(10^{10}\) amplification and an eight-order enclosure gap.

The bound peaks during the nonlinear excursion and later saturates/decays.

Thus extending the same second-order method to a later \(T\) is not a viable strategy.

## 4. Chief methodological decision

Do **not** immediately spend compute on a brute-force higher-\(N\) version of the same verifier.

The next verifier must first address **amplification**, not only defect.

Use the Fréchet derivative along the computed orbit:
\[
A(t)=Dg(\hat x(t)),
\]
and the linearized Volterra operator
\[
\mathcal L_{\hat x}e
=
e-I^\alpha[A(\cdot)e].
\]

The intended a-posteriori equation is
\[
\mathcal L_{\hat x}e
=
-d+\mathcal N_{\hat x}(e),
\]
where \(d\) is the defect and the nonlinear remainder is quadratic.

A validated approximate inverse / two-time resolvent for \(\mathcal L_{\hat x}\) can preserve the sign and rotation cancellations destroyed by scalar norm Gronwall estimates.

Only after measuring this orbit-linearized amplification should higher-order piecewise polynomials be introduced.

## 5. Why this route is preferable

TASK-0001 sensitivity diagnostics already indicate that the true variational response along the nonlinear witness is modest, while the absolute-value verifier predicts factors of \(10^6\)–\(10^{16}\).

Therefore the dominant gap is likely wrapping/cancellation loss rather than intrinsic instability.

A higher-order approximation alone lowers the defect but still multiplies it by the same pessimistic amplification.

## 6. Next gates

- ROUND-0006: audit published rigorous/a-posteriori methods for weakly singular Volterra equations that use high-order collocation, Newton–Kantorovich/approximate inverses, or nonautonomous linearized resolvents.
- TASK-0005: build a sign-aware orbit-linearized feasibility prototype first; if amplification collapses sufficiently, turn it into a rigorous certificate and combine with higher-order residuals only as needed.

TARGET-A20 remains OPEN.
