r"""Verified arithmetic layer for the TASK-0006 CAP (TASK-0007 hardening).

Two kinds of quantities feed the proof:

* **Arb balls** (python-flint, 128-bit): every elementary function (powers with real
  exponents, Gamma, square roots of exact data) is evaluated here and converted to a
  binary64 bound with ``arb_hi`` / ``arb_lo`` (float(arb) rounds to nearest, so one
  ``nextafter`` step outward is added and the result is re-checked in Arb).
* **binary64 algebra on non-negative data** (sums, dot products, matrix products,
  square roots): bounded with Higham's standard model.  For any summation order,
  with or without FMA, and for every BLAS blocking,

      fl( sum_{i<n} x_i y_i ) = sum_i x_i y_i (1 + theta_i),   |theta_i| <= gamma_n,
      gamma_n = n u / (1 - n u),   u = 2^-53,

  (Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., eq. (3.5) and
  §3.1: the bound depends only on the number of roundings on each term's path, not on
  the order).  For NON-NEGATIVE terms this gives  sum x_i y_i <= fl(...) / (1 - gamma_n)
  <= fl(...) (1 + 2 gamma_n), which ``infl(value, n)`` returns after one more outward
  rounding.  Nothing else about the platform is assumed: not the libm accuracy, not
  the reduction order of OpenBLAS, not the presence or absence of FMA.

Remaining IEEE-754 assumptions (listed for the paper): binary64 with round-to-nearest
for + - * / sqrt (required by the standard), ``nextafter`` exact, no flush-to-zero
of the quantities involved (all are >= 1e-300 or exactly 0), numpy reductions
performed in binary64 (no extended-precision or reduced-precision accumulation:
numpy/OpenBLAS accumulate in double; a higher-precision accumulator would only
make the bounds more conservative).
"""
from __future__ import annotations

import math
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np

U = 2.0 ** -53                 # unit roundoff of binary64


def gam(n):
    """Higham's gamma_n = n u / (1 - n u) (float or array, rounded up)."""
    n = np.asarray(n, dtype=np.float64)
    return np.nextafter(n * U / (1.0 - n * U), np.inf)


def infl(x, n):
    """Upper bound of the exact value of a non-negative float result ``x`` obtained
    through at most ``n`` roundings per term (dot product of length n, sum of n+1 terms,
    ...): x (1 + 2 gamma_n), rounded outward."""
    x = np.asarray(x, dtype=np.float64)
    return np.nextafter(x * (1.0 + 2.0 * gam(n)), np.inf)


def defl(x, n):
    """Lower bound counterpart of ``infl`` (x >= 0)."""
    x = np.asarray(x, dtype=np.float64)
    return np.maximum(np.nextafter(x * (1.0 - 2.0 * gam(n)), -np.inf), 0.0)


def arb_hi(x):
    """Smallest float we can certify to be >= the ball x (checked in Arb)."""
    from flint import arb
    x = arb(x)
    if not x.is_finite():
        raise ValueError(f"arb_hi of a non-finite ball: {x}")
    f = float(np.nextafter(float(x.upper()), np.inf))
    for _ in range(4):                       # cannot fail for finite x; kept as a guard
        if arb(f) >= x.upper():
            return f
        f = float(np.nextafter(f, np.inf))
    raise ValueError(f"arb_hi could not certify an upper float for {x}")


def arb_lo(x):
    from flint import arb
    x = arb(x)
    if not x.is_finite():
        raise ValueError(f"arb_lo of a non-finite ball: {x}")
    f = float(np.nextafter(float(x.lower()), -np.inf))
    for _ in range(4):
        if arb(f) <= x.lower():
            return f
        f = float(np.nextafter(f, -np.inf))
    raise ValueError(f"arb_lo could not certify a lower float for {x}")


def arb_norm2_hi(v):
    """Upper float bound of |v|_2 for a list of Arb balls (through magnitudes)."""
    from flint import arb
    tot = arb(0)
    for b in v:
        m = arb(b.abs_upper())
        tot += m * m
    return arb_hi(tot.sqrt())


# ---------------------------------------------------------------------------
# geometry tables: all real-exponent powers in Arb, one mesh row per job
# ---------------------------------------------------------------------------
_G = {}


def _tab_init(tm, phi, alpha_str, prec, c_alpha):
    from flint import arb, ctx
    from .validated import to_arb
    ctx.prec = prec
    _G["prec"] = prec
    _G["c_alpha_val"] = arb(float(c_alpha))
    _G["tm"] = [arb(float(v)) for v in tm]
    a = to_arb(alpha_str)
    _G["a"] = a
    _G["Ga"], _G["Ga1"] = a.gamma(), (a + 1).gamma()
    N = len(tm) - 1
    _G["N"] = N
    phi = np.asarray(phi, float)
    _G["phi0"] = [arb(float(phi[0, c])) for c in range(2)]
    # slopes m_k = (phi_{k+1} - phi_k) / h_k, exact from the float data
    _G["m"] = [[(arb(float(phi[k + 1, c])) - arb(float(phi[k, c]))) / (_G["tm"][k + 1] - _G["tm"][k])
                for c in range(2)] for k in range(N)]
    _G["mn"] = [arb(0) for _ in range(N)]
    for k in range(N):
        mk = _G["m"][k]
        _G["mn"][k] = (arb(mk[0].abs_upper()) ** 2 + arb(mk[1].abs_upper()) ** 2).sqrt()


def _hull0(x):
    """[0, upper(x)] for a ball whose true value is >= 0 (guards tiny negative radii)."""
    from flint import arb
    if x.lower() >= 0:
        return x
    return arb(0).union(arb(x.upper()))


def _tab_row(n):
    """Everything the CAP needs about node/cell n, from Arb balls.

    Returns floats (all upper bounds unless noted):
      w_hi, w_lo [n]   : cell weights w_{n,j} = ((t_n-t_j)^a - (t_n-t_{j+1})^a)/G(a+1), j<n
      d      [n-1]     : (t_n-t_{j+1})^{a-2} - (t_n-t_j)^{a-2}, j<=n-2   (cell n, Green part)
      rem    [n]       : (1/G(a)) int_{C_j} |k(t_n-s) - mean| ds bound, j<n  (mean-kernel remainder)
      O1, X1           : osc_{C_n} |xhat'| and sup_{C_n}|xhat'| for cell n (inf for n=0 or n=N)
      HA, DTA, Ea, GREEN : h_n^a/G(a+1); (t_{n+1}^a - t_n^a)/G(a+1); Ea[n]; h_n^2/8 (1-a)/G(a)
    """
    from flint import arb, ctx
    ctx.prec = _G["prec"]
    tm, a, Ga, Ga1, N = _G["tm"], _G["a"], _G["Ga"], _G["Ga1"], _G["N"]
    tn = tm[n]
    is_cell = n < N
    # --- powers of (t_n - t_j), j < n ---------------------------------------------------
    Pa = [None] * (n + 1)
    Pa1 = [None] * n
    Pa2 = [None] * n
    for j in range(n):
        dj = tn - tm[j]
        Pa[j] = dj ** a
        Pa1[j] = dj ** (a - 1)
        Pa2[j] = dj ** (a - 2)
    Pa[n] = arb(0)
    w_hi = np.zeros(n)
    w_lo = np.zeros(n)
    Wb = [None] * n
    for j in range(n):
        Wb[j] = _hull0((Pa[j] - Pa[j + 1]) / Ga1)
        w_hi[j] = arb_hi(Wb[j])
        w_lo[j] = arb_lo(Wb[j])
    d = np.zeros(max(n - 1, 0))
    for j in range(n - 1):
        d[j] = arb_hi(_hull0(Pa2[j + 1] - Pa2[j]))
    rem = np.zeros(n)
    for j in range(n):
        two_w = 2 * Wb[j]
        if j <= n - 2:
            hj = tm[j + 1] - tm[j]
            alt = hj / 2 * _hull0(Pa1[j + 1] - Pa1[j]) / Ga
            rem[j] = min(arb_hi(two_w), arb_hi(alt))
        else:
            rem[j] = arb_hi(two_w)
    out = dict(n=n, w_hi=w_hi, w_lo=w_lo, d=d, rem=rem)
    if not is_cell:
        return out
    tn1 = tm[n + 1]
    h = tn1 - tn
    out["HA"] = arb_hi(h ** a / Ga1)
    out["DTA"] = arb_hi(_hull0(tn1 ** a - tn ** a) / Ga1) if n > 0 else arb_hi(h ** a / Ga1)
    out["GREEN"] = arb_hi(h * h / 8 * (1 - a) / Ga)
    ca = _G["c_alpha_val"]
    if n > 0:
        out["Ea"] = min(arb_hi(h * h * a * (1 - a) * tn ** (a - 2) / 8 / Ga1), arb_hi(ca * h ** a / Ga1))
    else:
        out["Ea"] = arb_hi(ca * h ** a / Ga1)
    if n == 0:
        out["O1"] = out["X1"] = float("inf")
        return out
    # --- osc and sup of xhat' on C_n (see cap.xhat_prime_oscillation for the derivation) ---
    m, mn, phi0 = _G["m"], _G["mn"], _G["phi0"]
    phi0n = (arb(phi0[0].abs_upper()) ** 2 + arb(phi0[1].abs_upper()) ** 2).sqrt()
    # exact (cancelling) part D
    chord = (tn1 ** (a - 1) - tn ** (a - 1)) / Ga
    D = [phi0[0] * chord, phi0[1] * chord]
    rem_s = h * h / 8 * phi0n * (1 - a) * (2 - a) * tn ** (a - 3) / Ga
    for k in range(n - 1):                     # k <= n-2
        Qk = (tn1 - tm[k]) ** a - (tn1 - tm[k + 1]) ** a          # Delta_k(t_{n+1})
        br = (Qk - (Pa[k] - Pa[k + 1])) / Ga1                       # bracket_k(t_{n+1})
        D[0] += m[k][0] * br
        D[1] += m[k][1] * br
        rem_s += mn[k] * h * h / 8 * a * (1 - a) * _hull0(Pa2[k + 1] - Pa2[k]) / Ga1
    rem_s += mn[n - 1] * h ** a / Ga1 + mn[n] * h ** a / Ga1
    Dn = (arb(D[0].abs_upper()) ** 2 + arb(D[1].abs_upper()) ** 2).sqrt()
    O1 = Dn + 2 * rem_s
    out["O1"] = arb_hi(O1)
    # |xhat'(t_n)| exactly
    xp = [phi0[c] * tn ** (a - 1) / Ga for c in range(2)]
    for k in range(n):
        dk = (Pa[k] - Pa[k + 1]) / Ga1
        xp[0] += m[k][0] * dk
        xp[1] += m[k][1] * dk
    xpn = (arb(xp[0].abs_upper()) ** 2 + arb(xp[1].abs_upper()) ** 2).sqrt()
    out["X1"] = arb_hi(xpn + O1)
    return out


def interpolation_constants_arb(alpha_str, ratios, K=4000, prec=64):
    """c_alpha, c_loc and c_prev(ratio) as in cap.interpolation_constants, but every
    subinterval value is an Arb enclosure (tau as a ball over the subinterval; the ratio
    as a ball over one of <= 64 ratio groups).  Valid sup bounds by inclusion monotonicity."""
    from flint import arb, ctx
    from .validated import to_arb
    ctx.prec = prec
    a = to_arb(alpha_str)
    e = np.linspace(0.0, 1.0, K + 1)
    taus = [arb(float(e[i])).union(arb(float(e[i + 1]))) for i in range(K)]

    def pw(lo, hi, p):
        """[lo, hi]^p for 0 <= lo <= hi, p > 0 (increasing): [lo^p, hi^p], lo^p := 0 at lo = 0."""
        l = arb(0) if lo == 0.0 else arb(lo) ** p
        return l.union(arb(hi) ** p)

    ta = [pw(float(e[i]), float(e[i + 1]), a) for i in range(K)]                  # tau^a
    oma = [pw(float(1 - e[i + 1]), float(1 - e[i]), a) for i in range(K)]         # (1 - tau)^a
    c_alpha = max(arb_hi(ta[i] - taus[i]) for i in range(K))
    c_loc = max(arb_hi(ta[i] - taus[i] + 2 * taus[i] * oma[i]) for i in range(K))
    ratios = np.asarray(ratios, float)
    lo, hi = float(ratios.min()), float(ratios.max())
    edges = np.geomspace(lo * (1 - 1e-12), hi * (1 + 1e-12), 65) if hi > lo else np.array([lo * (1 - 1e-12), hi * (1 + 1e-12)])
    idx = np.clip(np.searchsorted(edges, ratios, side="right") - 1, 0, len(edges) - 2)
    cp_group = np.zeros(len(edges) - 1)
    for g in range(len(edges) - 1):
        if not np.any(idx == g):
            continue
        r = arb(float(edges[g])).union(arb(float(edges[g + 1])))
        ra, r1a = r ** a, (1 + r) ** a - 1
        cp_group[g] = max(arb_hi((1 - taus[i]) * ra + taus[i] * r1a - (taus[i] + r) ** a + ta[i]) for i in range(K))
    return c_alpha, c_loc, cp_group[idx]


def geometry_tables(tm, phi, alpha_str, workers=None, prec=128):
    """Assemble the Arb-backed tables for cap.Geometry (parallel over mesh rows)."""
    tm = np.asarray(tm, float)
    N = len(tm) - 1
    h = np.diff(tm)
    ratios = np.concatenate([[1.0], h[:-1] / h[1:]])
    c_alpha, c_loc, c_prev = interpolation_constants_arb(alpha_str, ratios)
    N1 = N + 1
    W_hi = np.zeros((N1, N)); W_lo = np.zeros((N1, N))
    D = np.zeros((N, N)); REM = np.zeros((N1, N))
    O1 = np.full(N, np.inf); X1 = np.full(N, np.inf)
    HA = np.zeros(N); DTA = np.zeros(N); Ea = np.zeros(N); GREEN = np.zeros(N)
    with ProcessPoolExecutor(max_workers=workers or os.cpu_count(), initializer=_tab_init,
                             initargs=(tm, phi, alpha_str, prec, c_alpha)) as ex:
        for r in ex.map(_tab_row, range(N, -1, -1), chunksize=max(1, N // ((workers or 8) * 16))):
            n = r["n"]
            W_hi[n, :n] = r["w_hi"]; W_lo[n, :n] = r["w_lo"]
            REM[n, :n] = r["rem"]
            if n < N:
                D[n, :max(n - 1, 0)] = r["d"]
                O1[n], X1[n] = r["O1"], r["X1"]
                HA[n], DTA[n], Ea[n], GREEN[n] = r["HA"], r["DTA"], r["Ea"], r["GREEN"]
    # dw[n, j] = w_{n,j} - w_{n+1,j} >= 0 (kernel decreasing in t): hi - lo, rounded outward
    DW = np.nextafter(np.maximum(W_hi[:-1] - W_lo[1:], 0.0), np.inf)
    return dict(W_hi=W_hi, W_lo=W_lo, DW=DW, D=D, REM=REM, O1=O1, X1=X1, HA=HA, DTA=DTA, Ea=Ea,
                GREEN=GREEN, c_alpha=c_alpha, c_loc=c_loc, c_prev=c_prev)


# ---------------------------------------------------------------------------
# Lipschitz constant of x -> S^{-1} Dg(x) S, adapted norms, without trigonometry
# ---------------------------------------------------------------------------
def lipschitz_A_cells_arb(st, x_lo, x_hi, tube_phys, prec=128):
    """D2[n] >= sup_{|u|_2 = 1} ||S^{-1} D^2g(x)[S u] S||_F over x in the widened cell box.

    D^2g(x)[e] = [[c e_x - a e_y, -a e_x], [b e_y, b e_x]],  c = -6 x + 2(1+theta), is linear
    in e and affine in c.  For fixed u the Frobenius norm is convex in c, so the sup over
    the c-interval of the cell is attained at an endpoint; for fixed c the map u -> G_c(u)
    is linear R^2 -> R^{2x2}, and its (2 -> Frobenius) operator norm is the square root of
    the largest eigenvalue of the 2x2 Gram matrix M_ij = <G_c(e_i), G_c(e_j)>_F, computed
    in Arb through the closed-form eigenvalue.  No sampling, no trigonometry."""
    from flint import arb, ctx
    ctx.prec = prec
    S, Si = st.S_arb, st.Si_arb
    q = st.q
    th, a, b = (arb(q[k].p) / arb(q[k].q) for k in ("theta", "a", "b"))
    tube = arb(float(tube_phys))

    def G_of(c, u):                       # u = (u1, u2) balls
        ex = S[0][0] * u[0] + S[0][1] * u[1]
        ey = S[1][0] * u[0] + S[1][1] * u[1]
        H = [[c * ex - a * ey, -a * ex], [b * ey, b * ex]]
        SM = [[Si[i][0] * H[0][j] + Si[i][1] * H[1][j] for j in range(2)] for i in range(2)]
        return [[SM[i][0] * S[0][j] + SM[i][1] * S[1][j] for j in range(2)] for i in range(2)]

    def opnorm(c):
        G1 = G_of(c, (arb(1), arb(0)))
        G2 = G_of(c, (arb(0), arb(1)))
        m11 = sum(G1[i][j] ** 2 for i in range(2) for j in range(2))
        m22 = sum(G2[i][j] ** 2 for i in range(2) for j in range(2))
        m12 = sum(G1[i][j] * G2[i][j] for i in range(2) for j in range(2))
        tr, det = m11 + m22, m11 * m22 - m12 * m12
        disc = _hull0(tr * tr - 4 * det)
        lam = (tr + disc.sqrt()) / 2
        return arb_hi(_hull0(lam).sqrt())

    x_lo = np.asarray(x_lo, float); x_hi = np.asarray(x_hi, float)
    out = np.zeros(len(x_lo))
    cache = {}
    for n in range(len(x_lo)):
        vals = []
        for xs, sgn in ((x_lo[n], -1), (x_hi[n], +1)):
            key = (float(xs), sgn)
            if key not in cache:
                x = arb(float(xs)) + sgn * tube
                cache[key] = opnorm(-6 * x + 2 * (1 + th))
            vals.append(cache[key])
        out[n] = max(vals)
    return out
