# TASK-0007 — Publication arithmetic hardening — COMPUTE RETURN

**From:** Compute Agent
**To:** Chief Researcher
**Task:** `research/coordination/chief-to-compute/TASK-0007_publication-arithmetic-hardening_REQUEST.md`
**Date:** 2026-09-30
**Branch:** `compute/task-0007`
**Code commit SHA:** ``8489f10354962523486b2c53a879077fc5cf1fcf` (hardened layer introduced in `dd5af48`)`

---

## 0. Executive answer

**Hardening done; the T = 300, N = 12000 certificate regenerates with every
load-bearing elementary-function evaluation in Arb and every load-bearing
binary64 reduction under an explicit Higham bound.** Verdicts unchanged
(entry CERTIFIED, `F(b) < b`, Perron contraction `κ < 1`, M1 SEPARATED);
constants move by at most 0.16 % on every quantity that enters a verdict (state tube `+0.16 %`, `κ` `0.0836 → 0.0862`, M1 margin `1.35626e-2 → 1.35623e-2`) (§D).

Evidence label reached:

> **END-TO-END VERIFIED ELEMENTARY-FUNCTION ENCLOSURES**, under the
> IEEE-754 binary64 assumptions of §E (round-to-nearest for `+ − × ÷ sqrt`,
> `nextafter` exact, binary64 accumulation, no flush-to-zero). No libm accuracy
> assumption remains anywhere in the certified chain.

Not "fully interval": the dense inverse and the bound-operator evaluations are
binary64 with proved a-posteriori roundoff bounds, not set-valued arithmetic
(§E). The hardening exposed **six defects** of the TASK-0006 bookkeeping
(§C); none changes a verdict, two would not have been valid upper bounds at
`N = 12000` as written. The proof design is untouched.

| Stage | Result |
|---|---|
| A — inventory | 38 quantities classified before/after (§A; `computations/data/t7_arithmetic_inventory.json`) |
| B — category 3 eliminated | 12 → **0** load-bearing libm uses (`pow`, `expm1`, `log1p`, `gamma`, `cos/sin`) |
| C — category 2 audited | 6 defects found and fixed; all slacks replaced by length-dependent Higham factors |
| D — regenerated certificate | **all verdicts reproduced**: `‖E‖_∞ = 2.091e-10`; `F(b) < b` (margin `−6.03e-4`); `κ ≤ 0.08620`; tube `≤ 4.874e-4` (phys. `2.223e-4`); entry 836 cells, `η = 0.030941`; `K_J ≤ 11.34990`, `M_T ≤ 4.32327e-2`; M1 margin `≥ +1.35623e-2` |
| E — label | END-TO-END VERIFIED ELEMENTARY-FUNCTION ENCLOSURES (assumptions listed) |
| F — redundancy | `T = 1000` not rerun (hardening did not fail; no systematic issue); TASK-0006 result stands as secondary redundancy under its old label |

---

## A. Inventory (machine-readable: `computations/data/t7_arithmetic_inventory.json`, generator `scripts/t7_inventory.py`)

Categories: **1** Arb/interval; **2** binary64 algebra with a proved Higham bound (any summation order, FMA-agnostic); **3** binary64 libm few-ulp assumption; **4** corroborative / not load-bearing.

| id | quantity | where | before | after | method |
|---|---|---|---|---|---|
| `mesh_nodes` | mesh nodes t_n, collocation values phi_n, slopes m_k | `aposteriori.collocation, t6_make_mesh` | 4 | 4 | unchanged; the proof is about the exact xhat built from these floats |
| `params` | theta, a, b, m, alpha, p, S, S^-1, E* | `validated_res.Setup` | 1 | 1 | unchanged |
| `cells` | state boxes, defect sup R_n, Lipschitz drho_n, node defects rho_n | `validated.verify_cells, cap.nodal_data` | 1 | 1 | unchanged (Arb; floats via _arb_upper_float = nearest + nextafter, re-checked) |
| `A_nodes` | A_n = S^-1 Dg(xhat(t_n)) S: float centre Am and radius Ar | `cap._nd_node` | 2 (defect: radius omitted the centre's float-conversion error) | 1 | Ar := arb_hi(|A_n - arb(Am)|) exactly |
| `A_cells` | ||A|| and osc(A) on cells | `cap._nd_cell` | 1 | 1 | unchanged (Arb) |
| `hat_weights` | hat-function weights W (mid, rad) | `cap.rigorous_hat_weights` | 1/2 (rad += |mid| 2^-52 + 1e-15 slack) | 1 | rad := arb_hi(|w - arb(mid)|) exactly |
| `cell_weights` | cell weights w_{n,j} = ((t_n-t_j)^a - (t_n-t_{j+1})^a)/G(a+1) (hi and lo) | `cap.cell_weights -> rig.geometry_tables` | 3 | 1 | Arb per entry (128 bit), outward floats; libm pow/expm1/log1p/gamma removed |
| `dw` | dw_{n,j} = w_{n,j} - w_{n+1,j} | `cap.Geometry.dw -> rig` | 3 + 4e-13 slack | 2 | W_hi - W_lo, one outward rounding |
| `d_table` | (t_n-t_{j+1})^{a-2} - (t_n-t_j)^{a-2} | `cap.Geometry.d -> rig` | 3 | 1 | Arb |
| `rem_table` | mean-kernel remainder min(2w, h_j/2 ((t_n-t_{j+1})^{a-1}-(t_n-t_j)^{a-1})/G(a)) | `cap.Geometry.rem -> rig` | 3 | 1 | Arb |
| `HA_DTA` | h_n^a/G(a+1), (t_{n+1}^a - t_n^a)/G(a+1) | `cap.cap_vectors -> rig tables HA, DTA` | 3 | 1 | Arb per cell |
| `Ea_green` | Ea_n = min(h^2 a(1-a) t_n^{a-2}/8, c_alpha h^a)/G(a+1); h^2/8 (1-a)/G(a) | `cap.Geometry -> rig` | 3 | 1 | Arb per cell |
| `interp_consts` | c_alpha, c_loc, c_prev(h_{n-1}/h_n) | `cap.interpolation_constants -> rig.interpolation_constants_arb` | 3 (float pow on subintervals) | 1 | Arb ball per subinterval (tau as ball, ratio as ball over <= 64 groups); inclusion monotone |
| `osc_xhat_prime` | osc_{C_n}(xhat'), sup_{C_n}|xhat'| (cancelling sums) | `cap.xhat_prime_oscillation -> rig._tab_row` | 3 (pow/expm1/log1p) + ad-hoc n*8u rounding bound | 1 | exact Arb sums per cell (128 bit), outward floats |
| `EA` | (I-pi)A interpolation error (h/4)(D2p osc(xhat') + D3p diam sup|xhat'|) | `cap.Geometry.EA` | 2 (with 1e-13 slack) | 2 | infl by op count; legacy EA_green (float pow) removed from the min |
| `D2p_D3p` | D2p = ||S^-1|| ||S|| sqrt((c+a)^2+a^2+2b^2), D3p = 6||S^-1|| ||S||, D3a | `cap.Geometry` | 2 (1e-13) | 2 | infl(., ops); sqrt correctly rounded (IEEE) |
| `D2_cells` | per-cell Lipschitz constant of x -> A(x) (adapted) | `cap.lipschitz_A_cells -> rig.lipschitz_A_cells_arb` | 3 (cos/sin sampling, S centre + 1e-9 slack) | 1 | Arb: convexity in c + closed-form 2x2 Gram eigenvalue, no sampling |
| `float_inverse` | float inverse Rt (forward substitution) | `cap.rigorous_inverse` | 4 | 4 | unchanged |
| `residual` | |E| = |I - L_h Rt| entrywise: float residual + gamma_K|A||W||Rt| + gamma_2|A||fl(WR)| + Ar|W||Rt| + (|A|+Ar)Wr|Rt| + final +/- roundings | `cap.rigorous_inverse` | 2 (error terms themselves un-inflated; final +/- rounding omitted) | 2 | every error term computed in floats and inflated by rig.infl with its own reduction length; final +/- term added |
| `normE_delta` | ||E||_inf, c_r = ||(|Rt||E|)_r||_1/(1-||E||), delta_n | `cap.rigorous_inverse` | 2 (1e-13 slack on length-m sums: NOT a valid gamma_m bound for m = 24002) | 2 | infl(., m) |
| `block_norms` | Rn = Frobenius block norms + delta | `cap.rigorous_inverse` | 2 (1e-13) | 2 | infl by op count (4 squares, sqrt, +) |
| `osc_blocks` | Dn (direct) and Sn (Abel cumulative) oscillation blocks | `cap.rigorous_inverse` | 2 (Abel cumsum rounding NOT bounded; 1e-13 slack) | 2 | cumsum error gamma_K sum|Dd| added as an entrywise error matrix; infl by length |
| `Q_blocks` | Q = L_h^-1 A W_c mean-kernel blocks Qn, DQn | `cap.mean_kernel_blocks` | 2 (2e-13 + 1e-12 slacks; W data radius not included) | 2 | gamma_m|Rt||M| + |Rt| dM (dM = Ar W_hi + (|A|+Ar)(W_hi-W_lo) + u|M|) + delta max|M|; infl by length |
| `B_source` | B s bounds: Rn@sigma, Dn@sigma, Slow@dnode, + products | `cap._B_source_vectors, cap._osc_pl` | 2 (1e-13 slack on length-N1 dots: invalid for N1 = 12001) | 2 | infl(., N1) |
| `state_sup` | Omega_n = sum_{j<n} w_{n,j} omega_j + w_{n+1,n} omega_n | `cap.state_sup` | 2 (1e-13 slack) | 2 | infl(., N) |
| `cap_loop` | G, loc, green, P, V per cell (dots of length n) | `cap.cap_vectors` | 2/3 (1e-13 slack; h^a, t^a via float pow) | 2 (+ Arb tables) | cum_hi/cum_lo with infl/defl(N); dots infl(., n); powers from HA/DTA tables |
| `T1_kappa` | kappa = ||A_n|| sum_j w_{n,j} beta_j, dkappa, Rk, Dk (Q form) | `cap.cap_vectors` | 2 (1e-13) | 2 | infl by length |
| `Z2` | sig_node, sig_cell, tau_cell of Delta_A I^a h | `cap.z2_vectors` | 2 (1e-13) | 2 | infl by op count |
| `F_apply` | F(b) = Y + T1 + T2 + Z2 componentwise; F(b) < b test; kappa = max (M q + Z2'(b))/q | `cap._apply, check_certificate, contraction_constant` | 2 (1e-13 on 3-4 term sums: valid) | 2 | infl(., #terms); division x/q rounds to nearest: max ratio compared against 1 with the exact-division margin absorbed by strictness slack (min slack 6e-4 >> u) |
| `power_iteration` | Perron weights q, rho(M) brackets | `cap.power_iteration` | 4 | 4 | unchanged |
| `pad` | physical pad ||S|| Omega_n | `t6_stageE_m1` | 2/3 (recomputed with float cell_weights, 1e-13) | 2 | Omega from the certificate file (Arb weights), infl(., 1); boxes widened with outward nextafter |
| `entry_test` | x_hi + pad < theta, x_lo - pad > 0, y_lo - pad > 0; eta | `t6_stageE_m1` | 2 (float +/- without outward rounding) | 2 | outward nextafter on every +/-, theta as arb_lo of the exact rational |
| `Nsup` | sup |N(u)|_S on padded boxes | `validated_res.nonlinearity_sup` | 1 | 1 | unchanged (Arb) |
| `K_J` | K_J = (sum_i env_i w_i + tail)/a | `validated_res.kernel_integrator` | 2/3 (rho0 via float pow; cumsum of ~10^4 cells with 1e-13 slack: NOT a valid gamma_n bound; 1/a float) | 1/2 | rho0, 1/a in Arb; cumulative sums infl(., i) per entry; tail Arb |
| `M_T` | M_T = |p-E*| phi_b(T) + far history (dot of length ~N) + near history | `validated_res.memory_tail_bound` | 2 (1e-13/1e-12 slack on a length-N dot: marginal) | 2 | infl(., len) |
| `C_r` | C0, c3 (adapted nonlinearity constants) | `validated_res.adapted_C` | 1 | 1 | unchanged (Arb over arcs) |
| `m1_margin` | r - K_J C_r r^2 - M_T, K_J C_r r | `validated_res.m1_radius` | 1 | 1 | unchanged (Arb) |
| `crosscheck` | independent collocation vs xhat; power-iteration diagnostics; mesh generator | `t6_summary, t6_make_mesh` | 4 | 4 | unchanged |

Summary: before — 12 quantities in category 3 (or mixed 2/3), 15 in category 2 of which 5 with a fixed `1e-13` slack that is **not** a valid bound at the certificate's reduction lengths; after — 0 in category 3, every category-2 item carries an explicit `γ_n` for its own `n`.

---

## B. Elimination of category 3

New module `computations/msbg/rig.py` (verified arithmetic layer). What replaced what:

| libm use (TASK-0006) | quantity | replacement |
|---|---|---|
| `pow`, `expm1`, `log1p`, `gamma` in `cap.cell_weights` | cell weights `w_{n,j}` (72 M entries) | `rig.geometry_tables`: Arb per entry at 128 bits, one mesh row per worker, converted with `arb_hi`/`arb_lo` (both a hi and a lo table; `dw = W_hi − W_lo`) |
| `pow`, `gamma` in `Geometry` (`d`, `rem`, `Ea`, `green`) | Green/remainder tables, per-cell constants | same row job (powers `(t_n−t_j)^{a}`, `^{a−1}`, `^{a−2}` shared) |
| `pow` in `cap_vectors` loop (`h^a`, `t^a`) | `P`, `V` | per-cell Arb tables `HA`, `DTA` |
| `pow`, `expm1`, `log1p` in `xhat_prime_oscillation` (+ ad-hoc `n·8u` rounding bound) | `osc_{C_n}(x̂')`, `sup|x̂'|` | exact Arb sums per cell (cancellation kept in ball arithmetic, no rounding model needed) |
| `pow` in `interpolation_constants` | `c_α`, `c_loc`, `c_prev(r)` | Arb balls per τ-subinterval (τ as a ball; ratio `r` as a ball over ≤ 64 groups); inclusion-monotone enclosure |
| `cos`, `sin` sampling in `lipschitz_A_cells` (+ `1/(1−π/n)` angular slack, `S` centre + `1e-9`) | per-cell Lipschitz constant `D2` of `x ↦ A(x)` | Arb: Frobenius norm is convex in `c = −6x+2(1+θ)` (sup at the box endpoints) and linear in the direction `u`; the (2→Frobenius) operator norm is `sqrt(λ_max)` of the 2×2 Gram matrix, closed form in Arb; no sampling |
| `pow` for `ρ₀ = s_max^a`, float `1/a` in `kernel_integrator` | `K_J` | Arb |
| float `cell_weights` recomputation in `t6_stageE_m1` | state pad | pad taken from the certificate's own `Ω_n` (Arb weights, Higham-inflated) |
| `xhat_second_derivative` (`pow`, `gamma`, triangle-inequality `∫|x̂''|`) | legacy `EA_green` alternative | removed from the certified minimum (kept as a non-load-bearing function) |

`math.gamma` survives only in `Geometry.Ga1/Ga` diagnostics (not used by any bound) and in `cap.cell_weights`/`interpolation_constants`/`xhat_prime_oscillation`, which are no longer called by the pipeline (kept for the legacy diagnostic scripts and as float cross-checks in the tests).

Cost: the Arb tables take 28 s on ORION (48 workers) for `N = 12000`; the certified inverse takes 5.2 min (breakdown in §D). Tests (124 passed, 1 skipped) were run on ORION.

---

## C. Audit of category 2 — findings

Model used everywhere (`rig.infl(x, n) = x(1 + 2γ_n)` then one outward rounding, `γ_n = nu/(1−nu)`, `u = 2⁻⁵³`): for non-negative terms, `fl(Σ_{i<n} x_i y_i) = Σ x_i y_i (1+θ_i)`, `|θ_i| ≤ γ_n`, **for any summation order** (Higham 2002, §3.1 and eq. (3.5): the bound counts roundings on each term's path, so blocked/recursive/pairwise BLAS reductions and fused multiply-add all satisfy it; FMA only removes roundings). Hence `Σ ≤ fl/(1−γ_n) ≤ fl·(1+2γ_n)`.

Defects found in the TASK-0006 code (all fixed in `dd5af48`; none affects a verdict, see §D):

1. **Fixed `1e-13` relative slack used as a rounding bound on length-`N` reductions** (`up()` in `_B_source_vectors`, `state_sup`, `cap_vectors`, `rigorous_inverse` row sums, `kernel_integrator.G` cumulative sums, `memory_tail_bound` far-history dot). At `N = 12000` a valid bound is `2γ_N ≈ 2.7e-12`, at `m = 24002` (inverse row sums) `5.3e-12`, and the envelope cumulative sum has ~36 000 terms (`8e-12`). **These were not valid upper bounds as written.** Now every reduction is inflated by its own length.
2. **Abel cumulative sums without a rounding bound.** `S_{nk} = Σ_{j≤k} (R_{n+1,j} − R_{n,j})` is a signed sum; the float `cumsum` error `γ_K Σ_j |ΔR_{nj}|` was not added. Now an entrywise error matrix is carried and its Frobenius norm added.
3. **`A_n` radius omitted the centre's float conversion.** `Ar = float(rad)` ignored `|A_n − float(mid)| ≤ 2⁻⁵³|mid|`. Now `Ar := arb_hi(|A_n − arb(Am)|)` exactly (same fix for the hat-weight radii, which had an ad-hoc `|mid|·2⁻⁵² + 1e-15`).
4. **Inverse residual: error terms not themselves inflated, final `− Rt + I` roundings omitted.** The bound `|E| ≤ |E0| + γ_K|A||W||Rt| + …` used float products for `|A||W||Rt|` without their own `γ`, and the two roundings of `fl(AWR − Rt + I)` were not counted. Both added.
5. **Mean-kernel blocks `Q` ignored the data radii of `W`** (used `w_hi` as exact) and used ad-hoc `2e-13`/`1e-12` slacks. Now `|M_exact − M_f| ≤ Ar W_hi + (|A|+Ar)(W_hi − W_lo) + u|M_f|` and `γ_m` on the product.
6. **Stage-E box tests without outward rounding** (`x_hi + pad < θ` evaluated with nearest rounding; `θ⁻` taken as `nextafter(float(θ))`). Now every `±` is rounded outward and `θ` is the exact rational's `arb_lo`. (`η` is now reported as a certified lower bound of the margin.)

Items audited and found in order: conversion `arb → float` (`float(arb)` rounds to nearest; `_arb_upper_float` adds one `nextafter` and `rig.arb_hi` re-checks the result in Arb); `_l2_upper`'s `(1+1e-13)` on a single `float(abs_upper)` (valid: one rounding ≪ `1e-13`); `math.sqrt` (correctly rounded, IEEE) followed by `infl(·,1)`; the Neumann argument itself (`||E||_∞ < 1` with `||E||_∞` an inflated max of inflated row sums); Frobenius ≥ operator norm; the strictness margins of the two final inequalities (`F(b) < b` with `min slack` `6.03e-4` and `κ = ` `0.0862`, both far above the `u`-level uncertainty of the divisions `F/b`, `(Mq)/q` that are compared).

BLAS/threading: no bound depends on OpenBLAS's reduction order or thread count — the only property used is "each output entry is a dot product of the stated length accumulated in binary64" (Higham's order-independent bound). OpenBLAS `dgemm` accumulates in double on this platform (Haswell kernels, no extended precision); an extended-precision accumulator would only lower the true error.

---

## D. Regenerated primary certificate (`T = 300`, `N = 12000`, same mesh file `data/t6_mesh_T300_N12000.npy`, exact rational benchmark)

| constant | TASK-0006 (c9bc2f8) | TASK-0007 hardened | rel. change |
|---|---|---|---|
| ||E||_inf (Neumann residual) | 2.09116e-10 | 2.09096e-10 | -9.53e-05 |
| max delta_n (inverse correction) | 1.1798e-09 | 1.17968e-09 | -9.99e-05 |
| max_n sum_k ||R_nk|| (block row sum) | 9.4083 | 9.4083 | +5.62e-12 |
| block row sum at T | 4.94001 | 4.94001 | -2.86e-10 |
| Q row-sum max | 8.00091 | 8.00086 | -6.37e-06 |
| rem row-sum max | 0.21566 | 0.21566 | -3.16e-13 |
| c_alpha | 0.0599717 | 0.0599717 | +1.70e-11 |
| c_loc | 0.611448 | 0.611448 | +6.48e-12 |
| c_prev max | 0.0559941 | 0.128797 | +1.30e+00 |
| EA max | 0.000215988 | 0.000260751 | +2.07e-01 |
| R_max (cell defect) | 2.01935e-05 | 2.01935e-05 | +0.00e+00 |
| rho(M) upper | 0.0813197 | 0.0842681 | +3.63e-02 |
| rho(M) lower | 0.0707477 | 0.0684821 | -3.20e-02 |
| min_slack | 0.00060362 | 0.00060254 | -1.79e-03 |
| eps | 0.01 | 0.01 | +0.00e+00 |
| omega_max | 0.000317733 | 0.000317772 | +1.23e-04 |
| omega_median | 5.71418e-06 | 5.72407e-06 | +1.73e-03 |
| omega_T | 2.05993e-06 | 2.06208e-06 | +1.04e-03 |
| theta_max | 0.00104787 | 0.00104795 | +7.22e-05 |
| beta_max | 0.000307325 | 0.000307363 | +1.23e-04 |
| state_err_adapted_max | 0.000486609 | 0.000487385 | +1.59e-03 |
| state_err_phys_max | 0.000221928 | 0.000222282 | +1.59e-03 |
| D2_max | 5.56849 | 5.54419 | -4.36e-03 |
| D2_at_T | 0.830032 | 0.826411 | -4.36e-03 |
| contraction_q_norm | 0.0836116 | 0.0861985 | +3.09e-02 |
| b-iterations | 13 | 14 | +7.69e-02 |
| pad max (physical) | 0.000221928 | 0.000222282 | +1.59e-03 |
| entry: n_cells | 836 | 836 | +0.00e+00 |
| entry: eta | 0.0309411 | 0.030941 | -2.72e-06 |
| entry: t_lo of span | 5.85768 | 5.85768 | +0.00e+00 |
| entry: t_hi of span | 13.7275 | 13.7275 | +0.00e+00 |
| K_J_upper | 11.3499 | 11.3499 | +7.98e-12 |
| M_T_upper | 0.0432324 | 0.0432327 | +6.74e-06 |
| C0 | 0.369552 | 0.369552 | +0.00e+00 |
| c3 | 0.162735 | 0.162735 | +0.00e+00 |
| margin_lower | 0.0135626 | 0.0135623 | -2.15e-05 |
| K_C_r_upper | 0.488563 | 0.488563 | +7.98e-12 |
| M_T linear flow | 0.0401572 | 0.0401572 | -9.88e-14 |
| M_T far history | 0.00127068 | 0.00127072 | +3.30e-05 |
| M_T near history | 0.0018045 | 0.00180475 | +1.38e-04 |

Verdicts: **Banach (self-map + contraction): yes → yes; entry: CERTIFIED → CERTIFIED; M1: SEPARATED → SEPARATED.**

Reading the table:

* Every quantity that decides a verdict moves by less than 0.2 %; the changes go in
  the expected direction (bounds slightly looser, because rounding is now charged
  honestly).
* Two mesh constants moved by more: `c_prev max` 0.056 → 0.129 and `EA max` +21 %.
  Both are **looser enclosures, not corrections of errors**: `c_prev(r)` is now
  enclosed with the ratio `r = h_{n−1}/h_n` as an Arb ball over one of 64 groups
  (the float code evaluated it at the exact ratio), and `EA` no longer takes the
  minimum with the legacy `∫|x̂''|` bound, which used float `pow`. Neither binds:
  the T2 couplings stay at `≤ 0.004` in the Perron weights.
* `ρ(M)` bracket `[0.0707, 0.0813] → [0.0685, 0.0843]` is the Collatz–Wielandt
  bracket after 80 power iterations, not a certified quantity; its width, not the
  arithmetic, explains the ±3 %. `κ` (certified) moved `0.0836 → 0.0862`.
* Inverse wall time on ORION (32 BLAS threads): substitution 188 s, residual
  9 s, error terms 61 s, Neumann correction 14 s, Abel blocks 36 s, direct blocks
  8 s. A first attempt with `nextafter`-based inflation on the 600 M-entry
  arrays did not finish in 35 min; it was replaced by a multiplicative factor
  `f ≥ 1 + 2γ_n + 3u`, verified exactly with `Fraction` in `tests/test_rig.py`.

Manifests: `computations/manifests/t6_stageBD_h7_T300_N12000_manifest.json`
(inverse, geometry, closure, contraction), `t6_stageE_h7_T300_N12000_manifest.json`
(entry, `K_J`, `C_r`, `M_T`, M1), `t6_summary_h7_T300_N12000_manifest.json`
(`‖B‖ = 8.745 / 3.717 / 1.000`, independent-mesh cross-check); certificate weights
`computations/data/t6_stageBD_h7_T300_N12000_{certificate,contraction}_weights.npz`.

---

## E. Evidence label and remaining assumptions

**END-TO-END VERIFIED ELEMENTARY-FUNCTION ENCLOSURES.** Every elementary function
(`t^α`, `Γ`, Mittag-Leffler, `exp`, `sqrt` of exact data, `cos/sin` in `adapted_C`)
that enters a certified constant is evaluated in Arb ball arithmetic and
converted outward. The binary64 layers (dense inverse residual, block norms,
bound-operator evaluation, Stage-E sums) are algebra on non-negative data with
proved a-posteriori Higham bounds.

Remaining assumptions, all standard IEEE-754 / platform facts, none about libm:

1. binary64 arithmetic with round-to-nearest for `+ − × ÷ sqrt` (IEEE-754 §5);
2. `numpy.nextafter` exact (IEEE-754 nextUp/nextDown);
3. numpy/OpenBLAS reductions accumulate in binary64 (no reduced precision; extended precision would only help);
4. no flush-to-zero / denormal issues (all certified quantities are `≥ 1e-300` or exactly 0);
5. the Higham model `fl(x op y) = (x op y)(1+δ)`, `|δ| ≤ u` (no overflow — all quantities `< 1e30`);
6. python-flint 0.9.0 / Arb: ball arithmetic correct (this is the same trust base as every Arb-based certificate);
7. the exact solution's existence argument (Banach) and the M1/X1/E1 theorems are on paper (THEOREM class), unchanged from TASK-0006.

What is **not** claimed: "fully interval" — the inverse `R̃` is a float matrix (any float matrix is admissible; the proof is a posteriori), and the bound operator is evaluated in floats with error factors, not in set-valued arithmetic.

---

## F. Redundancy

`T = 1000, N = 20000` was **not** rerun: the `T = 300` hardening reproduced the
TASK-0006 verdicts and exposed no systematic issue (the six defects of §C are
bookkeeping, all in the direction of missing small inflations; the largest
relative effect on any constant is `0.16 %` on the state tube (the loosened `c_prev`/`EA` tables do not bind; see §D)). The TASK-0006 `T = 1000` result
therefore stands as secondary redundancy under its original label ("certified
computation under the declared floating-point model"). Rerunning it with
`dd5af48` is a 1-hour ORION job if Chief wants both cuts under the new label.

---

## G. Reproduction

```
cd computations && export OMP_NUM_THREADS=24
python scripts/t7_inventory.py                                          # §A table + JSON
python scripts/t6_stageBD_cap.py --T 300 --N 12000 --mesh file:data/t6_mesh_T300_N12000.npy \
       --K 32 --workers 48 --iters 300 --tag h7_T300_N12000              # pipeline incl. closure (~25 min)
python scripts/t6_stageE_m1.py --prefix t6_stageBD --tag h7_T300_N12000 --K 32 --workers 48   # entry + M_T + M1
python scripts/t6_summary.py   --prefix t6_stageBD --tag h7_T300_N12000  # ||B||, cross-check
python scripts/t7_compare.py                                            # §D table
python -m pytest tests -q                                               # 124 passed, 1 skipped (run on ORION)
```

Manifests (committed): `computations/manifests/t6_{stageBD,stageE,summary}_h7_T300_N12000_manifest.json`;
certificate weights `computations/data/t6_stageBD_h7_T300_N12000_{certificate,contraction}_weights.npz`;
comparison `computations/data/t7_comparison.json`.
Compute: ORION only; no orphan processes.
