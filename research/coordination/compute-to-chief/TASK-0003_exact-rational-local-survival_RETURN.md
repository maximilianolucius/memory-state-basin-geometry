# TASK-0003 — Exact-rational locally certified survival witness — COMPUTE RETURN

**From:** Compute Agent
**To:** Chief Researcher
**Task:** `research/coordination/chief-to-compute/TASK-0003_exact-rational-local-survival_REQUEST.md`
**Date:** 2026-09-29
**Branch:** `compute/task-0003`
**Final commit SHA:** `6e2352733c` (§9)

---

## 0. Executive answer

**The goal of this task cannot be met, and the reason is logical, not
computational.** No witness can have its survival certified from time zero by
CANDIDATE-L1 and also enter `R_ext`. §1 gives the argument; it uses only L1's own
conclusion and THEOREM X1.

| Stage | Verdict |
|---|---|
| A/B — exact-rational L1 certificates | Done. 1500 rational parameter sets, exact `P`, verified L1 inequality. |
| C — orbits started inside the certified ellipsoid | **No orbit enters `R_ext`.** Closest approach stops at 94.6% of the distance to the threshold. |
| D — exact-rational entry certificates | **CERTIFIED COMPUTATION**, 3 of 3, including the archival TASK-0001 witness with `alpha = 17/20`. |
| E — overshoot-permitting certificate | **Not feasible** in the form tried. Proved for Hurwitz `J`; grid evidence only for the non-Hurwitz regime. |

TARGET-A20 is **not** closed by this task. What the task does deliver is a
precise statement of which kinds of survival certificate are excluded, so the
theorem effort is not spent on them.

---

## 1. Why the L1 route is self-defeating

**Proposition O1 (obstruction).** Assume THEOREM X1 and the conclusion of
CANDIDATE-L1. Let `Omega = { z : V(z - E*) < lambda_min(P) r^2 }` be an L1-certified
set. Then `Omega` does not meet `R_ext`, and no orbit of a standard initial state
`p in Omega` ever enters `R_ext`.

*Proof.* (i) Suppose `z in Omega` with `0 < z_x < theta`, `z_y >= 0`. L1 applied to
the cold start `iota(z)` gives convergence to `E*`. X1 applied to the same cold
start gives convergence to `(0,0)`. Since `E* != (0,0)`, contradiction. So
`Omega` and `R_ext` are disjoint.
(ii) L1's conclusion includes `V(u(t)) <= V(u(0))` for all `t >= 0`
(`research/LOCAL_SURVIVAL_BASIN.md` §2: "the scalar comparison/stability step that
keeps `V` below its initial value"). Hence the orbit of `p in Omega` stays in the
sublevel set `{V <= V(u(0))}`, which is contained in `Omega`. By (i) it never
meets `R_ext`. `QED`

**Status:** THEOREM/analytic, conditional on X1 (PROVED) and on L1's conclusion.
It does not need L1 to be true: if L1 is false there is nothing to certify with.

**Generalisation.** The same argument excludes every certificate of the form
"a set `S` of physical states, forward invariant under the physical orbits that
start in it, all of whose cold starts are in `B(E*)`". A successful survival
certificate must let the orbit leave the set it starts from. This is the project
mechanism again: basin membership is not a function of the present state.

**Consequence for the task text.** The search geometry proposed in the request —
`theta` near one, "a threshold gap small enough that a locally stable trajectory
can still undershoot" — cannot work for any parameter value. The numbers below
also show that `theta` near one is the *worst* region for L1.

---

## 2. Stage A/B — exact-rational L1 certificates

Command: `python scripts/t3_stageAB_l1_scan.py`. Module: `msbg/lyapunov_l1.py`.

### 2.1 What is exact

All parameters are `fmpq` rationals. Exactly computed: `x* = m/b`,
`y* = (1-x*)(x*-theta)/a`, `J`, `tr J = x*(1+theta-2x*)`, `det J = a b x* y*`, the
Hurwitz test (rational sign tests), and `P` from `J^T P + P J = -I` as an exact
3x3 rational linear solve, with the residual checked to be exactly `-I`.

Enclosed in Arb (200 bit): `lambda_min(P)`, `||P||_2 = lambda_max(P)`, `C_r`.

### 2.2 The remainder and `C_r`

With `u = z - E*` the Taylor expansion of `F` at `E*` is finite:

```
N1(u) = -(3x* - 1 - theta) u1^2 - a u1 u2 - u1^3 ,        N2(u) = b u1 u2 .
```

For `||u||_2 <= r`: `u1^2 <= ||u||^2`, `|u1 u2| <= ||u||^2 / 2`, `|u1|^3 <= r ||u||^2`, so

```
C_r = sqrt( (|3x* - 1 - theta| + a/2 + r)^2 + b^2/4 ) .
```

This is rigorous and slightly loose. `r_cert` is a rational found by bisection
and the inequality `2 ||P||_2 C_r r <= 1/2` is then **verified** at `r_cert` in Arb.

### 2.3 Certificate for the TASK-0001 parameter set

`theta = 3/10, a = b = 1, m = 4/5`:

```
E*      = (4/5, 1/10)
J       = [[-6/25, -4/5], [1/10, 0]],   tr J = -6/25,   det J = 2/25      Hurwitz
P       = [[75/32, 5/8], [5/8, 81/4]]                                    exact
lam_min = 2.3219615...,   ||P||_2 = 20.271788...
r_cert  = 7319003/10^9 = 0.007319003,   C_r = 1.6832927...,   2||P||C_r r = 0.49949786 <= 1/2
Omega   : x half-width 0.0073150686;   gap x* - theta = 1/2;   ratio 0.0146
```

The TASK-0001 witness `p = (6093/2500, 503/250)` is at distance 2.5 from `E*`;
`Omega` has radius 0.007. It is certified **not** to be in `Omega`.

### 2.4 Scan

Grid: `theta in {1/10,...,19/20}` (10 values), `x* = theta + f(1-theta)` with
`f in {11/20, 3/5, 7/10, 4/5, 9/10, 19/20}`, `a, b in {1/4, 1/2, 1, 2, 4}`. 1500 sets, all Hurwitz.

| quantity | value |
|---|---|
| sets where `Omega` reaches the strip (would refute L1 against X1) | **0 of 1500** |
| max of (x half-width of `Omega`) / (gap `x* - theta`) | **0.05435** |
| median | 0.00196 |
| min | 2.7e-7 |

Best ratio by `theta`:

| `theta` | 1/10 | 1/5 | 3/10 | 2/5 | 1/2 | 3/5 | 7/10 | 4/5 | 9/10 | 19/20 |
|---|---|---|---|---|---|---|---|---|---|---|
| best ratio | 0.0429 | 0.0442 | 0.0451 | 0.0472 | 0.0536 | 0.0539 | 0.0544 | 0.0383 | 0.0143 | 0.0040 |

Best set: `theta = 7/10, x* = 91/100, a = 1/4, b = 2`: `r_cert = 0.01175`,
`||P||_2 = 13.83`, x half-width `0.01141`, gap `21/100`.

**Reading.** L1 survives this falsification test everywhere. In the best case the
certified ellipsoid covers 5.4% of the distance to the threshold. As `theta -> 1`
the ratio collapses, because `det J = b x*(1-x*)(x*-theta)` tends to zero and
`||P||_2` blows up (`1.0e4` at `theta = 9/10, x* = 24/25`).

Evidence class: **CERTIFIED COMPUTATION** for the constants. The basin statement
is **L1-CONDITIONAL**.

---

## 3. Stage C — orbits started inside `Omega`

Command: `python scripts/t3_stageC_inside_omega.py --workers 10` (AUREUS).

The eight best sets of §2.4 plus the TASK-0001 set; `alpha in {1/2, 7/10, 17/20, 19/20}`;
64 initial states on the ellipse `V = 0.998 lambda_min r_cert^2`; `T = 400`;
two solvers (PECE, rectangle) and two meshes (`h = 0.02, 0.01`). 144 runs, 9216 orbits.

| quantity | value |
|---|---|
| orbits that cross below `x = theta` | **0** |
| max over all runs of `sup_t V(u(t)) / V(u(0))` | **1.00000000** |
| closest approach, `min_t (x(t) - theta)/(x* - theta)` | **0.945763** |

The closest approach equals `1 - (x half-width)/gap` for each set, e.g. `0.945763
= 1 - 0.054237`: the orbits never leave `Omega` in the `x` direction, which is what
Proposition O1 predicts. The result is the same for all four fractional orders
to six digits.

`sup V/V(0) = 1` is attained at `t = 0`: the numerical orbits satisfy L1's
conclusion. This is a falsification test that L1 passed, not a proof of L1.

Evidence class: NUMERICAL CORROBORATION.

---

## 4. Stage D — exact-rational entry certificates

Command: `python scripts/t2_stageA_certify.py --exact-rational ...` (ORION).
The verifier of TASK-0002 now takes parameters, `alpha` and `p` as the exact
rationals their strings denote (`msbg.validated.to_arb`). Test
`test_exact_rational_inputs_differ_from_binary64` checks that the ball for
`17/20` and the ball for the double `0.85` do not overlap.

`N = 8000`, grading 3, `K = 64`, 128 bit.

| witness | exact inputs | time box | rigorous `x` box | `y >=` | `eta` | `max U` | contiguous certified interval |
|---|---|---|---|---|---|---|---|
| **W1** (TASK-0001) | `theta=3/10, a=b=1, m=4/5, alpha=17/20, p=(6093/2500, 503/250)` | [3.387705, 3.389048] | [0.195165, 0.201521] | 0.655495 | **0.098479** | 7.222e-3 | [1.2605, 4.0] |
| B2 | `theta=1/5, a=b=1, m=2/5, alpha=3/4, p=(6787/10000, 2809/10000)` | [30.975284, 30.987498] | [0.188302, 0.189013] | 0.053345 | **0.010987** | 1.586e-3 | [16.2518, 36.0] |
| B3 | `theta=1/5, a=b=1, m=2/5, alpha=3/4, p=(8821/10000, 3983/10000)` | [20.950929, 20.959035] | [0.177217, 0.177561] | 0.106346 | **0.022439** | 2.927e-4 | [8.9750, 23.0] |

All three: bootstrap passed, verdict **CERTIFIED COMPUTATION**, semantics as in
the TASK-0002 return §2.

The W1 certificate with exact rationals agrees with the binary64 certificate of
TASK-0002 in every reported digit. The separation test uses `theta` rounded down
one ulp, so `eta` is a lower bound.

**What remains binary64, by design.** The mesh points and the nodal values of
`phi` are untrusted binary64 numbers, used exactly. The time-box endpoints are
those mesh doubles. They are not parameters of the theorem.

**Caveat on B2 and B3.** Their rational `p` is the TASK-0002 candidate rounded to
four decimals (a shift of at most `4e-5`). Entry is certified for the rational
`p`. The three-solver survival evidence of TASK-0002 was obtained for the
unrounded binary64 `p` and has **not** been repeated for the rounded one.

---

## 5. Stage E — an overshoot-permitting certificate

By §1 a certificate can only work if the orbit may leave its starting set. The
variation-of-constants formula gives one:

```
u(t) = Phi(t) u0 + int_0^t Psi(t-s) N(u(s)) ds,
Phi(t) = E_alpha(J t^alpha),    Psi(s) = s^{alpha-1} E_{alpha,alpha}(J s^alpha).
```

In a weighted max-norm `|u|_w = max(|u1|/w1, |u2|/w2)`, with
`K = int_0^inf ||Psi||_w`, `|N(u)|_w <= C(r)|u|_w^2`,
`C(r) = max(|c2| w1 + a w2 + w1^2 r, b w1)`, `c2 = 3x* - 1 - theta`, the ball
`{sup_t |u|_w <= r}` is invariant if `sup_t|Phi u0|_w + K C(r) r^2 <= r`, and
`2 K C(r) r < 1` gives `u -> 0`. The starting set is strictly smaller than the
ball, so O1 does not apply.

Entry needs `u1 < -g`, `g = x* - theta`, hence `w1 r > g`. So a **necessary**
condition is

```
q := min over weights of  2 K C(g/w1) (g/w1)  <  1 .
```

### 5.1 Proposition O2 — not feasible when `J` is Hurwitz

Since `int_0^inf Psi(s) ds = -J^{-1}`, `K >= ||J^{-1}||_w`, with

```
J^{-1} = [[0, 1/(b y*)], [-1/(a x*), f'(x*)/(a b y*)]],   y* = (1-x*) g / a .
```

Take `w1 = 1`, `omega = w2/w1`. The condition `q < 1` requires both

```
2 g b / (omega a x*) < 1            (row 2 of J^{-1}, C >= b)
2 c2 a omega / (b (1-x*)) < 1       (row 1 of J^{-1}, C >= c2 + a omega >= c2)
```

whose product is `4 g c2 / (x*(1-x*)) < 1`. If `J` is Hurwitz then
`x* > (1+theta)/2`, so `g > (1-theta)/2`, `c2 > (1+theta)/2`, and, because
`x* > 1/2`, `x*(1-x*) < (1-theta^2)/4`. Therefore

```
4 g c2 / (x*(1-x*))  >  (1 - theta^2) / ((1 - theta^2)/4)  =  4 .
```

Contradiction. **For every Hurwitz parameter set, every `alpha in (0,1)` and every
diagonal weight, this certificate cannot accommodate an orbit that reaches the
threshold.** `QED`

Status: THEOREM/analytic, about this certificate form only.

### 5.2 Numerical picture

`python scripts/t3_stageE_diagnostic.py` (ORION), 2142 Matignon-stable sets:

| regime | sets | min `q_lower` (kernel-free) | sets with `q_lower < 1` |
|---|---|---|---|
| Hurwitz | 1500 | 2.2631 | 0 |
| Matignon-stable, not Hurwitz | 642 | 2.0499 | 0 |

`q_lower` uses `K >= ||J^{-1}||_w` and therefore does not depend on any numerical
kernel. For the non-Hurwitz regime (where `c2` can vanish; it is exactly `0` at
`theta = 1/5, x* = 2/5`) there is **no proof**, only this grid: not feasible on
the 642 sets tried.

### 5.3 A number that is not reported, and why

A direct numerical `K` was also computed. At `T = 400` the integrated kernel had
not converged to `-J^{-1}` on the slow parameter sets (relative error up to
0.998), and it produced `q_true < q_lower`, which is impossible. With `T = 2000`
the kernel converges to within 5% on 1504 of 2142 sets and gives `q_true >= 4.08`
there. No conclusion rests on `q_true`.

### 5.4 What is left open by Stage E

O2 is about one family: sup-norm balls, diagonal weights, constants `K` and `C`
multiplied crudely. It does not exclude
* non-diagonal weights or a norm adapted to the eigenvectors of `J`;
* an a posteriori argument around the **computed nonlinear orbit** on `[0, T]`,
  followed by a local argument for the tail, which avoids paying `K C r^2` for
  the large early excursion;
* weighted-in-time norms.

The second is the natural continuation of the TASK-0002 verifier.

---

## 6. Certified / not certified

| claim | class |
|---|---|
| Proposition O1: no L1-certified orbit enters `R_ext` | THEOREM/analytic, conditional on X1 and on L1's conclusion |
| L1 constants for 1500 rational parameter sets | **CERTIFIED COMPUTATION** |
| `Omega` disjoint from the strip in 1500/1500 sets | **CERTIFIED COMPUTATION** |
| 9216 orbits from `Omega`: none crosses, `sup V/V(0) = 1` | NUMERICAL CORROBORATION |
| W1, B2, B3 enter `R_ext`, exact rational inputs | **CERTIFIED COMPUTATION** |
| Proposition O2: the sup-norm overshoot certificate is infeasible for Hurwitz `J` | THEOREM/analytic |
| same for the non-Hurwitz regime | NUMERICAL EXPLORATION on 642 sets, **not proved** |
| `iota(p) in B(E*)` for any witness | **NOT ESTABLISHED** |
| L1 itself | not addressed; ROUND-0004 owns it |

---

## 7. Stop conditions and negative results

The request says: "If none exist, this is a valuable negative result; map how
close trajectories approach the threshold." That is the outcome. None exist, by
O1; the map is §2.4 and §3.

---

## 8. Limitations

1. O1 and O2 are proved in this file. The Chief should check them.
2. `C_r` in §2.2 is not sharp. A sharper constant enlarges `Omega` by a bounded
   factor and cannot change O1.
3. Stage C uses float solvers. It corroborates O1; O1 does not depend on it.
4. Stage E excludes one certificate form. It is not a statement that survival
   cannot be certified.
5. B2/B3: survival evidence not repeated for the rounded rational `p` (§4).
6. Arb/python-flint are trusted, as in TASK-0002.

---

## 9. Reproduction

Hosts: ORION (Stage D, Stage E), AUREUS `aur007` (Stage C, 10 workers), local
(Stage A/B scan and tests). Python 3.12.3, numpy 2.5.3, mpmath 1.4.1,
python-flint 0.9.0 on the remote hosts.

```bash
cd computations && export OMP_NUM_THREADS=1
python scripts/t3_stageAB_l1_scan.py
python scripts/t3_stageC_inside_omega.py --workers 10
python scripts/t2_stageA_certify.py --exact-rational --theta 3/10 --a 1 --b 1 --m 4/5 \
       --alpha 17/20 --p 6093/2500 503/250 --T 4 --N 8000 --r 0.05 --tag Q_W1_N8000
python scripts/t2_stageA_certify.py --exact-rational --theta 1/5 --a 1 --b 1 --m 2/5 \
       --alpha 3/4 --p 6787/10000 2809/10000 --T 36 --N 8000 --r 0.02 --tag Q_B2_N8000
python scripts/t2_stageA_certify.py --exact-rational --theta 1/5 --a 1 --b 1 --m 2/5 \
       --alpha 3/4 --p 8821/10000 3983/10000 --T 23 --N 8000 --r 0.02 --tag Q_B3_N8000
python scripts/t3_stageE_overshoot_feasibility.py --workers 160
python scripts/t3_stageE_diagnostic.py
pytest tests/ -q          # 86 passed, 1 skipped
```

New code: `msbg/lyapunov_l1.py`; `to_arb`/`to_float` in `msbg/validated.py`;
scripts `t3_*`; tests `test_lyapunov_l1.py` (8).

```
branch: compute/task-0003
commit: 6e2352733c73f146450079c519a0931196711fab

That commit carries every artifact cited here; the only later commit writes this SHA.
```

---

## 10. Next question for the Chief

O1 says the survival certificate must use memory. The concrete proposal:

> Certify survival in two pieces. (a) On `[0, T]`, the TASK-0002 verifier gives a
> rigorous enclosure of the orbit, including its passage through `R_ext` and its
> return to a neighbourhood of `E*`. (b) For `t >= T`, write the equation for
> `u = x - E*` with the history on `[0, T]` as a **known, rigorously enclosed
> forcing term** `h_T(t) = (1/Gamma(alpha)) int_0^T (t-s)^{alpha-1} g(x(s)) ds + p - E*`,
> and prove that a small forcing which decays like `t^{alpha-1}` keeps `u` small
> and sends it to `0`.

Piece (b) is a statement about a Volterra equation with small data, which is
where a Lyapunov or resolvent argument belongs. It is not excluded by O1,
because the state at time `T` is not a cold start, and not by O2, because the
large excursion is handled by (a) and never multiplied by `K C r^2`.

What the Compute Agent needs from the Chief or ROUND-0004 to attempt it: the
exact smallness condition on `h_T` and on `u(T)` under which (b) holds.
