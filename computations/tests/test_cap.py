"""Tests for msbg.cap (TASK-0006 rigorous oscillation-Banach constants)."""
import math

import numpy as np
import pytest

flint = pytest.importorskip("flint")

from msbg.cap import (Geometry, _B_source_vectors, cap_vectors, cell_weights,   # noqa: E402
                      interpolation_constants, rigorous_hat_weights, rigorous_inverse,
                      xhat_second_derivative)
from msbg.orbit_linearized import hat_weights                                  # noqa: E402

ALPHA = 0.85


def _mesh(N=40, T=3.0):
    return T * (np.arange(N + 1) / N) ** 2


def test_rigorous_hat_weights_match_float():
    tm = _mesh()
    Wm, Wr = rigorous_hat_weights(tm, "17/20", workers=2)
    W = hat_weights(tm, ALPHA)
    assert np.all(Wr >= 0) and Wr.max() < 1e-13
    assert np.abs(Wm - W).max() < 1e-11
    # row sums of hat weights = int_0^{t_n} (t_n - s)^{a-1}/Gamma(a) ds = t_n^a / Gamma(a+1)
    rs = Wm.sum(1)
    assert np.allclose(rs, tm**ALPHA / math.gamma(ALPHA + 1), rtol=1e-10, atol=1e-14)


def test_cell_weights_sum():
    tm = _mesh()
    for n in (5, 17, 40):
        w = cell_weights(tm, tm[n], ALPHA)
        assert np.all(w[n:] < 1e-300)
        assert abs(w[:n].sum() - tm[n] ** ALPHA / math.gamma(ALPHA + 1)) < 1e-12


def test_rigorous_inverse_bounds_true_blocks():
    rng = np.random.default_rng(1)
    tm = _mesh(N=25)
    Wm, Wr = rigorous_hat_weights(tm, "17/20", workers=2)
    N1 = len(tm)
    Am = rng.normal(size=(N1, 2, 2)) * 0.5
    Ar = np.zeros_like(Am)
    Rn, Dn, normE, delta, R4 = rigorous_inverse(Wm, Wr, Am, Ar)
    assert normE < 1e-10
    m = 2 * N1
    Abig = np.zeros((m, m))
    for n in range(N1):
        Abig[2 * n:2 * n + 2, 2 * n:2 * n + 2] = Am[n]
    L = np.eye(m) - Abig @ np.kron(Wm, np.eye(2))
    Linv = np.linalg.inv(L).reshape(N1, 2, N1, 2)
    true_blocks = np.linalg.norm(Linv, axis=(1, 3))
    assert np.all(Rn >= true_blocks - 1e-13)
    Dd = Linv[1:] - Linv[:-1]
    idx = np.arange(N1 - 1)
    Dd[idx, :, idx, :] += Linv[idx + 1, :, idx + 1, :]
    Dd[idx, :, idx + 1, :] = 0.0
    true_diff = np.linalg.norm(Dd, axis=(1, 3))
    assert Dn.shape[0] == 2
    assert np.all(Dn[0] >= true_diff - 1e-13)
    Sc = np.cumsum(Linv[1:] - Linv[:-1], axis=2)
    true_S = np.linalg.norm(Sc, axis=(1, 3))
    mask = np.arange(N1 - 1)[:, None] >= np.arange(N1)[None, :] - 1
    assert np.all(Dn[1][mask] >= true_S[mask] - 1e-12)
    # consistency: for a smooth nodal source z the two-term split reproduces |y_{n+1}-y_n|
    z = np.sin(np.linspace(0, 1, N1))[:, None] * np.ones((1, 2))
    y = (Linv.reshape(2 * N1, 2 * N1) @ z.reshape(-1)).reshape(N1, 2)
    dy = np.linalg.norm(y[1:] - y[:-1], axis=1)
    zn = np.linalg.norm(z, axis=1)
    dz = np.linalg.norm(z[1:] - z[:-1], axis=1)
    bound = Dn[0] @ zn + np.diagonal(Rn)[1:] * dz
    assert np.all(bound >= dy - 1e-12)
    Slow = np.tril(Dn[1][:, :N1 - 1]); S1 = np.diagonal(Dn[1][:, 1:])
    bound_abel = Slow @ dz + S1 * zn[1:]
    assert np.all(bound_abel >= dy - 1e-12)
    sup, osc, bub = _B_source_vectors(Rn, Dn, zn, zn[:-1], dz, dz)
    assert np.all(osc >= dy - 1e-12)
    assert np.abs(Rn - true_blocks).max() < 1e-8


def test_interpolation_constants_dominate_samples():
    a = ALPHA
    c_alpha, c_loc, c_prev = interpolation_constants(a, [1.0, 0.5, 2.0])
    tau = np.linspace(0, 1, 200001)
    assert c_alpha >= np.max(tau**a - tau) and c_alpha < np.max(tau**a - tau) + 1e-3
    f = tau**a - tau + 2 * tau * (1 - tau) ** a
    assert c_loc >= f.max() and c_loc < f.max() + 1e-3
    for r, c in zip([1.0, 0.5, 2.0], c_prev):
        d = (1 - tau) * r**a + tau * ((1 + r) ** a - 1) - (tau + r) ** a + tau**a
        assert c >= d.max() and c < d.max() + 2e-3
    assert 0.059 < c_alpha < 0.061 and 0.60 < c_loc < 0.62


def test_xhat_second_derivative_constant_phi():
    """phi == phi0: xhat'' = phi0 (a-1) t^{a-2}/Gamma(a), int_{C_n}|xhat''| exact."""
    tm = np.linspace(0, 2, 21)
    phi0 = np.array([0.3, -0.4])
    phi = np.tile(phi0, (len(tm), 1))
    I2, X1 = xhat_second_derivative(tm, phi, ALPHA)
    n0 = math.sqrt(phi0 @ phi0)
    for n in range(1, 20):
        exact = n0 * (tm[n] ** (ALPHA - 1) - tm[n + 1] ** (ALPHA - 1)) / math.gamma(ALPHA)
        assert I2[n] >= exact and I2[n] < exact * (1 + 1e-9) + 1e-9
        d1 = n0 * tm[n] ** (ALPHA - 1) / math.gamma(ALPHA)          # |xhat'| decreasing: sup at t_n
        assert X1[n] >= d1


def test_B_source_vectors_identity():
    tm = _mesh(N=12)
    Wm, Wr = rigorous_hat_weights(tm, "17/20", workers=2)
    N1 = len(tm)
    Am = np.zeros((N1, 2, 2))
    Rn, Dn, *_ = rigorous_inverse(Wm, Wr, Am, np.zeros_like(Am))
    # A == 0: L_h = I; Frobenius block norms of the identity are sqrt(2) on the diagonal
    assert np.allclose(Rn, math.sqrt(2) * np.eye(N1), atol=1e-10)
    s_node = np.ones(N1)
    sup, osc, bub = _B_source_vectors(Rn, Dn, s_node, np.ones(N1 - 1), 0.5 * np.ones(N1 - 1))
    assert np.all(bub <= sup)
    assert sup.shape == (N1 - 1,) and osc.shape == (N1 - 1,)
    assert np.all(sup >= 1.0)


def test_cap_vectors_identity_case():
    """A == 0 (K == 0): T1 = T2 = Z2 = 0 and Y reproduces rho (PL part + interpolation part)."""
    tm = _mesh(N=15)
    Wm, Wr = rigorous_hat_weights(tm, "17/20", workers=2)
    N1 = len(tm)
    N = N1 - 1
    Am = np.zeros((N1, 2, 2))
    Rn, Dn, *_ = rigorous_inverse(Wm, Wr, Am, np.zeros_like(Am))
    phi = np.zeros((N1, 2))
    xbox = dict(theta=0.5, a=0.5, b=1.0, x_lo=0.4, x_hi=2.8)
    geo = Geometry(tm, ALPHA, phi, 1.0, 1.0, xbox)
    rho = 1e-6 * np.ones(N1)
    v = cap_vectors(geo, Rn, Dn, rho, 1e-6 * np.ones(N), np.zeros(N), np.zeros(N), np.zeros(N),
                    np.ones(N), np.ones(N), 0.0, 1.0)
    assert np.all(v["T1sup"] < 1e-300) and np.all(v["T1osc"] < 1e-300)
    assert np.all(v["T2sup"] < 1e-9) and np.all(v["Z2sup"] < 1e-300)   # T2: rounding slack of EA only
    assert np.all(v["Ysup"] >= 1e-6) and np.all(v["Ysup"] < 3e-6 * (1 + 1e-9))


def test_mean_kernel_blocks_bound_true_product():
    from msbg.cap import mean_kernel_blocks
    rng = np.random.default_rng(3)
    tm = _mesh(N=20)
    Wm, Wr = rigorous_hat_weights(tm, "17/20", workers=2)
    N1 = len(tm); N = N1 - 1
    Am = rng.normal(size=(N1, 2, 2)) * 0.5
    Rn, Dn, normE, delta, R4 = rigorous_inverse(Wm, Wr, Am, np.zeros_like(Am))
    w = np.zeros((N1, N))
    for n in range(1, N1):
        w[n, :n] = cell_weights(tm, tm[n], ALPHA)[:n]
    Qn, DQn = mean_kernel_blocks(R4, delta, Am, w)
    Abig = np.zeros((2 * N1, 2 * N1))
    for n in range(N1):
        Abig[2 * n:2 * n + 2, 2 * n:2 * n + 2] = Am[n]
    Linv = np.linalg.inv(np.eye(2 * N1) - Abig @ np.kron(Wm, np.eye(2)))
    Q = (Linv @ Abig @ np.kron(w, np.eye(2))).reshape(N1, 2, N, 2)
    assert np.all(Qn >= np.linalg.norm(Q, axis=(1, 3)) - 1e-12)
    assert np.all(DQn >= np.linalg.norm(Q[1:] - Q[:-1], axis=(1, 3)) - 1e-12)
    assert np.abs(Qn - np.linalg.norm(Q, axis=(1, 3))).max() < 1e-8


def test_cell_weights_stable_for_tiny_far_cells():
    import mpmath as mp
    tm = np.array([0.0, 1e-9, 2e-9, 500.0, 1000.0])
    w = cell_weights(tm, 1000.0, ALPHA)
    mp.mp.dps = 40
    a = mp.mpf(17) / 20
    for j in range(4):
        hi, lo = mp.mpf(1000) - mp.mpf(float(tm[j])), mp.mpf(1000) - mp.mpf(float(tm[j + 1]))
        exact = (hi**a - lo**a) / mp.gamma(a + 1)
        assert w[j] >= exact and w[j] <= exact * (1 + mp.mpf(10) ** -11)


def test_bubble_component_is_sharper_and_consistent():
    """beta = theta reproduces the two-component bounds; a smaller beta can only lower T1."""
    rng = np.random.default_rng(5)
    tm = _mesh(N=18)
    Wm, Wr = rigorous_hat_weights(tm, "17/20", workers=2)
    N1 = len(tm); N = N1 - 1
    Am = rng.normal(size=(N1, 2, 2)) * 0.4
    Rn, Dn, *_ = rigorous_inverse(Wm, Wr, Am, np.zeros_like(Am))
    phi = rng.normal(size=(N1, 2))
    geo = Geometry(tm, ALPHA, phi, 1.0, 1.0, dict(theta=0.5, a=0.5, b=1.0, x_lo=0.4, x_hi=2.8))
    normA = np.linalg.norm(Am, axis=(1, 2))[:-1] + 0.1
    args = (geo, Rn, Dn, 1e-6 * np.ones(N1), 1e-6 * np.ones(N), np.zeros(N), normA, 0.01 * np.ones(N))
    om, th = np.ones(N), 0.3 * np.ones(N)
    v2 = cap_vectors(*args, om, th, 1.0, 1.0)
    v3 = cap_vectors(*args, om, th, 1.0, 1.0, beta=th)
    assert np.allclose(v2["T1sup"], v3["T1sup"]) and np.allclose(v2["T1osc"], v3["T1osc"])
    v4 = cap_vectors(*args, om, th, 1.0, 1.0, beta=0.1 * th)
    assert np.all(v4["T1sup"] <= v2["T1sup"] * (1 + 1e-12)) and np.all(v4["T1osc"] <= v2["T1osc"] * (1 + 1e-12))
    assert np.allclose(v4["T2sup"], v2["T2sup"])
    assert np.all(v4["T2bub"] == v4["T2sup"]) and np.all(v4["T1bub"] == 0)


def test_state_sup_dominates_sampled_integral():
    """Omega_n must dominate sup_{C_n} sum_j w_j(t) omega_j for a non-constant omega."""
    from msbg.cap import state_sup
    tm = _mesh(N=30)
    N = len(tm) - 1
    w = np.zeros((N + 1, N))
    for n in range(1, N + 1):
        w[n, :n] = cell_weights(tm, tm[n], ALPHA)[:n]
    omega = np.zeros(N); omega[2] = 1.0; omega[10] = 0.3       # concentrated early: decreasing later
    Om = state_sup(w, omega)
    for n in range(N):
        for t in np.linspace(tm[n], tm[n + 1], 7)[1:]:
            val = float(np.dot(cell_weights(tm, t, ALPHA), omega))
            assert Om[n] >= val * (1 - 1e-12)
    naive = w[1:] @ omega
    assert np.any(naive < Om * (1 - 1e-6))                      # the naive end-point value is smaller


def _frac_int_pl(nodes, vals, t, alpha):
    """I^a f(t) for f piecewise linear on `nodes` (exact hat weights)."""
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scripts.t5_stageA_signaware import hat_row_at
    if t <= 0:
        return np.zeros(vals.shape[1])
    k = np.searchsorted(nodes, t, side="left")
    if nodes[k] == t:
        tt, vv = nodes[: k + 1], vals[: k + 1]
    else:
        lam = (t - nodes[k - 1]) / (nodes[k] - nodes[k - 1])
        tt = np.concatenate([nodes[:k], [t]])
        vv = np.vstack([vals[:k], (1 - lam) * vals[k - 1] + lam * vals[k]])
    return hat_row_at(tt, t, alpha, len(tt) - 1) @ vv


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_cellwise_bounds_dominate_explicit_functions(seed):
    """Empirical validation of the hand-derived bounds (Omega, V, P, T2 = (I-pi)K f, T1 sup/osc):
    explicit f = piecewise-linear + tent bubbles, explicit smooth A(t); every bounded quantity
    is evaluated by exact product integration and must lie below the bound."""
    from msbg.cap import mean_kernel_blocks
    rng = np.random.default_rng(seed)
    a = ALPHA
    N = 14
    tm = 2.5 * (np.arange(N + 1) / N) ** 1.7
    h = np.diff(tm)
    Afun = lambda t: np.array([[-0.4 + 0.3 * np.sin(1.3 * t), 0.8 * np.cos(0.7 * t)],
                               [-0.6 + 0.2 * t / 2.5, 0.1 - 0.5 * np.sin(t)]])
    # f: PL nodal values + tent bubbles
    Fn = rng.normal(size=(N + 1, 2))
    bub = rng.normal(size=(N, 2)) * rng.uniform(0.0, 0.4, size=(N, 1))
    fine = np.sort(np.concatenate([tm, 0.5 * (tm[:-1] + tm[1:])]))
    fvals = np.zeros((2 * N + 1, 2)); gvals = np.zeros((2 * N + 1, 2))
    fvals[0::2] = Fn
    fvals[1::2] = 0.5 * (Fn[:-1] + Fn[1:]) + bub
    gvals[1::2] = bub
    pts = [fvals[2 * n: 2 * n + 3] for n in range(N)]
    omega = np.array([np.linalg.norm(p, axis=1).max() for p in pts])
    theta = np.array([max(np.linalg.norm(p[i] - p[j]) for i in range(3) for j in range(3)) for p in pts])
    beta = np.linalg.norm(bub, axis=1)
    # operator data
    Am = np.array([Afun(t) for t in tm])
    samp = lambda n: np.linspace(tm[n], tm[n + 1], 41)
    normA = np.array([max(np.linalg.norm(Afun(t)) for t in samp(n)) for n in range(N)]) * 1.001
    oscA = np.array([max(np.linalg.norm(Afun(t) - Afun(s)) for t in samp(n)[::4] for s in samp(n)[::4])
                     for n in range(N)]) * 1.05 + 1e-6
    EAt = np.zeros(N)
    for n in range(N):
        for t in samp(n):
            lam = (t - tm[n]) / h[n]
            EAt[n] = max(EAt[n], np.linalg.norm(Afun(t) - (1 - lam) * Am[n] - lam * Am[n + 1]))
    Wm, Wr = rigorous_hat_weights(tm, "17/20", workers=2)
    Rn, Dn, normE, delta, R4 = rigorous_inverse(Wm, Wr, Am, np.zeros_like(Am))
    geo = Geometry(tm, a, np.zeros((N + 1, 2)), 1.0, 1.0, dict(theta=0.5, a=0.5, b=1.0, x_lo=0.4, x_hi=2.8))
    geo.EA = EAt * 1.05 + 1e-6
    geo.Qn, geo.DQn = mean_kernel_blocks(R4, delta, Am, geo.w)
    v = cap_vectors(geo, Rn, Dn, np.zeros(N + 1), np.zeros(N), np.zeros(N), normA, oscA, omega, theta,
                    0.0, 1.0, beta=beta)
    tol = 1 + 1e-9
    # exact quantities
    Inode = np.array([_frac_int_pl(fine, fvals, t, a) for t in tm])
    Knode = np.einsum("nij,nj->ni", Am, Inode)
    for n in range(N):
        for t in samp(n)[1:-1]:
            lam = (t - tm[n]) / h[n]
            It = _frac_int_pl(fine, fvals, t, a)
            assert np.linalg.norm(It) <= v["Omega"][n] * tol
            assert np.linalg.norm(It - Inode[n]) <= v["_V"][n] * tol
            assert np.linalg.norm(It - (1 - lam) * Inode[n] - lam * Inode[n + 1]) <= v["_P"][n] * tol
            Kt = Afun(t) @ It
            assert np.linalg.norm(Kt - (1 - lam) * Knode[n] - lam * Knode[n + 1]) <= v["T2sup"][n] * tol
    # T1: y = L_h^{-1} z,  z_k = A_k I^a[(I - pi) f](t_k)
    z = np.einsum("nij,nj->ni", Am, np.array([_frac_int_pl(fine, gvals, t, a) for t in tm]))
    Abig = np.zeros((2 * (N + 1), 2 * (N + 1)))
    for n in range(N + 1):
        Abig[2 * n:2 * n + 2, 2 * n:2 * n + 2] = Am[n]
    y = np.linalg.solve(np.eye(2 * (N + 1)) - Abig @ np.kron(Wm, np.eye(2)), z.reshape(-1)).reshape(N + 1, 2)
    yn = np.linalg.norm(y, axis=1)
    assert np.all(np.maximum(yn[:-1], yn[1:]) <= v["T1sup"] * tol)
    assert np.all(np.linalg.norm(y[1:] - y[:-1], axis=1) <= v["T1osc"] * tol)
    # the bounds are not vacuous: within a moderate factor somewhere
    assert np.max(np.maximum(yn[:-1], yn[1:]) / v["T1sup"]) > 0.02
