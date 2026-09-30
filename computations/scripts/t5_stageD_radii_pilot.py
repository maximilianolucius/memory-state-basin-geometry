#!/usr/bin/env python3
r"""TASK-0005 Stage D — approximate-inverse / radii-polynomial PILOT quantities.

Discrete setting on the graded mesh (nodal errors e_n in adapted coordinates):
    L_h e = d ,   L_h = I - W A     (hat-function weights W, A_j = S^{-1} Dg(xhat_j) S).
B := L_h^{-1} computed as a DENSE block inverse by forward substitution on the
identity (all 2(N+1) columns at once, BLAS).  Then, with R_{n,j} the 2x2 blocks:

  Y_n      = sum_j ||R_{n,j}||  Rs_j              rigorous cell defects Rs_j (TASK-0002 verifier,
                                                   converted to the adapted norm)
  Z2_n(r)  = sum_k ||R_{n,k}|| sum_j W_{k,j} C(r_j) r_j^2   cellwise radii r_j
  Y_MT     = sum_j ||(ell_T B)_j|| Rs_j            goal-oriented, ell_T the M_T functional

Newton-Kantorowich / radii form with CELLWISE radii:  r_n = 2 Y_n  and the check
    Y_n + Z2_n(r) + Z1 r_n  <  r_n   for all n,
reported as the Z1 BUDGET  (1 - (Y_n + Z2_n)/r_n)  that the operator-tail term
||I - B L_xhat|| would have to satisfy.  Z1 is NOT computed here: it is the
interpolation/off-grid remainder that ROUND-0006 is asked to formalise, and it is
left explicit.

Float sanity of B:  ||L_h B - I||_max  is reported.
Evidence class: pilot quantities.  Rs_j are CERTIFIED; everything else is float.
"""
import argparse
import os
import sys
import time
from math import gamma

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.aposteriori import collocation, graded_mesh                    # noqa: E402
from msbg.memory_tail import psi_scalar                                 # noqa: E402
from msbg.models import AlleePredatorPrey                               # noqa: E402
from msbg.orbit_linearized import hat_weights                           # noqa: E402
from msbg.provenance import RunRecorder                                 # noqa: E402
from msbg.validated import verify_cells                                 # noqa: E402
from msbg.validated_res import Setup, adapted_C, kernel_integrator, up  # noqa: E402
from scripts.t5_stageA_signaware import hat_row_at                      # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def dense_inverse(W, A):
    """R = L_h^{-1} as (N+1, 2, N+1, 2) via forward substitution on the identity."""
    N1 = W.shape[0]
    m = 2 * N1
    E = np.zeros((N1, 2, m))          # E[n] = rows of L^{-1} for state n, all columns
    AE = np.zeros((N1, 2, m))
    I = np.eye(2)
    for n in range(N1):
        rhs = np.zeros((2, m))
        rhs[0, 2 * n] = 1.0
        rhs[1, 2 * n + 1] = 1.0
        if n:
            rhs += np.tensordot(W[n, :n], AE[:n], axes=(0, 0))
        E[n] = np.linalg.solve(I - W[n, n] * A[n], rhs)
        AE[n] = A[n] @ E[n]
    return E.reshape(N1, 2, N1, 2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cand", default="W1")
    ap.add_argument("--T", type=float, default=1000.0)
    ap.add_argument("--N", type=int, default=6000)
    ap.add_argument("--K", type=int, default=32)
    ap.add_argument("--workers", type=int, default=160)
    args = ap.parse_args()
    np.seterr(all="ignore")
    specs = {"W1": ("3/10", "1", "1", "4/5", "17/20", ("6093/2500", "503/250")),
             "B215": ("1/2", "1/2", "1", "4/5", "17/20", ("277/100", "467/1000")),
             "B154": ("1/2", "1/2", "1", "4/5", "17/20", ("232/100", "1016/1000"))}
    st = Setup(*specs[args.cand])
    fl, pf = st.floats()
    al = fl["alpha"]
    model = AlleePredatorPrey(theta=fl["theta"], a=fl["a"], b=fl["b"], m=fl["m"])
    rec = RunRecorder(f"t5_stageD_{args.cand}", ROOT)
    tm = graded_mesh(args.T, args.N, 3.0)
    X, PHI, M = collocation(model, np.array(pf), al, tm)
    N = args.N

    t0 = time.time()
    cells = verify_cells(tm, PHI, st.str["theta"], st.str["a"], st.str["b"], st.str["m"],
                         st.str["alpha"], st.str["p"], 1e-3, prec=128, workers=args.workers, K=args.K)
    Rs = up(st.normSi * np.sqrt(2.0) * cells.R)          # rigorous, adapted norm
    Rs_n = np.concatenate([Rs, [Rs[-1]]])
    print(f"[cells] {time.time()-t0:.0f}s  rigorous defect: max {Rs.max():.3e}, "
          f"t<1: {Rs[tm[:-1]<1].max():.2e}, 1<t<60: {Rs[(tm[:-1]>=1)&(tm[:-1]<60)].max():.2e}, "
          f"t>60: {Rs[tm[:-1]>=60].max():.2e}", flush=True)

    S = np.array([[float(v.mid()) for v in row] for row in st.S_arb])
    Si = np.linalg.inv(S)
    A = np.einsum("ij,njk,kl->nil", Si, model.jac(X), S)
    W = hat_weights(tm, al)
    t1 = time.time()
    R = dense_inverse(W, A)
    print(f"[inverse] {time.time()-t1:.0f}s", flush=True)
    # sanity: L_h R = I
    LR = R.reshape(N + 1, 2, -1).copy()
    AR = np.einsum("nij,njm->nim", A, R.reshape(N + 1, 2, -1))
    LR = LR - np.tensordot(W, AR, axes=(1, 0))
    LR = LR.reshape(N + 1, 2, N + 1, 2)
    idx = np.arange(N + 1)
    LR[idx, :, idx, :] -= np.eye(2)
    resid = float(np.max(np.abs(LR)))
    del LR, AR
    Rn = np.sqrt(np.einsum("nikl->nk", R * R))            # Frobenius per block  (N+1, N+1)
    amp = Rn.sum(axis=1)
    Y = Rn @ Rs_n
    print(f"||L_h B - I||_max = {resid:.2e};  sup_n sum_j||R_nj|| = {amp.max():.2f} at t = "
          f"{tm[int(amp.argmax())]:.1f};  Y = max_n Y_n = {Y.max():.3e} at t = {tm[int(Y.argmax())]:.1f}",
          flush=True)

    # cellwise radii fixed point:  r_n = 2 Y_n ;  Z2_n = sum_k ||R_nk|| sum_j W_kj C(r_j) r_j^2
    C0, c3 = adapted_C(st, n_arcs=4000)
    r = 2.0 * Y
    for it in range(30):
        q = (C0 + c3 * r) * r * r
        Z2 = Rn @ (W @ q)
        r_new = 2.0 * (Y + Z2)
        if np.max(np.abs(r_new - r) / np.maximum(r, 1e-300)) < 1e-9:
            break
        r = r_new
    budget = 1.0 - (Y + Z2) / r
    print(f"cellwise radii: max r = {r.max():.3e}, max Z2 = {Z2.max():.3e}, "
          f"Z2/Y max = {np.max(Z2/np.maximum(Y,1e-300)):.3e};  Z1 budget min = {budget.min():.4f}")

    # goal-oriented: M_T functional
    lam = complex(float(st.mu.p) / float(st.mu.q), np.sqrt(float(st.nu2.p) / float(st.nu2.q)))
    E = np.array(st.E_f)
    u = X - E
    c2 = float(st.c2.p) / float(st.c2.q)
    DN = np.zeros((N + 1, 2, 2))
    DN[:, 0, 0] = -2 * c2 * u[:, 0] - fl["a"] * u[:, 1] - 3 * u[:, 0] ** 2
    DN[:, 0, 1] = -fl["a"] * u[:, 0]
    DN[:, 1, 0] = fl["b"] * u[:, 1]
    DN[:, 1, 1] = fl["b"] * u[:, 0]
    DNa = np.einsum("ij,njk,kl->nil", Si, DN, S)
    sg = np.geomspace(1e-6, 3.2 * args.T, 400)
    pg = np.array([complex(psi_scalar(al, lam, float(s), dps=14)) for s in sg])
    la, ph = np.log(np.abs(pg)), np.unwrap(np.angle(pg))
    Y_MT, amp_MT = 0.0, 0.0
    for tt in (args.T, 1.02 * args.T, 1.1 * args.T, 1.5 * args.T, 3.0 * args.T):
        om = hat_row_at(tm, tt, al, N)
        sig = np.clip(tt - tm, sg[0], sg[-1])
        psi = np.exp(np.interp(np.log(sig), np.log(sg), la)) * np.exp(1j * np.interp(np.log(sig), np.log(sg), ph))
        Rpsi = np.stack([np.stack([psi.real, -psi.imag], -1), np.stack([psi.imag, psi.real], -1)], -2)
        ell = om[:, None, None] * np.einsum("nij,njk->nik", Rpsi, DNa)      # (N+1, 2, 2)
        row = np.einsum("nij,njkl->ikl", ell, R)                              # (2, N+1, 2)
        rown = np.sqrt(np.einsum("ikl->k", row * row))
        amp_MT = max(amp_MT, float(rown.sum()))
        Y_MT = max(Y_MT, float(rown @ Rs_n))
    # M1 side: rigorous constants and the float M_T
    ker = kernel_integrator(st, 50.0, workers=min(args.workers, 32))
    K_up = ker.total_upper(st)
    print(f"goal-oriented: amp to M_T = {amp_MT:.3e}, Y_MT = {Y_MT:.3e};  K_J <= {K_up:.4f}, "
          f"C_r <= {C0:.4f} + {c3:.4f} r", flush=True)
    res = dict(cand=args.cand, T=args.T, N=N, K=args.K, resid_LB_minus_I=resid,
               Rs_max=float(Rs.max()), amp_state_sup=float(amp.max()), Y_state=float(Y.max()),
               t_of_Y=float(tm[int(Y.argmax())]), r_cellwise_max=float(r.max()),
               Z2_max=float(Z2.max()), Z1_budget_min=float(budget.min()),
               amp_MT=amp_MT, Y_MT=Y_MT, K_up=K_up, C0=C0, c3=c3,
               note="Z1 (operator tail ||I - B L_xhat||) is NOT computed; budget reported")
    rec.add("result", res)
    rec.add("evidence_class", "PILOT: Rs rigorous; B, Y, Z2 float; Z1 explicit and open")
    rec.save_npz("arrays", tm=tm, Rs=Rs, Y=Y, r=r, Z2=Z2, amp=amp, budget=budget)
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
