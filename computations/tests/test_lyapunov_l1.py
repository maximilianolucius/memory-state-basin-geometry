"""Regression tests for the exact-rational L1 certificate (TASK-0003)."""
import os
import sys

import pytest
from flint import fmpq, fmpq_mat

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.lyapunov_l1 import Q, l1_certificate        # noqa: E402
from msbg.validated import to_arb, to_float           # noqa: E402


def test_rational_parser():
    assert Q("17/20") == fmpq(17, 20)
    assert Q("0.85") == fmpq(17, 20)
    assert Q("2.4372") == fmpq(6093, 2500)
    assert Q("-0.5") == fmpq(-1, 2)
    assert Q(3) == fmpq(3)


def test_exact_equilibrium_and_jacobian_of_the_task0001_set():
    c = l1_certificate("3/10", "1", "1", "4/5")
    assert (c.x_star, c.y_star) == (fmpq(4, 5), fmpq(1, 10))
    assert c.trace == fmpq(-6, 25) and c.det == fmpq(2, 25)
    assert c.hurwitz
    assert c.P == [[fmpq(75, 32), fmpq(5, 8)], [fmpq(5, 8), fmpq(81, 4)]]


def test_lyapunov_equation_is_solved_exactly():
    for par in (("3/10", "1", "1", "4/5"), ("7/10", "1/4", "2", "91/50"), ("1/2", "2", "1/2", "9/20")):
        c = l1_certificate(*par)
        assert c.hurwitz
        J = fmpq_mat(2, 2, [c.J[0][0], c.J[0][1], c.J[1][0], c.J[1][1]])
        P = fmpq_mat(2, 2, [c.P[0][0], c.P[0][1], c.P[1][0], c.P[1][1]])
        R = J.transpose() * P + P * J
        assert [R[0, 0], R[0, 1], R[1, 0], R[1, 1]] == [-1, 0, 0, -1]


def test_l1_inequality_is_verified_not_assumed():
    c = l1_certificate("3/5", "1/4", "1", "22/25")
    assert c.lhs.upper() <= 0.5
    assert c.lam_min.lower() > 0
    assert c.lam_max.lower() >= c.lam_min.upper()


def test_non_hurwitz_set_is_refused():
    c = l1_certificate("1/5", "1", "1", "2/5")     # the B2/B3 regime: trace > 0
    assert not c.hurwitz and c.P is None


def test_omega_never_reaches_the_extinction_strip():
    """Consistency of L1 with the proved THEOREM X1: Omega must avoid {x < theta}."""
    for th in ("1/10", "1/2", "9/10"):
        for f in ("11/20", "4/5"):
            for a in ("1/4", "4"):
                thq = Q(th)
                xs = thq + Q(f) * (1 - thq)
                c = l1_certificate(th, a, "1", xs)
                assert c.hurwitz and c.omega_avoids_strip
                assert c.ratio_extent_gap < 0.1


def test_membership_test_is_strict_and_correct():
    c = l1_certificate("3/10", "1", "1", "4/5")
    assert c.contains("4/5", "1/10")                       # the equilibrium itself
    assert not c.contains("6093/2500", "503/250")          # the TASK-0001 witness is far outside
    assert not c.contains("3/10", "1/10")                  # a point on the threshold


def test_exact_rational_inputs_differ_from_binary64():
    """alpha = 17/20 is not the double 0.85; the verifier must be able to tell."""
    a_exact = to_arb("17/20")
    a_float = to_arb(0.85)
    assert not a_exact.overlaps(a_float)
    assert abs(to_float("17/20") - 0.85) == 0.0
