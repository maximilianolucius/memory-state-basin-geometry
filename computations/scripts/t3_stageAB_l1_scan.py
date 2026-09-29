#!/usr/bin/env python3
r"""TASK-0003 Stage A/B — exact-rational L1 certificates over a rational parameter grid.

For every Hurwitz parameter set the script produces the exact P, Arb enclosures
of lam_min(P), ||P||_2, C_r, a rational r_cert for which the L1 inequality
2 ||P|| C_r r <= 1/2 is VERIFIED, and the extent of the certified ellipsoid Omega
in the x direction.

Falsification role.  THEOREM X1 (proved) puts every cold start of
R_ext = {0 < x < theta, y >= 0} in the extinction basin.  CANDIDATE-L1 puts every
cold start of Omega in the survival basin.  So Omega must not meet R_ext; a single
parameter set with  x* - x_extent(Omega) <= theta  would refute L1 as stated.
The column ``extent/gap`` measures how far L1 is from even reaching the threshold.

Evidence class: CERTIFIED COMPUTATION (exact rational arithmetic + Arb) for the
constants; the basin conclusion itself is L1-CONDITIONAL.
"""
import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flint import fmpq                                    # noqa: E402
from msbg.lyapunov_l1 import Q, l1_certificate            # noqa: E402
from msbg.provenance import RunRecorder                   # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    thetas = ["1/10", "1/5", "3/10", "2/5", "1/2", "3/5", "7/10", "4/5", "9/10", "19/20"]
    fracs = ["11/20", "3/5", "7/10", "4/5", "9/10", "19/20"]   # x* = theta + f (1 - theta)
    aa = ["1/4", "1/2", "1", "2", "4"]
    bb = ["1/4", "1/2", "1", "2", "4"]
    rec = RunRecorder("t3_l1_scan", ROOT)
    rows = []
    for th, f, a, b in itertools.product(thetas, fracs, aa, bb):
        thq, fq = Q(th), Q(f)
        xs = thq + fq * (1 - thq)
        m = xs * Q(b)
        c = l1_certificate(thq, a, b, m)
        if not c.hurwitz:
            rows.append({"theta": th, "frac": f, "a": a, "b": b, "m": str(m), "hurwitz": False})
            continue
        rows.append({
            "theta": th, "frac": f, "a": a, "b": b, "m": str(m), "hurwitz": True,
            "x_star": str(c.x_star), "y_star": str(c.y_star),
            "trace": str(c.trace), "det": str(c.det),
            "P": [[str(v) for v in r] for r in c.P],
            "lam_min": c.lam_min.str(12), "lam_max": c.lam_max.str(12),
            "r_cert": str(c.r_cert), "r_cert_float": float(c.r_cert.p) / float(c.r_cert.q),
            "C_r": c.C_r.str(12), "lhs": c.lhs.str(12),
            "x_extent": c.x_extent.str(12), "y_extent": c.y_extent.str(12),
            "gap": str(c.gap), "extent_over_gap": c.ratio_extent_gap,
            "omega_avoids_strip": c.omega_avoids_strip,
        })
    H = [r for r in rows if r["hurwitz"]]
    H.sort(key=lambda r: -r["extent_over_gap"])
    print(f"parameter sets: {len(rows)}  Hurwitz: {len(H)}")
    print(f"sets where Omega reaches the strip (would refute L1): "
          f"{sum(1 for r in H if not r['omega_avoids_strip'])}")
    print(f"max extent/gap = {H[0]['extent_over_gap']:.5f}   "
          f"median = {H[len(H)//2]['extent_over_gap']:.5f}   min = {H[-1]['extent_over_gap']:.2e}")
    print(f"\n{'theta':>6}{'x*':>8}{'a':>5}{'b':>5}{'r_cert':>11}{'|P|':>10}{'x_ext':>11}"
          f"{'gap':>8}{'ext/gap':>9}")
    for r in H[:12]:
        print(f"{r['theta']:>6}{r['x_star']:>8}{r['a']:>5}{r['b']:>5}{r['r_cert_float']:11.3e}"
              f"{float(r['lam_max'].split()[0].strip('[')):10.2f}"
              f"{float(r['x_extent'].split()[0].strip('[')):11.3e}{r['gap']:>8}"
              f"{r['extent_over_gap']:9.5f}")
    by_theta = {}
    for r in H:
        by_theta[r["theta"]] = max(by_theta.get(r["theta"], 0.0), r["extent_over_gap"])
    print("\nbest extent/gap by theta:", {k: round(v, 5) for k, v in by_theta.items()})
    rec.save_json("rows", rows)
    rec.add("n_sets", len(rows))
    rec.add("n_hurwitz", len(H))
    rec.add("n_omega_reaching_strip", sum(1 for r in H if not r["omega_avoids_strip"]))
    rec.add("max_extent_over_gap", H[0]["extent_over_gap"])
    rec.add("best", H[:10])
    rec.add("best_extent_over_gap_by_theta", by_theta)
    rec.add("evidence_class", "CERTIFIED COMPUTATION (exact rationals + Arb); basin claim L1-CONDITIONAL")
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
