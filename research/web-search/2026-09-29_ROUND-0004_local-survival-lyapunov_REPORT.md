# ROUND-0004 — Exact local-survival Lyapunov audit

**Agent:** Deep Web Search Agent  
**Search date:** 2026-09-29  
**Request:** `research/coordination/chief-to-web/ROUND-0004_local-survival-lyapunov_REQUEST.md`  
**Priority:** P0 / FINAL SURVIVAL-THEOREM GATE

## Executive verdict

| Item | Verdict | Reason |
|---|---|---|
| Quadratic Caputo derivative inequality | **VERIFIED** | Ren & Wu (2019), Lemma 3.1, proves the quadratic inequality directly along real Caputo solutions and repairs the differentiability defect of the older Águila-Camacho et al. lemma. |
| Local Lyapunov implication | **VERIFIED** | Scalar Caputo comparison yields invariant sublevel sets; in CANDIDATE-L1 the estimate strengthens to (D^alpha Vle-kappa V), so Mittag–Leffler comparison gives explicit convergence. |
| CANDIDATE-L1 | **VERIFIED** | The Chief's constants are conservative but correct. No change is needed except to cite the source-safe quadratic inequality and state continuation/global-existence dependence. |
| Direct explicit basin-radius theorem for exact model | **NOT FOUND** | Published fractional Allee predator–prey Lyapunov results were found, but not this exact Caputo vector field with the explicit quadratic ellipsoid/radius used by L1. |
| Strict survival-entry novelty killer | **NOT FOUND IN SEARCHED CORPUS** | No published theorem located combines a rigorously survival-classified standard Caputo IVP, later physical entry below an Allee cold-start threshold, and opposite fate of the canonical cold start at that same present state. |

The final theorem strategy is therefore source-supported: if TASK-0003 finds an exact-rational standard initial point satisfying L1 and the validated integrator certifies its later entry into (R_{m ext}), the survival half and hence TARGET-A20 can be closed without a long-time numerical basin classifier.

---

# 1. Q1 — Quadratic Caputo derivative inequality

## 1.1 Historical source is not sufficient by itself

**Águila-Camacho, Duarte-Mermoud & Gallegos (2014)**, “Lyapunov functions for fractional order systems,” *Communications in Nonlinear Science and Numerical Simulation* 19(9), 2951–2957, DOI **10.1016/j.cnsns.2014.01.022**.

Their Lemma 1 proves, for a real continuous and differentiable scalar function (x(t)),
[
rac12,{}^C D^alpha x(t)^2
le
x(t),{}^C D^alpha x(t),
qquad 0<alpha<1.
]

The paper then uses quadratic Lyapunov functions in vector examples.

However, this is **not** the best load-bearing source for the present project because Caputo solutions need not be differentiable at the lower terminal even for analytic vector fields.

## 1.2 Correct load-bearing source: Ren & Wu 2019

**Ren, J.; Wu, C. (2019)**, “Advances in Lyapunov theory of Caputo fractional-order systems,” *Nonlinear Dynamics* 97, 2521–2531, DOI **10.1007/s11071-019-05145-9**.

The paper explicitly identifies the differentiability problem in the older widely used lemma and replaces it by an estimate valid along actual Caputo solutions.

### Lemma 3.1

For the Caputo system
[
{}^C_0D_t^alpha x=f(t,x),qquad x(0)=x_0,qquad 0<alpha<1,
]
under the regularity/growth hypotheses stated in that lemma (continuity in ((t,x)), (C^1) regularity away from (t=0), and controlled first derivatives), if (P) is any positive definite (n	imes n) matrix, then along the real solution
[
{}^C_0D_t^alpha!left[x(t)^	op P x(t)ight]
le
x(t)^	op P,{}^C_0D_t^alpha x(t)
+
left[{}^C_0D_t^alpha x(t)ight]^	op P x(t).
]

For real (x) and symmetric (P),
[
oxed{
{}^C D^alpha(x^	op P x)
le
2x^	op P,{}^C D^alpha x.
}
]

### Applicability to the project model

The shifted project field (umapsto F(E^*+u)) is autonomous and polynomial. Therefore:

- it is continuous everywhere;
- it is (C^infty) in (u);
- the time derivative required in the nonautonomous source hypotheses is zero;
- its first spatial derivatives have polynomial growth and are locally bounded on every ball used by L1.

Thus the source conditions are satisfied on the local domain relevant to the theorem.

### Boundary/order scope

The source estimate is stated for
[
0<alpha<1.
]
That is exactly the project regime. At (alpha=1), the classical chain rule gives equality separately.

### Q1 verdict

**VERIFIED.**

**Citation discipline:** use Ren–Wu 2019 Lemma 3.1 as the load-bearing quadratic estimate. Águila-Camacho et al. 2014 may be cited historically, but should not carry the proof.

---

# 2. Q2 — Local Lyapunov implication

## 2.1 Scalar comparison needed for invariance

**Wu (2020)**, “A general comparison principle for Caputo fractional-order ordinary differential equations,” *Fractals* 28(4), 2050070, DOI **10.1142/S0218348X2050070X**.

Theorem 3.2 gives a very general scalar comparison principle. In particular, if
[
{}^C D^alpha m(t)le g(t,m(t))
]
and the Caputo derivative is continuous, then (m(t)) is bounded above by the maximal solution of the corresponding scalar comparison equation with the ordered initial value.

For invariance of a Lyapunov sublevel, (gequiv0) can be used: if
[
{}^C D^alpha V(t)le0,qquad V(0)=V_0,
]
then comparison with the constant scalar solution (w(t)equiv V_0) gives
[
V(t)le V_0.
]

This is the correct fractional statement. It does **not** require claiming that (V(t)) is pointwise monotone.

## 2.2 Asymptotic convergence

A generic negative-definite fractional Lyapunov implication is available in the published literature, but its proof history requires care.

Useful current sources:

- **Wu (2021)**, “A complete result on the Lyapunov stability of Caputo fractional order nonautonomous systems by the comparison method,” *Nonlinear Dynamics* 105, 2473–2483, DOI **10.1007/s11071-021-06756-x**.
- **Wei, Cao, Chen & Wei (2022)**, “The proof of Lyapunov asymptotic stability theorems for Caputo fractional order systems,” *Applied Mathematics Letters* 129, 107961, DOI **10.1016/j.aml.2022.107961**.

Wei et al. explicitly revisit earlier Caputo Lyapunov asymptotic-stability criteria whose published proofs had been criticized and provide rigorous proofs of the standard sufficient conditions.

For CANDIDATE-L1, however, the Chief can avoid relying on the broadest abstract theorem because the derived inequality is stronger:
[
{}^C D^alpha V
le
-rac12|u|^2.
]
Since
[
V=u^	op Pulelambda_{max}(P)|u|^2,
]
we have
[
|u|^2gerac{V}{lambda_{max}(P)},
]
hence
[
{}^C D^alpha V
le
-kappa V,
qquad
kappa=rac{1}{2lambda_{max}(P)}.
]

Scalar comparison with
[
{}^C D^alpha w=-kappa w,qquad w(0)=V(u_0),
]
gives explicitly
[
0le V(u(t))
le
V(u_0)E_alpha(-kappa t^alpha)
	o0.
]

Thus
[
u(t)	o0.
]

### Q2 verdict

**VERIFIED.**

For the actual L1 proof, use the direct Mittag–Leffler scalar comparison. It gives both a clean source chain and an explicit decay estimate.

---

# 3. Q3 — Exact audit of CANDIDATE-L1

Consider
[
{}^C D^alpha u=Ju+N(u),
]
where (J) is Hurwitz and (P=P^	op>0) solves
[
J^	op P+PJ=-I.
]

Let
[
V(u)=u^	op Pu.
]

Assume
[
|N(u)|_2le C_r|u|_2^2
qquad(|u|_2le r).
]

By Ren–Wu 2019,
[
{}^C D^alpha V
le
2u^	op P(Ju+N(u)).
]

Because
[
2u^	op PJu
=
u^	op(J^	op P+PJ)u
=
-|u|_2^2,
]
and
[
2u^	op PN(u)
le
2|P|_2,|u|_2,|N(u)|_2
le
2|P|_2 C_r|u|_2^3,
]
we obtain inside the radius-(r) ball
[
{}^C D^alpha V
le
-left(1-2|P|_2C_r right)|u|_2^2.
]

The Chief assumes
[
2|P|_2C_r rlerac12.
]
Therefore
[
{}^C D^alpha V
le
-rac12|u|_2^2
le
-rac{1}{2lambda_{max}(P)}V.
	ag{L1-decay}
]

## 3.1 Invariance of the ball

Assume
[
V(u_0)<lambda_{min}(P)r^2.
	ag{L1-init}
]

This implies
[
|u_0|_2<r.
]

Suppose a first exit time (t_e) from the closed radius-(r) ball existed. On ([0,t_e]), (L1-decay) is valid. Scalar comparison yields
[
V(u(t))
le
V(u_0)E_alpha(-kappa t^alpha)
le
V(u_0)
<
lambda_{min}(P)r^2.
]

But at first exit,
[
|u(t_e)|_2=r
quadLongrightarrowquad
V(u(t_e))gelambda_{min}(P)r^2,
]
a contradiction.

Thus the trajectory never exits the ball.

## 3.2 Global continuation

Inside that invariant ball the trajectory is bounded and the polynomial vector field is locally Lipschitz.

The already-audited Caputo continuation result of Wu & Liu (2020), DOI **10.1515/fca-2020-0029**, rules out finite-time termination while the state remains bounded.

Hence the standard solution is global.

## 3.3 Convergence

The comparison estimate holds for all (tge0):
[
V(u(t))
le
V(u_0)E_alpha(-kappa t^alpha)
	o0.
]
Since
[
V(u)gelambda_{min}(P)|u|_2^2,
]
we conclude
[
u(t)	o0,
qquad
z(t)	o E^*.
]

By STRUCTURAL-E3 already proved in the project,
[
T_tiota(z_0)	oiota(E^*)
]
in compact-open topology, so the standard initial point belongs to the survival basin in the actual Doan–Kloeden continuation-state system.

## 3.4 Constants

The Chief's constant (1/2) is sufficient but not sharp.

A more general version is: for any (etain(0,1)), if
[
2|P|_2C_r rle1-eta,
]
then
[
{}^C D^alpha V
le
-rac{eta}{lambda_{max}(P)}V.
]

The current choice corresponds to (eta=1/2) and is convenient for certification.

Strict inequality in (L1-init) is recommended because it removes the boundary/equality case from the first-exit argument.

### Q3 verdict

[
oxed{	ext{CANDIDATE-L1 VERIFIED}}
]

No mathematical weakening or correction is necessary. The proof should simply use the source-safe Ren–Wu quadratic inequality and state the continuation dependency.

---

# 4. Q4 — Direct model prior and novelty killer

## 4.1 Exact-model explicit ellipsoidal basin certificate

ROUND-0003 already found the exact integer-order ecological vector field in Ye et al. 2019.

The present search targeted the exact Caputo fractionalization and phrases including:

- quadratic Lyapunov basin radius;
- explicit ellipsoidal region of attraction;
- local basin estimate;
- strong-Allee Caputo predator–prey;
- Lotka–Volterra/Holling-I predation with strong Allee;
- Lyapunov region/basin of coexistence.

No published source was located that gives the exact project Caputo system an explicit local ellipsoidal basin certificate of the L1 form.

### Strong adjacent prior

**Ramesh et al. (2025)**, *PLOS ONE* 20, e0305179, DOI **10.1371/journal.pone.0305179**, studies a different fractional predator–prey model with memory, Double Allee effect and Holling type-I response. It uses Lyapunov arguments for stability of the positive equilibrium.

This is relevant applied prior for “fractional Allee predator–prey + Lyapunov coexistence stability,” but the equations differ and it does not supply the exact quadratic radius certificate requested here.

### Direct-model theorem prior verdict

**NOT FOUND.**

## 4.2 Strict survival-entry novelty killer

The search specifically targeted the conjunction:

1. a standard Caputo IVP is rigorously in a survival/coexistence basin;
2. its later physical trajectory enters a region below an Allee threshold;
3. the standard cold start from that same physical point is rigorously extinction-bound;
4. hence equal current physical state with different reachable memory has opposite asymptotic fate.

No formally published theorem or model example satisfying this full conjunction was identified.

The closest inherited hereditary analogue remains Szaksz–Stepan–Habib 2024 for headpoint/history-dependent basin geometry, but it does not satisfy the strict Caputo/reachability/extinction-survival criterion.

### Strict novelty-killer verdict

**NOT FOUND IN SEARCHED CORPUS.**

This is a search-qualified statement, not proof of absence.

---

# 5. Exact source chain recommended for the paper

For the local survival theorem, the cleanest dependency chain is:

1. **Ren & Wu 2019, Lemma 3.1** — valid quadratic Caputo derivative inequality along real solutions.
2. Classical Lyapunov matrix theorem — Hurwitz (JRightarrow) unique (P>0) for (J^	op P+PJ=-I).
3. Exact/local algebra — certify (C_r) and the smallness inequality.
4. **Wu 2020, Theorem 3.2** — compare (V) with the Mittag–Leffler scalar solution.
5. **Wu & Liu 2020** — bounded trajectory implies continuation/global existence in the required Caputo setting.
6. Project STRUCTURAL-E3 — physical convergence lifts to compact-open continuation-state convergence.

Wei et al. 2022 and Wu 2021 are useful reference-level support for the general asymptotic-Lyapunov framework, but the L1 proof does not need to hide behind a generic theorem.

---

# 6. Novelty boundary after ROUND-0004

Not new:

- quadratic Lyapunov inequalities for Caputo systems;
- fractional Lyapunov direct/comparison methods;
- explicit local region-of-attraction estimates as a general technique;
- Allee predator–prey equilibrium stability;
- fractional Allee predator–prey Lyapunov analysis;
- the abstract E1 basin-entry implication.

Residual that survives this round:

> construct/certify, in the exact autonomous Caputo strong-Allee model, a standard initial point that lies inside the rigorous L1 survival ellipsoid and whose actual trajectory later enters the already-proved cold-start extinction strip; then infer a physically reachable present-state fiber containing both survival- and extinction-basin states.

This is now a sharply testable theorem statement.

---

# 7. Bibliography actions

Verified published additions recommended:

- Águila-Camacho, Duarte-Mermoud & Gallegos 2014 — DOI 10.1016/j.cnsns.2014.01.022 (historical; not load-bearing).
- Ren & Wu 2019 — DOI 10.1007/s11071-019-05145-9 (load-bearing quadratic inequality).
- Wu 2021 — DOI 10.1142/S0218348X21500924.
- Wu 2021 — DOI 10.1007/s11071-021-06756-x.
- Wei, Cao, Chen & Wei 2022 — DOI 10.1016/j.aml.2022.107961.

No unpublished source is required by the L1 proof.

---

# 8. Negative-search limitations

- Failure to locate the exact ellipsoidal certificate or survival-entry theorem is not proof of absence.
- Older fractional control literature contains many quadratic Lyapunov estimates; only sources whose assumptions could be verified against the project theorem were treated as load-bearing.
- The exact final theorem should receive one more hostile search after TASK-0003 fixes the parameter point, exact rational radius, (P), (C_r), and certified entry interval.
