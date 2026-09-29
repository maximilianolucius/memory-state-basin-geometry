#!/usr/bin/env python3
r"""TASK-0002 Stage A — rigorous certification of entry into R_ext.

Pipeline
--------
1. UNTRUSTED: piecewise-linear product-integration collocation on a graded mesh
   t_k = T (k/N)^grade gives nodal values phi_k.  Nothing about this step is
   trusted; it only proposes phi.
2. TRUSTED (Arb, parallel over cells): for every cell, rigorous bounds
   R_n >= sup |rho|, Lbar_n >= sup ||Dg|| on the r-tube, and a state box.
3. TRUSTED (Arb, parallel over rows): upper bounds of the weights W_{n,j}.
4. TRUSTED (binary64 with upward-rounding safeguards): the scalar recursion
   for Delta_n and U_n.
5. Bootstrap check  max_n U_n < r  and  kappa_n < 1  for all n.
6. Certificate: cells whose rigorous state box, inflated by U_n, lies in
   {0 < x < theta - eta, y > 0}.

Evidence class of a positive outcome: CERTIFIED COMPUTATION, conditional only on
(i) the a posteriori theorem stated in msbg/validated.py (proof in the return),
(ii) correctness of python-flint/Arb ball arithmetic, and (iii) the standard
local existence/continuation theory for Volterra equations with locally
Lipschitz nonlinearity.  If the bootstrap fails the outcome is UNDECIDED, never
"not certified".
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.aposteriori import collocation, graded_mesh                       # noqa: E402
from msbg.models import AlleePredatorPrey                                   # noqa: E402
from msbg.provenance import RunRecorder                                     # noqa: E402
from msbg.validated import (bound_recursion_rigorous, certify_entry,        # noqa: E402
                            row_weights_upper, verify_cells)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--theta", type=float, default=0.3)
    ap.add_argument("--a", type=float, default=1.0)
    ap.add_argument("--b", type=float, default=1.0)
    ap.add_argument("--m", type=float, default=0.8)
    ap.add_argument("--alpha", type=float, default=0.85)
    ap.add_argument("--p", type=float, nargs=2, default=[2.4372, 2.012])
    ap.add_argument("--T", type=float, default=4.0)
    ap.add_argument("--N", type=int, default=4000)
    ap.add_argument("--grade", type=float, default=3.0)
    ap.add_argument("--K", type=int, default=64)
    ap.add_argument("--r", type=float, default=0.05)
    ap.add_argument("--prec", type=int, default=128)
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    np.seterr(all="ignore")

    stage = "t2_stageA_certify" + (f"_{args.tag}" if args.tag else "")
    rec = RunRecorder(stage, ROOT)
    model = AlleePredatorPrey(theta=args.theta, a=args.a, b=args.b, m=args.m)
    p = np.array(args.p, float)
    rec.add("inputs", vars(args))
    rec.add("model_provenance", model.provenance)

    t0 = time.time()
    tm = graded_mesh(args.T, args.N, args.grade)
    X, PHI, M = collocation(model, p, args.alpha, tm)
    t_col = time.time() - t0
    print(f"[1] untrusted collocation N={args.N} grade={args.grade}: {t_col:.1f}s", flush=True)

    cells = verify_cells(tm, PHI, args.theta, args.a, args.b, args.m, args.alpha, p, args.r,
                         prec=args.prec, workers=args.workers, K=args.K)
    print(f"[2] rigorous cells (K={args.K}, prec={args.prec}): {cells.seconds:.1f}s  "
          f"R_max={cells.R.max():.3e}  L_max={cells.L.max():.3f}", flush=True)

    t1 = time.time()
    W = row_weights_upper(tm, args.alpha, prec=args.prec, workers=args.workers)
    print(f"[3] rigorous weights: {time.time()-t1:.1f}s", flush=True)

    t2 = time.time()
    U, D, kap = bound_recursion_rigorous(tm, args.alpha, cells.R, cells.L, W, prec=args.prec)
    finite = bool(np.isfinite(U).all())
    boot = finite and float(np.max(U)) < args.r
    print(f"[4] rigorous recursion: {time.time()-t2:.1f}s  max kappa={np.max(kap):.3e}  "
          f"max U={np.max(U):.3e}  bootstrap (max U < r={args.r}): {boot}", flush=True)

    cert = certify_entry(args.theta, cells, U, tm)
    ok = np.flatnonzero(cert["certified"]) if boot else np.array([], dtype=int)
    if len(ok):
        k = int(ok[np.argmax(cert["eta"][ok])])
        # contiguous certified run containing the best cell
        runs, start = [], ok[0]
        for i in range(1, len(ok)):
            if ok[i] != ok[i - 1] + 1:
                runs.append((start, ok[i - 1]))
                start = ok[i]
        runs.append((start, ok[-1]))
        best_run = max(runs, key=lambda r: tm[r[1] + 1] - tm[r[0]])
        verdict = "CERTIFIED"
        cert_rec = {
            "verdict": verdict,
            "best_cell": k,
            "time_box": [float(tm[k]), float(tm[k + 1])],
            "eta": float(cert["eta"][k]),
            "state_box_x": [float(cert["x_lo"][k]), float(cert["x_hi"][k])],
            "state_box_y_lower": float(cert["y_lo"][k]),
            "U_at_best": float(U[k]),
            "n_certified_cells": int(len(ok)),
            "longest_certified_time_interval": [float(tm[best_run[0]]),
                                                float(tm[best_run[1] + 1])],
            "min_eta_on_longest_interval": float(np.min(cert["eta"][best_run[0]:best_run[1] + 1])),
        }
        print(f"\nVERDICT: CERTIFIED")
        print(f"  best time box   t in [{tm[k]:.6f}, {tm[k+1]:.6f}]")
        print(f"  rigorous state  x in [{cert['x_lo'][k]:.6f}, {cert['x_hi'][k]:.6f}],  "
              f"y >= {cert['y_lo'][k]:.6f}")
        print(f"  margin          eta = theta - sup x = {cert['eta'][k]:.6f}")
        print(f"  enclosure radius U = {U[k]:.3e}")
        print(f"  certified on {len(ok)} cells; longest contiguous certified interval "
              f"t in [{tm[best_run[0]]:.4f}, {tm[best_run[1]+1]:.4f}] with eta >= "
              f"{cert_rec['min_eta_on_longest_interval']:.5f}")
    else:
        verdict = "UNDECIDED"
        cert_rec = {"verdict": verdict,
                    "reason": ("bootstrap failed" if not boot else
                               "no cell whose inflated box separates from the threshold")}
        print(f"\nVERDICT: UNDECIDED ({cert_rec['reason']})")

    rec.add("certificate", cert_rec)
    rec.add("bootstrap", {"r": args.r, "max_U": float(np.max(U)) if finite else None,
                          "max_kappa": float(np.max(kap)), "passed": boot})
    rec.add("timing_s", {"collocation": t_col, "cells": cells.seconds})
    rec.add("semantics", {
        "arithmetic": f"python-flint / Arb ball arithmetic at {args.prec} bits for every "
                      "transcendental and every enclosure; binary64 with explicit upward "
                      "rounding (nextafter + Higham gamma_n factor) for the non-negative "
                      "scalar recursion",
        "untrusted_inputs": "mesh points and nodal phi values, taken as exact binary64 numbers",
        "theorem": "a posteriori Volterra-Gronwall enclosure, msbg/validated.py docstring",
        "norm": "max-norm on R^2, induced row-sum norm on 2x2 matrices",
        "undecided_policy": "UNDECIDED whenever the bootstrap or the separation fails",
    })
    rec.add("evidence_class", "CERTIFIED COMPUTATION" if verdict == "CERTIFIED" else "UNDECIDED")
    rec.save_npz("arrays", tm=tm, X_nodes=X, PHI=PHI, R=cells.R, L=cells.L,
                 x_lo=cells.x_lo, x_hi=cells.x_hi, y_lo=cells.y_lo, y_hi=cells.y_hi,
                 U=U, D=D, kappa=kap, eta=cert["eta"], certified=cert["certified"])
    print("\nmanifest:", rec.finish())


if __name__ == "__main__":
    main()
