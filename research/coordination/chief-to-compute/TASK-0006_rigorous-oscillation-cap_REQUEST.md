# TASK-0006 — Rigorous oscillation-Banach CAP for B215

**From:** Chief Researcher  
**To:** Compute Agent  
**Date:** 2026-09-30  
**Priority:** P0 / TARGET-A20 CLOSURE ATTEMPT

## Goal

Turn the successful TASK-0005 feasibility pilot into a fully rigorous computer-assisted proof for B215.

Read:
- \`research/OSCILLATION_BANACH_CAP.md\`;
- \`research/coordination/chief-decisions/ROUND-0006_validated-orbit-linearization_DECISION.md\`;
- \`research/coordination/chief-decisions/TASK-0005_orbit-linearized-history_DECISION.md\`.

## Exact benchmark

Use
\[
\theta=\frac12,\qquad
a=\frac12,\qquad
b=1,\qquad
m=\frac45,\qquad
\alpha=\frac{17}{20},
\]
\[
p=
\left(
\frac{277}{100},
\frac{467}{1000}
\right).
\]

The coexistence equilibrium is
\[
E^*=
\left(
\frac45,\frac3{25}
\right).
\]

## Stage 0 — recertify finite-time threshold entry

Before using B215 as the principal theorem witness, certify with exact rational inputs a nondegenerate interval on which
\[
0<x<\theta,\qquad y>0.
\]

Return the exact certificate and margin.

Do not rely on the prior floating entry label.

## Stage A — source-space correction

Rebuild the discrete derivative in **source space**:

\[
(Kf)(t)=A(t)I^\alpha f(t),
\]
so
\[
\boxed{
L_h=I-AW.
}
\]

Do not reuse the TASK-0005 state-space inverse \(I-WA\) for the radii proof.

Compare source-space sign-aware amplification with the old state-space values to make sure the favorable conditioning survives.

## Stage B — choose the oscillation norm

Use
\[
\|f\|_\vartheta
=
\max\left\{
\|f\|_\infty,\,
\max_n
\frac{\operatorname{osc}_{C_n}f}{\vartheta_n}
\right\}.
\]

Choose fixed positive rational/outward-enclosed weights \(\vartheta_n\).

Possible initialization:
- empirical TASK-0005 source oscillation profile;
- then inflate it by a safety factor;
- optimize by positive-operator iteration / linear programming if useful.

The proof must bound both:
1. the sup component;
2. the oscillation component divided by \(\vartheta_n\).

A reported scalar sup-only \(Z_1\) is insufficient.

## Stage C — rigorous inverse

Construct a rigorous interval enclosure of
\[
L_h^{-1}
\]
or a verified approximate inverse with an explicit Neumann defect.

The final proof must establish invertibility.

Then use
\[
B=L_h^{-1}\pi+(I-\pi).
\]

Record a rigorous bound on \(\|B\|_\vartheta\).

## Stage D — rigorous radii constants

For
\[
\mathcal H(f)
=
f-[g(\hat x+I^\alpha f)-g(\hat x)]+\rho,
\]
compute rigorously:

\[
Y_0\ge\|B\rho\|_\vartheta,
\]
\[
Z_0=0
\]
if \(A^\dagger=B^{-1}\) is used exactly,
\[
Z_1\ge
\|L_h^{-1}\pi K(I-\pi)+(I-\pi)K\|_\vartheta,
\]
and
\[
Z_2(r)
\]
for the nonlinear derivative remainder.

Use the exact Church–Queirolo radii polynomial convention from ROUND-0006.

Return an actual strict negative interval value of the radii polynomial.

### Mesh refinement

TASK-0005 indicates the tail-mesh part of \(Z_1\) should drop sharply when the coarse tail step is reduced.

Refine the late mesh first.

Only introduce degree \(>1\) if:
- \(Y_0\) becomes binding; or
- \(Z_1\) requires a higher-order interpolation remainder.

## Stage E — rigorous goal-oriented \(M_T\)

Do not derive the final \(M_T\) solely from a worst-case uniform state tube.

Using the validated source ball, rigorously bound the induced error in
\[
v_T(t)
=
E_\alpha(Jt^\alpha)u_0+
\int_0^T\Psi_J(t-s)N(u(s))\,ds.
\]

Use an adjoint/dual bound based on the same source-space inverse where possible.

Certify:
\[
M_T<M_{\rm threshold}
\]
for the B215 M1 constants.

Also certify the infinite post-cut supremum, not only a finite window.

## Stage F — close or stop

Success requires all of:

1. exact-rational entry into \(R_{\rm ext}\);
2. rigorous radii-polynomial validation of the history;
3. rigorous M1 constants;
4. rigorous
   \[
   M_T+K_JC_rr^2<r.
   \]

If achieved, state explicitly:

\[
\boxed{\text{B215 survival is CERTIFIED}}
\]

and provide every constant needed for Chief to promote TARGET-A20.

If the CAP fails, identify whether the obstruction is:
- source-space inverse conditioning;
- oscillation \(Z_1\);
- nonlinear \(Z_2\);
- residual \(Y_0\);
- goal-functional \(M_T\).

## Return

Write:
\`research/coordination/compute-to-chief/TASK-0006_rigorous-oscillation-cap_RETURN.md\`.

No numerical basin label counts as success.
