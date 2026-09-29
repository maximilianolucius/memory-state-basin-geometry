# ROUND-0005 — Memory-tail resolvent survival audit

**From:** Chief Researcher  
**To:** Deep Web Search Agent  
**Date:** 2026-09-29  
**Priority:** P0 / PRINCIPAL SURVIVAL GATE

## Context

TASK-0003 proved O1: no forward-invariant physical-state survival certificate can produce the target threshold entry.

The new candidate theorem is
\`research/MEMORY_TAIL_SURVIVAL.md\`.

Audit this exact memory-dependent tail route. Do not reopen generic Lyapunov searches.

## Q1 — resolvent identity

For
\[
u=h+I^\alpha(Ju+N(u)),
\]
verify the matrix fractional variation-of-constants representation
\[
u(t)
=
\mathcal L_J h(t)
+
\int_0^t
s^{\alpha-1}E_{\alpha,\alpha}(Js^\alpha)
N(u(t-s))\,ds,
\]
with
\[
\mathcal L_Jh
=
h+
(J\Psi_J)*h.
\]

Extract exact assumptions for continuous \(h\), matrix \(J\), and locally Lipschitz \(N\).

## Q2 — \(L^1\) integrability of the matrix kernel

Audit when
\[
\Psi_J(t)=t^{\alpha-1}E_{\alpha,\alpha}(Jt^\alpha)
\]
belongs to
\[
L^1([0,\infty))
\]
in an induced matrix norm.

For Hurwitz \(J\), or more generally Matignon-stable \(J\), obtain:
- exact sector condition;
- large-\(t\) decay rate;
- references/theorem numbers;
- usable norm bounds or contour/asymptotic estimates.

## Q3 — inherited-memory input

For the actual standard Caputo trajectory and cut time \(T\),
\[
h_T(t)
=
p-E^*
+
\frac1{\Gamma(\alpha)}
\int_0^T
(t-s)^{\alpha-1}F(x(s))\,ds.
\]

Audit the theorem that this is the correct generalized Volterra input after splitting at \(T\).

Determine sufficient conditions under which the corresponding linear response
\[
v_T=\mathcal L_Jh_T
\]
satisfies
\[
v_T(t)\to0.
\]

Do not incorrectly require \(h_T(t)\to0\); it generally tends to \(p-E^*\).

## Q4 — audit CANDIDATE-M1

Audit:

If
\[
K_J=\int_0^\infty\|\Psi_J(s)\|\,ds<\infty,
\]
\[
\|N(u)\|\le C_r\|u\|^2\quad(\|u\|\le r),
\]
\[
M_T=\sup_{t\ge T}\|v_T(t)\|,
\qquad
v_T(t)\to0,
\]
and
\[
M_T+K_JC_rr^2<r,
\]
then the inherited continuation state converges to \(E^*\).

Required verdict:
- M1 VERIFIED;
- M1 NEEDS FIX;
- M1 INVALID.

Audit specifically the first-exit step and the limsup convolution argument.

## Q5 — direct prior

Search for published Caputo/Volterra results equivalent to:
- finite validated excursion;
- inherited-memory forcing after a cut time;
- resolvent-based nonlinear tail certification to a stable equilibrium.

Also search whether any source directly proves the project survival classification mechanism.

## Deliverables

Commit:
- \`research/coordination/web-to-chief/ROUND-0005_memory-tail-resolvent_RETURN.md\`;
- substantive report under \`research/web-search/\`;
- bibliography updates for formally published sources only.

No new generic search beyond this theorem.
