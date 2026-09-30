#!/usr/bin/env python
"""TASK-0007 A: machine-readable inventory of every load-bearing floating-point quantity of
the B215 certificate pipeline (t6_stageBD_cap -> t6_stageD_close -> t6_stageE_m1), with its
arithmetic category BEFORE (TASK-0006, commit c9bc2f8) and AFTER the hardening.

Categories (Chief's request):
  1  Arb / interval, already rigorous
  2  binary64 algebra with a proved Higham-style roundoff bound (any order, FMA-agnostic)
  3  binary64 libm evaluation covered only by a few-ulp assumption (pow, expm1, log1p, gamma, trig)
  4  corroborative / non-load-bearing (does not enter any certified bound)
Writes computations/data/t7_arithmetic_inventory.json and prints a Markdown table."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ITEMS = [
    # ---- inputs / data ------------------------------------------------------------------
    dict(id="mesh_nodes", quantity="mesh nodes t_n, collocation values phi_n, slopes m_k", where="aposteriori.collocation, t6_make_mesh",
         role="DATA: define xhat exactly (binary64 numbers taken as exact rationals)", before=4, after=4, method="unchanged; the proof is about the exact xhat built from these floats"),
    dict(id="params", quantity="theta, a, b, m, alpha, p, S, S^-1, E*", where="validated_res.Setup",
         role="exact rationals / Arb", before=1, after=1, method="unchanged"),
    # ---- cell enclosures ---------------------------------------------------------------
    dict(id="cells", quantity="state boxes, defect sup R_n, Lipschitz drho_n, node defects rho_n", where="validated.verify_cells, cap.nodal_data",
         role="Arb point/interval enclosures of xhat, rho on cells (K=32)", before=1, after=1, method="unchanged (Arb; floats via _arb_upper_float = nearest + nextafter, re-checked)"),
    dict(id="A_nodes", quantity="A_n = S^-1 Dg(xhat(t_n)) S: float centre Am and radius Ar", where="cap._nd_node",
         role="data of L_h", before="2 (defect: radius omitted the centre's float-conversion error)", after=1, method="Ar := arb_hi(|A_n - arb(Am)|) exactly"),
    dict(id="A_cells", quantity="||A|| and osc(A) on cells", where="cap._nd_cell", role="T2 constants", before=1, after=1, method="unchanged (Arb)"),
    dict(id="hat_weights", quantity="hat-function weights W (mid, rad)", where="cap.rigorous_hat_weights", role="matrix of L_h",
         before="1/2 (rad += |mid| 2^-52 + 1e-15 slack)", after=1, method="rad := arb_hi(|w - arb(mid)|) exactly"),
    # ---- geometry tables ---------------------------------------------------------------
    dict(id="cell_weights", quantity="cell weights w_{n,j} = ((t_n-t_j)^a - (t_n-t_{j+1})^a)/G(a+1) (hi and lo)", where="cap.cell_weights -> rig.geometry_tables",
         role="Omega, kappa, rem, T1, state pad", before=3, after=1, method="Arb per entry (128 bit), outward floats; libm pow/expm1/log1p/gamma removed"),
    dict(id="dw", quantity="dw_{n,j} = w_{n,j} - w_{n+1,j}", where="cap.Geometry.dw -> rig", role="V (nodal increments)", before="3 + 4e-13 slack", after=2, method="W_hi - W_lo, one outward rounding"),
    dict(id="d_table", quantity="(t_n-t_{j+1})^{a-2} - (t_n-t_j)^{a-2}", where="cap.Geometry.d -> rig", role="Green part of P", before=3, after=1, method="Arb"),
    dict(id="rem_table", quantity="mean-kernel remainder min(2w, h_j/2 ((t_n-t_{j+1})^{a-1}-(t_n-t_j)^{a-1})/G(a))", where="cap.Geometry.rem -> rig", role="T1 (Q form)", before=3, after=1, method="Arb"),
    dict(id="HA_DTA", quantity="h_n^a/G(a+1), (t_{n+1}^a - t_n^a)/G(a+1)", where="cap.cap_vectors -> rig tables HA, DTA", role="P, V", before=3, after=1, method="Arb per cell"),
    dict(id="Ea_green", quantity="Ea_n = min(h^2 a(1-a) t_n^{a-2}/8, c_alpha h^a)/G(a+1); h^2/8 (1-a)/G(a)", where="cap.Geometry -> rig", role="P", before=3, after=1, method="Arb per cell"),
    dict(id="interp_consts", quantity="c_alpha, c_loc, c_prev(h_{n-1}/h_n)", where="cap.interpolation_constants -> rig.interpolation_constants_arb", role="P",
         before="3 (float pow on subintervals)", after=1, method="Arb ball per subinterval (tau as ball, ratio as ball over <= 64 groups); inclusion monotone"),
    dict(id="osc_xhat_prime", quantity="osc_{C_n}(xhat'), sup_{C_n}|xhat'| (cancelling sums)", where="cap.xhat_prime_oscillation -> rig._tab_row", role="EA (T2)",
         before="3 (pow/expm1/log1p) + ad-hoc n*8u rounding bound", after=1, method="exact Arb sums per cell (128 bit), outward floats"),
    dict(id="EA", quantity="(I-pi)A interpolation error (h/4)(D2p osc(xhat') + D3p diam sup|xhat'|)", where="cap.Geometry.EA", role="T2", before="2 (with 1e-13 slack)", after=2, method="infl by op count; legacy EA_green (float pow) removed from the min"),
    dict(id="D2p_D3p", quantity="D2p = ||S^-1|| ||S|| sqrt((c+a)^2+a^2+2b^2), D3p = 6||S^-1|| ||S||, D3a", where="cap.Geometry", role="EA, Z2 osc", before="2 (1e-13)", after=2, method="infl(., ops); sqrt correctly rounded (IEEE)"),
    dict(id="D2_cells", quantity="per-cell Lipschitz constant of x -> A(x) (adapted)", where="cap.lipschitz_A_cells -> rig.lipschitz_A_cells_arb", role="Z2",
         before="3 (cos/sin sampling, S centre + 1e-9 slack)", after=1, method="Arb: convexity in c + closed-form 2x2 Gram eigenvalue, no sampling"),
    # ---- inverse -----------------------------------------------------------------------
    dict(id="float_inverse", quantity="float inverse Rt (forward substitution)", where="cap.rigorous_inverse", role="approximate inverse (any float matrix is admissible)", before=4, after=4, method="unchanged"),
    dict(id="residual", quantity="|E| = |I - L_h Rt| entrywise: float residual + gamma_K|A||W||Rt| + gamma_2|A||fl(WR)| + Ar|W||Rt| + (|A|+Ar)Wr|Rt| + final +/- roundings", where="cap.rigorous_inverse",
         role="Neumann invertibility, delta_n", before="2 (error terms themselves un-inflated; final +/- rounding omitted)", after=2,
         method="every error term computed in floats and inflated by rig.infl with its own reduction length; final +/- term added"),
    dict(id="normE_delta", quantity="||E||_inf, c_r = ||(|Rt||E|)_r||_1/(1-||E||), delta_n", where="cap.rigorous_inverse", role="inverse correction", before="2 (1e-13 slack on length-m sums: NOT a valid gamma_m bound for m = 24002)", after=2, method="infl(., m)"),
    dict(id="block_norms", quantity="Rn = Frobenius block norms + delta", where="cap.rigorous_inverse", role="T1, Y, Z2 (sup)", before="2 (1e-13)", after=2, method="infl by op count (4 squares, sqrt, +)"),
    dict(id="osc_blocks", quantity="Dn (direct) and Sn (Abel cumulative) oscillation blocks", where="cap.rigorous_inverse", role="T1, Y, Z2 (osc)",
         before="2 (Abel cumsum rounding NOT bounded; 1e-13 slack)", after=2, method="cumsum error gamma_K sum|Dd| added as an entrywise error matrix; infl by length"),
    dict(id="Q_blocks", quantity="Q = L_h^-1 A W_c mean-kernel blocks Qn, DQn", where="cap.mean_kernel_blocks", role="T1 (sharp form)",
         before="2 (2e-13 + 1e-12 slacks; W data radius not included)", after=2, method="gamma_m|Rt||M| + |Rt| dM (dM = Ar W_hi + (|A|+Ar)(W_hi-W_lo) + u|M|) + delta max|M|; infl by length"),
    # ---- bound operator ----------------------------------------------------------------
    dict(id="B_source", quantity="B s bounds: Rn@sigma, Dn@sigma, Slow@dnode, + products", where="cap._B_source_vectors, cap._osc_pl", role="Y, T1, Z2", before="2 (1e-13 slack on length-N1 dots: invalid for N1 = 12001)", after=2, method="infl(., N1)"),
    dict(id="state_sup", quantity="Omega_n = sum_{j<n} w_{n,j} omega_j + w_{n+1,n} omega_n", where="cap.state_sup", role="T2, Z2, state pad", before="2 (1e-13 slack)", after=2, method="infl(., N)"),
    dict(id="cap_loop", quantity="G, loc, green, P, V per cell (dots of length n)", where="cap.cap_vectors", role="T2", before="2/3 (1e-13 slack; h^a, t^a via float pow)", after="2 (+ Arb tables)", method="cum_hi/cum_lo with infl/defl(N); dots infl(., n); powers from HA/DTA tables"),
    dict(id="T1_kappa", quantity="kappa = ||A_n|| sum_j w_{n,j} beta_j, dkappa, Rk, Dk (Q form)", where="cap.cap_vectors", role="T1", before="2 (1e-13)", after=2, method="infl by length"),
    dict(id="Z2", quantity="sig_node, sig_cell, tau_cell of Delta_A I^a h", where="cap.z2_vectors", role="Z2", before="2 (1e-13)", after=2, method="infl by op count"),
    dict(id="F_apply", quantity="F(b) = Y + T1 + T2 + Z2 componentwise; F(b) < b test; kappa = max (M q + Z2'(b))/q", where="cap._apply, check_certificate, contraction_constant",
         role="the two Banach inequalities", before="2 (1e-13 on 3-4 term sums: valid)", after=2, method="infl(., #terms); division x/q rounds to nearest: max ratio compared against 1 with the exact-division margin absorbed by strictness slack (min slack 6e-4 >> u)"),
    dict(id="power_iteration", quantity="Perron weights q, rho(M) brackets", where="cap.power_iteration", role="choice of weights only (any positive weights give a valid norm)", before=4, after=4, method="unchanged"),
    # ---- Stage E -----------------------------------------------------------------------
    dict(id="pad", quantity="physical pad ||S|| Omega_n", where="t6_stageE_m1", role="entry certificate, N sup", before="2/3 (recomputed with float cell_weights, 1e-13)", after=2, method="Omega from the certificate file (Arb weights), infl(., 1); boxes widened with outward nextafter"),
    dict(id="entry_test", quantity="x_hi + pad < theta, x_lo - pad > 0, y_lo - pad > 0; eta", where="t6_stageE_m1", role="Stage 0", before="2 (float +/- without outward rounding)", after=2, method="outward nextafter on every +/-, theta as arb_lo of the exact rational"),
    dict(id="Nsup", quantity="sup |N(u)|_S on padded boxes", where="validated_res.nonlinearity_sup", role="M_T history terms", before=1, after=1, method="unchanged (Arb)"),
    dict(id="K_J", quantity="K_J = (sum_i env_i w_i + tail)/a", where="validated_res.kernel_integrator", role="M1",
         before="2/3 (rho0 via float pow; cumsum of ~10^4 cells with 1e-13 slack: NOT a valid gamma_n bound; 1/a float)", after="1/2", method="rho0, 1/a in Arb; cumulative sums infl(., i) per entry; tail Arb"),
    dict(id="M_T", quantity="M_T = |p-E*| phi_b(T) + far history (dot of length ~N) + near history", where="validated_res.memory_tail_bound", role="M1",
         before="2 (1e-13/1e-12 slack on a length-N dot: marginal)", after=2, method="infl(., len)"),
    dict(id="C_r", quantity="C0, c3 (adapted nonlinearity constants)", where="validated_res.adapted_C", role="M1", before=1, after=1, method="unchanged (Arb over arcs)"),
    dict(id="m1_margin", quantity="r - K_J C_r r^2 - M_T, K_J C_r r", where="validated_res.m1_radius", role="M1 verdict", before=1, after=1, method="unchanged (Arb)"),
    # ---- corroboration -----------------------------------------------------------------
    dict(id="crosscheck", quantity="independent collocation vs xhat; power-iteration diagnostics; mesh generator", where="t6_summary, t6_make_mesh", role="corroboration", before=4, after=4, method="unchanged"),
]


def main():
    out = {"task": "TASK-0007", "categories": {"1": "Arb/interval rigorous", "2": "binary64 algebra with proved Higham bound (any order, FMA-agnostic)",
                                                "3": "binary64 libm few-ulp assumption", "4": "corroborative / non-load-bearing"},
           "items": ITEMS}
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    path = os.path.join(ROOT, "data", "t7_arithmetic_inventory.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"| id | quantity | where | before | after | method |\n|---|---|---|---|---|---|")
    for it in ITEMS:
        print(f"| `{it['id']}` | {it['quantity']} | `{it['where']}` | {it['before']} | {it['after']} | {it['method']} |")
    n3 = sum(1 for it in ITEMS if str(it["after"]).startswith("3"))
    print(f"\ncategory-3 items after hardening: {n3}; written {path}")


if __name__ == "__main__":
    main()
