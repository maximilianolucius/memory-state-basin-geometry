#!/usr/bin/env python3
r"""TASK-0003 Stage C — orbits started inside the L1-certified ellipsoid Omega.

Two questions.

(1) Does any orbit started in Omega cross below x = theta?
    Structural answer (return report, section 1): NO, if L1 and X1 both hold.
    This script measures how close they come: the minimum over the orbit of
    (x(t) - theta) / (x* - theta), which is 1 at E* and 0 at the threshold.

(2) Numerical falsification test of the CONCLUSION of L1.  L1 asserts
    V(u(t)) <= V(u(0)) for every orbit started in Omega, with V = u^T P u.
    For a Caputo system this is not automatic from a pointwise inequality, so
    it is tested directly: sup_t V(u(t)) / V(u(0)) over orbits started on the
    boundary of 0.999 Omega, for several fractional orders.  A value above 1
    (beyond solver error) would refute the L1 conclusion numerically.

Initial states lie on the ellipse u^T P u = 0.998 * lam_min r_cert^2.
Two solvers (pece, pi_rect), two meshes.
Evidence class: NUMERICAL CORROBORATION / falsification test.
"""
import argparse
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.fastconv import solve_blocked               # noqa: E402
from msbg.lyapunov_l1 import l1_certificate          # noqa: E402
from msbg.models import AlleePredatorPrey            # noqa: E402
from msbg.provenance import RunRecorder              # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def one(job):
    np.seterr(all="ignore")
    th, a, b, m, alpha, T, h, method, n_ang = job
    c = l1_certificate(th, a, b, m)
    f = lambda q: float(Fraction(int(q.p), int(q.q)))
    P = np.array([[f(c.P[0][0]), f(c.P[0][1])], [f(c.P[1][0]), f(c.P[1][1])]])
    E = np.array([f(c.x_star), f(c.y_star)])
    level = 0.998 * float(c.level.lower())
    w, Vv = np.linalg.eigh(P)
    ang = np.linspace(0, 2 * np.pi, n_ang, endpoint=False)
    circ = np.stack([np.cos(ang), np.sin(ang)], axis=1)
    U0 = (circ * np.sqrt(level / w)[None, :]) @ Vv.T
    V0 = np.einsum("ij,jk,ik->i", U0, P, U0)
    model = AlleePredatorPrey(theta=float(Fraction(th)), a=float(Fraction(a)),
                              b=float(Fraction(b)), m=float(Fraction(m)))
    al = float(Fraction(alpha))
    N = int(round(T / h))
    r = solve_blocked(model, E[None, :] + U0, al, h, N, method=method, block=256, store=True,
                      store_stride=max(1, N // 4000))
    u = r.x - E[None, None, :]
    Vt = np.einsum("tij,jk,tik->ti", u, P, u)
    gap = E[0] - model.theta
    rel = (r.x[:, :, 0] - model.theta) / gap
    return {"theta": th, "a": a, "b": b, "m": m, "alpha": alpha, "method": method, "h": h,
            "T": T, "n_orbits": int(n_ang),
            "V0_over_level": float(np.max(V0) / float(c.level.lower())),
            "sup_V_ratio": float(np.max(Vt / V0[None, :])),
            "sup_V_ratio_after_t1": float(np.max(Vt[1:] / V0[None, :])),
            "final_V_ratio_max": float(np.max(Vt[-1] / V0)),
            "min_rel_distance_to_threshold": float(np.min(rel)),
            "max_abs_u1_over_gap": float(np.max(np.abs(u[:, :, 0])) / gap),
            "x_extent_over_gap": c.ratio_extent_gap,
            "crossed_threshold": bool(np.min(rel) < 0)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--T", type=float, default=400.0)
    ap.add_argument("--h", type=float, default=0.02)
    ap.add_argument("--n-ang", type=int, default=64)
    ap.add_argument("--top", type=int, default=8)
    args = ap.parse_args()
    scan = json.load(open(os.path.join(ROOT, "data", "t3_l1_scan_rows.json")))
    H = sorted([r for r in scan if r["hurwitz"]], key=lambda r: -r["extent_over_gap"])
    sets = [(r["theta"], r["a"], r["b"], r["m"]) for r in H[: args.top]]
    sets.append(("3/10", "1", "1", "4/5"))          # the TASK-0001 parameter set
    alphas = ["1/2", "7/10", "17/20", "19/20"]
    jobs = [(th, a, b, m, al, args.T, hh, meth, args.n_ang)
            for (th, a, b, m) in sets for al in alphas
            for meth in ("pece", "pi_rect") for hh in (args.h, args.h / 2)]
    print(f"jobs={len(jobs)} workers={args.workers}", flush=True)
    rec = RunRecorder("t3_stageC", ROOT)
    rows = []
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        for r in ex.map(one, jobs):
            rows.append(r)
    print(f"{'theta':>6}{'m':>8}{'a':>5}{'b':>5}{'alpha':>7}{'supV/V0':>10}{'min rel dist':>14}"
          f"{'max|u1|/gap':>13}{'crossed':>9}")
    for key in sorted({(r["theta"], r["m"], r["a"], r["b"], r["alpha"]) for r in rows}):
        g = [r for r in rows if (r["theta"], r["m"], r["a"], r["b"], r["alpha"]) == key]
        print(f"{key[0]:>6}{key[1]:>8}{key[2]:>5}{key[3]:>5}{key[4]:>7}"
              f"{max(r['sup_V_ratio'] for r in g):10.6f}"
              f"{min(r['min_rel_distance_to_threshold'] for r in g):14.6f}"
              f"{max(r['max_abs_u1_over_gap'] for r in g):13.6f}"
              f"{str(any(r['crossed_threshold'] for r in g)):>9}")
    print(f"\nany orbit from Omega crossed the threshold: {any(r['crossed_threshold'] for r in rows)}")
    print(f"max over everything of sup_t V(t)/V(0): {max(r['sup_V_ratio'] for r in rows):.8f}")
    print(f"closest approach to the threshold, in units of the gap: "
          f"{min(r['min_rel_distance_to_threshold'] for r in rows):.6f}")
    rec.save_json("rows", rows)
    rec.add("any_crossing", any(r["crossed_threshold"] for r in rows))
    rec.add("max_sup_V_ratio", max(r["sup_V_ratio"] for r in rows))
    rec.add("min_rel_distance", min(r["min_rel_distance_to_threshold"] for r in rows))
    rec.add("evidence_class", "NUMERICAL CORROBORATION / falsification test")
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
