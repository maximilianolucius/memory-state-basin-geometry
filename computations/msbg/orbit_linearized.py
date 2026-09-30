r"""Discrete orbit-linearized Volterra operator and its inverse (TASK-0005 Stage A/E).

On a mesh 0 = t_0 < ... < t_N, with A_j = Dg(xhat(t_j)), the piecewise-linear
product-integration discretisation of  L e = e - I^alpha[A e]  is

    (L_h e)_n = e_n - sum_{j<=n} W_{n,j} A_j e_j ,
    W_{n,j}   = (1/Gamma(alpha)) int_0^{t_n} (t_n - s)^{alpha-1} phi_j(s) ds ,

phi_j the hat function of node j.  L_h is block lower triangular, so L_h^{-1} and
L_h^{-T} act by forward/backward substitution in O(N^2) with 2x2 blocks and NO
absolute values: this is the sign-aware amplification the Chief asked for.

Quantities
----------
* amplification_rows(n): for a state index n, the row block of L_h^{-1}, i.e. the
  response of e_n to a unit cellwise defect anywhere; its l1 (over cells) norm is
  the induced (cellwise-sup -> |e_n|) amplification.  Obtained from two adjoint
  solves.
* functional_amplification(ell): for a row-vector functional ell (e.g. the
  M_T functional), the norm of  ell . L_h^{-1}  = dual norm of  L_h^{-T} ell^T .

Nothing here is rigorous: this is the Stage-I amplification surrogate of
research/VALIDATED_HISTORY_STRATEGY.md.  Norms: max-norm (per component) or the
adapted norm |S^{-1} u|_2 through a similarity transform of the blocks.
"""
from __future__ import annotations

from math import gamma

import numpy as np

__all__ = ["hat_weights", "OrbitLinearized"]


def _F0(a, b, t):
    return ((t - a) ** _F0.alpha - np.maximum(t - b, 0.0) ** _F0.alpha) / _F0.alpha


def _F1(a, b, t):
    """int_a^b (t-s)^{alpha-1} (s-a) ds  for t >= b."""
    al = _F0.alpha
    ta, tb = t - a, np.maximum(t - b, 0.0)
    return ta * (ta**al - tb**al) / al - (ta ** (al + 1) - tb ** (al + 1)) / (al + 1)


def hat_weights(tm, alpha):
    """W[n, j] for all 0 <= j <= n  (dense (N+1)x(N+1), zeros above the diagonal)."""
    _F0.alpha = alpha
    N = len(tm) - 1
    W = np.zeros((N + 1, N + 1))
    Ga = gamma(alpha)
    for n in range(1, N + 1):
        t = tm[n]
        j = np.arange(0, n + 1)
        w = np.zeros(n + 1)
        # rising part on [t_{j-1}, t_j] for j >= 1
        jr = j[1:]
        a, b = tm[jr - 1], np.minimum(tm[jr], t)
        w[1:] += _F1(a, b, t) / (tm[jr] - tm[jr - 1])
        # falling part on [t_j, t_{j+1}] for j <= n-1
        jf = j[:-1]
        a, b = tm[jf], np.minimum(tm[jf + 1], t)
        w[:-1] += _F0(a, b, t) - _F1(a, b, t) / (tm[jf + 1] - tm[jf])
        W[n, : n + 1] = w / Ga
    return W


class OrbitLinearized:
    def __init__(self, tm, A, alpha, S=None):
        """A: (N+1, 2, 2) Jacobians at the nodes; S: optional similarity (adapted norm)."""
        self.tm = np.asarray(tm, float)
        self.N = len(tm) - 1
        self.W = hat_weights(self.tm, alpha)
        if S is not None:
            Si = np.linalg.inv(S)
            A = np.einsum("ij,njk,kl->nil", Si, A, S)
        self.A = np.asarray(A, float)
        self.S = S
        I = np.eye(2)
        self.Dinv = np.array([np.linalg.inv(I - self.W[n, n] * self.A[n]) for n in range(self.N + 1)])
        self.DinvT = np.transpose(self.Dinv, (0, 2, 1))

    def solve(self, d):
        """e = L_h^{-1} d,  d: (N+1, 2)."""
        e = np.zeros_like(d)
        Ae = np.zeros_like(d)
        for n in range(self.N + 1):
            rhs = d[n] + (self.W[n, :n] @ Ae[:n] if n else 0.0)
            e[n] = self.Dinv[n] @ rhs
            Ae[n] = self.A[n] @ e[n]
        return e

    def solve_T(self, f):
        """y = L_h^{-T} f,  f: (N+1, 2).   (L_h^T y)_j = y_j - A_j^T sum_{n>=j} W_{n,j} y_n."""
        y = np.zeros_like(f)
        for j in range(self.N, -1, -1):
            s = f[j] + (self.A[j].T @ (self.W[j + 1:, j] @ y[j + 1:]) if j < self.N else 0.0)
            y[j] = self.DinvT[j] @ s
        return y

    def row_block_norms(self, n):
        """||R_{n,j}||_2 for all j, where e_n = sum_j R_{n,j} d_j."""
        rows = []
        for c in range(2):
            f = np.zeros((self.N + 1, 2))
            f[n, c] = 1.0
            rows.append(self.solve_T(f))
        R = np.stack(rows, axis=1)            # (N+1, 2, 2): R[j] = R_{n,j}
        return np.linalg.norm(R, ord=2, axis=(1, 2))

    def functional_dual(self, ell):
        """For ell (N+1, 2, 2) with  ell(e) = sum_j ell_j e_j,  return ||ell_j L_h^{-1}||_2 per j."""
        rows = []
        for c in range(2):
            rows.append(self.solve_T(ell[:, c, :]))
        R = np.stack(rows, axis=1)
        return np.linalg.norm(R, ord=2, axis=(1, 2))
