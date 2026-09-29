r"""Three independent history-retaining solvers for autonomous Caputo systems.

    ^C D^alpha_{0+} x(t) = g(x(t)),   x(0) = x0,   0 < alpha < 1.

All three retain the entire discrete history at every step; no memoryless
one-step surrogate is used anywhere (COMPUTE_AGENT_INITIAL_PROMPT.md, "Solver
rules").  Two different *formulations* are covered on purpose:

Volterra-integral formulation, x = x0 + I^alpha g(x)
    ``pi_rect``  product-integration rectangle rule (explicit).
                 weights b_k = (k+1)^alpha - k^alpha, global order O(h).
    ``pece``     Diethelm/Ford/Freed fractional Adams-Bashforth-Moulton
                 predictor-corrector: rectangle predictor + product-trapezoid
                 corrector, global order O(h^min(2, 1+alpha)).

differential (Caputo-derivative) formulation
    ``l1``       the classical L1 discretisation of ^C D^alpha, implicit,
                 solved by batched Newton; global order O(h^(2-alpha)).

``pi_rect``/``pece`` and ``l1`` discretise different objects (a weakly singular
integral versus the fractional derivative itself), which is what makes the
cross-check meaningful.

All solvers are *batched*: M initial conditions are advanced simultaneously with
the same weight vectors, so a history convolution step is a single BLAS gemv.
Cost is O(N^2 M d) flops and O(N M d) memory.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import gamma as _gamma

import numpy as np

__all__ = ["METHODS", "solve", "SolveResult", "solve_mp"]

METHODS = ("pi_rect", "pece", "l1")


@dataclass
class SolveResult:
    method: str
    alpha: float
    h: float
    n_steps: int
    t: np.ndarray          # (N+1,)
    x: np.ndarray          # (N+1, M, d) if stored, else None
    x_final: np.ndarray    # (M, d)
    newton_max_iter: int = 0
    newton_failures: int = 0

    @property
    def M(self) -> int:
        return self.x_final.shape[0]


def _weights_pi_rect(alpha: float, n: int) -> np.ndarray:
    k = np.arange(n + 1, dtype=np.float64)
    return (k + 1.0) ** alpha - k**alpha


def _weights_pece(alpha: float, n: int):
    k = np.arange(n + 2, dtype=np.float64)
    a_k = np.empty(n + 2, dtype=np.float64)
    a_k[0] = np.nan  # k = 0 term is n-dependent, handled separately
    kk = k[1:]
    a_k[1:] = (kk + 1.0) ** (alpha + 1.0) + (kk - 1.0) ** (alpha + 1.0) - 2.0 * kk ** (
        alpha + 1.0
    )
    return a_k


def _a0_pece(alpha: float, n: np.ndarray | float):
    n = np.asarray(n, dtype=np.float64)
    return n ** (alpha + 1.0) - (n - alpha) * (n + 1.0) ** alpha


def _weights_l1(alpha: float, n: int) -> np.ndarray:
    k = np.arange(n + 1, dtype=np.float64)
    return (k + 1.0) ** (1.0 - alpha) - k ** (1.0 - alpha)


def solve(
    model,
    x0,
    alpha: float,
    h: float,
    n_steps: int,
    method: str = "pece",
    store: bool = True,
    store_stride: int = 1,
    newton_tol: float = 1e-13,
    newton_maxit: int = 60,
) -> SolveResult:
    """Integrate ``model`` from every row of ``x0`` on a uniform mesh.

    Parameters
    ----------
    model     : object with ``g(X)`` -> (M,d) and, for ``l1``, ``jac(X)`` -> (M,d,d).
    x0        : (M, d) or (d,) initial physical states.
    alpha     : fractional order in (0, 1).
    h         : step size.
    n_steps   : number of steps N; final time is N*h.
    method    : one of :data:`METHODS`.
    store     : keep the trajectory (subsampled by ``store_stride``).
    """
    if method not in METHODS:
        raise ValueError(f"unknown method {method!r}")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must lie in (0,1)")

    X0 = np.atleast_2d(np.asarray(x0, dtype=np.float64))
    M, d = X0.shape
    N = int(n_steps)
    md = M * d

    G = np.empty((N + 1, md), dtype=np.float64)   # g evaluated along the history
    X = np.empty((N + 1, md), dtype=np.float64)
    X[0] = X0.reshape(md)
    G[0] = model.g(X0).reshape(md)

    newton_max_iter = 0
    newton_failures = 0

    if method == "pi_rect":
        b = _weights_pi_rect(alpha, N)
        c = h**alpha / _gamma(alpha + 1.0)
        for n in range(1, N + 1):
            acc = np.dot(b[n - 1 :: -1], G[:n])
            X[n] = X[0] + c * acc
            G[n] = model.g(X[n].reshape(M, d)).reshape(md)

    elif method == "pece":
        b = _weights_pi_rect(alpha, N)
        a_k = _weights_pece(alpha, N)
        cp = h**alpha / _gamma(alpha + 1.0)
        cc = h**alpha / _gamma(alpha + 2.0)
        for n in range(1, N + 1):
            pred = X[0] + cp * np.dot(b[n - 1 :: -1], G[:n])
            gp = model.g(pred.reshape(M, d)).reshape(md)
            acc = _a0_pece(alpha, n) * G[0]
            if n >= 2:
                acc = acc + np.dot(a_k[n - 1 : 0 : -1], G[1:n])
            acc = acc + gp
            X[n] = X[0] + cc * acc
            G[n] = model.g(X[n].reshape(M, d)).reshape(md)

    else:  # l1
        cw = _weights_l1(alpha, N)
        kappa = _gamma(2.0 - alpha) * h**alpha
        D = np.empty((N, md), dtype=np.float64)   # increments x_{j+1} - x_j
        eye = np.eye(d)
        for n in range(1, N + 1):
            if n >= 2:
                S = np.dot(cw[n - 1 : 0 : -1], D[: n - 1])
            else:
                S = np.zeros(md)
            rhs_const = X[n - 1] - S
            xn = X[n - 1].copy()            # initial guess: previous step
            ok = False
            for it in range(newton_maxit):
                Xr = xn.reshape(M, d)
                F = xn - rhs_const - kappa * model.g(Xr).reshape(md)
                nrm = np.max(np.abs(F))
                if nrm < newton_tol:
                    ok = True
                    newton_max_iter = max(newton_max_iter, it)
                    break
                J = eye[None, :, :] - kappa * model.jac(Xr)
                delta = np.linalg.solve(J, F.reshape(M, d)[:, :, None])[:, :, 0]
                xn = xn - delta.reshape(md)
            if not ok:
                newton_failures += 1
                newton_max_iter = max(newton_max_iter, newton_maxit)
            X[n] = xn
            D[n - 1] = X[n] - X[n - 1]
            G[n] = model.g(X[n].reshape(M, d)).reshape(md)

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
    return SolveResult(
        method=method,
        alpha=float(alpha),
        h=float(h),
        n_steps=N,
        t=tt,
        x=traj,
        x_final=X[-1].reshape(M, d).copy(),
        newton_max_iter=newton_max_iter,
        newton_failures=newton_failures,
    )


def solve_mp(model_mp, x0, alpha, h, n_steps, dps: int = 40, method: str = "pece"):
    """Arbitrary-precision single-trajectory version of ``pi_rect``/``pece``.

    ``model_mp`` must accept and return sequences of ``mpmath`` numbers.  Used
    for high-precision refinement of collision candidates, where float64 step
    noise would dominate.
    """
    import mpmath as mp

    with mp.workdps(dps + 15):
        a = mp.mpf(alpha)
        hh = mp.mpf(h)
        N = int(n_steps)
        d = len(x0)
        X = [[mp.mpf(v) for v in x0]]
        G = [list(model_mp(X[0]))]
        kk = [mp.mpf(k) for k in range(N + 2)]
        b = [(kk[k] + 1) ** a - kk[k] ** a for k in range(N + 1)]
        cp = hh**a / mp.gamma(a + 1)
        if method == "pece":
            a_k = [None] + [
                (kk[k] + 1) ** (a + 1) + (kk[k] - 1) ** (a + 1) - 2 * kk[k] ** (a + 1)
                for k in range(1, N + 2)
            ]
            cc = hh**a / mp.gamma(a + 2)
        for n in range(1, N + 1):
            pred = [
                X[0][i] + cp * mp.fsum(b[n - 1 - j] * G[j][i] for j in range(n))
                for i in range(d)
            ]
            if method == "pi_rect":
                xn = pred
            else:
                gp = list(model_mp(pred))
                a0 = kk[n] ** (a + 1) - (kk[n] - a) * (kk[n] + 1) ** a
                xn = []
                for i in range(d):
                    acc = a0 * G[0][i]
                    if n >= 2:
                        acc += mp.fsum(a_k[n - j] * G[j][i] for j in range(1, n))
                    acc += gp[i]
                    xn.append(X[0][i] + cc * acc)
            X.append(xn)
            G.append(list(model_mp(xn)))
    return [[+v for v in row] for row in X]
