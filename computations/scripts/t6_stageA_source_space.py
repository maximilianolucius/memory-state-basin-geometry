#!/usr/bin/env python3
"""TASK-0006 Stage A — sign-aware amplification of the SOURCE-space operator L_h = I - A W.

The TASK-0005 pilot used the state-space operator I - W A.  The radii proof lives
in source space (OSCILLATION_BANACH_CAP.md section 4), where the nodal derivative is
L_h = I - A W.  Both are inverted here by block substitution (no absolute values)
and their row-sum amplifications compared, in the adapted norm.
Evidence class: NUMERICAL EXPLORATION.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.aposteriori import collocation, graded_mesh   # noqa: E402
from msbg.models import AlleePredatorPrey              # noqa: E402
from msbg.orbit_linearized import hat_weights          # noqa: E402
from msbg.provenance import RunRecorder                # noqa: E402
from msbg.validated_res import Setup                   # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def dense_inverse_source(W, A):
    """R = (I - A W)^{-1} by forward substitution on the identity (source space)."""
    N1 = W.shape[0]
    m = 2 * N1
    F = np.zeros((N1, 2, m))          # F[n] = rows (n) of L_h^{-1}
    I = np.eye(2)
    for n in range(N1):
        rhs = np.zeros((2, m))
        rhs[0, 2 * n] = 1.0
        rhs[1, 2 * n + 1] = 1.0
        if n:
            rhs += A[n] @ np.tensordot(W[n, :n], F[:n], axes=(0, 0))
        F[n] = np.linalg.solve(I - W[n, n] * A[n], rhs)
    return F.reshape(N1, 2, N1, 2)


def main():
    np.seterr(all="ignore")
    st = Setup("1/2", "1/2", "1", "4/5", "17/20", ("277/100", "467/1000"))
    fl, pf = st.floats()
    al = fl["alpha"]
    model = AlleePredatorPrey(theta=fl["theta"], a=fl["a"], b=fl["b"], m=fl["m"])
    rec = RunRecorder("t6_stageA", ROOT)
    out = {}
    for tag, (T, N, grade) in {"T1000_N6000": (1000.0, 6000, 3.0)}.items():
        tm = graded_mesh(T, N, grade)
        X, PHI, M = collocation(model, np.array(pf), al, tm)
        S = np.array([[float(v.mid()) for v in row] for row in st.S_arb])
        Si = np.linalg.inv(S)
        A = np.einsum("ij,njk,kl->nil", Si, model.jac(X), S)
        W = hat_weights(tm, al)
        Rs = dense_inverse_source(W, A)
        from scripts.t5_stageD_radii_pilot import dense_inverse
        Rx = dense_inverse(W, A)
        rs = np.sqrt(np.einsum("nikl->nk", Rs * Rs)).sum(1)
        rx = np.sqrt(np.einsum("nikl->nk", Rx * Rx)).sum(1)
        # residual of the inverse
        WR = np.tensordot(W, Rs.reshape(N + 1, 2, -1), axes=(1, 0))      # (N+1, 2, m)
        res = Rs.reshape(N + 1, 2, -1) - np.einsum("nij,njm->nim", A, WR)  # L_h R = R - A (W R)
        idx = np.arange(N + 1)
        res = res.reshape(N + 1, 2, N + 1, 2)
        res[idx, :, idx, :] -= np.eye(2)
        resid = float(np.max(np.abs(res)))
        out[tag] = {"source_amp_sup": float(rs.max()), "t_source": float(tm[int(rs.argmax())]),
                    "state_amp_sup": float(rx.max()), "t_state": float(tm[int(rx.argmax())]),
                    "source_amp_at_T": float(rs[-1]), "resid_source": resid}
        print(f"{tag}: source-space sup amp = {rs.max():.3f} at t = {tm[int(rs.argmax())]:.1f}; "
              f"state-space = {rx.max():.3f} at t = {tm[int(rx.argmax())]:.1f}; at T: {rs[-1]:.3f}; "
              f"||L_h R - I|| = {resid:.1e}", flush=True)
    rec.add("result", out)
    rec.add("evidence_class", "NUMERICAL EXPLORATION")
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
