# TASK-0002 — Validated entry certification and near-equilibrium witness search — COMPUTE RETURN

**From:** Compute Agent
**To:** Chief Researcher
**Task:** `research/coordination/chief-to-compute/TASK-0002_validated-entry-near-equilibrium_REQUEST.md`
**Date:** 2026-09-29
**Branch:** `compute/task-0002`
**Final commit SHA:** see §9

---

## 0. Executive answer

| Stage | Verdict |
|---|---|
| A — validated finite-time enclosure | **CERTIFIED COMPUTATION.** Entry of the TASK-0001 witness into `R_ext` is certified with margin `eta = 0.0985`. |
| B — near-equilibrium witnesses | 237 confirmed witnesses; closest to `E*` with margin >= 0.01 is at `\|p - E*\| = 0.322` (TASK-0001: 2.5). Two of them are also **CERTIFIED** to enter `R_ext`. |
| C — continuation-state proximity | `D(T,R)` decays for every fixed `R`; stop condition not triggered. But convergence is **not uniform in `tau`**, which constrains the form of the survival-side theorem. |
| D — solver discipline | 18 new regression tests; every float discovery cross-checked; UNDECIDED is fail-safe |
| E — fast history convolution | Done, cross-validated to `1e-14` against the `O(N^2)` reference |

What Stage A does **not** do: it certifies *entry* into `R_ext` on a finite time
interval. It says nothing about the survival basin. `iota(p) in B(E*)` is exactly
as numerical as it was after TASK-0001.

---

## 1. Stage A — the certificate

Witness: `theta = 0.3, a = b = 1, m = 0.8, alpha = 0.85, p = (2.4372, 2.012)`.

Five independent runs of the verifier, varying mesh size, mesh grading, the
number of rigorous sample points per cell and the working precision:

| run | N | grading | K | precision | bootstrap `max U < r = 0.05` | best time box | rigorous `x` box | `y >=` | `eta` | cells certified |
|---|---|---|---|---|---|---|---|---|---|---|
| N4000 | 4000 | 3.0 | 64 | 128 bit | 2.995e-2, pass | [2.964871, 2.967328] | [0.194512, 0.208475] | 0.769481 | 0.091525 | 1277 |
| N4000p256 | 4000 | 3.0 | 64 | 256 bit | 2.995e-2, pass | [2.964871, 2.967328] | [0.194512, 0.208475] | 0.769481 | 0.091525 | 1277 |
| N4000K32 | 4000 | 3.0 | 32 | 128 bit | 3.314e-2, pass | [2.933043, 2.935483] | [0.194506, 0.209198] | 0.779194 | 0.090802 | 1277 |
| N4000g25 | 4000 | 2.5 | 64 | 128 bit | 3.896e-2, pass | [2.879051, 2.881104] | [0.194580, 0.210440] | 0.796267 | 0.089560 | 1479 |
| **N8000** | 8000 | 3.0 | 64 | 128 bit | **7.222e-3**, pass | **[3.387705, 3.389048]** | **[0.195165, 0.201521]** | **0.655495** | **0.098479** | 2556 |

**Certified statement (run N8000).** The solution of the Caputo IVP exists and is
unique on `[0, 4]`, and

```
for all t in [3.387705, 3.389048]:   0.195165 <= x(t) <= 0.201521 < theta - 0.098479,
                                     y(t) >= 0.655495 > 0.
```

Moreover the state lies in `R_ext` with positive margin on the whole contiguous
interval `t in [1.2605, 4.0]` (2556 cells).

Doubling the precision from 128 to 256 bits changes nothing in the reported
digits: the certificate is limited by the discretisation, not by rounding.

### What the reported `y` bound is, and an apparent contradiction with TASK-0001

TASK-0001 reported `y = 0.5476` at the deepest point `t = 3.90`. The certificate
reports `y >= 0.6555` at `t ~ 3.39`. These are different times; `y` is still
decreasing there. They are consistent.

---

## 2. Stage A — exact certification semantics

### 2.1 Theorem used

Let `g` be `C^1` on `R^2`, `0 < alpha < 1`, `p in R^2`, and
`0 = t_0 < t_1 < ... < t_N = T` with cells `C_n = [t_n, t_{n+1}]`, `h_n = t_{n+1} - t_n`.
Let `phi` be continuous and piecewise linear on the mesh and put

```
xhat = p + I^alpha[phi],        rho = phi - g(xhat).
```

Norms: max-norm on `R^2`, induced row-sum norm on matrices. Fix `r > 0` and
suppose that for every `n`

```
R_n    >= sup_{t in C_n} ||rho(t)||,
Lbar_n >= sup { ||Dg(xi)|| : xi in B_n },   B_n := hull(xhat(C_n)) + [-r, r]^2 .
```

Define, for `j < n`, `W_{n,j} = ((t_n - t_j)^alpha - (t_n - t_{j+1})^alpha) / alpha`, and

```
Delta_n = ( sum_{j<n} W_{n,j} R_j + h_n^alpha R_n / alpha ) / Gamma(alpha),
kappa_n = h_n^alpha Lbar_n / (alpha Gamma(alpha)),
U_n     = ( Delta_n + sum_{j<n} W_{n,j} Lbar_j U_j / Gamma(alpha) ) / (1 - kappa_n).
```

**Claim.** If `kappa_n < 1` for all `n` and `max_n U_n < r`, then
`^C D^alpha x = g(x), x(0) = p` has a unique continuous solution on `[0, T]` and
`sup_{t in C_n} ||x(t) - xhat(t)|| <= U_n` for every `n`.

### 2.2 Proof

*Step 0 (defect identity).* Both `x = p + I^alpha[g(x)]` and `xhat = p + I^alpha[phi]`, so
with `e = x - xhat`

```
e = I^alpha[ g(x) - g(xhat) ] - I^alpha[ rho ].                                  (1)
```

*Step 1 (local solution).* `g` is locally Lipschitz, so the Volterra equation has
a unique continuous solution on a maximal interval `[0, T_max)`, and if
`T_max <= T` then `||x(t)||` is unbounded as `t -> T_max`.

*Step 2 (the estimate under an a priori assumption).* Let `tau in (0, min(T, T_max))`
and suppose `||e(s)|| <= r` for all `s in [0, tau]`. Put
`E_n = sup { ||e(s)|| : s in C_n, s <= tau }` (zero if empty). For `s in C_j`,
`s <= tau`, both `xhat(s)` and `x(s)` lie in the convex box `B_j`, so by the mean
value inequality `||g(x(s)) - g(xhat(s))|| <= Lbar_j ||e(s)|| <= Lbar_j E_j`.
For `t in C_n`, `t <= tau`, (1) gives

```
||e(t)|| <= (1/Gamma(alpha)) [ sum_{j<n} w_j(t) (Lbar_j E_j + R_j)
                               + ((t - t_n)^alpha / alpha) (Lbar_n E_n + R_n) ],
w_j(t) = int_{C_j} (t - s)^{alpha-1} ds = ((t - t_j)^alpha - (t - t_{j+1})^alpha) / alpha.
```

Since `alpha - 1 < 0`, `d w_j / dt = (t - t_j)^{alpha-1} - (t - t_{j+1})^{alpha-1} < 0`:
each `w_j` is decreasing on `C_n`, so `w_j(t) <= w_j(t_n) = W_{n,j}`. Also
`(t - t_n)^alpha <= h_n^alpha`. Taking the supremum over admissible `t in C_n`,

```
E_n <= Delta_n + (1/Gamma(alpha)) sum_{j<n} W_{n,j} Lbar_j E_j + kappa_n E_n .
```

Because `kappa_n < 1`, induction on `n` gives `E_n <= U_n` for every `n`.
No monotonicity of `e` or of any comparison function is used; only the
supremum over each cell.

*Step 3 (bootstrap).* Let `S = { tau in [0, min(T, T_max)) : ||e|| <= r on [0, tau] }`.
`S` contains `0` since `e(0) = 0`; it is closed in `[0, min(T, T_max))` by
continuity; and by Step 2 every `tau in S` satisfies
`||e|| <= max_n U_n < r` on `[0, tau]`, so by continuity a neighbourhood of `tau`
lies in `S`. Hence `S = [0, min(T, T_max))`.

*Step 4 (global existence).* On `S`, `||x|| <= sup ||xhat|| + r`, which is finite, so
`T_max > T` by Step 1. Applying Step 2 with `tau = T` gives the claim. `QED`

### 2.3 What is trusted and what is not

| item | status |
|---|---|
| mesh points `t_k`, nodal values `phi_k` | **untrusted**; produced by a float collocation solver and then treated as exact binary64 numbers. A bad `phi` can only make `R_n` large and the verdict UNDECIDED. |
| `xhat(t)`, `xhat'(t)` | evaluated from their closed forms in **Arb ball arithmetic** (128 bit) |
| `R_n` | Arb. For `n >= 1`: `max_i |rho(s_i)| + (h_n / 2K) sup_{C_n} |rho'|` over `K+1` rigorous sample points, with `rho' = m_n - Dg(xhat) xhat'`. For `n = 0`, where `xhat'` is singular at `0`, `rho(C_0)` is enclosed directly. |
| `Lbar_n`, state boxes | Arb interval evaluation of `Dg` on `B_n`; boxes from the sampled values plus the Lipschitz remainder |
| weights `W_{n,j}` | Arb, rounded up to binary64 |
| recursion for `Delta_n`, `U_n` | binary64 with every operation rounded upward (`nextafter`) and a Higham `gamma_n` factor on each dot product; all terms are non-negative, so upward rounding is sound |
| python-flint 0.9.0 / Arb | trusted as a correct ball-arithmetic library |
| local existence/continuation for Volterra equations with locally Lipschitz `g` | used in Step 1 as standard theory; the Chief should cite it |

**UNDECIDED policy.** If any `kappa_n >= 1`, or `max U >= r`, or no cell box
separates from the threshold, the verdict is UNDECIDED. It is never "refuted".

### 2.4 Why wrapping had to be removed, and how

`xhat(t)` is a sum of `n` history terms `m_k d_k(t)` with slopes `m_k` of both
signs. A naive interval evaluation over a cell adds `|m_k|` times each term's
variation and cannot see the cancellation. Measured on a test mesh (`N = 300`)
before the fix: the rigorous defect bound was 60x the sampled defect (median),
and the resulting `U` was `1.1e6` against a non-rigorous estimate of `7.3`.

Fix: `K+1` rigorous *point* evaluations per cell (no range, so no wrapping) plus
a Lipschitz remainder that carries the loose range bound divided by `2K`.
Measured overestimation of `R_n` after the fix: `K = 4`: 4.2x, `K = 16`: 1.8x,
`K = 64`: 1.2x.

### 2.5 Soundness evidence for the verifier

1. **Exact solution test.** For the planar linear system `^C D^alpha x = A x` with
   `A` a scaled rotation, `x(t) = E_alpha(A t^alpha) x_0` is known in closed form.
   The rigorous box, inflated by `U_n`, contains the exact solution at every
   tested time, for `alpha = 0.6` and `0.85` (`tests/test_validated.py`).
2. **Deliberately bad `phi`.** Perturbing the untrusted nodal values by `1e-3`
   widens the enclosure and it still contains the exact solution.
3. **Monotone refinement.** `U` decreases under mesh refinement.
4. **Fail-safe.** A tube radius of `1e-9` yields a failed bootstrap, i.e. UNDECIDED.

### 2.6 A discrepancy found, and its resolution

A consistency check of the five certificates against the three float solvers at
`h = 2e-4` found float points **outside** the rigorous boxes: between 2208 and
6260 of 60003 points per certificate, worst excess `1.4e-3`. Located by solver
and mesh:

| solver | h | points outside | time range of those points | worst excess |
|---|---|---|---|---|
| `pi_rect` | 2e-4 | 1333 | [0.0004, 1.1292] | 5.96e-4 |
| `pi_rect` | 5e-5 | 850 | [0.0001, 0.6316] | 1.41e-4 |
| `pece` | 2e-4 | 3 | [0.0002, 0.0006] | 5.49e-4 |
| `pece` | 5e-5 | 2 | [0.0001, 0.0011] | 1.22e-4 |
| `l1` | 2e-4 | 1089 | [0.0002, 1.0400] | 1.33e-3 |

Evidenced: the excess shrinks under float mesh refinement and all offending
points are at `t < 1.13`, none near the certified time box.

To decide which side is wrong, an **independent** reference was built that
shares nothing with product integration: the generalised power series
`x(t) = sum_k a_k t^{k alpha}` with
`a_k = Gamma((k-1)alpha+1)/Gamma(k alpha+1) [g(x)]_{k-1}`, 120 terms, 60 digits.
At all 39 usable points in `t in [1e-6, 3.8e-2]` the series value lies **inside**
the rigorous box, and the float solvers differ from the series by up to
`6.1e-4` (`pi_rect`), `8.3e-4` (`pece`) and `1.45e-3` (`l1`).

Evidenced: series inside every box; float solvers off by about `1e-3` in the
initial layer. Inferred: the outside points are float error, not an enclosure
fault. Not verified: the region `t in [0.04, 1.13]`, where the series has no
usable accuracy and only the float-refinement trend supports that reading.

**Consequence for TASK-0001.** The Stage-A solver validation there tested
accuracy at the *end* of the horizon. It did not test the initial layer, where
the uniform-mesh float solvers are `1e-3` accurate at `h = 2e-4`. This does not
change any TASK-0001 conclusion (margins were `0.1`), but it is a limitation of
that validation that was not stated at the time.


---

## 3. Stage B — witnesses close to the coexistence equilibrium

Command: `python scripts/t2_stageB_near_equilibrium.py --workers 170 --T2 1000` (ORION).

**Design.** 450 parameter sets: `theta in {0.2,...,0.6}`, gap `x* - theta in
{0.03,...,0.3}`, `a in {0.5,1,2}`, `alpha in {0.55,...,0.92}`, `b = 1`. Phase 1: a
polar grid of 1080 constant histories around `E*`, radii geometric in
`[0.01, 2]`, PECE at `h = 0.01` to `T = 200`, positivity as a hard filter.
Phase 2: each candidate re-run to `T = 1000` with three solvers and two meshes
(`h = 0.02, 0.01`); a candidate is a witness only if **all six** runs agree that
it enters `R_ext` with positive margin and is still contracting towards `E*`.

**Counts.** 183 of 450 parameter sets have a Caputo-stable `E*`; 81 of those
produce candidates; 244 candidates went to phase 2; **237 confirmed**, 7 rejected
by solver/mesh disagreement. By order:

| `alpha` | 0.55 | 0.65 | 0.75 | 0.85 | 0.92 |
|---|---|---|---|---|---|
| confirmed witnesses | 2 | 75 | 107 | 47 | 6 |

TASK-0001 found no witness at `alpha = 0.55`; this search finds two. That
confirms the TASK-0001 caveat that the empty column there was a search
limitation.

**Pareto front** (`||p - E*||` minimised, margin maximised; margin is the minimum
over the six runs, spread is max minus min over them):

| `theta` | `m` | `a` | `alpha` | `\|\|p-E*\|\|` | margin | spread | dist to `E*` at T | `p` |
|---|---|---|---|---|---|---|---|---|
| 0.2 | 0.4 | 1 | 0.75 | 0.2681 | 0.00137 | 4.4e-4 | 5.4e-3 | (0.63214, 0.25403) |
| 0.2 | 0.4 | 1 | 0.75 | **0.3218** | 0.01149 | 3.8e-4 | 2.4e-3 | (0.67868, 0.28089) |
| 0.2 | 0.4 | 1 | 0.75 | **0.5567** | 0.02263 | 1.5e-4 | 2.4e-3 | (0.88210, 0.39834) |
| 0.3 | 0.6 | 2 | 0.75 | 0.6683 | 0.02747 | 2.3e-4 | 5.9e-3 | (1.22797, 0.28856) |
| 0.2 | 0.5 | 1 | 0.85 | 0.6683 | 0.02895 | 5.9e-4 | 1.1e-3 | (1.07874, 0.48414) |
| 0.2 | 0.5 | 1 | 0.85 | 0.8022 | 0.03610 | 4.4e-4 | 1.3e-3 | (1.19475, 0.55112) |
| 0.4 | 0.6 | 1 | 0.75 | 0.9630 | 0.04557 | 2.2e-4 | 3.7e-3 | (1.54841, 0.24723) |
| 0.3 | 0.5 | 2 | 0.75 | 1.1561 | 0.04872 | 2.3e-4 | 6.3e-3 | (1.63853, 0.25075) |
| 0.3 | 0.6 | 2 | 0.85 | 1.6660 | 0.08420 | 7.8e-4 | 2.3e-3 | (2.24072, 0.34930) |
| 0.6 | 0.9 | 1 | 0.75 | 2.0000 | 0.09602 | 1.8e-3 | 3.0e-2 | (2.77939, 0.71404) |

The trade-off is monotone and steep: every step towards `E*` costs margin. The
first row is reported but is **not** recommended: its margin (`1.4e-3`) is only
three times the solver spread.

### 3.1 The two near-equilibrium witnesses are also certified

Same verifier as Stage A, `N = 8000`, grading 3, `K = 64`, 128 bit, tube `r = 0.02`;
model `theta = 0.2, a = b = 1, m = 0.4, alpha = 0.75`, `E* = (0.4, 0.12)`:

| witness | `p` (exact binary64 input) | time box | rigorous `x` box | `y >=` | `eta` | `max U` | contiguous certified interval |
|---|---|---|---|---|---|---|---|
| B2 | (0.6786775656542838, 0.28089456754761033) | [30.975284, 30.987498] | [0.188301, 0.189011] | 0.053344 | **0.010989** | 1.586e-3 | [16.2518, 36.0] |
| B3 | (0.8821027335047349, 0.39834214296601306) | [20.959035, 20.967143] | [0.177206, 0.177551] | 0.106298 | **0.022449** | 2.928e-4 | [8.9750, 23.0] |

Evidence class: **CERTIFIED COMPUTATION**, same semantics as §2.

These two are much easier to enclose than the TASK-0001 witness despite a time
horizon nine times longer: the tube Lipschitz bound is `1.1`-`1.9` instead of
`17.2`, and the defect bound is `1e-8` instead of `1e-6`.

### 3.2 Caveats on Stage B

* The distance `||p - E*|| = 0.32` is small relative to TASK-0001 but it is **not**
  small in absolute terms: `E* = (0.4, 0.12)`, so `p` is 0.7 of `|E*|` away.
  Whether any explicit local-basin radius reaches that far is unknown.
* Linear Caputo stability of `E*` was used only to select parameter sets. It is
  not a basin proof and nothing here treats it as one.
* The near-equilibrium regime is reached by pushing `x*` towards `theta`
  (gap 0.2) at `alpha = 0.75`. It is a weakly damped spiral: see the
  non-monotone approach in §4.

---

## 4. Stage C — continuation-state proximity

Command: `python scripts/t2_stageC_continuation.py --Tmax 4000 --h 0.02 --candidates data/t2_stageC_candidates.json` (AUREUS).

`D(T,R) = sup_{tau in [0,R]} || T_T iota(p)(tau) - E* ||_inf`, evaluated from the
Doan-Kloeden formula with `g(x(s))` integrated exactly, cell by cell, against the
shifted kernel. Two solvers x two meshes; values below are PECE at `h = 0.01`;
"spread" is max minus min over the four runs.

**TASK-0001 witness** (`alpha = 0.85`, `E* = (0.8, 0.1)`):

| T | `\|\|x(T)-E*\|\|` | D(T,1) | D(T,10) | D(T,100) | D(T,1000) | spread |
|---|---|---|---|---|---|---|
| 100 | 5.205e-2 | 5.203e-2 | 6.139e-2 | 2.482e-1 | 6.372e-1 | 5.4e-4 |
| 500 | 1.498e-2 | 1.498e-2 | 1.756e-2 | 8.223e-2 | 3.445e-1 | 1.0e-4 |
| 1000 | 8.464e-3 | 8.463e-3 | 9.885e-3 | 4.750e-2 | 2.360e-1 | 9.3e-5 |
| 2000 | 4.745e-3 | 4.745e-3 | 5.532e-3 | 2.691e-2 | 1.509e-1 | 8.2e-5 |
| 4000 | 2.648e-3 | 2.645e-3 | 3.087e-3 | 1.509e-2 | 9.133e-2 | 7.2e-5 |

**B2** (`||p-E*|| = 0.322`, `alpha = 0.75`, `E* = (0.4, 0.12)`):

| T | `\|\|x(T)-E*\|\|` | D(T,1) | D(T,100) | D(T,1000) | spread |
|---|---|---|---|---|---|
| 100 | 1.546e-1 | 1.551e-1 | 1.551e-1 | 1.551e-1 | 1.6e-2 |
| 250 | 7.206e-2 | 7.206e-2 | 7.206e-2 | 8.171e-2 | 2.9e-2 |
| 500 | 3.025e-2 | 3.024e-2 | 3.024e-2 | 7.007e-2 | 4.9e-3 |
| 1000 | 7.741e-4 | 7.748e-4 | 1.211e-2 | 5.722e-2 | 1.2e-3 |
| 2000 | 1.190e-3 | 1.190e-3 | 7.169e-3 | 3.940e-2 | 7.5e-5 |
| 4000 | 7.285e-4 | 7.280e-4 | 4.385e-3 | 2.573e-2 | 1.8e-5 |

**B3** (`||p-E*|| = 0.557`): same pattern; at `T = 4000`,
`||x(T)-E*|| = 1.268e-3`, `D(T,100) = 7.636e-3`, `D(T,1000) = 4.477e-2`, spread `5.9e-6`.

### 4.1 Findings

1. **`D(T,R)` decays in `T` for every fixed `R`**, for all three candidates. The
   stop condition "continuation-state distance does not decay despite
   physical-state convergence evidence" is **not triggered**. Local decay
   exponents between `T = 2000` and `4000`: TASK-0001 witness `-0.84` at
   `R <= 100` (prediction `-alpha = -0.85`), `-0.73` at `R = 1000`; B2 `-0.71`
   (prediction `-0.75`), `-0.62` at `R = 1000`.

2. **The supremum is always attained at the far end `tau = R`** (24 of 24 cases for
   the TASK-0001 witness), and `D` depends essentially on `R/T`:
   `D(100,10) = 0.061`, `D(1000,100) = 0.048`; `D(100,100) = 0.248`,
   `D(1000,1000) = 0.236`.

3. **Convergence is not uniform in `tau`. This one is analysis, not numerics.**
   For fixed `T`,

   ```
   || T_T iota(p)(tau) - p || <= sup|g(x)| ((T + tau)^alpha - tau^alpha) / Gamma(alpha+1)  ->  0   (tau -> infinity),
   ```

   because `(T+tau)^alpha - tau^alpha ~ alpha T tau^{alpha-1}`. So every continuation
   state of a bounded orbit tends to the constant `p` at `tau = infinity`, and

   ```
   sup_{tau >= 0} || T_T iota(p)(tau) - E* ||  >=  || p - E* ||     for every T.
   ```

   **Consequence for the Chief.** A local-attractor theorem stated in the
   sup-norm over all of `R_+` cannot close the survival side, for any witness
   with `p != E*`. The theorem has to live in the compact-open topology the
   project already adopted (`research/STATE_ARCHITECTURE.md` §2) or in a weighted
   norm. This also means that proximity of `p` to `E*` (Stage B) helps exactly to
   the extent that the theorem's neighbourhood is measured in a topology where
   `T_T iota(p)` actually enters it.

4. **B2 approaches `E*` non-monotonically**: `||x(T)-E*||` is `7.7e-4` at `T = 1000`
   and `1.19e-3` at `T = 2000`. It is a weakly damped spiral, and the solver
   spread is large early (`2.9e-2` at `T = 250`, phase differences between
   solvers) before collapsing to `1.8e-5` at `T = 4000`. Any tail test for this
   witness that assumes monotone decay is wrong.

### 4.2 A bug fixed in this diagnostic

The first version integrated the nodes of every solver with a piecewise-linear
quadrature. That is consistent with PECE but not with the rectangle solver. The
symptom: all four runs agreed on `||x(T)-E*|| = 2.6476e-3` to seven digits, yet
the `pi_rect` runs violated the identity `C_T(0) = x(T)` by `3.2e-2` (`h = 0.02`)
and `1.6e-2` (`h = 0.01`), producing a spurious solver spread of `2.8e-2` that
did not decay with `T`. Each solver now uses its own quadrature; the identity
holds to `1.7e-4` (PECE, `O(h^2)`) and `1e-12` (rectangle), and the spread is at
most `5.4e-4` for the TASK-0001 witness.

---

## 5. Stage E — blocked history convolution

`msbg/fastconv.py`. Steps are processed in blocks; the far history of a whole
block is one Toeplitz matrix-matrix product (BLAS-3) instead of one
matrix-vector product per step. **Nothing is approximated**: same weights, same
predictor and corrector, different floating-point summation order.

Cross-validation against the `O(N^2)` reference (`tests/test_fastconv.py`, 11
tests): maximum relative difference `6.5e-14` over 400 trajectories and block
sizes 1, 7, 64, 1000, 5000; against the exact Mittag-Leffler solution the
blocked solver meets the same tolerances as the reference.

Measured effect: Stage B phase 1 (450 parameter sets x 1080 initial states,
`N = 20000`) had reported 25 of 450 sets after 17 minutes (ordered output, so a lower bound on progress) with the reference
solver; with the blocked solver all 450 finished in about 2 minutes.

**Limit, measured:** for a single trajectory the blocked solver is **19x
slower** than the reference (`9.35 s` vs `0.5 s` at `N = 20000`), because the
history already fits in cache and the Toeplitz gather dominates.
`solve_blocked` now falls back to the reference when the batch is smaller than
32 trajectories.

This is *not* an `O(N log N)` method. Small `alpha` at long horizons remains out
of reach.

---

## 6. Stop conditions

| stop condition | status |
|---|---|
| interval wrapping makes the finite-time enclosure undecidable at practical precision | **not triggered**, but it would have been with the naive interval evaluation (§2.4); resolved by `K`-point sampling |
| no near-equilibrium witness improves the theorem-closure geometry | **not triggered**: `\|\|p-E*\|\|` from 2.5 down to 0.32 with a certified entry |
| continuation-state distance does not decay despite physical-state convergence | **not triggered** for fixed `R`; see §4.1 item 3 for the non-uniformity |

---

## 7. Certified / not certified

| claim | class |
|---|---|
| The TASK-0001 witness orbit exists on `[0,4]` and lies in `{0 < x < theta - 0.0985, y > 0}` for `t in [3.387705, 3.389048]` | **CERTIFIED COMPUTATION** |
| Same orbit lies in `R_ext` for all `t in [1.2605, 4.0]` | **CERTIFIED COMPUTATION** |
| B2 orbit lies in `{0 < x < theta - 0.0110, y > 0}` for `t in [30.975284, 30.987498]` | **CERTIFIED COMPUTATION** |
| B3 orbit lies in `{0 < x < theta - 0.0224, y > 0}` for `t in [20.959035, 20.967143]` | **CERTIFIED COMPUTATION** |
| `sup_{tau>=0} \|\|T_T iota(p)(tau) - E*\|\| >= \|\|p - E*\|\|` for bounded orbits | THEOREM/analytic (elementary estimate, §4.1) |
| 237 near-equilibrium witnesses; Pareto front | NUMERICAL CORROBORATION |
| `D(T,R) -> 0` for fixed `R` | NUMERICAL CORROBORATION |
| `iota(p) in B(E*)` for any witness | **NOT ESTABLISHED.** Numerical only, exactly as after TASK-0001 |
| `iota(R_ext) in B(0,0)` (Theorem X1) | not addressed here; ROUND-0003 owns the hypothesis audit |

---

## 8. Limitations

1. **Entry only.** No finite-time enclosure can prove basin membership. The
   survival side is untouched.
2. **The a posteriori theorem is proved in this file, not in a published
   source.** The Chief should check §2.2 and supply the citation for Step 1.
3. **Arb/python-flint are trusted.** No independent ball-arithmetic library was
   used to cross-check.
4. **The inputs `p`, `theta`, `a`, `b`, `m`, `alpha` are the binary64 numbers
   nearest to the decimals written.** E.g. `alpha = 0.85` means the double
   `0.84999999999999997779...`. The certificates are for those exact doubles. A
   certificate for the exact rational `17/20` needs the parameters entered as
   Arb rationals; the code path exists (`arb(str)`) but was not used.
5. **Float solvers are about `1e-3` accurate in the initial layer at `h = 2e-4`**
   (§2.6). Not verified between `t = 0.04` and `t = 1.13`.
6. **Margins near `E*` are thin** (`0.011`, `0.022`). They are certified, but an
   open-family statement (Theorem E2) around B2 has little room.
7. **Tail evidence at `T = 1000` in Stage B phase 2**, not `4000`. The three
   candidates taken to Stage C were followed to `T = 4000`.
8. **Process errors during this task**, recorded: the first phase-2 design
   (`T = 4000`, `h = 0.01`, 300 workers on 172 physical cores) did not finish a
   single candidate in 60 minutes and was killed; the per-candidate cost had
   been extrapolated from `N = 40000`, below the quadratic regime. A first
   launch of the B2/B3 certificates used hand-typed coordinates differing from
   the confirmed candidates by `1e-6`; it was killed and relaunched from the
   data file.

---

## 9. Reproduction

Hosts: ORION (344 threads / 172 cores, 1007 GB) for Stage B and the
certificates; AUREUS (`aur007`, 32 threads, 186 GB, shared with other users) for
Stage C, the mesh-sizing prototype and four of the Stage A variants. Python
3.12.3, numpy 2.5.3, scipy 1.18.1, mpmath 1.4.1, python-flint 0.9.0 on both.
Tests run locally (Python 3.14.3, numpy 2.4.4, mpmath 1.3.0, python-flint 0.9.0).

```bash
cd computations && export OMP_NUM_THREADS=1
python scripts/t2_stageA_certify.py --N 8000 --K 64 --tag N8000
python scripts/t2_stageA_certify.py --N 4000 --K 64 --prec 256 --tag N4000p256
python scripts/t2_stageA_crosscheck.py
python scripts/t2_stageA_series_reference.py
python scripts/t2_stageB_near_equilibrium.py --workers 170 --T2 1000
python scripts/t2_stageA_certify.py --theta 0.2 --a 1.0 --b 1.0 --m 0.4 --alpha 0.75 \
       --p 0.6786775656542838 0.28089456754761033 --T 36 --N 8000 --r 0.02 --tag B2_N8000
python scripts/t2_stageA_certify.py --theta 0.2 --a 1.0 --b 1.0 --m 0.4 --alpha 0.75 \
       --p 0.8821027335047349 0.39834214296601306 --T 23 --N 8000 --r 0.02 --tag B3_N8000
python scripts/t2_stageC_continuation.py --Tmax 4000 --h 0.02 \
       --candidates data/t2_stageC_candidates.json
pytest tests/ -q          # 78 passed, 1 skipped
```

New code: `msbg/validated.py`, `msbg/aposteriori.py`, `msbg/fastconv.py`; scripts
`t2_*`; tests `test_validated.py` (7), `test_fastconv.py` (11). Artifacts:
`computations/data/t2_*`, `computations/manifests/t2_*`.

```
branch: compute/task-0002
commit: FINAL_SHA
```

---

## 10. Next question for the Chief

Given §4.1 item 3, the survival-side theorem must be stated in the compact-open
topology or a weighted norm. The concrete question:

> Is there a neighbourhood `N` of `iota(E*)` in `C(R_+, R^2)`, open in the
> compact-open topology and described by finitely many checkable inequalities on
> `f|_{[0,R]}`, such that `N subset B(E*)`?

If ROUND-0003 returns such an `N` with explicit `R` and radius, the Compute
Agent can test `T_T iota(p) in N` rigorously: the continuation state is an
explicit integral of `g(x(s))` over `[0,T]`, and the enclosure of `x` on `[0,T]`
from §2 turns it into an interval computation. The cost is the horizon: the
verifier has been run to `T = 36`; `T = 4000` needs either a much coarser
graded mesh in the tail or a different defect representation.
