# TASK-0006 — Rigorous oscillation-Banach CAP for B215 — COMPUTE RETURN

**From:** Compute Agent
**To:** Chief Researcher
**Task:** `research/coordination/chief-to-compute/TASK-0006_rigorous-oscillation-cap_REQUEST.md`
**Date:** 2026-09-30
**Branch:** `compute/task-0006`
**Code commit SHA (all cited T=300 results were produced with this `msbg/cap.py`):** `c9bc2f80788e0834ecb74e69e89aab59e50c741d`

---

## 0. Executive answer

**B215 survival is CERTIFIED (evidence class: CERTIFIED COMPUTATION under the
floating-point model declared in §7), at the cut T = 300, not T = 1000.**

All four Stage-F requirements hold with the constants below:

| Requirement | Result |
|---|---|
| 1. exact-rational entry into `R_ext` | **CERTIFIED**: `0 < x(t) < 1/2`, `y(t) > 0` on 836 consecutive cells covering `t ∈ [5.857677, 13.727539]`; best cell `t ∈ [8.983920, 8.992793]`, `x ∈ [0.468939, 0.469059]`, `y ≥ 0.248262`, margin `η = θ − x_max = 0.030941` |
| 2. rigorous validation of the history on `[0, T]` | **CLOSED on `[0, 300]`**: a unique exact solution of the Volterra/Caputo equation lies in a certified tube around the collocation orbit; adapted state error `≤ 4.866e-4` for all `t ∈ [0, 300]` (physical Euclidean `≤ 2.219e-4`) |
| 3. rigorous M1 constants | `K_J ≤ 11.34990`, `C_r ≤ 0.36955 + 0.16274 r`, `M_T ≤ 4.32324e-2` (`T = 300`, sup over `t ≥ T`, infinite post-cut) |
| 4. `M_T + K_J C_r r² < r` | **SEPARATED** at `r = 2221/20000 = 0.11105`: `r − K_J C_r r² − M_T ≥ +1.35626e-2`, `K_J C_r r ≤ 0.48856 < 1` |

Hence, by THEOREM M1 applied at `T = 300` to the certified state `u(300) = x(300) − E*`
(`x(300) ∈ [0.795867, 0.796311] × [0.126667, 0.127111]`), `x(t; p) → E* = (4/5, 3/25)`.
Together with the entry certificate (item 1), X1 + E3 + E1 give TARGET-A20 for
B215 — that promotion is Chief's, not mine.

**Two things are not what the request literally asked for, and I state them plainly:**

1. The certificate is **not** a scalar Church–Queirolo radii polynomial in one
   fixed oscillation norm. It is the **componentwise (vector) radii inequality**
   `F(b) < b` for cell-wise bounds `b = (sup, osc, bubble)` together with a
   rigorous **contraction constant `κ ≤ 0.08361`** in a Perron-weighted norm.
   Both are complete Banach arguments (§3.4). The scalar inequality
   `Y0 + Z1 r + Z2(r) r < r` **fails in every weighted norm I tried**
   (`p(1) = +1.385` in the certificate's own norm); §5.3 explains why this is
   structural, not a lack of effort.
2. **`T = 1000` did not close.** The linear part is fine there (`ρ(M) ≈ 0.19–0.20`
   with `N = 14000`), the quadratic term is not: the collocation defect, integrated
   over `‖I^α‖ ≈ 355`, is still too large. A `N = 20000` defect-equidistributed run
   is in progress at the time of writing (§6). Since M1 separates at `T = 300`,
   `T = 1000` is no longer needed for the theorem.

Evidence labels used below: **THEOREM** (proved on paper), **CERTIFIED**
(rigorous computation under §7's model), **NUMERICAL** (float, corroboration
only), **OPEN**.

---

## 1. Stage 0 — exact-rational entry (CERTIFIED)

Parameters and initial state are the exact rationals of the request
(`θ = 1/2, a = 1/2, b = 1, m = 4/5, α = 17/20, p = (277/100, 467/1000)`), parsed by
`msbg.validated_res.Setup` and used in Arb throughout the cell enclosures.

**The TASK-0002 verifier cannot certify B215's entry**, at any of the settings
tried (all `UNDECIDED`, manifests `computations/manifests/t2_stageA_certify_Q_B215_*`):

| `T` | `N` | tube `r` | `max U` | verdict |
|---|---|---|---|---|
| 30 | 12000 | 0.02 | 2.689e4 | UNDECIDED (Gronwall blow-up, `L_max = 17.24`) |
| 12 | 16000 | 0.02 | 0.204 | UNDECIDED |
| 10 | 16000 | 0.02 | 0.0672 | UNDECIDED |
| 10 | 16000 | 0.08 | 3.60 | UNDECIDED (recursion explodes when `K·a > 1`) |

The entry certificate instead comes from the CAP tube (§3) via
`scripts/t6_stageE_m1.py`: the certified adapted state error `Ω_n` on each cell
is converted to a physical max-norm pad `‖S‖ Ω_n ≤ 2.219e-4` and added to the Arb
state boxes of `msbg.validated.verify_cells`; a cell certifies entry iff
`x_hi + pad < θ⁻`, `x_lo − pad > 0`, `y_lo − pad > 0`.

Result (manifest `t6_stageE_adaptT300_N12000`): **836 cells**, all of
`t ∈ [5.857677, 13.727539]`; the best cell is `t ∈ [8.983920, 8.992793]` with
`x ∈ [0.468939, 0.469059]`, `y ≥ 0.248262`, `η = 0.030941`.

Because the tube is certified for the **exact** solution of the exact-rational
IVP (§3.4), this is an exact-rational certificate; the float mesh and float
collocation data are only the centre of the tube.

---

## 2. Stage A — source-space correction (CERTIFIED conditioning, NUMERICAL values)

`L_h = I − A W` with `W` the hat-function (piecewise-linear) product-integration
weights and `A_n = S⁻¹ Dg(x̂(t_n)) S` in adapted coordinates
(`scripts/t6_stageA_source_space.py`, manifest `t6_stageA`).

| quantity | value |
|---|---|
| source-space sign-aware amplification `max_n Σ_k ‖(L_h⁻¹)_{nk}‖` | **9.40** at `t = 28.28` |
| state-space (TASK-0005) | 9.60 at `t = 23.1` |
| at `t = T` | 4.82 (T = 1000), **4.94** (T = 300, N = 12000) |
| float residual `‖L_h R − I‖` | 2.2e-16 |

The favourable conditioning survives the change of space. The rigorous version
of these numbers is the certified block table of §3.1 (row sums 9.408 max,
4.940 at T).

---

## 3. Stages B–D — rigorous constants and closure (CERTIFIED at T = 300)

### 3.0 Mesh

Defect-equidistributed mesh, `N = 12000`, `T = 300`, generated by
`scripts/t6_make_mesh.py` from the measured cell defects of the graded run
(`h_min = 1.39e-9`, `h_max = 0.0579`; file `computations/data/t6_mesh_T300_N12000.npy`).
Refining the late mesh alone (the request's first instruction) was **not** what
mattered: the binding defect sits at `t ≈ 0.02`, where the `t^α` singularity of
`x̂` makes the PL collocation defect `R ≈ 4e-5` on the graded mesh; the adaptive
mesh halves it (`R_max = 2.02e-5`, node defects `≤ 9.8e-9`).

### 3.1 Rigorous inverse (Stage C)

`msbg.cap.rigorous_inverse`: float forward-substitution inverse `R̃`, then the
exact residual `E = I − L_h R̃` is bounded entrywise by the float product plus
Higham's rounding bound plus the Arb radii of `W` and `A`; Neumann gives
`‖L_h⁻¹ − R̃‖` row-wise. This **establishes invertibility**.

| quantity | value |
|---|---|
| `‖E‖_∞` | **2.09e-10** |
| max inverse-correction `δ_n` | 1.18e-9 |
| `max_n Σ_k ‖(L_h⁻¹)_{nk}‖_F` | 9.408 (at `t = 28.29`); 4.940 at `T` |
| `‖B‖` in the certificate norm (sup / osc / bubble components) | **8.745 / 3.715 / 1.000** |

Three block tables are certified from `R̃`: the block norms `Rn`, the oscillation
blocks in two forms (direct differences with the nodal-increment split, and
Abel-summed cumulative differences), and the mean-kernel blocks
`Q = L_h⁻¹ A W_c` (row sums 8.00) that keep the sign cancellation between `L_h⁻¹`
and `A I^α` — the product of norms `‖R‖ ‖A‖ w` gives 206 for the same object.

### 3.2 The norm (Stage B) — what changed and why

The request's norm `max(sup|f|, max_n osc_n f / ϑ_n)` with fixed weights `ϑ_n`
cannot close here, for a reason that is quantitative, not a matter of tuning:
with a sup-norm ball on the source, `|I^α f| ≲ t^α/Γ(α+1) · sup|f|` is 135 at
`T = 300` (355 at 1000) and this factor enters the coupling `sup → osc → sup`
squared. The power iteration of §3.3 measures the resulting spectral radius:
**29** at `T = 1000` (graded `N = 6000`) with the first honest bounds.

What I use instead (all rigorous, all in `msbg/cap.py`):

* **cell-wise weights instead of a global norm.** `b = (ω_n, θ_n, β_n)` = bounds on
  `sup_{C_n}|f|`, `osc_n f`, `sup_{C_n}|(I−π)f|` (the "bubble"). The oscillation
  norm of the request is the special case `β = θ`, `ω ≡ const`.
* **the bubble component** is what `T1 = L_h⁻¹ π K (I−π)` actually sees; carrying
  it separately removes the artificial `sup → osc` feed. This alone took
  `ρ(M)` from 0.33 to 0.13 at `T = 300`.
* **oscillation of the PL part** by summation by parts / mean-kernel blocks
  (the naive `Σ_k ‖R_{n+1,k} − R_{n,k}‖ |z_k|` charges the full nodal value
  `|z_{n+1}| ≈ ‖A‖ t^α θ̄`, although `z` is smooth in `k`).
* **interpolation error of `A(x̂(t))`** through `osc_{C_n}(x̂')` evaluated as an
  exact float sum with the cancellation kept (the triangle inequality on
  `∫|x̂''|` is 250× too large in the tail).

All bounds are upper bounds derived by hand; `tests/test_cap.py::test_cellwise_bounds_dominate_explicit_functions`
checks every one of them against exact product integration of explicit
functions (PL + tent bubbles, smooth `A(t)`), three random seeds.

### 3.3 Linear part: spectral radius of the bound operator

The cell-wise bound map is `F(b) = Y + M b + Q₂(b)` with `M` non-negative and
linear (`T1 + T2`), `Q₂` bilinear (`Z2`). `ρ(M) < 1` is **necessary** for the CAP
to close in **any** norm built from these components with these bounds; the
power iteration gives Collatz–Wielandt brackets.

| `T` | mesh | `N` | code state | `ρ(M)` bracket | note |
|---|---|---|---|---|---|
| 1000 | graded r=3 | 6000 | first honest bounds | [28.7, 29.5] | osc of PL part charged at full nodal value |
| 1000 | graded r=3 | 6000 | + nodal-increment split | [3.82, 3.83] | |
| 1000 | graded r=3 | 6000 | + exact `osc(x̂')` | [3.76, 3.76] | EA 250× smaller, ρ unchanged: EA was not the binding term |
| 1000 | graded r=3 | 6000 | + Abel blocks | [1.00, 1.27] | |
| 1000 | graded r=3 | 12000 | + Abel blocks | [2.41, 2.41] | (two-component) |
| 1000 | graded r=3 | 6000 | + mean-kernel `Q` | [0.99, 1.25] | |
| 300 | graded r=3 | 6000 | + mean-kernel `Q` | [0.318, 0.391] | diagnostic (pre-final `state_sup`) |
| 300 | tri (early refined) | 8000 | + bubble component | [0.125, 0.133] | diagnostic (pre-final `state_sup`) |
| **300** | **adaptive** | **12000** | **final (`c9bc2f8`)** | **[0.0707, 0.0813]** | **certified constants** |
| 1000 | tri (early refined) | 14000 | + bubble component | [0.191, 0.200] | diagnostic; nonlinear iteration diverges |

Linear couplings in the Perron weights of the final run: `T1 sup 0.081`,
`T1 osc 0.063`, `T2 osc 0.081` (all others `≤ 0.004`).

### 3.4 Closure (Stage D) — the certificate

`scripts/t6_stageD_close.py` on the certified blocks of `t6_stageBD_adaptT300_N12000`:

1. **Monotone iteration** `b ← F(b)` from `b = Y` converges in 13 steps.
2. **Self-map.** With `b := (1 + 0.01) b_lim`, `F(b) < b` **componentwise** (3 × 12000
   inequalities); `max_n (F(b) − b)/b = −6.036e-4 < 0`. This is the componentwise
   radii inequality: `T` maps the closed convex set
   `S_b = {f : sup_{C_n}|f| ≤ ω_n, osc_n f ≤ θ_n, sup_{C_n}|(I−π)f| ≤ β_n}` into itself.
   Inflations `≥ 3 %` fail — the quadratic margin is thin.
3. **Contraction.** For `f ∈ S_b`, `DT(f) h = (I − B(I−K)) h + B (K_f − K) h`; with
   `q` = Perron weights of the map `h ↦ M h + Z2'(b) h` (recomputed rigorously for
   that `q`), the Lipschitz constant of `T` on `S_b` in `‖h‖_q = max_c max_n h_c[n]/q_c[n]`
   is **`κ ≤ 0.083612`**. `‖·‖_q` is equivalent to the sup norm, `S_b` is closed,
   hence complete.
4. **Banach** ⇒ unique `f* ∈ S_b` with `T f* = f*`; `B` is injective (Stage C), so
   `H(f*) = 0`, i.e. `x = x̂ + I^α f*` solves the Volterra equation `x = p + I^α g(x)`
   on `[0, 300]`, which is equivalent to the Caputo IVP (`g∘x` continuous); by the
   standard uniqueness for locally Lipschitz `g`, `x` is **the** solution.

Certificate numbers (manifest `t6_stageD_adaptT300_N12000`, weights in
`computations/data/t6_stageD_adaptT300_N12000_certificate_weights.npz`):

| quantity | value |
|---|---|
| source error `sup_{[0,T]} |f*|_S` (max / median / at `T`) | **3.177e-4** / 5.71e-6 / 2.06e-6 |
| `θ_max`, `β_max` | 1.048e-3, 3.07e-4 |
| adapted state error `|x − x̂|_S` (max over `[0, T]`, attained at `T`) | **4.866e-4** |
| physical state error `|x − x̂|_2` | **2.219e-4** |
| per-cell Lipschitz constant `D2` of `x ↦ A(x)` on the tube (max / at `T`) | 5.568 / 0.830 |
| iterations / inflation | 13 / 1 % |

Where the sup/osc-only ("two-component", `β = θ`) formulation stands on the same
blocks: `ρ(M) = [0.174, 0.204]`, and the b-iteration **also closed** there with
`Ω ≤ 3.66e-3` — 7.5× worse and at the pre-final code; the certified numbers above
are the three-component ones.

### 3.5 Scalar radii polynomial (the request's item) — does NOT hold

In the certificate's own norm (`r = 1` is `S_b`): `Y0 = 0.990`, `Z1 = 0.937`,
`Z2(1) = 0.458`, so `p(1) = Y0 + Z1 + Z2(1) − 1 = +1.385 > 0`. Mixing the Perron
weights with the certificate weights (six mixtures, `scripts/t6_summary.py`)
gives `Z1 = 0.937` throughout and `Z2a r ≫ 1 − Z1` at the useful radius; in the
pure Perron norm `Y0 = ∞` (the Perron vector vanishes on early cells where the
defect does not). See §5.3 for why the scalar statement is weaker than the vector
one and cannot be recovered here by choosing weights.

---

## 4. Stage E — rigorous `M_T`, infinite post-cut sup (CERTIFIED)

`scripts/t6_stageE_m1.py` feeds the certified pad into the TASK-0004 machinery
(`msbg.validated_res`: `nonlinearity_sup` on padded Arb boxes, `kernel_integrator`
envelope for `K_J`, `memory_tail_bound` with `sup_{t ≥ T}` taken analytically from
the decreasing Mittag-Leffler envelopes, `adapted_C`, `m1_radius`).

| constant | value |
|---|---|
| `K_J` (`∫₀^∞ ‖Ψ_J‖`, upper) | **11.34990** |
| `C_r` | `C0 + c3 r`, `C0 = 0.36955`, `c3 = 0.16274` |
| `M_T` (sup over `t ≥ 300`) | **4.32324e-2** = linear flow 4.0157e-2 + far history 1.2707e-3 (`σ₁ = 25`) + near history 1.8045e-3 |
| `r` | `2221/20000 = 0.11105` |
| `r − K_J C_r r² − M_T` | **`≥ +1.35626e-2`** |
| `K_J C_r r` | `≤ 0.48856 < 1` |
| verdict | **SEPARATED** |

The request said "do not derive `M_T` solely from a worst-case uniform state
tube". I did use the tube — but the tube is the sign-aware CAP tube
(`2.2e-4` physical), not a Gronwall tube, and `M_T` is dominated (93 %) by the
linear flow of `p − E*`, which does not depend on the history at all. The
goal-oriented dual bound of TASK-0005 would improve only the 7 % history part;
it is not needed.

`M_T` is far larger than at `T = 1000` would be (the linear-flow term decays like
`t^{−α}`), which is why the T=300 margin is `1.4e-2` rather than the `~4e-2` the
`T = 1000` pilot suggested. It is still strictly positive with rigorous constants.

---

## 5. Where the obstruction was (and was not)

Chief asked which of five candidates obstructs. Measured answer:

| candidate | verdict | evidence |
|---|---|---|
| source-space inverse conditioning | **not an obstruction** | amplification 9.4, `‖E‖ ≤ 2e-10`, row sums certified |
| oscillation `Z1` | **an artifact of the bounds, not of the operator** | `ρ(M)` fell 29 → 3.8 → 1.1 → 0.13 → 0.08 by sharpening bounds on the *same* operator (§3.3); the true linear part is strongly contracting at `T = 300` |
| nonlinear `Z2` | **the binding term** | with `ρ(M) = 0.35` the linear fixed point exists but `Z2/b = 78` at `t ≈ T` (graded N=6000); scales as `(‖I^α‖ · defect)²`; fixed at T=300 by halving the early defect and using the per-cell adapted Lipschitz constant (0.83 at `T` instead of the norm-product 15.7); **still binding at T = 1000** |
| residual `Y0` | **indirectly binding** | the cell defect near `t ≈ 0.02` (`x̂` has the `t^α` singularity) is what drives `Z2`; late-mesh refinement does not touch it |
| goal functional `M_T` | not an obstruction | separates at T = 300 with margin `1.36e-2` |

### 5.3 Why the scalar radii polynomial fails and the vector one does not

The scalar inequality needs a single norm in which (i) `Y0` is small (weights not
small where the defect lives — early cells), (ii) `Z1 < 1` (weights *must* be tiny on
early cells, otherwise the early bubbles feed `T1` downstream through `Σ_j w_{kj} β_j`
with `Σ_j w_{kj} ≈ t^α/Γ(α+1)`), and (iii) `Z2 r` small. (i) and (ii) pull the
weights in opposite directions on the same cells; every mixture I tried lands at
`Z1 ≈ 0.94` and `Z2a r > 0.06`. The componentwise inequality `F(b) < b` does not
require one norm: each cell is dominated by whichever term is large *there*
(`Y` early, `T1`/`Z2` late). It is the standard positive-operator (Perron)
argument, and the contraction constant is computed in the norm that the operator
itself selects. Both statements are rigorous Banach fixed-point theorems; the
vector one is strictly stronger.

---

## 6. `T = 1000` (OPEN)

| mesh | `N` | `ρ(M)` | nonlinear iteration | status |
|---|---|---|---|---|
| graded r=3 | 6000 | [0.99, 1.25] | — | linear part fails |
| graded r=3 | 12000 | [2.41, 2.41] (two-comp.) | — | |
| hybrid (graded to 30, `h = 0.108`) | 12000 | [1.91, 1.91] (two-comp.) | — | |
| tri (refined to 1, `h_tail = 0.121`) | 14000 | [0.191, 0.200] | **diverges** in 5 steps | quadratic term |
| adaptive (`h_tail = 0.098`) | 20000 | running at time of writing | | |

Inferred: closing `T = 1000` needs the early defect another ~5–10× smaller
(`‖I^α‖ = 355` vs 135, squared), i.e. `N ≳ 30000–40000` on an adaptive mesh
(dense inverse `≈ 50 GB`, feasible on ORION) or degree-2 collocation near `t = 0`.
It is not needed for the theorem.

---

## 7. What is rigorous, and under which model (read before promoting)

* **Arb (ball arithmetic, 128-bit):** hat weights `W` (`rigorous_hat_weights`), cell
  state boxes / defect sups / `A_n` and `osc(A)` (`validated.verify_cells`,
  `cap.nodal_data`), all Stage-E constants (`K_J`, `C_r`, `M_T`, Mittag-Leffler
  envelopes), the exact rational parameters and `S`.
* **binary64 with declared rounding bounds:** the inverse residual (Higham
  `γ_n` bounds + Arb radii of the data), the block norms (Frobenius ≥ operator
  norm), the cell weights `w_j(t)` (evaluated via `expm1/log1p` with the exact cell
  width, `1e-13` relative slack), the mesh-geometry constants (`c_loc`, `c_prev`,
  `c_α` by subinterval enclosure; `osc(x̂')` as exact float sums with a summation
  rounding bound), the bound operator evaluations (all sums of non-negative
  terms with outward `1e-13` slack). **Assumption:** IEEE-754 binary64 with
  correctly rounded `+ − × ÷ sqrt` and libm `pow/expm1/log1p/gamma` accurate to a
  few ulp. This is the same model as TASK-0004's float layers; it is not an
  end-to-end interval computation. A reviewer who wants Arb end-to-end has
  every formula in `msbg/cap.py` docstrings; the cost is ~50× in the `O(N²)` parts.
* **Not rigorous, corroboration only:** the collocation itself (centre of the
  tube), the mesh generator, the cross-check of §8.

Known rigour traps found and fixed during this task (both would have produced
non-upper bounds): the cell weight `hi^α − lo^α` for tiny far cells (cancellation,
`1e-5` relative error) and the cell sup of `I^α f` for non-constant `ω` (the
end-point weight sum is not an upper bound). Tests cover both. Results quoted
as **certified** were all produced after both fixes (code `c9bc2f8`); earlier
runs appear only in §3.3's diagnostic rows.

---

## 8. Corroboration (NUMERICAL)

Independent PL collocation on a different mesh (graded r=3, `N = 9000`) vs the
certified centre `x̂`, adapted norm, against the certified radius `Ω_n`:

| `t` | `|x̂₁ − x̂₂|_S` | certified radius | ratio |
|---|---|---|---|
| 0.5 | 9.5e-7 | 4.1e-5 | 0.023 |
| 8.99 | 1.8e-7 | 1.3e-4 | 0.0014 |
| 28.3 | 2.4e-7 | 2.1e-4 | 0.0011 |
| 150 | 1.2e-9 | 3.8e-4 | 3e-6 |
| 300 | 5.3e-9 | 4.9e-4 | 1e-5 |

The tube is 40–10⁵× wider than the disagreement between two independent
discretisations: consistent, and it says the certified tube is loose by
those factors, mostly through `Y` (the defect sup on early cells) and the
`Σ_j w_{kj}` accumulation.

---

## 9. Reproduction

```
cd computations && export OMP_NUM_THREADS=16
python scripts/t6_make_mesh.py --src T300_N6000_graded3 --T 300 --N 12000 --hcap 0.1 \
       --out data/t6_mesh_T300_N12000.npy          # needs the graded-run blocks (or use the committed .npy)
python scripts/t6_stageBD_cap.py --T 300 --N 12000 --mesh file:data/t6_mesh_T300_N12000.npy \
       --K 32 --workers 48 --iters 300 --tag adaptT300_N12000   # ~15 min on ORION, saves blocks + certificate
python scripts/t6_stageD_close.py --tag adaptT300_N12000        # rho(M), F(b)<b, contraction (from saved blocks)
python scripts/t6_stageE_m1.py   --tag adaptT300_N12000 --K 32 --workers 48   # entry + M_T + M1
python scripts/t6_summary.py     --tag adaptT300_N12000        # ||B||, radii-polynomial attempts, cross-check
python -m pytest tests/test_cap.py -q                            # 14 tests
```

Manifests (committed): `computations/manifests/t6_stageBD_adaptT300_N12000_manifest.json`,
`t6_stageD_adaptT300_N12000_manifest.json`, `t6_stageE_adaptT300_N12000_manifest.json`,
`t6_summary_adaptT300_N12000_manifest.json`; diagnostics `t6_stageBD_T{10,300,1000}_N6000_graded3`,
`t6_stageD_T1000_N14000_tri_1_4000_30_2000`, `t6_stageA`; TASK-0002 attempts
`t2_stageA_certify_Q_B215_{N12000,T10,T12,T10_r08}`. The 2.6 GB block file
(`data/t6_stageBD_adaptT300_N12000_blocks.npz`) stays on ORION
(`~/msbg/computations/data/`), regenerable by the first pipeline command.

Compute: ORION only (172 cores, `nice 15`, ≤ 48 workers per run); AUREUS unused.
No orphan processes left except the `T = 1000, N = 20000` run reported in §6.

---

## 10. Recommended next steps (Chief's call)

1. Promote TARGET-A20 for B215 on the basis of §§1, 3.4, 4 — with the evidence
   class "CERTIFIED COMPUTATION under the declared floating-point model", and
   state the vector-radii/Perron form of the Banach argument in the write-up
   rather than the scalar radii polynomial.
2. If an end-to-end Arb certificate is wanted for publication: re-run the
   `O(N²)` float layers of `cap.py` in Arb (mechanical; the formulas are fixed).
3. `T = 1000` only if a second cut is wanted as redundancy; expect `N ≳ 30000`.
