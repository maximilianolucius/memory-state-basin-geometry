#!/usr/bin/env python3
"""TASK-0004 — amplification PROFILE in time (float), to explain the scan/verifier gap.

The witness scan recorded the J-resolvent amplification w(T) at T = 300, 600, 1000.
The verifier's bootstrap needs  max over [0,T]  of the bound, so the relevant
quantity is  sup_{t <= T} w(t).  This script prints the whole profile, in the
adapted 2-norm and with the Frobenius norm the rigorous code uses.
Evidence class: NUMERICAL EXPLORATION.
"""
import os
import sys
from math import gamma

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.memory_tail import psi_scalar            # noqa: E402
from msbg.models import AlleePredatorPrey          # noqa: E402
from msbg.provenance import RunRecorder            # noqa: E402
from msbg.solvers import solve                     # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def profile(label, theta, a, b, m, alpha, p, T_end=1000.0, h=0.02):
    np.seterr(all="ignore")
    model = AlleePredatorPrey(theta=theta, a=a, b=b, m=m)
    E = np.array([model.x_star, model.y_star])
    J = model.jac(E[None, :])[0]
    lam, V = np.linalg.eig(J)
    k = int(np.argmax(lam.imag))
    l, v = lam[k], V[:, k]
    S = np.column_stack([v.real, -v.imag])
    Si = np.linalg.inv(S)
    N = int(round(T_end / h))
    r = solve(model, np.atleast_2d(p), alpha, h, N, method="pece", store=True)
    x, t = r.x[:, 0, :], r.t
    A = np.einsum("ij,tjk,kl->til", Si, model.jac(x) - J[None], S)
    a2 = np.linalg.norm(A, ord=2, axis=(1, 2))
    aF = np.linalg.norm(A, ord="fro", axis=(1, 2))
    smid = (np.arange(N) + 0.5) * h
    sg = np.geomspace(smid[0], smid[-1], 400)
    pg = np.array([abs(complex(psi_scalar(alpha, complex(l), float(s), dps=16))) for s in sg])
    kern = np.exp(np.interp(np.log(smid), np.log(sg), np.log(pg))) * h
    kern[0] = h**alpha / gamma(alpha + 1)
    out = {}
    for name, coef in (("2-norm", a2), ("Frobenius", aF)):
        w = np.ones(N + 1)
        scale = 0.0
        logw = np.zeros(N + 1)
        for n in range(1, N + 1):
            w[n] = np.exp(-scale) + np.dot(kern[n - 1::-1], coef[:n] * w[:n])
            logw[n] = np.log10(w[n]) + scale / np.log(10)
            if w[n] > 1e100:
                w[: n + 1] /= 1e100
                scale += np.log(1e100)
        out[name] = logw
    marks = [1, 2, 5, 10, 20, 40, 60, 100, 200, 300, 600, 1000]
    print(f"\n{label}: p={p}  E*={E}")
    print(f"{'t':>6}{'x(t)':>9}{'a(2-norm)':>11}{'log10 w (2)':>13}{'log10 w (Fro)':>15}")
    for T in marks:
        n = int(round(T / h))
        print(f"{T:6d}{x[n,0]:9.4f}{a2[n]:11.4f}{out['2-norm'][n]:13.2f}{out['Frobenius'][n]:15.2f}")
    res = {"label": label, "sup_log10_w_2norm": float(out["2-norm"].max()),
           "t_of_sup": float(t[int(out["2-norm"].argmax())]),
           "sup_log10_w_frobenius": float(out["Frobenius"].max()),
           "log10_w_at_1000_2norm": float(out["2-norm"][-1])}
    print(f"   SUP over [0,1000]: 2-norm {res['sup_log10_w_2norm']:.2f} at t = {res['t_of_sup']:.1f};"
          f"  Frobenius {res['sup_log10_w_frobenius']:.2f}")
    return res


def main():
    rec = RunRecorder("t4_amplification_profile", ROOT)
    rows = [profile("B215 (rational p)", 0.5, 0.5, 1.0, 0.8, 0.85, [2.77, 0.467]),
            profile("W1", 0.3, 1.0, 1.0, 0.8, 0.85, [2.4372, 2.012])]
    rec.add("rows", rows)
    rec.add("evidence_class", "NUMERICAL EXPLORATION")
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
