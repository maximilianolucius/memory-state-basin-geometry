# ROUND-0004 — RETURN TO CHIEF

**Round ID:** ROUND-0004  
**Request:** `research/coordination/chief-to-web/ROUND-0004_local-survival-lyapunov_REQUEST.md`  
**Search date:** 2026-09-29  
**Agent:** Deep Web Search Agent  
**Final substantive evidence commit before this return:** `c4b9a63dbdad97a2d1ff45adaaea0eab4c12bd01`

## Required verdicts

- **Quadratic Caputo derivative inequality:** **VERIFIED**
- **Local Lyapunov implication:** **VERIFIED**
- **CANDIDATE-L1:** **VERIFIED**
- **Direct explicit-basin theorem for exact model:** **NOT FOUND**
- **Strict survival-entry novelty killer:** **NOT FOUND IN SEARCHED CORPUS**

## 1. Quadratic inequality — use Ren & Wu 2019

The older standard reference

**Águila-Camacho, Duarte-Mermoud & Gallegos (2014)**  
DOI `10.1016/j.cnsns.2014.01.022`

proves the scalar inequality
[
rac12,{}^CD^alpha x^2le x,{}^CD^alpha x
]
under the assumption that (x(t)) is continuous and differentiable.

That hypothesis is not safe as the sole load-bearing justification for a generic Caputo trajectory.

The correct source is:

**Ren, J.; Wu, C. (2019).**  
“Advances in Lyapunov Theory of Caputo Fractional-Order Systems.”  
*Nonlinear Dynamics* 97, 2521–2531.  
DOI `10.1007/s11071-019-05145-9`.

Their **Lemma 3.1** explicitly repairs the differentiability defect and proves, along an actual solution of a Caputo system under the source's continuity/(C^1)/growth hypotheses, for arbitrary positive-definite (P),
[
{}^CD^alpha(x^	op Px)
le
x^	op P({}^CD^alpha x)
+
({}^CD^alpha x)^	op Px.
]

For real (x) and symmetric (P),
[
oxed{
{}^CD^alpha(x^	op Px)
le
2x^	op P,{}^CD^alpha x.
}
]

The project vector field shifted about (E^*) is autonomous polynomial, hence satisfies the required local smoothness/growth conditions on every finite ball used in L1.

The source theorem covers (0<alpha<1), exactly the project regime.

### Verdict

**VERIFIED.**

**Chief action:** cite Ren–Wu 2019 Lemma 3.1 as load-bearing. Keep Águila-Camacho et al. 2014 only as historical background if desired.

## 2. Local Lyapunov implication

For a scalar Caputo comparison step use:

**Wu, C. (2020).**  
“A General Comparison Principle for Caputo Fractional-Order Ordinary Differential Equations.”  
*Fractals* 28(4), 2050070.  
DOI `10.1142/S0218348X2050070X`.

**Theorem 3.2** is sufficiently general for the required comparison.

Two useful consequences:

### Invariance

If
[
{}^CD^alpha V(t)le0,qquad V(0)=V_0,
]
comparison with the constant solution gives
[
V(t)le V_0.
]

This is the correct statement; it does not require claiming that (V(t)) is pointwise monotone.

### Convergence

If
[
{}^CD^alpha V(t)le-kappa V(t),qquad kappa>0,
]
then comparison with
[
w(t)=V_0E_alpha(-kappa t^alpha)
]
gives
[
0le V(t)le V_0E_alpha(-kappa t^alpha)	o0.
]

Hence a generic fractional LaSalle theorem is not needed for CANDIDATE-L1.

Modern supporting references are:

- **Wu (2021)**, *Nonlinear Dynamics* 105, 2473–2483, DOI `10.1007/s11071-021-06756-x`;
- **Wei, Cao, Chen & Wei (2022)**, *Applied Mathematics Letters* 129, 107961, DOI `10.1016/j.aml.2022.107961`.

Wei et al. is especially useful because it rigorously revisits/repairs the proof status of classical Caputo asymptotic-stability criteria.

### Verdict

**VERIFIED.**

## 3. Exact proof audit of CANDIDATE-L1

Let
[
{}^CD^alpha u=Ju+N(u),
qquad
V(u)=u^	op Pu,
]
where (J) is Hurwitz and
[
J^	op P+PJ=-I,
qquad P=P^	op>0.
]

Assume on (|u|_2le r),
[
|N(u)|_2le C_r|u|_2^2.
]

Ren–Wu gives
[
{}^CD^alpha V
le
2u^	op P(Ju+N(u)).
]

The linear term is exact:
[
2u^	op PJu
=
u^	op(J^	op P+PJ)u
=
-|u|_2^2.
]

The nonlinear term satisfies
[
2u^	op PN(u)
le
2|P|_2C_r|u|_2^3.
]

Therefore
[
{}^CD^alpha V
le
-left(1-2|P|_2C_r right)|u|_2^2.
]

Under the Chief's condition
[
2|P|_2C_r rlerac12,
]
we obtain
[
{}^CD^alpha V
le
-rac12|u|_2^2.
]

Since
[
Vlelambda_{max}(P)|u|_2^2,
]
this strengthens to
[
{}^CD^alpha V
le
-rac{1}{2lambda_{max}(P)}V.
	ag{L1}
]

Now assume
[
V(u_0)<lambda_{min}(P)r^2.
	ag{IC}
]

If a first exit from (|u|<r) existed, then on the interval up to that first exit, (L1) holds. Wu's scalar comparison theorem gives
[
V(u(t))
le
V(u_0)
E_alpha!left(
-rac{t^alpha}{2lambda_{max}(P)}
ight)
le
V(u_0)
<
lambda_{min}(P)r^2.
]

But at first exit, (|u|=r), so
[
V(u)gelambda_{min}(P)r^2,
]
a contradiction.

Thus the trajectory remains in the certified ball.

The already-audited Wu–Liu 2020 continuation theorem then gives global continuation because the trajectory is bounded, and the same Mittag–Leffler estimate implies
[
V(u(t))	o0,qquad u(t)	o0.
]

By project STRUCTURAL-E3,
[
T_tiota(z_0)	oiota(E^*)
]
in the compact-open continuation-state topology.

Therefore every standard initial state satisfying the L1 inequalities is rigorously in the survival basin.

### Constants

The Chief's (1/2) is conservative but correct.

More generally, for any (etain(0,1)),
[
2|P|C_r rle1-eta
]
gives
[
{}^CD^alpha V
le
-rac{eta}{lambda_{max}(P)}V.
]

The existing (1/2) choice is preferable for certified computation because it leaves a simple strict margin.

### Verdict

[
oxed{	ext{CANDIDATE-L1 VERIFIED}}
]

No correction of the theorem statement is required beyond source/regularity discipline.

## 4. Direct prior for the exact model

The targeted search did not locate a published theorem giving the **exact Caputo fractionalization** of the project strong-Allee predator–prey vector field an explicit local ellipsoidal basin radius of the L1 form.

Strong adjacent prior exists. In particular, **Ramesh et al. (2025)**, DOI `10.1371/journal.pone.0305179`, studies a different fractional predator–prey model with memory, Double Allee effect and Holling type-I response and uses Lyapunov methods for coexistence stability.

That does not subsume L1 for the project's exact vector field and does not supply the requested explicit quadratic certificate.

### Verdict

**DIRECT MODEL THEOREM PRIOR: NOT FOUND.**

## 5. Strict survival-entry novelty killer

The search targeted an exact conjunction:

1. a standard autonomous Caputo IVP is rigorously certified in a survival/coexistence basin;
2. the same orbit later enters a sub-Allee physical region;
3. the canonical cold start from the reached physical point is rigorously extinction-bound;
4. therefore the same current physical state supports two physically reachable memory states with different asymptotic fates.

No formally published result satisfying all four conditions was identified.

Hereditary/headpoint basin literature remains close conceptually but does not close this exact Caputo/reachability theorem.

### Verdict

**NOT FOUND IN SEARCHED CORPUS.**

This is search-qualified, not proof of absence.

## 6. Consequence for TARGET-A20

ROUND-0004 removes the last imported-theorem uncertainty from the preferred survival-classification route.

The remaining task is constructive/certification:

> find one exact-rational standard initial point (p) satisfying the verified L1 ellipsoid and certify that its actual Caputo trajectory later enters (R_{m ext}).

Then:

- L1 proves
  [
  iota(p)inmathcal B(E^*);
  ]
- X1 proves every canonical cold start in (R_{m ext}) lies in
  [
  mathcal B(0);
  ]
- TASK-0002-style validation proves actual entry;
- STRUCTURAL-E1 gives the multibasin reachable present-state fiber.

No long-time numerical classification is then required.

## 7. Bibliography/reference changes

Added verified published references:

- Águila-Camacho, Duarte-Mermoud & Gallegos 2014 — DOI `10.1016/j.cnsns.2014.01.022`;
- Ren & Wu 2019 — DOI `10.1007/s11071-019-05145-9`;
- Wu 2021 — DOI `10.1142/S0218348X21500924`;
- Wu 2021 — DOI `10.1007/s11071-021-06756-x`;
- Wei, Cao, Chen & Wei 2022 — DOI `10.1016/j.aml.2022.107961`.

Updated:

- `bibliography/references.bib`;
- `research/REFERENCES.md`;
- `research/LITERATURE_MAP.md`.

All added sources are formally published.

## 8. Files produced/modified

- `research/web-search/2026-09-29_ROUND-0004_local-survival-lyapunov_REPORT.md`;
- `research/coordination/web-to-chief/ROUND-0004_local-survival-lyapunov_RETURN.md`;
- `bibliography/references.bib`;
- `research/REFERENCES.md`;
- `research/LITERATURE_MAP.md`.

## 9. Recommended next search

Do not open another generic Lyapunov/basin round.

Wait for TASK-0003.

If TASK-0003 returns an L1-compatible certified witness, the next web round should be the **final theorem-specific novelty audit**, searching the exact:

- rational parameter vector;
- L1 radius/ellipsoid statement;
- certified threshold-entry statement;
- reachable multibasin-fiber conclusion;
- 2025–2026 direct competitors.

That is the proper pre-manuscript gate.
