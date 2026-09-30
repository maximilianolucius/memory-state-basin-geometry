# TASK-0004 — Memory-tail survival feasibility and certification — COMPUTE RETURN

**From:** Compute Agent
**To:** Chief Researcher
**Task:** `research/coordination/chief-to-compute/TASK-0004_memory-tail-survival_REQUEST.md`
**Date:** 2026-09-29
**Branch:** `compute/task-0004`
**Final commit SHA:** see §10

---

## 0. Executive answer

**Survival of W1 is NOT certified. TARGET-A20 is not closed.**

| Stage | Verdict |
|---|---|
| A — feasibility of M1 for W1 | **Feasible numerically** from `T = 500` (adapted norm). Not feasible for `T <= 200`. |
| B — resolvent identity | Holds at mesh order for PECE (`2.1e-4 -> 3.2e-5`). One column of the check was invalid (my error, §3). |
| C — rigorous finite history to the cut time | **NOT ACHIEVED.** Infeasible for W1 by any version of the verifier; infeasible for the best alternative witness by about 8 orders of magnitude. |
| D — rigorous kernel and constants | **CERTIFIED (conditional):** `K_J <= 5.8035`, `C_r <= 1.0781 + 0.7068 r`, threshold `M_T < 0.0381`. |
| E — certificate | **UNDECIDED.** No rigorous `M_T` exists because Stage C failed. |

The M1 inequality is numerically satisfied with a factor 2.8 to spare at
`T = 1000`. What is missing is not the inequality; it is a rigorous enclosure of
the orbit across the excursion. §5 quantifies that obstruction.

Everything that depends on M1 is **CONDITIONAL** (ROUND-0005 pending).

---

## 1. A point about `h_T` that affects how the numbers should be read

`h_T(t)` does not tend to zero. By the TASK-0002 Stage-C estimate, for fixed `T`
`h_T(t) -> p - E*` as `t -> infinity`. Measured: `sup_t |h_T|_inf = 0.99, 0.93, 0.81,
0.65, 0.50, 0.34` for `T = 50, ..., 2000`. The small object is the linear response
`v_T`, not the input. M1 is stated correctly in terms of `v_T`.

A closed form used below follows from linearity. For `t >= T`,

```
v_T(t) = E_alpha(J t^alpha)(p - E*) + int_0^T Psi_J(t - s) N(u(s)) ds .           (1.1)
```

(`v_T`, extended by `u` on `[0,T]`, solves the linear Volterra equation from time
`0` with source `N(u)` truncated at `T`.) This is what makes a rigorous bound of
`M_T` possible in principle: it needs `N(u(s))` on `[0,T]` and two scalar
Mittag-Leffler bounds, and no information about `t > T`.

---

## 2. Stage A — numerical feasibility for W1

Command: `python scripts/t4_stageAB_feasibility.py --workers 80` (ORION).
Orbit to `T_end = 6000`, PECE `h = 0.01` as reference. `M_T` is a supremum over the
finite window `[T, 6000]`.

### 2.1 Kernel constant in three norms

| norm | `K_J` (numerical) | exact lower bound |
|---|---|---|
| Euclidean | 13.106 | `\|\|J^{-1}\|\|_2 = 10.447` |
| weighted max, best weight ratio 0.397 | 9.306 | — |
| **adapted**, `\|u\|_S = \|S^{-1}u\|_2` | **5.795** | `1/\|lambda\| = 3.536` |

In the adapted norm `||Psi_J(s)|| = |psi_lambda(s)|` exactly, so `K_J` is a scalar
integral. The kernel matches its asymptote
`|lambda|^{-2} s^{-alpha-1}/|Gamma(-alpha)|` to 0.5% at `s = 3000`.

### 2.2 The M1 inequality

`f(r) = M_T + K_J C_r r^2 - r`, minimised over `r`; feasible iff `min f < 0`.

| T | `\|u(T)\|_inf` | norm | `M_T` | `min f` | feasible |
|---|---|---|---|---|---|
| 50 | 2.94e-1 | adapted | 4.74e-1 | +4.4e-1 | no |
| 100 | 5.21e-2 | adapted | 7.46e-2 | +4.2e-2 | no |
| 200 | 3.12e-2 | adapted | 4.42e-2 | +1.2e-2 | no |
| 500 | 1.50e-2 | Euclidean | 1.66e-2 | +2.7e-3 | no |
| 500 | 1.50e-2 | weighted max | 1.58e-2 | −1.8e-3 | **yes** |
| 500 | 1.50e-2 | adapted | 2.09e-2 | −1.1e-2 | **yes** |
| 1000 | 8.46e-3 | Euclidean | 9.31e-3 | −4.6e-3 | **yes** |
| 1000 | 8.46e-3 | adapted | 1.17e-2 | −2.1e-2 | **yes** |
| 2000 | 4.75e-3 | adapted | 6.53e-3 | −2.6e-2 | **yes** |

Spread of `M_T` over the three PECE runs: at most `1.4e-4` for `T >= 100`.
(The adapted-norm values in this table use numpy's unit eigenvector; in the
normalisation of §6 they are larger by `1/0.8485`, and so is the threshold. The
inequality is scale invariant.)

The norm matters: the adapted norm is feasible a factor 2 earlier in `T` than the
Euclidean one.

Evidence class: NUMERICAL EXPLORATION.

---

## 3. Stage B — the resolvent identity

`z := v_T + Psi_J * N(u)` was computed without forming `Psi_J`, as the solution of
`z = h_T + I_T^alpha[J z + N(u)]`, and compared with the full-history orbit.

| T | PECE `h=0.02`, `H=0.2` | PECE `h=0.02`, `H=0.1` | PECE `h=0.01`, `H=0.1` |
|---|---|---|---|
| 50 | 4.26e-4 | 4.26e-4 | 2.11e-4 |
| 500 | 1.61e-4 | 1.58e-4 | 4.44e-5 |
| 2000 | 1.21e-4 | 1.20e-4 | 3.22e-5 |

The defect is governed by the orbit step `h` and falls by 3.6–3.7 when `h` is
halved.

**Invalid column, reported.** The same check on the rectangle-rule orbit gave
defects of `3.6e-2 ... 6.2e-2`. That number is meaningless: I integrated the nodes
of a rectangle solver with a piecewise-linear quadrature. It is the same mistake
I made and fixed in TASK-0002 Stage C, repeated here. It says nothing about the
identity and is excluded.

Evidence class: NUMERICAL CORROBORATION (PECE only).

---

## 4. Theorem R — a resolvent form of the a posteriori bound

Needed for Stage C. Notation as in the TASK-0002 return §2; norm `|.|_S`.

`xhat = p + I^alpha[phi]`, `rho = phi - g(xhat)`, `e = x - xhat`. Then

```
e = I^alpha[ J e + q - rho ],     q(s) := g(x(s)) - g(xhat(s)) - J e(s),
```

and by variation of constants for the linear Volterra equation,
`e = Psi_J * (q - rho)`. By the mean value inequality
`|q(s)|_S <= a(s)|e(s)|_S` with
`a(s) >= sup { ||S^{-1}(Dg(xi) - J)S||_2 : |xi - xhat(s)|_S <= r }`.

With `W_{n,j} >= sup_{t in C_n} int_{C_j}|psi(t-s)|ds`, `w_n >= int_0^{h_n}|psi|`,
`D_n = sum_{j<n} W_{n,j} Rs_j + w_n Rs_n`,
`U_n = (D_n + sum_{j<n} W_{n,j} a_j U_j)/(1 - w_n a_n)`:
if every `w_n a_n < 1` and `max U_n < r`, the solution exists on `[0,T]` and
`sup_{C_n}|x - xhat|_S <= U_n`.

*Proof.* Identical to TASK-0002 §2.2 with the kernel `(t-s)^{alpha-1}/Gamma(alpha)`
replaced by `|psi_lambda(t-s)|`: a priori assumption `|e| <= r` on `[0,tau]`,
cellwise supremum, induction on `n`, continuity bootstrap, continuation. `QED`

Status: THEOREM/analytic, **conditional** on the variation-of-constants identity
(ROUND-0005). Implemented in `msbg/validated_res.py`.

**Why it is better than the TASK-0002 form, and by how much.** The coefficient
`a(s)` vanishes at `E*`, so after recovery the recursion is a contraction and the
bound stops growing; the TASK-0002 form uses `||Dg||`, which is about 1 at `E*`.

| T | log10 amplification, TASK-0002 form | log10, resolvent form (max norm) |
|---|---|---|
| 4 | 4.4 | 4.7 |
| 36 | 12.6 | 21.1 |
| 100 | 34.6 | 32.6 |
| 1000 | **417** | 32.9 |

The TASK-0002 verifier cannot reach any useful cut time.

---

## 5. Stage C — the obstruction, quantified

### 5.1 The amplification peaks during the excursion

Float profile of the resolvent amplification `w(t)` (adapted 2-norm):

| t | W1 `log10 w` | B215 `log10 w` |
|---|---|---|
| 5 | 8.5 | 4.5 |
| 20 | 11.7 | 6.5 |
| 40 | 14.2 | 6.7 |
| **sup** | **15.8** at `t = 56.5` | **6.7** at `t = 50.2` |
| 300 | 12.6 | 3.6 |
| 1000 | 11.3 | 2.4 |

The bootstrap needs `max U < r` over all cells, so the requirement is set by the
supremum.

**W1 is out of reach.** Supremum `10^15.8`; with a tube radius of `1e-3` the
defect would have to be below `1e-19`.

### 5.2 A metric error of mine, and its consequence

My first witness scan ranked candidates by `w(T)` at `T = 300, 600, 1000` instead
of `sup_{t<=T} w(t)`. It reported B215 at `10^3.4`; the supremum is `10^6.7`. I
selected B215, built the end-to-end driver and only then found the gap. The scan
was redone with the supremum:

| entry margin at least | M1-feasible witnesses | min `sup log10 w` |
|---|---|---|
| 0 | 115 | 5.43 |
| 0.01 | 55 | 5.98 |
| 0.02 | 24 | 6.53 |

Over all 115 M1-feasible witnesses: min 5.43, median 9.53, max 21.28. **No
witness has an amplification below `10^5.4`.**

### 5.3 One real attempt, measured

Witness B54 with exact rational inputs:
`theta = 1/2, a = b = 1, m = 4/5, alpha = 3/4, p = (1554/1000, 3344/10000)`,
`E* = (4/5, 3/50)`, `lambda = -1/25 + i sqrt(29)/25`. Float check: all three
solvers on two meshes agree that it enters `R_ext` (margin 0.0143) and converges
(`x(1000) = (0.79300, 0.06208)`).

`python scripts/t4_stageE_certificate.py ... --T 1000 --N 24000 --K 32` (ORION, 165 workers):
cell defects 265 s, recursion 92 s; max-norm defect `2.56e-7`, adapted-norm
defect `1.75e-6`, `K_up = 8.7998`, `max D = 2.58e-6`.

Rigorous recursion against the tube radius (`python scripts/t4_tube_sweep.py`):

| tube radius `r` | `a` at `T` | `K a` at `T` | `max U` | `max U / max D` | at `t =` | bootstrap |
|---|---|---|---|---|---|---|
| 2e-2 | 0.1893 | **1.666** | 1.1e56 | 4.2e61 | 999.9 | fails |
| 5e-3 | 0.0587 | 0.517 | 2.0e6 | 7.6e11 | 202.5 | fails |
| 2e-3 | 0.0330 | 0.290 | 5.9e4 | 2.3e10 | 109.4 | fails |
| 1e-3 | 0.0245 | 0.216 | 3.4e4 | 1.3e10 | 47.0 | fails |
| 1e-4 | 0.0171 | 0.151 | 2.4e4 | 9.3e9 | 46.6 | fails |
| 1e-5 | 0.0164 | 0.144 | 2.3e4 | 9.0e9 | 46.5 | fails |

Two separate mechanisms:

* **The tube cannot be large.** `a` on the tube is bounded below by (second
  derivative) x (tube radius). At `r = 2e-2`, `K a = 1.67 > 1` after recovery and
  the bound grows exponentially over the remaining horizon. This is a constraint
  on any verifier of this type: `r` must satisfy `K_J a_tail(r) < 1`.
* **With a small tube the bound is `2.4e4` and the requirement is `< 1e-4`.**
  The gap is 8 orders of magnitude.

The rigorous amplification is `9e9`. The float estimate in the exact 2-norm was
`1e6`. The factor `1e4` between them is the cost of rigor as implemented:
Frobenius instead of spectral norm, `sqrt(2)||S^{-1}||` to convert the max-norm
defect, the widening of kernel windows, and the tube. These enter an exponent.

### 5.4 What would be needed

With a piecewise-linear `phi` the defect is second order: `max D` falls by 4 when
`N` doubles. Closing 8 orders needs `N` larger by `1e4`, and the Arb cell work is
`O(N^2 K)`. Not feasible.

What could work, in decreasing order of expected gain:

1. **A higher-order `phi`.** Piecewise polynomials of degree `d` give defects of
   order `h^{d+1}`; `I^alpha` of a piecewise polynomial is still a closed form.
   The defect bound then needs a higher-order remainder as well: the present
   Lipschitz remainder `(h/2K) sup|rho'|` is first order in `1/K`.
2. **Sharper norms inside the exponent:** spectral norm by interval eigenvalue
   enclosure instead of Frobenius; defect measured directly in `|.|_S`.
3. **A sign-aware resolvent for the excursion.** The true sensitivity
   `d x(t)/d p` is below 1 (TASK-0001 D5: singular values 0.24, 0.08); the
   `10^6` comes from bounding `|Dg - J|` without sign while the orbit is far from
   `E*`. Linearising around the orbit removes it, at the price of a resolvent
   that is no longer a scalar Mittag-Leffler function.

Evidence class of §5: CERTIFIED for the bounds in the table of §5.3 (each row's
verdict is UNDECIDED); NUMERICAL EXPLORATION for §5.1 and §5.2.

---

## 6. Stage D — rigorous constants for W1

Command: `python scripts/t4_stageD_rigorous_constants.py --workers 12` (AUREUS).

Exact data: `lambda = (-3 + i sqrt 41)/25`,
`S = [[-4/5, 0], [3/25, -sqrt(41)/25]]`, `J S = S [[mu,-nu],[nu,mu]]`.

### 6.1 The kernel

With `rho = s^alpha`, `K_J = (1/alpha) int_0^inf |E_{alpha,alpha}(lambda rho)| d rho`.

* On `[0, rho_0]`: about 30 000 cells; on each,
  `|E| <= |E(midpoint)| + Lip * width/2`, the midpoint value from the Taylor
  series in Arb with a proved tail bound, `Lip` from a positive series (small
  argument) or from the representation below (large argument).
* On `[rho_0, inf)`: closed forms from the representation.

**Representation used.** For `alpha pi/2 < |arg z| < alpha pi`,

```
E_{a,a}(z) = (1/a) z^{(1-a)/a} exp(z^{1/a})
           + (sin(a pi)/pi) int_0^inf e^{-r} r^a / ((r^a e^{i a pi} - z)(r^a e^{-i a pi} - z)) dr,
```

giving `|I(z)| <= B/|z|^2`, `B = sin(a pi) Gamma(a+1)/(pi sin Delta)`,
`Delta = a pi - |arg z|`. Checked numerically against the Taylor series at four
arguments: agreement `1e-26 ... 3e-30`; measured `|I||z|^2 <= 0.149`, bound
`B = 0.2225`. **This is a numerical check, not a proof**; ROUND-0005 should audit it.

| `rho_0` | cells | finite part | tail | **`K_J` upper** |
|---|---|---|---|---|
| 200 | 29 958 | 5.790164 | 0.016358 | 5.806522 |
| 400 | 30 305 | 5.795290 | 0.008179 | **5.803469** |

Float value 5.7946. Cell bounds overestimate by a factor 1.0000–1.0042.

### 6.2 Nonlinearity and threshold

`|N(u)|_S <= (C0 + c3 r)|u|_S^2` with `C0 <= 1.078088`, `c3 <= 0.706762`
(20 000 arcs, Arb).

```
M_star := max_r [ r - K_up (C0 + c3 r) r^2 ]  >=  0.038078   at  r = 745/10000,
K_up C_r r <= 0.4889  ( < 1 ).
```

**Conditional statement.** If M1 holds and a rigorous bound `M_T < 0.038078` in
`|.|_S` is supplied for some cut time `T`, then survival of W1 follows.

Float values in this normalisation: `M_T = 0.0247` (`T = 500`), `0.0138`
(`T = 1000`), `0.0077` (`T = 2000`). All below the threshold; none is rigorous.

Evidence class: CERTIFIED COMPUTATION, conditional on the representation.

---

## 7. Certified / not certified

| claim | class |
|---|---|
| `K_J <= 5.803469` for W1, adapted norm | CERTIFIED, conditional on the ML representation |
| `C_r <= 1.078088 + 0.706762 r`; threshold `M_T < 0.038078` | CERTIFIED, same condition |
| Identity (1.1) for `v_T` | THEOREM/analytic, conditional on variation of constants |
| Theorem R | THEOREM/analytic, same condition |
| M1 inequality for W1 at `T >= 500` | NUMERICAL EXPLORATION |
| Resolvent identity at mesh order (PECE) | NUMERICAL CORROBORATION |
| Rigorous bounds `U_n` for B54 (§5.3) | CERTIFIED; verdict UNDECIDED in every row |
| Rigorous `M_T` for any witness | **NOT OBTAINED** |
| Survival of W1 or of any witness | **NOT CERTIFIED** |
| TARGET-A20 | **OPEN** |

---

## 8. Errors made in this task

1. **Wrong ranking metric in the witness scan** (§5.2): amplification at `T`
   instead of its supremum. Cost: a wrong candidate choice and one wasted
   end-to-end run.
2. **`K_J` "bound" of `1e33`** in the first version of `msbg/kernel_bound.py`:
   128-bit enclosures of `alpha` and `lambda` reused inside a series that cancels
   hundreds of bits. Ball arithmetic was correct; the design was not. Constants
   are now rebuilt from exact rationals at each working precision; regression
   test `test_constants_are_rebuilt_at_working_precision`.
3. **Silent NaN** from square roots of balls containing zero, in the coefficient
   `a_n` near `E*`. Norms are now taken from magnitudes.
4. **Quadrature mismatch in Stage B** for the rectangle solver (§3), a repeat of
   a TASK-0002 error.
5. **`numpy.trapz`** does not exist in numpy 2.5 on the compute hosts; the first
   Stage A run crashed after the kernel computation.

---

## 9. Limitations

1. `M_T` in Stage A is a supremum over `[T, 6000]`, not over `[T, inf)`.
2. Stage A uses the binary64 images of the W1 parameters; Stage D and §5.3 use
   exact rationals.
3. The Mittag-Leffler representation and the variation-of-constants identity are
   used, not proved here.
4. §5.4 is an assessment, not a result. Item 1 has not been tried.
5. Arb/python-flint are trusted.

---

## 10. Reproduction

Hosts: ORION (Stage A/B, witness scan, B54 attempt, tube sweep), AUREUS `aur007`
(Stage D, amplification studies), local (tests). Python 3.12.3, numpy 2.5.3,
mpmath 1.4.1, python-flint 0.9.0 on the remote hosts.

```bash
cd computations && export OMP_NUM_THREADS=1
python scripts/t4_stageAB_feasibility.py --workers 80
python scripts/t4_stageC_amplification.py
python scripts/t4_amplification_profile.py
python scripts/t4_witness_amplification_scan.py
python scripts/t4_stageD_rigorous_constants.py --workers 12
python scripts/t4_stageE_certificate.py --theta 1/2 --a 1 --b 1 --m 4/5 --alpha 3/4 \
       --p 1554/1000 3344/10000 --T 1000 --N 24000 --K 32 --r 0.02 --float-check --tag B54
python scripts/t4_tube_sweep.py
pytest tests/ -q          # 98 passed, 1 skipped
```

New code: `msbg/memory_tail.py`, `msbg/kernel_bound.py`, `msbg/validated_res.py`;
scripts `t4_*`; tests `test_memory_tail.py` (12).

```
branch: compute/task-0004
commit: FINAL_SHA
```

---

## 11. Next question for the Chief

M1 is numerically comfortable and its constants are certified. The project is
now blocked by one computational problem: a rigorous enclosure of an orbit
across its excursion, to a relative accuracy that beats an amplification of at
least `10^6`.

Two decisions are the Chief's:

1. **Is a higher-order validated integrator worth a task of its own?** It is the
   only route identified here that stays inside the current proof architecture
   (E1 + X1 + M1). It is a substantial piece of rigorous numerics and its success
   is not guaranteed; §5.4 item 3 may be needed as well.
2. **Or should the survival side be attacked analytically?** The obstruction is
   entirely in the excursion. A theorem that bounds the orbit from below during
   the excursion by comparison — the mirror image of X1 — would remove the need
   to enclose it. The Compute Agent can test candidate comparison functions
   numerically against the 237 witnesses on request.
