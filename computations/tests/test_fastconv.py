"""Cross-validation of the blocked history convolution against the O(N^2) reference.

TASK-0002 Stage E requires any fast convolution to be cross-validated against the
existing solvers.  The blocked solver changes only the floating-point summation
order, so agreement must be at the rounding level.
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.fastconv import solve_blocked                                # noqa: E402
from msbg.mittag_leffler import e_alpha                                # noqa: E402
from msbg.models import AlleePredatorPrey, LinearScalar, ScaledRotation  # noqa: E402
from msbg.solvers import solve                                         # noqa: E402


@pytest.mark.parametrize("method", ["pi_rect", "pece"])
@pytest.mark.parametrize("block", [1, 7, 64, 5000])
def test_blocked_equals_reference_nonlinear(method, block):
    model = AlleePredatorPrey(theta=0.3, a=1.0, b=1.0, m=0.8)
    rng = np.random.default_rng(3)
    X0 = np.column_stack([rng.uniform(0.35, 2.5, 50), rng.uniform(0.05, 3.0, 50)])
    ref = solve(model, X0, 0.85, 0.02, 1500, method=method, store=True, store_stride=5)
    fast = solve_blocked(model, X0, 0.85, 0.02, 1500, method=method, block=block,
                         store=True, store_stride=5)
    rel = np.max(np.abs(ref.x - fast.x) / np.maximum(1.0, np.abs(ref.x)))
    assert rel < 1e-11


@pytest.mark.parametrize("method", ["pi_rect", "pece"])
def test_blocked_against_exact_mittag_leffler(method):
    alpha, T, N = 0.6, 2.0, 2000
    exact = float(e_alpha(alpha, -1.0 * T**alpha, dps=25))
    r = solve_blocked(LinearScalar(lam=-1.0), [[1.0]], alpha, T / N, N, method=method,
                      block=128, store=False)
    tol = {"pi_rect": 1e-4, "pece": 1e-6}[method]
    assert abs(float(r.x_final[0, 0]) - exact) < tol


def test_blocked_planar_rotation_matches_reference():
    model = ScaledRotation(rho=1.0, theta=2.5)
    X0 = np.array([[1.0, 0.0], [0.0, 1.0], [0.3, -0.7]])
    ref = solve(model, X0, 0.75, 0.005, 1200, method="pece", store=False).x_final
    fast = solve_blocked(model, X0, 0.75, 0.005, 1200, method="pece", block=100,
                         store=False).x_final
    assert np.max(np.abs(ref - fast)) < 1e-12
