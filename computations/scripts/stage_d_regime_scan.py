#!/usr/bin/env python3
"""TASK-0001 Stage D, step 1 — regime scan for a sub-threshold survival witness.

Question
--------
Does the positive planar strong-Allee Caputo system admit a trajectory from a
*constant* initial history that (i) enters the CERTIFIED-CONDITIONAL extinction
region ``{0 <= x < theta}`` at some finite time and (ii) nevertheless converges
to the coexistence attractor?

Such a trajectory is exactly an ``embedded_age`` inter-basin collision
(s = 0, q = x(t;p)), hence a multibasin reachable present-state fibre by
REDUCTION-M1 - with the extinction side CERTIFIED-CONDITIONAL and the survival
side NUMERICAL.

This script only *locates a regime*; the witness itself is validated by
``stage_d_witness.py``.  Evidence class: CONJECTURE GENERATOR.
"""
from __future__ import annotations

import argparse
import itertools
import os
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.basins import Outcome, classify                      # noqa: E402
from msbg.models import AlleePredatorPrey, DoubleAlleePredatorPrey  # noqa: E402
from msbg.provenance import RunRecorder                        # noqa: E402
from msbg.solvers import solve                                 # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ic_grid(nx=30, ny=34, xmax=1.5, ymax=8.0, theta=0.2):
    """Constant initial histories with x0 > theta (outside the certified region)."""
    x0 = np.linspace(theta + 1e-3, xmax, nx)
    y0 = np.linspace(0.02, ymax, ny)
    XX, YY = np.meshgrid(x0, y0, indexing="ij")
    return np.stack([XX.ravel(), YY.ravel()], axis=1)


def run_config(cfg):
    np.seterr(all="ignore")
    family, theta, xstar, a, alpha, T, N = cfg
    cls = DoubleAlleePredatorPrey if family == "double" else AlleePredatorPrey
    model = cls(theta=theta, a=a, b=1.0, m=xstar)
    xs, ys = model.x_star, model.y_star
    if not (theta < xs < 1.0) or ys <= 0:
        return None
    E = np.array([xs, ys])
    X0 = ic_grid(theta=theta)
    r = solve(model, X0, alpha, T / N, N, method="pece", store=True, store_stride=2)
    traj = r.x
    lab = classify(traj, E, r_coex=0.02, r_ext=0.02)
    with np.errstate(all="ignore"):
        minx = np.nanmin(traj[:, :, 0], axis=0)
    coex = lab == Outcome.COEXISTENCE
    sub = coex & (minx < theta)
    margin = np.where(sub, theta - minx, -np.inf)
    best = int(np.argmax(margin)) if np.isfinite(margin).any() else -1
    return {
        "family": family,
        "theta": theta,
        "xstar": xstar,
        "a": a,
        "alpha": alpha,
        "T": T,
        "N": N,
        "n_ic": int(len(X0)),
        "n_coex": int(coex.sum()),
        "n_ext": int((lab == Outcome.EXTINCTION).sum()),
        "n_ambig": int((lab == Outcome.AMBIGUOUS).sum()),
        "n_div": int((lab == Outcome.DIVERGENT).sum()),
        "n_neg": int((lab == Outcome.NEGATIVE).sum()),
        "n_subthreshold_survivors": int(sub.sum()),
        "best_margin": float(margin[best]) if best >= 0 else None,
        "best_ic": X0[best].tolist() if best >= 0 else None,
        "best_minx": float(minx[best]) if best >= 0 else None,
        "min_coex_minx": float(minx[coex].min()) if coex.any() else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=min(64, os.cpu_count() or 8))
    ap.add_argument("--T", type=float, default=400.0)
    ap.add_argument("--N", type=int, default=4000)
    args = ap.parse_args()

    thetas_xstar = [
        (0.2, 0.70), (0.2, 0.80), (0.3, 0.75), (0.3, 0.85),
        (0.4, 0.80), (0.4, 0.90), (0.5, 0.85), (0.5, 0.95),
    ]
    alphas = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.97]
    aa = [0.5, 1.0, 2.0]
    cfgs = [
        (fam, th, xs, a, al, args.T, args.N)
        for fam in ("single", "double")
        for (th, xs) in thetas_xstar
        for a in aa
        for al in alphas
    ]
    print(f"configs={len(cfgs)} workers={args.workers}", flush=True)

    rec = RunRecorder("stage_d_regime_scan", ROOT)
    rows = []
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        for i, res in enumerate(ex.map(run_config, cfgs, chunksize=1)):
            if res is not None:
                rows.append(res)
            if (i + 1) % 50 == 0:
                print(f"  {i+1}/{len(cfgs)}", flush=True)

    hits = [r for r in rows if r["n_subthreshold_survivors"] > 0]
    hits.sort(key=lambda r: -r["best_margin"])
    print(f"\nconfigs with sub-threshold survivors: {len(hits)}/{len(rows)}")
    print(f"{'fam':7}{'theta':>6}{'x*':>6}{'a':>5}{'alpha':>6}{'nsub':>6}{'margin':>10}  best_ic")
    for r in hits[:30]:
        print(
            f"{r['family']:7}{r['theta']:6}{r['xstar']:6}{r['a']:5}{r['alpha']:6}"
            f"{r['n_subthreshold_survivors']:6d}{r['best_margin']:10.5f}  {r['best_ic']}"
        )
    rec.add("n_configs", len(rows))
    rec.add("n_configs_with_subthreshold_survivor", len(hits))
    rec.add("top_hits", hits[:40])
    rec.add("evidence_class", "CONJECTURE GENERATOR (floating-point regime scan)")
    rec.save_json("rows", rows)
    print("\nmanifest:", rec.finish())


if __name__ == "__main__":
    main()
