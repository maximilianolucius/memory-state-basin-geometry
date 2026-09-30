#!/usr/bin/env python
"""TASK-0006 Stages B-D: rigorous oscillation-Banach radii constants for B215.

Pipeline (everything after the collocation is a rigorous upper bound):
  collocation (float) -> verify_cells (Arb cell boxes, defect sup/Lipschitz)
  -> rigorous hat weights (Arb) -> nodal rho, A_n (Arb) -> certified dense inverse
  -> theta-norm weights by fixed-point optimisation -> Y0, Z1, Z2, radii polynomial.

Usage: t6_stageBD_cap.py --T 1000 --N 6000 --mesh graded3|tail_h:<h>|uniform ...
"""
import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.aposteriori import collocation, graded_mesh                      # noqa: E402
from msbg.cap import (Geometry, cap_constants, cap_vectors, iterate_bounds, mean_kernel_blocks,   # noqa: E402
                      lipschitz_A, lipschitz_A_cells, nodal_data, power_iteration, rigorous_hat_weights,
                      rigorous_inverse, up)
from msbg.models import AlleePredatorPrey                                  # noqa: E402
from msbg.provenance import RunRecorder                                    # noqa: E402
from msbg.validated import verify_cells                                    # noqa: E402
from msbg.validated_res import Setup                                       # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make_mesh(kind, T, N):
    if kind == "graded3":
        return graded_mesh(T, N, 3.0)
    if kind == "uniform":
        return np.linspace(0.0, T, N + 1)
    if kind.startswith("hybrid:"):
        # graded r=3 on [0, T1] with N1 nodes, then uniform step to T
        _, T1, N1 = kind.split(":")
        T1, N1 = float(T1), int(N1)
        head = graded_mesh(T1, N1, 3.0)
        n_tail = N - N1
        tail = np.linspace(T1, T, n_tail + 1)[1:]
        return np.concatenate([head, tail])
    if kind.startswith("file:"):
        tm = np.load(kind.split(":", 1)[1])
        assert tm[0] == 0.0 and abs(tm[-1] - T) < 1e-9 and len(tm) == N + 1 and np.all(np.diff(tm) > 0)
        return tm
    if kind.startswith("tri:"):
        # graded r=3 on [0, T1] (N1 cells), geometric-ish graded r=2 on [T1, T2] (N2 cells),
        # uniform on [T2, T] with the remaining cells
        _, T1, N1, T2, N2 = kind.split(":")
        T1, N1, T2, N2 = float(T1), int(N1), float(T2), int(N2)
        head = graded_mesh(T1, N1, 3.0)
        mid = T1 + (T2 - T1) * (np.arange(N2 + 1) / N2) ** 2
        tail = np.linspace(T2, T, N - N1 - N2 + 1)
        return np.concatenate([head, mid[1:], tail[1:]])
    raise ValueError(kind)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, default=1000.0)
    ap.add_argument("--N", type=int, default=6000)
    ap.add_argument("--mesh", default="graded3")
    ap.add_argument("--K", type=int, default=32)
    ap.add_argument("--workers", type=int, default=80)
    ap.add_argument("--iters", type=int, default=300)
    ap.add_argument("--tube", type=float, default=1e-2, help="initial physical tube radius for D2")
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    np.seterr(all="ignore")
    t0 = time.time()

    def log(*a):
        print(f"[{time.time() - t0:8.1f}s]", *a, flush=True)

    st = Setup("1/2", "1/2", "1", "4/5", "17/20", ("277/100", "467/1000"))
    fl, pf = st.floats()
    al = fl["alpha"]
    model = AlleePredatorPrey(theta=fl["theta"], a=fl["a"], b=fl["b"], m=fl["m"])
    tag = args.tag or f"{args.mesh.replace(':', '_')}_T{int(args.T)}_N{args.N}"
    rec = RunRecorder(f"t6_stageBD_{tag}", ROOT)
    rec.add("args", vars(args))

    tm = make_mesh(args.mesh, args.T, args.N)
    N = len(tm) - 1
    h = np.diff(tm)
    log(f"mesh {args.mesh}: N={N}, h_min={h.min():.3g}, h_max={h.max():.3g}, T={tm[-1]}")
    X, PHI, M = collocation(model, np.array(pf), al, tm)
    log("collocation done")

    strs = dict(theta=st.str["theta"], a=st.str["a"], b=st.str["b"], m=st.str["m"],
                alpha=st.str["alpha"], p=st.str["p"])
    cells = verify_cells(tm, PHI, strs["theta"], strs["a"], strs["b"], strs["m"], strs["alpha"],
                         strs["p"], 0.0, prec=128, workers=args.workers, K=args.K)
    log(f"cells: R_max={cells.R.max():.3e} drho_max={cells.drho.max():.3e} "
        f"x in [{cells.x_lo.min():.4f},{cells.x_hi.max():.4f}]")

    Wm, Wr = rigorous_hat_weights(tm, strs["alpha"], workers=args.workers)
    log(f"hat weights: max rad {Wr.max():.2e}, row-sum max {np.abs(Wm).sum(1).max():.4g}")

    rho, Am, Ar, normA, oscA = nodal_data(tm, PHI, strs, cells.x_lo, cells.x_hi, cells.y_lo,
                                          cells.y_hi, workers=args.workers)
    log(f"nodal data: rho_node max {rho.max():.3e}, ||A|| max {normA.max():.4g}, "
        f"osc A max {oscA.max():.3e}, A rad max {Ar.max():.2e}")

    Rn, Dn, normE, delta, R4 = rigorous_inverse(Wm, Wr, Am, Ar)
    amp_row = Rn.sum(1)
    log(f"inverse: ||E||_inf={normE:.3e}, delta max {delta.max():.3e}, "
        f"row-sum max {amp_row.max():.4g} at t={tm[int(np.argmax(amp_row))]:.2f}, at T {amp_row[-1]:.4g}")
    rec.add("inverse", dict(normE=normE, delta_max=float(delta.max()),
                           rowsum_max=float(amp_row.max()), rowsum_T=float(amp_row[-1])))

    nSi2 = float(up(float(st.normSi) * np.sqrt(2.0)))
    # Lipschitz constant of A on the tube |e|_S <= rmax * Omega_max: Omega_max <= T^a/Gamma(a+1)
    from math import gamma
    tube_phys = args.tube
    D2g = lipschitz_A(st, cells.x_lo, cells.x_hi, cells.y_lo, cells.y_hi, tube_phys)
    D2 = lipschitz_A_cells(st, cells.x_lo, cells.x_hi, tube_phys)
    log(f"D2 per cell (adapted, tube {tube_phys:.3g}): max {D2.max():.4g}, at T {D2[-1]:.4g}; "
        f"global norm-product constant was {D2g:.4g}")

    xbox = dict(theta=fl["theta"], a=fl["a"], b=fl["b"], x_lo=float(cells.x_lo.min()),
                x_hi=float(cells.x_hi.max()))
    diam = up(np.sqrt((cells.x_hi - cells.x_lo) ** 2 + (cells.y_hi - cells.y_lo) ** 2))
    geo = Geometry(tm, al, PHI, float(st.normS), float(st.normSi), xbox, diam)
    log(f"geometry: c_alpha={geo.c_alpha:.4f} c_loc={geo.c_loc:.4f} c_prev in "
        f"[{geo.c_prev.min():.4f},{geo.c_prev.max():.4f}] D2p={geo.D2p:.3g} "
        f"EA max(n>=1) {np.nanmax(geo.EA[1:]):.3e} (green {np.max(geo.EA_green[1:]):.3e}) O1 max {np.max(geo.O1[1:]):.3e}")
    geo.Qn, geo.DQn = mean_kernel_blocks(R4, delta, Am, geo.w)
    del R4
    log(f"mean-kernel blocks Q: row-sum max {geo.Qn.sum(1).max():.4g}, at T {geo.Qn[-1].sum():.4g}; "
        f"rem row-sum max {geo.rem.sum(1).max():.4g}; (compare ||R|| ||A|| w row-sum "
        f"{(Rn @ (np.concatenate([[normA[0]], np.maximum(normA[:-1], normA[1:]), [normA[-1]]]) * geo.w.sum(1))).max():.4g})")
    rec.add("Q", dict(rowsum_max=float(geo.Qn.sum(1).max()), rem_rowsum_max=float(geo.rem.sum(1).max())))
    rec.add("geometry", dict(c_alpha=geo.c_alpha, c_loc=geo.c_loc, c_prev_max=float(geo.c_prev.max()),
                             D2p=float(geo.D2p), EA_max=float(np.max(geo.EA[1:]))))
    from scripts.t6_stageD_close import close
    rec.save_npz("blocks", Rn=Rn, Dn=Dn, rho=rho, normA=normA, oscA=oscA, tm=tm, R=cells.R,
                 drho=cells.drho, diam=diam, Qn=geo.Qn, DQn=geo.DQn,
                 x_lo=cells.x_lo, x_hi=cells.x_hi, y_lo=cells.y_lo, y_hi=cells.y_hi)
    results, bc = close(geo, Rn, Dn, rho, cells.R, cells.drho, normA, oscA, st, cells.x_lo, cells.x_hi,
                        rec, log, iters=args.iters, tube0=args.tube)
    rec.add("results", results)
    rec.add("mesh", dict(N=N, T=float(tm[-1]), h_min=float(h.min()), h_max=float(h.max())))
    rec.add("cells", dict(R_max=float(cells.R.max()), normA_max=float(normA.max()), oscA_max=float(oscA.max()),
                         rho_node_max=float(rho.max())))
    print(json.dumps(results, indent=1, default=float))
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
