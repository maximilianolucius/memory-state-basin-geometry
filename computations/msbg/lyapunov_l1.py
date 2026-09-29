r"""Exact-rational certificate for CANDIDATE-L1 (research/LOCAL_SURVIVAL_BASIN.md).

Everything that can be exact is exact (``fmpq``); the only enclosures are of the
two eigenvalues of the rational symmetric matrix P and of one square root, done
in Arb.

Model:  F1 = x(1-x)(x-theta) - a x y,  F2 = y(b x - m),  all parameters rational.

Exact objects
-------------
    x* = m/b,   y* = (1-x*)(x*-theta)/a
    J  = [[x* (1 + theta - 2 x*), -a x*], [b y*, 0]]
    tr J = x* (1 + theta - 2 x*),   det J = a b x* y*
    Hurwitz  <=>  tr J < 0 and det J > 0        (exact rational sign tests)
    P solves J^T P + P J = -I   (3x3 rational linear system, solved exactly)

Exact remainder.  With u = z - E*,
    N1(u) = -(3 x* - 1 - theta) u1^2 - a u1 u2 - u1^3 ,     N2(u) = b u1 u2 .
(check: F1 is cubic in x and bilinear in (x,y), so its Taylor expansion at E* is
finite; the u1^2 coefficient is F1_xx/2 = -(3x* - (1+theta)), u1 u2 is -a, u1^3 is -1.)

Rigorous C_r.  For ||u||_2 <= r:  u1^2 <= ||u||^2, |u1 u2| <= ||u||^2/2, |u1|^3 <= r ||u||^2,
    |N1| <= (|3x*-1-theta| + a/2 + r) ||u||^2 =: A_r ||u||^2 ,   |N2| <= (b/2) ||u||^2 ,
    C_r := sqrt(A_r^2 + b^2/4).

L1 inequality:  2 ||P||_2 C_r r <= 1/2.  The left side is increasing in r, so the
largest admissible r is found by bisection over rationals and then a rational
r_cert strictly inside is fixed and VERIFIED in Arb.

Certified set:  Omega = { u : u^T P u < lam_min(P) r_cert^2 }.
Its extent in the x direction is  sqrt( lam_min r^2 (P^{-1})_{11} ).
"""
from __future__ import annotations

from dataclasses import dataclass

from flint import arb, ctx, fmpq, fmpq_mat

__all__ = ["L1Certificate", "l1_certificate", "Q"]


def Q(s) -> fmpq:
    """Exact rational from 'p/q', an int, or a decimal string like '0.85'."""
    if isinstance(s, fmpq):
        return s
    if isinstance(s, int):
        return fmpq(s)
    s = str(s).strip()
    if "/" in s:
        p, q = s.split("/")
        return fmpq(int(p), int(q))
    if "." in s:
        sign = -1 if s.startswith("-") else 1
        s2 = s.lstrip("+-")
        ip, fp = s2.split(".")
        return sign * fmpq(int(ip + fp), 10 ** len(fp))
    return fmpq(int(s))


def _arb(q: fmpq):
    return arb(q.p) / arb(q.q)


@dataclass
class L1Certificate:
    theta: fmpq
    a: fmpq
    b: fmpq
    m: fmpq
    x_star: fmpq
    y_star: fmpq
    J: list
    trace: fmpq
    det: fmpq
    hurwitz: bool
    P: list | None = None
    lam_min: object = None
    lam_max: object = None
    r_cert: fmpq | None = None
    C_r: object = None
    lhs: object = None
    level: object = None            # lam_min * r^2   (arb)
    x_extent: object = None         # arb, half-width of Omega in x
    y_extent: object = None
    gap: fmpq | None = None         # x* - theta
    omega_avoids_strip: bool | None = None   # certified: x* - x_extent > theta
    ratio_extent_gap: float | None = None

    def V(self, u1, u2):
        """u^T P u as an Arb ball for rational/arb inputs."""
        P = self.P
        u1 = _arb(u1) if isinstance(u1, fmpq) else arb(u1)
        u2 = _arb(u2) if isinstance(u2, fmpq) else arb(u2)
        return _arb(P[0][0]) * u1 * u1 + 2 * _arb(P[0][1]) * u1 * u2 + _arb(P[1][1]) * u2 * u2

    def contains(self, px, py) -> bool:
        """Certified membership of p in Omega (strict, in Arb)."""
        v = self.V(Q(px) - self.x_star, Q(py) - self.y_star)
        return bool(v.upper() < self.level.lower())


def l1_certificate(theta, a, b, m, prec: int = 200) -> L1Certificate:
    ctx.prec = prec
    th, a, b, m = Q(theta), Q(a), Q(b), Q(m)
    xs = m / b
    ys = (1 - xs) * (xs - th) / a
    J11 = xs * (1 + th - 2 * xs)
    J12 = -a * xs
    J21 = b * ys
    J22 = fmpq(0)
    tr = J11 + J22
    det = J11 * J22 - J12 * J21
    hur = bool(tr < 0 and det > 0 and th < xs < 1 and ys > 0)
    cert = L1Certificate(th, a, b, m, xs, ys, [[J11, J12], [J21, J22]], tr, det, hur,
                         gap=xs - th)
    if not hur:
        return cert
    # J^T P + P J = -I with P = [[p,q],[q,s]]:
    #   (1,1): 2(J11 p + J21 q) = -1
    #   (1,2): J12 p + (J11 + J22) q + J21 s = 0
    #   (2,2): 2(J12 q + J22 s) = -1
    A = fmpq_mat(3, 3, [2 * J11, 2 * J21, 0,
                        J12, J11 + J22, J21,
                        0, 2 * J12, 2 * J22])
    rhs = fmpq_mat(3, 1, [-1, 0, -1])
    sol = A.solve(rhs)
    p, q, s = sol[0, 0], sol[1, 0], sol[2, 0]
    # exact residual check
    Pm = fmpq_mat(2, 2, [p, q, q, s])
    Jm = fmpq_mat(2, 2, [J11, J12, J21, J22])
    res = Jm.transpose() * Pm + Pm * Jm
    assert res[0, 0] == -1 and res[1, 1] == -1 and res[0, 1] == 0 and res[1, 0] == 0
    assert p > 0 and p * s - q * q > 0, "P must be positive definite"
    cert.P = [[p, q], [q, s]]
    half_tr = _arb(p + s) / 2
    disc = (_arb(p - s) / 2) ** 2 + _arb(q) ** 2
    root = disc.sqrt()
    cert.lam_min = half_tr - root
    cert.lam_max = half_tr + root
    assert cert.lam_min.lower() > 0

    c2 = abs(3 * xs - 1 - th)

    def lhs_of(r: fmpq):
        Ar = _arb(c2 + a / 2 + r)
        C = (Ar * Ar + _arb(b * b / 4)).sqrt()
        return 2 * cert.lam_max * C * _arb(r), C

    lo, hi = fmpq(0), fmpq(1)
    while lhs_of(hi)[0].upper() < 0.5:
        hi *= 2
    for _ in range(80):
        mid = (lo + hi) / 2
        if lhs_of(mid)[0].upper() < 0.5:
            lo = mid
        else:
            hi = mid
    # a rational strictly inside, with a modest denominator
    r = fmpq(int(lo * 10**9 * fmpq(999, 1000)), 10**9) if lo > 0 else fmpq(0)
    val, C = lhs_of(r)
    assert val.upper() <= 0.5, "L1 inequality must hold at r_cert"
    cert.r_cert, cert.C_r, cert.lhs = r, C, val
    cert.level = cert.lam_min * _arb(r) ** 2
    detP = _arb(p * s - q * q)
    cert.x_extent = (cert.level * _arb(s) / detP).sqrt()     # (P^-1)_11 = s/det P
    cert.y_extent = (cert.level * _arb(p) / detP).sqrt()
    cert.omega_avoids_strip = bool((_arb(xs) - cert.x_extent).lower() > _arb(th).upper())
    cert.ratio_extent_gap = float(cert.x_extent.upper()) / float(xs - th)
    return cert
