#!/usr/bin/env python3
"""TASK-0001 Stage A — solver validation (mandatory gate before discovery).

Checks, in order:

A1  Mittag-Leffler implementation against three independent references
    (closed forms at alpha in {1/2,1,2}; Taylor vs Stieltjes route; the
    large-argument asymptote 1/(x Gamma(1-alpha))).
A2  scalar linear problem  ^C D^a x = lam x,  exact x0 E_a(lam t^a):
    absolute error and *observed* convergence order on a refinement ladder,
    for all three solvers, for lam < 0 and lam > 0.
A3  genuinely planar linear problem ^C D^a x = A x with A a scaled rotation,
    exact matrix Mittag-Leffler ground truth.
A4  long-horizon test to T = 1000 against the exact algebraic tail.
A5  bitwise determinism on repeated runs.
A6  cross-solver self-convergence on the nonlinear ecological model
    (no closed form exists there).
A7  positivity of the positive-cone model along tested trajectories.

Evidence class: NUMERICAL CORROBORATION of solver correctness; A1 additionally
cross-validates a special-function implementation against closed forms.
"""
from __future__ import annotations

import argparse
import os
import sys

import mpmath as mp
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.basins import positivity_report                       # noqa: E402
from msbg.mittag_leffler import (                               # noqa: E402
    e_alpha,
    e_alpha_closed_form,
    matrix_e_alpha_scaled_rotation,
)
from msbg.models import AlleePredatorPrey, LinearScalar, ScaledRotation  # noqa: E402
from msbg.provenance import RunRecorder                         # noqa: E402
from msbg.solvers import METHODS, solve                         # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def observed_order(hs, errs):
    hs = np.asarray(hs, float)
    errs = np.asarray(errs, float)
    ok = errs > 0
    if ok.sum() < 2:
        return None
    A = np.vstack([np.log(hs[ok]), np.ones(ok.sum())]).T
    slope, _ = np.linalg.lstsq(A, np.log(errs[ok]), rcond=None)[0]
    return float(slope)


def a1_mittag_leffler():
    rows = []
    for alpha, zs in (
        (1.0, [-5.0, -1.0, 0.5, 3.0, 1 + 1j]),
        (0.5, [-8.0, -2.0, 1.3, 1 + 1j, 1.35 - 1.99j]),
        (2.0, [-3.0, 1.7]),
    ):
        for z in zs:
            a = e_alpha(alpha, z, dps=30, route="taylor")
            b = e_alpha_closed_form(alpha, z, dps=30)
            rows.append(
                {
                    "check": "taylor_vs_closed_form",
                    "alpha": alpha,
                    "z": str(z),
                    "abs_diff": float(mp.nstr(abs(a - b), 8)),
                    "value": str(mp.nstr(a, 20)),
                }
            )
    # The Taylor route costs O(|z|^{1/alpha}) guard digits, so the comparison
    # points have to be chosen per alpha to stay affordable (|z|^{1/alpha} <= 400).
    for alpha in (0.3, 0.5, 0.6, 0.8):
        xs = [x for x in (0.5, 1.0, 2.5, 5.0, 12.5, 20.0) if x ** (1.0 / alpha) <= 400.0]
        for x in xs:
            t = e_alpha(alpha, -x, dps=30, route="taylor")
            s = e_alpha(alpha, -x, dps=30, route="stieltjes")
            rows.append(
                {
                    "check": "taylor_vs_stieltjes",
                    "alpha": alpha,
                    "z": f"-{x}",
                    "abs_diff": float(mp.nstr(abs(t - s), 8)),
                    "value": str(mp.nstr(t, 20)),
                }
            )
    for alpha in (0.4, 0.6, 0.85):
        for x in (1e3, 1e5, 1e7):
            s = e_alpha(alpha, -x, dps=25, route="stieltjes")
            asy = 1.0 / (mp.mpf(x) * mp.gamma(1 - mp.mpf(alpha)))
            rows.append(
                {
                    "check": "stieltjes_vs_asymptote",
                    "alpha": alpha,
                    "z": f"-{x:g}",
                    "ratio_to_asymptote": float(mp.nstr(s / asy, 10)),
                }
            )
    worst = max(r.get("abs_diff", 0.0) for r in rows)
    return rows, worst


def a2_scalar_linear(alphas=(0.4, 0.6, 0.85), lams=(-1.0, 0.7), T=2.0, ladder=(250, 500, 1000, 2000, 4000)):
    rows = []
    for alpha in alphas:
        for lam in lams:
            exact = float(e_alpha(alpha, lam * T**alpha, dps=30))
            model = LinearScalar(lam=lam)
            for method in METHODS:
                hs, errs = [], []
                for N in ladder:
                    h = T / N
                    r = solve(model, [[1.0]], alpha, h, N, method=method, store=False)
                    err = abs(float(r.x_final[0, 0]) - exact)
                    hs.append(h)
                    errs.append(err)
                rows.append(
                    {
                        "alpha": alpha,
                        "lam": lam,
                        "T": T,
                        "method": method,
                        "exact": exact,
                        "h": hs,
                        "abs_err": errs,
                        "observed_order": observed_order(hs, errs),
                    }
                )
    return rows


def a3_planar_linear(alpha=0.5, rho=1.0, theta=0.9734093253645294, T=3.0,
                     ladder=(500, 1000, 2000, 4000, 8000)):
    E = matrix_e_alpha_scaled_rotation(alpha, rho, theta, T, dps=30)
    Ex = np.array([[float(E[0, 0]), float(E[0, 1])], [float(E[1, 0]), float(E[1, 1])]])
    model = ScaledRotation(rho=rho, theta=theta)
    X0 = np.array([[1.0, 0.0], [0.0, 1.0], [0.37, -0.91]])
    exact = X0 @ Ex.T
    rows = []
    for method in METHODS:
        hs, errs = [], []
        for N in ladder:
            h = T / N
            r = solve(model, X0, alpha, h, N, method=method, store=False)
            hs.append(h)
            errs.append(float(np.max(np.abs(r.x_final - exact))))
        rows.append(
            {
                "alpha": alpha, "rho": rho, "theta": theta, "T": T, "method": method,
                "exact_matrix": Ex.tolist(), "h": hs, "max_abs_err": errs,
                "observed_order": observed_order(hs, errs),
            }
        )
    return rows


def a4_long_horizon(alpha=0.5, lam=-1.0, T=1000.0, N=200000):
    exact = float(e_alpha(alpha, lam * T**alpha, dps=30))
    tail = 1.0 / (abs(lam) * T**alpha * float(mp.gamma(1 - mp.mpf(alpha))))
    model = LinearScalar(lam=lam)
    rows = []
    for method in METHODS:
        r = solve(model, [[1.0]], alpha, T / N, N, method=method, store=False)
        v = float(r.x_final[0, 0])
        rows.append(
            {
                "method": method, "alpha": alpha, "lam": lam, "T": T, "N": N,
                "numeric": v, "exact": exact, "abs_err": abs(v - exact),
                "rel_err": abs(v - exact) / abs(exact),
                "algebraic_tail_1_over_x_Gamma": tail,
            }
        )
    return rows


def a5_determinism(alpha=0.6):
    model = AlleePredatorPrey()
    X0 = np.array([[0.9, 1.3], [0.35, 0.4], [1.2, 0.2]])
    out = {}
    for method in METHODS:
        a = solve(model, X0, alpha, 0.05, 2000, method=method, store=False).x_final
        b = solve(model, X0, alpha, 0.05, 2000, method=method, store=False).x_final
        out[method] = {
            "bitwise_identical": bool(np.array_equal(a.view(np.uint8), b.view(np.uint8))),
            "max_abs_diff": float(np.max(np.abs(a - b))),
        }
    return out


def a6_cross_solver(alpha=0.6, T=120.0, ladder=(2000, 4000, 8000, 16000)):
    model = AlleePredatorPrey()
    X0 = np.array([[0.9, 1.3], [0.35, 0.4], [1.2, 0.2], [0.75, 2.5]])
    ref = {}
    for method in METHODS:
        ref[method] = [
            solve(model, X0, alpha, T / N, N, method=method, store=False).x_final
            for N in ladder
        ]
    rows = []
    finest = {m: ref[m][-1] for m in METHODS}
    for m in METHODS:
        hs = [T / N for N in ladder[:-1]]
        errs = [float(np.max(np.abs(ref[m][i] - finest[m]))) for i in range(len(ladder) - 1)]
        rows.append({"kind": "self", "method": m, "h": hs, "err_vs_finest": errs,
                     "observed_order": observed_order(hs, errs)})
    for i, m1 in enumerate(METHODS):
        for m2 in METHODS[i + 1:]:
            rows.append(
                {
                    "kind": "pairwise", "methods": [m1, m2], "T": T, "alpha": alpha,
                    "max_abs_diff_finest": float(np.max(np.abs(finest[m1] - finest[m2]))),
                    "per_h": [
                        float(np.max(np.abs(ref[m1][k] - ref[m2][k]))) for k in range(len(ladder))
                    ],
                    "h": [T / N for N in ladder],
                }
            )
    return rows


def a7_positivity(alpha=0.6, T=300.0, N=6000):
    model = AlleePredatorPrey()
    g = np.linspace(0.02, 1.4, 20)
    yy = np.linspace(0.02, 3.0, 20)
    GG, YY = np.meshgrid(g, yy, indexing="ij")
    X0 = np.stack([GG.ravel(), YY.ravel()], axis=1)
    out = {}
    for method in METHODS:
        r = solve(model, X0, alpha, T / N, N, method=method, store=True, store_stride=5)
        with np.errstate(all="ignore"):
            pr = positivity_report(r.x)
        out[method] = {"min_x": pr.min_x, "min_y": pr.min_y, "n_trajectories_negative": pr.n_negative,
                       "n_ic": int(len(X0)), "tol": pr.tol}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    np.seterr(all="ignore")
    rec = RunRecorder("stage_a", ROOT)

    print("A1 Mittag-Leffler cross-validation ...", flush=True)
    rows, worst = a1_mittag_leffler()
    rec.add("A1_worst_abs_diff", worst)
    rec.add("A1_n_checks", len(rows))
    rec.save_json("A1_mittag_leffler", rows)
    print(f"    worst abs diff across {len(rows)} checks: {worst:.3e}")

    print("A2 scalar linear vs exact E_alpha ...", flush=True)
    a2 = a2_scalar_linear(ladder=(250, 500, 1000) if args.quick else (250, 500, 1000, 2000, 4000))
    rec.save_json("A2_scalar_linear", a2)
    for r in a2:
        print(f"    alpha={r['alpha']} lam={r['lam']:+.2f} {r['method']:8} "
              f"err(finest)={r['abs_err'][-1]:.3e} observed_order={r['observed_order']:.3f}")

    print("A3 planar linear vs exact matrix E_alpha ...", flush=True)
    a3 = a3_planar_linear(ladder=(500, 1000, 2000) if args.quick else (500, 1000, 2000, 4000, 8000))
    rec.save_json("A3_planar_linear", a3)
    for r in a3:
        print(f"    {r['method']:8} err(finest)={r['max_abs_err'][-1]:.3e} "
              f"observed_order={r['observed_order']:.3f}")

    print("A4 long horizon T=1000 ...", flush=True)
    a4 = a4_long_horizon(N=50000 if args.quick else 200000)
    rec.save_json("A4_long_horizon", a4)
    for r in a4:
        print(f"    {r['method']:8} x(T)={r['numeric']:.10f} exact={r['exact']:.10f} "
              f"rel_err={r['rel_err']:.3e}")

    print("A5 determinism ...", flush=True)
    a5 = a5_determinism()
    rec.add("A5_determinism", a5)
    print("   ", a5)

    print("A6 cross-solver agreement on the nonlinear model ...", flush=True)
    a6 = a6_cross_solver(ladder=(2000, 4000, 8000) if args.quick else (2000, 4000, 8000, 16000))
    rec.save_json("A6_cross_solver", a6)
    for r in a6:
        if r["kind"] == "self":
            print(f"    self  {r['method']:8} observed_order={r['observed_order']:.3f}")
        else:
            print(f"    pair  {r['methods'][0]:8}/{r['methods'][1]:8} "
                  f"max|diff| at finest h = {r['max_abs_diff_finest']:.3e}")

    print("A7 positivity ...", flush=True)
    a7 = a7_positivity(N=2000 if args.quick else 6000)
    rec.add("A7_positivity", a7)
    print("   ", a7)

    rec.add("evidence_class", "NUMERICAL CORROBORATION (solver validation); A1 closed-form cross-validation")
    print("\nmanifest:", rec.finish())


if __name__ == "__main__":
    main()
