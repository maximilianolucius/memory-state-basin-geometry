"""Soundness regression tests for the rigorous a posteriori enclosure (TASK-0002).

The decisive test is against an EXACT solution: for the linear planar system
^C D^a x = A x with A a scaled rotation, x(t) = E_a(A t^a) x0 is known in closed
form (msbg.mittag_leffler), so the rigorous box must contain it at every cell.
"""
import os
import sys

import mpmath as mp
import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.aposteriori import collocation, graded_mesh                        # noqa: E402
from msbg.mittag_leffler import matrix_e_alpha_scaled_rotation               # noqa: E402
from msbg.models import AlleePredatorPrey, ScaledRotation                    # noqa: E402
from msbg.validated import (bound_recursion_rigorous, certify_entry,         # noqa: E402
                            row_weights_upper, verify_cells)

RHO, THETA_ROT = 1.0, 2.5          # eigenvalues e^{+-2.5 i}: Caputo-stable for alpha < 1.59


def _linear_enclosure(alpha, T, N, grade, K, r, phi_perturb=0.0):
    model = ScaledRotation(rho=RHO, theta=THETA_ROT)
    Amat = model.A
    p = np.array([1.0, -0.5])
    tm = graded_mesh(T, N, grade)
    X, PHI, M = collocation(model, p, alpha, tm)
    if phi_perturb:
        rng = np.random.default_rng(0)
        PHI = PHI + phi_perturb * rng.standard_normal(PHI.shape)
    cells = verify_cells(tm, PHI, Amat[0, 0], Amat[0, 1], Amat[1, 0], Amat[1, 1], alpha, p, r,
                         prec=128, workers=4, K=K, kind="linear2")
    W = row_weights_upper(tm, alpha, workers=4)
    U, D, kap = bound_recursion_rigorous(tm, alpha, cells.R, cells.L, W)
    return model, p, tm, cells, U


def _exact(alpha, t, p):
    E = matrix_e_alpha_scaled_rotation(alpha, RHO, THETA_ROT, t, dps=30)
    Em = np.array([[float(E[0, 0]), float(E[0, 1])], [float(E[1, 0]), float(E[1, 1])]])
    return Em @ p


@pytest.mark.parametrize("alpha", [0.6, 0.85])
def test_rigorous_box_contains_exact_mittag_leffler_solution(alpha):
    T, N = 3.0, 120
    model, p, tm, cells, U = _linear_enclosure(alpha, T, N, grade=3.0, K=16, r=0.5)
    assert np.isfinite(U).all() and U.max() < 0.5, "bootstrap must pass on this easy problem"
    for n in range(0, N, 7):
        for t in (tm[n], 0.5 * (tm[n] + tm[n + 1]), tm[n + 1]):
            ex = _exact(alpha, t, p)
            assert cells.x_lo[n] - U[n] <= ex[0] <= cells.x_hi[n] + U[n]
            assert cells.y_lo[n] - U[n] <= ex[1] <= cells.y_hi[n] + U[n]


def test_enclosure_stays_valid_for_a_deliberately_bad_phi():
    """A poor untrusted phi must widen the enclosure, never break it."""
    alpha, T, N = 0.7, 2.0, 80
    model, p, tm, cells, U = _linear_enclosure(alpha, T, N, grade=3.0, K=16, r=5.0,
                                               phi_perturb=1e-3)
    assert np.isfinite(U).all()
    for n in range(0, N, 5):
        t = 0.5 * (tm[n] + tm[n + 1])
        ex = _exact(alpha, t, p)
        assert cells.x_lo[n] - U[n] <= ex[0] <= cells.x_hi[n] + U[n]
        assert cells.y_lo[n] - U[n] <= ex[1] <= cells.y_hi[n] + U[n]


def test_bound_decreases_with_mesh_refinement():
    alpha, T = 0.75, 2.0
    Ue = []
    for N in (40, 80, 160):
        _, _, _, _, U = _linear_enclosure(alpha, T, N, grade=3.0, K=16, r=1.0)
        Ue.append(U[-1])
    assert Ue[0] > Ue[1] > Ue[2]


def test_undecided_when_tube_is_too_small():
    """A tube radius smaller than the achievable bound must fail the bootstrap."""
    alpha, T, N = 0.85, 2.0, 30
    _, _, _, _, U = _linear_enclosure(alpha, T, N, grade=3.0, K=4, r=1e-9)
    assert (not np.isfinite(U).all()) or U.max() >= 1e-9


def test_cell_boxes_contain_nodal_values_allee():
    theta, a, b, m, al = 0.3, 1.0, 1.0, 0.8, 0.85
    p = np.array([2.4372, 2.012])
    model = AlleePredatorPrey(theta=theta, a=a, b=b, m=m)
    tm = graded_mesh(2.0, 60, 3.0)
    X, PHI, M = collocation(model, p, al, tm)
    cells = verify_cells(tm, PHI, theta, a, b, m, al, p, 0.05, workers=4, K=8)
    for n in range(60):
        assert cells.x_lo[n] <= X[n, 0] <= cells.x_hi[n]
        assert cells.y_lo[n] <= X[n, 1] <= cells.y_hi[n]
        assert cells.R[n] >= 0.0 and np.isfinite(cells.R[n])


def test_certify_entry_reports_undecided_on_infinite_bound():
    tm = np.linspace(0, 1, 4)

    class C:
        x_lo = np.array([0.1, 0.1, 0.1]); x_hi = np.array([0.2, 0.2, 0.2])
        y_lo = np.array([0.1, 0.1, 0.1]); y_hi = np.array([0.2, 0.2, 0.2])

    out = certify_entry(0.3, C, np.array([np.inf, np.inf, np.inf]), tm)
    assert not out["certified"].any()
