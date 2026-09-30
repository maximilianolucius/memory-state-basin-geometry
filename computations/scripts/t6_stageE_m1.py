#!/usr/bin/env python
"""TASK-0006 Stage E: entry certificate + rigorous M_T (infinite post-cut sup) + M1 inequality
from the cell-wise CAP certificate produced by t6_stageBD_cap.py.

Input: data/t6_stageBD_<tag>_certificate_weights.npz  (omega, theta, tm; F(b) < b verified there).
The certified source error f satisfies sup_{C_n}|f|_S <= omega_n, hence the state error
e = x - xhat satisfies |e(t)|_S <= Omega_n := sum_j w_{n+1,j} omega_j on C_n (rigorous cell
weights) and |e|_2 <= ||S|| Omega_n.  This pad widens the Arb state boxes of the cells; the
entry certificate, N-sup, M_T and the M1 radius are then those of TASK-0004 (validated_res).
"""
import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.aposteriori import collocation                                    # noqa: E402
from msbg.cap import cell_weights, up                                       # noqa: E402
from msbg.models import AlleePredatorPrey                                   # noqa: E402
from msbg.provenance import RunRecorder                                     # noqa: E402
from msbg.validated import verify_cells                                     # noqa: E402
from msbg.validated_res import (Setup, adapted_C, kernel_integrator, m1_radius,   # noqa: E402
                                memory_tail_bound, nonlinearity_sup)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True, help="tag of the t6_stageBD run")
    ap.add_argument("--prefix", default="t6_stageD", help="t6_stageD (closure driver) or t6_stageBD")
    ap.add_argument("--K", type=int, default=32)
    ap.add_argument("--workers", type=int, default=40)
    args = ap.parse_args()
    np.seterr(all="ignore")
    t0 = time.time()

    def log(*a):
        print(f"[{time.time() - t0:8.1f}s]", *a, flush=True)

    cert = np.load(os.path.join(ROOT, "data", f"{args.prefix}_{args.tag}_certificate_weights.npz"))
    tm, omega = cert["tm"], cert["omega"]
    N = len(tm) - 1
    st = Setup("1/2", "1/2", "1", "4/5", "17/20", ("277/100", "467/1000"))
    fl, pf = st.floats()
    al = fl["alpha"]
    model = AlleePredatorPrey(theta=fl["theta"], a=fl["a"], b=fl["b"], m=fl["m"])
    rec = RunRecorder(f"t6_stageE_{args.tag}", ROOT)
    rec.add("source_certificate", f"data/{args.prefix}_{args.tag}_certificate_weights.npz")

    X, PHI, M = collocation(model, np.array(pf), al, tm)
    strs = st.str
    cells = verify_cells(tm, PHI, strs["theta"], strs["a"], strs["b"], strs["m"], strs["alpha"],
                         strs["p"], 0.0, prec=128, workers=args.workers, K=args.K)
    log(f"cells recomputed: R_max={cells.R.max():.3e}")

    # state-error pad per cell (physical max-norm): |e|_inf <= |e|_2 <= ||S|| * Omega_n
    Om = np.zeros(N)
    for n in range(N):
        Om[n] = float(np.dot(cell_weights(tm, tm[n + 1], al)[: n + 1], omega[: n + 1]))
    pad = up(float(st.normS) * up(Om))
    log(f"state pad: max {pad.max():.3e} at t={tm[int(np.argmax(pad))]:.2f}; at T {pad[-1]:.3e}; "
        f"adapted Omega max {Om.max():.3e}")
    rec.add("pad", dict(max=float(pad.max()), at_T=float(pad[-1]), Omega_max=float(Om.max())))

    # ---- entry certificate -----------------------------------------------------------------
    th_lo = float(np.nextafter(st.theta_f, -np.inf))
    xlo, xhi, ylo = cells.x_lo - pad, cells.x_hi + pad, cells.y_lo - pad
    ok = np.flatnonzero((xlo > 0) & (ylo > 0) & (xhi < th_lo))
    if len(ok):
        k = int(ok[np.argmax(th_lo - xhi[ok])])
        entry = {"verdict": "CERTIFIED", "time_box": [float(tm[k]), float(tm[k + 1])],
                 "x_box": [float(xlo[k]), float(xhi[k])], "y_lower": float(ylo[k]),
                 "eta": float(th_lo - xhi[k]), "n_cells": int(len(ok)),
                 "time_span_of_certified_cells": [float(tm[ok[0]]), float(tm[ok[-1] + 1])]}
        log(f"ENTRY CERTIFIED: t in [{tm[k]:.6f},{tm[k+1]:.6f}], x in [{xlo[k]:.6f},{xhi[k]:.6f}], "
            f"y >= {ylo[k]:.6f}, eta = {th_lo - xhi[k]:.6f}; {len(ok)} cells, "
            f"t in [{tm[ok[0]]:.3f},{tm[ok[-1]+1]:.3f}]")
    else:
        entry = {"verdict": "UNDECIDED", "min_xhi_plus_pad": float(xhi.min())}
        log(f"ENTRY UNDECIDED: min(x_hi + pad) = {xhi.min():.6f} vs theta = {st.theta_f}")
    rec.add("entry", entry)

    # ---- M_T (sup over t >= T, rigorous) and M1 inequality -------------------------------------
    ker = kernel_integrator(st, float(tm[-1]), workers=args.workers)
    K_up = ker.total_upper(st)
    log(f"K_J <= {K_up:.5f}")
    Nsup = nonlinearity_sup(st, cells.x_lo, cells.x_hi, cells.y_lo, cells.y_hi, pad, workers=args.workers)
    mt = memory_tail_bound(st, tm, Nsup, K_up, sigma1_list=(1.0, 2.0, 5.0, 25.0, 50.0, 100.0, 200.0, 400.0))
    if mt is None:
        log("M_T: no admissible sigma1 < T; M1 skipped")
        rec.add("m1", {"verdict": "SKIPPED (T too short)"})
        print(json.dumps(dict(entry=entry), indent=1, default=float))
        print("manifest:", rec.finish())
        return
    C0, c3 = adapted_C(st)
    margin, r_m1, KCr = m1_radius(mt["M_T_upper"], K_up, C0, c3)
    sep = margin > 0 and KCr < 1
    m1 = {"verdict": "SEPARATED" if sep else "UNDECIDED", "T": float(tm[-1]),
          "norm": "adapted |S^-1 u|_2", "M_T_upper": mt["M_T_upper"], "M_T_terms": mt,
          "K_J_upper": K_up, "C0": C0, "c3": c3, "r": r_m1, "margin_lower": margin,
          "K_C_r_upper": KCr,
          "state_at_T_box": [[float(xlo[-1]), float(xhi[-1])], [float(ylo[-1]), float(cells.y_hi[-1] + pad[-1])]]}
    log(f"M_T <= {mt['M_T_upper']:.5e} = linear flow {mt['term_linear_flow']:.3e} + far history "
        f"{mt['term_far_history']:.3e} + near history {mt['term_near_history']:.3e} (sigma1={mt['sigma1']})")
    log(f"M1 at r = {r_m1}: r - K C_r r^2 - M_T >= {margin:+.5e}, K C_r r <= {KCr:.4f} -> {m1['verdict']}")
    rec.add("m1", m1)
    print(json.dumps(dict(entry=entry, m1=m1), indent=1, default=float))
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
