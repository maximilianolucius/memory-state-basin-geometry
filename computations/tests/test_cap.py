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
