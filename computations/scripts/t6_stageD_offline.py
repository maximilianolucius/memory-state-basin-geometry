#!/usr/bin/env python
"""Re-evaluate the TASK-0006 cell-wise bound operator from saved blocks (Rn, Dn, cells) of a
t6_stageBD run, without recomputing the certified inverse.  Power iteration -> rho(M)."""
import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.aposteriori import collocation                                    # noqa: E402
from msbg.cap import Geometry, cap_vectors, iterate_bounds, power_iteration, up   # noqa: E402
from msbg.models import AlleePredatorPrey                                   # noqa: E402
from msbg.provenance import RunRecorder                                     # noqa: E402
from msbg.validated_res import Setup                                        # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--iters", type=int, default=80)
    ap.add_argument("--xbox", default=None, help="x_lo,x_hi override (else from profile)")
    ap.add_argument("--variant", default="default")
    ap.add_argument("--workers", type=int, default=40)
    ap.add_argument("--K", type=int, default=32)
    args = ap.parse_args()
    np.seterr(all="ignore")
    t0 = time.time()

    def log(*a):
        print(f"[{time.time() - t0:8.1f}s]", *a, flush=True)

    B = np.load(os.path.join(ROOT, "data", f"t6_stageBD_{args.tag}_blocks.npz"))
    tm, Rn, Dn, rho, normA, oscA, R, drho = (B[k] for k in ("tm", "Rn", "Dn", "rho", "normA", "oscA", "R", "drho"))
    N = len(tm) - 1
    st = Setup("1/2", "1/2", "1", "4/5", "17/20", ("277/100", "467/1000"))
    fl, pf = st.floats()
    al = fl["alpha"]
    model = AlleePredatorPrey(theta=fl["theta"], a=fl["a"], b=fl["b"], m=fl["m"])
    X, PHI, M = collocation(model, np.array(pf), al, tm)
    xbox = dict(theta=fl["theta"], a=fl["a"], b=fl["b"], x_lo=float(X[:, 0].min()) - 1e-3,
                x_hi=float(X[:, 0].max()) + 1e-3)
    if "diam" in B.files:
        diam = B["diam"]
    else:
        from msbg.validated import verify_cells
        cells = verify_cells(tm, PHI, st.str["theta"], st.str["a"], st.str["b"], st.str["m"], st.str["alpha"],
                             st.str["p"], 0.0, prec=128, workers=args.workers, K=args.K)
        diam = up(np.sqrt((cells.x_hi - cells.x_lo) ** 2 + (cells.y_hi - cells.y_lo) ** 2))
        log("cells recomputed for diam")
    geo = Geometry(tm, al, PHI, float(st.normS), float(st.normSi), xbox, diam)
    nSi2 = float(up(float(st.normSi) * np.sqrt(2.0)))
    log(f"{args.tag}: N={N} T={tm[-1]}  geometry ready; EA(n>=1) max {np.max(geo.EA[1:]):.3e} (green {np.max(geo.EA_green[1:]):.3e}), "
        f"min(EA,2oscA) max {np.max(np.fmin(geo.EA[1:], 2*oscA[1:])):.3e}, oscA max {oscA.max():.3e}")
    rec = RunRecorder(f"t6_offline_{args.tag}_{args.variant}", ROOT)
    om, th, hist, v = power_iteration(geo, Rn, Dn, R, drho, normA, oscA, nSi2, iters=args.iters, log=log)
    h = np.diff(tm)
    out = {"rho_M": hist[-1], "tag": args.tag, "variant": args.variant}
    for key, den in (("T1sup", om), ("T2sup", om), ("T1osc", th), ("T2osc", th)):
        r_ = v[key] / den
        i = int(np.argmax(r_))
        log(f"   {key}/b: max {r_[i]:.4f} at cell {i} (t={tm[i]:.3f}, h={h[i]:.3g})")
        out[key] = dict(max=float(r_[i]), t=float(tm[i]))
    for nm, arr in (("normA*P", v["_S1"]), ("EA*Omega", v["_S2"]), ("2oscA*V", v["_S3"])):
        r_ = 2 * arr / th
        log(f"   2*{nm}/theta: max {r_.max():.4f} at t={tm[int(np.argmax(r_))]:.3f}")
        out[nm] = float(r_.max())
    # profile of the leading eigenvector-like weights (where the mass sits)
    for q in (0.1, 0.5, 0.9, 1.0):
        i = min(int(q * N), N - 1)
        log(f"   weights at t={tm[i]:.1f}: omega={om[i]:.3e} theta={th[i]:.3e} T1sup={v['T1sup'][i]:.3e} "
            f"S1={v['_S1'][i]:.3e} S2={v['_S2'][i]:.3e} S3={v['_S3'][i]:.3e} oscA={oscA[i]:.3e} EA={geo.EA[i]:.3e}")
    rec.add("result", out)
    rec.save_npz("power_weights", omega=om, theta=th, tm=tm)
    print(json.dumps(out, indent=1))
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
