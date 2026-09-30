"""Tests for msbg.rig (TASK-0007 verified arithmetic layer)."""
from fractions import Fraction

import numpy as np
import pytest

flint = pytest.importorskip("flint")

from msbg.rig import (U, arb_hi, arb_lo, arb_norm2_hi, defl, gam, geometry_tables, infl,   # noqa: E402
                      interpolation_constants_arb, lipschitz_A_cells_arb)


def test_arb_hi_lo_bracket_exact_rationals():
    from flint import arb
    for num, den in ((1, 3), (2, 3), (17, 20), (1, 10), (355, 113), (1, 7)):
        x = arb(num) / arb(den)
        hi, lo = arb_hi(x), arb_lo(x)
        assert Fraction(lo) <= Fraction(num, den) <= Fraction(hi)
        assert Fraction(hi) - Fraction(lo) <= Fraction(4 * abs(num), den) * Fraction(2) ** -52
    with pytest.raises(ValueError):
        arb_hi(arb(0) ** arb(-1))  # non-finite


def test_infl_dominates_exact_sums_any_order():
    rng = np.random.default_rng(0)
    for n in (3, 100, 12000):
        x = rng.random(n) * 10.0 ** rng.integers(-8, 8, n)
        y = rng.random(n)
        exact = sum(Fraction(float(a)) * Fraction(float(b)) for a, b in zip(x, y))
        for order in (slice(None), slice(None, None, -1)):
            s = float(np.dot(x[order], y[order]))
            assert Fraction(float(infl(s, n))) >= exact
            assert Fraction(float(defl(s, n))) <= exact
    assert gam(12000) > 12000 * U


def test_arb_norm2_hi():
    from flint import arb
    v = [arb(3) / 7, arb(-4) / 7]
    assert arb_norm2_hi(v) >= 5 / 7 and arb_norm2_hi(v) < 5 / 7 * (1 + 1e-12)


def test_geometry_tables_enclose_mpmath():
    import mpmath as mp
    mp.mp.dps = 40
    a = mp.mpf(17) / 20
    N = 25
    tm = 4.0 * (np.arange(N + 1) / N) ** 2
    phi = np.column_stack([np.sin(tm), np.cos(2 * tm)])
    T = geometry_tables(tm, phi, "17/20", workers=2)
    G1, Ga = mp.gamma(a + 1), mp.gamma(a)
    for n in range(1, N + 1):
        for j in range(n):
            w = ((mp.mpf(tm[n]) - mp.mpf(tm[j])) ** a - (mp.mpf(tm[n]) - mp.mpf(tm[j + 1])) ** a) / G1
            assert T["W_lo"][n, j] <= w <= T["W_hi"][n, j]
            if j <= n - 2:
                d = (mp.mpf(tm[n]) - mp.mpf(tm[j + 1])) ** (a - 2) - (mp.mpf(tm[n]) - mp.mpf(tm[j])) ** (a - 2)
                if n < N:
                    assert T["D"][n, j] >= d
                alt = (mp.mpf(tm[j + 1]) - mp.mpf(tm[j])) / 2 * ((mp.mpf(tm[n]) - mp.mpf(tm[j + 1])) ** (a - 1)
                                                                  - (mp.mpf(tm[n]) - mp.mpf(tm[j])) ** (a - 1)) / Ga
                assert T["REM"][n, j] >= min(2 * w, alt)
    for n in range(N):
        h = mp.mpf(tm[n + 1]) - mp.mpf(tm[n])
        assert T["HA"][n] >= h ** a / G1
        assert T["DTA"][n] >= (mp.mpf(tm[n + 1]) ** a - mp.mpf(tm[n]) ** a) / G1
        assert T["GREEN"][n] >= h * h / 8 * (1 - a) / Ga
    # dw >= w_{n,j} - w_{n+1,j} >= 0
    assert np.all(T["DW"] >= 0)
    # osc(xhat') table dominates a sampled oscillation of the exact xhat'
    from msbg.aposteriori import xhat_prime_eval
    m = (phi[1:] - phi[:-1]) / np.diff(tm)[:, None]
    for n in (3, 12, 24):
        ts = np.linspace(tm[n], tm[n + 1], 41)
        xp = xhat_prime_eval(ts, tm, phi[0], m, 0.85)
        osc = max(np.linalg.norm(xp[i] - xp[j]) for i in range(0, 41, 5) for j in range(0, 41, 5))
        assert T["O1"][n] >= osc * (1 - 1e-9)
        assert T["X1"][n] >= np.linalg.norm(xp, axis=1).max() * (1 - 1e-9)


def test_interpolation_constants_arb_dominate_samples():
    a = 0.85
    ca, cl, cp = interpolation_constants_arb("17/20", [1.0, 0.5, 2.0])
    tau = np.linspace(0, 1, 100001)
    assert ca >= np.max(tau**a - tau)
    assert cl >= np.max(tau**a - tau + 2 * tau * (1 - tau) ** a)
    for r, c in zip([1.0, 0.5, 2.0], cp):
        d = (1 - tau) * r**a + tau * ((1 + r) ** a - 1) - (tau + r) ** a + tau**a
        assert c >= d.max()


def test_lipschitz_arb_dominates_sampled_directions():
    from msbg.validated_res import Setup
    st = Setup("1/2", "1/2", "1", "4/5", "17/20", ("277/100", "467/1000"))
    S = np.array([[float(v.mid()) for v in row] for row in st.S_arb])
    Si = np.linalg.inv(S)
    th, a, b = 0.5, 0.5, 1.0
    x_lo = np.array([0.469, 0.79]); x_hi = np.array([2.77, 0.81])
    D2 = lipschitz_A_cells_arb(st, x_lo, x_hi, 1e-3)
    ang = np.linspace(0, 2 * np.pi, 2001)
    for n in range(2):
        for xs in np.linspace(x_lo[n] - 1e-3, x_hi[n] + 1e-3, 7):
            c = -6 * xs + 2 * (1 + th)
            for t in ang:
                u = np.array([np.cos(t), np.sin(t)])
                e = S @ u
                H = np.array([[c * e[0] - a * e[1], -a * e[0]], [b * e[1], b * e[0]]])
                assert np.linalg.norm(Si @ H @ S) <= D2[n] * (1 + 1e-12)


def test_infl_factor_is_valid_and_tiny_handling():
    from fractions import Fraction
    from msbg.rig import _factor_up
    for n in (1, 2, 4, 1000, 24002, 36516):
        f = Fraction(float(_factor_up(n)))
        u = Fraction(1, 2**53)
        g = n * u / (1 - n * u)
        assert f >= 1 + 2 * g + 3 * u
        # fl(x f) >= x f (1 - u) >= x (1 + 2 g)
        assert f * (1 - u) >= 1 + 2 * g
    x = np.array([0.0, 1e-300, 2.0**-1000, 1.0])
    y = infl(x, 3)
    assert y[0] == 0.0 and y[1] >= 1e-300 and y[2] >= 2.0**-1000 and y[3] > 1.0
    z = defl(x, 3)
    assert z[0] == 0.0 and z[2] == 0.0 and z[3] < 1.0
