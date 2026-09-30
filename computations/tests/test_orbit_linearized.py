"""Regression tests for the discrete orbit-linearized operator (TASK-0005)."""
import os
import sys
from math import gamma

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.mittag_leffler import e_alpha                     # noqa: E402
from msbg.orbit_linearized import OrbitLinearized, hat_weights  # noqa: E402
from scripts.t5_stageD_radii_pilot import dense_inverse     # noqa: E402

AL = 0.85
TM = np.concatenate([[0.0], np.geomspace(1e-4, 2.0, 200)])


def test_hat_weights_integrate_piecewise_linear_functions_exactly():
    W = hat_weights(TM, AL)
    for f, exact in ((TM, TM ** (AL + 1) / gamma(AL + 2)),
                     (np.ones_like(TM), TM**AL / gamma(AL + 1))):
        got = W @ f
        assert np.max(np.abs(got[1:] - exact[1:]) / exact[1:]) < 1e-12


def test_inverse_reproduces_scalar_mittag_leffler():
    A = np.tile(-np.eye(2), (len(TM), 1, 1))
    L = OrbitLinearized(TM, A, AL)
    e = L.solve(np.ones((len(TM), 2)))
    assert abs(e[-1, 0] - float(e_alpha(AL, -2.0**AL, dps=20))) < 1e-4


def test_adjoint_identity():
    rng = np.random.default_rng(1)
    A = 0.3 * rng.standard_normal((len(TM), 2, 2))
    L = OrbitLinearized(TM, A, AL)
    d, f = rng.standard_normal((len(TM), 2)), rng.standard_normal((len(TM), 2))
    assert abs(np.sum(L.solve(d) * f) - np.sum(d * L.solve_T(f))) < 1e-9 * abs(np.sum(d * f) + 1)


def test_dense_inverse_matches_forward_solve_and_row_norms():
    rng = np.random.default_rng(2)
    tm = np.concatenate([[0.0], np.geomspace(1e-3, 3.0, 60)])
    A = 0.5 * rng.standard_normal((len(tm), 2, 2))
    L = OrbitLinearized(tm, A, AL)
    R = dense_inverse(L.W, L.A)
    d = rng.standard_normal((len(tm), 2))
    e = np.einsum("nikl,kl->ni", R, d)
    assert np.max(np.abs(e - L.solve(d))) < 1e-10
    n = 40
    rn = L.row_block_norms(n)
    assert np.max(np.abs(rn - np.linalg.norm(R[n], ord=2, axis=(0, 2)))) < 1e-10


def test_similarity_transform_changes_norms_not_solutions():
    rng = np.random.default_rng(3)
    tm = np.concatenate([[0.0], np.geomspace(1e-3, 3.0, 80)])
    A = 0.5 * rng.standard_normal((len(tm), 2, 2))
    S = np.array([[1.0, 0.3], [-0.2, 0.7]])
    L0 = OrbitLinearized(tm, A, AL)
    L1 = OrbitLinearized(tm, A, AL, S=S)
    d = rng.standard_normal((len(tm), 2))
    e0 = L0.solve(d)
    e1 = L1.solve(d @ np.linalg.inv(S).T)
    assert np.max(np.abs(e1 - e0 @ np.linalg.inv(S).T)) < 1e-10
