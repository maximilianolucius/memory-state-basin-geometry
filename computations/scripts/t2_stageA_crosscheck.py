#!/usr/bin/env python3
"""TASK-0002 Stage A — consistency check of every certificate against float solvers.

Not part of the proof.  If a fine-mesh float solution ever fell outside a
rigorous box inflated by U_n, either that float solution is inaccurate or the
certificate is wrong; with the float meshes used here (errors ~1e-4 or better)
and U_n >= 3e-3, any such event would be a red flag for the verifier.
"""
import glob
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.models import AlleePredatorPrey          # noqa: E402
from msbg.provenance import RunRecorder            # noqa: E402
from msbg.solvers import METHODS, solve            # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    model = AlleePredatorPrey(theta=0.3, a=1.0, b=1.0, m=0.8)
    p = np.array([[2.4372, 2.012]])
    T, h = 4.0, 2e-4
    N = int(round(T / h))
    floats = {}
    for meth in METHODS:
        r = solve(model, p, 0.85, h, N, method=meth, store=True)
        floats[meth] = (r.t, r.x[:, 0, :])
        print(f"float {meth}: done", flush=True)
    rec = RunRecorder("t2_stageA_crosscheck", ROOT)
    rows = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "t2_stageA_certify_*_arrays.npz"))):
        d = np.load(f)
        tm, U = d["tm"], d["U"]
        lo_x, hi_x = d["x_lo"] - U, d["x_hi"] + U
        lo_y, hi_y = d["y_lo"] - U, d["y_hi"] + U
        worst = 0.0
        n_checked = 0
        outside = 0
        for meth, (t, x) in floats.items():
            cell = np.clip(np.searchsorted(tm, t, side="right") - 1, 0, len(tm) - 2)
            ex = np.maximum.reduce([lo_x[cell] - x[:, 0], x[:, 0] - hi_x[cell],
                                    lo_y[cell] - x[:, 1], x[:, 1] - hi_y[cell]])
            worst = max(worst, float(ex.max()))
            outside += int((ex > 0).sum())
            n_checked += len(t)
        tag = os.path.basename(f).replace("t2_stageA_certify_", "").replace("_arrays.npz", "")
        rows.append({"certificate": tag, "points_checked": n_checked,
                     "points_outside": outside, "worst_excess": worst})
        print(f"{tag:12} checked {n_checked} float points (3 solvers): outside={outside} "
              f"worst excess={worst:+.3e} (negative = inside)")
    rec.add("rows", rows)
    rec.add("all_inside", all(r["points_outside"] == 0 for r in rows))
    rec.add("evidence_class", "consistency check, not part of the proof")
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
