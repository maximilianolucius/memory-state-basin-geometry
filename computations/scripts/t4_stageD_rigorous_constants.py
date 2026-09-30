#!/usr/bin/env python3
r"""TASK-0004 Stage D — rigorous K_J, C_r and the resulting threshold for M_T (witness W1).

Exact data:  theta = 3/10, a = b = 1, m = 4/5, alpha = 17/20,
    J = [[-6/25, -4/5], [1/10, 0]],   lambda = (-3 + i sqrt(41))/25,
    eigenvector v = (J12, lambda - J11) = (-4/5, (3 + i sqrt(41))/25),
    S = [Re v, -Im v] = [[-4/5, 0], [3/25, -sqrt(41)/25]],   J S = S [[mu,-nu],[nu,mu]].

Adapted norm  |u|_S := |S^{-1} u|_2.  In it  Psi_J(s) = S R(s) S^{-1} with R(s) the
real 2x2 form of the complex number psi_lambda(s), so the induced norm of Psi_J(s)
is EXACTLY |psi_lambda(s)| and  K_J = int_0^inf |psi_lambda|.

Outputs (all rigorous upper/lower bounds):
    K_up   >= K_J
    C0, c3 with  |N(u)|_S <= (C0 + c3 r) |u|_S^2  for |u|_S <= r
    M_star := max_r [ r - K_up (C0 + c3 r) r^2 ]  evaluated at a rational r_star.
M1 then certifies survival as soon as a rigorous  M_T < M_star  is available.

Evidence class: CERTIFIED COMPUTATION for the constants, conditional on the
Mittag-Leffler integral representation stated in msbg/kernel_bound.py.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flint import arb, ctx, fmpq                       # noqa: E402
from msbg.kernel_bound import kernel_bound             # noqa: E402
from msbg.provenance import RunRecorder                # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def nonlinearity_constants(n_arcs=20000):
    ctx.prec = 128
    s41 = arb(41).sqrt()
    S = [[arb(-4) / 5, arb(0)], [arb(3) / 25, -s41 / 25]]
    det = S[0][0] * S[1][1] - S[0][1] * S[1][0]
    Si = [[S[1][1] / det, -S[0][1] / det], [-S[1][0] / det, S[0][0] / det]]
    c2 = arb(11) / 10          # 3 x* - 1 - theta = 12/5 - 13/10
    a_, b_ = arb(1), arb(1)
    two_pi = 2 * arb.pi()
    C0 = 0.0
    c3 = 0.0
    half = two_pi / (2 * n_arcs)
    for k in range(n_arcs):
        th = arb((two_pi * (2 * k + 1) / (2 * n_arcs)).mid(), half.abs_upper())
        xi = (th.cos(), th.sin())
        u1 = S[0][0] * xi[0] + S[0][1] * xi[1]
        u2 = S[1][0] * xi[0] + S[1][1] * xi[1]
        n2 = (-c2 * u1 * u1 - a_ * u1 * u2, b_ * u1 * u2)
        n3 = (-u1 * u1 * u1, arb(0))
        q2 = (Si[0][0] * n2[0] + Si[0][1] * n2[1], Si[1][0] * n2[0] + Si[1][1] * n2[1])
        q3 = (Si[0][0] * n3[0] + Si[0][1] * n3[1], Si[1][0] * n3[0] + Si[1][1] * n3[1])
        C0 = max(C0, float((q2[0] * q2[0] + q2[1] * q2[1]).sqrt().abs_upper()))
        c3 = max(c3, float((q3[0] * q3[0] + q3[1] * q3[1]).sqrt().abs_upper()))
    return C0 * (1 + 1e-15), c3 * (1 + 1e-15), S, Si


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--rho0", type=float, default=200.0)
    args = ap.parse_args()
    rec = RunRecorder("t4_stageD", ROOT)
    ctx.prec = 128
    spec = ("17/20", "-3/25", "41/625")          # lambda = -3/25 + i sqrt(41)/25, exact
    out = {}
    for rho0 in (args.rho0, 2 * args.rho0):
        kb = kernel_bound(spec, rho0=rho0, workers=args.workers)
        out[rho0] = kb
        print(f"rho0={rho0:7.1f}: K_upper = {kb['K_upper']:.6f}   (finite {kb['finite_part_upper']:.6f}, "
              f"midpoint sum {kb['finite_part_midpoint_sum']:.6f}, tail {kb['tail_upper']:.6f}; "
              f"{kb['n_cells']} cells)", flush=True)
    kb = min(out.values(), key=lambda d: d["K_upper"])
    K_up = kb["K_upper"]
    C0, c3, S, Si = nonlinearity_constants()
    print(f"C_r = {C0:.6f} + {c3:.6f} r   (adapted norm, rigorous upper bounds)")
    # threshold
    Ka, C0a, c3a = arb(K_up), arb(C0), arb(c3)
    best = None
    for num in range(200, 1200):
        r = arb(fmpq(num, 10000))
        m = r - Ka * (C0a + c3a * r) * r * r
        lo = float(m.lower())
        if best is None or lo > best[0]:
            best = (lo, num, float((Ka * (C0a + c3a * r) * r).abs_upper()))
    M_star, num, KCr = best
    print(f"M_star >= {M_star:.6f}  at r_star = {num}/10000,  K C_r r_star <= {KCr:.4f}  (< 1 required)")
    print(f"numerical M_T (adapted norm, TASK-0004 Stage A): T=500: 2.092e-2, T=1000: 1.171e-2, "
          f"T=2000: 6.531e-3")
    rec.add("K_bounds_by_rho0", out)
    rec.add("K_upper", K_up)
    rec.add("C_r", {"C0": C0, "c3": c3})
    rec.add("M_star_lower", M_star)
    rec.add("r_star", f"{num}/10000")
    rec.add("K_C_r_upper_at_r_star", KCr)
    rec.add("lambda", "(-3 + i sqrt(41))/25")
    rec.add("norm", "|u|_S = |S^{-1} u|_2, S = [[-4/5, 0],[3/25, -sqrt(41)/25]]")
    rec.add("evidence_class", "CERTIFIED COMPUTATION, conditional on the Mittag-Leffler "
                              "integral representation (msbg/kernel_bound.py)")
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
