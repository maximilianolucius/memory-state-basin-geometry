# State Architecture and Current Theorem Program

**Owner:** Chief Researcher  
**Date:** 2026-09-29  
**Status:** VERIFIED ARCHITECTURE / EXTINCTION SIDE PROVED / SURVIVAL CONVERGENCE OPEN

## 1. Continuation-state architecture

For
\[
{}^C D_{0+}^{\alpha}x(t)=g(x(t);\mu),
\qquad 0<\alpha<1,
\]
use the Doan–Kloeden state space
\[
\mathfrak C=C(\mathbb R_+,\mathbb R^d)
\]
with compact-open topology.

The canonical physical embedding and present evaluation are
\[
\iota(x_0)(t)\equiv x_0,
\qquad
e_0(f)=f(0).
\]

Define
\[
\mathcal R_\alpha
=
\{T_t\iota(x_0):t\ge0,\ x_0\in X_{\rm phys}\},
\]
and
\[
\mathcal F_z=e_0^{-1}(z)\cap\mathcal R_\alpha.
\]

Principal statements remain restricted to physically reachable states.

## 2. Basin-entry architecture

The central criterion is no longer a two-advanced-orbit collision.

Let
\[
\iota(U_-)\subseteq\mathcal B(A_-).
\]

If
\[
\iota(p)\in\mathcal B(A_+),
\qquad A_+\neq A_-,
\]
and
\[
z=P(p,t_*)\in U_-,
\]
then
\[
T_{t_*}\iota(p),\ \iota(z)\in\mathcal F_z
\]
have distinct asymptotic fates.

This is STRUCTURAL-E1.

The second state is the canonical **cold start at the reached physical point**. Same-age collision, transversality and IFT are not required for existence.

## 3. Open persistence

STRUCTURAL-E2 shows that strict entry persists by continuity.

The only difficult persistence hypotheses are basin membership:
- persistence of the cold-start basin region;
- persistence of the survival-basin initial state.

## 4. Physical-to-memory-state bridge

STRUCTURAL-E3 proves:
\[
x(t;p)\to x^*,\quad g(x^*)=0
\Longrightarrow
T_t\iota(p)\to\iota(x^*)
\]
in compact-open topology.

Therefore a rigorous physical convergence theorem for a standard IVP is sufficient to classify its continuation-state basin.

A late physical near-hit is not enough; no restart argument is allowed.

## 5. Verified cold-start extinction region

For
\[
{}^C D^\alpha x=x(1-x)(x-\theta)-axy,
\]
\[
{}^C D^\alpha y=y(bx-m),
\]
with
\[
a,b,m>0,\quad0<\theta<1,\quad\theta<m/b,
\]
THEOREM-X1 proves
\[
R_{\rm ext}=\{0<x<\theta,\ y\ge0\}
\]
satisfies
\[
\iota(R_{\rm ext})
\subseteq
\mathcal B(\iota(0,0)).
\]

This is now closed from published viability, comparison, scalar-Allee and continuation results.

## 6. TASK-0001 witness

At
\[
\theta=0.3,\quad a=b=1,\quad m=0.8,\quad\alpha=0.85,
\]
the standard initial state
\[
p=(2.4372,2.012)
\]
has a strongly corroborated numerical orbit that enters \(R_{\rm ext}\) and later approaches
\[
E^*=(0.8,0.1).
\]

Entry is numerically robust but not yet interval-certified.

Physical convergence to \(E^*\) is not yet proved.

Thus TARGET-A20 remains CONJECTURED.

## 7. Novelty boundary after ROUND-0003

Known:
- ecological vector field at integer order: Ye et al. 2019;
- fixed-sign Caputo derivative does not imply monotonicity at one order: Diethelm 2016;
- fractional Double-Allee models and basin plots;
- hereditary headpoint/history effects;
- abstract E1 logic.

Search-qualified residual:
a rigorously established autonomous Caputo case in which
\[
\iota(z)\in\mathcal B(A_{\rm ext}),
\]
but another physically reachable continuation state
\[
\phi\in\mathcal F_z
\]
belongs to
\[
\mathcal B(A_{\rm surv}).
\]

## 8. Exact remaining gate

For one standard IVP \(p\), prove:
\[
x(t;p)\to E^*
\]
and certify:
\[
x(t_*;p)\in R_{\rm ext}.
\]

Then:
\[
\text{X1 + E3 + E1}
\Longrightarrow
\text{TARGET-A20}.
\]

## 9. Active work

- ROUND-0003: COMPLETE / ASSIMILATED.
- TASK-0002: ACTIVE.
- next web round: WAIT FOR TASK-0002 OR EXACT SURVIVAL THEOREM.
- manuscript: BLOCKED.
