# ROUND-0002 — Scalar/triangular fiber-purity theorem audit

**Agent:** Deep Web Search Agent  
**Search date:** 2026-09-29  
**Request:** `research/coordination/chief-to-web/ROUND-0002_scalar-triangular-purity_REQUEST.md`  
**Priority:** P0 / PURITY GATE

## Executive verdict

| Question | Verdict | Main reason |
|---|---|---|
| S1 imported scalar nonintersection hypotheses | **NEEDS FIX** | Cong–Tuan gives exactly the strict global separation needed, but under an explicit global-in-state Lipschitz condition. Diethelm–Ford 2012 must not be the load-bearing proof because Cong–Tuan explicitly identifies its proof as incomplete. |
| S1 novelty status | **STANDARD CONSEQUENCE** | The reachable-fiber conclusion is a short consequence of scalar separation, intervalwise asymptotic classification, and positive basin invariance. Doan–Kloeden 2022 already supplies the intervalwise scalar attractor classification for a broad dissipative/simple-zero class. |
| Scalar strong-Allee instantiation | **FOUND RIGOROUSLY** | Area–Nieto 2023 supplies an exact Caputo Allee cubic; Doan–Kloeden 2022 supplies a published general theorem that rigorously gives the below-threshold extinction / above-threshold survival partition for that cubic. |
| Triangular extension | **USEFUL COMPLETENESS** | Cong–Tuan proves nonintersection/nonlocal dynamics for triangular Caputo systems, and Doan–Kloeden 2022 proves a strong attractor theorem for a special product-triangular class. The Chief's broader "closed scalar coordinate determines full basin" fiber-purity corollary is not directly located, but is not principal novelty. |
| Monotone/comparison extension | **EXTRA CONDITIONS REQUIRED** | Wu 2020/2023 and Cheng–Wu 2026 give scalar/system comparison machinery for ordered solutions; they do not make basin membership a function of the endpoint (e_0). Equal endpoint does not imply ordered memory histories. |

## 1. Search coverage

Targeted searches were run for:

1. scalar Caputo trajectory separation/nonintersection;
2. exact hypotheses and proof status of Cong–Tuan 2017 and Diethelm–Ford 2012;
3. scalar autonomous Caputo attractors with multiple simple equilibria;
4. Caputo strong/Allee single-species models with exact global threshold behavior;
5. triangular/cascade Caputo attractors and nonlocal flows;
6. scalar and multidimensional Caputo comparison principles;
7. endpoint/headpoint/history-to-basin factorization;
8. 2025–2026 comparison-principle updates relevant to order-preserving systems.

No broad "memory-state basin geometry" search was repeated.

---

# Q1 — Exact scalar nonintersection hypothesis audit

## 2. Cong–Tuan 2017 is the correct load-bearing separation source

**N. D. Cong; H. T. Tuan.** "Generation of Nonlocal Fractional Dynamical Systems by Fractional Differential Equations." *Journal of Integral Equations and Applications* 29(4), 585–608 (2017). DOI **10.1216/JIE-2017-29-4-585**. **PUBLISHED.**

They consider, for (0<\alpha<1),
[
{}^C D_{0+}^{\alpha}x(t)=f(t,x(t)),
]
on either
[
J=[0,T] quad	ext{or}quad J=[0,\infty).
]

A continuous (x:J\to\mathbb R) is a solution when it satisfies the Caputo equation on (J\setminus\{0\}), equivalently the associated Volterra integral equation with the prescribed initial value.

### Exact scalar hypothesis

In Section 3.1 they assume (f:J\times\mathbb R\to\mathbb R) is continuous and that there exists a continuous nonnegative (L:J\to\mathbb R_+) such that
[
|f(t,x)-f(t,y)|\le L(t)|x-y|,
qquad
t\in J,;x,y\in\mathbb R.
	ag{CT-Lip}
]

Under this hypothesis the IVP has a unique solution on the whole declared interval (J).

### Exact separation result

**Theorem 4 ("Different trajectories do not meet")** in the author/full-text version, Section 3.1, p. 6 of the manuscript PDF:

if (x_{10}\neq x_{20}), then the corresponding solutions satisfy
[
x_1(t)\neq x_2(t)
qquad\forall t\in J.
]

More strongly, the proof shows that
[
x_{10}<x_{20}
quad\Longrightarrowquad
x_1(t)<x_2(t)
qquad\forall t\in J.
]

Thus the result is **strict order preservation**, not merely non-equality.

The same paper subsequently proves a quantitative lower separation bound in terms of a Mittag–Leffler factor.

### Equilibrium barriers

For the autonomous equation
[
{}^C D_{0+}^{\alpha}x=g(x),
]
if (g(c)=0), then (x(t)\equiv c) is the equilibrium solution. Applying strict separation to (x_0<c) versus (c), or (x_0>c) versus (c), yields
[
x_0<c \Rightarrow x(t)<c,qquad
x_0>c \Rightarrow x(t)>c,
]
throughout (J).

At equality (x_0=c), uniqueness gives the stationary equilibrium trajectory.

Hence, under the exact Cong–Tuan hypotheses, equilibrium solutions are valid noncrossable barriers exactly as needed by S1-H1/S1-H3.

## 3. Important correction: Diethelm–Ford 2012 is not safe as proof source

**K. Diethelm; N. J. Ford.** "Volterra Integral Equations and Fractional Calculus: Do Neighboring Solutions Intersect?" *Journal of Integral Equations and Applications* 24(1), 25–37 (2012). DOI **10.1216/JIE-2012-24-1-25**. **PUBLISHED.**

Diethelm–Ford state separation/nonintersection results, including their Theorem 4.1. However, Cong–Tuan 2017 explicitly analyze the argument and state that the proof of Diethelm–Ford Theorem 3.1 is incomplete, and therefore so is Theorem 4.1. The issue is precisely nonlocality: the backward-in-time subinterval argument treats a terminal-value construction as though the relevant forcing were independent of the future segment, which is not justified for a history-dependent equation.

**Audit consequence:** retain Diethelm–Ford as historical background only; use Cong–Tuan 2017 for the rigorous separation theorem.

## 4. Why S1 needs a hypothesis fix

The current S1 statement wisely makes nonintersection an explicit hypothesis. That abstract theorem is fine.

But if the manuscript says that Cong–Tuan automatically verifies S1-H1 for a generic autonomous scalar (g), it must add the source's actual condition: global-in-state Lipschitz continuity (with continuous time-dependent Lipschitz bound in the nonautonomous formulation), or provide a separate localization/extension argument that stays inside a bounded invariant interval.

This matters for Allee cubics: a cubic vector field is not globally Lipschitz on all of (mathbb R).

Therefore the imported-theorem audit verdict is:

> **NEEDS FIX** — not because S1 is false, but because the exact source hypothesis must be stated and the cubic Allee specialization should use the stronger dissipative scalar theorem below rather than pretending the cubic satisfies global Lipschitz on all (mathbb R).

---

# Q2 — Prior and novelty status of Proposition S1

## 5. Stronger scalar asymptotic prior: Doan–Kloeden 2022

**Thai Son Doan; Peter E. Kloeden.** "Attractors of Caputo Fractional Differential Equations with Triangular Vector Fields." *Fractional Calculus and Applied Analysis* 25(2), 720–734 (2022). DOI **10.1007/s13540-022-00030-6**. **PUBLISHED.**

For the scalar autonomous Caputo equation
[
{}^C D_{0+}^{\alpha}x(t)=g(x(t)),qquad 0<\alpha<1,
]
they assume:

**(H1) dissipativity:** there exist (a,b>0) such that
[
g(x)x\le a-bx^2
qquad\forall x\in\mathbb R;
]

**(H2) nondegenerate equilibria:** (g\in C^1(\mathbb R)) and
[
g'(x)\neq0
qquad\forall x\in N(g):=\{x:g(x)=0\}.
]

These assumptions imply finitely many simple zeros
[
x_1<\cdots<x_{2k+1}
]
with alternating vector-field sign.

### Theorem 2.2

Their Theorem 2.2 proves:

1. the global attractor is
   [
   [\min N(g),\max N(g)];
   ]
2. every solution converges to an equilibrium in (N(g));
3. the convergence rate is (t^{-\alpha});
4. successive equilibria are joined by heteroclinic trajectories in the nonlocal dynamical-system sense.

### Proposition 2.4 — the key basin partition

The proof machinery gives the sharper interval classification. In their notation, initial data on each interval between adjacent zeros converge to the stable endpoint selected by the sign pattern. In particular, the asymptotic limit is constant on each equilibrium-separated interval.

This is essentially S1-H2 for a large, mathematically natural scalar class.

## 6. Novelty status of S1

No published source was located that formulates the exact statement in the Chief's modern language:
[
\mathcal F_x=e_0^{-1}(x)\cap\mathcal R_\alpha
]
is basin-pure for every (x), with (mathcal R_\alpha) the physically reachable Doan–Kloeden continuation-state set.

However, once one combines:

- strict scalar nonintersection / equilibrium barriers;
- intervalwise asymptotic classification;
- positive invariance of basins under the continuation-state semigroup;

the reachable-fiber conclusion follows in a few lines.

The fiber formulation is therefore useful for the project's dichotomy/minimal-dimension narrative, but it is not a defensible principal novelty claim.

### Q2 verdict

**STANDARD CONSEQUENCE.**

Recommended contribution label: **COMPLETENESS RESULT / IMPOSSIBILITY COROLLARY**, not NEW THEOREM.

---

# Q3 — Rigorous scalar strong-Allee specialization

## 7. Clean published Caputo Allee model

**Iván Area; Juan J. Nieto.** "On the Fractional Allee Logistic Equation in the Caputo Sense." *Examples and Counterexamples* 4 (2023), 100121. DOI **10.1016/j.exco.2023.100121**. **PUBLISHED.**

The model is the Caputo fractional Allee logistic equation
[
{}^C D_{0+}^{\alpha}x
=
x(1-x)(x-\theta),
qquad 0<\theta<1,quad 0<\alpha<1.
	ag{A}
]

The paper itself is primarily concerned with formal power-series construction and numerical comparison; it is not the best source for the global basin theorem.

But equation (A) lies directly in the Doan–Kloeden 2022 scalar class.

Let
[
g(x)=x(1-x)(x-\theta)
=-x^3+(1+\theta)x^2-\theta x.
]

Then:

- (g\in C^1(\mathbb R));
- (xg(x)) has leading term (-x^4), so the dissipativity inequality
  [
  xg(x)\le a-bx^2
  ]
  holds for suitable (a,b>0);
- the equilibria (0,\theta,1) are simple:
  [
  g'(0)=-\theta<0,qquad
  g'(\theta)=\theta(1-\theta)>0,qquad
  g'(1)=\theta-1<0.
  ]

Therefore Doan–Kloeden Theorem 2.2 / Proposition 2.4 applies and gives the rigorous asymptotic partition:

[
0<x_0<\theta
\Longrightarrow
x(t;x_0)\to0,
]
[
\theta<x_0<1
\Longrightarrow
x(t;x_0)\to1,
]
and for (x_0>1), the dissipative sign pattern sends the solution to (1).

The threshold (x=\theta) is a stationary unstable equilibrium, while (0) and (1) are stationary stable equilibria in the scalar phase portrait.

Combining this published interval classification with the scalar noncrossing/barrier property yields exactly the S1 strong-Allee fiber-purity corollary:
[
0<x<\theta
\Longrightarrow
\mathcal F_x\subseteq\mathcal B(0),
]
[
x>\theta
\Longrightarrow
\mathcal F_x\subseteq\mathcal B(1)
]
on the positive physical domain, with the separator fiber at (x=\theta) consisting of the stationary lift.

### Q3 verdict

**FOUND RIGOROUSLY.**

Important wording: the rigorous threshold conclusion is obtained by combining the **published exact Area–Nieto model** with the **published general Doan–Kloeden attractor theorem**. It should not be attributed as a theorem proved by Area–Nieto themselves.

## 8. Other Allee papers checked

**Kalra & Malhotra (2024)**, "Modeling and Analysis of Fractional Order Logistic Equation Incorporating Additive Allee Effect," *Contemporary Mathematics* 5(1), 380–401, DOI **10.37256/cm.5120243183**, is a published Caputo Allee model and useful contextual reference. Its extinction/survival threshold exposition relies materially on numerical simulation, so it should not be the load-bearing proof source for S1.

An older Allee fractional model by Abbas et al. (2011) uses a Riemann–Liouville formulation, not the target Caputo class, and is therefore not selected as the S1 specialization.

---

# Q4 — Triangular extension

## 9. Cong–Tuan triangular nonintersection

Cong–Tuan 2017 also treats triangular systems
[
{}^C D^\alpha x_1=f_1(t,x_1),
]
[
{}^C D^\alpha x_2=f_2(t,x_1,x_2),
quad\ldots
]
under a global Lipschitz condition in the state variables.

Their triangular results propagate strict coordinatewise separation recursively and construct a nonlocal two-parameter flow for the triangular system.

This shows that triangularity is a genuine structural class where finite-dimensional physical trajectory collision is strongly restricted.

## 10. Doan–Kloeden 2022 triangular attractors

Doan–Kloeden 2022 prove an attractor theorem for a **special product-triangular class** whose coordinates have the form
[
g_i(x_1,\ldots,x_i)
=
h_i(x_1,\ldots,x_{i-1})f_i(x_i),
]
with the multiplier (h_i) nonvanishing/positive under their hypotheses and with scalar factors satisfying the corresponding dissipativity and simple-zero assumptions.

Their **Theorem 3.1** gives a Cartesian-product global attractor and convergence of every solution to a Cartesian product of scalar equilibrium sets.

This is substantial direct prior for a triangular purity program.

Crucially, the paper itself notes that more general triangular systems of the form
[
{}^C D^\alpha x=f(x),qquad
{}^C D^\alpha y=g(x,y)
]
lose the special sign-product structure; their full attractor description does not automatically extend.

## 11. Status of the Chief's P2 formulation

The Chief's proposed safe theorem says:

> if a closed scalar coordinate has an audited separator theorem **and** that scalar interval determines the full-system asymptotic basin, then equality of the full present state forces equality of that basin-determining coordinate and hence the reachable fiber is pure.

The implication is mathematically sound and useful as a completeness corollary. No source was found expressing this exact physically reachable fiber statement.

But the special product-triangular subclass is already heavily covered by Doan–Kloeden 2022.

### Q4 verdict

**USEFUL COMPLETENESS.**

Do not claim general triangularity is sufficient. The extra "basin-determining coordinate" hypothesis is essential.

---

# Q5 — Monotone/comparison extension

## 12. Wu 2020, Wu 2023, Cheng–Wu 2026

### Scalar comparison

**Cong Wu (2020)**, "A General Comparison Principle for Caputo Fractional-Order Ordinary Differential Equations," *Fractals* 28(4), 2050070. DOI **10.1142/S0218348X2050070X**. **PUBLISHED.**

This develops a general scalar Caputo comparison principle using maximal solutions and Vainikko's Caputo derivative framework.

### System comparison

**Cong Wu (2023)**, "Comparison Principles for Systems of Caputo Fractional Order Ordinary Differential Equations," *Chaos, Solitons & Fractals* 171, 113437. DOI **10.1016/j.chaos.2023.113437**. **PUBLISHED.**

The paper proves system comparison principles for quasi-monotone, mixed quasi-monotone and mixed-monotone structures. These are order-comparison theorems: ordered data and suitable differential inequalities produce ordered solution bounds.

### Current extension

**Tong Cheng; Cong Wu (2026)**, "Analysis of Caputo Fractional Order Systems: The Complete System Comparison Principles," *Journal of Mathematical Analysis and Applications* 559(1), 130509. DOI **10.1016/j.jmaa.2026.130509**. **PUBLISHED.**

This extends/completes the system comparison framework, including variants of Chaplygin-type comparison.

## 13. Why comparison alone does not imply endpoint-fiber purity

An endpoint fiber contains memory states (phi,psi) satisfying
[
e_0(phi)=e_0(psi),
]
but this says nothing about the pointwise order of their histories.

Comparison theorems require an order relation or differential inequality from which a future order can be propagated. They do **not** provide:

[
e_0(phi)=e_0(psi)
quad\Longrightarrowquad
omega(phi)=omega(psi),
]
nor do they make basin membership factor through (e_0).

Even if two histories happen to be ordered, monotonicity alone generally preserves order; it does not force convergence to the same attractor.

A monotone/comparison purity theorem therefore needs an additional endpoint-determining object, for example:

- a scalar coordinate/functional whose current value defines invariant threshold regions;
- a theorem that basin labels are constant on each endpoint-determined order interval;
- or an explicit factorization
  [
  \text{basin-label}=B\circ e_0
  ]
  on (mathcal R_\alpha).

No published Caputo theorem of this form was located in the searched corpus.

### Q5 verdict

**EXTRA CONDITIONS REQUIRED.**

The strongest currently justified route is P2-style: comparison can help prove an endpoint-determining separator theorem, but cannot replace it.

---

# 14. Exact residual after ROUND-0002

The scalar branch is essentially closed as a novelty source.

For a broad dissipative scalar Caputo class with simple equilibria, published theory already provides:

- noncrossing/separation;
- equilibrium barriers;
- intervalwise asymptotic convergence;
- the strong-Allee extinction/survival pattern for an exact published cubic model.

The project's fiber-purity restatement is useful, but it is a **standard completeness consequence** of those ingredients.

The triangular branch remains useful only if the Chief wants a clean impossibility/completeness theorem at a scope beyond the already-published product-triangular class.

The monotone branch does not currently yield endpoint-fiber purity without an additional endpoint-determining hypothesis.

---

# 15. Bibliography/reference actions recommended

Add/verify:

1. Area & Nieto 2023 — DOI **10.1016/j.exco.2023.100121**.
2. Kalra & Malhotra 2024 — DOI **10.37256/cm.5120243183** (contextual, not load-bearing).
3. Wu 2023 — DOI **10.1016/j.chaos.2023.113437**.
4. Correct Wu 2020 metadata to *Fractals* 28(4), article **2050070**.
5. Keep Doan–Kloeden 2022 — DOI **10.1007/s13540-022-00030-6** as the principal scalar/triangular asymptotic reference.
6. Keep Cheng–Wu 2026 — DOI **10.1016/j.jmaa.2026.130509** for current comparison coverage.
7. Add a source note that Diethelm–Ford 2012 is historical background rather than the load-bearing separation proof.

All above are formally published.

---

# 16. Negative-search limitations

- The exact phrase "reachable present-state fiber" is project terminology; an equivalent result could exist under order-convex basin, threshold functional, quotient/factor, or monotone-semiflow language.
- Older monographs and non-digitized Volterra literature are not uniformly full-text searchable.
- Failure to locate a monotone endpoint-factor theorem is not proof that no such theorem exists.
- The strongest search for a triangular/monotone theorem should be repeated only after the Chief fixes an exact P2/P3 statement; broad searches are now low-yield.

---

# 17. Recommended next search

Do **not** open another generic scalar-purity round.

Highest-value next triggers are:

1. if Compute TASK-0001 returns a Double-Allee baseline or collision candidate, run **W-A004/model-specific audit** against the exact equations and parameter regime;
2. if the Chief promotes an exact triangular/monotone purity theorem, search that exact statement/sign class before promotion;
3. otherwise wait for the constructive branch, because the scalar novelty question is now sufficiently closed.
