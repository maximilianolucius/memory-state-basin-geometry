#!/usr/bin/env python3
r"""TASK-0001 Stage D — falsification test of the CERTIFIED-CONDITIONAL extinction region.

The witness rests on the claim that every constant initial history in

    R_ext = {0 < x < theta, y >= 0}

converges to extinction, which follows from
  (a) invariance of the positive cone,
  (b) the scalar Caputo comparison principle (Wu 2020): since a x y >= 0,
        ^C D^a x <= x(1-x)(x-theta) =: f(x),  so  x(t) <= u(t),
      where ^C D^a u = f(u), u(0) = x(0),
  (c) COROLLARY-S1A (research/CLAIMS.md): u(0) in (0,theta) implies u(t) -> 0,
  (d) theta < m/b, which then forces y -> 0 by comparison with ^C D^a v = -(m - b theta) v.

None of (a)-(d) is proved here.  What IS done here is to try to FALSIFY the
consequences numerically:

  T1  no trajectory started in R_ext ever leaves the positive cone;
  T2  no trajectory started in R_ext is labelled anything but EXTINCTION;
  T3  the comparison inequality x(t) <= u(t) holds pointwise along every tested
      trajectory, where u is the scalar Allee solution from the same x(0);
  T4  u(t) itself never leaves (0, theta) - the barrier property;
  T5  y(t) <= y(0) E_a(-(m - b theta) t^a) pointwise, the predicted predator bound.

A single violation would kill the extinction half of the witness.
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.basins import Outcome, classify                       # noqa: E402
from msbg.mittag_leffler import e_alpha                         # noqa: E402
from msbg.models import AlleePredatorPrey, ScalarAllee          # noqa: E402
from msbg.provenance import RunRecorder                         # noqa: E402
from msbg.solvers import METHODS, solve                         # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--theta", type=float, default=0.3)
    ap.add_argument("--a", type=float, default=1.0)
    ap.add_argument("--b", type=float, default=1.0)
    ap.add_argument("--m", type=float, default=0.8)
    ap.add_argument("--alpha", type=float, default=0.85)
    ap.add_argument("--T", type=float, default=2000.0)
    ap.add_argument("--h", type=float, default=0.02)
    ap.add_argument("--nx", type=int, default=40)
    ap.add_argument("--ny", type=int, default=40)
    ap.add_argument("--ymax", type=float, default=5.0)
    args = ap.parse_args()
    np.seterr(all="ignore")

    rec = RunRecorder("stage_d_certified_region", ROOT)
    model = AlleePredatorPrey(theta=args.theta, a=args.a, b=args.b, m=args.m)
    scal = ScalarAllee(theta=args.theta)
    E = np.array([model.x_star, model.y_star])
    N = int(round(args.T / args.h))
    assert model.theta < model.x_star, "theta < m/b is required by ingredient (d)"

    xs = np.linspace(1e-4, args.theta * (1 - 1e-6), args.nx)
    ys = np.linspace(0.0, args.ymax, args.ny)
    XX, YY = np.meshgrid(xs, ys, indexing="ij")
    X0 = np.stack([XX.ravel(), YY.ravel()], axis=1)
    print(f"{len(X0)} constant histories in R_ext = (0,{args.theta}) x [0,{args.ymax}], "
          f"T={args.T}, h={args.h}, alpha={args.alpha}")

    r = solve(model, X0, args.alpha, args.h, N, method="pece", store=True,
              store_stride=max(1, N // 5000))
    tr, t = r.x, r.t
    ru = solve(scal, xs[:, None], args.alpha, args.h, N, method="pece", store=True,
               store_stride=max(1, N // 5000))
    u = ru.x[:, :, 0]                       # (K, nx)
    U = np.repeat(u, args.ny, axis=1)       # align with the (x,y) ravel order

    # T1 positivity
    minall = float(np.nanmin(tr))
    # T2 labels
    lab = classify(tr, E, r_coex=0.05, r_ext=0.05)
    counts = {Outcome.NAMES[k]: int((lab == k).sum()) for k in range(5)}
    # T3 comparison inequality
    viol = tr[:, :, 0] - U
    worst_cmp = float(np.nanmax(viol))
    n_viol = int((viol > 1e-8).any(axis=0).sum())
    # T4 barrier property of u
    u_in_band = bool(np.nanmin(u) > -1e-12 and np.nanmax(u) < args.theta + 1e-9)
    # T5 predator bound
    c = args.m - args.b * args.theta
    ml = np.array([float(e_alpha(args.alpha, -c * max(tv, 0.0) ** args.alpha, dps=20))
                   for tv in t])
    bound = X0[:, 1][None, :] * ml[:, None]
    yviol = tr[:, :, 1] - bound
    worst_y = float(np.nanmax(yviol))
    n_yviol = int((yviol > 1e-8).any(axis=0).sum())

    print(f"T1 positivity          : min over all trajectories = {minall:.3e}   "
          f"{'PASS' if minall > -1e-9 else 'FAIL'}")
    print(f"T2 labels              : {counts}   "
          f"{'PASS' if counts['EXTINCTION'] == len(X0) else 'FAIL'}")
    print(f"T3 x(t) <= u(t)        : worst excess = {worst_cmp:+.3e} over {n_viol} trajectories   "
          f"{'PASS' if n_viol == 0 else 'FAIL'}")
    print(f"T4 0 < u(t) < theta    : {'PASS' if u_in_band else 'FAIL'} "
          f"(min {np.nanmin(u):.3e}, max {np.nanmax(u):.6f})")
    print(f"T5 y(t) <= y0 E_a(-c t^a), c = m - b theta = {c}: worst excess = {worst_y:+.3e} "
          f"over {n_yviol} trajectories   {'PASS' if n_yviol == 0 else 'FAIL'}")

    rec.add("parameters", vars(args))
    rec.add("T1_positivity_min", minall)
    rec.add("T2_label_counts", counts)
    rec.add("T2_all_extinction", counts["EXTINCTION"] == len(X0))
    rec.add("T3_comparison_worst_excess", worst_cmp)
    rec.add("T3_n_violating_trajectories", n_viol)
    rec.add("T4_u_stays_in_0_theta", u_in_band)
    rec.add("T5_predator_bound_worst_excess", worst_y)
    rec.add("T5_n_violating_trajectories", n_yviol)
    rec.add("evidence_class",
            "NUMERICAL FALSIFICATION TEST of a CERTIFIED-CONDITIONAL claim; passing does not "
            "prove the claim, failing would refute it")
    rec.save_npz("region_check", X0=X0, labels=lab, t=t,
                 min_x=np.nanmin(tr[:, :, 0], axis=0), final=r.x_final)
    print("\nmanifest:", rec.finish())


if __name__ == "__main__":
    main()
