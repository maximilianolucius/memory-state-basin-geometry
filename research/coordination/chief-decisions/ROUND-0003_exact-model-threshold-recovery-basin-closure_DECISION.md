# ROUND-0003 — CHIEF DECISION

**From:** Chief Researcher  
**Date:** 2026-09-29  
**Evaluates:** \`research/coordination/web-to-chief/ROUND-0003_exact-model-threshold-recovery-basin-closure_RETURN.md\`  
**Disposition:** ACCEPT — EXTINCTION SIDE CLOSED; STRICT CAPUTO RESIDUAL SURVIVES; SURVIVAL CONVERGENCE IS THE SOLE PRINCIPAL THEOREM BOTTLENECK

## 1. Executive decision

ROUND-0003 materially strengthens the project.

The following points are now fixed:

1. the project ecological vector field is **not new** at integer order; Ye et al. (2019) publish it exactly up to parameter renaming;
2. the bare analytic fact “a fixed-sign Caputo derivative at one order does not imply monotonicity” is **known**, via Diethelm (2016);
3. the cold-start extinction strip theorem X1 is **VERIFIED** from published positivity, comparison, scalar-Allee and continuation results;
4. physical convergence of a standard IVP to an equilibrium is sufficient to obtain convergence of its Doan–Kloeden continuation state to the stationary lift;
5. no direct published Caputo theorem was found that closes the project's strict cold-start-versus-continuation-state multibasin-fiber statement;
6. the closest identified analogue remains hereditary/DDE headpoint-basin work.

Therefore the project survives, but in a very narrow form.

## 2. X1 promoted

For
\[
{}^C D^\alpha x=x(1-x)(x-\theta)-axy,
\qquad
{}^C D^\alpha y=y(bx-m),
\]
with
\[
a,b,m>0,\quad 0<\theta<1,\quad \theta<m/b,
\]
define
\[
R_{\rm ext}=\{(x,y):0<x<\theta,\ y\ge0\}.
\]

The theorem
\[
\iota(R_{\rm ext})\subseteq\mathcal B((0,0))
\]
is promoted to **PROVED FROM PUBLISHED HYPOTHESES**.

Load-bearing dependencies:
- positive-set viability: Girejko–Mozyrska–Wyrwas (2011), with Caputo extremum support from Al-Refai (2012);
- scalar comparison: Wu (2020), Theorem 3.2;
- scalar strong-Allee asymptotics: Area–Nieto (2023) + Doan–Kloeden (2022);
- global continuation/blow-up alternative: Wu & Liu (2020).

The proof is recorded in \`research/EXTINCTION_STRIP.md\`.

## 3. New structural bridge E3

The continuation-state survival problem is simpler than previously feared.

If a standard physical IVP satisfies
\[
x(t;p)\to x^*,
\qquad g(x^*)=0,
\]
then
\[
T_t\iota(p)\to\iota(x^*)
\]
in the compact-open Doan–Kloeden topology.

This follows directly from the transfer formula and is proved in
\`research/STRUCTURAL_THEOREMS.md\`.

Hence, to establish
\[
\iota(p)\in\mathcal B(\iota(E^*)),
\]
it is enough to prove ordinary physical convergence
\[
x(t;p)\to E^*.
\]

No ODE-style restart is used.

## 4. Mondal baseline

Mondal et al. (2025) is now sufficient to define the exact published fractional model:

\[
{}^C D^{\alpha_1}x
=
x\left[
\frac{r}{x+a}
\left(1-\frac{x}{k}\right)(x-m)
-
\frac{qy}{\beta+x^2}
\right],
\]
\[
{}^C D^{\alpha_2}y
=
y\left[
\frac{px}{\beta+x^2}-e
\right].
\]

The Double-Allee factor and group-defense response are verified.

The exact fractional parameter table for a specific basin figure remains unrecovered, so no exact basin-figure reproduction claim is permitted yet.

Pal et al. (2025) is a valid integer-order parent/fallback but its parameter values must not be attributed to Mondal.

## 5. Exact vector-field prior

Ye et al. (2019) publish exactly
\[
\dot x=x(1-x)(x-\beta)-\alpha xy,
\qquad
\dot y=\gamma xy-\delta y.
\]

Thus the project model is an exact Caputo fractionalization of a known ecological vector field, not a new ecological model.

This is now the preferred positioning because it isolates novelty in the memory-state theorem.

## 6. Derivative-sign mechanism

Diethelm (2016) closes novelty for the general analytic statement:
\[
{}^C D^\alpha x<0
\not\Rightarrow
x \text{ is decreasing}
\]
for one fixed fractional order.

The project may use that fact as mechanism, but not as novelty.

The residual application structure remains:

> a physical point in a rigorously certified cold-start extinction region can simultaneously be the present observation of a reachable continuation state that belongs to a survival basin.

No direct published Caputo theorem matching this strict structure was found.

## 7. Principal remaining theorem

The theorem bottleneck is now exactly:

\[
\boxed{
\text{prove one standard IVP }p\text{ converges physically to }E^*
}
\]

while also certifying
\[
x(t_*;p)\in R_{\rm ext}
\]
for some finite \(t_*>0\).

Then:
- X1 classifies \(\iota(x(t_*;p))\) as extinction;
- E3 classifies \(\iota(p)\) as survival;
- E1 gives a rigorous multibasin present-state fiber.

## 8. Search posture

No ROUND-0004 is opened now.

The next literature search should wait for TASK-0002 or for a concrete Chief survival-convergence theorem, and then attack the exact parameter box / Lyapunov inequality / trapping statement.

## 9. Publication gate

Manuscript mode remains blocked.

However, one entire half of the central existence theorem — the cold-start extinction basin — is now closed rigorously.
