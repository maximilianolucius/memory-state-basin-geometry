r"""A posteriori enclosure of Caputo solutions — float prototype and shared formulas.

The rigorous version lives in :mod:`msbg.validated`; this module holds the
closed forms both use, and a *non-rigorous* estimate of the final enclosure
radius used only to choose the mesh before paying for ball arithmetic.

Approximate solution
--------------------
Let ``phi`` be continuous and piecewise linear on the mesh ``0 = t_0 < ... < t_N``,
with nodal values ``phi_k`` and slopes ``m_k`` on ``[t_k, t_{k+1}]``.  Define

    xhat(t) = p + I^alpha[phi](t)
            = p + phi_0 t^alpha / Gamma(alpha+1)
                + (1/Gamma(alpha+2)) sum_k m_k [ (t-t_k)_+^{alpha+1} - (t-t_{k+1})_+^{alpha+1} ]

    xhat'(t) = phi_0 t^{alpha-1} / Gamma(alpha)
             + (1/Gamma(alpha+1)) sum_k m_k [ (t-t_k)_+^{alpha} - (t-t_{k+1})_+^{alpha} ] .

(Using ``phi = phi_0 + I^1[phi']`` and ``I^alpha I^1 = I^{alpha+1}``.)  Both are
closed forms with only non-negative powers of non-negative quantities, so they
can be evaluated in ball arithmetic on an *interval* ``t`` without spurious
singularities.  Continuity of ``phi`` is what removes the ``(t-t_k)^{alpha-1}``
singularities from ``xhat'`` at interior mesh points.

Defect and a posteriori bound
-----------------------------
With ``rho = phi - g(xhat)`` the defect is exactly ``delta = xhat - p - I^alpha[g(xhat)]
= I^alpha[rho]``.  If ``R_n >= sup_{cell n} ||rho||``, ``Lbar_n`` bounds ``||Dg||`` on
the tube ``xhat(cell n) + B(r)``, and

    W_{n,j}  = max_{t in cell n} int_{cell j} (t-s)^{alpha-1} ds          (= value at t = t_n)
    Delta_n  = (1/Gamma(alpha)) [ sum_{j<n} W_{n,j} R_j + h_n^alpha R_n / alpha ]
    U_n      = [ Delta_n + (1/Gamma(alpha)) sum_{j<n} W_{n,j} Lbar_j U_j ]
               / [ 1 - h_n^alpha Lbar_n / (alpha Gamma(alpha)) ]

then ``max_n U_n < r`` implies ``sup_{cell n} ||x - xhat|| <= U_n`` for every n.
The proof (first-exit bootstrap plus a within-cell sup argument that does NOT
need monotonicity of the comparison function) is in the TASK-0002 return.
"""
from __future__ import annotations

from math import gamma

import numpy as np

__all__ = ["graded_mesh", "collocation", "xhat_eval", "xhat_prime_eval",
           "cell_weights_max", "bound_recursion", "prototype_radius"]


def graded_mesh(T, N, r):
    k = np.arange(N + 1, dtype=np.float64)
    return T * (k / N) ** r


def _pw(z, e):
    """(z)_+^e for arrays, e > 0."""
    return np.where(z > 0, np.abs(z) ** e, 0.0)


def xhat_eval(t, tm, phi0, m, p, alpha):
    """Closed form of xhat at scalar/array times t (float, non-rigorous)."""
    t = np.atleast_1d(np.asarray(t, float))
    a1 = alpha + 1.0
    base = np.outer(t**alpha, phi0) / gamma(alpha + 1.0)       # (T, d)
    A = _pw(t[:, None] - tm[None, :-1], a1) - _pw(t[:, None] - tm[None, 1:], a1)  # (T, N)
    return p[None, :] + base + (A @ m) / gamma(alpha + 2.0)


def xhat_prime_eval(t, tm, phi0, m, alpha):
    t = np.atleast_1d(np.asarray(t, float))
    base = np.outer(t ** (alpha - 1.0), phi0) / gamma(alpha)
    A = _pw(t[:, None] - tm[None, :-1], alpha) - _pw(t[:, None] - tm[None, 1:], alpha)
    return base + (A @ m) / gamma(alpha + 1.0)


def collocation(model, p, alpha, tm, newton_tol=1e-14, maxit=50):
    """Piecewise-linear product-integration collocation: x_n = xhat(t_n), phi_n = g(x_n).

    Non-rigorous; its only job is to produce a good ``phi``.  Everything is checked
    a posteriori.
    """
    p = np.asarray(p, float)
    N = len(tm) - 1
    d = len(p)
    X = np.empty((N + 1, d))
    PHI = np.empty((N + 1, d))
    X[0] = p
    PHI[0] = model.g(p[None, :])[0]
    M = np.zeros((N, d))
    a1 = alpha + 1.0
    G1, G2 = gamma(alpha + 1.0), gamma(alpha + 2.0)
    for n in range(1, N + 1):
        t = tm[n]
        known = p + PHI[0] * t**alpha / G1
        if n >= 2:
            w = (t - tm[: n - 1]) ** a1 - (t - tm[1:n]) ** a1
            known = known + (w @ M[: n - 1]) / G2
        h = tm[n] - tm[n - 1]
        c = h**a1 / G2 / h                    # coefficient of (phi_n - phi_{n-1})
        x = X[n - 1].copy()
        for _ in range(maxit):
            gx = model.g(x[None, :])[0]
            F = x - known - c * (gx - PHI[n - 1])
            if np.max(np.abs(F)) < newton_tol:
                break
            J = np.eye(d) - c * model.jac(x[None, :])[0]
            x = x - np.linalg.solve(J, F)
        X[n] = x
        PHI[n] = model.g(x[None, :])[0]
        M[n - 1] = (PHI[n] - PHI[n - 1]) / h
    return X, PHI, M


def cell_weights_max(tm, n, alpha):
    """W_{n,j} = int_{cell j} (t_n - s)^{alpha-1} ds for j < n (the max over t in cell n)."""
    t = tm[n]
    return ((t - tm[:n]) ** alpha - (t - tm[1 : n + 1]) ** alpha) / alpha


def bound_recursion(tm, alpha, R, L):
    """U_n from the within-cell Volterra-Gronwall recursion (float version)."""
    N = len(tm) - 1
    U = np.zeros(N)
    D = np.zeros(N)
    Ga = gamma(alpha)
    for n in range(N):
        h = tm[n + 1] - tm[n]
        if n:
            W = cell_weights_max(tm, n, alpha)
            hist_R = W @ R[:n]
            hist_U = W @ (L[:n] * U[:n])
        else:
            hist_R = hist_U = 0.0
        D[n] = (hist_R + h**alpha * R[n] / alpha) / Ga
        den = 1.0 - h**alpha * L[n] / (alpha * Ga)
        if den <= 0:
            U[n:] = np.inf
            return U, D
        U[n] = (D[n] + hist_U / Ga) / den
    return U, D


def prototype_radius(model, p, alpha, T, N, r_grade, r_tube=0.05, samples=6):
    """Non-rigorous estimate of the a posteriori radius, used to size the mesh."""
    tm = graded_mesh(T, N, r_grade)
    X, PHI, M = collocation(model, p, alpha, tm)
    phi0 = PHI[0]
    R = np.zeros(N)
    L = np.zeros(N)
    lo = np.zeros((N, 2))
    hi = np.zeros((N, 2))
    fr = np.linspace(0.0, 1.0, samples + 2)
    for n in range(N):
        ts = tm[n] + fr * (tm[n + 1] - tm[n])
        ts[0] = max(ts[0], 1e-300)
        xs = xhat_eval(ts, tm, phi0, M, np.asarray(p, float), alpha)
        phis = PHI[n] + (ts - tm[n])[:, None] * M[n][None, :]
        rho = phis - model.g(xs)
        R[n] = np.max(np.abs(rho))
        lo[n], hi[n] = xs.min(0) - r_tube, xs.max(0) + r_tube
        corners = np.array([[lo[n, 0], lo[n, 1]], [lo[n, 0], hi[n, 1]],
                            [hi[n, 0], lo[n, 1]], [hi[n, 0], hi[n, 1]]])
        L[n] = np.max(np.abs(model.jac(np.vstack([corners, xs]))).sum(2).max(1))
    U, D = bound_recursion(tm, alpha, R, L)
    return {"tm": tm, "X": X, "R": R, "L": L, "U": U, "D": D, "lo": lo, "hi": hi}
