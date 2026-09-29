#!/usr/bin/env python3
r"""TASK-0001 Stage D, step 3 — mesh-validated two-phase witness search.

Why a v2
--------
``stage_d_focus_scan.py`` used h = T/N = 0.1, which is far too coarse for
initial states well above the carrying capacity: the cubic term makes the first
steps violent and the explicit product-integration schemes overshoot through
x = 0.  Those runs reported spectacular "margins" (up to 3.35) that are pure
discretisation artefacts - every one of them has ``min x < 0``, i.e. it leaves
the positive cone, which the model forbids.  A direct mesh ladder on the best
candidate showed min x moving from 0.118 (h = 0.1) to 0.369 (h <= 0.02), so the
coarse-mesh margin was wrong by an order of magnitude.

v2 therefore
  * uses h = 0.01 in the transient phase;
  * hard-rejects any trajectory that leaves the positive cone;
  * separates dip detection (phase 1, short horizon, fine mesh) from survival
    confirmation (phase 2, long horizon, candidates only);
  * reports the mesh-refinement difference for every surviving candidate.

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
POS_TOL = 1e-9


def make(family, theta, a, b, m):
    cls = DoubleAlleePredatorPrey if family == "double" else AlleePredatorPrey
    return cls(theta=theta, a=a, b=b, m=m)


def phase1(cfg):
    """Fine-mesh short-horizon dip detection over a grid, positivity enforced."""
    np.seterr(all="ignore")
    family, theta, xstar, a, alpha, T1, h1, nx, ny, xmax, ymax = cfg
    model = make(family, theta, a, 1.0, xstar)
    if not (theta < model.x_star < 1.0) or model.y_star <= 0:
        return None
    N = int(round(T1 / h1))
    x0 = np.linspace(theta + 1e-3, xmax, nx)
    y0 = np.linspace(0.02, ymax, ny)
    XX, YY = np.meshgrid(x0, y0, indexing="ij")
    X0 = np.stack([XX.ravel(), YY.ravel()], axis=1)
    r = solve(model, X0, alpha, h1, N, method="pece", store=True, store_stride=1)
    tr = r.x
    finite = np.isfinite(tr).all(axis=0).all(axis=1)
    minall = np.nanmin(tr, axis=(0, 2))
    positive = finite & (minall > -POS_TOL)
    i = np.nanargmin(np.where(np.isfinite(tr[:, :, 0]), tr[:, :, 0], np.inf), axis=0)
    j = np.arange(tr.shape[1])
    minx, tmin, ymin = tr[i, j, 0], r.t[i], tr[i, j, 1]
    dips = positive & (minx < theta)
    # An extinction-bound orbit dips below theta and stays there, so ranking the
    # dips by depth would select precisely the trajectories that are NOT wanted.
    # The candidate set is therefore restricted to orbits that have already
    # RECOVERED above theta by the end of the short horizon; only those can be
    # survivors.
    recovered = dips & (r.x_final[:, 0] > theta) & (r.x_final[:, 1] > 0.0)
    return dict(family=family, theta=theta, xstar=xstar, a=a, alpha=alpha,
                T1=T1, h1=h1, X0=X0, minx=minx, tmin=tmin, ymin=ymin,
                positive=positive, dips=dips, cand=recovered, x_end_phase1=r.x_final)


def phase2(job):
    """Long-horizon survival confirmation for one candidate, plus a mesh check."""
    np.seterr(all="ignore")
    family, theta, xstar, a, alpha, p, T2, h2 = job
    model = make(family, theta, a, 1.0, xstar)
    E = np.array([model.x_star, model.y_star])
    out = {}
    for tag, hh in (("h", h2), ("h_half", h2 / 2)):
        N = int(round(T2 / hh))
        r = solve(model, np.atleast_2d(p), alpha, hh, N, method="pece", store=True,
                  store_stride=max(1, N // 8000))
        x = r.x[:, 0, :]
        if not np.isfinite(x).all() or np.nanmin(x) < -POS_TOL:
            out[tag] = {"invalid": True, "min": float(np.nanmin(x))}
            continue
        dE = np.linalg.norm(x - E, axis=1)
        K = len(dE)
        k0, k1 = int(0.65 * K), int(0.30 * K)
        i = int(np.argmin(x[:, 0]))
        out[tag] = {
            "invalid": False, "minx": float(x[i, 0]), "tmin": float(r.t[i]),
            "ymin": float(x[i, 1]), "margin": float(theta - x[i, 0]),
            "tail_dE": float(np.nanmax(dE[k0:])), "prev_dE": float(np.nanmax(dE[k1:k0])),
            "dist_final": float(dE[-1]), "final": x[-1].tolist(),
            "min_x_overall": float(np.nanmin(x[:, 0])), "min_y_overall": float(np.nanmin(x[:, 1])),
        }
    a_, b_ = out.get("h", {}), out.get("h_half", {})
    ok = (not a_.get("invalid", True)) and (not b_.get("invalid", True))
    surviving = ok and b_["tail_dE"] < 0.05 and b_["tail_dE"] <= 0.7 * b_["prev_dE"]
    return {
        "family": family, "theta": theta, "xstar": xstar, "a": a, "alpha": alpha,
        "p": list(map(float, p)), "T2": T2, "h2": h2, "detail": out,
        "mesh_diff_minx": (abs(a_["minx"] - b_["minx"]) if ok else None),
        "margin": (b_["margin"] if ok else None),
        "survival_label": bool(surviving),
        "witness": bool(surviving and ok and b_["margin"] > 0),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--T1", type=float, default=120.0)
    ap.add_argument("--h1", type=float, default=0.01)
    ap.add_argument("--T2", type=float, default=2000.0)
    ap.add_argument("--h2", type=float, default=0.04)
    ap.add_argument("--nx", type=int, default=36)
    ap.add_argument("--ny", type=int, default=36)
    ap.add_argument("--xmax", type=float, default=2.5)
    ap.add_argument("--ymax", type=float, default=5.0)
    ap.add_argument("--per-config", type=int, default=6)
    args = ap.parse_args()

    regimes = [("single", th, xs, a)
               for (th, xs) in ((0.3, 0.80), (0.4, 0.80), (0.4, 0.90), (0.5, 0.85), (0.5, 0.95))
               for a in (0.5, 1.0, 2.0)]
    regimes += [("double", th, xs, a)
                for (th, xs) in ((0.3, 0.80), (0.4, 0.80)) for a in (1.0,)]
    alphas = [0.55, 0.65, 0.75, 0.85, 0.92]
    cfgs = [(f, th, xs, a, al, args.T1, args.h1, args.nx, args.ny, args.xmax, args.ymax)
            for (f, th, xs, a) in regimes for al in alphas]
    print(f"phase1 configs={len(cfgs)} grid={args.nx}x{args.ny} h1={args.h1} T1={args.T1}",
          flush=True)

    rec = RunRecorder("stage_d_scan_v2", ROOT)
    jobs, p1summary, store = [], [], {}
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        for i, d in enumerate(ex.map(phase1, cfgs, chunksize=1)):
            if d is None:
                continue
            key = f"{d['family']}_th{d['theta']}_xs{d['xstar']}_a{d['a']}_al{d['alpha']}"
            for nm in ("X0", "minx", "tmin", "ymin", "positive", "dips", "cand",
                       "x_end_phase1"):
                store[f"{key}__{nm}"] = np.asarray(d[nm])
            nc = int(d["cand"].sum())
            p1summary.append({"key": key, "n_ic": int(len(d["X0"])),
                              "n_positive": int(d["positive"].sum()),
                              "n_dips_below_theta": int(d["dips"].sum()),
                              "n_recovered_candidates": nc})
            if nc:
                marg = np.where(d["cand"], d["theta"] - d["minx"], -np.inf)
                for k in np.argsort(-marg)[: args.per_config]:
                    jobs.append((d["family"], d["theta"], d["xstar"], d["a"], d["alpha"],
                                 d["X0"][k], args.T2, args.h2))
            print(f"  [{i+1}/{len(cfgs)}] {key}: positive={d['positive'].sum()}/{len(d['X0'])} "
                  f"dips={int(d['dips'].sum())} recovered={nc}", flush=True)

    print(f"\nphase2 candidate trajectories: {len(jobs)} (T2={args.T2}, h2={args.h2})", flush=True)
    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        for i, r in enumerate(ex.map(phase2, jobs, chunksize=1)):
            results.append(r)
            if (i + 1) % 20 == 0:
                print(f"  phase2 {i+1}/{len(jobs)}", flush=True)

    wit = [r for r in results if r["witness"]]
    wit.sort(key=lambda r: -r["margin"])
    print(f"\nMESH-VALIDATED, POSITIVITY-RESPECTING WITNESSES: {len(wit)}/{len(results)}")
    print(f"{'family':7}{'theta':>6}{'x*':>6}{'a':>5}{'alpha':>6}{'margin':>10}{'minx':>10}"
          f"{'meshdiff':>11}{'distE*':>10}  p")
    for r in wit[:30]:
        d = r["detail"]["h_half"]
        print(f"{r['family']:7}{r['theta']:6}{r['xstar']:6}{r['a']:5}{r['alpha']:6}"
              f"{r['margin']:10.5f}{d['minx']:10.5f}{r['mesh_diff_minx']:11.2e}"
              f"{d['dist_final']:10.2e}  {np.round(r['p'],5).tolist()}")
    rec.save_npz("phase1_diagnostics", **store)
    rec.save_json("phase1_summary", p1summary)
    rec.save_json("phase2_results", results)
    rec.add("n_phase2", len(results))
    rec.add("n_witnesses", len(wit))
    rec.add("best_witnesses", wit[:15])
    rec.add("positivity_tolerance", POS_TOL)
    rec.add("evidence_class", "NUMERICAL CORROBORATION / CONJECTURE GENERATOR")
    print("\nmanifest:", rec.finish())


if __name__ == "__main__":
    main()
