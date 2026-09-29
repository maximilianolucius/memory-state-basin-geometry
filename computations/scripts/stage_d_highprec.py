#!/usr/bin/env python3
r"""TASK-0001 Stage D — arbitrary-precision recomputation of the witness dip.

Why this is a separate script
-----------------------------
The high-precision check embedded in ``stage_d_witness.py`` (D4) was run at
``T = 200, N = 2000``, i.e. ``h = 0.1``.  Stage C's mesh study already showed
that step is outside the admissible range for this model, and indeed at that
step BOTH the mpmath and the float64 solution go extinct (they agree to
2.3e-10 with each other, and are qualitatively wrong).  That comparison
therefore only establishes that the two arithmetics agree on a bad mesh.

This script redoes the check on an admissible mesh: the horizon is cut to just
past the dip, so ``h = 0.01`` is affordable in mpmath's O(N^2) history sum.

It answers: is the sub-threshold dip a float64 artefact?
Evidence class: NUMERICAL CORROBORATION at 30 significant digits.
"""
from __future__ import annotations

import argparse
import os
import sys

import mpmath as mp
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.models import AlleePredatorPrey, DoubleAlleePredatorPrey  # noqa: E402
from msbg.provenance import RunRecorder                             # noqa: E402
from msbg.solvers import solve, solve_mp                            # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", default="single")
    ap.add_argument("--theta", type=float, default=0.3)
    ap.add_argument("--a", type=float, default=1.0)
    ap.add_argument("--b", type=float, default=1.0)
    ap.add_argument("--m", type=float, default=0.8)
    ap.add_argument("--alpha", type=float, default=0.85)
    ap.add_argument("--p", type=float, nargs=2, required=True)
    ap.add_argument("--T", type=float, default=50.0)
    ap.add_argument("--N", type=int, default=5000)
    ap.add_argument("--dps", type=int, default=30)
    args = ap.parse_args()
    np.seterr(all="ignore")

    rec = RunRecorder("stage_d_highprec", ROOT)
    cls = DoubleAlleePredatorPrey if args.family == "double" else AlleePredatorPrey
    model = cls(theta=args.theta, a=args.a, b=args.b, m=args.m)
    p = np.array(args.p, float)
    h = args.T / args.N
    print(f"p={p} alpha={args.alpha} T={args.T} N={args.N} h={h} dps={args.dps}", flush=True)

    traj = solve_mp(model.g_mp, [mp.mpf(str(p[0])), mp.mpf(str(p[1]))], args.alpha,
                    mp.mpf(str(args.T)) / args.N, args.N, dps=args.dps, method="pece")
    xs_mp = [row[0] for row in traj]
    ys_mp = [row[1] for row in traj]
    i = int(np.argmin([float(v) for v in xs_mp]))
    t_mp = i * h

    r = solve(model, np.atleast_2d(p), args.alpha, h, args.N, method="pece", store=True)
    x64 = r.x[:, 0, :]
    j = int(np.argmin(x64[:, 0]))

    minx_mp = float(xs_mp[i])
    print(f"mpmath  dps={args.dps}: min x = {mp.nstr(xs_mp[i], 20)} at t = {t_mp:.4f}, "
          f"y = {mp.nstr(ys_mp[i], 12)}")
    print(f"float64 same mesh  : min x = {x64[j, 0]:.20f} at t = {r.t[j]:.4f}")
    print(f"|difference|       : {abs(minx_mp - x64[j, 0]):.3e}")
    print(f"margin theta - min x: mpmath {model.theta - minx_mp:+.12f}, "
          f"float64 {model.theta - x64[j, 0]:+.12f}")
    print(f"min y over the run : mpmath {float(min(ys_mp)):.6e}, "
          f"float64 {x64[:, 1].min():.6e}  (positivity)")

    rec.add("model", {"theta": model.theta, "a": model.a, "b": model.b, "m": model.m,
                      "alpha": args.alpha, "provenance": model.provenance})
    rec.add("p", p.tolist())
    rec.add("mesh", {"T": args.T, "N": args.N, "h": h})
    rec.add("mpmath", {"dps": args.dps, "min_x": str(mp.nstr(xs_mp[i], 25)),
                       "t_min": t_mp, "y_at_min": str(mp.nstr(ys_mp[i], 20)),
                       "margin": str(mp.nstr(model.theta - xs_mp[i], 20)),
                       "min_y": str(mp.nstr(min(ys_mp), 12))})
    rec.add("float64", {"min_x": float(x64[j, 0]), "t_min": float(r.t[j]),
                        "margin": float(model.theta - x64[j, 0]),
                        "min_y": float(x64[:, 1].min())})
    rec.add("abs_difference_min_x", abs(minx_mp - x64[j, 0]))
    rec.add("dip_is_not_a_float64_artefact", bool(model.theta - minx_mp > 0))
    rec.add("evidence_class", "NUMERICAL CORROBORATION at 30 significant digits")
    print("\nmanifest:", rec.finish())


if __name__ == "__main__":
    main()
