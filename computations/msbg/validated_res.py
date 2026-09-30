r"""J-resolvent a posteriori enclosure and memory-tail (M1) certificate.  Arb + rounded floats.

SETTING.  Planar Allee system, exact rational parameters, E* the coexistence
equilibrium, J = DF(E*) with a complex pair lambda = mu +- i nu (nu > 0),
Matignon stable with  a pi/2 < |arg lambda| < a pi.

ADAPTED NORM.  S = [[J12, 0], [mu - J11, -nu]]  satisfies  J S = S [[mu,-nu],[nu,mu]].
|u|_S := |S^{-1} u|_2.  For every scalar function f analytic at the spectrum,
f(J) = S R(f(lambda)) S^{-1} with R(w) the real 2x2 form of the complex number w,
hence  ||f(J)||_S = |f(lambda)|.  In particular
    ||Psi_J(s)||_S = |psi_lambda(s)|,   ||E_a(J t^a)||_S = |E_a(lambda t^a)|.

THEOREM R (resolvent a posteriori bound).  xhat = p + I^a[phi], rho = phi - g(xhat),
e = x - xhat.  Then  e = I^a[ J e + (g(x) - g(xhat) - J e) - rho ],  i.e.
    e = Psi_J * ( q - rho ),      |q(s)|_S <= a(s) |e(s)|_S,
    a(s) >= sup { ||S^{-1}(Dg(xi) - J) S||_2 : |xi - xhat(s)|_S <= r }.
With  W_{n,j} >= sup_{t in C_n} int_{C_j} |psi(t-s)| ds  (j < n),
      w_n     >= int_0^{h_n} |psi|,
      D_n = sum_{j<n} W_{n,j} Rs_j + w_n Rs_n,     Rs_j >= sup_{C_j} |rho|_S,
      U_n = ( D_n + sum_{j<n} W_{n,j} a_j U_j ) / (1 - w_n a_n),
if every w_n a_n < 1 and max U_n < r then x exists on [0,T] and
sup_{C_n} |x - xhat|_S <= U_n.   (Proof: TASK-0004 return, section 4; same
bootstrap as the TASK-0002 theorem with the kernel (t-s)^{a-1}/Gamma(a) replaced
by |psi_lambda|.  It uses the variation-of-constants identity for the linear
Volterra equation, which ROUND-0005 audits.)

MEMORY-TAIL BOUND.  For t >= T,
    v_T(t) = E_a(J t^a)(p - E*) + int_0^T Psi_J(t-s) N(u(s)) ds,
so  M_T <= phi_b(T) |p - E*|_S + sum_{far} h_j psi_dec(T - t_{j+1}) N_j + N_near K_up,
with phi_b, psi_dec the decreasing closed-form bounds from the Mittag-Leffler
integral representation and N_j >= sup_{C_j} |N(u)|_S.
"""
from __future__ import annotations

import math
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from .kernel_bound import envelope_table, exact_constants
from .lyapunov_l1 import Q

__all__ = ["Setup", "kernel_integrator", "cell_coefficients", "resolvent_recursion",
           "nonlinearity_sup", "memory_tail_bound", "m1_radius"]

_UP = 1.0 + 1e-13


def _l2_upper(balls):
    """Upper bound of sqrt(sum b_i^2) from magnitudes (avoids sqrt of balls containing 0)."""
    from flint import arb
    tot = arb(0)
    for b in balls:
        m = arb(b.abs_upper())
        tot += m * m
    return float(tot.sqrt().abs_upper()) * (1.0 + 1e-13)


def up(x):
    return np.nextafter(np.asarray(x, dtype=np.float64) * _UP, np.inf)


class Setup:
    """Exact equilibrium data and adapted-norm constants (Arb, rounded outward to floats)."""

    def __init__(self, theta, a, b, m, alpha, p, prec=200):
        from flint import arb, ctx
        ctx.prec = prec
        self.str = dict(theta=str(theta), a=str(a), b=str(b), m=str(m), alpha=str(alpha),
                        p=[str(p[0]), str(p[1])])
        th, a_, b_, m_, al = (Q(v) for v in (theta, a, b, m, alpha))
        self.q = dict(theta=th, a=a_, b=b_, m=m_, alpha=al, p=[Q(p[0]), Q(p[1])])
        xs = m_ / b_
        ys = (1 - xs) * (xs - th) / a_
        J11, J12, J21 = xs * (1 + th - 2 * xs), -a_ * xs, b_ * ys
        tr, det = J11, -J12 * J21
        mu = tr / 2
        nu2 = det - tr * tr / 4
        assert th < xs < 1 and ys > 0 and nu2 > 0, "need a coexistence point with complex eigenvalues"
        self.xs, self.ys, self.J = xs, ys, [[J11, J12], [J21, Q(0)]]
        self.mu, self.nu2 = mu, nu2
        self.spec = (str(al), str(mu), str(nu2))
        A = lambda q: arb(q.p) / arb(q.q)
        nu = A(nu2).sqrt()
        S = [[A(J12), arb(0)], [A(mu - J11), -nu]]
        dS = S[0][0] * S[1][1]
        Si = [[S[1][1] / dS, arb(0)], [-S[1][0] / dS, S[0][0] / dS]]
        self.S_arb, self.Si_arb = S, Si
        fro = lambda M: _l2_upper([M[0][0], M[0][1], M[1][0], M[1][1]])
        self.normS = fro(S)                                   # Frobenius >= ||S||_2
        self.normSi = fro(Si)                                 # Frobenius >= ||S^{-1}||_2
        c = (A(self.q["p"][0] - xs), A(self.q["p"][1] - ys))
        xi = (Si[0][0] * c[0] + Si[0][1] * c[1], Si[1][0] * c[0] + Si[1][1] * c[1])
        self.c_norm = _l2_upper(xi)
        self.c2 = 3 * xs - 1 - th
        self.C = exact_constants(self.spec, prec)
        self.alpha_f = float(al.p) / float(al.q)
        self.E_f = (float(xs.p) / float(xs.q), float(ys.p) / float(ys.q))
        self.theta_f = float(th.p) / float(th.q)

    def floats(self):
        f = lambda q: float(q.p) / float(q.q)
        return {k: f(v) for k, v in self.q.items() if k != "p"}, [f(v) for v in self.q["p"]]


# ---------------------------------------------------------------------------
# kernel integrals from a rigorous envelope table
# ---------------------------------------------------------------------------
class kernel_integrator:
    r"""Upper bounds of  int_{s0}^{s1} |psi_lambda(s)| ds  for 0 <= s0 <= s1 <= s_max.

    |psi(s)| ds = (1/a) |E_{a,a}(lambda rho)| d rho with rho = s^a.  ``env`` is a rigorous
    piecewise-constant upper envelope of |E_{a,a}(lambda rho)| on [0, rho0].
    """

    def __init__(self, setup: Setup, s_max, workers=None):
        self.al = setup.alpha_f
        rho0 = float(up(s_max ** self.al)) * 1.0000001
        self.edges, self.env, self.mid = envelope_table(setup.spec, rho0, workers)
        w = np.diff(self.edges)
        self.G = np.concatenate([[0.0], np.cumsum(up(self.env * w))]) * _UP     # upper cumulative
        self.G_lo = np.concatenate([[0.0], np.cumsum(self.env * w)]) * (1 - 1e-12)
        self.inv_a = float(up(1.0 / self.al))
        self.rho0 = rho0

    def _Gup(self, rho):
        i = np.clip(np.searchsorted(self.edges, rho, side="right") - 1, 0, len(self.env) - 1)
        return up(self.G[i] + self.env[i] * np.maximum(rho - self.edges[i], 0.0))

    def _Glo(self, rho):
        i = np.clip(np.searchsorted(self.edges, rho, side="right") - 1, 0, len(self.env) - 1)
        v = self.G_lo[i] + self.env[i] * np.maximum(rho - self.edges[i], 0.0)
        return np.nextafter(v * (1 - 1e-12), -np.inf)

    def integral(self, s0, s1):
        s0 = np.maximum(np.asarray(s0, float), 0.0)
        s1 = np.asarray(s1, float)
        rb = np.minimum(up(s1 ** self.al), self.rho0)
        ra = np.maximum(np.nextafter(s0 ** self.al * (1 - 1e-13), -np.inf), 0.0)
        return np.maximum(up((self._Gup(rb) - self._Glo(ra)) * self.inv_a), 0.0)

    def total_upper(self, setup: Setup):
        """K_up >= int_0^inf |psi|: table up to rho0 plus the closed-form tail."""
        from flint import arb
        C = setup.C
        a = C["a"]
        x0 = C["xl"] * arb(self.rho0)
        tail = C["B"] / (C["xl"] ** 2 * arb(self.rho0)) \
            + (-(C["c"] * x0 ** (1 / a))).exp() / (C["c"] * C["xl"])
        return float(up((self.G[-1] + float(tail.abs_upper())) * self.inv_a))


# ---------------------------------------------------------------------------
# per-cell coefficient a_n and nonlinearity sup N_n   (Arb, parallel)
# ---------------------------------------------------------------------------
_W = {}


def _l2_upper(balls):
    """Upper bound of sqrt(sum b_i^2) for Arb balls b_i.

    Squares of balls that contain 0 are balls that contain negative numbers, and
    Arb's sqrt of such a ball is NaN.  The bound is therefore taken from the
    magnitudes |b_i| <= abs_upper(b_i), which are non-negative exact floats.
    """
    from flint import arb
    tot = arb(0)
    for b in balls:
        m = arb(b.abs_upper())
        tot += m * m
    return float(tot.sqrt().abs_upper()) * _UP


def _cinit(strs):
    from flint import arb, ctx
    ctx.prec = 128
    st = Setup(strs["theta"], strs["a"], strs["b"], strs["m"], strs["alpha"], strs["p"], prec=128)
    A = lambda q: arb(q.p) / arb(q.q)
    _W.update(S=st.S_arb, Si=st.Si_arb, th=A(st.q["theta"]), a=A(st.q["a"]), b=A(st.q["b"]),
              m=A(st.q["m"]), xs=A(st.xs), ys=A(st.ys), c2=A(st.c2),
              J=[[A(v) for v in row] for row in st.J])


def _box(lo, hi, pad):
    """Ball containing [lo - pad, hi + pad]."""
    from flint import arb
    lo_, hi_ = arb(float(lo)) - arb(float(pad)), arb(float(hi)) + arb(float(pad))
    return lo_.union(hi_)


def _fro_conj(M):
    """Frobenius norm (>= 2-norm) of S^{-1} M S."""
    S, Si = _W["S"], _W["Si"]
    SM = [[Si[i][0] * M[0][j] + Si[i][1] * M[1][j] for j in range(2)] for i in range(2)]
    T = [[SM[i][0] * S[0][j] + SM[i][1] * S[1][j] for j in range(2)] for i in range(2)]
    return _l2_upper([T[0][0], T[0][1], T[1][0], T[1][1]])


def _coef(job):
    xlo, xhi, ylo, yhi, pad = job
    x, y = _box(xlo, xhi, pad), _box(ylo, yhi, pad)
    th, a, b, m, J = _W["th"], _W["a"], _W["b"], _W["m"], _W["J"]
    Dg = [[-3 * x * x + 2 * (1 + th) * x - th - a * y, -a * x], [b * y, b * x - m]]
    M = [[Dg[i][j] - J[i][j] for j in range(2)] for i in range(2)]
    return _fro_conj(M)


def _nsup(job):
    xlo, xhi, ylo, yhi, pad = job
    x, y = _box(xlo, xhi, pad), _box(ylo, yhi, pad)
    u1, u2 = x - _W["xs"], y - _W["ys"]
    n1 = -_W["c2"] * u1 * u1 - _W["a"] * u1 * u2 - u1 * u1 * u1
    n2 = _W["b"] * u1 * u2
    Si = _W["Si"]
    q = (Si[0][0] * n1 + Si[0][1] * n2, Si[1][0] * n1 + Si[1][1] * n2)
    return _l2_upper(q)


def _pmap(fn, jobs, strs, workers):
    with ProcessPoolExecutor(max_workers=workers or os.cpu_count(), initializer=_cinit,
                             initargs=(strs,)) as ex:
        return np.array(list(ex.map(fn, jobs, chunksize=max(1, len(jobs) // ((workers or 8) * 4)))))


def cell_coefficients(setup, x_lo, x_hi, y_lo, y_hi, pad, workers=None):
    jobs = [(x_lo[n], x_hi[n], y_lo[n], y_hi[n], pad) for n in range(len(x_lo))]
    return _pmap(_coef, jobs, setup.str, workers)


def nonlinearity_sup(setup, x_lo, x_hi, y_lo, y_hi, pads, workers=None):
    jobs = [(x_lo[n], x_hi[n], y_lo[n], y_hi[n], float(pads[n])) for n in range(len(x_lo))]
    return _pmap(_nsup, jobs, setup.str, workers)


# ---------------------------------------------------------------------------
# recursion
# ---------------------------------------------------------------------------
def resolvent_recursion(tm, Rs, a_coef, ker: kernel_integrator, sub=4):
    """U_n, D_n, kappa_n.  ``sub`` splits C_n when taking the sup over t in C_n."""
    N = len(tm) - 1
    U = np.zeros(N)
    D = np.zeros(N)
    kap = np.zeros(N)
    fr = np.linspace(0.0, 1.0, sub + 1)
    for n in range(N):
        h = tm[n + 1] - tm[n]
        w_self = float(ker.integral(0.0, h))
        if n:
            W = np.zeros(n)
            for k in range(sub):
                ta, tb = tm[n] + fr[k] * h, tm[n] + fr[k + 1] * h
                W = np.maximum(W, ker.integral(ta - tm[1:n + 1], tb - tm[:n]))
            hist_R = float(up(np.dot(W, Rs[:n]))) * (1 + (n + 2) * 2.0 ** -52)
            hist_U = float(up(np.dot(W, up(a_coef[:n] * U[:n])))) * (1 + (n + 2) * 2.0 ** -52)
        else:
            hist_R = hist_U = 0.0
        D[n] = float(up(hist_R + float(up(w_self * Rs[n]))))
        kap[n] = float(up(w_self * a_coef[n]))
        if kap[n] >= 1.0:
            U[n:] = D[n:] = kap[n:] = np.inf
            return U, D, kap
        U[n] = float(up((D[n] + hist_U) / np.nextafter(1.0 - kap[n], -np.inf)))
    return U, D, kap


# ---------------------------------------------------------------------------
# M_T and the M1 inequality
# ---------------------------------------------------------------------------
def memory_tail_bound(setup: Setup, tm, Nsup, K_up, sigma1_list=(25.0, 50.0, 100.0, 200.0, 400.0)):
    """Rigorous upper bound of M_T = sup_{t >= T} |v_T(t)|_S, T = tm[-1]."""
    from flint import arb, ctx
    ctx.prec = 200
    C = setup.C
    a, xl, c = C["a"], C["xl"], C["c"]
    T = float(tm[-1])

    def phi_b(t):
        x = xl * arb(t) ** a
        return (1 / a) * (-(c * x ** (1 / a))).exp() + C["Bphi"] / x

    def psi_dec(sig):
        s = arb(sig)
        x = xl * s ** a
        pole = (1 / a) * xl ** ((1 - a) / a) * (-(c * xl ** (1 / a) * s)).exp()
        return pole + s ** (a - 1) * C["B"] / (x * x)

    term_phi = float(phi_b(T).abs_upper()) * setup.c_norm * _UP
    h = np.diff(tm)
    best = None
    for s1 in sigma1_list:
        if s1 >= T:
            continue
        far = tm[1:] <= T - s1
        if not far.any():
            continue
        dist = T - tm[1:][far]
        # psi_dec is decreasing: evaluate on a coarse rigorous ladder and use the value at a
        # smaller-or-equal sigma for every cell
        ladder = np.geomspace(s1, max(T, s1 * 1.0001), 400)
        vals = np.array([float(psi_dec(float(np.nextafter(v, -np.inf))).abs_upper()) for v in ladder])
        idx = np.clip(np.searchsorted(ladder, dist, side="right") - 1, 0, len(ladder) - 1)
        far_sum = float(up(np.dot(up(h[far] * vals[idx]), Nsup[far]))) * (1 + 1e-12)
        near = float(np.max(Nsup[~far])) if (~far).any() else 0.0
        near_term = float(up(near * K_up))
        tot = float(up(term_phi + far_sum + near_term))
        cand = {"sigma1": s1, "term_linear_flow": term_phi, "term_far_history": far_sum,
                "term_near_history": near_term, "N_near_sup": near, "M_T_upper": tot}
        if best is None or tot < best["M_T_upper"]:
            best = cand
    return best


def adapted_C(setup: Setup, n_arcs=20000):
    """(C0, c3) with |N(u)|_S <= (C0 + c3 r)|u|_S^2 for |u|_S <= r; rigorous."""
    from flint import arb, ctx
    ctx.prec = 128
    _cinit(setup.str)
    S, Si = _W["S"], _W["Si"]
    two_pi = 2 * arb.pi()
    half = float((two_pi / (2 * n_arcs)).abs_upper())
    C0 = c3 = 0.0
    for k in range(n_arcs):
        th = arb((two_pi * (2 * k + 1) / (2 * n_arcs)).mid(), half)
        xi = (th.cos(), th.sin())
        u1 = S[0][0] * xi[0] + S[0][1] * xi[1]
        u2 = S[1][0] * xi[0] + S[1][1] * xi[1]
        n2 = (-_W["c2"] * u1 * u1 - _W["a"] * u1 * u2, _W["b"] * u1 * u2)
        q2 = (Si[0][0] * n2[0] + Si[0][1] * n2[1], Si[1][0] * n2[0] + Si[1][1] * n2[1])
        q3 = (Si[0][0] * (-u1 ** 3), Si[1][0] * (-u1 ** 3))
        C0 = max(C0, _l2_upper(q2))
        c3 = max(c3, _l2_upper(q3))
    return C0 * _UP, c3 * _UP


def m1_radius(M_up, K_up, C0, c3):
    """Rational r maximising  r - K (C0 + c3 r) r^2 - M ;  returns (margin_lower, r, K C r)."""
    from flint import arb, fmpq
    best = None
    for num in range(1, 4000):
        r = arb(fmpq(num, 20000))
        val = r - arb(K_up) * (arb(C0) + arb(c3) * r) * r * r - arb(M_up)
        lo = float(val.lower())
        if best is None or lo > best[0]:
            best = (lo, f"{num}/20000", float((arb(K_up) * (arb(C0) + arb(c3) * r) * r).abs_upper()))
    return best
