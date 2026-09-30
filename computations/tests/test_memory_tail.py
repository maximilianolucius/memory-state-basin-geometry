"""Regression tests for the TASK-0004 memory-tail tools and rigorous kernel bounds."""
import os
import sys

import mpmath as mp
import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg import kernel_bound as kb                                              # noqa: E402
from msbg.memory_tail import inherited_input, linear_volterra, ml2, psi_scalar   # noqa: E402
from msbg.mittag_leffler import e_alpha                                          # noqa: E402
from msbg.models import AlleePredatorPrey                                        # noqa: E402
from msbg.solvers import solve                                                   # noqa: E402
from msbg.validated_res import Setup, _l2_upper, adapted_C, kernel_integrator    # noqa: E402

W1 = ("17/20", "-3/25", "41/625")
LAM = mp.mpc(-3, mp.sqrt(41)) / 25


def test_ml2_reduces_to_known_functions():
    assert abs(ml2(0.85, 1, -2.3) - e_alpha(0.85, -2.3, dps=25)) < mp.mpf("1e-20")
    assert abs(ml2(1, 1, mp.mpc(1, 2)) - mp.e ** mp.mpc(1, 2)) < mp.mpf("1e-12")


def test_linear_volterra_against_exact_mittag_leffler():
    J = np.array([[-1.0]])
    n, H = 400, 0.01
    z = linear_volterra(np.ones((n + 1, 1)), np.zeros((n + 1, 1)), J, 0.85, H)
    assert abs(z[-1, 0] - float(e_alpha(0.85, -(n * H) ** 0.85, dps=20))) < 1e-5


def test_inherited_input_at_T_equals_the_state():
    """h_T(T) = x(T) - E*: the split of the Volterra integral at T is exact."""
    model = AlleePredatorPrey(theta=0.3, a=1.0, b=1.0, m=0.8)
    p, E = np.array([1.2, 0.3]), np.array([0.8, 0.1])
    r = solve(model, p[None, :], 0.85, 0.005, 4000, method="pece", store=True)
    x, t = r.x[:, 0, :], r.t
    hT = inherited_input(t, model.g(x), p - E, 0.85, 4000, t[-1:])
    assert np.max(np.abs(hT[0] - (x[-1] - E))) < 5e-5


@pytest.mark.parametrize("rho", [2, 10, 40])
def test_integral_representation_matches_the_series(rho):
    rep, pole, I = kb.representation_value(0.85, LAM * rho)
    assert abs(rep - ml2(0.85, 0.85, LAM * rho, dps=25)) < mp.mpf("1e-18")
    C = kb.exact_constants(W1, 128)
    assert float(abs(I)) * float(abs(LAM * rho)) ** 2 <= float(C["B"].lower())


def test_envelope_cells_are_upper_bounds_and_tight():
    kb._init(W1)
    for cell in ((0.0, 2.5e-4), (3.0, 3.006), (40.0, 40.08)):
        sup, val = kb._cell(cell)
        for rho in np.linspace(cell[0], cell[1], 5):
            true = float(abs(ml2(0.85, 0.85, LAM * float(rho), dps=20)))
            assert true <= sup
        assert sup / val < 1.02


def test_constants_are_rebuilt_at_working_precision():
    """The first version reused 128-bit constants at 400 bits and returned K ~ 1e33."""
    lo = kb.exact_constants(W1, 128)["a"]
    hi = kb.exact_constants(W1, 600)["a"]
    assert float(hi.rad()) < float(lo.rad()) * 1e-100


def test_kernel_integrator_bounds_the_true_integral():
    st = Setup("1/2", "1/2", "1", "4/5", "17/20", ("277/100", "467/1000"))
    ker = kernel_integrator(st, 12.0, workers=4)
    lam = mp.mpc(float(st.mu.p) / float(st.mu.q), mp.sqrt(mp.mpf(int(st.nu2.p)) / int(st.nu2.q)))
    for a, b in ((0.5, 1.5), (3.0, 10.0)):
        true = float(mp.quad(lambda s: abs(psi_scalar(0.85, lam, s, dps=15)), [a, b]))
        bound = float(ker.integral(a, b))
        assert true <= bound <= 1.01 * true


def test_kernel_total_respects_the_exact_lower_bound():
    """int_0^inf Psi = -J^{-1}, so K >= 1/|lambda| whatever the numerics say."""
    st = Setup("1/2", "1/2", "1", "4/5", "17/20", ("277/100", "467/1000"))
    ker = kernel_integrator(st, 12.0, workers=4)
    assert ker.total_upper(st) >= float((1 / st.C["xl"]).upper())


def test_l2_upper_handles_balls_containing_zero():
    from flint import arb
    v = _l2_upper([arb(0, 1e-3), arb(0, 2e-3)])
    assert np.isfinite(v) and v >= np.hypot(1e-3, 2e-3)


def test_adapted_nonlinearity_constant_is_an_upper_bound():
    st = Setup("1/2", "1/2", "1", "4/5", "17/20", ("277/100", "467/1000"))
    C0, c3 = adapted_C(st, n_arcs=720)
    S = np.array([[-0.4, 0.0], [0.04, -np.sqrt(29) / 25]])
    Si = np.linalg.inv(S)
    rng = np.random.default_rng(5)
    for _ in range(200):
        xi = rng.standard_normal(2)
        xi *= rng.uniform(0.0, 0.2) / np.linalg.norm(xi)
        u = S @ xi
        N = np.array([-0.9 * u[0] ** 2 - 0.5 * u[0] * u[1] - u[0] ** 3, u[0] * u[1]])
        r = np.linalg.norm(xi)
        assert np.linalg.norm(Si @ N) <= (C0 + c3 * 0.2) * r * r * (1 + 1e-12)
