#!/usr/bin/env python3
"""TASK-0004 — rigorous recursion versus tube radius, on the stored B54 cell data.

The bootstrap needs  max U < r.  A large r inflates a_n = sup ||S^{-1}(Dg - J)S|| on the
tube; after recovery the recursion is a contraction only if  K_J * a_tail < 1, and a_tail
is bounded below by (second derivative) x (tube radius).  So r cannot be large.  A small
r needs a small U, i.e. a small defect.  This script measures both sides rigorously.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.provenance import RunRecorder                                         # noqa: E402
from msbg.validated_res import (Setup, cell_coefficients, kernel_integrator,    # noqa: E402
                                resolvent_recursion, up)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    st = Setup("1/2", "1", "1", "4/5", "3/4", ("1554/1000", "3344/10000"))
    d = np.load(os.path.join(ROOT, "data", "t4_certificate_B54_arrays.npz"))
    tm, Rs = d["tm"], d["Rs"]
    ker = kernel_integrator(st, float(tm[-1]), workers=160)
    K_up = ker.total_upper(st)
    rec = RunRecorder("t4_tube_sweep", ROOT)
    rows = []
    print(f"K_up = {K_up:.4f};  defect: max Rs = {Rs.max():.3e}")
    print(f"{'r':>9}{'a_tail(T)':>11}{'K a_tail':>10}{'max a':>8}{'max D':>11}{'max U':>12}"
          f"{'U/D':>11}{'t of max U':>12}{'bootstrap':>10}")
    for r in (2e-2, 5e-3, 2e-3, 1e-3, 3e-4, 1e-4, 1e-5):
        pad = float(up(st.normS * r))
        a = cell_coefficients(st, d["x_lo"], d["x_hi"], d["y_lo"], d["y_hi"], pad, workers=160)
        U, D, kap = resolvent_recursion(tm, Rs, a, ker, sub=4)
        fin = np.isfinite(U).all()
        mu = float(np.max(U)) if fin else float("inf")
        k = int(np.argmax(U)) if fin else -1
        rows.append({"r": r, "a_tail": float(a[-1]), "K_a_tail": float(K_up * a[-1]),
                     "max_a": float(a.max()), "max_D": float(D.max()), "max_U": mu,
                     "ratio": mu / float(D.max()), "t_of_max_U": float(tm[k]) if fin else None,
                     "bootstrap": bool(fin and mu < r)})
        print(f"{r:9.0e}{a[-1]:11.4f}{K_up*a[-1]:10.3f}{a.max():8.3f}{D.max():11.3e}{mu:12.3e}"
              f"{mu/D.max():11.3e}{(tm[k] if fin else float('nan')):12.2f}"
              f"{str(bool(fin and mu < r)):>10}", flush=True)
    rec.add("rows", rows)
    rec.add("K_up", K_up)
    rec.add("evidence_class", "CERTIFIED bounds; the verdict of every row is UNDECIDED unless bootstrap")
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
