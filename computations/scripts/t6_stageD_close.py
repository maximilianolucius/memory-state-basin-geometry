#!/usr/bin/env python
"""TASK-0006 Stage D closure: from the rigorous blocks of a t6_stageBD run, (1) spectral radius
of the linear bound operator, (2) monotone iteration b <- F(b), (3) certificate F(b) < b for
b = (omega, theta, beta) = cell-wise bounds of (sup|f|, osc f, sup|(I-pi)f|).

Usable standalone (--tag: reload saved blocks) or through ``close`` from t6_stageBD_cap.py.
"""
import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.aposteriori import collocation                                      # noqa: E402
from msbg.cap import (COMPONENTS, Geometry, check_certificate, contraction_constant,     # noqa: E402
                      iterate_bounds,
                      lipschitz_A_cells, power_iteration, up)
from msbg.models import AlleePredatorPrey                                     # noqa: E402
from msbg.provenance import RunRecorder                                       # noqa: E402
from msbg.validated_res import Setup                                          # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def close(geo, Rn, Dn, rho, R, drho, normA, oscA, st, x_lo, x_hi, rec, log, iters=300, tube0=1e-2,
          bubble=True, eps=1e-3):
    tm, N, h = geo.tm, geo.N, geo.h
    nSi2 = float(up(float(st.normSi) * np.sqrt(2.0)))
    args = (geo, Rn, Dn, rho, R, drho, normA, oscA)
    res = {"bubble_component": bool(bubble)}
    # ---- (1) spectral radius ---------------------------------------------------------------
    log(f"--- power iteration on the linear bound operator M (bubble={bubble})")
    bp, phist, vp = power_iteration(geo, Rn, Dn, R, drho, normA, oscA, nSi2, iters=80, log=None, bubble=bubble)
    res["spectral_radius"] = dict(cw_lower=phist[-1]["cw_lower"], cw_upper=phist[-1]["cw_upper"], n_iter=len(phist))
    log(f"rho(M) in [{phist[-1]['cw_lower']:.4f}, {phist[-1]['cw_upper']:.4f}] after {len(phist)} iterations")
    for i, c in enumerate(COMPONENTS[: 3 if bubble else 2]):
        for p in ("T1", "T2"):
            r_ = vp[p + c] / bp[i]
            j = int(np.argmax(r_))
            res[f"power_{p}{c}"] = dict(max=float(r_[j]), t=float(tm[j]))
    log("   linear couplings in the Perron weights: " + ", ".join(
        f"{k[6:]} {v['max']:.3f}@t={v['t']:.1f}" for k, v in res.items() if k.startswith("power_")))
    # ---- (2) monotone iteration -------------------------------------------------------------
    D2 = lipschitz_A_cells(st, x_lo, x_hi, tube0)
    log(f"--- b-iteration (D2 per cell on tube {tube0}: max {D2.max():.4g}, at T {D2[-1]:.4g})")
    b, hist, v = iterate_bounds(*args, D2, nSi2, iters=iters, log=None, bubble=bubble)
    conv = max(hist[-1]["growth"]) < 1 + 1e-6 and np.isfinite(hist[-1]["omega_max"])
    for hrow in hist[:3] + hist[-2:]:
        log(f"  b-iter {hrow['it']:3d}: growth {hrow['growth']}  omega_max={hrow['omega_max']:.3e} "
            f"theta_max={hrow['theta_max']:.3e} beta_max={hrow['beta_max']:.3e} Omega_max={hrow['Omega_max']:.3e}")
    res["iteration"] = dict(converged=bool(conv), n_iter=len(hist), last=hist[-1])
    rec.save_json("iteration_history", hist)
    if not conv:
        res["certificate"] = dict(ok=False, reason="b-iteration diverged")
        log("CERTIFICATE: NOT OBTAINED (b-iteration diverged)")
        return res, None
    # ---- (3) certificate --------------------------------------------------------------------
    best = None
    for eps_try in (0.3, 0.1, 0.03, 0.01, eps):                # inflate the limit: widest strict margin wins
        bc_ = [x * (1 + eps_try) for x in b]
        Om_ = up(geo.w[1:] @ bc_[0])
        tube_ = float(up(float(st.normS) * float(Om_.max())))
        D2c_ = lipschitz_A_cells(st, x_lo, x_hi, tube_)
        ok_, contr_, slack_, F_, vc_ = check_certificate(*args, D2c_, nSi2, bc_, bubble=bubble)
        log(f"   inflation eps={eps_try}: F(b) < b: {ok_}, max_n (F(b) - b)/b = {-slack_:+.3e}")
        if ok_ and (best is None or slack_ > best[3]):
            best = (eps_try, bc_, Om_, slack_, tube_, D2c_, ok_, contr_, F_, vc_)
    if best is None:
        res["certificate"] = dict(ok=False, reason="F(b) < b failed for every inflation")
        log("CERTIFICATE: NOT OBTAINED (F(b) < b failed)")
        return res, None
    eps, bc, Om, slack, tube_phys, D2c, ok, contr, F, vc = best
    res["certificate"] = dict(ok=bool(ok), ratio_nonconstant_part_b_norm=contr, min_slack=slack, eps=eps,
                              radii_polynomial_componentwise_max=-slack,
                              D2_max=float(D2c.max()), D2_at_T=float(D2c[-1]), tube_phys=tube_phys,
                              omega_max=float(bc[0].max()), omega_median=float(np.median(bc[0])),
                              omega_T=float(bc[0][-1]), theta_max=float(bc[1].max()), beta_max=float(bc[2].max()),
                              state_err_adapted_max=float(Om.max()), state_err_adapted_T=float(Om[-1]),
                              state_err_phys_max=tube_phys)
    log(f"CERTIFICATE: F(b) < b componentwise: {ok}; min slack {slack:.3e}; "
        f"sup|f|_S <= {bc[0].max():.3e}; state error (adapted) <= {Om.max():.3e}, at T {Om[-1]:.3e}; "
        f"physical <= {tube_phys:.3e}")
    kappa, q = contraction_constant(geo, Rn, Dn, R, drho, normA, oscA, D2c, nSi2, bc, iters=80)
    res["certificate"]["contraction_q_norm"] = kappa
    res["certificate"]["banach"] = bool(ok and kappa < 1.0)
    log(f"CONTRACTION in the q-weighted norm (Perron weights of M + Z2'(b)): kappa <= {kappa:.6f}  "
        f"-> Banach fixed point in the b-set: {ok and kappa < 1.0}")
    rec.save_npz("contraction_weights", q_sup=q[0], q_osc=q[1], q_bub=q[2], tm=tm)
    # norm constants of the classical radii polynomial in the b-weighted norm (r = 1 is the b-set)
    Y0 = float(max(np.max(vc["Y" + c] / bc[i]) for i, c in enumerate(COMPONENTS)))
    Z1 = float(max(np.max((vc["T1" + c] + vc["T2" + c]) / bc[i]) for i, c in enumerate(COMPONENTS)))
    Z2 = float(max(np.max(vc["Z2" + c] / bc[i]) for i, c in enumerate(COMPONENTS)))
    res["radii_polynomial_weighted_norm"] = dict(Y0=Y0, Z1=Z1, Z2_at_r1=Z2, p_at_r1=Y0 + Z1 + Z2 - 1.0,
                                                 note="upper bounds; p(1) = Y0 + Z1 + Z2(1) - 1 (componentwise F(b) < b is the sharper statement)")
    log(f"   weighted-norm radii polynomial at r = 1: Y0={Y0:.4f} Z1={Z1:.4f} Z2={Z2:.4f} -> p(1) <= {Y0 + Z1 + Z2 - 1:+.4f}")
    rec.save_npz("certificate_weights", omega=bc[0], theta=bc[1], beta=bc[2], tm=tm, Fsup=F[0], Fosc=F[1],
                 Fbub=F[2], Omega=Om)
    return res, bc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--iters", type=int, default=300)
    ap.add_argument("--no-bubble", action="store_true")
    a = ap.parse_args()
    np.seterr(all="ignore")
    t0 = time.time()

    def log(*x):
        print(f"[{time.time() - t0:8.1f}s]", *x, flush=True)

    B = np.load(os.path.join(ROOT, "data", f"t6_stageBD_{a.tag}_blocks.npz"))
    tm = B["tm"]
    st = Setup("1/2", "1/2", "1", "4/5", "17/20", ("277/100", "467/1000"))
    fl, pf = st.floats()
    model = AlleePredatorPrey(theta=fl["theta"], a=fl["a"], b=fl["b"], m=fl["m"])
    X, PHI, M = collocation(model, np.array(pf), fl["alpha"], tm)
    xbox = dict(theta=fl["theta"], a=fl["a"], b=fl["b"], x_lo=float(B["x_lo"].min()), x_hi=float(B["x_hi"].max()))
    geo = Geometry(tm, fl["alpha"], PHI, float(st.normS), float(st.normSi), xbox, B["diam"])
    geo.Qn, geo.DQn = B["Qn"], B["DQn"]
    sfx = "_nobubble" if a.no_bubble else ""
    rec = RunRecorder(f"t6_stageD_{a.tag}{sfx}", ROOT)
    rec.add("source_blocks", f"data/t6_stageBD_{a.tag}_blocks.npz")
    log(f"{a.tag}: N={geo.N} T={tm[-1]} blocks loaded")
    res, bc = close(geo, B["Rn"], B["Dn"], B["rho"], B["R"], B["drho"], B["normA"], B["oscA"], st,
                    B["x_lo"], B["x_hi"], rec, log, iters=a.iters, bubble=not a.no_bubble)
    rec.add("results", res)
    print(json.dumps(res, indent=1, default=float))
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
