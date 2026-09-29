# ROUND-0003 — RETURN TO CHIEF

**Round ID:** ROUND-0003  
**Request:** `research/coordination/chief-to-web/ROUND-0003_exact-model-threshold-recovery-basin-closure_REQUEST.md`  
**Search date:** 2026-09-29  
**Agent:** Deep Web Search Agent  
**Final substantive evidence commit before this return:** `756dc9b932f19c91a60c05b4b335e81ed95132f7`

## Required verdicts

- **Mondal 2025 baseline:** **MODEL VERIFIED / PARAMETER-TABLE RECOVERY PARTIAL**
- **Exact project vector-field prior:** **DIRECT INTEGER-ORDER PRIOR FOUND; NO EXACT CAPUTO PRIOR FOUND**
- **Caputo sign-vs-monotonicity mechanism:** **KNOWN GENERAL FACT BUT NEW APPLICATION STRUCTURE POSSIBLE**
- **Candidate X1 cold-start extinction strip:** **X1 VERIFIED**
- **Survival-basin closure:** **SUFFICIENT PIECES AVAILABLE**
- **Exact basin-entry novelty killer:** **CLOSE HEREDITARY ANALOGUE; STRICT CAPUTO RESIDUAL SURVIVES**
- **Overall theorem program:** **SURVIVES NARROWLY; EXTINCTION SIDE CLOSED, SURVIVAL SIDE REMAINS THE PRINCIPAL BOTTLENECK**

# 1. Mondal et al. 2025 — exact fractional model

Primary source:

**Mondal, R.; Pal, D.; Takeuchi, Y.; Mukherjee, D.; Kesh, D.; Saha, A. (2025).**  
“Dynamics of a fractional order predator-prey system with double Allee effect and group defense.”  
*Chinese Journal of Physics* 98, 613–632.  
DOI `10.1016/j.cjph.2025.09.020`.

The incommensurate system is
[
{}^CD^{alpha_1}x
=
xleft[
rac r{x+a}
left(1-rac{x}{k}ight)(x-m)
-rac{qy}{eta+x^2}
ight],
]
[
{}^CD^{alpha_2}y
=
yleft[
rac{px}{eta+x^2}-e
ight],
qquad 0<alpha_1,alpha_2<1.
]

The commensurate version uses the same right-hand side and a common order (alpha).

The exact Double-Allee structure is
[
rac{x-m}{x+a}
left(1-rac{x}{k}ight),
]
and the group-defense functional response is the simplified Monod–Haldane / dome-shaped form
[
rac{x}{eta+x^2}.
]

Verified equilibria:
[
E_0=(0,0),quad E_1=(k,0),quad E_2=(m,0)
]
((E_2) for strong Allee (m>0)), plus interior equilibria satisfying
[
ex^{*2}-px^*+eeta=0,
qquad
x^*=rac{ppmsqrt{p^2-4eta e^2}}{2e}.
]

The primary source verifies:
- existence/uniqueness;
- non-negativity;
- boundedness;
- Matignon local-stability analysis;
- commensurate and incommensurate fractional orders.

For strong Allee, (E_0) is always locally stable.

The basin-stability/multistability layer is **numerical**, not a global basin theorem.

## Provenance limitation

The accessible primary Elsevier text did not expose the complete numerical parameter table and exact basin-figure/table mapping required for faithful reproduction of a specific fractional basin plot.

Do **not** fill this gap from the ResearchGate “full text” that appears under the Mondal title: the surfaced PDF is actually the distinct Pal et al. 2025 integer-order paper below.

Therefore Compute may implement the Mondal equations exactly, but should not claim reproduction of a particular Mondal basin figure until the actual fractional table is recovered from the correct PDF.

# 2. Verified fallback / integer-order parent

**Pal, D.; Mondal, R.; Kesh, D.; Mukherjee, D. (2025).**  
“Non-spatial Dynamics and Spatiotemporal Patterns Formation in a Predator–Prey Model with Double Allee and Dome-shaped Response Function.”  
*Bulletin of Mathematical Biology* 87(2), article 35.  
DOI `10.1007/s11538-025-01411-7`.

This uses
[
dot u=
uleft[
rac r{u+a}left(1-rac ukight)(u-m)
-rac{qv}{b+u^2}
ight],
]
[
dot v=
vleft[
rac{pu}{b+u^2}-d
ight].
]

Verified parent values include
[
r=1, a=0.9, k=2, q=5, p=1.2, d=0.4,
]
with (m) and (b) varied.

This is a safe fallback reproduction target, but its parameter values must not be represented as the fractional Mondal parameter table.

# 3. Exact prior for the project-constructed model

A direct published prior exists.

**Ye, Y.; Liu, H.; Wei, Y.; Zhang, K.; Ma, M.; Ye, J. (2019).**  
“Dynamic study of a predator-prey model with Allee effect and Holling type-I functional response.”  
*Advances in Difference Equations* 2019, 369.  
DOI `10.1186/s13662-019-2311-1`.

Their strong-Allee ODE is
[
dot x=x(1-x)(x-eta)-alpha xy,
]
[
dot y=gamma xy-delta y.
]

Under
[
etaleftrightarrow	heta,quad
alphaleftrightarrow a,quad
gammaleftrightarrow b,quad
deltaleftrightarrow m,
]
this is **exactly the project vector field**.

Ye et al. prove integer-order boundedness and analyze equilibria, local stability and Hopf bifurcation; they also exhibit strong-Allee bistability.

Hence:

> **The ecological vector field is prior art and must not be claimed as novel.**

The targeted search did not identify an exact published classical-Caputo fractionalization of this same four-term vector field, nor the project's cold-start-versus-continuation-state theorem.

# 4. Caputo derivative sign versus monotonicity

The load-bearing novelty boundary is:

**Diethelm, K. (2016).**  
“Monotonicity of functions and sign changes of their Caputo derivatives.”  
*Fractional Calculus and Applied Analysis* 19(2), 561–566.  
DOI `10.1515/fca-2016-0029`.

Theorem 2.1:
monotonicity implies the corresponding sign of the Caputo derivative for **every**
[
alphain(0,1).
]

Theorem 2.2:
the converse is obtained only when the sign condition holds for all orders in an interval
[
alphain(alpha_0,1).
]

The paper explicitly shows that fixed sign for one/few fractional orders is insufficient to infer monotonicity.

Therefore:
[
{}^CD^alpha x<0
]
for one fixed (0<alpha<1) on a later time interval does **not** imply that (x(t)) decreases there.

This analytic fact is known.

The project may still have new structure in the combination:

> cold-start comparison proves extinction below a physical threshold, while a reachable continuation state carrying prehistory passes through the same region and recovers.

No direct published strong-Allee threshold-recovery theorem of that form was identified.

## Verdict

**KNOWN GENERAL FACT BUT NEW APPLICATION STRUCTURE POSSIBLE.**

# 5. Candidate X1 — cold-start extinction strip

For
[
{}^CD^alpha x=x(1-x)(x-	heta)-axy,
]
[
{}^CD^alpha y=y(bx-m),
]
assume
[
a,b,m>0,quad0<	heta<1,quad
	heta<rac mb.
]

For every standard cold start
[
0<x_0<	heta,qquad y_0ge0,
]
the source-audited proof is valid.

## 5.1 Positive cone

The polynomial vector field is locally Lipschitz and quasi-positive:
[
F_1(0,y)=0,qquad F_2(x,0)=0.
]

Published Caputo viability theory:
**Girejko–Mozyrska–Wyrwas 2011**, DOI `10.1016/j.jmaa.2011.04.004`, supplies positive-set viability machinery.

Caputo extremum results from **Al-Refai 2012**, DOI `10.14232/ejqtde.2012.1.55`, also support the standard first-contact proof.

Thus nonnegative standard initial data remain nonnegative.

## 5.2 Prey comparison

Because (y(t)ge0),
[
{}^CD^alpha x
le
x(1-x)(x-	heta).
]

**Wu 2020**, DOI `10.1142/S0218348X2050070X`, Theorem 3.2 supplies the scalar comparison form needed here.

If (u) solves
[
{}^CD^alpha u=u(1-u)(u-	heta),
qquad u(0)=x_0,
]
then
[
0le x(t)le u(t).
]

ROUND-0002 already verified
[
0<x_0<	heta
Longrightarrow
0<u(t)<	heta,qquad u(t)	o0.
]

Hence
[
x(t)	o0.
]

## 5.3 Predator comparison

Let
[
delta=m-b	heta>0.
]

Since (x(t)<	heta),
[
{}^CD^alpha y
le
-delta y.
]

Comparison with
[
v(t)=y_0E_alpha(-delta t^alpha)
]
gives
[
0le y(t)le v(t)	o0.
]

## 5.4 Global continuation

The comparison bounds imply, on every finite interval,
[
0le x(t)le	heta,qquad
0le y(t)le y_0.
]

**Wu & Liu 2020**, DOI `10.1515/fca-2020-0029`, give the Caputo continuation/blow-up alternative. The bounded solution cannot terminate at a finite maximal time.

Therefore
[
(x(t),y(t))	o(0,0).
]

## Verdict

[
oxed{	ext{X1 VERIFIED}}
]

The Chief can promote the cold-start strip after rewriting the proof with these exact imported dependencies.

# 6. Survival basin in the continuation-state space

No off-the-shelf theorem was found that says a late physical near-hit to a Matignon-stable equilibrium places the associated continuation history in its basin.

That would incorrectly behave like an ODE restart.

However, a standard physical convergence proof is sufficient.

For (f_0=iota(p)),
[
(T_tf_0)(	heta)
=
p+
rac1{Gamma(alpha)}
int_0^t
(t+	heta-s)^{alpha-1}g(x(s)),ds.
]

Subtracting this from the Volterra formula for (x(t+	heta)) gives
[
x(t+	heta)-(T_tf_0)(	heta)
=
rac1{Gamma(alpha)}
int_t^{t+	heta}
(t+	heta-s)^{alpha-1}g(x(s)),ds.
]

If a standard physical IVP is proved to satisfy
[
x(t;p)	o x^*,qquad g(x^*)=0,
]
then for every compact memory-age interval (0le	hetale N),
[
sup_{	hetale N}
|x(t+	heta)-(T_tiota(p))(	heta)|
le
rac{N^alpha}{Gamma(alpha+1)}
sup_{sin[t,t+N]}|g(x(s))|
	o0.
]

Also
[
sup_{	hetale N}|x(t+	heta)-x^*|	o0.
]

Hence
[
T_tiota(p)	oiota(x^*)
]
in the compact-open Doan–Kloeden topology.

Therefore:

> proving physical convergence of the standard IVP to (E^*) is sufficient to prove continuation-state basin membership.

What remains missing is exactly that physical convergence theorem for the TASK-0001 survival witness.

**Doan–Kloeden 2024**, DOI `10.1007/s13540-024-00324-x`, provides the correct continuation-state/global-attractor framework but not an explicit local trapping set that closes this particular witness.

## Verdict

**SUFFICIENT PIECES AVAILABLE.**

# 7. Exact basin-entry novelty killer

The closest published analogue found remains:

**Szaksz, Stepan & Habib (2024)**,  
*Journal of Sound and Vibration* 571, 118045,  
DOI `10.1016/j.jsv.2023.118045`.

They define a reduced DDE basin through the **headpoint** of constrained history functions and explicitly note that a trajectory can have an initial-history headpoint outside the reduced BoA while later entering and leaving that BoA.

This is conceptually close to:
- same physical/headpoint location;
- different history information;
- physical-region membership not determining fate.

But it is not the strict project theorem:
- not autonomous Caputo (0<alpha<1);
- not the Doan–Kloeden reachable set;
- not comparison between (iota(z)) and a physically reached continuation state (T_tiota(p));
- not rigorously opposite extinction/survival basins.

No direct published Caputo theorem equivalent to E1's cold-start basin-entry instantiation was found.

## Verdict

**CLOSE HEREDITARY ANALOGUE; STRICT CAPUTO RESIDUAL SURVIVES.**

# 8. Current novelty boundary

The final paper must **not** claim novelty for:

- the predator–prey vector field;
- Caputo Double-Allee modeling;
- fractional multistability/basin plots;
- the fact that a single fixed-order Caputo derivative sign need not determine monotonicity;
- history/headpoint basin effects in hereditary systems;
- comparison, viability, or continuation machinery;
- E1 as a purely abstract logical implication.

The defensible residual is:

> In an autonomous continuous Caputo system, establish rigorously that a standard IVP in a survival basin enters an open physical region whose canonical cold starts are in the extinction basin; consequently a physically reachable present-state fiber contains two continuation states with distinct asymptotic fates.

For the project model, the extinction half is now source-closed.

# 9. Principal remaining theorem gap

The bottleneck is no longer X1, collision geometry, or derivative-sign interpretation.

It is:

[
oxed{
	ext{prove one standard IVP of the exact Caputo model converges to }E^*
}
]

while certifying that its finite-time trajectory enters (R_{m ext}).

If TASK-0002 supplies:
- a validated finite-time entry; and
- a witness lying in a rigorously provable physical convergence/trapping regime;

then E1 closes TARGET-A20 directly.

# 10. Bibliography/reference changes

Added verified published entries:
- Ye et al. 2019 — DOI `10.1186/s13662-019-2311-1`;
- Diethelm 2016 — DOI `10.1515/fca-2016-0029`;
- Al-Refai 2012 — DOI `10.14232/ejqtde.2012.1.55`;
- Wu & Liu 2020 — DOI `10.1515/fca-2020-0029`;
- Pal et al. 2025 — DOI `10.1007/s11538-025-01411-7`.

Updated:
- `bibliography/references.bib`;
- `research/REFERENCES.md`;
- `research/LITERATURE_MAP.md`.

All additions are formally published.

# 11. Files produced/modified

- `research/web-search/2026-09-29_ROUND-0003_exact-model-threshold-recovery-basin-closure_REPORT.md`
- `research/coordination/web-to-chief/ROUND-0003_exact-model-threshold-recovery-basin-closure_RETURN.md`
- `bibliography/references.bib`
- `research/REFERENCES.md`
- `research/LITERATURE_MAP.md`

# 12. Negative-search limitations

- Exact Mondal 2025 fractional basin-table values remain unresolved from the accessible primary indexing layer.
- No exact Caputo prior found is a search result, not proof of absence.
- The strict basin-entry theorem may exist under different hereditary/factor-state terminology.
- Local Matignon stability is not treated as basin proof.
- Numerical basin plots are not treated as global theorems.

# 13. Recommended next trigger

Do not open another generic literature round.

Wait for TASK-0002 or a Chief proof candidate for survival convergence.

Then hostile-search:
1. the exact parameter box;
2. the exact trapping/Lyapunov inequality;
3. the exact survival theorem statement;
4. any 2025–2026 model-specific competitor.

That is now the highest-value literature gate.
