r"""Physical-state collision detection, refinement and nondegeneracy diagnostics.

The finite-dimensional discovery condition of TASK-0001 is

    H(p, q, t, s) = x(t; p) - x(s; q) = 0,

with p, q standard (constant-history) initial states of the *same* autonomous
Caputo system.  Three regimes are handled.

same-age      t = s.  Detected from sign changes of the two components of
              x(t;p) - x(t;q) on the common mesh.
cross-age     t != s.  Detected as genuine transversal intersections of the two
              planar polylines, i.e. segment-segment crossings.  This is the
              generic planar picture: two curves in R^2 meet in isolated points.
embedded-age  s = 0, i.e. x(t;p) = q.  Here q is itself a physical state whose
              canonical embedding iota(q) lies in R_alpha, so no root solving is
              needed at all: the condition "the orbit of p enters an open set of
              q's with a different outcome" is an OPEN condition.  This is the
              cheapest and most robust route to a multibasin fibre, and the one
              Stage D actually exploits.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

__all__ = [
    "Collision",
    "same_age_collisions",
    "cross_age_collisions",
    "refine_collision",
    "collision_jacobian",
]


@dataclass
class Collision:
    kind: str                  # "same_age" | "cross_age" | "embedded_age"
    p: tuple
    q: tuple
    t: float
    s: float
    x_p: tuple
    x_q: tuple
    residual: float
    meta: dict = field(default_factory=dict)


def _seg_intersect(p1, p2, q1, q2):
    """Intersection parameters of segments p1->p2 and q1->q2, or ``None``."""
    r = p2 - p1
    ss = q2 - q1
    den = r[0] * ss[1] - r[1] * ss[0]
    if den == 0.0:
        return None
    dq = q1 - p1
    u = (dq[0] * ss[1] - dq[1] * ss[0]) / den
    v = (dq[0] * r[1] - dq[1] * r[0]) / den
    if -1e-12 <= u <= 1.0 + 1e-12 and -1e-12 <= v <= 1.0 + 1e-12:
        return u, v
    return None


def same_age_collisions(t, xa, xb, tol_window: int | None = None):
    """Same-age collisions from simultaneous sign changes of both components."""
    d = xa - xb
    out = []
    s0 = np.sign(d[:, 0])
    s1 = np.sign(d[:, 1])
    c0 = np.flatnonzero(s0[:-1] * s0[1:] < 0)
    c1 = np.flatnonzero(s1[:-1] * s1[1:] < 0)
    for i in c0:
        j = c1[np.argmin(np.abs(c1 - i))] if len(c1) else None
        if j is None:
            continue
        if abs(int(j) - int(i)) <= (tol_window if tol_window is not None else 1):
            w = abs(d[i, 0]) / (abs(d[i, 0]) + abs(d[i + 1, 0]) + 1e-300)
            tc = t[i] + w * (t[i + 1] - t[i])
            xc = xa[i] + w * (xa[i + 1] - xa[i])
            res = float(np.linalg.norm(xc - (xb[i] + w * (xb[i + 1] - xb[i]))))
            out.append((float(tc), tuple(map(float, xc)), res))
    return out


def cross_age_collisions(t, xa, xb, min_age_gap: float = 0.0, max_hits: int = 200):
    """Transversal crossings of the two planar orbit polylines.

    Returns a list of ``(t, s, x, cos_angle)``; ``cos_angle`` near +-1 flags a
    near-tangential (degenerate) crossing.
    """
    hits = []
    na, nb = len(xa) - 1, len(xb) - 1
    # coarse bounding-box rejection on blocks to keep this O(n^2) loop usable
    for i in range(na):
        p1, p2 = xa[i], xa[i + 1]
        lo = np.minimum(p1, p2) - 1e-15
        hi = np.maximum(p1, p2) + 1e-15
        cand = np.flatnonzero(
            (np.minimum(xb[:-1], xb[1:]) <= hi).all(axis=1)
            & (np.maximum(xb[:-1], xb[1:]) >= lo).all(axis=1)
        )
        for j in cand:
            res = _seg_intersect(p1, p2, xb[j], xb[j + 1])
            if res is None:
                continue
            u, v = res
            tc = t[i] + u * (t[i + 1] - t[i])
            sc = t[j] + v * (t[j + 1] - t[j])
            if abs(tc - sc) < min_age_gap:
                continue
            xc = p1 + u * (p2 - p1)
            ra = p2 - p1
            rb = xb[j + 1] - xb[j]
            ca = float(
                ra @ rb / (np.linalg.norm(ra) * np.linalg.norm(rb) + 1e-300)
            )
            hits.append((float(tc), float(sc), tuple(map(float, xc)), ca))
            if len(hits) >= max_hits:
                return hits
    return hits


def _endpoint(model, p, alpha, t, h, method="pece"):
    from .solvers import solve

    n = max(1, int(round(t / h)))
    hh = t / n
    r = solve(model, np.atleast_2d(p), alpha, hh, n, method=method, store=False)
    return r.x_final[0]


def refine_collision(
    model,
    p,
    q,
    alpha,
    t0,
    s0,
    h,
    method="pece",
    max_iter: int = 40,
    tol: float = 1e-12,
    fd: float = 1e-6,
):
    """Newton refinement of ``H(t,s) = x(t;p) - x(s;q) = 0`` in the ages (t,s).

    The time derivative of a Caputo solution is *not* ``g(x)``, so the 2x2
    Jacobian is built by central finite differences of the solver endpoint map
    on a mesh that is kept commensurate with ``h``.
    """
    p = np.asarray(p, float)
    q = np.asarray(q, float)
    t, s = float(t0), float(s0)
    hist = []
    for it in range(max_iter):
        F = _endpoint(model, p, alpha, t, h, method) - _endpoint(model, q, alpha, s, h, method)
        nrm = float(np.linalg.norm(F))
        hist.append((t, s, nrm))
        if nrm < tol:
            break
        dt = fd * max(1.0, abs(t))
        ds = fd * max(1.0, abs(s))
        Ft = (
            _endpoint(model, p, alpha, t + dt, h, method)
            - _endpoint(model, p, alpha, t - dt, h, method)
        ) / (2 * dt)
        Fs = -(
            _endpoint(model, q, alpha, s + ds, h, method)
            - _endpoint(model, q, alpha, s - ds, h, method)
        ) / (2 * ds)
        J = np.column_stack([Ft, Fs])
        try:
            step = np.linalg.solve(J, -F)
        except np.linalg.LinAlgError:
            break
        lam = 1.0
        for _ in range(20):                      # simple damping
            tn, sn = t + lam * step[0], s + lam * step[1]
            if tn > 0 and sn >= 0:
                Fn = _endpoint(model, p, alpha, tn, h, method) - _endpoint(
                    model, q, alpha, sn, h, method
                )
                if np.linalg.norm(Fn) < nrm:
                    break
            lam *= 0.5
        t, s = t + lam * step[0], s + lam * step[1]
    return {"t": t, "s": s, "residual": hist[-1][2] if hist else np.inf, "history": hist}


def collision_jacobian(
    model, p, q, alpha, t, s, h, method="pece", fd: float = 1e-5, free=("p", "q", "t", "s")
):
    """Finite-difference Jacobian of ``H`` in the declared free variables.

    Returns the matrix, its singular values, numerical rank and the identity of
    the columns, so that CANDIDATE-M2's "nonsingular d x d minor" hypothesis can
    be tested against an explicitly declared variable split.
    """
    p = np.asarray(p, float)
    q = np.asarray(q, float)
    cols, names = [], []

    def Hval(pp, qq, tt, ss):
        return _endpoint(model, pp, alpha, tt, h, method) - _endpoint(
            model, qq, alpha, ss, h, method
        )

    if "p" in free:
        for k in range(len(p)):
            e = np.zeros_like(p)
            e[k] = fd * max(1.0, abs(p[k]))
            cols.append((Hval(p + e, q, t, s) - Hval(p - e, q, t, s)) / (2 * e[k]))
            names.append(f"p{k}")
    if "q" in free:
        for k in range(len(q)):
            e = np.zeros_like(q)
            e[k] = fd * max(1.0, abs(q[k]))
            cols.append((Hval(p, q + e, t, s) - Hval(p, q - e, t, s)) / (2 * e[k]))
            names.append(f"q{k}")
    if "t" in free:
        dt = fd * max(1.0, abs(t))
        cols.append((Hval(p, q, t + dt, s) - Hval(p, q, t - dt, s)) / (2 * dt))
        names.append("t")
    if "s" in free:
        ds = fd * max(1.0, abs(s))
        cols.append((Hval(p, q, t, s + ds) - Hval(p, q, t, s - ds)) / (2 * ds))
        names.append("s")

    J = np.column_stack(cols)
    sv = np.linalg.svd(J, compute_uv=False)
    rank = int((sv > sv[0] * 1e-8).sum()) if sv[0] > 0 else 0
    return {"J": J, "columns": names, "singular_values": sv, "rank": rank}
