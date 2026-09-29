r"""Rigorous ball-arithmetic certification (python-flint / Arb).

Everything here is CERTIFIED COMPUTATION in the sense of PROTOCOL.md: every
arithmetic operation is Arb ball arithmetic, and every truncated series carries
an explicit, proved tail bound, so an output enclosure is a mathematically valid
statement about the real object.

Arithmetic semantics (required disclosure)
-----------------------------------------
* Arb ``arb``/``acb`` balls; every operation returns an enclosure of the exact
  result for every point of the input balls.
* working precision ``flint.ctx.prec`` bits, stated with each result;
* Gamma values come from Arb's proved ``gamma`` implementation;
* the Mittag-Leffler series is truncated at index ``K`` and the neglected tail
  is bounded as proved in :func:`_tail_bound`;
* root certification uses the Krawczyk operator; a successful test proves
  *existence and uniqueness* of a zero in the returned box.
"""
from __future__ import annotations

from dataclasses import dataclass

from flint import acb, arb, ctx

__all__ = ["e_alpha_ball", "e_alpha_prime_ball", "krawczyk_certify_zero",
           "krawczyk_certify_zero_auto", "CertifiedZero"]


def _tail_bound(alpha, R, K, derivative=False):
    r"""Rigorous bound on the neglected tail of the E_alpha series.

    For ``T_k = R^k / Gamma(alpha k + 1)`` the ratio
    ``T_{k+1}/T_k = R Gamma(alpha k + 1)/Gamma(alpha k + alpha + 1)``
    is *decreasing* in ``k`` because ``Gamma(x + alpha)/Gamma(x)`` is increasing
    in ``x > 0`` (log-convexity of Gamma).  Hence if the ratio at ``k = K+1``
    is ``rho < 1`` then

        sum_{k > K} T_k <= T_{K+1} / (1 - rho).

    For the derivative series ``T'_k = k R^{k-1} / Gamma(alpha k + 1)`` the ratio
    picks up a factor ``(k+1)/k <= (K+2)/(K+1)``, which is used as ``rho'``.

    Returns an ``arb`` upper bound, or ``None`` if the ratio test fails.
    """
    a = arb(alpha)
    k1 = arb(K + 1)
    num = a * k1 + 1
    ratio = R * (num.gamma() / (num + a).gamma())
    if derivative:
        ratio = ratio * (arb(K + 2) / arb(K + 1))
    if not (ratio.upper() < 1):
        return None
    if derivative:
        t = k1 * R ** arb(K) * num.rgamma()
    else:
        t = R ** k1 * num.rgamma()
    return (t / (1 - ratio)).abs_upper()


def _series(alpha, Z, K, derivative=False):
    a = arb(alpha)
    total = acb(0)
    if derivative:
        for k in range(1, K + 1):
            total += arb(k) * Z ** (k - 1) * (a * k + 1).rgamma()
    else:
        for k in range(0, K + 1):
            total += Z**k * (a * k + 1).rgamma()
    return total


def e_alpha_ball(alpha, Z, K: int = 120, prec: int | None = 300):
    """Rigorous enclosure of ``E_alpha(Z)`` for an ``acb`` box ``Z``."""
    if prec is not None:
        ctx.prec = prec
    Z = acb(Z)
    R = abs(Z).abs_upper()
    tail = _tail_bound(alpha, R, K)
    if tail is None:
        raise ValueError(f"tail ratio test failed for K={K}, |Z|<={R}")
    s = _series(alpha, Z, K)
    return acb(arb(s.real.mid(), s.real.rad() + tail), arb(s.imag.mid(), s.imag.rad() + tail))


def e_alpha_prime_ball(alpha, Z, K: int = 120, prec: int | None = 300):
    """Rigorous enclosure of ``E_alpha'(Z)``."""
    if prec is not None:
        ctx.prec = prec
    Z = acb(Z)
    R = abs(Z).abs_upper()
    tail = _tail_bound(alpha, R, K, derivative=True)
    if tail is None:
        raise ValueError(f"derivative tail ratio test failed for K={K}, |Z|<={R}")
    s = _series(alpha, Z, K, derivative=True)
    return acb(arb(s.real.mid(), s.real.rad() + tail), arb(s.imag.mid(), s.imag.rad() + tail))


@dataclass
class CertifiedZero:
    alpha: float
    box_re: str
    box_im: str
    radius_re: str
    radius_im: str
    prec_bits: int
    series_K: int
    method: str = "Krawczyk operator on E_alpha with proved series tail bound"
    unique: bool = True

    def as_dict(self):
        return dict(
            alpha=self.alpha,
            enclosure_real=self.box_re,
            enclosure_imag=self.box_im,
            radius_real=self.radius_re,
            radius_imag=self.radius_im,
            prec_bits=self.prec_bits,
            series_K=self.series_K,
            method=self.method,
            unique_in_box=self.unique,
            evidence_class="CERTIFIED COMPUTATION",
        )


def krawczyk_certify_zero(alpha, z_hat, radius, K: int = 160, prec: int = 400):
    r"""Certify a simple zero of ``E_alpha`` in the box around ``z_hat``.

    Krawczyk operator with ``Y = 1/E_alpha'(z_hat)``:

        K(Z) = z_hat - Y E_alpha(z_hat) + (1 - Y E_alpha'(Z)) (Z - z_hat)

    If ``K(Z)`` is contained in the *interior* of ``Z`` then ``E_alpha`` has
    exactly one zero in ``Z``.  Returns ``(CertifiedZero, Z)`` or ``(None, Z)``.
    """
    ctx.prec = prec
    zc = acb(z_hat)
    r = arb(radius)
    Z = acb(arb(zc.real.mid(), r), arb(zc.imag.mid(), r))
    Fc = e_alpha_ball(alpha, acb(zc.real.mid(), zc.imag.mid()), K=K)
    Fpc = e_alpha_prime_ball(alpha, acb(zc.real.mid(), zc.imag.mid()), K=K)
    Y = acb(Fpc.real.mid(), Fpc.imag.mid()) ** (-1)
    FpZ = e_alpha_prime_ball(alpha, Z, K=K)
    zmid = acb(zc.real.mid(), zc.imag.mid())
    Kop = zmid - Y * Fc + (acb(1) - Y * FpZ) * (Z - zmid)
    ok = bool(Z.real.contains_interior(Kop.real)) and bool(Z.imag.contains_interior(Kop.imag))
    if not ok:
        return None, Z
    # the certified enclosure is K(Z), which is tighter than Z
    cz = CertifiedZero(
        alpha=float(alpha),
        box_re=str(Kop.real),
        box_im=str(Kop.imag),
        radius_re=str(Kop.real.rad()),
        radius_im=str(Kop.imag.rad()),
        prec_bits=prec,
        series_K=K,
    )
    return cz, Kop


def krawczyk_certify_zero_auto(
    alpha,
    z_hat,
    radii=(1e-32, 1e-28, 1e-24, 1e-20, 1e-16, 1e-12, 1e-9, 1e-6, 1e-4),
    K: int = 200,
    prec: int = 600,
):
    """Try a ladder of box radii and return the tightest successful certificate.

    The Krawczyk test fails both when the box is too large (the derivative is not
    close enough to constant on it) and when it is too small relative to the
    accuracy of the enclosure of ``E_alpha`` at the centre, which depends on the
    working precision and on the series truncation.  Sweeping the radius removes
    that platform sensitivity; the attempt log is returned for the record.
    """
    attempts = []
    best = None
    for r in radii:
        cz, box = krawczyk_certify_zero(alpha, z_hat, r, K=K, prec=prec)
        attempts.append({"radius": float(r), "certified": cz is not None})
        if cz is not None and best is None:
            best = (cz, box, float(r))
    if best is None:
        return None, None, attempts
    cz, box, r = best
    return cz, box, attempts
