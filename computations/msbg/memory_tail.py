r"""Memory-tail split of a Caputo orbit (research/MEMORY_TAIL_SURVIVAL.md), float tools.

For t >= T,
    u(t) = h_T(t) + I_T^alpha[ J u + N(u) ](t),
    h_T(t) = p - E* + (1/Gamma(alpha)) int_0^T (t-s)^{alpha-1} F(x(s)) ds.

* :func:`inherited_input` evaluates h_T from a computed orbit, integrating the
  piecewise-linear interpolant of F(x(s)) EXACTLY against the kernel.
* :func:`linear_volterra` solves  z = h + I_T^alpha[ J z + f ]  on a uniform grid
  by the implicit product-trapezoid rule.  With f = 0 it returns v_T = L_J h_T;
  with h = 0 and f = N(u) it returns  Psi_J * N(u)  WITHOUT ever forming Psi_J.
* :func:`psi_scalar` evaluates  psi_lambda(s) = s^{alpha-1} E_{alpha,alpha}(lambda s^alpha)
  for complex lambda in arbitrary precision.

Nothing here is rigorous.  Evidence class of everything built on it:
NUMERICAL EXPLORATION / NUMERICAL CORROBORATION.
"""
from __future__ import annotations

from math import gamma

import mpmath as mp
import numpy as np

__all__ = ["inherited_input", "linear_volterra", "psi_scalar", "ml2", "remainder_split"]


def inherited_input(t_nodes, F_nodes, p_minus_E, alpha, n_T, t_eval, chunk=256):
    """h_T(t) for T = t_nodes[n_T], at the times ``t_eval`` (all >= T)."""
    tj = t_nodes[:n_T]
    tj1 = t_nodes[1:n_T + 1]
    phi = F_nodes[:n_T]
    m = (F_nodes[1:n_T + 1] - F_nodes[:n_T]) / (tj1 - tj)[:, None]
    out = np.empty((len(t_eval), F_nodes.shape[1]))
    a1 = alpha + 1.0
    for c0 in range(0, len(t_eval), chunk):
        t = np.asarray(t_eval[c0:c0 + chunk])[:, None]           # (C,1)
        A = t - tj[None, :]
        B = np.maximum(t - tj1[None, :], 0.0)
        w0 = (A**alpha - B**alpha) / alpha
        w1 = (A**a1 - B**a1) / a1
        for k in range(F_nodes.shape[1]):
            val = (phi[None, :, k] + m[None, :, k] * A) * w0 - m[None, :, k] * w1
            out[c0:c0 + chunk, k] = p_minus_E[k] + val.sum(axis=1) / gamma(alpha)
    return out


def linear_volterra(h, f, J, alpha, H):
    """Solve z_n = h_n + I^alpha[J z + f](t_n), n = 0..n_max, uniform step H.

    Product-trapezoid (piecewise-linear in J z + f), implicit in z_n.
    """
    n_max = len(h) - 1
    d = J.shape[0]
    z = np.empty((n_max + 1, d))
    G = np.empty((n_max + 1, d))
    z[0] = h[0]
    G[0] = J @ z[0] + f[0]
    c = H**alpha / gamma(alpha + 2.0)
    k = np.arange(n_max + 2, dtype=np.float64)
    a = np.empty(n_max + 2)
    a[0] = 0.0
    kk = k[1:]
    a[1:] = (kk + 1) ** (alpha + 1) + (kk - 1) ** (alpha + 1) - 2 * kk ** (alpha + 1)
    Minv = np.linalg.inv(np.eye(d) - c * J)
    for n in range(1, n_max + 1):
        a0 = n ** (alpha + 1.0) - (n - alpha) * (n + 1.0) ** alpha
        acc = a0 * G[0]
        if n >= 2:
            acc = acc + a[n - 1:0:-1] @ G[1:n]
        rhs = h[n] + c * (acc + f[n])
        z[n] = Minv @ rhs
        G[n] = J @ z[n] + f[n]
    return z


def ml2(alpha, beta, z, dps=30):
    """Two-parameter Mittag-Leffler E_{alpha,beta}(z), adaptive-precision Taylor series."""
    zz = mp.mpmathify(z)
    az = float(abs(zz))
    if az == 0:
        return 1 / mp.gamma(beta)
    guard = int(az ** (1.0 / float(alpha)) / 2.302585) + 25
    with mp.workdps(dps + guard):
        a, b = mp.mpf(alpha), mp.mpf(beta)
        tol = mp.mpf(10) ** (-(dps + 10))
        tot = mp.mpf(0)
        prev = mp.inf
        k = 0
        while True:
            term = zz**k / mp.gamma(a * k + b)
            tot += term
            at = abs(term)
            if k > 5 and at <= prev and at < tol * max(1, abs(tot)):
                break
            prev = at
            k += 1
            if k > 400000:
                raise RuntimeError("ml2 did not converge")
        val = +tot
    return val


def psi_scalar(alpha, lam, s, dps=25):
    """psi_lambda(s) = s^{alpha-1} E_{alpha,alpha}(lam s^alpha), complex lam."""
    s = mp.mpf(s)
    return s ** (mp.mpf(alpha) - 1) * ml2(alpha, alpha, mp.mpmathify(lam) * s ** mp.mpf(alpha), dps)


def remainder_split(theta, a, b, xs):
    """Coefficients of N(u): N1 = -c2 u1^2 - a u1 u2 - u1^3,  N2 = b u1 u2."""
    return {"c2": 3 * xs - 1 - theta, "a": a, "b": b}
