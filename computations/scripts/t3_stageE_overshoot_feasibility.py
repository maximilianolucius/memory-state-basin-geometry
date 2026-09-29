#!/usr/bin/env python3
r"""TASK-0003 Stage E — is an overshoot-permitting survival certificate feasible?

WHY L1 CANNOT WORK, AND WHAT COULD
----------------------------------
L1 keeps the orbit inside the set it starts from (a Lyapunov sublevel set), and
that set cannot meet R_ext (return report, section 1).  A certificate can only
succeed if the set where the orbit LIVES is strictly larger than the set where
it STARTS.  The variation-of-constants formula gives such a certificate:

    u(t) = Phi(t) u0 + int_0^t Psi(t-s) N(u(s)) ds,
    Phi(t) = E_alpha(J t^alpha),   Psi(s) = s^{alpha-1} E_{alpha,alpha}(J s^alpha).

Weighted max-norm |u|_w = max(|u1|/w1, |u2|/w2).  With
    M(u0) = sup_t |Phi(t) u0|_w ,      K = int_0^inf ||Psi(s)||_w ds ,
    |N(u)|_w <= C(r) |u|_w^2  for |u|_w <= r,
    C(r) = max( |c2| w1 + a w2 + w1^2 r ,  b w1 ),   c2 = 3x* - 1 - theta,
the ball {sup_t |u(t)|_w <= r} is invariant as soon as

    (I)   M(u0) + K C(r) r^2 <= r ,

and 2 K C(r) r < 1 then gives u(t) -> 0 (limsup argument).  Entry into R_ext
needs the orbit to reach u1 < -(x* - theta) =: -g, which the certificate can
only accommodate if  w1 r > g.  A sufficient condition for entry from the linear
orbit alone is

    (II)  -min_t [Phi(t) u0]_1  -  w1 K C(r) r^2  >  g .

THIS SCRIPT IS A FEASIBILITY STUDY, NOT A CERTIFICATE.  Phi and the integral of
Psi are computed with the float PECE solver on a finite horizon, K carries an
estimated tail, and nothing is enclosed.  Its only purpose is to decide whether
(I) and (II) can hold simultaneously for ANY parameter set, before anyone
invests in rigorous bounds for K.

Evidence class: NUMERICAL EXPLORATION.
"""
import argparse
import itertools
import os
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.provenance import RunRecorder      # noqa: E402
from msbg.solvers import solve               # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Lin:
    """^C D^a v = J v + c  (c constant), batched."""

    def __init__(self, J, c):
        self.J, self.c = J, c

    def g(self, X):
        return X @ self.J.T + self.c[None, :]

    def jac(self, X):
        return np.broadcast_to(self.J, (X.shape[0], 2, 2)).copy()


def one(cfg):
    np.seterr(all="ignore")
    theta, frac, a, b, alpha, T, h = cfg
    xs = theta + frac * (1 - theta)
    ys = (1 - xs) * (xs - theta) / a
    g = xs - theta
    J = np.array([[xs * (1 + theta - 2 * xs), -a * xs], [b * ys, 0.0]])
    lam = np.linalg.eigvals(J)
    if not (np.all(lam.real < 0)):
        return None
    N = int(round(T / h))
    # Phi columns
    rP = solve(Lin(J, np.zeros(2)), np.eye(2), alpha, h, N, method="pece", store=True)
    Phi = rP.x                                  # (K, 2 initial, 2 comps): Phi[t, j, i] = Phi_ij
    # W_j(t) = int_0^t Psi(s) e_j ds : forced problems from zero
    Wc = []
    for j in range(2):
        rW = solve(Lin(J, np.eye(2)[j]), np.zeros((1, 2)), alpha, h, N, method="pece", store=True)
        Wc.append(rW.x[:, 0, :])
    W = np.stack(Wc, axis=1)                    # (K, j, i)
    dW = np.abs(np.diff(W, axis=0))             # |int over one step of Psi_ij|  (lower bound of int|Psi|)
    t = rP.t
    c2 = abs(3 * xs - 1 - theta)
    Jinv = np.linalg.inv(J)
    best = None
    for omega in np.geomspace(1e-3, 1e3, 61):   # omega = w2 / w1, take w1 = 1
        w = np.array([1.0, omega])
        # induced weighted max-norm of the kernel, integrated:  sum_j |Psi_ij| w_j / w_i
        kern = np.einsum("tji,j->ti", dW, w) / w[None, :]      # (K-1, i)
        K_fin = float(np.max(np.sum(kern, axis=0)))
        # tail: Psi ~ t^{-alpha-1}; match the last decade
        k0 = int(0.5 * len(kern))
        tail_rate = np.sum(kern[k0:], axis=0)
        # int_{T/2}^{T} c s^{-a-1} = c ((T/2)^-a - T^-a)/a  ;  int_T^inf = c T^-a / a
        fac = (T ** -alpha) / ((T / 2) ** -alpha - T ** -alpha)
        K = K_fin + float(np.max(tail_rate * fac))
        K_lower = float(np.max(np.abs(Jinv) @ w / w))
        for phi in np.linspace(0, 2 * np.pi, 72, endpoint=False):
            d = np.array([np.cos(phi), np.sin(phi) * omega])   # |d|_w = 1
            lin = np.einsum("tji,j->ti", Phi, d)               # Phi(t) d
            M1 = float(np.max(np.max(np.abs(lin) / w[None, :], axis=1)))
            dip1 = float(-np.min(lin[:, 0]))                   # undershoot of u1 per unit |u0|_w
            if dip1 <= 0:
                continue
            # scale s = |u0|_w ; unknown r.  (I): s M1 + K C(r) r^2 <= r ; (II): s dip1 - K C r^2 > g
            for r in np.geomspace(g * 1.0001, 50 * g, 40):
                C = max(c2 + a * omega + r, b)
                delta = K * C * r * r
                if delta >= r or 2 * K * C * r >= 1:
                    break
                s_max = (r - delta) / M1
                margin = s_max * dip1 - delta - g             # > 0  => feasible
                # the start must not already lie in the strip or outside the cone
                u0 = s_max * d
                start_ok = (u0[0] > -g) and (ys + u0[1] > 0) and (xs + u0[0] > 0)
                score = margin / g
                if start_ok and (best is None or score > best["score"]):
                    best = {"score": float(score), "omega": float(omega), "phi": float(phi),
                            "r": float(r), "K": K, "K_lower_Jinv": K_lower, "C": float(C),
                            "M1": M1, "dip1": dip1, "delta": float(delta),
                            "s_max": float(s_max), "two_KCr": float(2 * K * C * r),
                            "u0": u0.tolist()}
    out = {"theta": theta, "frac": frac, "a": a, "b": b, "alpha": alpha, "x_star": xs,
           "y_star": ys, "gap": g, "eig": [[float(l.real), float(l.imag)] for l in lam],
           "T": T, "h": h, "best": best}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=100)
    ap.add_argument("--T", type=float, default=400.0)
    ap.add_argument("--h", type=float, default=0.02)
    args = ap.parse_args()
    thetas = [0.1, 0.3, 0.5, 0.7, 0.9]
    fracs = [0.505, 0.52, 0.55, 0.6, 0.7, 0.85]
    aa = [0.25, 1.0, 4.0]
    bb = [0.05, 0.25, 1.0, 4.0]
    alphas = [0.5, 0.7, 0.85, 0.95]
    cfgs = [(th, f, a, b, al, args.T, args.h)
            for th, f, a, b, al in itertools.product(thetas, fracs, aa, bb, alphas)]
    print(f"configs={len(cfgs)} workers={args.workers}", flush=True)
    rec = RunRecorder("t3_stageE", ROOT)
    rows = []
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        for i, r in enumerate(ex.map(one, cfgs, chunksize=2)):
            if r is not None:
                rows.append(r)
    have = [r for r in rows if r["best"] is not None]
    feas = [r for r in have if r["best"]["score"] > 0]
    have.sort(key=lambda r: -r["best"]["score"])
    print(f"Hurwitz configs: {len(rows)};  with an admissible (I): {len(have)};  "
          f"FEASIBLE (I)+(II): {len(feas)}")
    print(f"{'theta':>6}{'x*':>7}{'a':>6}{'b':>6}{'alpha':>6}{'score':>9}{'K':>9}{'K>=|J^-1|':>11}"
          f"{'2KCr':>7}{'r/g':>7}{'dip/M':>7}")
    for r in have[:15]:
        b_ = r["best"]
        print(f"{r['theta']:6}{r['x_star']:7.3f}{r['a']:6}{r['b']:6}{r['alpha']:6}{b_['score']:9.3f}"
              f"{b_['K']:9.2f}{b_['K_lower_Jinv']:11.2f}{b_['two_KCr']:7.3f}"
              f"{b_['r']/r['gap']:7.2f}{b_['dip1']/b_['M1']:7.3f}")
    rec.save_json("rows", rows)
    rec.add("n_hurwitz", len(rows))
    rec.add("n_feasible", len(feas))
    rec.add("best_score", have[0]["best"]["score"] if have else None)
    rec.add("top", have[:10])
    rec.add("evidence_class", "NUMERICAL EXPLORATION - not a certificate")
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
