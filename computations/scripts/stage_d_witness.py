#!/usr/bin/env python3
r"""TASK-0001 Stage D — inter-basin collision witness, validated.

THE OBJECT
----------
Let p be a standard (constant-history) initial state of

    ^C D^a x = x(1-x)(x-theta) - a x y,      ^C D^a y = y(b x - m),     0 < a < 1,

with theta < m/b, and suppose the orbit of p converges to the coexistence
attractor E* while at some time t* its prey component satisfies x(t*) < theta.
Put z = (x(t*), y(t*)).  Then

    e_0(T_{t*} iota(p)) = z = e_0(iota(z)),       T_{t*} iota(p), iota(z) in R_alpha,

so both continuation states lie in the same reachable present-state fibre F_z,
while

    iota(z) in B(0,0)          [CERTIFIED-CONDITIONAL, see msbg/basins.py]
    T_{t*} iota(p) in B(E*)    [NUMERICAL]

By REDUCTION-M1 (research/CLAIMS.md) the fibre F_z is multibasin.  This is the
``embedded_age`` collision (s = 0): it needs no root solving, because "the orbit
of p enters the open region {x < theta}" is an OPEN condition - which is also why
its persistence under perturbation does not require the implicit function
theorem, only continuity of the solution map.

WHAT THIS SCRIPT VALIDATES
--------------------------
D1  the witness orbit under all three solvers, on a mesh ladder;
D2  horizon sensitivity of the survival label, plus the observed algebraic decay
    exponent of dist(x(t), E*), compared with the linearised prediction t^{-a};
D3  the whole time interval on which x(t) < theta (a one-parameter family of
    multibasin fibres, not a single point);
D4  high-precision (mpmath) recomputation of the witness;
D5  the collision Jacobian of H(p, z, t, 0) = x(t;p) - z and its rank;
D6  openness: persistence of the witness under perturbation of
    (alpha, theta, a, b, m, p);
D7  same-age (t = s) and cross-age (t != s) collisions between orbits with
    different conservative labels, with Newton refinement and Jacobian SVD.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import mpmath as mp
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.basins import Outcome, certified_extinction_predicate, classify, positivity_report  # noqa: E402
from msbg.collisions import (  # noqa: E402
    collision_jacobian,
    cross_age_collisions,
    refine_collision,
    same_age_collisions,
)
from msbg.models import AlleePredatorPrey, DoubleAlleePredatorPrey  # noqa: E402
from msbg.provenance import RunRecorder, set_seed                  # noqa: E402
from msbg.solvers import METHODS, solve, solve_mp                  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make_model(family, theta, a, b, m, c=0.5):
    if family == "double":
        return DoubleAlleePredatorPrey(theta=theta, c=c, a=a, b=b, m=m)
    return AlleePredatorPrey(theta=theta, a=a, b=b, m=m)


def orbit_diag(model, p, alpha, T, N, method="pece", stride=1):
    r = solve(model, np.atleast_2d(p), alpha, T / N, N, method=method, store=True,
              store_stride=stride)
    x = r.x[:, 0, :]
    t = r.t
    E = np.array([model.x_star, model.y_star])
    i = int(np.nanargmin(np.where(np.isfinite(x[:, 0]), x[:, 0], np.inf)))
    dE = np.linalg.norm(x - E, axis=1)
    k0 = int(0.65 * len(t))
    k1 = int(0.30 * len(t))
    below = x[:, 0] < model.theta
    idx = np.flatnonzero(below)
    return {
        "t": t, "x": x, "E": E,
        "t_dip": float(t[i]), "x_dip": float(x[i, 0]), "y_dip": float(x[i, 1]),
        "margin": float(model.theta - x[i, 0]),
        "tail_dE": float(np.nanmax(dE[k0:])), "prev_dE": float(np.nanmax(dE[k1:k0])),
        "final": x[-1].tolist(),
        "t_below_first": (float(t[idx[0]]) if len(idx) else None),
        "t_below_last": (float(t[idx[-1]]) if len(idx) else None),
        "n_below": int(len(idx)),
        "min_x_overall": float(np.nanmin(x[:, 0])), "min_y_overall": float(np.nanmin(x[:, 1])),
        "max_abs": float(np.nanmax(np.abs(x))),
    }


def decay_exponent(t, dE, t_lo_frac=0.4):
    k = int(len(t) * t_lo_frac)
    tt, dd = t[k:], dE[k:]
    ok = (tt > 0) & (dd > 0) & np.isfinite(dd)
    if ok.sum() < 10:
        return None
    A = np.vstack([np.log(tt[ok]), np.ones(ok.sum())]).T
    return float(np.linalg.lstsq(A, np.log(dd[ok]), rcond=None)[0][0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", default="single")
    ap.add_argument("--theta", type=float, default=0.4)
    ap.add_argument("--a", type=float, default=1.0)
    ap.add_argument("--b", type=float, default=1.0)
    ap.add_argument("--m", type=float, default=0.8)
    ap.add_argument("--alpha", type=float, default=0.75)
    ap.add_argument("--p", type=float, nargs=2, default=None,
                    help="witness initial state; if omitted a local search is run")
    ap.add_argument("--T", type=float, default=800.0)
    ap.add_argument("--N", type=int, default=16000)
    args = ap.parse_args()

    set_seed()
    np.seterr(all="ignore")
    rec = RunRecorder("stage_d_witness", ROOT)
    model = make_model(args.family, args.theta, args.a, args.b, args.m)
    E = np.array([model.x_star, model.y_star])
    cert = certified_extinction_predicate(model)
    rec.add("model", {"class": type(model).__name__, "provenance": model.provenance,
                      "theta": model.theta, "a": model.a, "b": model.b, "m": model.m,
                      "alpha": args.alpha, "E_star": E.tolist(),
                      "theta_lt_xstar": bool(model.theta < model.x_star)})
    print(f"model={type(model).__name__} theta={model.theta} a={model.a} b={model.b} m={model.m} "
          f"alpha={args.alpha}  E*={E}")

    # ---------------- locate the witness ------------------------------------
    if args.p is None:
        xs = np.linspace(model.theta + 1e-3, 4.0, 60)
        ys = np.linspace(0.02, 6.0, 60)
        XX, YY = np.meshgrid(xs, ys, indexing="ij")
        X0 = np.stack([XX.ravel(), YY.ravel()], axis=1)
        r = solve(model, X0, args.alpha, args.T / 8000, 8000, method="pece", store=True,
                  store_stride=4)
        tr = r.x
        dE = np.linalg.norm(tr - E, axis=2)
        K = tr.shape[0]
        k0, k1 = int(0.65 * K), int(0.30 * K)
        coex = (np.nanmax(dE[k0:], axis=0) < 0.05) & (
            np.nanmax(dE[k0:], axis=0) <= 0.7 * np.nanmax(dE[k1:k0], axis=0)
        ) & np.isfinite(tr).all(axis=0).all(axis=1)
        minx = np.nanmin(tr[:, :, 0], axis=0)
        sub = coex & (minx < model.theta)
        assert sub.any(), "no sub-threshold survivor in the search window"
        p = X0[int(np.argmax(np.where(sub, model.theta - minx, -np.inf)))]
        print(f"witness search: {int(coex.sum())} coexistence labels, {int(sub.sum())} "
              f"sub-threshold; best p = {p}")
        rec.add("D0_search", {"n_ic": int(len(X0)), "n_coex": int(coex.sum()),
                              "n_subthreshold": int(sub.sum()), "p": p.tolist()})
    else:
        p = np.array(args.p, float)
    rec.add("witness_p", p.tolist())

    # ---------------- D1: three solvers, mesh ladder ------------------------
    d1 = []
    for method in METHODS:
        for N in (args.N // 4, args.N // 2, args.N, 2 * args.N):
            d = orbit_diag(model, p, args.alpha, args.T, N, method=method,
                           stride=max(1, N // 4000))
            d1.append({k: v for k, v in d.items() if k not in ("t", "x", "E")}
                      | {"method": method, "N": N, "h": args.T / N})
            print(f"D1 {method:8} N={N:6d} x_dip={d['x_dip']:.8f} t_dip={d['t_dip']:8.3f} "
                  f"margin={d['margin']:+.6f} tail_dE={d['tail_dE']:.3e} final={np.round(d['final'],6)}")
    rec.save_json("D1_mesh_ladder", d1)
    margins = [r["margin"] for r in d1]
    rec.add("D1_margin_min", float(np.min(margins)))
    rec.add("D1_margin_max", float(np.max(margins)))
    rec.add("D1_all_solvers_all_meshes_subthreshold", bool(np.min(margins) > 0))
    print(f"D1 margin across 3 solvers x 4 meshes: min={np.min(margins):+.6f} "
          f"max={np.max(margins):+.6f}")

    # ---------------- D2: horizon ladder + decay exponent -------------------
    d2 = []
    for T in (args.T / 4, args.T / 2, args.T, 2 * args.T, 4 * args.T):
        N = int(T / (args.T / args.N))
        d = orbit_diag(model, p, args.alpha, T, N, method="pece", stride=max(1, N // 6000))
        dE = np.linalg.norm(d["x"] - E, axis=1)
        d2.append({"T": T, "N": N, "x_dip": d["x_dip"], "margin": d["margin"],
                   "final": d["final"], "dist_final": float(dE[-1]),
                   "decay_exponent": decay_exponent(d["t"], dE),
                   "tail_dE": d["tail_dE"]})
        print(f"D2 T={T:8.1f} dist(E*)={dE[-1]:.3e} decay_exponent={d2[-1]['decay_exponent']} "
              f"(linearised prediction {-args.alpha})")
    rec.save_json("D2_horizon_ladder", d2)
    rec.add("D2_linearised_decay_prediction", -args.alpha)

    # ---------------- D3: the whole sub-threshold arc ------------------------
    d = orbit_diag(model, p, args.alpha, args.T, args.N, method="pece", stride=1)
    below = d["x"][:, 0] < model.theta
    idx = np.flatnonzero(below)
    arc = d["x"][idx]
    certified = cert(arc)
    pr = positivity_report(d["x"][:, None, :])
    print(f"D3 x(t) < theta on t in [{d['t'][idx[0]]:.4f}, {d['t'][idx[-1]]:.4f}] "
          f"({len(idx)} mesh points); all in certified region: {bool(certified.all())}")
    print(f"   positivity along the witness orbit: min x = {pr.min_x:.6e}, min y = {pr.min_y:.6e}")
    rec.add("D3_subthreshold_arc", {
        "t_first": float(d["t"][idx[0]]), "t_last": float(d["t"][idx[-1]]),
        "n_mesh_points": int(len(idx)),
        "all_points_in_certified_extinction_region": bool(certified.all()),
        "x_range": [float(arc[:, 0].min()), float(arc[:, 0].max())],
        "y_range": [float(arc[:, 1].min()), float(arc[:, 1].max())],
        "z_deepest": [d["x_dip"], d["y_dip"]], "t_deepest": d["t_dip"],
        "positivity_min_x": pr.min_x, "positivity_min_y": pr.min_y,
    })
    rec.save_npz("witness_orbit", t=d["t"], x=d["x"], E=E, p=p,
                 arc_index=idx, arc=arc)

    # ---------------- D4: high-precision recomputation ----------------------
    Nmp = 2000
    Tmp = min(args.T, 200.0)
    traj = solve_mp(model.g_mp, [mp.mpf(str(p[0])), mp.mpf(str(p[1]))], args.alpha,
                    mp.mpf(str(Tmp)) / Nmp, Nmp, dps=30, method="pece")
    xs_mp = [float(row[0]) for row in traj]
    i_mp = int(np.argmin(xs_mp))
    f64 = orbit_diag(model, p, args.alpha, Tmp, Nmp, method="pece", stride=1)
    print(f"D4 mpmath dps=30 N={Nmp} T={Tmp}: min x = {xs_mp[i_mp]:.12f} at t={i_mp*Tmp/Nmp:.4f}; "
          f"float64 same mesh: {f64['x_dip']:.12f}  |diff|={abs(xs_mp[i_mp]-f64['x_dip']):.3e}")
    rec.add("D4_high_precision", {
        "dps": 30, "N": Nmp, "T": Tmp, "min_x_mp": xs_mp[i_mp],
        "t_min_mp": i_mp * Tmp / Nmp, "min_x_float64_same_mesh": f64["x_dip"],
        "abs_diff": abs(xs_mp[i_mp] - f64["x_dip"]),
        "margin_mp": model.theta - xs_mp[i_mp],
    })

    # ---------------- D5: collision Jacobian for H(p,z,t,0) ------------------
    z = np.array([d["x_dip"], d["y_dip"]])
    Jz = collision_jacobian(model, p, z, args.alpha, d["t_dip"], 0.0,
                            args.T / args.N, free=("p", "t"))
    print(f"D5 Jacobian of H(p,z,t,0) in {Jz['columns']}: singular values "
          f"{np.array2string(Jz['singular_values'], precision=4)} rank={Jz['rank']}")
    rec.add("D5_embedded_age_jacobian", {
        "columns": Jz["columns"], "singular_values": Jz["singular_values"].tolist(),
        "rank": Jz["rank"], "z": z.tolist(), "t": d["t_dip"],
        "note": "H(p,z,t,0) = x(t;p) - z.  In the variables (z) the Jacobian is -I, so the "
                "witness is automatically transversal; the interesting content is the rank in "
                "(p,t), reported here.",
    })

    # ---------------- D6: openness under perturbation -----------------------
    d6 = []
    base = dict(alpha=args.alpha, theta=model.theta, a=model.a, b=model.b, m=model.m,
                px=p[0], py=p[1])
    for key in ("alpha", "theta", "a", "b", "m", "px", "py"):
        for rel in (-0.05, -0.02, 0.02, 0.05):
            q = dict(base)
            q[key] = base[key] * (1.0 + rel)
            if key == "alpha" and not (0 < q["alpha"] < 1):
                continue
            mdl = make_model(args.family, q["theta"], q["a"], q["b"], q["m"])
            if not (mdl.theta < mdl.x_star < 1.0):
                d6.append({"perturbed": key, "rel": rel, "skipped": "no coexistence equilibrium"})
                continue
            dd = orbit_diag(mdl, [q["px"], q["py"]], q["alpha"], args.T, args.N,
                            method="pece", stride=max(1, args.N // 4000))
            surv = dd["tail_dE"] < 0.05 and dd["tail_dE"] <= 0.7 * dd["prev_dE"]
            d6.append({"perturbed": key, "rel": rel, "value": q[key],
                       "margin": dd["margin"], "survival_label": bool(surv),
                       "witness_persists": bool(surv and dd["margin"] > 0),
                       "tail_dE": dd["tail_dE"], "final": dd["final"]})
            print(f"D6 {key:6} {rel:+.0%} -> margin={dd['margin']:+.6f} survival={surv} "
                  f"persists={d6[-1]['witness_persists']}")
    rec.save_json("D6_openness", d6)
    tested = [r for r in d6 if "witness_persists" in r]
    rec.add("D6_persistence_fraction",
            float(np.mean([r["witness_persists"] for r in tested])) if tested else None)

    # ---------------- D7: same-age and cross-age collisions ------------------
    q_ext = np.array([min(0.5 * model.theta, 0.1), 0.1])   # certified extinction start
    print(f"D7 pairing witness p={p} (coexistence) with q={q_ext} "
          f"(certified extinction: {bool(cert(q_ext[None, :])[0])})")
    rp = solve(model, np.atleast_2d(p), args.alpha, args.T / args.N, args.N, method="pece",
               store=True, store_stride=4)
    rq = solve(model, np.atleast_2d(q_ext), args.alpha, args.T / args.N, args.N, method="pece",
               store=True, store_stride=4)
    xa, xb, tt = rp.x[:, 0, :], rq.x[:, 0, :], rp.t
    sa = same_age_collisions(tt, xa, xb)
    ca = cross_age_collisions(tt, xa, xb, max_hits=40)
    print(f"   same-age collisions: {len(sa)};  cross-age crossings: {len(ca)}")
    d7 = {"q_ext": q_ext.tolist(),
          "q_ext_certified_extinction": bool(cert(q_ext[None, :])[0]),
          "same_age": [{"t": t, "x": list(x), "residual": r} for t, x, r in sa],
          "cross_age": [{"t": t, "s": s, "x": list(x), "cos_angle": c} for t, s, x, c in ca[:20]]}
    refined = []
    for (tc, sc, xc, cang) in ca[:5]:
        res = refine_collision(model, p, q_ext, args.alpha, tc, sc, args.T / args.N)
        J = collision_jacobian(model, p, q_ext, args.alpha, res["t"], res["s"],
                               args.T / args.N, free=("p", "q", "t", "s"))
        refined.append({"t0": tc, "s0": sc, "t": res["t"], "s": res["s"],
                        "residual": res["residual"], "cos_angle_initial": cang,
                        "jacobian_columns": J["columns"],
                        "singular_values": J["singular_values"].tolist(),
                        "rank": J["rank"]})
        print(f"   refined cross-age: t={res['t']:.6f} s={res['s']:.6f} "
              f"|H|={res['residual']:.3e} rank={J['rank']} "
              f"sv={np.array2string(J['singular_values'], precision=3)}")
    d7["refined"] = refined
    rec.save_json("D7_collisions", d7)

    # ---------------- D8: the Caputo-specific mechanism, made explicit -------
    # On {0 < x < theta, y >= 0} the prey vector field is strictly negative:
    #     g_x = x(1-x)(x-theta) - a x y < 0 ,
    # so ^C D^a x(t) < 0 throughout the sub-threshold window.  For alpha = 1 a
    # strictly negative derivative forces x to decrease, x can never return to
    # theta, and (with x bounded below by 0) the orbit must go extinct: no
    # survival orbit can enter {x < theta}.  For 0 < alpha < 1 the implication
    # "^C D^a x < 0  =>  x decreasing" is FALSE, because the fixed lower terminal
    # makes d/dt I^a[phi] indefinite in sign even for phi <= 0.  The witness is a
    # direct, checkable instance: x rises from its minimum back through theta on
    # an interval where its Caputo derivative is strictly negative.
    gvals = model.g(d["x"])[:, 0]
    win = np.arange(int(np.argmin(d["x"][:, 0])), len(d["t"]))
    exit_rel = np.flatnonzero(d["x"][win, 0] >= model.theta)
    if len(exit_rel):
        win = win[: exit_rel[0] + 1]
    rise = float(d["x"][win[-1], 0] - d["x"][win[0], 0])
    gmax = float(np.nanmax(gvals[win]))
    mono = bool(np.all(np.diff(d["x"][win, 0]) > -1e-12))
    print(f"D8 recovery window t in [{d['t'][win[0]]:.4f}, {d['t'][win[-1]]:.4f}]: "
          f"x rises by {rise:+.6f} while max_t g_x = {gmax:.3e} (< 0 required); "
          f"x monotone increasing: {mono}")
    rec.add("D8_caputo_mechanism", {
        "t_start": float(d["t"][win[0]]), "t_end": float(d["t"][win[-1]]),
        "x_start": float(d["x"][win[0], 0]), "x_end": float(d["x"][win[-1], 0]),
        "x_rise": rise,
        "max_g_x_on_window": gmax,
        "caputo_derivative_strictly_negative_throughout": bool(gmax < 0),
        "x_monotone_increasing_on_window": mono,
        "integer_order_counterpart": "for alpha = 1, g_x < 0 forces x to decrease, so no "
                                     "survival orbit can enter {x < theta}: the phenomenon is "
                                     "specific to 0 < alpha < 1",
    })
    rec.save_npz("witness_mechanism", t=d["t"], x=d["x"], g_x=gvals, window=win)

    rec.add("conclusion", {
        "multibasin_fibre_witness": True,
        "extinction_side": "CERTIFIED-CONDITIONAL (Wu 2020 scalar Caputo comparison + "
                           "COROLLARY-S1A; requires positivity of the cone and theta < m/b)",
        "survival_side": "NUMERICAL CORROBORATION only - no rigorous memory-state trapping "
                         "region is established here",
        "overall_evidence_class": "NUMERICAL CORROBORATION (conditional certification on one side)",
    })
    print("\nmanifest:", rec.finish())


if __name__ == "__main__":
    main()
