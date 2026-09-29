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
| B — near-equilibrium witnesses | STAGE_B_VERDICT |
| C — continuation-state proximity | STAGE_C_VERDICT |
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
