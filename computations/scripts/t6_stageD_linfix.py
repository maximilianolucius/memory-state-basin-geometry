#!/usr/bin/env python
"""TASK-0006 diagnostic: linear fixed point b* = (I - M)^{-1} Y of the cell-wise bound map from
the saved blocks of a t6_stageBD run, and the size of the quadratic term Z2(b*) against b*.
Z2(b*)/b* < 1 - rho-ish is what the closure needs; the ratio says by how much it fails."""
import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.aposteriori import collocation                                     # noqa: E402
from msbg.cap import Geometry, cap_vectors, lipschitz_A_cells, up            # noqa: E402
from msbg.models import AlleePredatorPrey                                    # noqa: E402
from msbg.provenance import RunRecorder                                      # noqa: E402
from msbg.validated_res import Setup                                         # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--tube", type=float, default=1e-2)
    a = ap.parse_args()
    np.seterr(all="ignore")
    B = np.load(os.path.join(ROOT, "data", f"t6_stageBD_{a.tag}_blocks.npz"))
    tm, Rn, Dn, rho, normA, oscA, R, drho = (B[k] for k in ("tm", "Rn", "Dn", "rho", "normA", "oscA", "R", "drho"))
    N = len(tm) - 1
    st = Setup("1/2", "1/2", "1", "4/5", "17/20", ("277/100", "467/1000"))
    fl, pf = st.floats()
    al = fl["alpha"]
    model = AlleePredatorPrey(theta=fl["theta"], a=fl["a"], b=fl["b"], m=fl["m"])
    X, PHI, M = collocation(model, np.array(pf), al, tm)
    xbox = dict(theta=fl["theta"], a=fl["a"], b=fl["b"], x_lo=float(B["x_lo"].min()), x_hi=float(B["x_hi"].max()))
    geo = Geometry(tm, st.str["alpha"], PHI, float(st.normS), float(st.normSi), xbox, B["diam"])
    geo.Qn, geo.DQn = B["Qn"], B["DQn"]
    nSi2 = float(up(float(st.normSi) * np.sqrt(2.0)))
    D2 = lipschitz_A_cells(st, B["x_lo"], B["x_hi"], a.tube)
    args = (geo, Rn, Dn, rho, R, drho, normA, oscA)
    v = cap_vectors(*args, np.full(N, 1e-300), np.full(N, 1e-300), 0.0, nSi2)
    Ys, Yo = v["Ysup"].copy(), v["Yosc"].copy()
    om, th = np.maximum(Ys, 1e-300), np.maximum(Yo, 1e-300)
    for it in range(600):
        v = cap_vectors(*args, om, th, 0.0, nSi2)
        o2 = up(v["Ysup"] + v["T1sup"] + v["T2sup"]); t2 = up(v["Yosc"] + v["T1osc"] + v["T2osc"])
        g = max((o2 / om).max(), (t2 / th).max())
        om, th = o2, t2
        if g < 1 + 1e-9:
            break
    Om = v["Omega"]
    v = cap_vectors(*args, om, th, D2, nSi2)
    out = {"tag": a.tag, "N": N, "T": float(tm[-1]), "lin_iters": it + 1, "lin_converged": bool(g < 1 + 1e-9),
           "Ysup_max": float(Ys.max()), "Ysup_median": float(np.median(Ys)), "Yosc_max": float(Yo.max()),
           "omega_max": float(om.max()), "omega_median": float(np.median(om)), "omega_T": float(om[-1]),
           "theta_max": float(th.max()), "Omega_max": float(Om.max()), "Omega_T": float(Om[-1]),
           "state_err_phys_max": float(st.normS) * float(Om.max())}
    for key, den in (("Z2sup", om), ("Z2osc", th), ("T1sup", om), ("T2sup", om), ("T1osc", th), ("T2osc", th)):
        r = v[key] / den
        i = int(r.argmax())
        out[f"{key}_over_b"] = {"max": float(r[i]), "t": float(tm[i])}
    # where does omega at T come from: Y, T1 (Q part / remainder part), T2
    i = N - 1
    out["omega_T_split"] = {"Y": float(v["Ysup"][i]), "T1": float(v["T1sup"][i]), "T2": float(v["T2sup"][i]),
                            "Z2": float(v["Z2sup"][i])}
    # contribution of early cells to Omega_T
    w = geo.w[-1] * om
    for tc in (0.1, 1.0, 10.0, 30.0, 100.0):
        out[f"Omega_T_from_t<{tc}"] = float(w[tm[1:] <= tc].sum())
    rec = RunRecorder(f"t6_linfix_{a.tag}", ROOT)
    rec.add("result", out)
    rec.save_npz("linfix", omega=om, theta=th, tm=tm, Omega=Om)
    print(json.dumps(out, indent=1))
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
