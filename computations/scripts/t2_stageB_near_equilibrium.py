#!/usr/bin/env python3
r"""TASK-0002 Stage B — witnesses close to the coexistence equilibrium.

Goal (Chief request, Stage B)
-----------------------------
Find initial constant histories ``p`` whose orbit
  1. enters ``R_ext = {0 < x < theta, y >= 0}`` with a strict margin, and
  2. converges to the coexistence equilibrium ``E*``,
with ``||p - E*||`` as small as possible.  A witness close to ``E*`` is the one a
local-basin theorem can plausibly certify.

Why such witnesses can exist
----------------------------
For ``0 < alpha < 1`` the Caputo stability condition is ``|arg lambda| > alpha pi/2``,
which admits eigenvalues with *positive* real part.  So ``E*`` can sit close to
the Allee threshold (``x* - theta`` small) and still be locally attracting, with
large, slowly damped oscillations.  That is the regime scanned here: the scan is
parameterised by the gap ``x* - theta`` and by ``alpha``.

Method
------
Phase 1 (per parameter set, one worker each): a polar grid of initial states
around ``E*``, radii geometric in ``[r_min, r_max]``; PECE at ``h = 0.01`` to
``T1``; positivity is a hard filter; record depth below ``theta``, recovery above
``theta`` by ``T1``, and the tail distance to ``E*``.

Phase 2 (per candidate, one worker each): long horizon ``T2``, three solvers,
two meshes; a candidate is a witness only if all six runs agree that it enters
``R_ext`` with positive margin and ends contracting towards ``E*``.

The Pareto frontier over (``||p - E*||`` down, margin up) is then extracted.

Evidence class: NUMERICAL CORROBORATION / CONJECTURE GENERATOR.  Local linear
stability of ``E*`` is reported as a fact about the linearisation only; it is
NOT a basin proof.
"""
from __future__ import annotations

import argparse
import os
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.models import AlleePredatorPrey          # noqa: E402
from msbg.provenance import RunRecorder            # noqa: E402
from msbg.fastconv import solve_blocked            # noqa: E402
from msbg.solvers import METHODS, solve            # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POS_TOL = 1e-12


def caputo_spectrum(model):
    """Linearisation at E*: eigenvalues and the Caputo stability margin."""
    E = np.array([[model.x_star, model.y_star]])
    lam = np.linalg.eigvals(model.jac(E)[0])
    return lam, float(np.min(np.abs(np.angle(lam))))


def phase1(cfg):
    np.seterr(all="ignore")
    theta, gap, a, alpha, T1, h, n_r, n_ang, r_min, r_max = cfg
    xstar = theta + gap
    if not (0 < theta < xstar < 1):
        return None
    model = AlleePredatorPrey(theta=theta, a=a, b=1.0, m=xstar)
    lam, minarg = caputo_spectrum(model)
    stable = minarg > alpha * np.pi / 2
    if not stable:
        return {"theta": theta, "gap": gap, "a": a, "alpha": alpha, "stable": False,
                "eig": [[float(l.real), float(l.imag)] for l in lam]}
    E = np.array([model.x_star, model.y_star])
    radii = np.geomspace(r_min, r_max, n_r)
    ang = np.linspace(0, 2 * np.pi, n_ang, endpoint=False)
    R, A = np.meshgrid(radii, ang, indexing="ij")
    X0 = np.stack([E[0] + R.ravel() * np.cos(A.ravel()),
                   E[1] + R.ravel() * np.sin(A.ravel())], axis=1)
    keep = (X0[:, 0] > 0) & (X0[:, 1] > 0)
    X0 = X0[keep]
    N = int(round(T1 / h))
    # blocked history convolution: same PECE arithmetic, BLAS-3 far history
    r = solve_blocked(model, X0, alpha, h, N, method="pece", block=256, store=True,
                      store_stride=2)
    tr = r.x
    finite = np.isfinite(tr).all(axis=0).all(axis=1)
    mins = np.where(finite, np.nanmin(tr, axis=(0, 2)), -np.inf)
    positive = finite & (mins > POS_TOL)
    i = np.nanargmin(np.where(np.isfinite(tr[:, :, 0]), tr[:, :, 0], np.inf), axis=0)
    jj = np.arange(tr.shape[1])
    minx, tmin = tr[i, jj, 0], r.t[i]
    K = tr.shape[0]
    k0, k1 = int(0.7 * K), int(0.4 * K)
    dE = np.linalg.norm(tr - E, axis=2)
    tail = np.nanmax(dE[k0:], axis=0)
    prev = np.nanmax(dE[k1:k0], axis=0)
    recovered = positive & (minx < theta) & (r.x_final[:, 0] > theta)
    contracting = tail < 0.9 * prev
    cand = recovered & contracting
    return {
        "theta": theta, "gap": gap, "a": a, "alpha": alpha, "stable": True,
        "xstar": float(E[0]), "ystar": float(E[1]),
        "eig": [[float(l.real), float(l.imag)] for l in lam],
        "caputo_margin_rad": float(minarg - alpha * np.pi / 2),
        "n_ic": int(len(X0)), "n_positive": int(positive.sum()),
        "n_candidates": int(cand.sum()),
        "X0": X0[cand].tolist(),
        "dist_p_E": np.linalg.norm(X0[cand] - E, axis=1).tolist(),
        "margin": (theta - minx[cand]).tolist(),
        "tmin": tmin[cand].tolist(),
        "min_pos": mins[cand].tolist(),
        "tail_dE": tail[cand].tolist(),
    }


def phase2(job):
    """Six-run confirmation: three solvers x two meshes, long horizon."""
    np.seterr(all="ignore")
    theta, gap, a, alpha, p, T2, h2 = job
    model = AlleePredatorPrey(theta=theta, a=a, b=1.0, m=theta + gap)
    E = np.array([model.x_star, model.y_star])
    runs = {}
    for method in METHODS:
        for hh in (h2, h2 / 2):
            N = int(round(T2 / hh))
            r = solve(model, np.atleast_2d(p), alpha, hh, N, method=method, store=True,
                      store_stride=max(1, N // 6000))
            x = r.x[:, 0, :]
            ok = bool(np.isfinite(x).all() and np.nanmin(x) > POS_TOL)
            dE = np.linalg.norm(x - E, axis=1)
            K = len(dE)
            t = r.t
            k0 = int(0.5 * K)
            tt, dd = t[k0:], dE[k0:]
            good = (tt > 0) & (dd > 0)
            expo = (float(np.polyfit(np.log(tt[good]), np.log(dd[good]), 1)[0])
                    if good.sum() > 10 else None)
            runs[f"{method}_h{hh}"] = {
                "valid": ok,
                "minx": float(np.nanmin(x[:, 0])) if ok else None,
                "margin": float(theta - np.nanmin(x[:, 0])) if ok else None,
                "min_pos": float(np.nanmin(x)) if ok else None,
                "dist_final": float(dE[-1]) if ok else None,
                "tail_max_last_quarter": float(np.nanmax(dE[int(0.75 * K):])) if ok else None,
                "tail_max_prev_quarter": float(np.nanmax(dE[int(0.5 * K):int(0.75 * K)]))
                if ok else None,
                "decay_exponent": expo,
            }
    vals = list(runs.values())
    all_valid = all(v["valid"] for v in vals)
    witness = all_valid and all(
        v["margin"] > 0 and v["tail_max_last_quarter"] < v["tail_max_prev_quarter"]
        for v in vals)
    margins = [v["margin"] for v in vals if v["valid"]]
    return {
        "theta": theta, "gap": gap, "a": a, "alpha": alpha, "p": list(map(float, p)),
        "dist_p_E": float(np.linalg.norm(np.asarray(p) - E)),
        "E_star": E.tolist(), "T2": T2, "h2": h2, "runs": runs,
        "witness": bool(witness),
        "margin_min": min(margins) if margins else None,
        "margin_spread": (max(margins) - min(margins)) if margins else None,
        "dist_final_max": max(v["dist_final"] for v in vals) if all_valid else None,
        "min_pos_min": min(v["min_pos"] for v in vals) if all_valid else None,
    }


def pareto(rows):
    """Non-dominated set for (dist_p_E minimise, margin_min maximise)."""
    rows = sorted(rows, key=lambda r: (r["dist_p_E"], -r["margin_min"]))
    front, best = [], -np.inf
    for r in rows:
        if r["margin_min"] > best:
            front.append(r)
            best = r["margin_min"]
    return front


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=330)
    ap.add_argument("--T1", type=float, default=200.0)
    ap.add_argument("--h", type=float, default=0.01)
    ap.add_argument("--T2", type=float, default=4000.0)
    ap.add_argument("--h2", type=float, default=0.02)
    ap.add_argument("--n-r", type=int, default=30)
    ap.add_argument("--n-ang", type=int, default=36)
    ap.add_argument("--r-min", type=float, default=0.01)
    ap.add_argument("--r-max", type=float, default=2.0)
    ap.add_argument("--per-config", type=int, default=4)
    args = ap.parse_args()

    thetas = [0.2, 0.3, 0.4, 0.5, 0.6]
    gaps = [0.03, 0.06, 0.1, 0.15, 0.2, 0.3]
    aa = [0.5, 1.0, 2.0]
    alphas = [0.55, 0.65, 0.75, 0.85, 0.92]
    cfgs = [(th, g, a, al, args.T1, args.h, args.n_r, args.n_ang, args.r_min, args.r_max)
            for th in thetas for g in gaps for a in aa for al in alphas]
    print(f"phase1 configs={len(cfgs)} workers={args.workers} ICs/config<={args.n_r*args.n_ang} "
          f"T1={args.T1} h={args.h}", flush=True)

    rec = RunRecorder("t2_stageB", ROOT)
    p1, jobs = [], []
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        for i, d in enumerate(ex.map(phase1, cfgs, chunksize=1)):
            if d is None:
                continue
            p1.append({k: v for k, v in d.items()
                       if k not in ("X0", "dist_p_E", "margin", "tmin", "min_pos", "tail_dE")})
            if d.get("stable") and d["n_candidates"]:
                order = np.argsort(d["dist_p_E"])
                taken = 0
                for k in order:
                    if d["margin"][k] <= 0:
                        continue
                    jobs.append((d["theta"], d["gap"], d["a"], d["alpha"], d["X0"][k],
                                 args.T2, args.h2))
                    taken += 1
                    if taken >= args.per_config:
                        break
            if (i + 1) % 25 == 0:
                print(f"  phase1 {i+1}/{len(cfgs)}  candidates so far: {len(jobs)}", flush=True)
    n_stable = sum(1 for r in p1 if r.get("stable"))
    print(f"\nphase1 done: {n_stable} Caputo-stable parameter sets, "
          f"{len(jobs)} near-equilibrium candidates to confirm", flush=True)

    res = []
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        for i, r in enumerate(ex.map(phase2, jobs, chunksize=1)):
            res.append(r)
            if (i + 1) % 50 == 0:
                print(f"  phase2 {i+1}/{len(jobs)}", flush=True)
    wit = [r for r in res if r["witness"]]
    front = pareto(wit)
    print(f"\nCONFIRMED WITNESSES (3 solvers x 2 meshes agree): {len(wit)}/{len(res)}")
    print("PARETO FRONT  (||p-E*|| minimised, margin maximised):")
    print(f"{'theta':>6}{'gap':>6}{'a':>5}{'alpha':>6}{'|p-E*|':>9}{'margin':>9}"
          f"{'spread':>9}{'distE(T)':>10}{'minpos':>9}  p")
    for r in front:
        print(f"{r['theta']:6}{r['gap']:6}{r['a']:5}{r['alpha']:6}{r['dist_p_E']:9.4f}"
              f"{r['margin_min']:9.5f}{r['margin_spread']:9.1e}{r['dist_final_max']:10.2e}"
              f"{r['min_pos_min']:9.2e}  {np.round(r['p'], 5).tolist()}")
    rec.save_json("phase1", p1)
    rec.save_json("phase2", res)
    rec.save_json("pareto", front)
    rec.add("n_configs", len(cfgs))
    rec.add("n_caputo_stable", n_stable)
    rec.add("n_candidates", len(jobs))
    rec.add("n_confirmed_witnesses", len(wit))
    rec.add("pareto_front", front)
    rec.add("evidence_class", "NUMERICAL CORROBORATION / CONJECTURE GENERATOR")
    print("\nmanifest:", rec.finish())


if __name__ == "__main__":
    main()
