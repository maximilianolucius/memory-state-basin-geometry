#!/usr/bin/env python3
r"""TASK-0002 Stage C — continuation-state proximity to the equilibrium lift.

For a standard initial state p the Doan-Kloeden continuation state at time T is
the function of tau >= 0

    C_T(tau) := T_T iota(p)(tau) = p + (1/Gamma(a)) int_0^T (T + tau - s)^{a-1} g(x(s)) ds .

C_T(0) = x(T).  For tau > 0 it is the memory-only forecast: where the solution
would go if the vector field were switched off after time T.  The equilibrium
lift is the constant function iota(E*) == E*.  In the compact-open topology of
C(R_+, R^2), T_T iota(p) -> iota(E*) iff, for every fixed R,

    D(T, R) := sup_{tau in [0, R]} || C_T(tau) - E* ||  ->  0   as  T -> infinity.

This script evaluates D(T, R) on a grid of T and R.  The integrand g(x(s)) is
replaced by the continuous piecewise-linear interpolant of its nodal values
and integrated EXACTLY against the shifted kernel cell by cell:

    int_{t_j}^{t_{j+1}} (t - s)^{a-1} [phi_j + m_j (s - t_j)] ds
      = (phi_j + m_j (t - t_j)) (A^a - B^a)/a - m_j (A^{a+1} - B^{a+1})/(a+1),
    A = t - t_j,  B = t - t_{j+1},  t = T + tau >= t_{j+1}.

Discipline (Chief request D): two solvers (pece, pi_rect) x two meshes.

Evidence class: NUMERICAL CORROBORATION only.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from math import gamma

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.fastconv import solve_blocked                # noqa: E402
from msbg.models import AlleePredatorPrey             # noqa: E402
from msbg.provenance import RunRecorder               # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def continuation_state(t_nodes, g_nodes, p, alpha, T_index, taus):
    """C_T(tau) for T = t_nodes[T_index], exact PL product integration."""
    tj = t_nodes[:T_index]
    tj1 = t_nodes[1:T_index + 1]
    phi = g_nodes[:T_index]
    m = (g_nodes[1:T_index + 1] - g_nodes[:T_index]) / (tj1 - tj)[:, None]
    T = t_nodes[T_index]
    out = np.empty((len(taus), 2))
    for i, tau in enumerate(taus):
        t = T + tau
        A = t - tj
        B = np.maximum(t - tj1, 0.0)
        Aa, Ba = A**alpha, B**alpha
        Aa1, Ba1 = A ** (alpha + 1), B ** (alpha + 1)
        w0 = (Aa - Ba) / alpha
        w1 = (Aa1 - Ba1) / (alpha + 1)
        contrib = (phi + m * (t - tj)[:, None]) * w0[:, None] - m * w1[:, None]
        out[i] = p + contrib.sum(0) / gamma(alpha)
    return out


def one(job):
    np.seterr(all="ignore")
    label, theta, a, b, mm, alpha, p, Tmax, h, method, Ts, Rs, n_tau = job
    model = AlleePredatorPrey(theta=theta, a=a, b=b, m=mm)
    E = np.array([model.x_star, model.y_star])
    N = int(round(Tmax / h))
    r = solve_blocked(model, np.atleast_2d(p), alpha, h, N, method=method, block=512,
                      store=True, store_stride=1)
    x = r.x[:, 0, :]
    t = r.t
    gv = model.g(x)
    rows = []
    for T in Ts:
        k = int(round(T / h))
        for R in Rs:
            taus = np.concatenate([[0.0], np.geomspace(max(R * 1e-4, h), R, n_tau)])
            C = continuation_state(t, gv, np.asarray(p, float), alpha, k, taus)
            d = np.linalg.norm(C - E, axis=1, ord=np.inf)
            rows.append({"T": T, "R": R, "D": float(d.max()), "tau_argmax": float(taus[d.argmax()]),
                         "phys_dist": float(np.max(np.abs(x[k] - E))),
                         "C0_minus_xT": float(np.max(np.abs(C[0] - x[k])))})
    return {"label": label, "method": method, "h": h, "E": E.tolist(), "p": list(map(float, p)),
            "theta": theta, "a": a, "b": b, "m": mm, "alpha": alpha, "rows": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=64)
    ap.add_argument("--Tmax", type=float, default=4000.0)
    ap.add_argument("--h", type=float, default=0.02)
    ap.add_argument("--candidates", default="",
                    help="json file with a list of {label,theta,a,b,m,alpha,p}")
    ap.add_argument("--n-tau", type=int, default=160)
    args = ap.parse_args()

    cands = [{"label": "TASK-0001 witness", "theta": 0.3, "a": 1.0, "b": 1.0, "m": 0.8,
              "alpha": 0.85, "p": [2.4372, 2.012]}]
    if args.candidates and os.path.exists(args.candidates):
        cands += json.load(open(args.candidates))
    Ts = [t for t in (100.0, 250.0, 500.0, 1000.0, 2000.0, 4000.0) if t <= args.Tmax]
    Rs = [1.0, 10.0, 100.0, 1000.0]
    jobs = []
    for c in cands:
        for method in ("pece", "pi_rect"):
            for h in (args.h, args.h / 2):
                jobs.append((c["label"], c["theta"], c["a"], c["b"], c["m"], c["alpha"], c["p"],
                             args.Tmax, h, method, Ts, Rs, args.n_tau))
    print(f"candidates={len(cands)} jobs={len(jobs)} Tmax={args.Tmax}", flush=True)
    rec = RunRecorder("t2_stageC", ROOT)
    res = []
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        for r in ex.map(one, jobs):
            res.append(r)
            print(f"  done {r['label']} {r['method']} h={r['h']}", flush=True)

    # cross-solver / cross-mesh spread and a compact table per candidate
    summary = []
    for c in cands:
        mine = [r for r in res if r["label"] == c["label"]]
        ref = next(r for r in mine if r["method"] == "pece" and r["h"] == args.h / 2)
        print(f"\n{c['label']}  (theta={c['theta']}, a={c['a']}, m={c['m']}, alpha={c['alpha']}, "
              f"p={c['p']}, E*={np.round(ref['E'],4).tolist()})")
        print(f"{'T':>7}{'||x(T)-E*||':>13}" + "".join(f"{'D(T,R='+str(int(R))+')':>15}" for R in Rs)
              + f"{'solver/mesh spread':>20}")
        for T in Ts:
            line = [row for row in ref["rows"] if row["T"] == T]
            spread = 0.0
            for R in Rs:
                vals = [next(row["D"] for row in r["rows"] if row["T"] == T and row["R"] == R)
                        for r in mine]
                spread = max(spread, max(vals) - min(vals))
            print(f"{T:7.0f}{line[0]['phys_dist']:13.3e}" +
                  "".join(f"{next(r['D'] for r in line if r['R']==R):15.3e}" for R in Rs) +
                  f"{spread:20.2e}")
            summary.append({"label": c["label"], "T": T, "phys_dist": line[0]["phys_dist"],
                            **{f"D_R{int(R)}": next(r["D"] for r in line if r["R"] == R)
                               for R in Rs}, "spread": spread})
    rec.save_json("runs", res)
    rec.save_json("summary", summary)
    rec.add("evidence_class", "NUMERICAL CORROBORATION")
    rec.add("definition", "D(T,R) = sup_{tau in [0,R]} ||T_T iota(p)(tau) - E*||_inf")
    print("\nmanifest:", rec.finish())


if __name__ == "__main__":
    main()
