#!/usr/bin/env python3
r"""TASK-0001 Stage D — SAME-AGE inter-basin collision, solved as a root problem.

This is the Chief's condition in its strictest form:

    H(p, q, t, s) = x(t;p) - x(s;q) = 0 ,   with  t = s ,

and with p, q in distinct conservatively classified outcome sets.

Formulation
-----------
Fix the survivor p (its orbit dips below theta) and fix an age t inside the
sub-threshold window.  Solve for q in the *certified* extinction region
R_ext = {0 < x < theta, y > 0}:

    Phi_t(q) := x(t;q) - x(t;p) = 0 ,    q in R_ext .

This is 2 equations in the 2 unknowns q, i.e. a square system; its Jacobian is
the variational matrix

    D_q x(t;q) = d x(t;q) / d q ,

whose invertibility is exactly the "nonsingular d x d derivative minor with
respect to explicitly declared solved variables" required by CANDIDATE-M2
(research/STATE_ARCHITECTURE.md, item 2).  The Jacobian is computed by central
differences of the solver endpoint map, and its singular values are reported.

If a root q* is found with q* in R_ext, then
  * iota(q*) lies in B(0,0)              [CERTIFIED-CONDITIONAL]
  * T_t iota(p) lies in B(E*)            [NUMERICAL]
  * e_0(T_t iota(p)) = x(t;p) = x(t;q*) = e_0(T_t iota(q*))
so F_{x(t;p)} is multibasin, with BOTH members reached at the SAME age t.

Evidence class: NUMERICAL CORROBORATION (floating point root of a nonlinear
system); the extinction side is CERTIFIED-CONDITIONAL.
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.basins import certified_extinction_predicate       # noqa: E402
from msbg.models import AlleePredatorPrey, DoubleAlleePredatorPrey  # noqa: E402
from msbg.provenance import RunRecorder, set_seed            # noqa: E402
from msbg.solvers import METHODS, solve                      # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def endpoint(model, Q, alpha, t, h, method="pece"):
    n = max(1, int(round(t / h)))
    return solve(model, np.atleast_2d(Q), alpha, t / n, n, method=method, store=False).x_final


def jac_q(model, q, alpha, t, h, fd=1e-6, method="pece"):
    cols = []
    for k in range(2):
        e = np.zeros(2)
        e[k] = fd * max(1.0, abs(q[k]))
        plus = endpoint(model, q + e, alpha, t, h, method)[0]
        minus = endpoint(model, q - e, alpha, t, h, method)[0]
        cols.append((plus - minus) / (2 * e[k]))
    return np.column_stack(cols)


def newton_q(model, q0, target, alpha, t, h, method="pece", maxit=40, tol=1e-12):
    q = np.array(q0, float)
    hist = []
    for _ in range(maxit):
        F = endpoint(model, q, alpha, t, h, method)[0] - target
        nrm = float(np.linalg.norm(F))
        hist.append((q.tolist(), nrm))
        if nrm < tol:
            break
        J = jac_q(model, q, alpha, t, h, method=method)
        try:
            step = np.linalg.solve(J, -F)
        except np.linalg.LinAlgError:
            break
        lam = 1.0
        for _ in range(25):
            qn = q + lam * step
            if qn[0] > 0 and qn[1] > 0:
                Fn = endpoint(model, qn, alpha, t, h, method)[0] - target
                if np.linalg.norm(Fn) < nrm:
                    break
            lam *= 0.5
        q = q + lam * step
    return q, hist


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", default="single")
    ap.add_argument("--theta", type=float, default=0.4)
    ap.add_argument("--a", type=float, default=1.0)
    ap.add_argument("--b", type=float, default=1.0)
    ap.add_argument("--m", type=float, default=0.8)
    ap.add_argument("--alpha", type=float, default=0.75)
    ap.add_argument("--p", type=float, nargs=2, required=True)
    ap.add_argument("--T", type=float, default=200.0)
    ap.add_argument("--h", type=float, default=0.01)
    ap.add_argument("--nq", type=int, default=90)
    args = ap.parse_args()

    set_seed()
    np.seterr(all="ignore")
    rec = RunRecorder("stage_d_sameage", ROOT)
    cls = DoubleAlleePredatorPrey if args.family == "double" else AlleePredatorPrey
    model = cls(theta=args.theta, a=args.a, b=args.b, m=args.m)
    cert = certified_extinction_predicate(model)
    p = np.array(args.p, float)
    N = int(round(args.T / args.h))
    E = np.array([model.x_star, model.y_star])
    rec.add("model", {"class": type(model).__name__, "provenance": model.provenance,
                      "theta": model.theta, "a": model.a, "b": model.b, "m": model.m,
                      "alpha": args.alpha, "E_star": E.tolist()})
    rec.add("p", p.tolist())

    rp = solve(model, np.atleast_2d(p), args.alpha, args.h, N, method="pece", store=True)
    xp = rp.x[:, 0, :]
    tt = rp.t
    below = np.flatnonzero(xp[:, 0] < model.theta)
    assert len(below), "the reference orbit never enters {x < theta}"
    print(f"p = {p}: orbit below theta on t in [{tt[below[0]]:.4f}, {tt[below[-1]]:.4f}], "
          f"min x = {xp[below, 0].min():.8f}")

    # ---- search ages inside the sub-threshold window -----------------------
    ages = np.unique(np.round(np.linspace(tt[below[0]], tt[below[-1]], 9), 6))
    qx = np.linspace(1e-3, model.theta * 0.999, args.nq)
    qy = np.linspace(1e-3, 3.0, args.nq)
    QX, QY = np.meshgrid(qx, qy, indexing="ij")
    Q = np.stack([QX.ravel(), QY.ravel()], axis=1)
    print(f"searching {len(Q)} starting points in the certified region "
          f"{{0<x<{model.theta}, y>0}} at {len(ages)} ages")

    found = []
    for t in ages:
        n = max(1, int(round(t / args.h)))
        target = solve(model, np.atleast_2d(p), args.alpha, t / n, n,
                       method="pece", store=False).x_final[0]
        XQ = solve(model, Q, args.alpha, t / n, n, method="pece", store=False).x_final
        dist = np.linalg.norm(XQ - target, axis=1)
        k = int(np.argmin(dist))
        qstar, hist = newton_q(model, Q[k], target, args.alpha, t, args.h)
        res = float(np.linalg.norm(
            endpoint(model, qstar, args.alpha, t, args.h)[0] - target))
        inside = bool(cert(qstar[None, :])[0])
        J = jac_q(model, qstar, args.alpha, t, args.h)
        sv = np.linalg.svd(J, compute_uv=False)
        rank = int((sv > sv[0] * 1e-10).sum()) if sv[0] > 0 else 0
        rec_row = {
            "t": float(t), "target_x_t_p": target.tolist(),
            "q_seed": Q[k].tolist(), "grid_min_distance": float(dist[k]),
            "q_star": qstar.tolist(), "residual": res,
            "q_star_in_certified_extinction_region": inside,
            "jacobian_dq": J.tolist(), "singular_values": sv.tolist(),
            "rank": rank, "det": float(np.linalg.det(J)),
            "condition_number": float(sv[0] / sv[-1]) if sv[-1] > 0 else None,
            "newton_iterations": len(hist),
        }
        found.append(rec_row)
        print(f"  t={t:8.4f}  x(t;p)={np.round(target,8)}  q*={np.round(qstar,8)}  "
              f"|H|={res:.2e}  in R_ext={inside}  det Dq={rec_row['det']:+.3e}  "
              f"sv={np.array2string(sv, precision=3)}")

    good = [f for f in found if f["residual"] < 1e-10 and f["q_star_in_certified_extinction_region"]]
    print(f"\nSAME-AGE inter-basin collisions with |H| < 1e-10 and q* certified: "
          f"{len(good)}/{len(found)}")

    # ---- cross-solver confirmation of the best root ------------------------
    if good:
        best = min(good, key=lambda f: f["residual"])
        cross = {}
        for method in METHODS:
            for hh in (args.h, args.h / 2):
                v = endpoint(model, np.array(best["q_star"]), args.alpha, best["t"], hh,
                             method)[0]
                w = endpoint(model, p, args.alpha, best["t"], hh, method)[0]
                cross[f"{method}_h{hh}"] = {
                    "x_t_q": v.tolist(), "x_t_p": w.tolist(),
                    "abs_diff": float(np.linalg.norm(v - w)),
                }
        print("cross-solver check of the best root:")
        for k, v in cross.items():
            print(f"    {k:18} |x(t;p)-x(t;q*)| = {v['abs_diff']:.3e}")
        rec.add("best_root", best)
        rec.add("best_root_cross_solver", cross)

    rec.save_json("roots", found)
    rec.add("n_ages_tested", len(found))
    rec.add("n_certified_same_age_collisions", len(good))
    rec.add("evidence_class",
            "NUMERICAL CORROBORATION (floating-point root of a square nonlinear system); "
            "the extinction side of the pair is CERTIFIED-CONDITIONAL")
    print("\nmanifest:", rec.finish())


if __name__ == "__main__":
    main()
