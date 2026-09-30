r"""Rigorous upper bound of  K = int_0^inf |psi_lambda(s)| ds,
    psi_lambda(s) = s^{alpha-1} E_{alpha,alpha}(lambda s^alpha),   lambda complex, 0 < alpha < 1.

Substituting rho = s^alpha (s^{alpha-1} ds = d rho / alpha):

    K = (1/alpha) int_0^inf | E_{alpha,alpha}(lambda rho) | d rho .

REPRESENTATION USED FOR LARGE ARGUMENT (to be audited by ROUND-0005)
-------------------------------------------------------------------
Collapsing the Hankel contour of  E_{a,a}(z) = (1/2 pi i) int_Ha e^zeta /(zeta^a - z) d zeta
onto the negative real axis, for  a pi/2 < |arg z| < a pi  (pole zeta_0 = z^{1/a} inside):

    E_{a,a}(z) = (1/a) z^{(1-a)/a} exp(z^{1/a})  +  I(z),
    I(z) = (sin(a pi)/pi) int_0^inf e^{-r} r^a / ( (r^a e^{i a pi} - z)(r^a e^{-i a pi} - z) ) dr .

With phi = |arg z| and Delta = a pi - phi in (0, pi/2):
    |r^a e^{+i a pi sgn} - z| >= |z| sin(Delta)   (nearest ray),   >= |z|  (far ray, angle > pi/2),
so, with x = |z|,
    |I(z)|  <= B / x^2,            B  = sin(a pi) Gamma(a+1) / (pi sin Delta),
    |I'(z)| <= B1 / x^3,           B1 = sin(a pi) Gamma(a+1) (1/sin^2 Delta + 1/sin Delta) / pi,
and the pole term has modulus (1/a) x^{(1-a)/a} exp(-c x^{1/a}),  c = -cos(phi/a) > 0.

BOUND
-----
* [0, rho_0]: cells; on each cell  |E(lambda rho)| <= |E(lambda rho_mid)| + Lip * width/2,
  E(lambda rho_mid) from the Taylor series in Arb with a proved tail bound, Lip from
  the positive series  sum k x^{k-1}/Gamma(a k + a)  (small x) or from the
  representation (large x), whichever is smaller.
* [rho_0, inf): closed forms  B /(|lambda|^2 rho_0)  and  exp(-c y_0)/(c |lambda|),
  y_0 = (|lambda| rho_0)^{1/a}.
"""
from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor

__all__ = ["ml_aa_ball", "kernel_bound", "envelope_table", "exact_constants",
           "representation_value"]


def _series_tail(a, beta, R, K):
    """sum_{k>K} R^k / Gamma(a k + beta) <= T_{K+1}/(1 - ratio); needs a(K+1)+beta >= 2."""
    from flint import arb
    k1 = arb(K + 1)
    num = a * k1 + beta
    assert num.lower() > 2
    ratio = R * (num.gamma() / (num + a).gamma())
    if not (ratio.upper() < 1):
        return None
    return (R ** k1 * num.rgamma() / (1 - ratio)).abs_upper()


def ml_aa_ball(a, z, prec):
    """Rigorous enclosure of E_{a,a}(z) at an acb point/ball z."""
    from flint import acb, arb, ctx
    ctx.prec = prec
    R = abs(z).abs_upper()
    K = 40
    while True:
        tail = _series_tail(a, a, R, K)
        if tail is not None and float(tail) < 2.0 ** (-(prec // 2)):
            break
        K = int(K * 1.5) + 10
        if K > 200000:
            raise RuntimeError("series tail did not become small")
    tot = acb(0)
    zp = acb(1)
    for k in range(K + 1):
        tot += zp * (a * k + a).rgamma()
        zp *= z
    return acb(arb(tot.real.mid(), tot.real.rad() + tail), arb(tot.imag.mid(), tot.imag.rad() + tail))


def _lip_series(a, x, prec):
    """sum_{k>=1} k x^{k-1} / Gamma(a k + a)  (all terms positive), upper bound."""
    from flint import arb, ctx
    ctx.prec = prec
    tot = arb(0)
    xp = arb(1)
    k = 1
    while True:
        term = arb(k) * xp * (a * k + a).rgamma()
        tot += term
        if k > 8 and float(term.abs_upper()) < 1e-30 and float((x * (a * k + a).gamma() / (a * (k + 1) + a).gamma() * arb(k + 1) / arb(k)).abs_upper()) < 0.5:
            tot += term            # geometric remainder with ratio < 1/2
            break
        xp *= x
        k += 1
        if k > 100000:
            raise RuntimeError
    return tot


_C = {}


def exact_constants(spec, prec):
    """All constants rebuilt from EXACT data at the requested precision.

    ``spec = (alpha, mu, nu2)`` with alpha, mu rational strings and nu2 a rational
    string:  lambda = mu + i sqrt(nu2).  Rebuilding at the working precision is
    essential: the Taylor series of E_{a,a} cancels about |z|^{1/a}/ln 2 bits, so a
    128-bit enclosure of alpha or lambda reused at 400 bits destroys the result
    (first version of this module: K 'bound' of 1e33).
    """
    from flint import acb, arb, ctx
    from .lyapunov_l1 import Q
    ctx.prec = prec
    al, mu, nu2 = (Q(v) for v in spec)
    a = arb(al.p) / arb(al.q)
    lam = acb(arb(mu.p) / arb(mu.q), (arb(nu2.p) / arb(nu2.q)).sqrt())
    xl = abs(lam)
    phi = arb.pi() - (lam.imag / (-lam.real)).atan() if float(lam.real.mid()) < 0 else (lam.imag / lam.real).atan()
    pi = arb.pi()
    Delta = a * pi - phi
    assert Delta.lower() > 0 and float(Delta.upper()) < float(pi.lower()) / 2, "need a pi/2 < a pi - phi"
    assert (phi - a * pi / 2).lower() > 0, "Matignon stability required"
    sD = Delta.sin()
    common = (a * pi).sin() / pi
    return dict(a=a, lam=lam, xl=xl, phi=phi, sD=sD,
                B=common * (a + 1).gamma() / sD,                       # |I_{a,a}(z)| <= B/x^2
                B1=common * (a + 1).gamma() * (1 / (sD * sD) + 1 / sD),  # |I'_{a,a}(z)| <= B1/x^3
                Bphi=common * a.gamma() / sD,                          # |I_{a,1}(z)| <= Bphi/x
                c=-(phi / a).cos())


def _init(spec):
    _C["spec"] = spec
    _C.update(exact_constants(spec, 128))
    assert _C["c"].lower() > 0


def _cell(job):
    """Upper bounds on [r0, r1] of  sup |E_{a,a}(lambda rho)|  and of its integral."""
    from flint import arb, ctx
    r0, r1 = job
    c128 = _C
    x_hi_f = float((c128["xl"] * arb(r1)).abs_upper())
    bits = 128 + int(1.6 * x_hi_f ** (1.0 / float(c128["a"].mid()))) + 32
    C = exact_constants(_C["spec"], bits)
    a, lam, xl = C["a"], C["lam"], C["xl"]
    lo, hi = arb(r0), arb(r1)
    mid = (lo + hi) / 2
    width = hi - lo
    x_hi, x_lo = xl * hi, xl * lo
    val = abs(ml_aa_ball(a, lam * mid, bits))
    lip = None
    if x_hi_f < 3.0:
        lip = xl * _lip_series(a, x_hi, bits)
    if float(x_lo.lower()) > 0.5:
        g1 = (1 / a) * (((1 - a) / a) * x_lo ** ((1 - 2 * a) / a)
                        + (1 / a) * x_hi ** ((2 - 2 * a) / a)) * (-(C["c"] * x_lo ** (1 / a))).exp()
        rep = xl * (C["B1"] / x_lo ** 3 + g1)
        if lip is None or float(rep.abs_upper()) < float(lip.abs_upper()):
            lip = rep
    sup = val + lip * width / 2
    out = (float(sup.abs_upper()) * (1 + 2.0 ** -50), float(val.abs_upper()))
    ctx.prec = 128
    return out


def envelope_table(spec, rho0, workers=None, d_small=2.5e-4, rel=2e-3):
    """Rigorous piecewise-constant upper envelope of |E_{a,a}(lambda rho)| on [0, rho0]."""
    import numpy as np
    _init(spec)
    xl = float(_C["xl"].mid())
    edges = [0.0]
    r_switch = 2.0 / xl
    while edges[-1] < r_switch:
        edges.append(edges[-1] + d_small)
    while edges[-1] < rho0:
        edges.append(min(rho0, edges[-1] * (1 + rel)))
    jobs = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]
    with ProcessPoolExecutor(max_workers=workers or os.cpu_count(), initializer=_init,
                             initargs=(spec,)) as ex:
        res = list(ex.map(_cell, jobs, chunksize=128))
    return np.array(edges), np.array([r[0] for r in res]), np.array([r[1] for r in res])


def kernel_bound(spec, rho0=200.0, workers=None, d_small=2.5e-4, rel=2e-3):
    """Rigorous upper bound of K = int_0^inf |psi_lambda| and its pieces."""
    import math
    import numpy as np
    from flint import arb, ctx
    edges, sup, mid = envelope_table(spec, rho0, workers, d_small, rel)
    w = np.diff(edges)
    finite_up = math.fsum(np.nextafter(sup * w, np.inf)) * (1 + 1e-12)
    finite_mid = math.fsum(mid * w)
    ctx.prec = 128
    C = exact_constants(spec, 128)
    a = C["a"]
    x0 = C["xl"] * arb(rho0)
    tail_alg = C["B"] / (C["xl"] ** 2 * arb(rho0))
    tail_exp = (-(C["c"] * x0 ** (1 / a))).exp() / (C["c"] * C["xl"])
    tail = float((tail_alg + tail_exp).abs_upper())
    inv_a = float((1 / a).abs_upper())
    return {"K_upper": (finite_up + tail) * inv_a * (1 + 1e-12),
            "finite_part_upper": finite_up * inv_a,
            "finite_part_midpoint_sum": finite_mid * inv_a, "tail_upper": tail * inv_a,
            "rho0": rho0, "n_cells": len(w), "B": float(C["B"].abs_upper()),
            "B1": float(C["B1"].abs_upper()), "Bphi": float(C["Bphi"].abs_upper()),
            "c": float(C["c"].lower()), "phi": float(C["phi"].mid()),
            "abs_lambda": float(C["xl"].mid()),
            "K_lower_exact_identity": float((1 / C["xl"]).lower())}


def representation_value(alpha, z, dps=25):
    """Non-rigorous evaluation of the representation (used only to TEST the formula)."""
    import mpmath as mp
    with mp.workdps(dps):
        a = mp.mpf(alpha)
        z = mp.mpmathify(z)
        pole = (1 / a) * z ** ((1 - a) / a) * mp.e ** (z ** (1 / a))
        f = lambda r: mp.e ** (-r) * r**a / ((r**a * mp.e ** (1j * a * mp.pi) - z)
                                             * (r**a * mp.e ** (-1j * a * mp.pi) - z))
        I = mp.sin(a * mp.pi) / mp.pi * mp.quad(f, [0, 1, 10, mp.inf])
        return pole + I, pole, I
