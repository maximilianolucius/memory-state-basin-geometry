"""Regression tests for the three history-retaining Caputo solvers."""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.mittag_leffler import e_alpha, matrix_e_alpha_scaled_rotation  # noqa: E402
from msbg.models import AlleePredatorPrey, LinearScalar, ScaledRotation  # noqa: E402
from msbg.solvers import METHODS, solve, solve_mp                        # noqa: E402

# reference accuracies at T=2, N=2000 against the exact E_alpha solution, and
# the convergence order observed on 2026-09-29 (ORION/R11, see
# data/stage_a_A2_scalar_linear.json).  Tolerances are deliberately loose enough
# to be platform independent but tight enough to catch a broken weight vector.
EXPECTED = {
    "pi_rect": dict(tol=2e-4, order=(0.85, 1.15)),
    "pece":    dict(tol=5e-6, order=(1.30, 1.75)),
    "l1":      dict(tol=5e-4, order=(0.85, 1.25)),
}


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("alpha", [0.4, 0.6, 0.85])
def test_scalar_linear_against_exact_mittag_leffler(method, alpha):
    T, N = 2.0, 2000
    exact = float(e_alpha(alpha, -1.0 * T**alpha, dps=25))
    r = solve(LinearScalar(lam=-1.0), [[1.0]], alpha, T / N, N, method=method, store=False)
    assert abs(float(r.x_final[0, 0]) - exact) < EXPECTED[method]["tol"]


@pytest.mark.parametrize("method", METHODS)
def test_observed_convergence_order(method):
    T, alpha = 2.0, 0.6
    exact = float(e_alpha(alpha, -1.0 * T**alpha, dps=25))
    hs, errs = [], []
    for N in (500, 1000, 2000, 4000):
        r = solve(LinearScalar(lam=-1.0), [[1.0]], alpha, T / N, N, method=method, store=False)
        hs.append(T / N)
        errs.append(abs(float(r.x_final[0, 0]) - exact))
    A = np.vstack([np.log(hs), np.ones(len(hs))]).T
    order = float(np.linalg.lstsq(A, np.log(errs), rcond=None)[0][0])
    lo, hi = EXPECTED[method]["order"]
    assert lo <= order <= hi, f"{method} observed order {order}"


@pytest.mark.parametrize("method", METHODS)
def test_planar_linear_against_exact_matrix_mittag_leffler(method):
    alpha, rho, theta, T, N = 0.5, 1.0, 0.9734093253645294, 3.0, 4000
    E = matrix_e_alpha_scaled_rotation(alpha, rho, theta, T, dps=25)
    Ex = np.array([[float(E[0, 0]), float(E[0, 1])], [float(E[1, 0]), float(E[1, 1])]])
    X0 = np.array([[1.0, 0.0], [0.37, -0.91]])
    r = solve(ScaledRotation(rho=rho, theta=theta), X0, alpha, T / N, N, method=method, store=False)
    assert np.max(np.abs(r.x_final - X0 @ Ex.T)) < 5e-3


@pytest.mark.parametrize("method", METHODS)
def test_determinism_bitwise(method):
    X0 = np.array([[0.9, 1.3], [0.35, 0.4]])
    a = solve(AlleePredatorPrey(), X0, 0.6, 0.05, 800, method=method, store=False).x_final
    b = solve(AlleePredatorPrey(), X0, 0.6, 0.05, 800, method=method, store=False).x_final
    assert np.array_equal(a, b)


def test_batched_equals_single():
    """A batch must give exactly what each initial condition gives alone."""
    X0 = np.array([[0.9, 1.3], [0.35, 0.4], [1.2, 0.2]])
    for method in METHODS:
        batch = solve(AlleePredatorPrey(), X0, 0.6, 0.05, 400, method=method, store=False).x_final
        for i in range(len(X0)):
            one = solve(AlleePredatorPrey(), X0[i:i + 1], 0.6, 0.05, 400, method=method,
                        store=False).x_final
            assert np.max(np.abs(batch[i] - one[0])) < 1e-12


def test_mp_solver_agrees_with_float_solver():
    import mpmath as mp

    model = LinearScalar(lam=-1.0)
    alpha, N, T = 0.6, 200, 1.0
    f = solve(model, [[1.0]], alpha, T / N, N, method="pece", store=False).x_final[0, 0]
    m = solve_mp(model.g_mp, [1.0], alpha, mp.mpf(T) / N, N, dps=25, method="pece")[-1][0]
    assert abs(float(m) - float(f)) < 1e-10


def test_positive_cone_is_respected_on_tested_trajectories():
    X0 = np.array([[0.5, 0.3], [0.25, 1.1], [1.1, 0.6]])
    for method in METHODS:
        r = solve(AlleePredatorPrey(), X0, 0.6, 0.05, 2000, method=method, store=True,
                  store_stride=10)
        assert np.nanmin(r.x) > -1e-9
