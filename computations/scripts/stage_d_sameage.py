#!/usr/bin/env python3
r"""TASK-0001 Stage D — SAME-AGE inter-basin collision search (v2).

The Chief's condition in its strictest form:

    H(p, q, t, s) = x(t;p) - x(s;q) = 0 ,   t = s ,

with p and q in distinct conservatively classified outcome sets.

Formulation
-----------
Fix the survivor p, whose orbit enters {x < theta}, and an age t inside that
window.  Solve the *square* system

    Phi_t(q) := x(t;q) - x(t;p) = 0 ,     q in the extinction-labelled set,

whose Jacobian is the variational matrix D_q x(t;q); its invertibility is
exactly the "nonsingular d x d minor in explicitly declared solved variables"
of CANDIDATE-M2.

Two failure modes of the naive version, both fixed here
-------------------------------------------------------
1. ``Phi_t`` always has the trivial root ``q = p``.  Unconstrained Newton walks
   straight out of the search box and converges to it, reporting a spurious
   ``|H| ~ 1e-15``.  v2 runs a **projected** Newton clipped to the search box
   and explicitly rejects any iterate that approaches p.
2. Restricting q to the CERTIFIED region ``{0 < x < theta}`` is unnecessarily
   strong: q only has to lie in the *extinction basin*, which is larger.  v2
   searches the whole box, labels every grid point by the conservative
   classifier, and reports two tiers - q* merely extinction-labelled
   (NUMERICAL) and q* additionally inside ``{0 < x < theta}``
   (CERTIFIED-CONDITIONAL).

Even when no root exists, the run is informative: the reported
``image_gap`` is the distance from ``x(t;p)`` to the image of the
extinction-labelled set under the time-t map, i.e. how far the same-age
condition is from being satisfiable at that age.
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.basins import Outcome, certified_extinction_predicate, classify  # noqa: E402
from msbg.models import AlleePredatorPrey, DoubleAlleePredatorPrey         # noqa: E402
from msbg.provenance import RunRecorder, set_seed                          # noqa: E402
from msbg.solvers import METHODS, solve                                    # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def endpoint(model, Q, alpha, t, h, method="pece"):
    n = max(1, int(round(t / h)))
    return solve(model, np.atleast_2d(Q), alpha, t / n, n, method=method, store=False).x_final


def jac_q(model, q, alpha, t, h, fd=1e-6, method="pece"):
    cols = []
    for k in range(2):
        e = np.zeros(2)
        e[k] = fd * max(1.0, abs(q[k]))
        cols.append(
            (endpoint(model, q + e, alpha, t, h, method)[0]
             - endpoint(model, q - e, alpha, t, h, method)[0]) / (2 * e[k])
        )
    return np.column_stack(cols)


def projected_newton(model, q0, target, alpha, t, h, box, p, method="pece",
                     maxit=30, tol=1e-12, p_guard=1e-3):
    """Newton on Phi_t(q)=0, iterates clipped to ``box``, trivial root excluded."""
    (xlo, xhi), (ylo, yhi) = box
    q = np.clip(np.array(q0, float), [xlo, ylo], [xhi, yhi])
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
        lam, improved = 1.0, False
        for _ in range(30):
            qn = np.clip(q + lam * step, [xlo, ylo], [xhi, yhi])
            if np.linalg.norm(qn - p) < p_guard:        # refuse the trivial root
                lam *= 0.5
                continue
            if np.linalg.norm(endpoint(model, qn, alpha, t, h, method)[0] - target) < nrm:
                improved = True
                break
            lam *= 0.5
        if not improved:
            break
        q = qn
    F = endpoint(model, q, alpha, t, h, method)[0] - target
    return q, float(np.linalg.norm(F)), hist


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", default="single")
    ap.add_argument("--theta", type=float, default=0.3)
    ap.add_argument("--a", type=float, default=1.0)
    ap.add_argument("--b", type=float, default=1.0)
    ap.add_argument("--m", type=float, default=0.8)
    ap.add_argument("--alpha", type=float, default=0.85)
    ap.add_argument("--p", type=float, nargs=2, required=True)
    ap.add_argument("--T", type=float, default=200.0)
    ap.add_argument("--h", type=float, default=0.01)
    ap.add_argument("--nq", type=int, default=70)
    ap.add_argument("--qxmax", type=float, default=1.6)
    ap.add_argument("--qymax", type=float, default=5.0)
    ap.add_argument("--label-T", type=float, default=800.0)
    ap.add_argument("--label-h", type=float, default=0.02)
    ap.add_argument("--n-ages", type=int, default=9)
    args = ap.parse_args()

    set_seed()
    np.seterr(all="ignore")
    rec = RunRecorder("stage_d_sameage", ROOT)
    cls = DoubleAlleePredatorPrey if args.family == "double" else AlleePredatorPrey
    model = cls(theta=args.theta, a=args.a, b=args.b, m=args.m)
    cert = certified_extinction_predicate(model)
    p = np.array(args.p, float)
    E = np.array([model.x_star, model.y_star])
    box = ((1e-4, args.qxmax), (1e-4, args.qymax))
    rec.add("model", {"class": type(model).__name__, "provenance": model.provenance,
                      "theta": model.theta, "a": model.a, "b": model.b, "m": model.m,
                      "alpha": args.alpha, "E_star": E.tolist()})
    rec.add("p", p.tolist())
    rec.add("search_box", {"x": list(box[0]), "y": list(box[1])})

    # ---- reference orbit and its sub-threshold window ----------------------
    N = int(round(args.T / args.h))
    rp = solve(model, np.atleast_2d(p), args.alpha, args.h, N, method="pece", store=True)
    xp, tt = rp.x[:, 0, :], rp.t
    below = np.flatnonzero(xp[:, 0] < model.theta)
    assert len(below), "the reference orbit never enters {x < theta}"
    print(f"p = {p}: below theta on t in [{tt[below[0]]:.4f}, {tt[below[-1]]:.4f}], "
          f"min x = {xp[below, 0].min():.8f}", flush=True)

    # ---- label the search box ---------------------------------------------
    qx = np.linspace(box[0][0], box[0][1], args.nq)
    qy = np.linspace(box[1][0], box[1][1], args.nq)
    QX, QY = np.meshgrid(qx, qy, indexing="ij")
    Q = np.stack([QX.ravel(), QY.ravel()], axis=1)
    NL = int(round(args.label_T / args.label_h))
    rl = solve(model, Q, args.alpha, args.label_h, NL, method="pece", store=True,
               store_stride=max(1, NL // 4000))
    lab = classify(rl.x, E, r_coex=0.05, r_ext=0.05)
    ext = lab == Outcome.EXTINCTION
    certified = cert(Q)
    print(f"search box {args.nq}x{args.nq}: "
          f"{int(ext.sum())} extinction-labelled, {int(certified.sum())} inside the certified "
          f"region, {int((lab == Outcome.COEXISTENCE).sum())} coexistence, "
          f"{int((lab == Outcome.AMBIGUOUS).sum())} ambiguous", flush=True)
    rec.add("label_counts", {Outcome.NAMES[k]: int((lab == k).sum()) for k in range(5)})

    ages = np.unique(np.round(np.linspace(tt[below[0]], tt[below[-1]], args.n_ages), 6))
    found = []
    for t in ages:
        n = max(1, int(round(t / args.h)))
        target = endpoint(model, p, args.alpha, t, args.h)[0]
        XQ = endpoint(model, Q, args.alpha, t, args.h)
        d_all = np.linalg.norm(XQ - target, axis=1)
        d_ext = np.where(ext, d_all, np.inf)
        k = int(np.argmin(d_ext))
        image_gap = float(d_ext[k])
        qstar, res, hist = projected_newton(model, Q[k], target, args.alpha, t, args.h,
                                            box, p)
        J = jac_q(model, qstar, args.alpha, t, args.h)
        sv = np.linalg.svd(J, compute_uv=False)
        in_cert = bool(cert(qstar[None, :])[0])
        # outcome label of the refined q*
        rq = solve(model, np.atleast_2d(qstar), args.alpha, args.label_h, NL, method="pece",
                   store=True, store_stride=max(1, NL // 4000))
        lq = int(classify(rq.x, E, r_coex=0.05, r_ext=0.05)[0])
        row = {
            "t": float(t), "x_t_p": target.tolist(),
            "image_gap_over_extinction_set": image_gap,
            "q_seed": Q[k].tolist(), "q_star": qstar.tolist(), "residual": res,
            "q_star_label": Outcome.NAMES[lq],
            "q_star_in_certified_region": in_cert,
            "distance_to_p": float(np.linalg.norm(qstar - p)),
            "singular_values": sv.tolist(), "det": float(np.linalg.det(J)),
            "condition_number": float(sv[0] / sv[-1]) if sv[-1] > 0 else None,
            "newton_steps": len(hist),
        }
        found.append(row)
        print(f"  t={t:8.4f} x(t;p)={np.round(target,7)} image_gap={image_gap:.3e} "
              f"q*={np.round(qstar,6)} |H|={res:.2e} label={row['q_star_label']:11} "
              f"cert={in_cert} det={row['det']:+.2e}", flush=True)

    good = [f for f in found
            if f["residual"] < 1e-9 and f["q_star_label"] == "EXTINCTION"
            and f["distance_to_p"] > 1e-3]
    gold = [f for f in good if f["q_star_in_certified_region"]]
    print(f"\nSAME-AGE inter-basin collisions, |H| < 1e-9, q* extinction-labelled, "
          f"q* != p : {len(good)}/{len(found)}   (of which q* certified: {len(gold)})")
    if not good:
        gaps = [f["image_gap_over_extinction_set"] for f in found]
        print(f"NEGATIVE RESULT. Smallest gap between x(t;p) and the image of the "
              f"extinction-labelled set: {min(gaps):.3e} at t="
              f"{found[int(np.argmin(gaps))]['t']:.4f}. A negative search is not an "
              f"impossibility theorem.")

    if good:
        best = min(good, key=lambda f: f["residual"])
        cross = {}
        for method in METHODS:
            for hh in (args.h, args.h / 2):
                v = endpoint(model, np.array(best["q_star"]), args.alpha, best["t"], hh, method)[0]
                w = endpoint(model, p, args.alpha, best["t"], hh, method)[0]
                cross[f"{method}_h{hh}"] = {"abs_diff": float(np.linalg.norm(v - w)),
                                            "x_t_q": v.tolist(), "x_t_p": w.tolist()}
        print("cross-solver check of the best root:")
        for k2, v in cross.items():
            print(f"    {k2:18} |x(t;p)-x(t;q*)| = {v['abs_diff']:.3e}")
        rec.add("best_root", best)
        rec.add("best_root_cross_solver", cross)

    rec.save_json("roots", found)
    rec.save_npz("labelled_box", Q=Q, labels=lab, certified=certified)
    rec.add("n_ages_tested", len(found))
    rec.add("n_same_age_inter_basin_collisions", len(good))
    rec.add("n_with_certified_q", len(gold))
    rec.add("min_image_gap", float(min(f["image_gap_over_extinction_set"] for f in found)))
    rec.add("evidence_class",
            "NUMERICAL CORROBORATION (floating-point root of a square nonlinear system); "
            "a null result here is a negative search, not an impossibility theorem")
    print("\nmanifest:", rec.finish())


if __name__ == "__main__":
    main()
