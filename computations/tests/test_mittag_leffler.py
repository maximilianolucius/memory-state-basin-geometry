"""Regression tests for the Mittag-Leffler implementation."""
import os
import sys

import mpmath as mp
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.mittag_leffler import (  # noqa: E402
    e_alpha,
    e_alpha_closed_form,
    e_alpha_zero,
    matrix_e_alpha_scaled_rotation,
)


@pytest.mark.parametrize(
    "alpha,z",
    [(1.0, -5.0), (1.0, 3.0), (1.0, 1 + 1j),
     (0.5, -8.0), (0.5, 1.3), (0.5, 1 + 1j),
     (2.0, -3.0), (2.0, 1.7)],
)
def test_taylor_matches_closed_form(alpha, z):
    a = e_alpha(alpha, z, dps=25, route="taylor")
    b = e_alpha_closed_form(alpha, z, dps=25)
    assert abs(a - b) < mp.mpf(10) ** -20


@pytest.mark.parametrize("alpha", [0.3, 0.5, 0.6, 0.8])
@pytest.mark.parametrize("x", [0.5, 1.0, 5.0, 12.5])
def test_two_routes_agree(alpha, x):
    """Taylor and Stieltjes must agree wherever both are affordable.

    The Taylor route costs O(|z|^{1/alpha}) guard digits, so for small alpha the
    larger arguments are out of budget and are skipped rather than compared
    against a deliberately crippled evaluation.
    """
    if x ** (1.0 / alpha) > 400.0:
        pytest.skip(f"Taylor route out of budget for alpha={alpha}, x={x}")
    t = e_alpha(alpha, -x, dps=25, route="taylor")
    s = e_alpha(alpha, -x, dps=25, route="stieltjes")
    assert abs(t - s) < mp.mpf(10) ** -20


@pytest.mark.parametrize("alpha", [0.3, 0.5, 0.8])
@pytest.mark.parametrize("x", [1e-25, 1e-10])
def test_stieltjes_route_reproduces_E_alpha_of_zero(alpha, x):
    """E_alpha(0) = 1 is the exact normalisation of the branch-cut integral."""
    assert abs(e_alpha(alpha, -x, dps=25, route="stieltjes") - 1) < mp.mpf("1e-9")


@pytest.mark.parametrize("x", [50.0, 1e4, 1e8])
def test_stieltjes_matches_closed_form_far_out(x):
    s = e_alpha(0.5, -x, dps=25, route="stieltjes")
    c = e_alpha_closed_form(0.5, -x, dps=25)
    assert abs(s - c) / abs(c) < mp.mpf("1e-20")


def test_taylor_route_refuses_unaffordable_arguments():
    """The series must refuse rather than silently run for minutes."""
    with pytest.raises(ValueError):
        e_alpha(0.2, -50.0, dps=25, route="taylor")


@pytest.mark.parametrize("alpha", [0.4, 0.6, 0.85])
def test_large_argument_asymptote(alpha):
    """E_alpha(-x) ~ 1/(x Gamma(1-alpha)) as x -> infinity."""
    x = mp.mpf(10) ** 7
    s = e_alpha(alpha, -x, dps=25, route="stieltjes")
    asy = 1 / (x * mp.gamma(1 - mp.mpf(alpha)))
    assert abs(s / asy - 1) < mp.mpf("1e-5")


def test_value_at_zero():
    for alpha in (0.25, 0.5, 0.75, 0.99):
        assert abs(e_alpha(alpha, 0, dps=25) - 1) < mp.mpf(10) ** -22


def test_matrix_form_is_rotation_like():
    E = matrix_e_alpha_scaled_rotation(0.5, 1.0, 0.7, 1.3, dps=25)
    assert abs(E[0, 0] - E[1, 1]) < mp.mpf(10) ** -22
    assert abs(E[0, 1] + E[1, 0]) < mp.mpf(10) ** -22


def test_known_zero_of_E_half():
    """The first non-real zero of E_1/2, located two independent ways."""
    mp.mp.dps = 40
    w = mp.findroot(mp.erfc, mp.mpc("-1.35", "1.99"))
    z_closed = -w
    z_own = e_alpha_zero(0.5, mp.mpc("1.3548", "-1.9915"), dps=30)
    assert abs(z_closed - z_own) < mp.mpf("1e-25")
    assert abs(e_alpha(0.5, z_own, dps=30)) < mp.mpf("1e-25")
