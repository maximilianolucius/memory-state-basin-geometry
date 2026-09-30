r"""Oscillation-Banach computer-assisted proof (TASK-0006) — rigorous constants.

Space: X = C([0,T], R^2), coordinates xi = S^{-1} u (adapted), Euclidean |.|_2 on xi,
norm  ||f|| = max( max_n sup_{C_n}|f|/omega_n ,  max_n osc_n(f)/theta_n ),
omega_n, theta_n > 0 (omega == 1 is the Chief's norm; omega is kept general).
pi = nodal piecewise-linear interpolation;  B = L_h^{-1} pi + (I - pi);
L_h = I - A W  on nodal vectors (source space), W the hat-function weights,
A_n = S^{-1} Dg(xhat(t_n)) S.

Radii / Newton-Kantorovich:  T(f) = f - B H(f),  H(f) = f - [g(xhat + I^a f) - g(xhat)] + rho.
If  Y0 + (Z1 + Z2(r)) r < r  with
    Y0 >= ||B rho||,   Z1 >= ||I - B(I - K)||,   Z2(r) >= sup_{||f||<=r} ||B(K_f - K)||,
    K f = A I^a f,  K_f f' = Dg(xhat + I^a f) I^a f',
then T is a contraction of the closed ball of radius r into itself, so H has a
unique zero there (Banach), and x = xhat + I^a f is the exact Caputo solution.

Every bound below is an UPPER bound computed either in Arb or in binary64 with
outward rounding of non-negative sums; the dense inverse is float but is
converted to rigorous block bounds through a Neumann-series residual.
"""
from __future__ import annotations

import math
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from .validated import _arb_upper_float, to_arb
from .validated_res import Setup, _l2_upper

__all__ = ["rigorous_hat_weights", "cell_weights", "nodal_data", "rigorous_inverse",
           "cap_constants", "radii_polynomial"]

_UP = 1.0 + 1e-13


def up(x):
    return np.nextafter(np.asarray(x, dtype=np.float64) * _UP, np.inf)


# ---------------------------------------------------------------------------
# rigorous weights
# ---------------------------------------------------------------------------
_HW = {}


def _hw_init(tm, alpha_s):
    from flint import arb, ctx
    ctx.prec = 128
    _HW["tm"] = [arb(float(v)) for v in tm]
    _HW["a"] = to_arb(alpha_s)
    _HW["G1"] = (_HW["a"] + 1).gamma()
    _HW["G2"] = (_HW["a"] + 2).gamma()


def _F0(a_, b_, t, A):
    from flint import arb
    tb = t - b_
    tb = arb(0) if tb.upper() <= 0 else tb
    return ((t - a_) ** A - (tb ** A if tb.upper() > 0 else arb(0))) / A


def _F1(a_, b_, t, A):
    """int_a^b (t-s)^{A-1} (s-a) ds for t >= b."""
    from flint import arb
    ta, tb = t - a_, t - b_
    tb = arb(0) if tb.upper() <= 0 else tb
    tbA = tb ** A if tb.upper() > 0 else arb(0)
    tbA1 = tb ** (A + 1) if tb.upper() > 0 else arb(0)
    return ta * (ta ** A - tbA) / A - (ta ** (A + 1) - tbA1) / (A + 1)


def _hw_row(n):
    """Row n of the hat-function weights: mid and rad (floats), j = 0..n."""
    from flint import arb
    tm, A, Ga = _HW["tm"], _HW["a"], _HW["a"].gamma()
    t = tm[n]
    mid = np.zeros(n + 1)
    rad = np.zeros(n + 1)
    for j in range(n + 1):
        w = arb(0)
        if j >= 1:
            a_, b_ = tm[j - 1], tm[j]
            w += _F1(a_, b_, t, A) / (tm[j] - tm[j - 1])
        if j <= n - 1:
            a_, b_ = tm[j], tm[j + 1]
            w += _F0(a_, b_, t, A) - _F1(a_, b_, t, A) / (tm[j + 1] - tm[j])
        w = w / Ga
        mid[j] = float(w.mid())
        rad[j] = float(w.rad()) * (1 + 1e-15) + abs(mid[j]) * 2.0 ** -52
    return n, mid, rad


def rigorous_hat_weights(tm, alpha_s, workers=None):
    N = len(tm) - 1
    Wm = np.zeros((N + 1, N + 1))
    Wr = np.zeros((N + 1, N + 1))
    with ProcessPoolExecutor(max_workers=workers or os.cpu_count(), initializer=_hw_init,
                             initargs=(tm, alpha_s)) as ex:
        for n, mid, rad in ex.map(_hw_row, range(N, 0, -1), chunksize=max(1, N // ((workers or 8) * 8))):
            Wm[n, : n + 1] = mid
            Wr[n, : n + 1] = rad
    return Wm, Wr


def cell_weights(tm, t, alpha):
    """w_j(t) = (1/Gamma(a)) int_{C_j} (t-s)^{a-1} ds, upper bounds, for all cells with t_j < t."""
    a = alpha
    lo = np.maximum(t - tm[1:], 0.0)
    hi = np.maximum(t - tm[:-1], 0.0)
    w = (hi**a - lo**a) / (a * math.gamma(a))
    return up(np.maximum(w, 0.0))


# ---------------------------------------------------------------------------
# nodal data (Arb): rho(t_n), A_n, ||A|| and osc(A) on cells, D2 bound
# ---------------------------------------------------------------------------
_ND = {}


def _nd_init(tm, phi, strs):
    from flint import arb, ctx
    from . import validated as V
    ctx.prec = 128
    V._init(tm, phi, strs["theta"], strs["a"], strs["b"], strs["m"], strs["alpha"], strs["p"],
            0.0, 128, K=1)
    st = Setup(strs["theta"], strs["a"], strs["b"], strs["m"], strs["alpha"], strs["p"], prec=128)
    _ND["S"], _ND["Si"] = st.S_arb, st.Si_arb
    _ND["V"] = V


def _xhat_at(n, s):
    """xhat(s) exactly (Arb) for s in cell n (s an arb)."""
    from flint import arb
    V = _ND["V"]
    G = V._G
    tm, phi, mm = G["tm"], G["phi"], G["m"]
    A, G1, G2, p = G["a"], G["G1"], G["G2"], G["p"]
    base = s ** A if s.upper() > 0 else arb(0)
    acc = [arb(0), arb(0)]
    for k in range(n + 1):
        tk, tk1 = tm[k], tm[k + 1]
        d = V._pos_pow(s - tk, A + 1) - (V._pos_pow(s - tk1, A + 1) if k < n else arb(0))
        acc[0] += mm[k][0] * d
        acc[1] += mm[k][1] * d
    return [p[c] + phi[0][c] * base / G1 + acc[c] / G2 for c in range(2)]


def _conj(M):
    S, Si = _ND["S"], _ND["Si"]
    SM = [[Si[i][0] * M[0][j] + Si[i][1] * M[1][j] for j in range(2)] for i in range(2)]
    return [[SM[i][0] * S[0][j] + SM[i][1] * S[1][j] for j in range(2)] for i in range(2)]


def _nd_node(n):
    """rho(t_n) (adapted, upper bound of |.|_2), A_n mid/rad (adapted), at node n."""
    from flint import arb
    V = _ND["V"]
    G = V._G
    tm, phi = G["tm"], G["phi"]
    x = _xhat_at(n if n < len(tm) - 1 else n - 1, tm[n])
    g = V._g(x[0], x[1])
    rho = [phi[n][c] - g[c] for c in range(2)]
    Si = _ND["Si"]
    q = (Si[0][0] * rho[0] + Si[0][1] * rho[1], Si[1][0] * rho[0] + Si[1][1] * rho[1])
    rho_up = _l2_upper(q)
    Dg = V._Dg(x[0], x[1])
    Aa = _conj(Dg)
    mid = np.array([[float(Aa[i][j].mid()) for j in range(2)] for i in range(2)])
    rad = np.array([[float(Aa[i][j].rad()) for j in range(2)] for i in range(2)])
    return n, rho_up, mid, rad


def _nd_cell(job):
    """||A|| and osc(A) upper bounds on cell n from its state box (max-norm box lo/hi)."""
    from flint import arb
    n, xlo, xhi, ylo, yhi = job
    V = _ND["V"]
    x = arb(float(xlo)).union(arb(float(xhi)))
    y = arb(float(ylo)).union(arb(float(yhi)))
    Aa = _conj(V._Dg(x, y))
    normA = _l2_upper([Aa[0][0], Aa[0][1], Aa[1][0], Aa[1][1]])
    oscA = 2.0 * _l2_upper([arb(0, Aa[i][j].rad()) for i in range(2) for j in range(2)])
    return n, normA, oscA


def nodal_data(tm, phi, strs, x_lo, x_hi, y_lo, y_hi, workers=None):
    N = len(tm) - 1
    rho = np.zeros(N + 1)
    Am = np.zeros((N + 1, 2, 2))
    Ar = np.zeros((N + 1, 2, 2))
    normA = np.zeros(N)
    oscA = np.zeros(N)
    with ProcessPoolExecutor(max_workers=workers or os.cpu_count(), initializer=_nd_init,
                             initargs=(tm, phi, strs)) as ex:
        for n, r, m, rd in ex.map(_nd_node, range(N + 1), chunksize=max(1, N // 400)):
            rho[n], Am[n], Ar[n] = r, m, rd
        jobs = [(n, x_lo[n], x_hi[n], y_lo[n], y_hi[n]) for n in range(N)]
        for n, na, oa in ex.map(_nd_cell, jobs, chunksize=max(1, N // 400)):
            normA[n], oscA[n] = na, oa
    return rho, Am, Ar, normA, oscA


# ---------------------------------------------------------------------------
# rigorous dense inverse of L_h = I - A W  (source space)
# ---------------------------------------------------------------------------
def rigorous_inverse(Wm, Wr, Am, Ar):
    """Block bounds  Rn[n,k] >= ||(L_h^{-1})_{nk}||_2,  Dn[n,k] >= ||(L_h^{-1})_{n+1,k} - (L_h^{-1})_{nk}||_2.

    Rt: float inverse by forward substitution.  E := I - L_h Rt with L_h the EXACT
    matrix (I - A W); |E| is bounded entrywise by the float residual plus the rounding
    error of the two products (Higham, gamma_n) plus the data uncertainty of A and W.
    Then L_h^{-1} = Rt + Rt E (I - E)^{-1}, and every entry of row r of the correction is
    bounded by  c_r := ||(|Rt| |E|)_r||_1 / (1 - ||E||_inf),  so the Frobenius norm of the
    correction on block (n, k) is <= sqrt(c_{n,0}^2 + c_{n,1}^2) =: delta_n.
    """
    N1 = Wm.shape[0]
    m = 2 * N1
    I2 = np.eye(2)
    F = np.zeros((N1, 2, m))
    for n in range(N1):
        rhs = np.zeros((2, m))
        rhs[0, 2 * n] = 1.0
        rhs[1, 2 * n + 1] = 1.0
        if n:
            rhs += Am[n] @ np.tensordot(Wm[n, :n], F[:n], axes=(0, 0))
        F[n] = np.linalg.solve(I2 - Wm[n, n] * Am[n], rhs)
    R4 = F.reshape(N1, 2, N1, 2)                          # [n, i, k, l]
    absR = np.abs(R4)
    # exact-arithmetic residual of the float product, entrywise bounds
    WR = np.tensordot(Wm, R4, axes=(1, 0))                # [n, l, k, l2] = sum_j W_nj R_{j l, k l2}
    AWR = np.einsum("nil,nlkm->nikm", Am, WR)
    E0 = AWR - R4
    E0[np.arange(N1), 0, np.arange(N1), 0] += 1.0
    E0[np.arange(N1), 1, np.arange(N1), 1] += 1.0
    u = 2.0 ** -53
    gN = N1 * u / (1 - N1 * u)
    g2 = 2 * u / (1 - 2 * u)
    absWR = np.tensordot(np.abs(Wm), absR, axes=(1, 0))
    absA = np.abs(Am)
    err_prod = gN * np.einsum("nil,nlkm->nikm", absA, absWR) \
        + g2 * np.einsum("nil,nlkm->nikm", absA, np.abs(WR))
    WrR = np.tensordot(Wr, absR, axes=(1, 0))
    err_data = np.einsum("nil,nlkm->nikm", Ar, absWR) + np.einsum("nil,nlkm->nikm", absA + Ar, WrR)
    Eabs = np.abs(E0) + err_prod + err_data
    del WR, AWR, E0, absWR, WrR, err_prod, err_data
    Em = Eabs.reshape(m, m)
    normE = float(up(np.max(Em.sum(axis=1))))
    if normE >= 1.0:
        raise RuntimeError(f"Neumann residual ||E||_inf = {normE} >= 1: inverse not certified")
    c = (absR.reshape(m, m) @ Em).sum(axis=1) / (1.0 - normE)
    delta = up(np.sqrt(c[0::2] ** 2 + c[1::2] ** 2))
    del Em, Eabs
    Rn = up(np.sqrt(np.einsum("nikl->nk", R4 * R4)) + delta[:, None])
    # oscillation blocks.  For nodal sources z (lower-triangular R):
    #   y_{n+1} - y_n = sum_{k<=n-1} (R_{n+1,k} - R_{n,k}) z_k
    #                   + (R_{n+1,n} - R_{n,n} + R_{n+1,n+1}) z_n  +  R_{n+1,n+1} (z_{n+1} - z_n),
    # so Dn[n, k] bounds the first two kinds of blocks and the last term is charged separately
    # (in _B_source_vectors) against a bound of the nodal difference |z_{n+1} - z_n|.
    Dd = R4[1:] - R4[:-1]                                    # [n, i, k, l], n = 0..N1-2
    idx = np.arange(N1 - 1)
    Dd[idx, :, idx, :] += R4[idx + 1, :, idx + 1, :]
    Dd[idx, :, idx + 1, :] = 0.0
    Dn = up(np.sqrt(np.einsum("nikl->nk", Dd * Dd)) + 2.0 * delta[1:, None] + delta[:-1, None])
    del Dd
    return Rn, Dn, normE, delta, R4


# ---------------------------------------------------------------------------
# the constants
# ---------------------------------------------------------------------------
def _submax(fn, K=4000):
    """Rigorous upper bound of max_{tau in [0,1]} of a function given through an
    interval-monotone enclosure fn(a, b) >= sup_{[a,b]} (vectorised over subintervals)."""
    e = np.linspace(0.0, 1.0, K + 1)
    return float(up(np.max(fn(e[:-1], e[1:]))))


def interpolation_constants(alpha, ratios):
    """c_alpha = max (tau^a - tau);  c_loc = max [tau^a - tau + 2 tau (1-tau)^a]
    (= sup_t ||(I-pi) I^a[(f-f_n) 1_{C_n}]||_{C_n} in units theta_n h_n^a/Gamma(a+1));
    c_prev(r) = max_tau [(1-tau) r^a + tau((1+r)^a - 1) - (tau+r)^a + tau^a]
    (= chord minus K for the previous cell of relative length r = h_{n-1}/h_n)."""
    a = alpha
    c_alpha = _submax(lambda lo, hi: hi**a - lo)
    c_loc = _submax(lambda lo, hi: hi**a - lo + 2 * hi * (1 - lo) ** a)
    r = np.asarray(ratios, float)
    K = 4000
    e = np.linspace(0.0, 1.0, K + 1)
    lo, hi = e[:-1][None, :], e[1:][None, :]
    rr = r[:, None]
    d = (1 - lo) * rr**a + hi * ((1 + rr) ** a - 1) - (lo + rr) ** a + hi**a
    c_prev = up(np.max(d, axis=1))
    return c_alpha, c_loc, c_prev


def xhat_second_derivative(tm, phi, alpha):
    """Per cell n >= 1: upper bounds  I2[n] >= int_{C_n} |xhat''|_2 dt  and  X1[n] >= sup_{C_n} |xhat'|_2,
    for xhat = p + I^a phi with phi piecewise linear (float, with rounding slack).
    xhat'(t)  = phi_0 t^{a-1}/G(a) + sum_k m_k [(t-t_k)_+^a - (t-t_{k+1})_+^a]/G(a+1),
    xhat''(t) = phi_0 (a-1) t^{a-2}/G(a) + sum_k m_k [(t-t_k)_+^{a-1} - (t-t_{k+1})_+^{a-1}]/G(a).
    Cell 0 is not covered (xhat'' not integrable at 0): I2[0] = X1[0] = inf."""
    a = alpha
    N = len(tm) - 1
    phi = np.asarray(phi, float)
    h = np.diff(tm)
    m = (phi[1:] - phi[:-1]) / h[:, None]
    mn = np.sqrt((m * m).sum(1)) * (1 + 1e-14)
    phi0 = math.sqrt(phi[0] @ phi[0])
    Ga, Ga1 = math.gamma(a), math.gamma(a + 1)
    I2 = np.full(N, np.inf)
    X1 = np.full(N, np.inf)
    for n in range(1, N):
        k = np.arange(n + 1)
        tk, tk1 = tm[k], tm[k + 1]
        J = ((tm[n + 1] - tk) ** a - (tm[n] - tk) ** a
             - np.maximum(tm[n + 1] - tk1, 0.0) ** a + np.maximum(tm[n] - tk1, 0.0) ** a) / a
        term0 = phi0 * (tm[n] ** (a - 1) - tm[n + 1] ** (a - 1)) / Ga
        s = float(np.dot(mn[: n + 1], np.abs(J))) / Ga + term0
        I2[n] = s * (1 + 1e-12) + 1e-13 * (n + 1) * tm[n] ** a
        kk = np.arange(n)
        d1 = phi[0] * tm[n] ** (a - 1) / Ga + (m[:n] * (((tm[n] - tm[kk]) ** a
                                                       - (tm[n] - tm[kk + 1]) ** a) / Ga1)[:, None]).sum(0)
        X1[n] = math.sqrt(d1 @ d1) * (1 + 1e-12) + 1e-13 * (n + 1) * tm[n] ** a + I2[n]
    return I2, X1


def xhat_prime_oscillation(tm, phi, alpha):
    """Per cell n >= 1:  O1[n] >= osc_{C_n} |xhat'|  and  X1[n] >= sup_{C_n} |xhat'|_2, WITHOUT the
    triangle-inequality loss of xhat_second_derivative.  With Delta_k(t) = (t-t_k)^a - (t-t_{k+1})^a,

      xhat'(t) - xhat'(t_n) = phi_0 (t^{a-1} - t_n^{a-1})/G(a)
                              + sum_{k<=n-1} m_k [Delta_k(t) - Delta_k(t_n)]/G(a+1) + m_n (t-t_n)^a/G(a+1).

    For k <= n-2 the bracket is smooth on C_n: bracket(t) = tau * bracket(t_{n+1}) + E_k(t) with
    |E_k| <= h^2/8 sup|bracket''|.  The sum  D_n = sum_k m_k bracket_k(t_{n+1})  is evaluated as a
    plain float sum (cancellations kept) with a rounding-error bound; only the remainders are
    summed in absolute value.  Cell 0: inf."""
    a = alpha
    N = len(tm) - 1
    phi = np.asarray(phi, float)
    h = np.diff(tm)
    m = (phi[1:] - phi[:-1]) / h[:, None]                  # slopes (N, 2)
    mn = np.sqrt((m * m).sum(1))
    Ga, Ga1 = math.gamma(a), math.gamma(a + 1)
    u = 2.0 ** -52

    def delta(t, k):                                       # (t - t_k)^a - (t - t_{k+1})^a, t > t_{k+1}
        base = t - tm[k + 1]
        return base ** a * np.expm1(a * np.log1p(h[k] / base))

    O1 = np.full(N, np.inf)
    X1 = np.full(N, np.inf)
    for n in range(1, N):
        k2 = np.arange(n - 1)                              # k <= n-2
        phi0 = math.sqrt(phi[0] @ phi[0])
        # first-order (chord) part of phi_0 (t^{a-1} - t_n^{a-1})/G(a): kept in the exact sum,
        # since it cancels against the memory sum (xhat' -> 0 while both pieces are O(t^{a-1}))
        D = phi[0] * ((tm[n + 1] ** (a - 1) - tm[n] ** (a - 1)) / Ga)
        errD = 4.0 * u * phi0 * (tm[n] ** (a - 1) + tm[n + 1] ** (a - 1)) / Ga
        rem = h[n] ** 2 / 8.0 * phi0 * (1 - a) * (2 - a) * tm[n] ** (a - 3) / Ga     # its curvature
        if n >= 2:
            d_np1 = delta(tm[n + 1], k2)
            d_n = delta(tm[n], k2)
            br = (d_np1 - d_n) / Ga1                       # bracket_k(t_{n+1}), k <= n-2
            D = D + (m[k2] * br[:, None]).sum(0)           # vector, cancellations kept
            errD += n * 8.0 * u * float(np.dot(mn[k2], np.abs(d_np1) + np.abs(d_n))) / Ga1
            # smooth remainders: h^2/8 * a(1-a) [(t_n - t_{k+1})^{a-2} - (t_n - t_k)^{a-2}] / G(a+1)
            b2 = a * (1 - a) * ((tm[n] - tm[k2 + 1]) ** (a - 2) - (tm[n] - tm[k2]) ** (a - 2)) / Ga1
            rem += h[n] ** 2 / 8.0 * float(np.dot(mn[k2], b2)) * (1 + 1e-12)
        Dn = math.sqrt(D @ D)
        errD += n * 4.0 * u * Dn
        rem += mn[n - 1] * h[n] ** a / Ga1                                   # kink of the previous cell
        rem += mn[n] * h[n] ** a / Ga1                                       # own cell
        O1[n] = (Dn + errD + 2.0 * rem) * (1 + 1e-12)
        # |xhat'(t_n)| exactly (float sum, rounding bound)
        kk = np.arange(n)
        dk = delta(tm[n], kk[:-1]) if n >= 2 else np.zeros(0)
        d_last = (tm[n] - tm[n - 1]) ** a                                    # k = n-1: (t_n - t_{n-1})^a - 0
        dall = np.concatenate([dk, [d_last]])
        v = phi[0] * tm[n] ** (a - 1) / Ga + (m[kk] * (dall / Ga1)[:, None]).sum(0)
        X1[n] = math.sqrt(v @ v) * (1 + n * 4.0 * u) + n * 8.0 * u * float(np.dot(mn[kk], dall)) / Ga1 + O1[n]
    return O1, X1


def _B_source_vectors(Rn, Dn, sigma_node, sigma_cell, tau_cell, dnode=None):
    """Cell-wise bounds of B s = L_h^{-1} pi s + (I - pi) s for a source s with
    |s(t_j)| <= sigma_node[j], sup_{C_n}|s| <= sigma_cell[n], osc_n(s) <= tau_cell[n] and
    |s(t_{n+1}) - s(t_n)| <= dnode[n] (default: tau_cell, since both nodes lie in C_n).
    Returns (sup_cell, osc_cell) arrays of length N."""
    if dnode is None:
        dnode = tau_cell
    y_sup = Rn @ sigma_node                                   # |y_n|
    diag1 = np.diagonal(Rn)[1:]                               # ||R_{n+1,n+1}||
    y_osc = Dn @ sigma_node + diag1 * dnode                   # |y_{n+1} - y_n|
    pl_sup = np.maximum(y_sup[:-1], y_sup[1:])                # PL part on C_n
    ip_sup = np.minimum(tau_cell, 2.0 * sigma_cell)           # |(I-pi)s| <= osc_n(s)
    ip_osc = np.minimum(2.0 * tau_cell, 4.0 * sigma_cell)
    return up(pl_sup + ip_sup), up(y_osc + ip_osc)


class Geometry:
    """Mesh-dependent, theta-independent quantities (computed once)."""

    def __init__(self, tm, alpha, phi, normS, normSi, xbox, diam=None):
        self.tm = np.asarray(tm, float)
        self.alpha = a = float(alpha)
        N = self.N = len(tm) - 1
        self.h = h = np.diff(self.tm)
        self.Ga1 = math.gamma(a + 1)
        self.Ga = math.gamma(a)
        # cell weights at nodes: w[n, j] = (1/G(a)) int_{C_j} (t_n - s)^{a-1} ds
        w = np.zeros((N + 1, N))
        for n in range(1, N + 1):
            w[n, :n] = cell_weights(self.tm, self.tm[n], a)[:n]
        self.w = w
        self.dw = np.maximum(w[:-1] - w[1:], 0.0)          # dw[n, j] = w_nj - w_{n+1,j}, j < n
        ratios = np.concatenate([[1.0], h[:-1] / h[1:]])
        self.c_alpha, self.c_loc, self.c_prev = interpolation_constants(a, ratios)
        # E_a[n] >= sup_{C_n} |t^a - chord| / G(a+1)
        with np.errstate(divide="ignore"):
            ea = np.minimum(h**2 * a * (1 - a) * self.tm[:-1] ** (a - 2) / 8.0, self.c_alpha * h**a)
        self.Ea = up(ea / self.Ga1)
        # d[n, j] = (t_n - t_{j+1})^{a-2} - (t_n - t_j)^{a-2}  for j <= n-2 (Green's function part)
        d = np.zeros((N, N))
        for n in range(2, N):
            j = np.arange(n - 1)
            d[n, :n - 1] = (self.tm[n] - self.tm[j + 1]) ** (a - 2) - (self.tm[n] - self.tm[j]) ** (a - 2)
        self.d = up(np.maximum(d, 0.0))
        self.green = up(h**2 / 8.0 * (1 - a) / self.Ga)
        # interpolation error of A(xhat(t)) on C_n:  E_A[n] >= sup_{C_n} ||(I-pi)A||_2.
        # For v in C^1:  |(I-pi)v| <= (h/4) osc_{C_n}(v');  A' = dA(xhat)[xhat'] so
        #   osc(A') <= D2p osc(xhat') + D3p diam(xhat(C_n)) sup|xhat'|.
        th, aa, bb = xbox["theta"], xbox["a"], xbox["b"]
        c = max(abs(-6 * xbox["x_lo"] + 2 * (1 + th)), abs(-6 * xbox["x_hi"] + 2 * (1 + th)))
        self.D2p = up(normSi * normS * math.sqrt((c + aa) ** 2 + aa**2 + 2 * bb**2))   # ||dA[e]|| <= D2p |e|_phys
        self.D3p = up(6.0 * normSi * normS)
        O1, X1 = xhat_prime_oscillation(self.tm, phi, a)
        if diam is None:
            diam = np.full(N, np.inf)
        self.EA = up(h / 4.0 * (self.D2p * O1 + self.D3p * np.asarray(diam, float) * X1))   # inf on cell 0
        self.O1, self.X1 = O1, X1
        # legacy Green's-function bound (triangle inequality on int|xhat''|), kept for comparison
        I2, X1g = xhat_second_derivative(self.tm, phi, a)
        self.EA_green = up(h / 4.0 * (self.D2p * I2 + self.D3p * h * X1g**2))
        self.EA = np.fmin(self.EA, self.EA_green)
        self.I2 = I2


def cap_vectors(geo: Geometry, Rn, Dn, rho_node, R_cell, drho_cell, normA, oscA, omega, theta,
                D2, normSi_sqrt2):
    """Cell-wise rigorous bounds for the Newton-like map T f = f - B H(f) on the set
    {f : sup_{C_n}|f| <= omega_n, osc_n f <= theta_n}:

        sup_{C_n}|T f| <= Ysup_n + T1sup_n + T2sup_n + Z2sup_n
        osc_n(T f)     <= Yosc_n + T1osc_n + T2osc_n + Z2osc_n

    (Y: B rho;  T1: L_h^{-1} pi K (I-pi) f;  T2: (I-pi) K f;  Z2: B (K_f - K) f' with the
    Lipschitz constant D2 of x -> A(x) on the tube |e|_S <= max Omega).  All returned arrays
    have length N; the dict also carries diagnostics prefixed by '_'."""
    tm, a, N, h, w, dw = geo.tm, geo.alpha, geo.N, geo.h, geo.w, geo.dw
    Ga1 = geo.Ga1
    omega = np.asarray(omega, float)
    theta = np.asarray(theta, float)
    om_hat = np.concatenate([[omega[0]], np.minimum(omega[:-1], omega[1:])])      # |f(t_n)| <= om_hat[n]
    # ---- Y: B rho -----------------------------------------------------------------
    Rs_cell = up(normSi_sqrt2 * R_cell)
    tau_rho = up(np.fmin(2.0 * Rs_cell, np.nan_to_num(normSi_sqrt2 * h * drho_cell, nan=np.inf)))
    Ysup, Yosc = _B_source_vectors(Rn, Dn, rho_node, Rs_cell, tau_rho)
    # ---- T1: L_h^{-1} pi K (I - pi) f ;  |(I-pi)f| <= theta_j on C_j ----------------
    normA_node = np.concatenate([[normA[0]], np.maximum(normA[:-1], normA[1:]), [normA[-1]]])
    wth = w @ theta                                            # |I^a (I-pi) f| at nodes
    kappa = up(normA_node * wth)
    # nodal difference of z_n = A_n I^a[(I-pi)f](t_n):
    #   |z_{n+1} - z_n| <= osc_n(A) |u_n| + ||A_{n+1}|| (sum_{j<n} dw_{nj} theta_j + w_{n+1,n} theta_n)
    du = np.einsum("nj,j->n", dw, theta) + np.diagonal(w[1:]) * theta      # dw[n, j] for j < n, w[n+1, n]
    dkappa = up(oscA * wth[:-1] + normA_node[1:] * du)
    Rk = Rn @ kappa
    Dk = Dn @ kappa + np.diagonal(Rn)[1:] * dkappa
    T1sup = up(np.maximum(Rk[:-1], Rk[1:]))
    T1osc = up(Dk)
    # ---- T2: (I - pi) K f ---------------------------------------------------------------
    Omega = up(w[1:] @ omega)                                 # sup_{C_n} |I^a f|
    OmegaN = np.concatenate([[0.0], Omega])                   # |I^a f (t_n)|  (Omega_{n-1})
    cum = np.concatenate([[0.0], np.cumsum(theta)])
    P = np.zeros(N)                                           # sup_{C_n} |(I-pi) I^a f|
    V = np.zeros(N)                                           # sup_{C_n} |I^a f - I^a f(t_n)|
    for n in range(N):
        G = np.minimum(cum[n] - cum[:n], omega[:n] + om_hat[n])          # |f - f_n| on C_j, j < n
        loc = h[n] ** a / Ga1 * (geo.c_loc * theta[n] + (geo.c_prev[n] * G[n - 1] if n else 0.0))
        green = geo.green[n] * float(np.dot(geo.d[n, :n - 1], G[:n - 1])) if n >= 2 else 0.0
        P[n] = om_hat[n] * geo.Ea[n] + loc + green
        V[n] = (om_hat[n] * (tm[n + 1] ** a - tm[n] ** a) / Ga1 + float(np.dot(dw[n, :n], G))
                + h[n] ** a * theta[n] / Ga1)
    P, V = up(P), up(V)
    # (I-pi)((A - A_n) u_n): either the interpolation error of A (Green's function, needs
    # int |xhat''|) or the crude 2 osc_n(A); both are valid upper bounds, take the smaller
    EA = np.fmin(np.where(np.isfinite(geo.EA), geo.EA, np.inf), 2.0 * oscA)
    S1, S2, S3 = up(normA * P), up(EA * OmegaN[:-1]), up(2.0 * oscA * V)
    S = up(S1 + S2 + S3)                                      # sup_{C_n} |(I-pi)(A I^a f)|
    T2sup, T2osc = S, up(2.0 * S)
    # ---- Z2: source s = Delta_A I^a f',  |Delta_A| <= D2 |I^a f| ---------------------------
    sig_node = D2 * OmegaN * OmegaN
    sig_cell = D2 * Omega * Omega
    tau_cell = np.minimum(4.0 * D2 * V * Omega, 2.0 * sig_cell)
    Z2sup, Z2osc = _B_source_vectors(Rn, Dn, sig_node, sig_cell, tau_cell)
    return {"Ysup": Ysup, "Yosc": Yosc, "T1sup": T1sup, "T1osc": T1osc, "T2sup": T2sup,
            "T2osc": T2osc, "Z2sup": Z2sup, "Z2osc": Z2osc, "Omega": Omega,
            "_S1": S1, "_S2": S2, "_S3": S3, "_P": P, "_V": V, "_kappa": kappa, "_Rk": Rk, "_Dk": Dk}


def cap_constants(geo, Rn, Dn, rho_node, R_cell, drho_cell, normA, oscA, omega, theta, D2,
                  normSi_sqrt2, rmax=1.0):
    """Norm constants Y0, Z1, Z2a in ||f|| = max(max_n sup|f|/omega_n, max_n osc_n f/theta_n),
    with Z2(r) <= Z2a r valid for r <= rmax (D2 must cover the tube of radius rmax max Omega)."""
    v = cap_vectors(geo, Rn, Dn, rho_node, R_cell, drho_cell, normA, oscA, omega, theta, D2, normSi_sqrt2)
    om, th = np.asarray(omega, float), np.asarray(theta, float)
    mx = lambda x, d: float(np.max(up(x / d)))
    Y0 = max(mx(v["Ysup"], om), mx(v["Yosc"], th))
    T1_sup, T1_osc = mx(v["T1sup"], om), mx(v["T1osc"], th)
    T2_sup, T2_osc = mx(v["T2sup"], om), mx(v["T2osc"], th)
    Z1 = max(float(up(T1_sup + T2_sup)), float(up(T1_osc + T2_osc)))
    Z2a = max(mx(v["Z2sup"], om), mx(v["Z2osc"], th))
    out = {"Y0": Y0, "Z1": Z1, "T1_sup": T1_sup, "T1_osc": T1_osc, "T2_sup": T2_sup,
           "T2_osc": T2_osc, "Z2a": Z2a, "Z2b": 0.0, "rmax": rmax,
           "Omega_max": float(v["Omega"].max()), "kappa_max": float(v["_kappa"].max())}
    out.update({k: val for k, val in v.items() if k.startswith("_")})
    out["_S"] = v["T2sup"]
    return out


def power_iteration(geo, Rn, Dn, R_cell, drho_cell, normA, oscA, normSi_sqrt2, iters=40, log=None):
    """Power iteration for the linear part M (T1 + T2, no Y, no Z2) of the cell-wise bound
    map: b <- M b / max(M b).  The growth factor max(M b)/max(b) converges to the spectral
    radius rho(M) (M is a non-negative matrix acting on (omega, theta)).  rho(M) < 1 is
    necessary for the CAP to close in ANY weighted (omega, theta)-norm with these bounds,
    and the limiting b is the optimal weight profile."""
    N = geo.N
    omega, theta = np.ones(N), np.ones(N)
    rho0 = np.zeros(N + 1)
    hist = []
    for it in range(iters):
        v = cap_vectors(geo, Rn, Dn, rho0, R_cell, drho_cell, normA, oscA, omega, theta, 0.0, normSi_sqrt2)
        om_new = v["T1sup"] + v["T2sup"]
        th_new = v["T1osc"] + v["T2osc"]
        ratios = np.concatenate([om_new / omega, th_new / theta])
        lo, hi = float(np.min(ratios)), float(np.max(ratios))   # Collatz-Wielandt: lo <= rho(M) <= hi
        scale = max(om_new.max(), th_new.max())
        hist.append(dict(it=it, cw_lower=lo, cw_upper=hi))
        if log:
            iw = int(np.argmax(ratios))
            log(f"  power-iter {it:2d}: rho(M) in [{lo:.4f}, {hi:.4f}]  (max ratio at "
                f"{'osc' if iw >= N else 'sup'} cell {iw % N}, t={geo.tm[iw % N]:.2f})")
        omega, theta = np.maximum(om_new / scale, 1e-300), np.maximum(th_new / scale, 1e-300)
        if it > 5 and hi - lo < 1e-4 * hi:
            break
    return omega, theta, hist, v


def iterate_bounds(geo, Rn, Dn, rho_node, R_cell, drho_cell, normA, oscA, D2, normSi_sqrt2,
                   iters=200, log=None, tol=1e-9):
    """Monotone iteration  b <- F(b) = Y + M b + Q(b)  from b = Y for the cell-wise bounds
    b = (omega, theta).  If it converges, F(b) < b for b := (1+eps) b_lim can be checked and
    then T maps the b-ball into itself and is a contraction there (Banach) -- the CAP closes.
    If ratio F(b)/b stays > 1 the linear part has spectral radius >= 1 in every weighted norm:
    NO choice of oscillation weights can close the CAP with these bounds.
    Returns (omega, theta, history, vectors)."""
    args = (geo, Rn, Dn, rho_node, R_cell, drho_cell, normA, oscA)
    v = cap_vectors(*args, np.full(geo.N, 1e-300), np.full(geo.N, 1e-300), D2, normSi_sqrt2)
    omega, theta = v["Ysup"].copy(), v["Yosc"].copy()
    omega = np.maximum(omega, 1e-300); theta = np.maximum(theta, 1e-300)
    hist = []
    for it in range(iters):
        v = cap_vectors(*args, omega, theta, D2, normSi_sqrt2)
        om_new = up(v["Ysup"] + v["T1sup"] + v["T2sup"] + v["Z2sup"])
        th_new = up(v["Yosc"] + v["T1osc"] + v["T2osc"] + v["Z2osc"])
        g_om, g_th = float(np.max(om_new / omega)), float(np.max(th_new / theta))
        lin = float(np.max(np.concatenate([(v["T1sup"] + v["T2sup"]) / omega,
                                           (v["T1osc"] + v["T2osc"]) / theta])))
        hist.append(dict(it=it, growth_sup=g_om, growth_osc=g_th, Z1_in_current_norm=lin,
                         omega_max=float(om_new.max()), theta_max=float(th_new.max()),
                         Omega_max=float(v["Omega"].max())))
        if log:
            log(f"  b-iter {it:3d}: growth sup {g_om:.6f} osc {g_th:.6f}  Z1(current weights)={lin:.4f}  "
                f"omega_max={om_new.max():.3e} theta_max={th_new.max():.3e} Omega_max={v['Omega'].max():.3e}")
        omega, theta = om_new, th_new
        if max(g_om, g_th) < 1 + tol or not np.isfinite(om_new.max() + th_new.max()) or om_new.max() > 1e6:
            break
    return omega, theta, hist, v


def radii_polynomial(c):
    """min over r of p(r) = Y0 + (Z1 + Z2a r + Z2b r^2 - 1) r; returns (min p, r, contraction)."""
    if c["Z1"] >= 1.0:
        return float("inf"), None, None
    rs = np.geomspace(c["Y0"] * (1 + 1e-9), 10.0, 20000)
    p = c["Y0"] + (c["Z1"] + c["Z2a"] * rs + c["Z2b"] * rs**2 - 1.0) * rs
    i = int(np.argmin(p))
    return float(p[i]), float(rs[i]), float(c["Z1"] + c["Z2a"] * rs[i] + c["Z2b"] * rs[i] ** 2)


def lipschitz_A(st: Setup, x_lo, x_hi, y_lo, y_hi, tube_phys):
    """D2: Lipschitz constant of x -> S^{-1} Dg(x) S in adapted 2-norms on the physical box
    [x_lo - tube, x_hi + tube] x [y_lo - tube, y_hi + tube]  (tube_phys = sup |e|_2 physical).

    D^2 g[e] has rows ((-6x + 2(1+theta)) e_x - a e_y,  -a e_x) and (b e_y, b e_x);
    with |e|_2 <= ||S|| |xi|_S the Frobenius norm is <= ||S|| sqrt((c + a)^2 + a^2 + 2 b^2),
    c = sup |-6x + 2(1+theta)|, and conjugation costs ||S^{-1}|| ||S||.
    """
    th, a, b = (float(st.q[k].p) / float(st.q[k].q) for k in ("theta", "a", "b"))
    xs = (float(x_lo.min()) - tube_phys, float(x_hi.max()) + tube_phys)
    c = max(abs(-6 * xs[0] + 2 * (1 + th)), abs(-6 * xs[1] + 2 * (1 + th)))
    fro = math.sqrt((c + a) ** 2 + a ** 2 + 2 * b ** 2)
    return float(up(float(st.normSi) * float(st.normS) ** 2 * fro))
