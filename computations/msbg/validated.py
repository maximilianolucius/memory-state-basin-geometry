r"""Rigorous a posteriori enclosure of a planar Caputo trajectory (Arb ball arithmetic).

THEOREM USED (proved in the TASK-0002 return, section 2)
-------------------------------------------------------
Let g be C^1, alpha in (0,1), p in R^2 and 0 = t_0 < ... < t_N = T.  Let phi be the
continuous piecewise-linear function with nodal values phi_k and slopes m_k, and

    xhat = p + I^alpha[phi],   rho = phi - g(xhat)   (so xhat - p - I^alpha[g(xhat)] = I^alpha[rho]).

Fix r > 0 and suppose, for every cell C_n = [t_n, t_{n+1}],

    R_n    >= sup_{t in C_n} ||rho(t)||_inf ,
    Lbar_n >= sup { ||Dg(xi)||_inf : xi in xhat(C_n) + [-r, r]^2 } .

With W_{n,j} = ((t_n - t_j)^alpha - (t_n - t_{j+1})^alpha)/alpha (j < n), set

    Delta_n = ( sum_{j<n} W_{n,j} R_j + h_n^alpha R_n / alpha ) / Gamma(alpha)
    kappa_n = h_n^alpha Lbar_n / (alpha Gamma(alpha))
    U_n     = ( Delta_n + sum_{j<n} W_{n,j} Lbar_j U_j / Gamma(alpha) ) / (1 - kappa_n) .

If every kappa_n < 1 and max_n U_n < r, the Caputo IVP  ^C D^alpha x = g(x), x(0)=p
has a unique continuous solution on [0,T] and

    sup_{t in C_n} ||x(t) - xhat(t)||_inf <= U_n    for every n.

WHAT IS TRUSTED
---------------
Only this module's arithmetic.  The nodal values phi_k come from an untrusted
solver and are treated as given exact binary64 numbers; the mesh points likewise.
Every quantity entering the theorem is computed in Arb ball arithmetic and every
float handed to the scalar recursion is an outward-rounded bound of an Arb ball.
The recursion itself runs in binary64 with explicit upward-rounding safeguards
(see :func:`_up`, :func:`_dot_up`).

RANGE OF xhat OVER A CELL, WITHOUT WRAPPING
-------------------------------------------
    xhat(t)  = p + phi_0 t^a/G(a+1) + sum_k m_k d_k(t)/G(a+2),
               d_k(t) = (t-t_k)_+^{a+1} - (t-t_{k+1})_+^{a+1}
    xhat'(t) = phi_0 t^{a-1}/G(a) + sum_k m_k e_k(t)/G(a+1),
               e_k(t) = (t-t_k)_+^{a}   - (t-t_{k+1})_+^{a}

On C_n every d_k is non-decreasing in t, every e_k with k < n is non-increasing
and e_n is non-decreasing, and t^a (resp. t^{a-1}) is increasing (resp.
decreasing).  So each term's exact range over C_n is the hull of its two
endpoint values, and summing those hulls encloses the range of the sum.

DEFECT BOUND ON A CELL
----------------------
For n >= 1, rho is C^1 on C_n, so by the mean value theorem
    rho(C_n) subset rho(c_n) + rho'(C_n) [-h_n/2, h_n/2],
    rho'(C_n) subset m_n - Dg(xhat(C_n)) xhat'(C_n),
with c_n the cell midpoint.  On C_0 xhat' is singular at 0, so rho(C_0) is
enclosed directly (C_0 is tiny on a graded mesh).
"""
from __future__ import annotations

import math
import os
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

import numpy as np

__all__ = ["CellResult", "verify_cells", "row_weights_upper", "bound_recursion_rigorous",
           "certify_entry", "to_arb", "to_float"]

_U = 2.0**-53          # unit roundoff of binary64


def to_arb(v):
    """Exact conversion of an input to an Arb ball.

    * ``str`` such as ``"17/20"`` or ``"0.85"``: the exact RATIONAL it denotes;
    * ``fmpq``: that rational;
    * ``float``/``int``: that exact binary64 number (NOT the decimal it prints as).

    TASK-0003 Stage D requires the formal parameters to be rationals, so the
    string form is the one to use for parameters, alpha and the initial state.
    """
    from flint import arb, fmpq
    if isinstance(v, str):
        from .lyapunov_l1 import Q
        q = Q(v)
        return arb(q.p) / arb(q.q)
    if isinstance(v, fmpq):
        return arb(v.p) / arb(v.q)
    return arb(float(v))


def to_float(v):
    """Nearest binary64 to an input (used only by the UNTRUSTED float stages)."""
    if isinstance(v, str):
        from fractions import Fraction
        return float(Fraction(v))
    return float(v)


def _up(x):
    """Smallest binary64 >= x after one more rounding step (outward safeguard)."""
    return np.nextafter(np.asarray(x, dtype=np.float64), np.inf)


def _dot_up(w, v):
    """Rigorous upper bound of sum_i w_i v_i for non-negative binary64 vectors.

    Higham: |fl(sum) - sum| <= gamma_n sum |w_i v_i|, gamma_n = n u/(1 - n u), and
    every product carries one more relative u.  So (1 + gamma_{n+1}) fl(sum)
    rounded up is an upper bound whenever all terms are non-negative.
    """
    n = len(w)
    if n == 0:
        return 0.0
    s = float(np.dot(w, v))
    g = (n + 1) * _U / (1.0 - (n + 1) * _U)
    return float(_up(s * (1.0 + g) * (1.0 + 2 * _U)))


def _arb_upper_float(x):
    """binary64 upper bound of an arb ball (float(arb) rounds to nearest)."""
    from flint import arb
    v = float(arb(x).upper())
    return float(np.nextafter(v, np.inf))


def _arb_lower_float(x):
    from flint import arb
    v = float(arb(x).lower())
    return float(np.nextafter(v, -np.inf))


# --------------------------------------------------------------------------
# per-cell rigorous work (runs in worker processes)
# --------------------------------------------------------------------------
_G = {}


def _init(tm, phi, theta, a, b, m, alpha, p, r_tube, prec, K=16, kind="allee"):
    """Worker initialiser.  ``kind='allee'`` uses (theta, a, b, m) as the Allee
    parameters; ``kind='linear2'`` reinterprets them as the entries (a11, a12, a21,
    a22) of a constant matrix, used for the exact Mittag-Leffler regression test."""
    from flint import arb, ctx
    ctx.prec = prec
    _G["K"] = int(K)
    _G["kind"] = kind
    _G["tm_f"] = tm
    _G["tm"] = [arb(float(v)) for v in tm]
    _G["phi"] = [(arb(float(u)), arb(float(v))) for u, v in phi]
    N = len(tm) - 1
    _G["m"] = [((_G["phi"][k + 1][0] - _G["phi"][k][0]) / (_G["tm"][k + 1] - _G["tm"][k]),
                (_G["phi"][k + 1][1] - _G["phi"][k][1]) / (_G["tm"][k + 1] - _G["tm"][k]))
               for k in range(N)]
    A = to_arb(alpha)
    _G["a"] = A
    _G["G1"] = (A + 1).gamma()
    _G["G2"] = (A + 2).gamma()
    _G["Ga"] = A.gamma()
    _G["p"] = (to_arb(p[0]), to_arb(p[1]))
    _G["par"] = tuple(to_arb(v) for v in (theta, a, b, m))
    _G["r"] = to_arb(r_tube)


def _g(x, y):
    if _G.get("kind") == "linear2":
        a11, a12, a21, a22 = _G["par"]
        return (a11 * x + a12 * y, a21 * x + a22 * y)
    th, a, b, m = _G["par"]
    return (x * (1 - x) * (x - th) - a * x * y, y * (b * x - m))


def _Dg(x, y):
    if _G.get("kind") == "linear2":
        a11, a12, a21, a22 = _G["par"]
        return ((a11 + 0 * x, a12 + 0 * x), (a21 + 0 * x, a22 + 0 * x))
    th, a, b, m = _G["par"]
    return ((-3 * x * x + 2 * (1 + th) * x - th - a * y, -a * x),
            (b * y, b * x - m))


def _hull(u, v):
    from flint import arb
    return arb.union(u, v)


def _pos_pow(z, e):
    """(z)_+^e for a ball z whose TRUE value is known to be >= 0.

    Rounding can make the ball straddle 0; since the true value is non-negative,
    replacing the ball by [0, upper] still encloses it.
    """
    from flint import arb
    if z.upper() <= 0:
        return arb(0)
    if z.lower() < 0:
        z = arb(0).union(arb(z.upper()))
    return z ** e


def _cell_work(n):
    """Rigorous enclosures for cell n.

    Two layers:
      * a LOOSE layer (termwise monotone hulls) giving enclosures of xhat(C_n) and
        xhat'(C_n); these are valid but wrap, because they add |m_k| times each
        term's variation and so cannot see cancellation between history terms of
        opposite sign;
      * a TIGHT layer of K+1 rigorous point evaluations s_i = t_n + i h_n / K.
    They combine through the Lipschitz remainder
        sup_{C_n} |f| <= max_i |f(s_i)| + (h_n / (2K)) sup_{C_n} |f'| ,
    applied to f = rho (defect) and f = xhat (state box).  The loose layer then
    only enters divided by K.
    """
    from flint import arb
    tm, phi, mm = _G["tm"], _G["phi"], _G["m"]
    A, G1, G2, Ga = _G["a"], _G["G1"], _G["G2"], _G["Ga"]
    p = _G["p"]
    K = _G["K"]
    a1 = A + 1
    tl, tr = tm[n], tm[n + 1]
    h = tr - tl
    pts = [tl + h * arb(i) / K for i in range(K + 1)]
    if n == 0:
        pts[0] = arb(0)

    # ---- tight layer: xhat at the K+1 points ---------------------------------
    xs = []
    for s in pts:
        base = s ** A if n > 0 or s.upper() > 0 else arb(0)
        acc = [arb(0), arb(0)]
        for k in range(n + 1):
            tk, tk1 = tm[k], tm[k + 1]
            d = _pos_pow(s - tk, a1) - (_pos_pow(s - tk1, a1) if k < n else arb(0))
            acc[0] += mm[k][0] * d
            acc[1] += mm[k][1] * d
        xs.append([p[c] + phi[0][c] * base / G1 + acc[c] / G2 for c in range(2)])

    # ---- loose layer: xhat(C_n) and xhat'(C_n) via monotone hulls ------------
    base_l = tl ** A if n > 0 else arb(0)
    xr = [p[c] + phi[0][c] * _hull(base_l, tr ** A) / G1 for c in range(2)]
    acc_r = [arb(0), arb(0)]
    for k in range(n + 1):
        tk, tk1 = tm[k], tm[k + 1]
        dl = _pos_pow(tl - tk, a1) - (_pos_pow(tl - tk1, a1) if k < n else arb(0))
        dr = _pos_pow(tr - tk, a1) - (_pos_pow(tr - tk1, a1) if k < n else arb(0))
        rng = _hull(dl, dr)
        acc_r[0] += mm[k][0] * rng
        acc_r[1] += mm[k][1] * rng
    xr = [xr[c] + acc_r[c] / G2 for c in range(2)]

    if n == 0:
        # xhat' is singular at t = 0: enclose rho(C_0) directly (C_0 is tiny)
        tt = arb(0).union(tr)
        ph = [phi[0][c] + mm[0][c] * tt for c in range(2)]
        gx = _g(xr[0], xr[1])
        rho = [ph[c] - gx[c] for c in range(2)]
        R = max(_arb_upper_float(abs(rho[0])), _arb_upper_float(abs(rho[1])))
        box = xr
        rho_pts_mag = R
        lam = float("nan")
        xp_mag = float("nan")
    else:
        bp = _hull(tl ** (A - 1), tr ** (A - 1))
        xp = [phi[0][c] * bp / Ga for c in range(2)]
        accp = [arb(0), arb(0)]
        for k in range(n + 1):
            tk, tk1 = tm[k], tm[k + 1]
            el = _pos_pow(tl - tk, A) - (_pos_pow(tl - tk1, A) if k < n else arb(0))
            er = _pos_pow(tr - tk, A) - (_pos_pow(tr - tk1, A) if k < n else arb(0))
            rng = _hull(el, er)
            accp[0] += mm[k][0] * rng
            accp[1] += mm[k][1] * rng
        xp = [xp[c] + accp[c] / G1 for c in range(2)]
        radius = h / (2 * K)
        # tight state box: every t in C_n is within h/(2K) of some s_i
        xp_abs = [abs(xp[0]), abs(xp[1])]
        box = []
        for c in range(2):
            hull_c = xs[0][c]
            for i in range(1, K + 1):
                hull_c = hull_c.union(xs[i][c])
            spread = xp_abs[c] * radius
            box.append(hull_c.union(hull_c - spread).union(hull_c + spread))
        # rho at the points, and a Lipschitz bound of rho on the cell
        rho_pts = []
        for i, s in enumerate(pts):
            ph = [phi[n][c] + mm[n][c] * (s - tl) for c in range(2)]
            gs = _g(xs[i][0], xs[i][1])
            rho_pts.append([abs(ph[c] - gs[c]) for c in range(2)])
        J = _Dg(box[0], box[1])
        drho = [abs(mm[n][c] - (J[c][0] * xp[0] + J[c][1] * xp[1])) for c in range(2)]
        Rc = []
        for c in range(2):
            mx = rho_pts[0][c]
            for i in range(1, K + 1):
                mx = arb(max(_arb_upper_float(mx), _arb_upper_float(rho_pts[i][c])))
            Rc.append(mx + drho[c] * radius)
        R = max(_arb_upper_float(Rc[0]), _arb_upper_float(Rc[1]))
        rho_pts_mag = max(max(_arb_upper_float(v[0]), _arb_upper_float(v[1])) for v in rho_pts)
        lam = max(_arb_upper_float(drho[0]), _arb_upper_float(drho[1]))
        xp_mag = max(_arb_upper_float(xp_abs[0]), _arb_upper_float(xp_abs[1]))

    # ---- tube Lipschitz bound on box + [-r, r]^2 -----------------------------
    r = _G["r"]
    bx = box[0].union(box[0] - r).union(box[0] + r)
    by = box[1].union(box[1] - r).union(box[1] + r)
    J = _Dg(bx, by)
    rows = [abs(J[0][0]) + abs(J[0][1]), abs(J[1][0]) + abs(J[1][1])]
    L = max(_arb_upper_float(rows[0]), _arb_upper_float(rows[1]))

    return (n, R, L,
            _arb_lower_float(box[0]), _arb_upper_float(box[0]),
            _arb_lower_float(box[1]), _arb_upper_float(box[1]),
            rho_pts_mag, lam)


@dataclass
class CellResult:
    R: np.ndarray
    L: np.ndarray
    x_lo: np.ndarray
    x_hi: np.ndarray
    y_lo: np.ndarray
    y_hi: np.ndarray
    rho_mid: np.ndarray
    drho: np.ndarray
    seconds: float


def verify_cells(tm, phi, theta, a, b, m, alpha, p, r_tube, prec=128, workers=None, K=16,
                 kind="allee"):
    """Rigorous per-cell quantities, parallel over cells."""
    N = len(tm) - 1
    workers = workers or os.cpu_count()
    t0 = time.time()
    out = [None] * N
    # schedule long rows first: cell n costs O(n)
    order = list(range(N - 1, -1, -1))
    with ProcessPoolExecutor(max_workers=workers, initializer=_init,
                             initargs=(tm, phi, theta, a, b, m, alpha, p, r_tube, prec, K, kind)) as ex:
        for res in ex.map(_cell_work, order, chunksize=max(1, N // (workers * 8))):
            out[res[0]] = res[1:]
    arr = np.array(out, dtype=np.float64)
    return CellResult(R=arr[:, 0], L=arr[:, 1], x_lo=arr[:, 2], x_hi=arr[:, 3],
                      y_lo=arr[:, 4], y_hi=arr[:, 5], rho_mid=arr[:, 6], drho=arr[:, 7],
                      seconds=time.time() - t0)


# --------------------------------------------------------------------------
# weights and the scalar recursion
# --------------------------------------------------------------------------
_W = {}


def _winit(tm, alpha, prec):
    from flint import arb, ctx
    ctx.prec = prec
    _W["tm"] = [arb(float(v)) for v in tm]
    _W["a"] = to_arb(alpha)


def _wrow(n):
    tm, A = _W["tm"], _W["a"]
    t = tm[n]
    row = np.empty(n, dtype=np.float64)
    for j in range(n):
        w = ((t - tm[j]) ** A - (t - tm[j + 1]) ** A if j < n - 1 else (t - tm[j]) ** A) / A
        row[j] = _arb_upper_float(w)
    return n, row


def row_weights_upper(tm, alpha, prec=128, workers=None):
    """Upper bounds of W_{n,j} for all j < n, computed in Arb, parallel over rows."""
    N = len(tm) - 1
    workers = workers or os.cpu_count()
    rows = [None] * (N + 1)
    rows[0] = np.empty(0)
    with ProcessPoolExecutor(max_workers=workers, initializer=_winit,
                             initargs=(tm, alpha, prec)) as ex:
        for n, row in ex.map(_wrow, range(N, 0, -1), chunksize=max(1, N // (workers * 8))):
            rows[n] = row
    return rows


def bound_recursion_rigorous(tm, alpha, R, L, Wrows, prec=128):
    """U_n and Delta_n with every operation rounded upward (all terms non-negative)."""
    from flint import arb, ctx
    ctx.prec = prec
    A = to_arb(alpha)
    Ga_inv = _arb_upper_float(1 / A.gamma())
    N = len(tm) - 1
    U = np.zeros(N)
    D = np.zeros(N)
    kap = np.zeros(N)
    for n in range(N):
        h = arb(float(tm[n + 1])) - arb(float(tm[n]))
        ha_over_a = _arb_upper_float(h ** A / A)
        W = Wrows[n] if n else np.empty(0)
        hist_R = _dot_up(W, R[:n])
        hist_U = _dot_up(W, _up(L[:n] * U[:n]))
        D[n] = float(_up(_up(hist_R + float(_up(ha_over_a * R[n]))) * Ga_inv))
        kap[n] = float(_up(ha_over_a * L[n] * Ga_inv * (1 + 4 * _U)))
        if kap[n] >= 1.0:
            U[n:] = np.inf
            D[n:] = np.inf
            kap[n:] = np.inf
            return U, D, kap
        num = float(_up(D[n] + float(_up(hist_U * Ga_inv))))
        den_lo = float(np.nextafter(1.0 - kap[n], -np.inf))
        U[n] = float(_up(num / den_lo * (1 + 2 * _U)))
    return U, D, kap


def certify_entry(theta, cells: CellResult, U, tm):
    """Cells on which the rigorous state box lies strictly inside R_ext.

    Returns, for every cell, eta_n = theta - (x_hi + U) (positive => certified with
    margin eta_n), together with the lower bounds x_lo - U and y_lo - U, which must
    be positive for the box to lie in the open strip {0 < x < theta, y > 0}.
    """
    xlo = cells.x_lo - U
    xhi = cells.x_hi + U
    ylo = cells.y_lo - U
    eta = theta - xhi
    ok = (xlo > 0) & (ylo > 0) & (eta > 0) & np.isfinite(U)
    return {"eta": eta, "x_lo": xlo, "x_hi": xhi, "y_lo": ylo, "certified": ok,
            "t_lo": tm[:-1], "t_hi": tm[1:]}
