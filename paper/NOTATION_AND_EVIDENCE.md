# Notation and Evidence Map

**Status:** locked for manuscript v1

| Symbol | Meaning | Evidence/source |
|---|---|---|
| \(\mathfrak C\) | \(C(\mathbb R_+,\mathbb R^d)\), continuation-state space, compact-open topology | Doan--Kloeden |
| \(T_t\) | continuation-state semidynamical system | Doan--Kloeden |
| \(\iota(z)\) | canonical cold-start state, constant history/forcing state | background |
| \(e_0\) | present evaluation \(e_0(f)=f(0)\) | background |
| \(\mathcal R_\alpha\) | physically reachable continuation states | project definition |
| \(\mathcal F_z\) | reachable present-state fiber \(e_0^{-1}(z)\cap\mathcal R_\alpha\) | project definition |
| \(\mathcal B(A)\) | basin of invariant state/set \(A\) in continuation state space | standard |
| \(R_{\rm ext}\) | cold-start extinction strip \(0<x<\theta,\ y\ge0\) | X1 |
| \(E^*\) | positive coexistence equilibrium | exact algebra |
| \(J\) | Jacobian at \(E^*\) | exact algebra |
| \(\Psi_J(t)\) | \(t^{\alpha-1}E_{\alpha,\alpha}(Jt^\alpha)\) | resolvent theory |
| \(v_T\) | inherited linear-memory response after finite cut | exact variation of constants |
| \(M_T\) | \(\sup_{t\ge T}\|v_T(t)\|\) | certified bound |
| \(K_J\) | \(\int_0^\infty\|\Psi_J(s)\|ds\) | analytic + certified bound |
| \(C_r\) | quadratic remainder coefficient in chosen adapted norm | certified bound |
| \(I_*\) | certified threshold-entry time interval | TASK-0006 |

## Evidence classes used in manuscript

**ANALYTIC:** exact proof in manuscript.

**PUBLISHED PRIOR:** theorem imported from a formally published source; hypotheses checked explicitly.

**CERTIFIED COMPUTATION:** machine-assisted upper/lower enclosure with a declared arithmetic model.

**NUMERICAL CORROBORATION:** visual/diagnostic only; never used to prove a theorem.

## Main theorem dependency table

| Manuscript result | Dependencies | Evidence |
|---|---|---|
| Prop. 2.1 physical-to-continuation convergence | continuation-state formula | ANALYTIC |
| Prop. 2.2 basin-entry criterion | basin positive invariance | ANALYTIC |
| Thm. 3.1 scalar purity | no-crossing + interval basin classification | ANALYTIC/PUBLISHED PRIOR |
| Thm. 4.1 extinction strip | viability + scalar comparison + continuation | ANALYTIC/PUBLISHED PRIOR |
| Thm. 4.2 memory-tail survival | stable ML kernel + exact resolvent split | ANALYTIC/PUBLISHED PRIOR |
| finite B215 enclosure | CAP cellwise fixed point | CERTIFIED COMPUTATION |
| B215 convergence | finite history + M1 certified constants | ANALYTIC + CERTIFIED COMPUTATION |
| Thm. 5.1 main multibasin fiber | Prop. 2.1 + Prop. 2.2 + Thm. 4.1 + B215 convergence/entry | NEW THEOREM / CERTIFIED REALIZATION |

## Exact B215 constants to keep synchronized

\[
\alpha=\frac{17}{20},\quad
\theta=\frac12,\quad
a=\frac12,\quad
b=1,\quad
m=\frac45,
\]
\[
p=(277/100,467/1000),
\qquad
E^*=(4/5,3/25).
\]

Primary certificate:
\[
T=300,\quad N=12000,
\]
\[
I_*=[5.8576774143,13.7275388580],
\]
\[
\text{physical tube}\le2.2193\times10^{-4},
\]
\[
\kappa\le0.083612,
\]
\[
K_J\le11.3499043,
\quad
M_T\le0.043232414,
\]
\[
r=2221/20000,
\]
\[
r-K_JC_rr^2-M_T\ge0.0135626.
\]

Secondary redundant certificate:
\[
T=1000,\quad N=20000,
\]
\[
\kappa\le0.187495,
\qquad
M_T\le0.0154786,
\]
\[
\text{M1 margin}\ge0.0413364.
\]

## Referee-sensitive language

Until TASK-0007 completes, use:

> certified under the stated arithmetic model

and not:

> fully interval / end-to-end interval arithmetic.

Do not call \(I_*\) an interval of **distinct** fibers unless injectivity of \(t\mapsto x(t;p)\) is separately certified.
