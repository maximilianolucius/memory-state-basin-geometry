#!/usr/bin/env python3
"""TASK-0003 Stage E — diagnostic: the quantity that decides feasibility.

For the certificate to accommodate an orbit that reaches the threshold, the ball
radius must satisfy w1 r > g, and convergence needs 2 K C(r) r < 1.  Since C(r) r
is increasing in r, a NECESSARY condition is

    q := min over weights of  2 K(w) C(g/w1) (g/w1)  <  1 .

Two versions are reported: q_true with K = numerical int ||Psi||_w, and q_lower
with K replaced by its exact lower bound ||J^{-1}||_w  (since
int_0^inf Psi = -J^{-1}).  q_lower >= 1 is therefore an obstruction that does not
depend on the numerical kernel at all.
"""
import itertools
import os
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.provenance import RunRecorder                     # noqa: E402
from msbg.solvers import solve                              # noqa: E402
from scripts.t3_stageE_overshoot_feasibility import Lin     # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def one(cfg):
    np.seterr(all="ignore")
    theta, frac, a, b, alpha, T, h = cfg
    xs = theta + frac * (1 - theta)
    ys = (1 - xs) * (xs - theta) / a
    g = xs - theta
    J = np.array([[xs * (1 + theta - 2 * xs), -a * xs], [b * ys, 0.0]])
    lam = np.linalg.eigvals(J)
    matignon = float(np.min(np.abs(np.angle(lam)))) - alpha * np.pi / 2
    if not (theta < xs < 1) or matignon <= 0.02:
        return None
    hurwitz = bool(np.all(lam.real < 0))
    N = int(round(T / h))
    Wc = []
    for j in range(2):
        rW = solve(Lin(J, np.eye(2)[j]), np.zeros((1, 2)), alpha, h, N, method="pece", store=True)
        Wc.append(rW.x[:, 0, :])
    W = np.stack(Wc, axis=1)
    dW = np.abs(np.diff(W, axis=0))
    Jinv = np.linalg.inv(J)
    # consistency of the kernel: W(T) -> -J^{-1}
    kern_check = float(np.max(np.abs(W[-1].T + Jinv)) / np.max(np.abs(Jinv)))
    c2 = abs(3 * xs - 1 - theta)
    best_true, best_low = np.inf, np.inf
    for omega in np.geomspace(1e-4, 1e4, 161):
        w = np.array([1.0, omega])
        kern = np.einsum("tji,j->ti", dW, w) / w[None, :]
        K = float(np.max(np.sum(kern, axis=0)))            # finite-horizon LOWER estimate
        Kl = float(np.max(np.abs(Jinv) @ w / w))
        C = max(c2 + a * omega + g, b)
        best_true = min(best_true, 2 * K * C * g)
        best_low = min(best_low, 2 * Kl * C * g)
    return {"theta": theta, "frac": frac, "a": a, "b": b, "alpha": alpha, "x_star": xs,
            "gap": g, "q_true": best_true, "q_lower": best_low, "kernel_check": kern_check,
            "trace": float(J[0, 0]), "det": float(np.linalg.det(J)), "hurwitz": hurwitz,
            "matignon_margin": matignon, "c2": float(3 * xs - 1 - theta)}


def main():
    thetas = [0.1, 0.3, 0.5, 0.7, 0.9]
    fracs = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.505, 0.55, 0.6, 0.7, 0.85]
    aa = [0.25, 1.0, 4.0]
    bb = [0.01, 0.05, 0.25, 1.0, 4.0]
    alphas = [0.5, 0.7, 0.85, 0.95]
    cfgs = [(th, f, a, b, al, 2000.0, 0.05)
            for th, f, a, b, al in itertools.product(thetas, fracs, aa, bb, alphas)]
    rec = RunRecorder("t3_stageE_diag", ROOT)
    with ProcessPoolExecutor(max_workers=160) as ex:
        rows = [r for r in ex.map(one, cfgs, chunksize=2) if r is not None]
    for tag, sel in (("Hurwitz", [r for r in rows if r["hurwitz"]]),
                     ("Matignon-only (not Hurwitz)", [r for r in rows if not r["hurwitz"]])):
        if sel:
            a_ = np.array([r["q_lower"] for r in sel]); b_ = np.array([r["q_true"] for r in sel])
            print(f"{tag}: n={len(sel)}  q_lower min {a_.min():.4f} (<1: {(a_<1).sum()})   "
                  f"q_true min {b_.min():.4f} (<1: {(b_<1).sum()})")
    rows_conv = [r for r in rows if r["kernel_check"] < 0.05]
    print(f"configs with converged kernel (check < 5%): {len(rows_conv)}; among them q_true<1: "
          f"{sum(1 for r in rows_conv if r['q_true'] < 1)}, max(q_true, q_lower)<1: "
          f"{sum(1 for r in rows_conv if max(r['q_true'], r['q_lower']) < 1)}")
    rows_conv.sort(key=lambda r: max(r["q_true"], r["q_lower"]))
    for r in rows_conv[:8]:
        print(f"   theta={r['theta']} x*={r['x_star']:.3f} a={r['a']} b={r['b']} alpha={r['alpha']} "
              f"hurwitz={r['hurwitz']} c2={r['c2']:+.3f} q_true={r['q_true']:.3f} "
              f"q_lower={r['q_lower']:.3f} kernel_check={r['kernel_check']:.3f}")
    ql = np.array([r["q_lower"] for r in rows])
    qt = np.array([r["q_true"] for r in rows])
    print(f"configs {len(rows)}")
    print(f"q_lower (kernel-free obstruction):  min {ql.min():.4f}  median {np.median(ql):.3f}  "
          f"count < 1: {(ql < 1).sum()}")
    print(f"q_true  (numerical kernel):         min {qt.min():.4f}  median {np.median(qt):.3f}  "
          f"count < 1: {(qt < 1).sum()}")
    print(f"kernel consistency |W(T) + J^-1| / |J^-1|: max {max(r['kernel_check'] for r in rows):.3e}")
    rows.sort(key=lambda r: r["q_true"])
    print(f"{'theta':>6}{'frac':>7}{'a':>6}{'b':>6}{'alpha':>6}{'q_true':>9}{'q_lower':>9}{'trace':>10}")
    for r in rows[:10]:
        print(f"{r['theta']:6}{r['frac']:7}{r['a']:6}{r['b']:6}{r['alpha']:6}{r['q_true']:9.4f}"
              f"{r['q_lower']:9.4f}{r['trace']:10.4f}")
    rec.save_json("rows", rows)
    rec.add("min_q_lower", float(ql.min()))
    rec.add("min_q_true", float(qt.min()))
    rec.add("n_q_lower_below_1", int((ql < 1).sum()))
    rec.add("n_q_true_below_1", int((qt < 1).sum()))
    rec.add("evidence_class", "NUMERICAL EXPLORATION")
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
