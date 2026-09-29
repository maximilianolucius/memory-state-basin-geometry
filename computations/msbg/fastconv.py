r"""Blocked history convolution for the batched Caputo solvers (TASK-0002 Stage E).

The PECE and product-integration-rectangle schemes of :mod:`msbg.solvers` spend
almost all their time in the history sums

    sum_{j<n} b_{n-1-j} G_j ,        sum_{1<=j<n} a_{n-j} G_j ,

one matrix-vector product (gemv) per step.  For a batch of M initial conditions
each gemv streams the whole history G[:n] (n x 2M doubles) from memory, so the
cost is memory-bandwidth bound and scales badly across cores.

Blocking reorders the SAME sums.  Steps are processed in blocks n0 <= n < n0+B.
For every step of a block the far history j < n0 is a Toeplitz matrix-matrix
product computed once per block,

    FP = T_b @ G[:n0],     T_b[i, j] = b_{n0+i-1-j},

which is compute bound (BLAS-3) and reads G[:n0] once per block instead of once
per step.  Only the near history n0 <= j < n is summed step by step.

Nothing is approximated: the weights, the predictor and the corrector are those
of :mod:`msbg.solvers`; only the floating-point summation order changes.  The
module is cross-validated against the O(N^2) reference in
``tests/test_fastconv.py``.
"""
from __future__ import annotations

from math import gamma as _gamma

import numpy as np

from .solvers import SolveResult, _a0_pece, _weights_pece, _weights_pi_rect

__all__ = ["solve_blocked"]


def _toeplitz_block(w, n0, B, offset):
    """Rows i=0..B-1, cols j=0..n0-1 of  T[i, j] = w[n0 + i + offset - j]  (copy)."""
    # w[n0 + offset - j + i]: for fixed i, j runs 0..n0-1 -> indices n0+offset+i ... offset+i+1
    idx = (n0 + offset) + np.arange(B)[:, None] - np.arange(n0)[None, :]
    return w[idx]


def solve_blocked(model, x0, alpha, h, n_steps, method="pece", block=256,
                  store=True, store_stride=1):
    """Blocked version of :func:`msbg.solvers.solve` for ``pi_rect`` and ``pece``."""
    if method not in ("pi_rect", "pece"):
        raise ValueError("blocked solver implements pi_rect and pece")
    X0 = np.atleast_2d(np.asarray(x0, dtype=np.float64))
    M, d = X0.shape
    N = int(n_steps)
    md = M * d
    G = np.empty((N + 1, md))
    X = np.empty((N + 1, md))
    X[0] = X0.reshape(md)
    G[0] = model.g(X0).reshape(md)

    b = _weights_pi_rect(alpha, N + 1)
    cp = h**alpha / _gamma(alpha + 1.0)
    if method == "pece":
        a = _weights_pece(alpha, N + 1)
        a = a.copy()
        a[0] = 0.0
        cc = h**alpha / _gamma(alpha + 2.0)

    n0 = 1
    while n0 <= N:
        B = min(block, N - n0 + 1)
        # far history, one GEMM per block --------------------------------------
        # predictor far part: j in [0, n0-1], weight b_{n-1-j}, n = n0 + i
        Tb = _toeplitz_block(b, n0, B, -1)            # T[i,j] = b[n0-1+i-j]
        FP = Tb @ G[:n0]
        if method == "pece":
            # corrector far part: j in [1, n0-1], weight a_{n-j}
            if n0 >= 2:
                Ta = _toeplitz_block(a, n0 - 1, B, 0)   # T[i,j'] = a[n0-1+i-j'], j = j'+1
                FC = Ta @ G[1:n0]
            else:
                FC = np.zeros((B, md))
        # near history, step by step --------------------------------------------
        for i in range(B):
            n = n0 + i
            near = n - n0
            acc = FP[i]
            if near:
                acc = acc + np.dot(b[near - 1::-1], G[n0:n])
            pred = X[0] + cp * acc
            if method == "pi_rect":
                X[n] = pred
            else:
                gp = model.g(pred.reshape(M, d)).reshape(md)
                s = _a0_pece(alpha, n) * G[0] + FC[i]
                if near:
                    # j in [n0, n-1] (all >= 1 because n0 >= 1): weight a_{n-j}
                    s = s + np.dot(a[near:0:-1], G[n0:n])
                X[n] = X[0] + cc * (s + gp)
            G[n] = model.g(X[n].reshape(M, d)).reshape(md)
        n0 += B

    t = h * np.arange(N + 1)
    if store:
        sl = slice(None, None, store_stride)
        traj = X[sl].reshape(-1, M, d).copy()
        tt = t[sl].copy()
        if tt[-1] != t[-1]:
            traj = np.concatenate([traj, X[-1].reshape(1, M, d)], axis=0)
            tt = np.concatenate([tt, t[-1:]])
    else:
        traj, tt = None, t
    return SolveResult(method=method, alpha=float(alpha), h=float(h), n_steps=N, t=tt,
                       x=traj, x_final=X[-1].reshape(M, d).copy())
