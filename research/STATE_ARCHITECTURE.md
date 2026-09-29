# State Architecture and Theorem Program

**Owner:** Chief Researcher  
**Date:** 2026-09-29  
**Status:** VERIFIED BASELINE / POSITIVE WITNESS FOUND NUMERICALLY / BASIN CLOSURE OPEN

## 1. Governing architecture

For
\[
{}^C D_{0+}^{\alpha}x(t)=g(x(t);\mu),
\qquad 0<\alpha<1,
\]
use the Doan–Kloeden continuation-state space
\[
\mathfrak C=C(\mathbb R_+,\mathbb R^d)
\]
with compact-open topology.

The canonical physical embedding and present evaluation are
\[
\iota(x_0)(t)\equiv x_0,\qquad e_0(f)=f(0).
\]

The physically reachable set and present-state fiber are
\[
\mathcal R_\alpha=
\{T_t\iota(x_0):t\ge0,\ x_0\in X_{\rm phys}\},
\]
\[
\mathcal F_z=e_0^{-1}(z)\cap\mathcal R_\alpha.
\]

Basins are positively invariant under the continuation semigroup.

## 2. Old collision reduction

The general implication
\[
P(p,t)=P(q,s)=z,\quad
\iota(p)\in\mathcal B(A_1),\quad
\iota(q)\in\mathcal B(A_2)
\]
implies a multibasin \(\mathcal F_z\).

This remains correct but is no longer the most efficient formulation.

## 3. Principal reduction after TASK-0001 — basin entry

Let \(U_-\subset X_{\rm phys}\) satisfy
\[
\iota(U_-)\subseteq\mathcal B(A_-).
\]

If a standard initial state \(p\) satisfies
\[
\iota(p)\in\mathcal B(A_+),\qquad A_+\neq A_-,
\]
and its orbit enters
\[
z=P(p,t_*)\in U_-,
\]
then
\[
T_{t_*}\iota(p),\ \iota(z)\in\mathcal F_z
\]
belong to different basins.

This is THEOREM E1 in \`research/STRUCTURAL_THEOREMS.md\`.

### Key consequence

The second reachable state can be the **cold start at the reached physical state**:
\[
s=0,\qquad q=z.
\]

Therefore:
- no same-age collision is required;
- no nonlinear root problem is required;
- no transversality/IFT hypothesis is required for existence.

The scientific object is the mismatch between:
1. the continuation state carrying prehistory;
2. the canonical constant state with the same present physical value.

## 4. Open persistence

Entry into an open physical basin region is an open finite-horizon condition under continuous solution dependence.

Hence parameter persistence of the **entry event** is easy.

The hard part is persistence of:
- \(\iota(U_-)\subseteq\mathcal B_\mu(A_-(\mu))\);
- \(\iota(p)\in\mathcal B_\mu(A_+(\mu))\).

This is THEOREM E2.

The old CANDIDATE-M2 transversality program is demoted to a secondary geometry question.

## 5. Cold-start extinction strip

For the project-constructed strong-Allee predator–prey system
\[
{}^C D^\alpha x=x(1-x)(x-\theta)-axy,
\]
\[
{}^C D^\alpha y=y(bx-m),
\]
the candidate cold-start basin region is
\[
R_{\rm ext}=\{0<x<\theta,\ y\ge0\}.
\]

Under positivity, the audited comparison principle and
\[
\theta<m/b,
\]
the proof in \`research/EXTINCTION_STRIP.md\` gives
\[
\iota(R_{\rm ext})\subseteq\mathcal B((0,0)).
\]

Status:
**proof draft complete; source/hypothesis audit pending ROUND-0003.**

## 6. TASK-0001 witness

At
\[
\theta=0.3,\ a=b=1,\ m=0.8,\ \alpha=0.85,
\]
the standard initial state
\[
p=(2.4372,2.012)
\]
has a numerically survival-bound orbit that penetrates \(R_{\rm ext}\) by about \(0.103\) in prey coordinate and later recovers.

Evidence:
- three full-history solvers;
- fine-mesh agreement;
- horizon ladder;
- 30-digit recomputation;
- broad parameter/order scan.

Classification:
**NUMERICAL CORROBORATION**, not theorem.

If the survival basin membership is proved and X1 is audited, E1 immediately promotes every reached state on the sub-threshold arc to a rigorous multibasin fiber.

## 7. Caputo-specific mechanism

For the model,
\[
0<x<\theta,\ y\ge0
\Longrightarrow
{}^C D^\alpha x<0.
\]

At integer order this makes \(x\) locally decreasing and prevents recovery across the threshold.

For \(0<\alpha<1\), a continuation state can carry prior contributions from the fixed lower terminal, and the sign of the Caputo derivative on a later subinterval does not determine local monotonicity.

TASK-0001 exhibits:
\[
{}^C D^\alpha x<0
\]
while \(x(t)\) rises back through \(\theta\).

The literature status of this mechanism is being audited in ROUND-0003.

## 8. Current theorem bottleneck

The principal remaining burden is **survival-side basin proof**.

The project needs either:
- a continuation-state trapping neighborhood for the coexistence equilibrium;
- a Lyapunov/LaSalle basin certificate;
- a published model with an already rigorous survival basin;
- or another analytic argument placing a standard initial state in \(\mathcal B(A_{\rm surv})\).

Finite-horizon convergence plots are not sufficient.

## 9. Active tasks

- TASK-0001: COMPLETE / MERGED.
- ROUND-0003: exact model + mechanism + basin-closure audit.
- TASK-0002: validated entry enclosure + near-equilibrium witness search.
- manuscript: BLOCKED.
