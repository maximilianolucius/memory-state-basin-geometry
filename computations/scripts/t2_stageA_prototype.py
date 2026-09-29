#!/usr/bin/env python3
"""TASK-0002 Stage A, step 0 — size the mesh with a NON-rigorous radius estimate.

Evidence class: none (engineering estimate).  Its only purpose is to choose the
mesh and the certification time before running the ball-arithmetic verifier.
"""
import argparse
import os
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.aposteriori import prototype_radius   # noqa: E402
from msbg.models import AlleePredatorPrey       # noqa: E402
from msbg.provenance import RunRecorder         # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def one(cfg):
    np.seterr(all="ignore")
    theta, a, b, m, alpha, p, T, N, rg = cfg
    model = AlleePredatorPrey(theta=theta, a=a, b=b, m=m)
    out = prototype_radius(model, p, alpha, T, N, rg)
    tm, X, U = out["tm"], out["X"], out["U"]
    best = None
    for n in range(len(U)):
        if not np.isfinite(U[n]):
            break
        lo_x = out["lo"][n, 0] + 0.05     # undo the tube inflation used for L
        hi_x = out["hi"][n, 0] - 0.05
        eta = theta - (hi_x + U[n])
        if lo_x - U[n] > 0 and eta > 0 and (best is None or eta > best["eta"]):
            best = {"cell": n, "t_lo": float(tm[n]), "t_hi": float(tm[n + 1]),
                    "eta": float(eta), "U": float(U[n])}
    return {"N": N, "grade": rg, "T": T, "U_max": float(np.nanmax(U[np.isfinite(U)])),
            "U_end": float(U[-1]), "R_max": float(out["R"].max()),
            "D_max": float(out["D"].max()), "best_certifiable": best,
            "finite": bool(np.isfinite(U).all())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args()
    theta, a, b, m, alpha, p, T = 0.3, 1.0, 1.0, 0.8, 0.85, [2.4372, 2.012], 4.0
    cfgs = [(theta, a, b, m, alpha, p, T, N, rg)
            for N in (1000, 2000, 4000) for rg in (1.0 / alpha, 2.0, 3.0)]
    rec = RunRecorder("t2_stageA_prototype", ROOT)
    rows = []
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        for r in ex.map(one, cfgs):
            rows.append(r)
            b_ = r["best_certifiable"]
            print(f"N={r['N']:5d} grade={r['grade']:.3f}  R_max={r['R_max']:.2e} "
                  f"D_max={r['D_max']:.2e} U_end={r['U_end']:.3e}  finite={r['finite']}  "
                  + (f"best eta={b_['eta']:.4f} on t in [{b_['t_lo']:.3f},{b_['t_hi']:.3f}] U={b_['U']:.2e}"
                     if b_ else "NOT certifiable"), flush=True)
    rec.save_json("rows", rows)
    rec.add("evidence_class", "none - engineering estimate for mesh sizing")
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
