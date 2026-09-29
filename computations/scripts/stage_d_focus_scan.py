#!/usr/bin/env python3
"""TASK-0001 Stage D, step 2 — focused scan, saving per-initial-condition diagnostics.

Unlike ``stage_d_regime_scan.py`` this script stores the *raw diagnostics* for
every initial condition (minimum prey value over the orbit, the time at which it
occurs, the tail distance to the coexistence point, the contraction ratio between
the last two windows, the tail norm), so that classification thresholds can be
varied afterwards without recomputing anything.

Evidence class: NUMERICAL CORROBORATION / CONJECTURE GENERATOR.
"""
from __future__ import annotations

import argparse
import os
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.models import AlleePredatorPrey, DoubleAlleePredatorPrey  # noqa: E402
from msbg.provenance import RunRecorder                             # noqa: E402
from msbg.solvers import solve                                      # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def diagnostics(cfg):
    np.seterr(all="ignore")
    family, theta, xstar, a, alpha, T, N, nx, ny, xmax, ymax = cfg
    cls = DoubleAlleePredatorPrey if family == "double" else AlleePredatorPrey
    model = cls(theta=theta, a=a, b=1.0, m=xstar)
    xs, ys = model.x_star, model.y_star
    E = np.array([xs, ys])
    x0 = np.linspace(theta + 1e-3, xmax, nx)
    y0 = np.linspace(0.02, ymax, ny)
    XX, YY = np.meshgrid(x0, y0, indexing="ij")
    X0 = np.stack([XX.ravel(), YY.ravel()], axis=1)
    r = solve(model, X0, alpha, T / N, N, method="pece", store=True, store_stride=2)
    tr = r.x
    K = tr.shape[0]
    k0, k1 = int(0.65 * K), int(0.30 * K)
    with np.errstate(all="ignore"):
        imin = np.nanargmin(np.where(np.isfinite(tr[:, :, 0]), tr[:, :, 0], np.inf), axis=0)
        minx = tr[imin, np.arange(tr.shape[1]), 0]
        tmin = r.t[imin]
        ymin = tr[imin, np.arange(tr.shape[1]), 1]
        dE = np.linalg.norm(tr - E, axis=2)
        nn = np.linalg.norm(tr, axis=2)
        tail_dE = np.nanmax(dE[k0:], axis=0)
        prev_dE = np.nanmax(dE[k1:k0], axis=0)
        tail_n = np.nanmax(nn[k0:], axis=0)
        prev_n = np.nanmax(nn[k1:k0], axis=0)
        finite = np.isfinite(tr).all(axis=0).all(axis=1)
        mx = np.nanmax(np.abs(tr), axis=(0, 2))
    return dict(
        family=family, theta=theta, xstar=xstar, a=a, alpha=alpha, T=T, N=N,
        E=E, X0=X0, minx=minx, tmin=tmin, ymin=ymin,
        tail_dE=tail_dE, prev_dE=prev_dE, tail_n=tail_n, prev_n=prev_n,
        finite=finite, maxabs=mx, x_final=r.x_final,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--T", type=float, default=800.0)
    ap.add_argument("--N", type=int, default=8000)
    ap.add_argument("--nx", type=int, default=40)
    ap.add_argument("--ny", type=int, default=40)
    ap.add_argument("--xmax", type=float, default=4.0)
    ap.add_argument("--ymax", type=float, default=6.0)
    args = ap.parse_args()

    regimes = [
        ("single", 0.2, 0.80, 2.0), ("single", 0.2, 0.80, 1.0), ("single", 0.2, 0.80, 0.5),
        ("single", 0.2, 0.70, 0.5), ("single", 0.3, 0.75, 1.0), ("single", 0.4, 0.80, 1.0),
        ("double", 0.2, 0.80, 0.5), ("double", 0.2, 0.80, 1.0),
    ]
    alphas = [0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
    cfgs = [
        (fam, th, xs, a, al, args.T, args.N, args.nx, args.ny, args.xmax, args.ymax)
        for (fam, th, xs, a) in regimes
        for al in alphas
    ]
    print(f"configs={len(cfgs)} workers={args.workers} grid={args.nx}x{args.ny} T={args.T} N={args.N}",
          flush=True)

    rec = RunRecorder("stage_d_focus", ROOT)
    summary, store = [], {}
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        for i, d in enumerate(ex.map(diagnostics, cfgs, chunksize=1)):
            key = f"{d['family']}_th{d['theta']}_xs{d['xstar']}_a{d['a']}_al{d['alpha']}"
            for name in ("X0", "minx", "tmin", "ymin", "tail_dE", "prev_dE",
                         "tail_n", "prev_n", "finite", "maxabs", "x_final", "E"):
                store[f"{key}__{name}"] = np.asarray(d[name])
            coex = (d["tail_dE"] < 0.05) & (d["tail_dE"] <= 0.7 * d["prev_dE"]) & d["finite"]
            sub = coex & (d["minx"] < d["theta"])
            marg = np.where(sub, d["theta"] - d["minx"], -np.inf)
            b = int(np.argmax(marg)) if np.isfinite(marg).any() else -1
            summary.append(dict(
                key=key, family=d["family"], theta=d["theta"], xstar=d["xstar"], a=d["a"],
                alpha=d["alpha"], n_ic=int(len(d["X0"])), n_coex=int(coex.sum()),
                n_sub=int(sub.sum()),
                best_margin=(float(marg[b]) if b >= 0 else None),
                best_ic=(d["X0"][b].tolist() if b >= 0 else None),
                best_minx=(float(d["minx"][b]) if b >= 0 else None),
                best_tmin=(float(d["tmin"][b]) if b >= 0 else None),
                best_ymin=(float(d["ymin"][b]) if b >= 0 else None),
                best_tail_dE=(float(d["tail_dE"][b]) if b >= 0 else None),
            ))
            print(f"  [{i+1}/{len(cfgs)}] {key}: n_coex={coex.sum()} n_sub={sub.sum()} "
                  f"margin={summary[-1]['best_margin']}", flush=True)

    hits = [s for s in summary if s["n_sub"] > 0]
    hits.sort(key=lambda s: -s["best_margin"])
    print(f"\nregimes with sub-threshold survivors: {len(hits)}/{len(summary)}")
    for s in hits[:20]:
        print(f"  {s['key']:44} nsub={s['n_sub']:4d} margin={s['best_margin']:+.5f} "
              f"minx={s['best_minx']:.5f} t={s['best_tmin']:.2f} y={s['best_ymin']:.5f} "
              f"IC={s['best_ic']}")
    rec.save_npz("diagnostics", **store)
    rec.save_json("summary", summary)
    rec.add("n_regimes", len(summary))
    rec.add("n_regimes_with_witness_candidate", len(hits))
    rec.add("classifier_thresholds", {"tail_dE": 0.05, "contraction": 0.7, "window": "last 35%"})
    rec.add("evidence_class", "NUMERICAL CORROBORATION / CONJECTURE GENERATOR")
    print("\nmanifest:", rec.finish())


if __name__ == "__main__":
    main()
