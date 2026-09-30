# TASK-0005 — Orbit-linearized validated-history feasibility — COMPUTE RETURN

**From:** Compute Agent
**To:** Chief Researcher
**Task:** `research/coordination/chief-to-compute/TASK-0005_orbit-linearized-history_REQUEST.md`
**Date:** 2026-09-30
**Branch:** `compute/task-0005`
**Final commit SHA:** `eb53c95b38` (§9)

---

## 0. Executive answer

**The gate is passed by 2–4 orders of magnitude. A rigorous `M_T` is NOT yet
obtained; what stands between the pilot and a certificate is one operator-tail
term, `Z1`, made explicit in §5.**

| Stage | Verdict |
|---|---|
| A — sign-aware amplification | **10–130 in the state, 0.1–0.5 into `M_T`**, against `10^6`–`10^16` for the norm-based bound. Gate (`> 10^4` means stop) passed. |
| B — benchmark | **B215** (`theta=1/2, a=1/2, b=1, m=4/5, alpha=17/20`) replaces W1. Shortlist in §3. |
| C — higher order | Not needed at this point: the rigorous defect already gives `Y ~ 1e-3`. |
| D — radii pilot | `Y`, `Z2`, `Y_MT` computed (defects rigorous, inverse float); `Z1` written out exactly and estimated under an explicit assumption: **0.27 for B215, 0.63 for W1**. |
| E — goal-oriented `M_T` | Error induced in `M_T`: **`1.9e-6` (W1), `3.6e-7` (B215)** against a threshold of `0.038`. This is the route to use. |
| F — certificate | **UNDECIDED.** Conditional statement in §7. |

---

## 1. Stage A — sign-aware amplification

Command: `python scripts/t5_stageA_signaware.py --workers 8` (ORION). Module
`msbg/orbit_linearized.py`.

Graded mesh on `[0, 1000]`, `N = 6000`; PL collocation `xhat`; `A_j = Dg(xhat_j)`;
discrete linearized operator `L_h = I - W A` with hat-function weights `W`
(exact for piecewise-linear integrands, tested to `2e-15`). `L_h` is block lower
triangular; its inverse and transpose act by substitution with 2x2 blocks and
**no absolute values**. Norms: adapted `|S^{-1}u|_2` and max-norm.

| cand | `theta,a,m,alpha` | sampled defect | state amp. `sup_n sum_j\|\|R_nj\|\|` | at `t` | amp. at `T` | amp. to `M_T` | `Y_state` | `Y_MT` | Thm-R `log10` |
|---|---|---|---|---|---|---|---|---|---|
| W1 | .3, 1, .8, .85 | 7.4e-5 | **133** | 52 | 2.8 | 0.22 | 2.0e-4 | 2.8e-8 | 15.8 |
| B54 | .5, 1, .8, .75 | 3.1e-6 | 17 | 39 | 2.9 | 0.45 | 5.2e-6 | 1.5e-9 | 6.0 |
| B75 | .5, 2, .8, .75 | 3.5e-6 | 13 | 39 | 2.9 | 0.46 | 4.6e-6 | 1.8e-9 | 6.0 |
| **B215** | .5, .5, .8, .85 | 8.8e-5 | **8.9** | 22 | 3.6 | **0.09** | 1.2e-4 | 8.5e-9 | 6.7 |
| B180 | .5, .5, .8, .85 | 5.0e-5 | 16 | 29 | 1.9 | 3.6 | 6.8e-5 | 2.8e-7 | 6.0 |
| B154 | .5, .5, .8, .85 | 3.5e-5 | 4.0 | 2.7 | 1.9 | 3.6 | 4.8e-5 | 1.7e-7 | 5.4 |
| B15 | .4, 1, .7, .75 | 7.9e-7 | 104 | 52 | 3.6 | 0.19 | 1.9e-5 | 2.7e-10 | 6.8 |
| B3 | .2, 1, .4, .75 | 1.1e-5 | 184 | 170 | 40.6 | 8.5 | 9.2e-5 | 4.7e-6 | — |

Notes.
* The amplification peaks during the excursion and is `2–4` after recovery,
  except for B3 (non-Hurwitz, weakly damped: 41).
* Initial-condition sensitivity: the response to a unit defect on cell 0 stays
  below 1 in every case, consistent with TASK-0001 D5 (singular values 0.24, 0.08).
* The functional amplification into `M_T` is attained at `t = T` and collapses
  for `t > T` (W1: `0.216, 0.005, 0.001, 0, 0` at `t/T = 1, 1.02, 1.1, 1.5, 3`).
* Max-norm amplifications are within a factor 2 of the adapted ones.

**Why the norm-based bound was so wrong.** Theorem R bounds `|e|` by
`int |psi| (a |e| + |rho|)` with `a = ||Dg - J||`; during the excursion `a ~ 1–3`
for `~50` time units and the exponential of the integrated coefficient is what
appears. The true linear response is contracting: rotations and sign changes in
`Dg` cancel, which the scalar bound cannot see.

Evidence class: NUMERICAL EXPLORATION.

---

## 2. Stage E — goal-oriented amplification

Same run. With `ell_t(e) = int_0^T Psi_J(t-s) DN(u(s)) e(s) ds` in adapted
coordinates (PL quadrature, `psi_lambda` from a 400-point arbitrary-precision
table), the dual norm `||ell_t L_h^{-1}||` is the amplification from cellwise
defects to the error of `v_T(t)`:

```
W1 :  0.22   ->  Y_MT = 2.8e-8   (threshold 0.038)
B215:  0.09  ->  Y_MT = 8.5e-9
```

The Stage-D pilot with **rigorous** cell defects gives `Y_MT = 1.9e-6` (W1) and
`3.6e-7` (B215). Either way `M_T` is insensitive to the history error at the
`1e-6` level. **This is the route: certify `M_T` through the functional, not
through a uniform state tube.**

---

## 3. Stage B — benchmark shortlist

Criteria: M1 margin, sign-aware amplification, entry margin, simplicity.

| rank | cand | rational data | sign-aware amp. | entry margin | `Y_MT` (rigorous defects) | `Z1` pilot | M1 margin at `T=1000` |
|---|---|---|---|---|---|---|---|
| 1 | **B215** | `theta=1/2, a=1/2, b=1, m=4/5, alpha=17/20, p=(277/100, 467/1000)` | 8.9 | 0.028 | 3.6e-7 | 0.27 | `M/thr = 0.19` |
| 2 | B54 | `1/2, 1, 1, 4/5, 3/4, p=(1554/1000, 3344/10000)` | 17 | 0.014 | 1.5e-9 (float) | not run | 0.37 |
| 3 | B75 | `1/2, 2, 1, 4/5, 3/4` | 13 | 0.012 | 1.8e-9 (float) | not run | 0.38 |
| — | W1 | `3/10, 1, 1, 4/5, 17/20` | 133 | 0.105 | 1.9e-6 | **0.63** | 0.36 |

W1 keeps the largest entry margin and the published-cubic provenance, but its
excursion term alone costs `Z1 ~ 0.38`. B215's rational `p` was confirmed a
witness by three solvers on two meshes in TASK-0004 (§5.3 there used B54; B215's
own float check is in `manifests/t4_certificate_*` and TASK-0002).

---

## 4. Stage D — radii pilot

Command: `python scripts/t5_stageD_radii_pilot.py --cand {W1,B215} --N 6000 --K 32`.

`B = L_h^{-1}` as a dense block inverse (forward substitution on the identity,
`||L_h B - I||_max = 9e-16`). Cell defects `Rs_j` from the TASK-0002 verifier,
rigorous, converted to the adapted norm.

| | W1 | B215 |
|---|---|---|
| rigorous defect max (`t<1` / `1<t<60` / `t>60`) | 4.9e-4 / 4.7e-5 / 1.1e-5 | 6.9e-4 / 3.2e-5 / 2.1e-6 |
| `Y = max_n sum_j \|\|R_nj\|\| Rs_j` | 1.0e-3 (at `t = 53`) | 1.2e-3 (at `t = 0.03`) |
| cellwise radius `r_n = 2(Y_n + Z2_n)`, max | 2.7e-3 | 2.5e-3 |
| `Z2(r)`, max | 1.3e-3 | 5.2e-6 |
| `Z1` budget `1 - (Y + Z2)/r` | 0.50 | 0.50 |
| `Y_MT` | 1.9e-6 | 3.6e-7 |
| `K_J` upper, `C_r` | 5.84, `1.079 + 0.707 r` | 11.41, `0.370 + 0.163 r` |

The budget of 0.5 is by construction; taking `r_n = 4(Y_n + Z2_n)` raises it to
0.75 at negligible cost in `Z2`.

---

## 5. The operator tail `Z1`, exactly and estimated

**Source formulation.** Put `e = I^alpha[f]`. The exact fixed point for the
source is `f = G(f) := g(xhat + I^alpha f) - g(xhat) - rho = K f + R(I^alpha f) - rho`,
`(Kf)(t) = A(t)(I^alpha f)(t)`. The collocation solution has `f_hat = 0`
(`rho` vanishes at the nodes). With `pi` the nodal piecewise-linear
interpolation and `B := L_h^{-1} pi + (I - pi)` on `C([0,T])`,

```
I - B (I - K)  =  L_h^{-1} pi K (I - pi)  +  (I - pi) K .                       (5.1)
```

(Verified algebraically: `L_h^{-1}(I - K_h) = I` on nodal values and
`pi K pi = K_h`.) Both terms vanish on piecewise-linear `f`.

**Obstruction in the plain sup norm.** For an arbitrary bounded `f`,
`|(I - pi)f|` can be `2|f|` on every cell and
`|I^alpha[(I-pi)f](t)| <= 2|f| t^alpha/Gamma(alpha+1) ~ 750 |f|` at `t = 1000`.
So `Z1` is not small in `C([0,T])` with the sup norm: **the radii argument has to
live in a space that controls cell oscillations** (a Hölder-type or mesh-weighted
oscillation norm). This is the exact question for ROUND-0006.

**Pilot estimate** (`python scripts/t5_stageD_Z1_pilot.py`), under the explicit
assumption `f in { |f| <= 1, osc_n(f) <= theta_n }` with `theta_n` the oscillation
profile of the computed source:

```
T1_n = sum_k ||R_nk|| ||A_k|| sum_j W_kj theta_j                 (first term of 5.1)
T2_n = ||A_n|| 2 h_n^alpha/Gamma(alpha+1) + osc_n(A) t_{n+1}^alpha/Gamma(alpha+1)   (second term)
```

| | `Z1` pilot | `T1` (excursion) | `T2` (mesh) | where |
|---|---|---|---|---|
| W1 | **0.63** | 0.38 | 0.25–0.36 | `t = 53` / `t = 1000` |
| B215 | **0.27** | 0.01 | 0.26 | `t = 1000` |

`T2` is a pure mesh term dominated by the coarse tail cells (`h = 0.5` at
`t ~ 1000`): `2 h^alpha ||A||/Gamma(alpha+1)` with `||A|| ~ |lambda| = 0.28`. Halving
the tail step to `0.1` brings it to `~0.08`. `T1` is the excursion term; for W1
it does not go away with the mesh.

**Status:** these numbers rest on an unproved assumption about the function
class. They say the budget is plausible for B215 and not for W1. They are not a
`Z1` bound.

---

## 6. Stage C — not attempted, and why

The rigorous defect (`5e-4` in the initial layer, `1e-5` after) already gives
`Y ~ 1e-3` and `Y_MT ~ 1e-6`, far inside every margin. The binding term is `Z1`,
which a higher-order `phi` does not reduce (it is set by the mesh and by the
function class, §5). If ROUND-0006 returns a setting in which `Z1` is a
higher-order interpolation remainder, degree 2–3 becomes worth it; then the
defect bound also needs a higher-order remainder (the present Lipschitz
remainder is first order in `1/K`).

---

## 7. Stage F — what would close, conditionally

For B215, if a theorem of the form V1 holds in a space where `Z1 <= 0.27` (§5) with
`B = L_h^{-1} pi + (I - pi)`, then with `r_n = 4(Y_n + Z2_n)`:

```
Y + Z1 r + Z2 <= (Y + Z2) + 0.27 * 4 (Y + Z2) = 2.08 (Y + Z2) < 4 (Y + Z2) = r ,
```

the true orbit lies within `r_n <= 5e-3` (adapted) of `xhat` on every cell, the
entry certificate holds (margin 0.028 against `||S|| r < 3e-3`), and

```
M_T <= M_T(float, PECE h=0.01) + Y_MT + (quadratic in r)  <=  0.0052 + 3.6e-7 + O(1e-5)
```

in the exact-`S` normalisation, against the B215 threshold `1/(4 K C0) ~ 0.059`.
**Every step of this chain except the V1 theorem is computed.** The chain is
conditional and is not claimed.

---

## 8. Limitations and errors

1. `Z1` is an estimate under an assumption, not a bound (§5).
2. `B`, `Y`, `Z2`, `Y_MT` are float; only the cell defects are rigorous. An
   interval version of the dense inverse is straightforward (`N = 6000`, 2x2 blocks)
   but was not built pending the theorem.
3. Stage A's `M_T` functional uses an interpolated `psi_lambda` table (400 points).
4. **Error:** the first Stage A run evaluated `psi_lambda` in arbitrary precision at
   every node for every `t` (30 000 evaluations at `|z| ~ 250`), which would have
   taken hours; killed after 33 minutes and replaced by the table.
5. `Y_MT` for B215 in the pilot printed as `0.0` at the manifest's rounding; the
   value is `3.554e-7` (log).

---

## 9. Reproduction

Hosts: ORION (all stages), local (tests). Python 3.12.3, numpy 2.5.3, mpmath 1.4.1,
python-flint 0.9.0.

```bash
cd computations && export OMP_NUM_THREADS=1
python scripts/t5_stageA_signaware.py --workers 8
python scripts/t5_stageD_radii_pilot.py --cand W1   --N 6000 --K 32 --workers 80
python scripts/t5_stageD_radii_pilot.py --cand B215 --N 6000 --K 32 --workers 80
python scripts/t5_stageD_Z1_pilot.py --cand W1
python scripts/t5_stageD_Z1_pilot.py --cand B215
pytest tests/ -q          # 103 passed, 1 skipped
```

New code: `msbg/orbit_linearized.py`; scripts `t5_*`; tests `test_orbit_linearized.py` (5).

```
branch: compute/task-0005
commit: eb53c95b38456a0ba2f0340fd8475bb5747c58d3

That commit carries every artifact cited here; the only later commit writes this SHA.
```

---

## 10. Next question for the Chief / ROUND-0006

Identity (5.1) is exact and its two terms are explicit. The single question is:

> In which norm on `C([0,T])` — Hölder-`alpha`, or a mesh-weighted oscillation
> norm `max_n osc_n(f)/theta_n` — is the radii (Newton–Kantorovich) argument
> valid with `B = L_h^{-1} pi + (I - pi)`, and what are the constants of `K` and
> of `L_h^{-1}` in that norm?

If the answer is a mesh-weighted oscillation norm, the Compute Agent can compute
every constant rigorously from the dense inverse (the Hölder amplification of
`L_h^{-1}` is `max_n sum_j ||R_{n+1,j} - R_{n,j}||/h_n^alpha`, available from `R`),
refine the tail mesh to bring `T2` below 0.1, and run the certificate for B215.
