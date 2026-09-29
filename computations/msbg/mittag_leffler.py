r"""Arbitrary-precision Mittag-Leffler function.

E_alpha(z) = sum_{k>=0} z^k / Gamma(alpha k + 1),  0 < alpha <= 1 (also alpha = 2 for tests).

Two independent evaluation routes are implemented so that they can be
cross-checked against each other and against closed forms:

route T ("taylor")
    adaptive-precision truncated Taylor series with an explicit tail bound.
    Valid for every z; cost grows like |z|^(1/alpha), so it is used for
    moderate |z|.

route S ("stieltjes")
    for z = -x with x > 0 and 0 < alpha < 1, the branch-cut (Stieltjes)
    representation obtained by collapsing the Bromwich contour of
    p^(alpha-1)/(p^alpha + lambda):

        E_alpha(-lambda t^alpha)
          = (lambda sin(alpha pi)/pi)
            int_0^inf e^{-r t} r^{alpha-1}
                      / (r^{2 alpha} + 2 lambda r^alpha cos(alpha pi) + lambda^2) dr

    With t = 1 and lambda = x this evaluates E_alpha(-x) directly.  The
    integrand is positive and exponentially damped, so mpmath.quad is
    accurate and cheap for arbitrarily large x.  Verified at x -> 0 by the
    exact value 1 (see tests).

Closed forms used as independent ground truth in the test-suite:
    E_1(z)    = exp(z)
    E_{1/2}(z)= exp(z^2) erfc(-z)
    E_2(z)    = cosh(sqrt(z))
"""
from __future__ import annotations

import math

import mpmath as mp

__all__ = [
    "e_alpha",
    "e_alpha_closed_form",
    "e_alpha_series_dps_estimate",
    "matrix_e_alpha_scaled_rotation",
    "e_alpha_zero",
]


def e_alpha_series_dps_estimate(alpha: float, absz: float, dps: int) -> int:
    """Working precision needed so that the Taylor route delivers ``dps`` digits.

    The largest term of the series has magnitude ~ exp(|z|^(1/alpha)); working
    precision must absorb that cancellation.
    """
    if absz <= 0:
        return dps + 10
    growth = absz ** (1.0 / alpha)
    guard = int(math.ceil(growth / math.log(10.0))) + 20
    return dps + guard


#: the Taylor route costs O(|z|^{1/alpha}) guard digits; beyond this budget the
#: series is refused rather than silently running for minutes (see :func:`e_alpha`).
TAYLOR_GUARD_BUDGET_DIGITS = 4000


def _e_alpha_taylor(alpha, z, dps: int):
    """Truncated Taylor series with a rigorous-in-exact-arithmetic tail bound.

    The truncation index is chosen so that the neglected tail is below
    10^-(dps+5) relative to the running partial sum, using the monotone
    ratio |z|/Gamma decay of the terms past the maximal term.
    """
    work = e_alpha_series_dps_estimate(float(alpha), float(abs(z)), dps)
    if work - dps > TAYLOR_GUARD_BUDGET_DIGITS:
        raise ValueError(
            f"Taylor route for alpha={alpha}, |z|={float(abs(z)):g} needs {work - dps} guard "
            f"digits (budget {TAYLOR_GUARD_BUDGET_DIGITS}); use route='stieltjes' (z real "
            f"negative) or a smaller |z|."
        )
    zz0 = mp.mpmathify(z)
    if zz0 == 0:
        with mp.workdps(dps):
            return mp.mpf(1), 1
    with mp.workdps(work):
        a = mp.mpf(alpha)
        zz = mp.mpmathify(z)
        tol = mp.mpf(10) ** (-(dps + 10))
        total = mp.mpf(1)
        kmax = 200000
        peak = mp.mpf(1)
        prev = mp.mpf(1)
        k = 1
        while k <= kmax:
            term = zz**k / mp.gamma(a * k + 1)
            total += term
            at = abs(term)
            if at > peak:
                peak = at
            # Terms first grow (up to index ~ |z|^{1/alpha}/alpha) and then decay
            # super-geometrically.  Truncation must be judged on the ABSOLUTE size
            # of the term relative to the answer, not relative to the peak: the
            # peak only sets how many guard digits the working precision needs to
            # absorb the cancellation.
            if k > 2 and at <= prev and at < tol * max(mp.mpf(1), abs(total)):
                break
            prev = at
            k += 1
        if k > kmax:
            raise RuntimeError(
                f"Mittag-Leffler Taylor series did not converge for alpha={alpha}, "
                f"|z|={float(abs(zz)):g} within {kmax} terms"
            )
        tail_terms = k
    with mp.workdps(dps):
        return +mp.mpmathify(total), tail_terms


def _e_alpha_stieltjes(alpha, x, dps: int):
    r"""E_alpha(-x), x > 0, 0 < alpha < 1, via the branch-cut representation.

    Collapsing the Bromwich contour of ``p^{a-1}/(p^a + x)`` onto the negative
    real axis (no poles lie on the principal sheet for ``0 < a < 1``) gives

        E_a(-x) = (x sin(a pi)/pi)
                  int_0^inf e^{-r} r^{a-1}
                            / (r^{2a} + 2 x r^a cos(a pi) + x^2) dr .

    The substitution ``s = r^a`` removes the ``r^{a-1}`` endpoint singularity
    exactly, because ``r^{a-1} dr = ds / a``:

        E_a(-x) = (x sin(a pi)/(pi a))
                  int_0^inf e^{-s^{1/a}} / (s^2 + 2 x s cos(a pi) + x^2) ds .

    Sanity check at ``x -> 0``: the integral equals ``pi a / (x sin(a pi))``,
    so the prefactor gives exactly ``E_a(0) = 1`` (unit-tested).

    The denominator is smallest near ``s = -x cos(a pi)``, which is positive when
    ``a > 1/2``; that point, together with ``s = x`` and the ``e^{-s^{1/a}}``
    decay scale ``s = 1``, is used as a quadrature split point.
    """
    with mp.workdps(dps + 20):
        a = mp.mpf(alpha)
        lam = mp.mpf(x)
        sa = mp.sin(a * mp.pi)
        ca = mp.cos(a * mp.pi)
        inv_a = 1 / a

        def f(s):
            if s == 0:
                return 1 / (lam * lam)
            return mp.e ** (-(s**inv_a)) / (s * s + 2 * lam * ca * s + lam * lam)

        pts = [mp.mpf(0), mp.mpf(1), lam, 10 * lam, 100 * lam]
        if ca < 0:
            pts.append(-lam * ca)
        pts = sorted(set(p for p in pts if p >= 0))
        pts.append(mp.inf)
        val = lam * sa / (mp.pi * a) * mp.quad(f, pts)
    with mp.workdps(dps):
        return +val


def e_alpha(alpha, z, dps: int = 30, route: str | None = None):
    """Evaluate E_alpha(z) to ``dps`` decimal digits.

    Parameters
    ----------
    alpha : positive order (0 < alpha <= 2 supported by the Taylor route).
    z     : real or complex argument.
    route : ``"taylor"``, ``"stieltjes"`` or ``None`` (automatic).
    """
    zz = mp.mpmathify(z)
    if route is None:
        is_neg_real = (mp.im(zz) == 0) and (mp.re(zz) < 0)
        # the Taylor cost is set by |z|^{1/alpha}, not by |z|, so the switch-over
        # threshold has to depend on alpha.
        pricey = (float(abs(zz)) ** (1.0 / alpha) > 150.0) if abs(zz) > 0 else False
        route = "stieltjes" if (is_neg_real and pricey and 0 < alpha < 1) else "taylor"
    if route == "stieltjes":
        if not (0 < alpha < 1):
            raise ValueError("stieltjes route requires 0 < alpha < 1")
        if mp.im(zz) != 0 or mp.re(zz) >= 0:
            raise ValueError("stieltjes route requires z real and negative")
        return _e_alpha_stieltjes(alpha, -mp.re(zz), dps)
    val, _ = _e_alpha_taylor(alpha, zz, dps)
    return val


def e_alpha_closed_form(alpha, z, dps: int = 30):
    """Independent closed form for alpha in {1/2, 1, 2}; ``None`` otherwise."""
    with mp.workdps(dps + 10):
        zz = mp.mpmathify(z)
        a = mp.mpf(alpha)
        if a == 1:
            out = mp.e**zz
        elif a == mp.mpf(1) / 2:
            out = mp.e ** (zz * zz) * mp.erfc(-zz)
        elif a == 2:
            out = mp.cosh(mp.sqrt(zz))
        else:
            return None
    with mp.workdps(dps):
        return +out


def matrix_e_alpha_scaled_rotation(alpha, rho, theta, t, dps: int = 30):
    r"""E_alpha(A t^alpha) for A = rho * [[cos th, -sin th],[sin th, cos th]].

    The algebra generated by I and J = [[0,-1],[1,0]] is isomorphic to C, so
    with lambda = rho e^{i theta} and w = E_alpha(lambda t^alpha),

        E_alpha(A t^alpha) = [[Re w, -Im w], [Im w, Re w]] .

    This is exact (no matrix series is summed) and is the ground truth used to
    validate the solvers on a genuinely two-dimensional problem.
    """
    with mp.workdps(dps + 10):
        lam = mp.mpf(rho) * mp.e ** (mp.mpc(0, 1) * mp.mpf(theta))
        z = lam * mp.mpf(t) ** mp.mpf(alpha)
        w = e_alpha(alpha, z, dps=dps + 10)
        c, s = mp.re(w), mp.im(w)
    with mp.workdps(dps):
        return mp.matrix([[+c, -s], [+s, +c]])


def e_alpha_zero(alpha, z0, dps: int = 40):
    """Refine a zero of E_alpha near ``z0`` (complex Newton via mpmath.findroot)."""
    with mp.workdps(dps + 20):
        f = lambda z: e_alpha(alpha, z, dps=dps + 20, route="taylor")
        root = mp.findroot(f, mp.mpmathify(z0), tol=mp.mpf(10) ** (-(dps + 5)))
    with mp.workdps(dps):
        return +root
