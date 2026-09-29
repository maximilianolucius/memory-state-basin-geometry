# ROUND-0004 — CHIEF DECISION

**Date:** 2026-09-29  
**Evaluates:** \`research/coordination/web-to-chief/ROUND-0004_local-survival-lyapunov_RETURN.md\`  
**Disposition:** ACCEPT — L1 PROMOTED TO PROVED LOCAL SURVIVAL THEOREM

## 1. Executive decision

ROUND-0004 removes the final imported-theorem uncertainty from the preferred survival route.

The following are now accepted:

- the quadratic Caputo inequality required by L1 is valid along actual solutions, using Ren & Wu (2019), Lemma 3.1;
- scalar comparison gives an explicit Mittag-Leffler upper bound for the Lyapunov function;
- the first-exit argument rigorously proves invariance of the certified ball;
- boundedness plus Wu & Liu (2020) yields global continuation;
- the same comparison estimate gives convergence to the coexistence equilibrium;
- STRUCTURAL-E3 then lifts physical convergence to compact-open continuation-state convergence.

Therefore CANDIDATE-L1 is promoted to **THEOREM-L1 — explicit local survival basin**.

## 2. THEOREM-L1

Let
\[
{}^CD^\alpha u=Ju+N(u),\qquad 0<\alpha<1,
\]
where \(J\) is Hurwitz.

Let \(P=P^\top>0\) solve
\[
J^\top P+PJ=-I.
\]

Assume that on \(\|u\|_2\le r\),
\[
\|N(u)\|_2\le C_r\|u\|_2^2,
\]
and
\[
2\|P\|_2C_r r\le\frac12.
\]

Then every standard initial state satisfying
\[
u_0^\top Pu_0<\lambda_{\min}(P)r^2
\]
is global and converges to the equilibrium.

More explicitly,
\[
V(t)\le
V(0)E_\alpha\!\left(
-\frac{t^\alpha}{2\lambda_{\max}(P)}
\right).
\]

Hence its canonical continuation state belongs to the survival basin.

## 3. Load-bearing source chain

Use:
1. Ren & Wu 2019, Lemma 3.1 — quadratic Caputo inequality;
2. classical continuous-time Lyapunov matrix theorem for Hurwitz \(J\);
3. Wu 2020, Theorem 3.2 — scalar comparison;
4. Wu & Liu 2020 — continuation/global existence;
5. project STRUCTURAL-E3 — physical convergence to compact-open continuation-state convergence.

Águila-Camacho et al. 2014 is historical only, not load-bearing.

## 4. Novelty disposition

L1 itself is not the principal novelty. Explicit quadratic fractional Lyapunov methods are established mathematics.

The strict residual remains:

> construct/certify a standard initial condition lying in the rigorous L1 survival ellipsoid whose actual Caputo trajectory later enters the already-proved cold-start extinction strip.

No direct published theorem satisfying that full conjunction was found in ROUND-0004.

## 5. Consequence for TASK-0003

TASK-0003 is no longer conditional on literature audit.

Its acceptance criterion is exact:

1. exact rational parameters;
2. exact/rationally certified \(E^*\), \(J\), \(P\);
3. rigorous \(C_r\), \(r\), and L1 inequality;
4. rigorous initial-point ellipsoid inclusion;
5. validated finite-time entry into \(R_{\rm ext}\).

If one candidate satisfies all five, TARGET-A20 is proved immediately by L1 + X1 + E1.

## 6. Search posture

No further web round now.

If TASK-0003 succeeds, the next search is the final theorem-specific novelty audit keyed to the exact rational witness and final theorem statement.
