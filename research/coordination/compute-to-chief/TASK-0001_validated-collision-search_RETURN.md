# TASK-0001 — Validated Caputo collision-search infrastructure — COMPUTE RETURN

**From:** Compute Agent
**To:** Chief Researcher
**Task:** `research/coordination/chief-to-compute/TASK-0001_validated-collision-search_REQUEST.md`
**Date:** 2026-09-29
**Branch:** `compute/task-0001`
**Final commit SHA:** _see the bottom of this file_

---

## 0. Executive answer

| Stage | Verdict |
|---|---|
| A — solver validation | **PASS** (three history-retaining solvers, two different formulations) |
| B — published intersection reproduction | **PASS in substance, with a provenance caveat**; one item is a **CERTIFIED COMPUTATION** |
| C — Double-Allee baseline as specified | **HALTED** (stop condition triggered: Mondal et al. 2025 is not recoverable locally) |
| C′ — substitute baseline | **PASS**, on a clearly labelled PROJECT-CONSTRUCTED model |
| D — inter-basin collision discovery | **WITNESS FOUND**, extinction side CERTIFIED-CONDITIONAL, survival side NUMERICAL |

The single most important thing in this return is not a number, it is a structural
simplification of **CANDIDATE-M2**:

> The existence of a multibasin reachable present-state fibre is an **open
> condition**. It needs no transversality hypothesis, no nonsingular `d x d`
> minor and no implicit function theorem. It needs only (i) an open set of
> physical states whose canonical embeddings lie in one basin, (ii) one physical
> state in a different basin whose orbit enters that open set, and (iii)
> continuity of the solution map. Items 2-4 and 6 of the CANDIDATE-M2 burden
> list in `research/STATE_ARCHITECTURE.md` §5 are therefore **not needed for
> persistence**; only items 1 (robust basin membership) and 5 (fixed-lower-terminal
> memory) are load-bearing.

Section 5 states this precisely; Section 8 says what is still missing to make it
a theorem.

### The witness in one block

```
model (PROJECT-CONSTRUCTED, prey term = published Area-Nieto 2023 cubic)
    ^C D^a x = x(1-x)(x - 3/10) - x y ,     ^C D^a y = y(x - 4/5) ,   a = 0.85
    extinction (0,0)   eigenvalues -3/10, -4/5        -> stable for every a in (0,1)
    Allee threshold (3/10, 0)   eigenvalues -1/2, 21/100   -> saddle
    prey-only (1, 0)            eigenvalues 1/5, -7/10     -> saddle
    coexistence E* = (4/5, 1/10)  eigenvalues (-3 +- i sqrt(41))/25
                                                          -> Caputo-stable for a < 1.27893
    (all four exact, from rational/radical arithmetic)

constant initial history      p = (2.4372, 2.012)          -> converges to E*
its orbit is inside {0 < x < 3/10} for   t in [1.26, 35.74]
deepest point                 z* = (0.196626, 0.032057)  at t = 3.90
margin theta - min x          0.1029  (3 solvers x 4 meshes agree to 1.7e-4;
                                       30-digit mpmath agrees to 3.1e-12)
every z on that arc:  iota(z) in B(0,0)   [CERTIFIED-CONDITIONAL]
                      T_t iota(p) in B(E*) [NUMERICAL]
=> F_z is multibasin for a whole one-parameter family of z.
```

The Caputo-specific mechanism, in one line: on that arc `^C D^a x(t) <= -0.0108 < 0`
by exact algebra, and yet `x` rises monotonically by `+0.1034` back through
`theta` — the equivalence "negative derivative <=> decreasing", which makes the
Allee threshold an absolute barrier at `alpha = 1`, is destroyed by power-law
memory, while the comparison principle that traps a *cold start* below `theta`
survives. That asymmetry is the entire construction (§6).


---

## 1. What was built

`computations/msbg/` — library; `computations/scripts/` — one script per stage;
`computations/tests/` — 61 pytest checks; `computations/data/`,
`computations/manifests/`, `computations/figures/` — artifacts, each manifest
recording host, package versions, BLAS build, git commit and artifact SHA-256.

### Three history-retaining solvers, two formulations

| key | formulation | scheme | nominal order |
|---|---|---|---|
| `pi_rect` | Volterra integral `x = x0 + I^a g(x)` | product-integration rectangle, explicit | `O(h)` |
| `pece` | Volterra integral | Diethelm–Ford–Freed fractional Adams predictor–corrector | `O(h^min(2,1+a))` |
| `l1` | Caputo derivative itself | classical L1, implicit, batched Newton | `O(h^(2-a))` |

`pi_rect`/`pece` discretise a weakly singular integral; `l1` discretises the
fractional derivative. They are therefore independent in the sense the task
asked for, not two tunings of the same quadrature. No memoryless one-step
surrogate appears anywhere: every step consumes the whole discrete history.

Solvers are **batched** — `M` initial conditions advance together against the
same weight vectors, so one history convolution is one BLAS call. Cost
`O(N^2 M d)`, memory `O(N M d)`.

### Arbitrary-precision Mittag-Leffler function

Needed because every exact solution used as ground truth is a Mittag-Leffler
value. Two independent evaluation routes:

* **Taylor**, adaptive working precision. The series has maximal term of size
  `~exp(|z|^{1/a})`, so the guard-digit budget is set by `|z|^{1/a}`, not by
  `|z|`; the implementation computes that budget and *refuses* arguments beyond
  it instead of running for minutes at reduced accuracy.
* **Stieltjes**, for `z = -x < 0` and `0 < a < 1`. Collapsing the Bromwich
  contour of `p^{a-1}/(p^a + x)` onto the branch cut (no poles lie on the
  principal sheet) and substituting `s = r^a`, which removes the `r^{a-1}`
  endpoint singularity *exactly* because `r^{a-1} dr = ds/a`:

  `E_a(-x) = (x sin(a pi)/(pi a)) int_0^inf e^{-s^{1/a}} / (s^2 + 2 x s cos(a pi) + x^2) ds`

  The normalisation is exact: as `x -> 0` the integral equals `pi a/(x sin(a pi))`,
  giving `E_a(0) = 1`. This route is accurate and cheap for arbitrarily large `x`,
  where the Taylor route is unusable.

### Arb ball-arithmetic certification layer

`msbg/certify.py` gives rigorous enclosures of `E_a` and `E_a'` (Arb balls,
truncated series **plus a proved tail bound**) and a Krawczyk root test.
The tail bound: for `T_k = R^k/Gamma(a k + 1)` the ratio
`T_{k+1}/T_k = R Gamma(ak+1)/Gamma(ak+a+1)` is decreasing in `k` because
`Gamma(x+a)/Gamma(x)` is increasing in `x>0` (log-convexity of Gamma), so if the
ratio at `k=K+1` is `rho<1` then `sum_{k>K} T_k <= T_{K+1}/(1-rho)` — all three
quantities computed as Arb balls.

---

## 2. Stage A — solver validation: PASS

Command: `python scripts/stage_a_validate.py`. Artifacts:
`data/stage_a_A*.json`, `manifests/stage_a_manifest.json`.

**A1 — Mittag-Leffler implementation.** 43 checks, worst absolute discrepancy
`0.0` at 30 digits:

* Taylor vs closed forms `E_1 = exp`, `E_{1/2}(z) = e^{z^2} erfc(-z)`,
  `E_2(z) = cosh(sqrt z)` — 12 checks;
* Taylor vs Stieltjes on their common domain — 22 checks;
* Stieltjes vs the large-argument asymptote `1/(x Gamma(1-a))` — 9 checks,
  ratios `0.99968 … 1.00146` at `x = 1e3` tightening to `1.0000000 … 1.0000002`
  at `x = 1e7`, approached monotonically from above.

**A2 — scalar linear `^C D^a x = lam x` against the exact `x0 E_a(lam t^a)`**,
`T = 2`, meshes `N = 250 … 4000`, `a in {0.4, 0.6, 0.85}`, `lam in {-1, +0.7}`.
Observed orders (least squares on log h):

| a | lam | `pi_rect` | `pece` | `l1` |
|---|---|---|---|---|
| 0.40 | −1.0 | 1.011 | 1.275 | 1.004 |
| 0.40 | +0.7 | 1.017 | 1.391 | 0.979 |
| 0.60 | −1.0 | 1.002 | 1.474 | 1.014 |
| 0.60 | +0.7 | 1.005 | 1.581 | 0.926 |
| 0.85 | −1.0 | 1.000 | 2.515 | 1.035 |
| 0.85 | +0.7 | 0.999 | 1.798 | **0.327** |

Finest-mesh absolute errors: `pi_rect` 1.2e-3 … 1.6e-5, `pece` 8.8e-10 … 7.9e-5,
`l1` 1.3e-5 … 6.0e-4.

Two honest caveats, not smoothed over:
* the `pece` entry `2.515` at `a = 0.85, lam = -1` exceeds its own theoretical
  `min(2, 1+a) = 1.85`; its finest error is `8.8e-10`, i.e. the ladder is
  reaching the round-off floor and the fitted slope there is not an order;
* the `l1` entry `0.327` at `a = 0.85, lam = +0.7` is **not** an order. The error
  sequence is non-monotone in `h` (`8.4e-4, 1.86e-4, 3.68e-4, 3.08e-4, 2.10e-4`),
  the signature of a leading error term changing sign inside the ladder. No order
  is claimed for that configuration. `l1` is never used as a primary solver; it
  is the independent cross-check.

**A3 — genuinely planar linear problem** `^C D^{0.5} x = A x`, `A` a scaled
rotation, against the **exact** matrix Mittag-Leffler value (see §3 for why the
matrix value is exact and not itself a numerical approximation).
Observed orders `pi_rect` 1.010, `pece` 1.489, `l1` 1.035; finest errors
6.8e-4, 9.5e-6, 1.3e-4.

**A4 — long horizon** `T = 1000`, `N = 200000`, `a = 0.5`, `lam = -1`, against
the exact algebraic tail. Relative errors `pi_rect` 2.5e-6, `pece` 1.3e-8,
`l1` 1.2e-6. All three reproduce the `t^{-a}` algebraic decay; none develops the
spurious oscillation or exponential decay that a memoryless surrogate would.

**A5 — determinism.** All three solvers bitwise identical on repeated runs
(`max_abs_diff = 0.0`), asserted in `tests/test_solvers.py::test_determinism_bitwise`.

**A6 — cross-solver agreement on the nonlinear ecological model** (no closed
form exists): self-convergence orders `pi_rect` 1.390, `pece` 1.807, `l1` 1.678;
pairwise maximum differences at the finest mesh `pi_rect/pece` 1.4e-3,
`pi_rect/l1` 1.6e-3, `pece/l1` 1.9e-4. Agreement is consistent with the
individual convergence orders — **no disagreement beyond convergence
expectations**, so the Stage-A stop condition is not triggered.

**A7 — positivity.** 400 initial conditions, `T = 300`, all three solvers:
`0` trajectories leave the positive cone; `min x = 1.11e-3`, `min y = 4.29e-4`.

**Regression tests.** `pytest tests/ -q`: **60 passed, 1 skipped** (the skip is a
Taylor-route argument deliberately out of guard-digit budget).

---

## 3. Stage B — reachable present-state non-injectivity in `d = 2`

Command: `python scripts/stage_b_intersection.py`.

### Provenance caveat, stated first

The task asked to reproduce a published multidimensional Caputo physical-state
intersection example from Cong–Tuan (2017). **The text of that paper is not
available in this repository** — only the reference entry and prose summaries.
The construction below was derived independently and is **not verified to be the
published example**. Stage B's stated purpose (validate same-present collision
detection, exercise root refinement, confirm that distinct continuation states
can share a physical endpoint) is met either way. No novelty is claimed: linear
Caputo systems and the zeros of `E_a` are classical.

### The construction, and why it is exact

For `^C D^a x = A x` the solution is exactly `x(t) = E_a(A t^a) x0`. Let `z` be
any non-real zero of `E_a` and put

```
A = [[Re z, -Im z], [Im z, Re z]]      (= |z| R(arg z), eigenvalues z and conj z)
```

The algebra generated by `I` and `J = [[0,-1],[1,0]]` is isomorphic to `C`, so
with `w = E_a(z t^a)`

```
E_a(A t^a) = [[Re w, -Im w], [Im w, Re w]],      det E_a(A t^a) = |w|^2 .
```

At `t = 1`, `w = E_a(z) = 0`, hence `E_a(A)` is the **zero matrix** and

```
x(1; x0) = 0      for EVERY x0 in R^2 .
```

`e_0 . T_1` is therefore *constant* on the reachable set: this is the strongest
possible form of KNOWN-A02, and it is exact algebra once a zero of `E_a` is
known. Existence of zeros is classical: for `0 < a < 1` with `1/a` non-integral,
`E_a` has order `1/a > 1` and non-integral order, so by Hadamard factorisation it
has infinitely many zeros.

### CERTIFIED COMPUTATION — the zero

Located two independent ways and then certified:

* via the closed form (`erfc(-z) = 0`): `z = 1.35481012811200624889985054089 - 1.99146684283387957728215784262 i`;
* via Newton on our own Taylor series: agreement `9.905e-42`;
* **Krawczyk test in Arb ball arithmetic**, `prec = 600` bits, series index
  `K = 200`, box-radius ladder `1e-32 … 1e-4` (the first four radii fail because
  the box is tighter than the achievable enclosure of `E_a` at the centre; the
  largest radius fails because the derivative is not near-constant on it):

```
Re z* in [1.35481012811200624889985054 +/- 1.88e-27]
Im z* in [-1.99146684283387957728215784 +/- 3.61e-27]     UNIQUE zero in the box
E_a(box) = [+/- 1.01e-23] + [+/- 1.03e-23] i              contains 0
```

Evidence class: **CERTIFIED COMPUTATION** (existence *and* uniqueness), with the
arithmetic semantics documented in `msbg/certify.py`.

### Numerical confirmation

Three solvers, five initial states, meshes `N = 1000 … 32000`:
`|x(1)|` at the finest mesh `pi_rect` 6.4e-4, `pece` 8.6e-6, `l1` 7.6e-5,
observed orders 1.005 / 1.494 / 1.079 — i.e. they converge to the predicted
exact zero at their own established rates. An independent arbitrary-precision
(`mpmath`, dps 30) PECE run at `N = 4000` gives `x(1) = (4.39e-5, -3.02e-5)`,
consistent with the same order.

### Collision machinery calibrated

The polyline detector recovers the known collision (`t = 0.999995`,
`s = 0.999998`, `x = (4.4e-7, 2.4e-6)`) and also finds a genuine *cross-age*
crossing of the same two orbits at `t = 0.0358`, `s = 0.3596`.

### A structural fact worth keeping

`d x(t;p)/dp = E_a(A t^a)`, which **vanishes identically** at the collision time.
So this collision is *maximally degenerate* in the initial states: the
`p`- and `q`-columns of the collision Jacobian are zero and all the rank sits in
the two age columns (singular values `1.359, 1.359`, rank 2). A linear
construction therefore cannot be used to test CANDIDATE-M2's nondegeneracy
hypothesis — that test needs the nonlinear model, and is done in Stage D.

---

## 4. Stage C — Double-Allee baseline

### Stage C as specified: HALTED

The task's own stop rule was triggered. Everything this repository contains
about Mondal, R.; Pal, D.; Takeuchi, Y.; Mukherjee, D.; Kesh, D.; Saha, A.
(2025), *Dynamics of a Fractional Order Predator–Prey System with Double Allee
Effect and Group Defense*, Chinese Journal of Physics 98, 613–632,
DOI 10.1016/j.cjph.2025.09.020, is the bibliography entry
`MondalEtAl2025DoubleAlleeFractional` plus one-line role descriptions in
`research/REFERENCES.md`, `research/LITERATURE_MAP.md`,
`research/INHERITED_KNOWLEDGE.md`, `research/NOVELTY_MATRIX.md` and
`research/source/`. There are **no equations, no functional forms** (the
group-defence response is not even named) and **no parameter values**. The same
gap holds for the fallbacks Rahmi et al. (2021), Pal & Saha (2015) and
Contreras Julio & Aguirre (2018).

Rather than guess, the exact missing items are listed in §9 as a web-search
request.

### Stage C′ — substitute baseline, labelled

A **PROJECT-CONSTRUCTED** positive planar strong-Allee Caputo predator–prey
system whose prey growth term is exactly the published Area–Nieto (2023) cubic
recorded in `research/CLAIMS.md` (COROLLARY-S1A), with the standard
Lotka–Volterra predation pair:

```
^C D^a x = x (1 - x)(x - theta) - a x y
^C D^a y = y (b x - m)
```

This is *not* a reproduction of any published parameterisation and is labelled as
such in `msbg/models.py`. A double-Allee variant
`x(1-x)(x-theta)/(x+c) - a x y` is included to check that the Stage-D phenomenon
is not an artefact of one functional form.

**C1/C2 — exact equilibria and the Caputo sector test**, in exact rational and
radical arithmetic (sympy), for the Stage-D witness regime
`theta = 3/10, a = 1, b = 1, m = 4/5`:

| equilibrium | eigenvalues (exact) | Caputo-stable for |
|---|---|---|
| `(0,0)` extinction | `-3/10, -4/5` | all `a in (0,1)` (bound 2.0) |
| `(3/10, 0)` Allee threshold | `-1/2, +21/100` | never (saddle) |
| `(4/5, 1/10)` coexistence | `(-3 +/- i sqrt(41))/25` | `a < 1.27893` |
| `(1, 0)` prey-only | `+1/5, -7/10` | never (saddle) |

So the system is bistable between extinction and coexistence **for every
`a in (0,1)`**, and this is certified by exact arithmetic, not by a numerical
eigenvalue solve. `theta < m/b` also holds exactly, which is the hypothesis the
extinction argument of §5.2 needs. The same table is produced for four other
parameter sets in the same manifest.

Declaring the symbolic unknowns `positive` silently drops every equilibrium on an
axis, including the extinction state the whole task is about; they are declared
real for exactly that reason.

**C3–C5 — outcome classes and three-solver cross-check.** Five initial states
spanning the extinction region, a predator-driven collapse, coexistence, the
Stage-D witness candidate and a high-prey start: **all three solvers agree on all
five labels**, with two outcome classes present. Positivity holds
(`min x = 1.31e-4`, `min y = 3.22e-5`).

**C6 — mesh and horizon sensitivity.** This is where the Stage-D correction
originates and it is reported prominently:

| N (T = 800) | h | max abs difference vs finest |
|---|---|---|
| 2 000 | 0.40 | **nan** (blows up) |
| 4 000 | 0.20 | **7.95e-1** |
| 8 000 | 0.10 | 9.81e-6 |
| 16 000 | 0.05 | 7.16e-7 |

At `h >= 0.2` the explicit product-integration schemes overshoot through `x = 0`
for initial states above the carrying capacity and the cubic then drives a
blow-up. **`h <= 0.1` is the minimum admissible step for this model class, and
Stage D uses `h = 0.01–0.02`.**

Horizon: labels identical at `T = 200, 400, 800, 1600, 3200`.

---

## 5. Stage D — inter-basin collision: a witness

### 5.1 The reduction actually used

`REDUCTION-M1` needs `x(t;p) = x(s;q)` with `p, q` in distinct basins. Three
regimes of that condition were searched; the productive one is the degenerate
age `s = 0`:

* **same-age** `t = s` — square root problem, §5.6;
* **cross-age** `t != s` — transversal crossing of two planar polylines;
* **embedded-age** `s = 0`, i.e. `x(t;p) = q`. Here `q` is itself a physical
  state, so `iota(q) = T_0 iota(q)` is already in `R_alpha` and **no root solving
  is needed at all**. The condition degenerates to

  > the orbit of `p` enters an open set of physical states whose canonical
  > embeddings lie in a different basin,

  which is an **open condition**.

This is the structural point of §0. Write `R_ext` for a set of physical states
with `iota(R_ext) in B(0,0)`, and suppose `iota(p) in B(A)` with `A != (0,0)` and
`x(t*;p) in R_ext`. Then with `z := x(t*;p)`,

```
e_0(T_{t*} iota(p)) = z = e_0(iota(z)),   both in R_alpha,
T_{t*} iota(p) in B(A)                    (positive invariance of basins),
iota(z) in B(0,0)                         (z in R_ext),
```

so `F_z` is multibasin.

Persistence under a perturbation `mu` of the model splits into two halves, and
they are not equally hard:

* the **collision** half — "the orbit of `p` still enters `R_ext`" — persists
  from continuity of `(p, t, mu) -> x(t;p,mu)` and openness of `R_ext` alone.
  **No transversality, no nonsingular minor, no implicit function theorem.**
* the **basin** half — "`iota(p)` is still in `B(A)`, and `iota(R_ext)` is still
  in `B(0,0)`" — does *not* follow from continuity and is the binding
  constraint. §5.8 measures exactly this: across 28 perturbations the collision
  half never failed and the basin half failed 11 times.

In CANDIDATE-M2's own terms (`research/STATE_ARCHITECTURE.md` §5), items 2, 3,
4 and 6 of the nonstandard-burden list are not needed for existence or for
persistence of a multibasin fibre; items 1 and 5 are.

### 5.2 The certified extinction region

For the Stage-C′ model with `theta < m/b`, take

```
R_ext = {(x,y) : 0 < x < theta, y >= 0} .
```

`iota(R_ext) in B(0,0)` follows from ingredients already audited in this
repository — positivity of the cone, the scalar Caputo comparison principle
(Wu 2020, ref. 22) giving `x(t) <= u(t)` for the scalar Allee solution `u` with
`u(0) = x(0)`, COROLLARY-S1A giving `u(t) -> 0` for `u(0) in (0,theta)`, and then
`^C D^a y <= -(m - b theta) y` giving `y(t) <= y(0) E_a(-(m-b theta) t^a) -> 0`.
Label: **CERTIFIED-CONDITIONAL**. The Compute Agent does not promote it; §8.2
lists exactly what the Chief must audit. §5.7 reports a numerical falsification
test of its consequences.

### 5.3 The witness

```
model   ^C D^a x = x(1-x)(x - 3/10) - x y ,   ^C D^a y = y(x - 4/5)
        theta = 0.3,  a = 1,  b = 1,  m = 0.8,  alpha = 0.85
        extinction (0,0)              eigs -3/10, -4/5      Caputo-stable for all a in (0,1)
        Allee threshold (3/10, 0)     eigs -1/2, 21/100     saddle
        prey-only (1, 0)              eigs 1/5, -7/10       saddle
        coexistence E* = (4/5, 1/10)  eigs (-3 +- i sqrt 41)/25   Caputo-stable for a < 1.27893
initial constant history   p = (2.4372, 2.012)
```

Found by `stage_d_scan_v2.py`, validated by `stage_d_witness.py`.

### 5.4 The witness survives every validation the task asked for

**Mesh ladder, three solvers.** `margin = theta - min_t x(t)`, horizon `T = 2000`:

| `h` | `pi_rect` | `pece` | `l1` |
|---|---|---|---|
| 0.08 | 0.098913 | **extinction (qualitatively wrong)** | 0.103699 |
| 0.04 | 0.102260 | 0.105394 | 0.103317 |
| 0.02 | 0.102592 | 0.103342 | 0.103024 |
| 0.01 | **0.102664** | **0.102833** | **0.102835** |

At `h = 0.01` the three solvers — two formulations — agree to `1.7e-4` on a
margin of `0.1028`. The coarsest rung is reported, not hidden: at `h = 0.08`
the PECE scheme flips the *qualitative* outcome to extinction. That step is
already outside the admissible range established in Stage C (§4, C6), but it is
a concrete demonstration that a plausible-looking mesh can manufacture the
opposite conclusion in this model.

**Arbitrary precision.** `stage_d_highprec.py`, mpmath at 30 significant digits,
`h = 0.01`:

```
mpmath  dps=30 : min x = 0.19713188874147125066...  at t = 3.9000
float64 same h : min x = 0.19713188874147125063      at t = 3.9000
|difference|   = 3.05e-12
margin         : mpmath +0.102868111255, float64 +0.102868111259
min y          : 3.290245e-02 (both)  -> positivity holds
```

The dip is **not** a floating-point artefact.

**Horizon ladder and the approach to the attractor.** With `h = 0.02` fixed:

| `T` | `dist(x(T), E*)` | fitted decay exponent |
|---|---|---|
| 500 | 1.61e-2 | −0.794 |
| 1000 | 9.11e-3 | −0.818 |
| 2000 | 5.11e-3 | −0.832 |
| 4000 | 2.86e-3 | −0.840 |
| 8000 | **1.59e-3** | **−0.844** |

The linearised Caputo prediction at a locally asymptotically stable equilibrium
is algebraic decay with exponent `-alpha = -0.85`. The measured exponent climbs
monotonically towards it. This is the strongest available finite-horizon
evidence that the orbit really is converging to `E*` and is not, say, on a slow
limit cycle — but it is still not a basin proof (§8.1).

**Positivity.** Along the witness orbit `min x = 0.19663`, `min y = 0.03206`.

### 5.5 Not a point — an arc of multibasin fibres

The orbit of `p` is inside `R_ext` for

```
t in [1.26, 35.74]       (1725 mesh points at h = 0.02, all verified inside R_ext)
x(t) in [0.196626, 0.299953],   y(t) in [0.036152, 1.698559]
deepest point   z* = (0.196626, 0.032057)   at t = 3.90
```

so there is a **one-parameter family** of multibasin reachable present-state
fibres `{F_{x(t;p)} : t in [1.26, 35.74]}`, not a single accidental one.

**Nondegeneracy.** For the embedded-age condition `H(p,z,t,0) = x(t;p) - z`
the derivative in `z` is `-I`, so transversality in `z` is automatic; the
informative test is the rank in the remaining declared variables. At the deepest
point, with free variables `(p_1, p_2, t)`:

```
singular values of D_{(p,t)} H  =  [0.24375, 0.07923],   rank 2 (full row rank)
```

so the collision map is a submersion there. This is the CANDIDATE-M2
nondegeneracy hypothesis, satisfied — and, by §5.1, not actually needed for
existence or persistence.

### 5.6 Same-age and cross-age collisions

`stage_d_witness.py` D7 paired the witness `p` with the certified-extinction
start `q = (0.1, 0.1)`: **0 same-age collisions, 0 cross-age crossings**. That is
expected — two arbitrary planar orbits need not meet — and it is reported as a
null result, not suppressed.

`stage_d_sameage.py` attacks the strict condition properly, by *solving* for `q`
rather than guessing it: fix an age `t` in the sub-threshold window and solve the
square system `Phi_t(q) = x(t;q) - x(t;p) = 0` over the extinction-labelled part
of a search box, with a projected Newton clipped to the box.

> **Correction recorded.** The first version of this search was wrong. It let
> Newton leave the box, and Newton went to the trivial root `q = p`, reporting
> `|H| ~ 1e-15` at five of nine ages with `q* = p` to machine precision. Those
> "roots" were the reference orbit itself. v2 clips the iterate to the box and
> rejects iterates approaching `p`. The buggy output is not part of the record;
> the fix is commit `63f7e87`.

**Result: NEGATIVE, in two runs of increasing search range.**

| run | search box | grid | extinction-labelled | roots found | smallest image gap |
|---|---|---|---|---|---|
| narrow | `(0,1.6] x (0,5]` | 50 x 50 | 2242 (500 certified) | 0/9 | 2.46e-2 at `t = 26.29` |
| wide | `(0,8] x (0,20]` | 64 x 64 | 2095 (192 certified) | 0/9 | **9.65e-3** at `t = 17.95` |

The informative quantity is the **image gap**: the distance from `x(t;p)` to the
image of the extinction-labelled grid under the time-`t` map. Widening the box
by a factor of five in each direction cut the gap by 2.5x but did not close it:

| `t` | 1.26 | 5.43 | 9.60 | 13.77 | 17.95 | 22.12 | 26.29 | 30.46 | 34.63 |
|---|---|---|---|---|---|---|---|---|---|
| gap, narrow box | 1.16e-1 | 7.78e-2 | 5.82e-2 | 4.29e-2 | 3.29e-2 | 2.66e-2 | 2.46e-2 | 2.63e-2 | 2.48e-2 |
| gap, wide box | 4.09e-2 | 1.88e-2 | 1.14e-2 | 9.84e-3 | **9.65e-3** | 1.15e-2 | 1.54e-2 | 2.23e-2 | 2.96e-2 |

**Two limitations of this search, declared rather than glossed.**

1. *The root-finder contributes nothing here.* `Phi_t` always has the trivial
   root `q = p`, and in the wide-box run the projected Newton was pinned against
   the guard sphere around `p` at **every** age — `distance_to_p = 1.000e-3`
   exactly, nine times out of nine, with `q*` labelled COEXISTENCE. The guard
   radius (`1e-3`) is too small to escape the trivial root's basin of
   attraction. So the negative result rests entirely on the **grid image gap**,
   which is computed without Newton, and not on the refinement.
2. *Part of the wide box is excluded for numerical, not dynamical, reasons.*
   1331 of 4096 grid points are DIVERGENT at the labelling step size
   `h = 0.02`, because initial prey densities up to `x = 8` need a finer mesh
   (§4, C6). Those points are not available as candidates. A correct wide-box
   search needs a graded or adaptive mesh in the labelling phase.

**Interpretation, stated carefully.** A negative search is not an impossibility
theorem (PROTOCOL.md), and this one is weaker than a clean negative because of
the two limitations above. What it does establish is that the *strict* same-age
form of `REDUCTION-M1` is much harder to realise here than the embedded-age
form, which is unsurprising: the embedded-age condition is open (codimension 0),
whereas the same-age condition asks a specific point to lie in the image of a
set under a specific time-`t` map. The multibasin fibre does **not** need the
same-age version — `T_t iota(p)` and `iota(z)` already sit in the same fibre with
`z = x(t;p)`. The Chief should note that the Cong–Tuan same-age intersection
phenomenon and the multibasin-fibre phenomenon are *different requirements*, and
only the second is needed for TARGET-A20.

### 5.7 Falsification test of the certified extinction region

`stage_d_certified_region.py`, 484 constant histories filling
`R_ext = (0, 0.3) x [0, 5]`, `T = 800`, `h = 0.04`, `alpha = 0.85`:

| test | result |
|---|---|
| T1 positivity of every trajectory | min over all trajectories `0.000e+00` — **PASS** |
| T2 every trajectory labelled EXTINCTION | 484/484 EXTINCTION, 0 coexistence, 0 ambiguous — **PASS** |
| T3 comparison inequality `x(t) <= u(t)` | worst excess `+4.39e-15` (round-off), 0 violating trajectories — **PASS** |
| T4 barrier property `0 < u(t) < theta` | min `1.86e-07`, max `0.300000` — **PASS** |
| T5 predator bound `y(t) <= y(0) E_a(-(m - b theta) t^a)` | worst excess `0.000e+00`, 0 violating trajectories — **PASS** |

Passing does not prove the CERTIFIED-CONDITIONAL claim; a single failure would
have refuted it. In particular T3 and T5 are direct numerical checks of the two
comparison steps the Chief has to justify analytically.

### 5.8 Persistence: what is robust and what is not

`stage_d_witness.py` D6 perturbs one quantity at a time by `+-2%` and `+-5%`
(`alpha, theta, a, b, m, p_1, p_2`), 28 runs, holding everything else fixed.
**17/28 keep the witness.** The failures are one-sided and completely
systematic — and, crucially:

```
failures in which the COLLISION was lost (orbit no longer enters R_ext):   0 / 28
failures in which only SURVIVAL was lost (orbit enters R_ext, then dies): 11 / 28
```

| perturbed | −5% | −2% | +2% | +5% |
|---|---|---|---|---|
| `alpha` | keep | keep | survival lost | survival lost |
| `theta` | keep | keep | survival lost | survival lost |
| `a` | keep | keep | keep | survival lost |
| `b` | keep | keep | keep | survival lost |
| `m` | survival lost | survival lost | keep | keep |
| `p_1` | survival lost | survival lost | keep | keep |
| `p_2` | keep | keep | keep | survival lost |

Read this carefully, because it is the sharpest empirical statement in the
return: **the collision half of the construction never failed under any
perturbation; the only thing that ever fails is basin membership.** That is
precisely item 1 of the CANDIDATE-M2 burden list, and it says the theorem effort
should go there and not into transversality.

This particular `p` sits near the survival edge of the witness set — as any
maximiser of the margin would. It is not the interior of the witness set: at
`alpha = 0.85` alone, `stage_d_scan_v2.py` found **92 mesh-reliable witnesses**
over the searched grid, so the set of witnessing initial states has substantial
size at fixed parameters.

### 5.9 Order dependence

`stage_d_scan_v2.py`: 85 configurations (family x theta x x* x a x alpha),
1296 constant histories each at `h = 0.01`, positivity enforced as a hard
filter, candidates re-run to `T = 2000` at `h = 0.04` and `h = 0.02`.
**219 mesh-reliable witnesses** (mesh difference below 5% of the margin) out of
372 long-horizon candidates:

| `alpha` | 0.55 | 0.65 | 0.75 | 0.85 | 0.92 |
|---|---|---|---|---|---|
| orbits recovering above `theta` (phase 1, out of 22 032 each) | 2 | 366 | 849 | 531 | 72 |
| mesh-reliable witnesses (phase 2) | **0** | 6 | 88 | 92 | 33 |
| largest margin | — | 0.02556 | 0.07849 | 0.10409 | 0.06824 |

Witnesses exist across `alpha in [0.65, 0.92]`, and 28 of the 219 are in the
double-Allee family rather than the single-Allee one, so the phenomenon is neither a single-order accident nor
an artefact of one functional form. The `alpha = 0.55` column is a **negative
search result** under a strict finite-horizon classifier, not an impossibility:
see §8.5 for why small `alpha` is out of reach at this cost.

Figure `figures/F5_alpha_dependence.png`.

---

## 6. The mechanism, stated sharply

This is the part the Chief should read even if nothing else survives review.

**Why the integer-order system cannot do this.** On
`R_ext = {0 < x < theta, y >= 0}` the prey field is strictly negative:

```
g_x(x,y) = x(1-x)(x-theta) - a x y < 0        for 0 < x < theta, y >= 0,
```

because `(1-x) > 0`, `(x-theta) < 0` and `a x y >= 0`. For `alpha = 1`,
`x' = g_x < 0` means `x` is *decreasing*; it can never return to `theta`; being
bounded below by `0` it converges, and the limit must be `0`. So for `alpha = 1`
**no survival-bound orbit can enter `R_ext` at all**, and `R_ext` is contained in
the extinction basin.

**Why the Caputo system can.** For `0 < alpha < 1` the implication

```
^C D^alpha x(t) < 0  on an interval    =>    x decreasing there
```

is **false**. Writing `x(t) = x0 + I^alpha[phi](t)` with `phi = g_x(x,y) <= 0`,
for `t1 < t2`

```
x(t2) - x(t1) = (1/Gamma(a)) [ int_0^{t1} ((t2-s)^{a-1} - (t1-s)^{a-1}) phi(s) ds
                             + int_{t1}^{t2} (t2-s)^{a-1} phi(s) ds ] .
```

Since `a - 1 < 0`, the bracket in the first integral is *negative* while `phi` is
negative, so that term is **positive**. The two terms compete and the sign of the
increment is genuinely indefinite. The fixed lower terminal at `0` is exactly
what makes this possible — which is precisely the "fixed-lower-terminal Caputo
memory" item the Chief listed as the nonstandard burden of CANDIDATE-M2
(`research/STATE_ARCHITECTURE.md` §5, item 5). Here it is not a burden, it is the
engine.

The witness is a direct, checkable instance of that failure: on the recovery
window its Caputo derivative is strictly negative throughout (by the algebra
above, not by measurement) while `x` climbs from its minimum back through
`theta`. The numbers for the window are in §5.

**Consequence for the project.** The phenomenon is not "memory makes basins
fuzzy". It is sharper: *the equivalence between the sign of the derivative and
monotonicity, which is what makes the integer-order Allee threshold an absolute
barrier, is destroyed by power-law memory — while the comparison principle that
makes the sub-threshold region attract from a cold start survives.* That
asymmetry is the whole construction.

---

## 7. Stop conditions — one triggered (Stage C)

The task listed five stop conditions. Status of each:

| stop condition | status |
|---|---|
| the two solvers disagree beyond convergence expectations | **not triggered** — pairwise differences 1.9e-4 … 1.6e-3 at the finest mesh, consistent with the observed orders |
| the published baseline cannot be faithfully reconstructed | **TRIGGERED for Stage C**, handled by halting Stage C and labelling the substitute (§4) |
| collision candidates vanish under mesh/horizon refinement | **not triggered** — the witness margin is stable across four meshes, five horizons and three solvers, and is reproduced to 3e-12 at 30 digits; but see §5.4 on the coarsest rung, where PECE flips the outcome |
| only boundary/ambiguous outcomes are found | **not triggered** — two clean outcome classes, all three solvers agreeing on all five test labels; the search box of §5.6 had 0 ambiguous out of 2500 |
| the candidate Jacobian is rank-deficient at all robust roots | **not triggered** — the embedded-age Jacobian has full row rank 2 (§5.5) |

---

## 8. What is NOT established — the honest gap list

1. **The survival side is numerical.** `T_t iota(p) in B(E*)` rests on a
   finite-horizon tail test plus horizon/mesh/solver stability. It is *not* a
   basin proof. What would close it: a trapping region in the continuation-state
   space `C(R_+, R^2)` for the coexistence attractor. The natural tools already
   in the local bibliography are Doan & Kloeden (2024), *Attractors of Caputo
   Semi-Dynamical Systems* (ref. 18), and the Caputo linearisation/Mittag-Leffler
   stability theory. **This is the single most valuable next theorem.**

2. **The extinction side is CERTIFIED-CONDITIONAL, not proved here.** It needs
   three ingredients the Chief must audit and assemble:
   (a) invariance of the positive cone for this Caputo system — used but not
   proved here, only verified numerically over every tested trajectory;
   (b) the scalar Caputo comparison principle in the form
   `^C D^a x <= f(x), x(0)=u(0)  =>  x <= u` — Wu (2020), ref. 22 in
   `research/REFERENCES.md`; its exact hypotheses must be checked against this
   vector field;
   (c) COROLLARY-S1A from `research/CLAIMS.md` for the scalar Allee cubic.
   Plus `theta < m/b`, which is exact arithmetic.
   The Compute Agent does not promote this to a theorem.

3. **Stage B is not verified to be the Cong–Tuan example.** The source text is
   not local. The mechanism is independently derived and certified, but the claim
   "we reproduced their construction" is *not* made.

4. **The model is PROJECT-CONSTRUCTED.** Nothing here reproduces a published
   fractional Double-Allee parameterisation, because none is recoverable locally.
   The applied realisation the Charter prefers is therefore still open.

5. **Small `alpha` is beyond the affordable horizon.** Convergence to either
   attractor is algebraic, `dist ~ t^{-alpha}`, so a strict tail test at
   `alpha = 0.3` would need `T ~ 10^5`–`10^6` with `h <= 0.02`, i.e. `N ~ 10^7`
   and `O(N^2)` history work. With a uniform-mesh quadratic-cost solver that is
   not affordable. **The absence of witnesses at `alpha = 0.55` in the searched
   window is a negative search result, not an impossibility.** Closing this needs
   either fast convolution quadrature (`O(N log^2 N)`) or graded meshes.

6. **No interval certification of a trajectory.** C-A022 remains open for the
   nonlinear model: `msbg/certify.py` certifies the Stage-B special-function
   root rigorously, but no validated integrator for the Caputo IVP is implemented,
   so no trajectory-level enclosure exists.

---

## 9. What the Compute Agent needs next

### 9.1 For the Deep Web Search Agent (blocking Stage C)

Exactly these items, for Mondal, R.; Pal, D.; Takeuchi, Y.; Mukherjee, D.;
Kesh, D.; Saha, A. (2025), Chinese Journal of Physics 98, 613–632,
DOI 10.1016/j.cjph.2025.09.020:

1. the state equations, with the explicit double-Allee factor and the
   group-defence functional response written out;
2. the parameter values of the multistable regime whose basins the paper
   computes, with the figure/table they belong to;
3. the fractional orders used there, commensurate and incommensurate;
4. the coordinates of the attractors reported in that regime, so a reproduction
   can be *checked* rather than asserted.

Same four items for any one of Rahmi et al. (2021) *Fractal Fract.* 5(3) 84,
Pal & Saha (2015), or Contreras Julio & Aguirre (2018), as a fallback.

Additionally, and now much more sharply targeted than a broad round:

5. **is there a published theorem stating that a Caputo trajectory of a positive
   bistable system can cross an Allee threshold and recover?** The searchable
   phrasing is non-monotonicity of solutions with sign-definite Caputo
   derivative, or failure of the derivative/monotonicity equivalence for
   `0 < alpha < 1`. This is the mechanism of §6 and it is the thing most likely
   to already exist in the literature in some form.
6. **is there a published basin-of-attraction theorem in the Doan–Kloeden
   continuation-state space** (as opposed to the physical state), which would
   supply the missing survival-side trapping argument of §8.1?

### 9.2 For the Chief (theorem work, in priority order)

1. **Survival-side trapping in the continuation-state space** (§8.1). Without it
   the witness stays numerical.
2. **Assemble the extinction-side proposition** from (a)+(b)+(c) in §8.2 and
   decide whether it is promoted; if it is, the extinction half of every fibre in
   the sub-threshold arc becomes rigorous.
3. **Restate CANDIDATE-M2 using the open-condition argument of §5.** The IFT and
   the nondegeneracy hypothesis are not needed for *existence and persistence* of
   a multibasin fibre. They are needed only for the stronger statements — a
   locally unique collision, a smooth collision manifold, or `alpha`-differentiability.
   The numerical Jacobian evidence in §5 supports the stronger version too, but
   the cheap version is the one that should carry the main theorem.
4. Decide whether the applied realisation must be a *published* Double-Allee
   model (then Stage C has to be unblocked first) or whether a
   project-constructed positive strong-Allee predator–prey system, with the
   published Area–Nieto cubic as its prey term, is acceptable for the manuscript.

### 9.3 Next compute task the Compute Agent recommends

`TASK-0002`: once the Chief fixes the trapping hypotheses, implement
(i) a validated/interval Caputo integrator sufficient to enclose the witness
orbit on `[0, t*]` and to certify entry into `R_ext`, and (ii) fast convolution
quadrature so the small-`alpha` end of the persistence interval becomes
affordable. Together these would move the witness from NUMERICAL CORROBORATION
to CERTIFIED COMPUTATION on both sides.

---

## 10. Reproduction

### 10.1 Hosts and environments

Both hosts named in `COMPUTE_AGENT_INITIAL_PROMPT.md` are in use. AUREUS had no
scientific Python stack at the start of the task and was provisioned for it
(venv with numpy/scipy/mpmath/python-flint/sympy/matplotlib/pytest, key-based
access, no credentials in any committed file).

| host | role | CPU / RAM | python | numpy | scipy | mpmath | python-flint |
|---|---|---|---|---|---|---|---|
| ORION | large multi-process sweeps (shared machine, jobs niced, 1 BLAS thread per worker) | 344 threads (2 x Xeon 6787P) / 1007 GB | 3.12.3 | 2.5.3 | 1.18.1 | 1.4.1 | 0.9.0 |
| AUREUS (`aur007`) | single-process high-thread stages and arbitrary-precision work | 32 threads / 186 GB | 3.12.3 | 2.5.3 | 1.18.1 | 1.4.1 | 0.9.0 |
| R11 (local) | development and the test suite | 32 threads / 62 GB | 3.14.3 | 2.4.4 | 1.17.1 | 1.3.0 | 0.9.0 |

Every manifest under `computations/manifests/` records the host, all package
versions, the numpy BLAS build, the wall time, the project seed
(`msbg.provenance.SEED = 20260929`) and a SHA-256 for each artifact it wrote.
The launchers export the local git SHA to the remote runs, because the remote
copies are rsync'd trees rather than checkouts.

Which stage ran where: Stage A, Stage B, `stage_d_scan_v2`, `stage_d_witness` on
ORION; Stage C, `stage_d_certified_region`, `stage_d_highprec`,
`stage_d_sameage` on AUREUS; the pytest suite locally. An early exploratory pass
also used the R39 fallback host named in `AGENTS.md` while AUREUS was being
provisioned; nothing in this report depends on it.

### 10.2 Exact commands

```bash
cd computations
python3 -m venv venv
./venv/bin/pip install numpy scipy mpmath python-flint sympy matplotlib pytest
export OMP_NUM_THREADS=1

python scripts/stage_a_validate.py
python scripts/stage_b_intersection.py
python scripts/stage_c_baseline.py
python scripts/stage_d_scan_v2.py --workers 40
python scripts/stage_d_witness.py --theta 0.3 --a 1.0 --b 1.0 --m 0.8 \
       --alpha 0.85 --p 2.4372 2.012 --T 2000 --N 100000
python scripts/stage_d_highprec.py --theta 0.3 --a 1.0 --b 1.0 --m 0.8 \
       --alpha 0.85 --p 2.4372 2.012 --T 50 --N 5000 --dps 30
python scripts/stage_d_certified_region.py --theta 0.3 --a 1.0 --b 1.0 --m 0.8 \
       --alpha 0.85 --T 800 --h 0.04 --nx 22 --ny 22 --ymax 5.0
python scripts/stage_d_sameage.py --theta 0.3 --a 1.0 --b 1.0 --m 0.8 \
       --alpha 0.85 --p 2.4372 2.012 --T 200 --h 0.01 --nq 64 \
       --qxmax 8.0 --qymax 20.0 --label-T 400 --label-h 0.02
python scripts/make_figures.py
pytest tests/ -q
```

On the remote hosts, `scripts/sync_orion.sh push` / `scripts/sync_aureus.sh push`
followed by `THREADS=n scripts/run_orion.sh <script> [args]` or
`THREADS=n scripts/run_aureus.sh <script> [args]`, then `... pull`.

The two superseded coarse-mesh scans (`stage_d_regime_scan.py`,
`stage_d_focus_scan.py`) are kept in the repository together with their data so
that the `h = 0.1` correction described in `computations/README.md` is auditable.

### 10.3 Artifacts

```
computations/msbg/           library (7 modules)
computations/scripts/        11 stage scripts + 4 host helpers
computations/tests/          61 checks: 60 passed, 1 skipped
computations/data/           raw json / npz for every stage
computations/manifests/      per-run environment + artifact hashes
computations/figures/        F1..F5
computations/reports/EVIDENCE_LEDGER.md   one line per assertion, with its class
```

Figures, each answering one theorem-level question:

| figure | question it answers |
|---|---|
| `F1_witness_orbit.png` | does a survival-bound orbit enter the certified extinction region? |
| `F2_caputo_mechanism.png` | what is the Caputo-specific mechanism? (`x` rises while `^C D^a x < 0`) |
| `F3_solver_convergence.png` | are the solvers trustworthy? |
| `F4_stageB_collapse.png` | is reachable present-state observation non-injective in `d = 2`? |
| `F5_alpha_dependence.png` | over which fractional orders does the witness persist? |

### 10.4 Corrections made during this task, recorded rather than hidden

1. **Coarse-mesh scans produced false margins.** `h = 0.1` gave "margins" up to
   3.35, every one of which left the positive cone. Superseded by
   `stage_d_scan_v2.py` at `h = 0.01`; both the wrong and the right runs are in
   the repository (§ `computations/README.md`).
2. **The first candidate-ranking selected the wrong trajectories.** Ranking dips
   by depth selects the orbits that go extinct, since those dip deepest. Fixed by
   restricting candidates to orbits that recover above `theta`.
3. **The first same-age search converged to the trivial root.** Unconstrained
   Newton left the box and returned `q* = p` with `|H| ~ 1e-15`. A projected
   Newton with a guard against `p` (commit `63f7e87`) stops the false positive,
   but does **not** make the refinement useful: in the wide-box run it sits on
   the guard sphere at every age. The same-age conclusion is therefore drawn
   from the grid image gap and explicitly not from the root-finder (§5.6).
4. **The first high-precision check used an inadmissible step.** At `h = 0.1`
   both mpmath and float64 go extinct and agree only with each other. Redone at
   `h = 0.01` in `stage_d_highprec.py`.
5. **A Mittag-Leffler quadrature bug and a series-truncation bug** were caught by
   the test suite (a degenerate quadrature split point for the branch-cut
   integral; a truncation criterion measured against the peak term instead of
   the answer). Both fixed; Stage A and Stage B were re-run afterwards.

### 10.5 Branch and commit

```
branch: compute/task-0001
final commit SHA: FINAL_SHA_PLACEHOLDER
```

---

## 11. Next question for the Chief

> Is there a trapping region in the Doan-Kloeden continuation-state space
> `C(R_+, R^2)` for the coexistence attractor of a positive strong-Allee Caputo
> predator-prey system — one that a numerically computed orbit can be *verified*
> to enter?

Everything else in this return is either certified, conditionally certified on
results the repository already audits, or a clearly labelled negative search.
That one question is what stands between the witness and TARGET-A20.
