#!/usr/bin/env python3
r"""TASK-0004 Stages C+D+E — end-to-end certificate: entry into R_ext AND memory-tail survival.

Pipeline (trusted unless stated):
 1. exact rational setup, adapted norm (msbg.validated_res.Setup);
 2. UNTRUSTED float collocation on a graded mesh -> nodal phi;
 3. rigorous per-cell defect and state boxes (msbg.validated.verify_cells, Arb);
 4. rigorous a_n >= ||S^{-1}(Dg - J)S||_2 on the tube (Arb);
 5. rigorous envelope of |E_{a,a}(lambda rho)| and kernel integrals;
 6. resolvent recursion, bootstrap  max U < r  (THEOREM R);
 7. entry certificate: cells whose inflated box lies in {0 < x < theta, y > 0};
 8. rigorous N_j >= sup |N(u)|_S, K_up, (C0, c3), M_T upper bound;
 9. M1 inequality  M_T + K (C0 + c3 r) r^2 < r  at a rational r.

Verdicts: ENTRY in {CERTIFIED, UNDECIDED};  M1 inequality in {SEPARATED, UNDECIDED}.
Survival itself is CONDITIONAL on CANDIDATE M1 and on the Mittag-Leffler
representation and variation-of-constants identity (ROUND-0005).
"""
from __future__ import annotations

import argparse
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.aposteriori import collocation, graded_mesh                            # noqa: E402
from msbg.models import AlleePredatorPrey                                        # noqa: E402
from msbg.provenance import RunRecorder                                          # noqa: E402
from msbg.solvers import METHODS, solve                                          # noqa: E402
from msbg.validated import verify_cells                                          # noqa: E402
from msbg.validated_res import (Setup, adapted_C, cell_coefficients,             # noqa: E402
                                kernel_integrator, m1_radius, memory_tail_bound,
                                nonlinearity_sup, resolvent_recursion, up)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--theta", default="1/2")
    ap.add_argument("--a", default="1/2")
    ap.add_argument("--b", default="1")
    ap.add_argument("--m", default="4/5")
    ap.add_argument("--alpha", default="17/20")
    ap.add_argument("--p", nargs=2, default=["277/100", "467/1000"])
    ap.add_argument("--T", type=float, default=1000.0)
    ap.add_argument("--N", type=int, default=16000)
    ap.add_argument("--grade", type=float, default=3.0)
    ap.add_argument("--K", type=int, default=64)
    ap.add_argument("--r", type=float, default=0.02, help="tube radius in the adapted norm")
    ap.add_argument("--sub", type=int, default=4)
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    ap.add_argument("--float-check", action="store_true")
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    np.seterr(all="ignore")
    rec = RunRecorder("t4_certificate" + (f"_{args.tag}" if args.tag else ""), ROOT)
    st = Setup(args.theta, args.a, args.b, args.m, args.alpha, args.p)
    fl, pf = st.floats()
    model = AlleePredatorPrey(theta=fl["theta"], a=fl["a"], b=fl["b"], m=fl["m"])
    print(f"E* = ({st.xs}, {st.ys}),  lambda = {st.mu} + i sqrt({st.nu2}),  |p-E*|_S <= {st.c_norm:.5f}")
    print(f"||S||_2 <= {st.normS:.5f}, ||S^-1||_2 <= {st.normSi:.5f}", flush=True)
    rec.add("inputs", vars(args))
    rec.add("exact", {"E_star": [str(st.xs), str(st.ys)], "J": [[str(v) for v in r] for r in st.J],
                      "mu": str(st.mu), "nu_squared": str(st.nu2),
                      "S": "[[J12, 0],[mu - J11, -nu]]"})

    if args.float_check:
        fc = {}
        for meth in METHODS:
            for h in (0.02, 0.01):
                n = int(round(args.T / h))
                r_ = solve(model, [pf], fl["alpha"], h, n, method=meth, store=True,
                           store_stride=max(1, n // 5000))
                x = r_.x[:, 0, :]
                fc[f"{meth}_h{h}"] = {"min_x": float(x[:, 0].min()), "final": x[-1].tolist(),
                                      "min_pos": float(x.min())}
                print(f"float {meth:8} h={h}: min x = {x[:,0].min():.6f} "
                      f"(theta - min x = {fl['theta']-x[:,0].min():+.6f}), x(T) = {x[-1]}", flush=True)
        rec.add("float_check", fc)

    t0 = time.time()
    tm = graded_mesh(args.T, args.N, args.grade)
    X, PHI, M = collocation(model, np.array(pf), fl["alpha"], tm)
    print(f"[2] collocation: {time.time()-t0:.1f}s", flush=True)

    r_box = float(up(st.normS * args.r))
    cells = verify_cells(tm, PHI, st.str["theta"], st.str["a"], st.str["b"], st.str["m"],
                         st.str["alpha"], st.str["p"], r_box, prec=128, workers=args.workers,
                         K=args.K)
    Rs = up(st.normSi * np.sqrt(2.0) * cells.R)
    print(f"[3] cells: {cells.seconds:.1f}s  max-norm defect R_max = {cells.R.max():.3e}", flush=True)

    a_coef = cell_coefficients(st, cells.x_lo, cells.x_hi, cells.y_lo, cells.y_hi, r_box,
                               workers=args.workers)
    t1 = time.time()
    ker = kernel_integrator(st, args.T, workers=args.workers)
    K_up = ker.total_upper(st)
    print(f"[5] envelope: {time.time()-t1:.1f}s ({len(ker.env)} cells)  K_up = {K_up:.5f}  "
          f"(exact lower bound 1/|lambda| = {float((1/st.C['xl']).mid()):.5f})", flush=True)

    t2 = time.time()
    U, D, kap = resolvent_recursion(tm, Rs, a_coef, ker, sub=args.sub)
    finite = bool(np.isfinite(U).all())
    boot = finite and float(U.max()) < args.r
    print(f"[6] recursion: {time.time()-t2:.1f}s  max a_n = {a_coef.max():.3f}  max kappa = "
          f"{np.max(kap):.3e}  max D = {np.max(D):.3e}  max U = {np.max(U):.3e}  "
          f"bootstrap (< r = {args.r}): {boot}", flush=True)
    res = {"bootstrap": {"passed": boot, "max_U": float(U.max()) if finite else None, "r": args.r,
                         "max_kappa": float(np.max(kap)), "amplification_maxU_over_maxD":
                         float(U.max() / D.max()) if finite else None}}
    entry = {"verdict": "UNDECIDED"}
    m1 = {"verdict": "UNDECIDED"}
    if boot:
        pad = up(st.normS * U)
        th_lo = float(np.nextafter(st.theta_f, -np.inf))
        xlo, xhi, ylo = cells.x_lo - pad, cells.x_hi + pad, cells.y_lo - pad
        ok = np.flatnonzero((xlo > 0) & (ylo > 0) & (xhi < th_lo))
        if len(ok):
            k = int(ok[np.argmax(th_lo - xhi[ok])])
            entry = {"verdict": "CERTIFIED", "time_box": [float(tm[k]), float(tm[k + 1])],
                     "x_box": [float(xlo[k]), float(xhi[k])], "y_lower": float(ylo[k]),
                     "eta": float(th_lo - xhi[k]), "n_cells": int(len(ok)),
                     "time_span_of_certified_cells": [float(tm[ok[0]]), float(tm[ok[-1] + 1])]}
            print(f"[7] ENTRY CERTIFIED: t in [{tm[k]:.6f}, {tm[k+1]:.6f}], x in "
                  f"[{xlo[k]:.6f}, {xhi[k]:.6f}], y >= {ylo[k]:.6f}, eta = {th_lo - xhi[k]:.6f}; "
                  f"{len(ok)} cells in t in [{tm[ok[0]]:.3f}, {tm[ok[-1]+1]:.3f}]", flush=True)
        else:
            print("[7] ENTRY UNDECIDED", flush=True)
        Nsup = nonlinearity_sup(st, cells.x_lo, cells.x_hi, cells.y_lo, cells.y_hi, pad,
                                workers=args.workers)
        mt = memory_tail_bound(st, tm, Nsup, K_up)
        C0, c3 = adapted_C(st)
        margin, r_m1, KCr = m1_radius(mt["M_T_upper"], K_up, C0, c3)
        sep = margin > 0 and KCr < 1
        m1 = {"verdict": "SEPARATED" if sep else "UNDECIDED", "T": args.T, "norm": "adapted |S^-1 u|_2",
              "M_T_upper": mt["M_T_upper"], "M_T_terms": mt, "K_J_upper": K_up, "C0": C0, "c3": c3,
              "r": r_m1, "margin_lower": margin, "K_C_r_upper": KCr,
              "state_at_T_box": [[float(xlo[-1]), float(xhi[-1])],
                                 [float(ylo[-1]), float(cells.y_hi[-1] + pad[-1])]]}
        print(f"[8] M_T <= {mt['M_T_upper']:.5e}  = linear flow {mt['term_linear_flow']:.3e} + far "
              f"history {mt['term_far_history']:.3e} + near history {mt['term_near_history']:.3e} "
              f"(sigma1 = {mt['sigma1']})")
        print(f"    K_J <= {K_up:.5f},  C_r <= {C0:.5f} + {c3:.5f} r")
        print(f"[9] M1 inequality at r = {r_m1}:  r - K C_r r^2 - M_T >= {margin:+.5e},  "
              f"K C_r r <= {KCr:.4f}   ->  {m1['verdict']}", flush=True)
    res.update(entry=entry, m1=m1)
    rec.add("result", res)
    rec.add("semantics", {
        "trusted": "Arb ball arithmetic for every enclosure; binary64 with upward rounding for "
                   "non-negative sums; exact rationals for the model, alpha and p",
        "untrusted": "mesh and nodal phi (exact binary64 inputs)",
        "conditional_on": ["CANDIDATE M1", "variation-of-constants identity for linear Caputo "
                           "Volterra equations", "integral representation of E_{a,b} in the "
                           "sector a pi/2 < |arg z| < a pi", "THEOREM X1 and E1 for the fibre claim"],
    })
    rec.add("evidence_class", "CERTIFIED COMPUTATION (conditional, see semantics)")
    rec.save_npz("arrays", tm=tm, U=U, D=D, kappa=kap, a_coef=a_coef, Rs=Rs, R=cells.R,
                 x_lo=cells.x_lo, x_hi=cells.x_hi, y_lo=cells.y_lo, y_hi=cells.y_hi)
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
