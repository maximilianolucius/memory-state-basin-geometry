#!/usr/bin/env python
"""TASK-0006 Stages B-D: rigorous oscillation-Banach radii constants for B215.

Pipeline (everything after the collocation is a rigorous upper bound):
  collocation (float) -> verify_cells (Arb cell boxes, defect sup/Lipschitz)
  -> rigorous hat weights (Arb) -> nodal rho, A_n (Arb) -> certified dense inverse
  -> theta-norm weights by fixed-point optimisation -> Y0, Z1, Z2, radii polynomial.

Usage: t6_stageBD_cap.py --T 1000 --N 6000 --mesh graded3|tail_h:<h>|uniform ...
"""
import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.aposteriori import collocation, graded_mesh                      # noqa: E402
from msbg.cap import (Geometry, cap_constants, cap_vectors, iterate_bounds,   # noqa: E402
                      lipschitz_A, nodal_data, power_iteration, rigorous_hat_weights,
                      rigorous_inverse, up)
from msbg.models import AlleePredatorPrey                                  # noqa: E402
from msbg.provenance import RunRecorder                                    # noqa: E402
from msbg.validated import verify_cells                                    # noqa: E402
from msbg.validated_res import Setup                                       # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make_mesh(kind, T, N):
    if kind == "graded3":
        return graded_mesh(T, N, 3.0)
    if kind == "uniform":
        return np.linspace(0.0, T, N + 1)
    if kind.startswith("hybrid:"):
        # graded r=3 on [0, T1] with N1 nodes, then uniform step to T
        _, T1, N1 = kind.split(":")
        T1, N1 = float(T1), int(N1)
        head = graded_mesh(T1, N1, 3.0)
        n_tail = N - N1
        tail = np.linspace(T1, T, n_tail + 1)[1:]
        return np.concatenate([head, tail])
    if kind.startswith("tri:"):
        # graded r=3 on [0, T1] (N1 cells), geometric-ish graded r=2 on [T1, T2] (N2 cells),
        # uniform on [T2, T] with the remaining cells
        _, T1, N1, T2, N2 = kind.split(":")
        T1, N1, T2, N2 = float(T1), int(N1), float(T2), int(N2)
        head = graded_mesh(T1, N1, 3.0)
        mid = T1 + (T2 - T1) * (np.arange(N2 + 1) / N2) ** 2
        tail = np.linspace(T2, T, N - N1 - N2 + 1)
        return np.concatenate([head, mid[1:], tail[1:]])
    raise ValueError(kind)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, default=1000.0)
    ap.add_argument("--N", type=int, default=6000)
    ap.add_argument("--mesh", default="graded3")
    ap.add_argument("--K", type=int, default=32)
    ap.add_argument("--workers", type=int, default=80)
    ap.add_argument("--iters", type=int, default=300)
    ap.add_argument("--tube", type=float, default=1e-2, help="initial physical tube radius for D2")
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    np.seterr(all="ignore")
    t0 = time.time()

    def log(*a):
        print(f"[{time.time() - t0:8.1f}s]", *a, flush=True)

    st = Setup("1/2", "1/2", "1", "4/5", "17/20", ("277/100", "467/1000"))
    fl, pf = st.floats()
    al = fl["alpha"]
    model = AlleePredatorPrey(theta=fl["theta"], a=fl["a"], b=fl["b"], m=fl["m"])
    tag = args.tag or f"{args.mesh.replace(':', '_')}_T{int(args.T)}_N{args.N}"
    rec = RunRecorder(f"t6_stageBD_{tag}", ROOT)
    rec.add("args", vars(args))

    tm = make_mesh(args.mesh, args.T, args.N)
    N = len(tm) - 1
    h = np.diff(tm)
    log(f"mesh {args.mesh}: N={N}, h_min={h.min():.3g}, h_max={h.max():.3g}, T={tm[-1]}")
    X, PHI, M = collocation(model, np.array(pf), al, tm)
    log("collocation done")

    strs = dict(theta=st.str["theta"], a=st.str["a"], b=st.str["b"], m=st.str["m"],
                alpha=st.str["alpha"], p=st.str["p"])
    cells = verify_cells(tm, PHI, strs["theta"], strs["a"], strs["b"], strs["m"], strs["alpha"],
                         strs["p"], 0.0, prec=128, workers=args.workers, K=args.K)
    log(f"cells: R_max={cells.R.max():.3e} drho_max={cells.drho.max():.3e} "
        f"x in [{cells.x_lo.min():.4f},{cells.x_hi.max():.4f}]")

    Wm, Wr = rigorous_hat_weights(tm, strs["alpha"], workers=args.workers)
    log(f"hat weights: max rad {Wr.max():.2e}, row-sum max {np.abs(Wm).sum(1).max():.4g}")

    rho, Am, Ar, normA, oscA = nodal_data(tm, PHI, strs, cells.x_lo, cells.x_hi, cells.y_lo,
                                          cells.y_hi, workers=args.workers)
    log(f"nodal data: rho_node max {rho.max():.3e}, ||A|| max {normA.max():.4g}, "
        f"osc A max {oscA.max():.3e}, A rad max {Ar.max():.2e}")

    Rn, Dn, normE, delta, R4 = rigorous_inverse(Wm, Wr, Am, Ar)
    amp_row = Rn.sum(1)
    log(f"inverse: ||E||_inf={normE:.3e}, delta max {delta.max():.3e}, "
        f"row-sum max {amp_row.max():.4g} at t={tm[int(np.argmax(amp_row))]:.2f}, at T {amp_row[-1]:.4g}")
    rec.add("inverse", dict(normE=normE, delta_max=float(delta.max()),
                           rowsum_max=float(amp_row.max()), rowsum_T=float(amp_row[-1])))
    del R4

    nSi2 = float(up(float(st.normSi) * np.sqrt(2.0)))
    # Lipschitz constant of A on the tube |e|_S <= rmax * Omega_max: Omega_max <= T^a/Gamma(a+1)
    from math import gamma
    tube_phys = args.tube
    D2 = lipschitz_A(st, cells.x_lo, cells.x_hi, cells.y_lo, cells.y_hi, tube_phys)
    log(f"D2 (Lipschitz of A on tube, phys radius {tube_phys:.3g}) = {D2:.4g}")

    xbox = dict(theta=fl["theta"], a=fl["a"], b=fl["b"], x_lo=float(cells.x_lo.min()),
                x_hi=float(cells.x_hi.max()))
    diam = up(np.sqrt((cells.x_hi - cells.x_lo) ** 2 + (cells.y_hi - cells.y_lo) ** 2))
    geo = Geometry(tm, al, PHI, float(st.normS), float(st.normSi), xbox, diam)
    log(f"geometry: c_alpha={geo.c_alpha:.4f} c_loc={geo.c_loc:.4f} c_prev in "
        f"[{geo.c_prev.min():.4f},{geo.c_prev.max():.4f}] D2p={geo.D2p:.3g} "
        f"EA max(n>=1) {np.nanmax(geo.EA[1:]):.3e} (green {np.max(geo.EA_green[1:]):.3e}) O1 max {np.max(geo.O1[1:]):.3e}")
    rec.add("geometry", dict(c_alpha=geo.c_alpha, c_loc=geo.c_loc, c_prev_max=float(geo.c_prev.max()),
                             D2p=float(geo.D2p), EA_max=float(np.max(geo.EA[1:]))))
    results = {}
    # ---- spectral radius of the linear part (power iteration) -----------------------------
    log("--- power iteration on the linear bound operator M")
    om_p, th_p, phist, vp = power_iteration(geo, Rn, Dn, cells.R, cells.drho, normA, oscA, nSi2,
                                            iters=60, log=log)
    rhoM = phist[-1]
    results["spectral_radius"] = dict(cw_lower=rhoM["cw_lower"], cw_upper=rhoM["cw_upper"], n_iter=len(phist))
    rec.save_json("power_history", phist)
    rec.save_npz("power_weights", omega=om_p, theta=th_p, tm=tm, T1sup=vp["T1sup"], T2sup=vp["T2sup"],
                 T1osc=vp["T1osc"], T2osc=vp["T2osc"], S1=vp["_S1"], S2=vp["_S2"], S3=vp["_S3"])
    for key, den in (("T1sup", om_p), ("T2sup", om_p), ("T1osc", th_p), ("T2osc", th_p)):
        r_ = vp[key] / den
        i = int(np.argmax(r_))
        log(f"   [power weights] {key}/b: max {r_[i]:.4f} at cell {i} (t={tm[i]:.3f}, h={h[i]:.3g})")
        results[f"power_ratio_{key}"] = dict(max=float(r_[i]), cell=i, t=float(tm[i]))
    for nm, arr in (("normA*P", vp["_S1"]), ("EA*Omega", vp["_S2"]), ("2oscA*V", vp["_S3"])):
        r_ = 2 * arr / th_p
        log(f"   [power weights] 2*{nm}/theta: max {r_.max():.4f} at t={tm[int(np.argmax(r_))]:.3f}")
        results[f"power_T2osc_part_{nm}"] = float(r_.max())
    # ---- cell-wise monotone iteration b <- Y + M b + Q(b) --------------------------------
    log("--- cell-wise bound iteration")
    omega, theta, hist, v = iterate_bounds(geo, Rn, Dn, rho, cells.R, cells.drho, normA, oscA, D2,
                                           nSi2, iters=args.iters, log=log)
    conv = hist[-1]["growth_sup"] < 1 + 1e-6 and hist[-1]["growth_osc"] < 1 + 1e-6
    results["iteration"] = dict(converged=bool(conv), last=hist[-1], n_iter=len(hist))
    rec.save_json("iteration_history", hist)
    # ---- where does the growth come from (current weights) --------------------------------
    for key, den in (("T1sup", omega), ("T2sup", omega), ("Z2sup", omega),
                     ("T1osc", theta), ("T2osc", theta), ("Z2osc", theta)):
        r_ = v[key] / den
        i = int(np.argmax(r_))
        log(f"   {key}/b: max {r_[i]:.4f} at cell {i} (t={tm[i]:.3f}, h={h[i]:.3g})")
        results[f"ratio_{key}"] = dict(max=float(r_[i]), cell=i, t=float(tm[i]))
    iS = int(np.argmax(v["T2osc"] / theta))
    log(f"   T2 split at cell {iS}: normA*P={v['_S1'][iS]:.3e} EA*Omega={v['_S2'][iS]:.3e} "
        f"2oscA*V={v['_S3'][iS]:.3e}  (theta={theta[iS]:.3e}, omega={omega[iS]:.3e})")
    results["T2_split"] = dict(cell=iS, normA_P=float(v["_S1"][iS]), EA_Omega=float(v["_S2"][iS]),
                               oscA_V=float(v["_S3"][iS]))
    # global split of T2osc/theta over cells: which of the three terms dominates where
    for nm, arr in (("normA*P", v["_S1"]), ("EA*Omega", v["_S2"]), ("2oscA*V", v["_S3"])):
        r_ = 2 * arr / theta
        log(f"   2*{nm}/theta: max {r_.max():.4f} at t={tm[int(np.argmax(r_))]:.3f}")
        results[f"T2osc_part_{nm}"] = float(r_.max())
    if conv:
        # ---- certificate: b := (1+eps) b_lim,  check F(b) < b componentwise -----------------
        eps = 1e-3
        om_c, th_c = omega * (1 + eps), theta * (1 + eps)
        tube_phys = float(st.normS) * float((geo.w[1:] @ om_c).max())
        D2c = lipschitz_A(st, cells.x_lo, cells.x_hi, cells.y_lo, cells.y_hi, tube_phys)
        vc = cap_vectors(geo, Rn, Dn, rho, cells.R, cells.drho, normA, oscA, om_c, th_c, D2c, nSi2)
        Fsup = up(vc["Ysup"] + vc["T1sup"] + vc["T2sup"] + vc["Z2sup"])
        Fosc = up(vc["Yosc"] + vc["T1osc"] + vc["T2osc"] + vc["Z2osc"])
        ok = bool(np.all(Fsup < om_c) and np.all(Fosc < th_c))
        contr = float(max(np.max((vc["T1sup"] + vc["T2sup"] + vc["Z2sup"]) / om_c),
                          np.max((vc["T1osc"] + vc["T2osc"] + vc["Z2osc"]) / th_c)))
        log(f"CERTIFICATE: F(b) < b componentwise: {ok}; contraction constant {contr:.6f}; "
            f"D2 on tube {D2c:.4g} (phys radius {tube_phys:.3e}); sup|f| <= {om_c.max():.3e}, "
            f"state error |I^a f| <= {float((geo.w[1:] @ om_c).max()):.3e}, at T: {float(geo.w[-1] @ om_c):.3e}")
        results["certificate"] = dict(ok=ok, contraction=contr, D2=D2c, tube_phys=tube_phys,
                                      omega_max=float(om_c.max()), state_err_max=float((geo.w[1:] @ om_c).max()),
                                      state_err_T=float(geo.w[-1] @ om_c), eps=eps)
        rec.save_npz("certificate_weights", omega=om_c, theta=th_c, tm=tm, Fsup=Fsup, Fosc=Fosc)
    else:
        results["certificate"] = dict(ok=False, reason="iteration did not converge: rho(M) >= 1")
    # ---- norm constants with the final weights (for the report) ----------------------------
    c = cap_constants(geo, Rn, Dn, rho, cells.R, cells.drho, normA, oscA, omega, theta, D2, nSi2)
    results["norm_constants_final_weights"] = {k: float(val) for k, val in c.items() if not k.startswith("_")}
    log(f"norm constants in the final weighted norm: Y0={c['Y0']:.4g} Z1={c['Z1']:.4g} "
        f"[T1 {c['T1_sup']:.3g}/{c['T1_osc']:.3g} T2 {c['T2_sup']:.3g}/{c['T2_osc']:.3g}] Z2a={c['Z2a']:.3g}")
    rec.save_npz("profile", omega=omega, theta=theta, tm=tm, **{k.strip("_"): val for k, val in v.items()})
    rec.add("results", results)
    rec.add("mesh", dict(N=N, T=float(tm[-1]), h_min=float(h.min()), h_max=float(h.max())))
    rec.add("cells", dict(R_max=float(cells.R.max()), drho_max=float(cells.drho.max()),
                         normA_max=float(normA.max()), oscA_max=float(oscA.max()),
                         rho_node_max=float(rho.max())))
    rec.save_npz("blocks", Rn=Rn, Dn=Dn, rho=rho, normA=normA, oscA=oscA, tm=tm, R=cells.R,
                 drho=cells.drho, diam=diam, x_lo=cells.x_lo, x_hi=cells.x_hi, y_lo=cells.y_lo, y_hi=cells.y_hi)
    print(json.dumps(results, indent=1))
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
