#!/usr/bin/env python3
r"""TASK-0004 — which witness is the cheapest to certify end to end?

For every confirmed witness of TASK-0002 Stage B, and for W1, this computes

  * log10 A_R(T): amplification of the J-resolvent error recursion up to T
    (kernel ||Psi_J(t-s)||, coefficient ||Dg(x(s)) - J||), in the adapted norm;
    the defect of any rigorous history on [0,T] has to beat 10^{-log10 A_R};
  * K_J (adapted norm, numerical), C0 (adapted, numerical);
  * M_T ~ sup_{t in [T, T_end]} |u(t)|_S as a proxy for the linear response
    (Stage A showed v_T and u differ by O(K C |u|^2));
  * the M1 threshold 1/(4 K_J C0) and whether M_T is below it.

Evidence class: NUMERICAL EXPLORATION.
"""
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from math import gamma

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.memory_tail import psi_scalar            # noqa: E402
from msbg.models import AlleePredatorPrey          # noqa: E402
from msbg.provenance import RunRecorder            # noqa: E402
from msbg.solvers import solve                     # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def one(job):
    np.seterr(all="ignore")
    label, theta, a, b, m, alpha, p = job
    T_end, h = 1200.0, 0.04
    model = AlleePredatorPrey(theta=theta, a=a, b=b, m=m)
    E = np.array([model.x_star, model.y_star])
    J = model.jac(E[None, :])[0]
    lam, V = np.linalg.eig(J)
    if abs(lam[0].imag) < 1e-12:
        return {"label": label, "skipped": "real eigenvalues (adapted complex norm not defined)"}
    k = int(np.argmax(lam.imag))
    l, v = lam[k], V[:, k]
    if abs(np.angle(l)) <= alpha * np.pi / 2 + 0.02:
        return {"label": label, "skipped": "not Matignon stable"}
    S = np.column_stack([v.real, -v.imag])
    Si = np.linalg.inv(S)
    N = int(round(T_end / h))
    r = solve(model, np.atleast_2d(p), alpha, h, N, method="pece", store=True)
    x, t = r.x[:, 0, :], r.t
    if not np.isfinite(x).all():
        return {"label": label, "skipped": "orbit not finite"}
    u = x - E
    us = np.linalg.norm(u @ Si.T, axis=1)
    Dg = model.jac(x)
    # adapted induced norm of Dg - J :  || S^{-1} (Dg - J) S ||_2
    A = np.einsum("ij,tjk,kl->til", Si, Dg - J[None], S)
    a_res = np.linalg.norm(A, ord=2, axis=(1, 2))
    smid = (np.arange(N) + 0.5) * h
    sg = np.geomspace(smid[0], smid[-1], 260)
    pg = np.array([abs(complex(psi_scalar(alpha, complex(l), float(s), dps=16))) for s in sg])
    kern = np.exp(np.interp(np.log(smid), np.log(sg), np.log(pg))) * h
    kern[0] = h**alpha / gamma(alpha + 1)
    K = float(np.sum(0.5 * (pg[1:] * sg[1:] + pg[:-1] * sg[:-1]) * np.diff(np.log(sg)))
              + pg[0] * sg[0] / alpha + abs(l) ** -2 * sg[-1] ** (-alpha) / gamma(1 - alpha))
    w = np.ones(N + 1)
    scale = 0.0
    marks = {}
    sup_log = 0.0
    t_sup = 0.0
    for n in range(1, N + 1):
        w[n] = np.exp(-scale) + np.dot(kern[n - 1::-1], a_res[:n] * w[:n])
        lw = float(np.log10(w[n]) + scale / np.log(10))
        if lw > sup_log and n * h <= 1000.0:
            sup_log, t_sup = lw, n * h
        if w[n] > 1e100:
            w[: n + 1] /= 1e100
            scale += np.log(1e100)
        for T in (300.0, 600.0, 1000.0):
            if n == int(round(T / h)):
                marks[T] = float(np.log10(w[n]) + scale / np.log(10))
    ang = np.linspace(0, 2 * np.pi, 721)
    xi = np.stack([np.cos(ang), np.sin(ang)], 1)
    uu = xi @ S.T
    c2 = 3 * model.x_star - 1 - theta
    N2 = np.stack([-c2 * uu[:, 0] ** 2 - a * uu[:, 0] * uu[:, 1], b * uu[:, 0] * uu[:, 1]], 1)
    C0 = float(np.max(np.linalg.norm(N2 @ Si.T, axis=1)))
    thr = 1.0 / (4 * K * C0)
    out = {"label": label, "theta": theta, "a": a, "b": b, "m": m, "alpha": alpha,
           "p": list(map(float, p)), "dist_p_E": float(np.linalg.norm(np.asarray(p) - E)),
           "hurwitz": bool(np.all(lam.real < 0)), "K_adapted": K, "C0_adapted": C0,
           "M1_threshold": thr, "log10_A_R": marks,
           "sup_log10_A_R": sup_log, "t_of_sup": t_sup,
           "max_speed": float(np.max(np.abs(np.diff(x, axis=0))) / h),
           "min_x_minus_theta": float(np.min(x[:, 0]) - theta)}
    for T in (300.0, 600.0, 1000.0):
        n = int(round(T / h))
        out[f"M_proxy_T{int(T)}"] = float(np.max(us[n:]))
        out[f"M1_feasible_T{int(T)}"] = bool(np.max(us[n:]) < thr)
    return out


def main():
    ph2 = json.load(open(os.path.join(ROOT, "data", "t2_stageB_phase2.json")))
    jobs = [("W1", 0.3, 1.0, 1.0, 0.8, 0.85, [2.4372, 2.012])]
    for i, r in enumerate(ph2):
        if r["witness"]:
            jobs.append((f"B{i}", r["theta"], r["a"], 1.0, r["theta"] + r["gap"], r["alpha"], r["p"]))
    print(f"witnesses: {len(jobs)}", flush=True)
    rec = RunRecorder("t4_witness_scan", ROOT)
    with ProcessPoolExecutor(max_workers=150) as ex:
        rows = list(ex.map(one, jobs, chunksize=1))
    ok = [r for r in rows if "skipped" not in r]
    feas = [r for r in ok if r["M1_feasible_T1000"]]
    print(f"usable: {len(ok)} (skipped {len(rows)-len(ok)});  M1-feasible at T=1000: {len(feas)}")
    # The first version ranked by the amplification AT T = 1000.  The verifier's bootstrap
    # needs the SUPREMUM over [0, T]; the amplification peaks during the excursion and
    # decays afterwards, so the old ranking understated the requirement by up to 4 orders.
    feas.sort(key=lambda r: r["sup_log10_A_R"])
    print(f"{'label':>6}{'theta':>6}{'m':>6}{'a':>5}{'alpha':>6}{'|p-E*|':>8}{'Hurw':>6}{'K':>8}"
          f"{'thr':>9}{'M(1000)':>10}{'SUP log10A':>12}{'log10A(1000)':>13}{'entry':>9}")
    for r in feas[:14] + [q for q in ok if q["label"] == "W1"]:
        print(f"{r['label']:>6}{r['theta']:6}{r['m']:6.2f}{r['a']:5}{r['alpha']:6}{r['dist_p_E']:8.3f}"
              f"{str(r['hurwitz']):>6}{r['K_adapted']:8.2f}{r['M1_threshold']:9.4f}"
              f"{r['M_proxy_T1000']:10.2e}{r['sup_log10_A_R']:12.2f}{r['log10_A_R'][1000.0]:13.2f}"
              f"{-r['min_x_minus_theta']:9.4f}")
    la = np.array([r["sup_log10_A_R"] for r in feas]) if feas else np.array([])
    if len(la):
        for em in (0.0, 0.01, 0.02):
            sel = [r["sup_log10_A_R"] for r in feas if -r["min_x_minus_theta"] >= em]
            if sel:
                print(f"entry margin >= {em}: {len(sel)} witnesses, min SUP log10 A = {min(sel):.2f}")
        print(f"\nSUP log10 A_R among M1-feasible witnesses: min {la.min():.2f}, "
              f"median {np.median(la):.2f}, max {la.max():.2f}")
    rec.save_json("rows", rows)
    rec.add("n_usable", len(ok))
    rec.add("n_M1_feasible_T1000", len(feas))
    rec.add("min_sup_log10_A_R_among_feasible", float(la.min()) if len(la) else None)
    rec.add("evidence_class", "NUMERICAL EXPLORATION")
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
