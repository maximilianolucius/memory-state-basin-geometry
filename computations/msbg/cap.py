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

from .rig import U, arb_hi, arb_norm2_hi, defl, gam, geometry_tables, infl, lipschitz_A_cells_arb
from .validated import _arb_upper_float, to_arb
from .validated_res import Setup, _l2_upper

__all__ = ["state_sup", "rigorous_hat_weights", "cell_weights", "nodal_data", "rigorous_inverse",
           "cap_constants", "radii_polynomial"]

def up(x):
    """Outward-rounded upper bound of a non-negative float expression with at most 4
    roundings on each term's path (rig.infl(x, 4)).  Longer reductions must call rig.infl
    with their actual length; every load-bearing call site below does."""
    return infl(x, 4)


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
    """Row n of the hat-function weights: mid (float) and a certified float radius, j = 0..n."""
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
        rad[j] = arb_hi(abs(w - arb(mid[j])))              # exact: |ball - its float centre|
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
    """w_j(t) = (1/Gamma(a)) int_{C_j} (t-s)^{a-1} ds, upper bounds, for all cells with t_j < t.

    hi^a - lo^a is evaluated as -hi^a expm1(a log1p(-(hi-lo)/hi)), which has no cancellation
    when the cell is tiny compared with its distance to t (relative error a few ulp; the
    final ``up`` adds 1e-13 relative).  Relies on libm pow/expm1/log1p being accurate to
    a few ulp (declared, not proved)."""
    a = alpha
    lo = np.maximum(t - tm[1:], 0.0)
    hi = np.maximum(t - tm[:-1], 0.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        width = np.where(lo > 0, np.diff(tm), hi)               # exact cell width (no t - t_j cancellation)
        frac = np.where(hi > 0, width / np.where(hi > 0, hi, 1.0), 0.0)
        w = np.where(frac < 1.0, -(hi**a) * np.expm1(a * np.log1p(-np.minimum(frac, 0.999999999))), hi**a)
        w = np.where(frac >= 0.999999999, hi**a - lo**a, w)
    w = w / (a * math.gamma(a))
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
    """rho(t_n) (adapted, upper bound of |.|_2), A_n float centre and certified radius, at node n."""
    from flint import arb
    V = _ND["V"]
    G = V._G
    tm, phi = G["tm"], G["phi"]
    x = _xhat_at(n if n < len(tm) - 1 else n - 1, tm[n])
    g = V._g(x[0], x[1])
    rho = [phi[n][c] - g[c] for c in range(2)]
    Si = _ND["Si"]
    q = (Si[0][0] * rho[0] + Si[0][1] * rho[1], Si[1][0] * rho[0] + Si[1][1] * rho[1])
    rho_up = arb_norm2_hi(q)
    Dg = V._Dg(x[0], x[1])
    Aa = _conj(Dg)
    mid = np.array([[float(Aa[i][j].mid()) for j in range(2)] for i in range(2)])
    rad = np.array([[arb_hi(abs(Aa[i][j] - arb(mid[i, j]))) for j in range(2)] for i in range(2)])
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
def _tick(log, label, _t=[None]):
    import time
    now = time.time()
    if log is not None and _t[0] is not None:
        log(f"   inverse stage '{label}': {now - _t[0]:.1f}s")
    _t[0] = now


def rigorous_inverse(Wm, Wr, Am, Ar, log=None):
    """Block bounds  Rn[n,k] >= ||(L_h^{-1})_{nk}||_2  and oscillation blocks (direct and Abel form).

    Rt: float inverse by forward substitution (any float matrix would do).  With the EXACT
    matrix L_h = I - A W, A in [Am +- Ar], W in [Wm +- Wr]:  E := I - L_h Rt, and
        L_h^{-1} = Rt + Rt E (I - E)^{-1}   whenever ||E||_inf < 1.
    |E| is bounded entrywise by the float residual E0 = fl(fl(Am fl(Wm Rt)) - Rt + I) plus
      * the rounding of the two products and of the two final +/- (Higham gamma_n, any order),
      * the data radii Ar |W||Rt| + (|A| + Ar) Wr |Rt|.
    Every error term is itself computed in floats and inflated by rig.infl with its own
    reduction length, so all returned arrays are certified upper bounds.  Row r of the
    correction Rt E (I-E)^{-1} has l1 norm <= c_r := ||(|Rt||E|)_r||_1 / (1 - ||E||_inf); the
    Frobenius norm of the correction on block (n, k) is <= sqrt(c_{n,0}^2 + c_{n,1}^2) =: delta_n.
    """
    N1 = Wm.shape[0]
    m = 2 * N1
    K = N1
    _tick(None, 'start')
    _tick.__defaults__[0][0] = __import__('time').time()
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
    _tick(log, 'substitution')
    absR = np.abs(R4)
    ar = np.arange(N1)
    # ---- float residual -------------------------------------------------------------------
    WR = np.tensordot(Wm, R4, axes=(1, 0))                # [n, l, k, l2], dots of length K
    AWR = np.einsum("nil,nlkm->nikm", Am, WR)             # dots of length 2
    E0 = AWR - R4
    E0[ar, 0, ar, 0] += 1.0
    E0[ar, 1, ar, 1] += 1.0
    _tick(log, 'float residual')
    # ---- certified entrywise bound of |E_exact| --------------------------------------------
    absA = np.abs(Am)
    absWR_hi = infl(np.tensordot(np.abs(Wm), absR, axes=(1, 0)), K)          # >= |Wm||Rt|
    A_absWR = infl(np.einsum("nil,nlkm->nikm", absA, absWR_hi), 2)            # >= |Am||Wm||Rt|
    A_absfWR = infl(np.einsum("nil,nlkm->nikm", absA, np.abs(WR)), 2)         # >= |Am||fl(WR)|
    err_prod = infl(gam(K) * A_absWR + gam(2) * A_absfWR, 3)
    ArW = infl(np.einsum("nil,nlkm->nikm", Ar, absWR_hi), 2)                  # Ar |W||Rt|
    WrR = infl(np.tensordot(Wr, absR, axes=(1, 0)), K)                         # Wr |Rt|
    AWrR = infl(np.einsum("nil,nlkm->nikm", infl(absA + Ar, 1), WrR), 2)       # (|A|+Ar) Wr |Rt|
    err_data = infl(ArW + AWrR, 1)
    err_fin = infl(gam(2) * infl(np.abs(AWR) + absR, 1), 1)                    # the two final +/- ...
    err_fin[ar, 0, ar, 0] += 2.0 * gam(2)                                      # ... incl. the +I entries
    err_fin[ar, 1, ar, 1] += 2.0 * gam(2)
    Eabs = infl(np.abs(E0) + err_prod + err_data + err_fin, 3)
    _tick(log, 'error terms')
    del WR, AWR, E0, absWR_hi, A_absWR, A_absfWR, err_prod, ArW, WrR, AWrR, err_data, err_fin
    Em = Eabs.reshape(m, m)
    normE = float(infl(np.max(Em.sum(axis=1)), m))
    if normE >= 1.0:
        raise RuntimeError(f"Neumann residual ||E||_inf = {normE} >= 1: inverse not certified")
    c = infl(infl(absR.reshape(m, m) @ Em, m).sum(axis=1), m)
    c = infl(c / (1.0 - normE), 1)
    delta = infl(np.sqrt(infl(c[0::2] ** 2 + c[1::2] ** 2, 3)), 1)
    _tick(log, 'Neumann correction')
    del Em, Eabs
    fro = lambda X: infl(np.sqrt(infl(np.einsum("nikl->nk", X * X), 4)), 1)
    Rn = infl(fro(R4) + delta[:, None], 1)
    # ---- oscillation blocks ---------------------------------------------------------------
    #   y_{n+1} - y_n = sum_{k<=n-1} (R_{n+1,k} - R_{n,k}) z_k
    #                   + (R_{n+1,n} - R_{n,n} + R_{n+1,n+1}) z_n  +  R_{n+1,n+1} (z_{n+1} - z_n),
    # and, by summation by parts with S_{nk} = sum_{j<=k} (R_{n+1,j} - R_{n,j}), S_{n,n+1} = S_{nn} + R_{n+1,n+1}:
    #   y_{n+1} - y_n = sum_{k<=n} S_{nk} (z_k - z_{k+1}) + S_{n,n+1} z_{n+1}.
    Dd = R4[1:] - R4[:-1]                                    # one rounding per entry: relative u
    idx = np.arange(N1 - 1)
    Sc = np.cumsum(Dd, axis=2)                               # cumulative over k, dots of length <= K
    Sabs = infl(np.cumsum(np.abs(Dd), axis=2), K + 1)        # >= sum_j |true Dd| (incl. the subtraction u)
    Serr = infl(gam(K) * Sabs, 1)                            # entrywise rounding bound of Sc
    del Sabs
    Sn = infl(infl(fro(Sc), 1) + fro(Serr) + (np.arange(N1)[None, :] + 1.0) * infl(delta[1:, None] + delta[:-1, None], 1), 3)
    del Sc, Serr
    _tick(log, 'Abel blocks')
    Sn[idx[:, None] < np.arange(N1)[None, :] - 1] = 0.0      # only k <= n+1 are used
    Dd[idx, :, idx, :] += R4[idx + 1, :, idx + 1, :]         # one more rounding on the diagonal blocks
    Dd[idx, :, idx + 1, :] = 0.0
    Dn = infl(infl(fro(Dd), 2) + infl(2.0 * delta[1:, None] + delta[:-1, None], 1), 1)
    del Dd
    Dn = np.stack([Dn, Sn], axis=0)                          # (2, N1-1, N1): direct and Abel blocks
    _tick(log, 'direct blocks')
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


def mean_kernel_blocks(R4, delta, Am, Ar, W_hi, W_lo):
    """Blocks of  Q = L_h^{-1} diag(A) W_c  (W_c = cell weights at nodes), which acts on the
    cell MEANS of a source g:  (L_h^{-1} pi K g)_n = sum_j Q_nj mean_{C_j}(g) + remainder.
    Keeps the sign cancellation between L_h^{-1} and A I^a (Q ~ L_h^{-1} - I), which the
    product of norms ||R|| ||A|| w destroys.
    Certified:  Q_exact = (Rt + Delta) M_exact with |Delta_(n,i),:|_1 <= delta_n and
    |M_exact - Mf| <= Ar W_hi + (|A| + Ar)(W_hi - W_lo) + u|Mf|;  the float product Rt Mf
    carries Higham's gamma_m.  Returns Qn[n, j] >= ||Q_nj||_F, DQn[n, j] >= ||Q_{n+1,j} - Q_nj||_F."""
    N1 = R4.shape[0]
    N = W_hi.shape[1]
    m = 2 * N1
    Rt = R4.reshape(m, m)
    Mf = (Am[:, :, None, :] * W_hi[:, None, :, None]).reshape(m, 2 * N)
    Qf = Rt @ Mf                                              # dots of length m
    absRt = np.abs(Rt)
    absM = infl(np.abs(Mf), 1)
    dW = np.nextafter(W_hi - W_lo, np.inf)
    dM = infl((Ar[:, :, None, :] * W_hi[:, None, :, None]
               + infl(np.abs(Am) + Ar, 1)[:, :, None, :] * dW[:, None, :, None]).reshape(m, 2 * N)
              + U * np.abs(Mf), 4)
    err = infl(gam(m) * infl(absRt @ absM, m), 1) + infl(absRt @ dM, m) \
        + np.repeat(delta, 2)[:, None] * infl(absM + dM, 1).max(axis=0)[None, :]
    err = infl(err, 2)
    del Mf, absM, dM
    Q4 = Qf.reshape(N1, 2, N, 2)
    E4 = err.reshape(N1, 2, N, 2)
    fro = lambda X: infl(np.sqrt(infl(np.einsum("nikl->nk", X * X), 4)), 1)
    eb = fro(E4)
    Qn = infl(fro(Q4) + eb, 1)
    DQn = infl(infl(fro(Q4[1:] - Q4[:-1]), 1) + eb[1:] + eb[:-1], 2)
    return Qn, DQn


def _osc_pl(Rn, Dn, sigma_node, dnode):
    """|y_{n+1} - y_n| for y = L_h^{-1} z with |z_k| <= sigma_node[k], |z_{k+1} - z_k| <= dnode[k]:
    minimum of the direct block bound and the Abel (summation by parts) bound."""
    N1 = Rn.shape[0]
    diag1 = np.diagonal(Rn)[1:]                               # ||R_{n+1,n+1}||
    if Dn.ndim == 3:                                          # (direct blocks, Abel blocks)
        Dd, Sn = Dn[0], Dn[1]
        Slow = np.tril(Sn[:, :N1 - 1])                        # S_{nk}, k <= n
        S1 = np.diagonal(Sn[:, 1:])                           # S_{n,n+1}
        direct = infl(infl(Dd @ sigma_node, N1) + infl(diag1 * dnode, 1), 1)
        abel = infl(infl(Slow @ dnode, N1) + infl(S1 * sigma_node[1:], 1), 1)
        return np.minimum(direct, abel)
    return infl(infl(Dn @ sigma_node, N1) + infl(diag1 * dnode, 1), 1)


def _B_source_vectors(Rn, Dn, sigma_node, sigma_cell, tau_cell, dnode=None):
    """Cell-wise bounds of B s = L_h^{-1} pi s + (I - pi) s for a source s with
    |s(t_j)| <= sigma_node[j], sup_{C_n}|s| <= sigma_cell[n], osc_n(s) <= tau_cell[n] and
    |s(t_{n+1}) - s(t_n)| <= dnode[n] (default: tau_cell, since both nodes lie in C_n).
    Returns (sup_cell, osc_cell, bubble_cell) arrays of length N, bubble = sup_{C_n}|(I-pi) B s|."""
    if dnode is None:
        dnode = tau_cell
    N1 = Rn.shape[0]
    y_sup = infl(Rn @ sigma_node, N1)                         # |y_n|
    y_osc = _osc_pl(Rn, Dn, sigma_node, dnode)                # |y_{n+1} - y_n|
    pl_sup = np.maximum(y_sup[:-1], y_sup[1:])                # PL part on C_n
    ip_sup = np.minimum(tau_cell, 2.0 * sigma_cell)           # |(I-pi)s| <= osc_n(s)
    ip_osc = np.minimum(2.0 * tau_cell, 4.0 * sigma_cell)
    return infl(pl_sup + ip_sup, 1), infl(y_osc + ip_osc, 1), ip_sup


class Geometry:
    """Mesh-dependent, weight-independent quantities.  All real-exponent powers and Gamma
    values come from rig.geometry_tables (Arb, per mesh row, converted outward); the few
    remaining float operations here are +, *, /, sqrt on non-negative data, inflated with
    rig.infl.  ``alpha_str`` is the exact rational order (e.g. "17/20")."""

    def __init__(self, tm, alpha_str, phi, normS, normSi, xbox, diam=None, workers=None, tables=None):
        from fractions import Fraction
        self.tm = np.asarray(tm, float)
        self.alpha_str = alpha_str
        self.alpha = a = float(Fraction(alpha_str))           # diagnostics only
        N = self.N = len(tm) - 1
        self.h = h = np.diff(self.tm)
        self.Ga1 = math.gamma(a + 1)                          # diagnostics only (not load-bearing)
        self.Ga = math.gamma(a)
        T = tables if tables is not None else geometry_tables(self.tm, phi, alpha_str, workers)
        self.w, self.w_lo, self.dw = T["W_hi"], T["W_lo"], T["DW"]
        self.rem, self.d, self.green = T["REM"], T["D"], T["GREEN"]
        self.Ea, self.HA, self.DTA = T["Ea"], T["HA"], T["DTA"]
        self.c_alpha, self.c_loc, self.c_prev = T["c_alpha"], T["c_loc"], T["c_prev"]
        self.O1, self.X1 = T["O1"], T["X1"]
        self.Qn = self.DQn = None
        # interpolation error of A(xhat(t)) on C_n:  E_A[n] >= sup_{C_n} ||(I-pi)A||_2.
        # For v in C^1:  |(I-pi)v| <= (h/4) osc_{C_n}(v');  A' = dA(xhat)[xhat'] so
        #   osc(A') <= D2p osc(xhat') + D3p diam(xhat(C_n)) sup|xhat'|.
        th, aa, bb = xbox["theta"], xbox["a"], xbox["b"]
        c = max(infl(abs(-6 * xbox["x_lo"] + 2 * (1 + th)), 3), infl(abs(-6 * xbox["x_hi"] + 2 * (1 + th)), 3))
        self.D2p = float(infl(normSi * normS * math.sqrt(infl((c + aa) ** 2 + aa ** 2 + 2 * bb ** 2, 5)), 3))
        self.D3p = float(infl(6.0 * normSi * normS, 2))
        if diam is None:
            diam = np.full(N, np.inf)
        self.diam = np.asarray(diam, float)
        with np.errstate(invalid="ignore"):
            self.EA = infl(h / 4.0 * infl(self.D2p * self.O1 + self.D3p * self.diam * self.X1, 3), 2)   # inf on cell 0
        self.D3a = float(infl(self.D3p * normS, 1))            # ||S^-1 D^3g[S u, dx] S|| <= D3a |u| |dx|_phys


def state_sup(w, omega):
    """Omega_n >= sup_{t in C_n} |I^a f(t)| for sup_{C_j}|f| <= omega_j.
    For t in C_n:  |I^a f(t)| <= sum_{j<n} w_j(t) omega_j + (t - t_n)^a/G(a+1) omega_n, and each
    w_j(t), j < n, is DEcreasing in t (the kernel is decreasing), so it is bounded by its value
    at t_n; the own-cell part is increasing and bounded by its value at t_{n+1}.
    (sum_j w_j(t_{n+1}) omega_j alone is NOT an upper bound for non-constant omega.)"""
    N = w.shape[1]
    return infl(infl(np.einsum("nj,j->n", w[:-1], omega), N) + infl(np.diagonal(w[1:]) * omega, 1), 1)


def z2_vectors(geo, Rn, Dn, D2, Om_b, V_b, Om_p, V_p):
    """Bounds of  B [ (A(xhat + e) - A(xhat)) I^a h ]  for  |e| <= Om_b, |I^a h| <= Om_p on cells
    (V_*: sup_{C_n}|u - u(t_n)| for u = e resp. I^a h).  With Om_p = Om_b this bounds B N(e)
    (N the Taylor remainder, with a spare factor 2); with a different p it bounds the nonlinear
    part of DT(f) h -- needed for the contraction constant.
    Delta_A(t) = A(xhat(t) + e(t)) - A(xhat(t)),  |Delta_A| <= D2 |e|, and over a cell
    osc(Delta_A) <= 2 D2 V_b + D3a diam(xhat(C_n)) Om_b   (D2 g(x) is affine in x)."""
    N = geo.N
    D2c = np.broadcast_to(np.asarray(D2, float), (N,))       # scalar or per-cell
    D2n = np.concatenate([[D2c[0]], np.maximum(D2c[:-1], D2c[1:]), [D2c[-1]]])
    ObN = np.concatenate([[0.0], Om_b])
    OpN = np.concatenate([[0.0], Om_p])
    sig_node = infl(D2n * ObN * OpN, 2)
    sig_cell = infl(D2c * Om_b * Om_p, 2)
    with np.errstate(invalid="ignore"):
        extra = np.where(Om_b * Om_p > 0, infl(geo.D3a * geo.diam * Om_b * Om_p, 3), 0.0) if np.any(D2c > 0) else 0.0
    tau_cell = np.fmin(infl(2.0 * D2c * infl(V_b * Om_p + Om_b * V_p, 3) + extra, 3), 2.0 * sig_cell)
    return _B_source_vectors(Rn, Dn, sig_node, sig_cell, tau_cell)


def cap_vectors(geo: Geometry, Rn, Dn, rho_node, R_cell, drho_cell, normA, oscA, omega, theta,
                D2, normSi_sqrt2, beta=None):
    """Cell-wise rigorous bounds for the Newton-like map T f = f - B H(f) on the set
    {f : sup_{C_n}|f| <= omega_n, osc_n f <= theta_n, sup_{C_n}|(I-pi) f| <= beta_n}:

        sup_{C_n}|T f| <= Ysup_n + T1sup_n + T2sup_n + Z2sup_n
        osc_n(T f)     <= Yosc_n + T1osc_n + T2osc_n + Z2osc_n
        sup|(I-pi)T f| <= Ybub_n + T2bub_n + Z2bub_n

    (Y: B rho;  T1: L_h^{-1} pi K (I-pi) f;  T2: (I-pi) K f;  Z2: B (K_f - K) f' with the
    Lipschitz constant D2 of x -> A(x) on the tube |e|_S <= max Omega).  beta = theta
    (default) reproduces the two-component oscillation norm; carrying the bubble separately
    is sharper because T1 only sees the bubble.  Every float reduction is inflated with
    rig.infl by its length; the mesh tables are Arb-backed (rig.geometry_tables)."""
    N, h, w, dw = geo.N, geo.h, geo.w, geo.dw
    N1 = N + 1
    omega = np.asarray(omega, float)
    theta = np.asarray(theta, float)
    beta = theta if beta is None else np.minimum(np.asarray(beta, float), theta)
    om_hat = np.concatenate([[omega[0]], np.minimum(omega[:-1], omega[1:])])      # |f(t_n)| <= om_hat[n]
    # ---- Y: B rho -----------------------------------------------------------------
    Rs_cell = infl(normSi_sqrt2 * R_cell, 1)
    tau_rho = np.fmin(2.0 * Rs_cell, np.nan_to_num(infl(normSi_sqrt2 * h * drho_cell, 2), nan=np.inf))
    Ysup, Yosc, Ybub = _B_source_vectors(Rn, Dn, rho_node, Rs_cell, tau_rho)
    # ---- T1: L_h^{-1} pi K (I - pi) f ;  |(I-pi)f| <= beta_j on C_j ----------------
    normA_node = np.concatenate([[normA[0]], np.maximum(normA[:-1], normA[1:]), [normA[-1]]])
    wth = infl(w @ beta, N)                                    # |I^a (I-pi) f| at nodes
    kappa = infl(normA_node * wth, 1)
    # nodal difference of z_n = A_n I^a[(I-pi)f](t_n):
    #   |z_{n+1} - z_n| <= osc_n(A) |u_n| + ||A_{n+1}|| (sum_{j<n} dw_{nj} beta_j + w_{n+1,n} beta_n)
    du = infl(infl(np.einsum("nj,j->n", dw, beta), N) + infl(np.diagonal(w[1:]) * beta, 1), 1)
    dkappa = infl(infl(oscA * wth[:-1], 1) + infl(normA_node[1:] * du, 1), 1)
    Rk = infl(Rn @ kappa, N1)
    Dk = _osc_pl(Rn, Dn, kappa, dkappa)
    if geo.Qn is not None:
        # mean/remainder split: (K g)(t_k) = A_k sum_j [w_kj mean_j(g) + r_kj], |r_kj| <= rem_kj beta_j
        kr = infl(normA_node * infl(geo.rem @ beta, N), 1)
        Rk = np.minimum(Rk, infl(infl(geo.Qn @ beta, N) + infl(Rn @ kr, N1), 1))
        Dk = np.minimum(Dk, infl(infl(geo.DQn @ beta, N) + _osc_pl(Rn, Dn, kr, infl(kr[:-1] + kr[1:], 1)), 1))
    T1sup = np.maximum(Rk[:-1], Rk[1:])
    T1osc = Dk
    # ---- T2: (I - pi) K f ---------------------------------------------------------------
    Omega = state_sup(w, omega)                               # sup_{C_n} |I^a f|
    OmegaN = np.concatenate([[0.0], Omega])                   # |I^a f (t_n)|  (Omega_{n-1})
    cs = np.cumsum(theta)
    cum_hi = np.concatenate([[0.0], infl(cs, N)])
    cum_lo = np.concatenate([[0.0], defl(cs, N)])
    P = np.zeros(N)                                           # sup_{C_n} |(I-pi) I^a f|
    V = np.zeros(N)                                           # sup_{C_n} |I^a f - I^a f(t_n)|
    for n in range(N):
        # |f - f_n| on C_j, j < n:  <= min( sum_{i=j}^{n-1} theta_i,  omega_j + omega_hat_n )
        G = np.minimum(np.nextafter(cum_hi[n] - cum_lo[:n], np.inf), infl(omega[:n] + om_hat[n], 1))
        loc = infl(geo.HA[n] * infl(geo.c_loc * theta[n] + (geo.c_prev[n] * G[n - 1] if n else 0.0), 3), 1)
        green = infl(geo.green[n] * infl(float(np.dot(geo.d[n, :n - 1], G[:n - 1])), n), 1) if n >= 2 else 0.0
        P[n] = infl(infl(om_hat[n] * geo.Ea[n], 1) + loc + green, 2)
        V[n] = infl(infl(om_hat[n] * geo.DTA[n], 1) + infl(float(np.dot(dw[n, :n], G)), n + 1)
                    + infl(geo.HA[n] * theta[n], 1), 2)
    # (I-pi)((A - A_n) u_n): either the interpolation error of A (osc of xhat') or the crude
    # 2 osc_n(A); both are valid upper bounds, take the smaller
    EA = np.fmin(np.where(np.isfinite(geo.EA), geo.EA, np.inf), 2.0 * oscA)
    S1, S2, S3 = infl(normA * P, 1), infl(EA * OmegaN[:-1], 1), infl(2.0 * oscA * V, 1)
    S = infl(S1 + S2 + S3, 2)                                 # sup_{C_n} |(I-pi)(A I^a f)|
    T2sup, T2osc = S, 2.0 * S
    # ---- Z2: source s = Delta_A I^a f',  |Delta_A| <= D2 |I^a f| ---------------------------
    Z2sup, Z2osc, Z2bub = z2_vectors(geo, Rn, Dn, D2, Omega, V, Omega, V)
    zero = np.zeros(N)
    return {"Ybub": Ybub, "T1bub": zero, "T2bub": S, "Z2bub": Z2bub,
            "Ysup": Ysup, "Yosc": Yosc, "T1sup": T1sup, "T1osc": T1osc, "T2sup": T2sup,
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


COMPONENTS = ("sup", "osc", "bub")


def _apply(v, parts):
    """Sum the named parts ('Y', 'T1', 'T2', 'Z2') for the three components."""
    return [infl(sum(v[p + c] for p in parts), len(parts)) for c in COMPONENTS]


def power_iteration(geo, Rn, Dn, R_cell, drho_cell, normA, oscA, normSi_sqrt2, iters=40, log=None,
                    bubble=True):
    """Power iteration for the linear part M (T1 + T2, no Y, no Z2) of the cell-wise bound
    map acting on b = (omega, theta, beta).  Collatz-Wielandt: min ratio <= rho(M) <= max ratio.
    rho(M) < 1 is necessary for the CAP to close in ANY weighted norm built from these
    components with these bounds.  bubble=False ties beta = theta (two-component osc norm)."""
    N = geo.N
    b = [np.ones(N), np.ones(N), np.ones(N)]
    rho0 = np.zeros(N + 1)
    hist = []
    for it in range(iters):
        v = cap_vectors(geo, Rn, Dn, rho0, R_cell, drho_cell, normA, oscA, b[0], b[1], 0.0, normSi_sqrt2,
                        beta=b[2] if bubble else None)
        new = _apply(v, ("T1", "T2"))
        if not bubble:
            new[2] = new[1]
        k = 3 if bubble else 2
        ratios = np.concatenate([new[i] / b[i] for i in range(k)])
        lo, hi = float(np.min(ratios)), float(np.max(ratios))
        scale = max(x.max() for x in new)
        hist.append(dict(it=it, cw_lower=lo, cw_upper=hi))
        if log:
            iw = int(np.argmax(ratios))
            log(f"  power-iter {it:2d}: rho(M) in [{lo:.4f}, {hi:.4f}]  (max ratio at "
                f"{COMPONENTS[iw // N]} cell {iw % N}, t={geo.tm[iw % N]:.2f})")
        b = [np.maximum(x / scale, 1e-300) for x in new]
        if it > 5 and hi - lo < 1e-4 * hi:
            break
    return b, hist, v


def iterate_bounds(geo, Rn, Dn, rho_node, R_cell, drho_cell, normA, oscA, D2, normSi_sqrt2,
                   iters=200, log=None, tol=1e-9, bubble=True):
    """Monotone iteration  b <- F(b) = Y + M b + Q(b)  from b = Y for b = (omega, theta, beta).
    If it converges, F(b) < b for b := (1+eps) b_lim can be checked; then T maps the b-set
    into itself and is a contraction there (Banach) -- the CAP closes.
    Returns (b, history, vectors)."""
    args = (geo, Rn, Dn, rho_node, R_cell, drho_cell, normA, oscA)
    tiny = np.full(geo.N, 1e-300)
    v = cap_vectors(*args, tiny, tiny, D2, normSi_sqrt2, beta=tiny)
    b = [np.maximum(x, 1e-300) for x in _apply(v, ("Y",))]
    hist = []
    for it in range(iters):
        v = cap_vectors(*args, b[0], b[1], D2, normSi_sqrt2, beta=b[2] if bubble else None)
        new = _apply(v, ("Y", "T1", "T2", "Z2"))
        lin = _apply(v, ("T1", "T2"))
        if not bubble:
            new[2], lin[2] = new[1], lin[1]
        g = [float(np.max(new[i] / b[i])) for i in range(3)]
        hist.append(dict(it=it, growth=g, lin_ratio=float(max(np.max(lin[i] / b[i]) for i in range(3))),
                         omega_max=float(new[0].max()), theta_max=float(new[1].max()),
                         beta_max=float(new[2].max()), Omega_max=float(v["Omega"].max())))
        if log:
            log(f"  b-iter {it:3d}: growth sup {g[0]:.6f} osc {g[1]:.6f} bub {g[2]:.6f}  omega_max={new[0].max():.3e} "
                f"theta_max={new[1].max():.3e} beta_max={new[2].max():.3e} Omega_max={v['Omega'].max():.3e}")
        b = new
        if max(g) < 1 + tol or not np.isfinite(sum(x.max() for x in new)) or new[0].max() > 1e3:
            break
    return b, hist, v


def contraction_constant(geo, Rn, Dn, R_cell, drho_cell, normA, oscA, D2, normSi_sqrt2, b, iters=60,
                         log=None):
    """Rigorous Lipschitz constant of T on the b-set in a q-weighted norm
        ||h||_q = max_c max_n (component c of h on C_n) / q_c[n].
    |DT(f) h| <= M q + Z2(b; q) componentwise for f in the b-set and h with ||h||_q <= 1
    (M: T1 + T2;  Z2(b; q): z2_vectors with Om_b from b and Om_p from q).  q is the power
    iterate of this non-negative map; the returned kappa = max (M q + Z2(b; q)) / q is a valid
    bound for that particular q whatever the convergence of the iteration."""
    N = geo.N
    rho0 = np.zeros(N + 1)
    vb = cap_vectors(geo, Rn, Dn, rho0, R_cell, drho_cell, normA, oscA, b[0], b[1], 0.0, normSi_sqrt2, beta=b[2])
    Om_b, V_b = vb["Omega"], vb["_V"]
    q = [x / max(y.max() for y in b) for x in b]
    kappa = np.inf
    for it in range(iters):
        v = cap_vectors(geo, Rn, Dn, rho0, R_cell, drho_cell, normA, oscA, q[0], q[1], 0.0, normSi_sqrt2, beta=q[2])
        z = z2_vectors(geo, Rn, Dn, D2, Om_b, V_b, v["Omega"], v["_V"])
        new = [up(v["T1" + c] + v["T2" + c] + z[i]) for i, c in enumerate(COMPONENTS)]
        ratios = np.concatenate([new[i] / q[i] for i in range(3)])
        lo, hi = float(ratios.min()), float(ratios.max())
        if log:
            log(f"  contraction power-iter {it:2d}: kappa in [{lo:.4f}, {hi:.4f}]")
        if hi < kappa:
            kappa, qbest = hi, [x.copy() for x in q]
        scale = max(x.max() for x in new)
        q = [np.maximum(x / scale, 1e-300) for x in new]
        if it > 5 and hi - lo < 1e-3 * hi:
            break
    return kappa, qbest


def check_certificate(geo, Rn, Dn, rho_node, R_cell, drho_cell, normA, oscA, D2, normSi_sqrt2, b,
                      bubble=True):
    """F(b) < b componentwise (self-mapping of the b-set) and the contraction constant
    max (M b + Q(b)) / b  (the Lipschitz constant of T on the b-set in the b-weighted norm)."""
    v = cap_vectors(geo, Rn, Dn, rho_node, R_cell, drho_cell, normA, oscA, b[0], b[1], D2, normSi_sqrt2,
                    beta=b[2] if bubble else None)
    F = _apply(v, ("Y", "T1", "T2", "Z2"))
    L = _apply(v, ("T1", "T2", "Z2"))
    k = 3 if bubble else 2
    ok = all(bool(np.all(F[i] < b[i])) for i in range(k))
    contr = float(max(np.max(L[i] / b[i]) for i in range(k)))
    slack = float(min(np.min(1.0 - F[i] / b[i]) for i in range(k)))
    return ok, contr, slack, F, v


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


def lipschitz_A_cells(st: Setup, x_lo, x_hi, tube_phys, n_ang=None):
    """Per-cell Lipschitz constant of x -> A(x) = S^{-1} Dg(x) S in adapted norms on the cell
    box widened by tube_phys (physical).  Arb, closed-form 2x2 Gram eigenvalue, no trigonometry
    (rig.lipschitz_A_cells_arb); ``n_ang`` is accepted for backward compatibility and ignored."""
    return lipschitz_A_cells_arb(st, x_lo, x_hi, tube_phys)
