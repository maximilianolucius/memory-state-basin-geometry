#!/usr/bin/env python3
r"""TASK-0004 Stage C — can the TASK-0002 verifier reach a useful cut time T?

The TASK-0002 a posteriori bound is  U = (I - V_L)^{-1} Delta,  where V_L is the
Volterra operator with kernel (t-s)^{alpha-1} Lbar(s) / Gamma(alpha) and
Lbar(s) >= ||Dg|| on the tube.  Its amplification factor

    A(T) := sup_{t <= T} [ (I - V_L)^{-1} 1 ](t)

is what the defect has to beat: the verifier certifies only if
(defect bound) x A(T) < tube radius.  A(T) uses |Dg| with no sign information.

Two variants are compared:
  (G)  the verifier's kernel  (t-s)^{alpha-1}/Gamma(alpha)  with Lbar = ||Dg(xhat)||;
  (R)  a J-resolvent kernel  ||Psi_J(t-s)||  with coefficient ||Dg(xhat(s)) - J||,
       i.e. the error equation rewritten around the linearisation at E*.

Evidence class: NUMERICAL EXPLORATION (float; decides which rigorous method is worth building).
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


def main():
    np.seterr(all="ignore")
    al, h, Tmax = 0.85, 0.02, 1000.0
    model = AlleePredatorPrey(theta=0.3, a=1.0, b=1.0, m=0.8)
    J = np.array([[-6 / 25, -4 / 5], [1 / 10, 0.0]])
    N = int(round(Tmax / h))
    r = solve(model, [[2.4372, 2.012]], al, h, N, method="pece", store=True)
    x, t = r.x[:, 0, :], r.t
    Dg = model.jac(x)
    L = np.abs(Dg).sum(2).max(1)
    a_res = np.abs(Dg - J[None]).sum(2).max(1)
    # (G) power kernel
    b = (np.arange(N + 1) + 1.0) ** al - np.arange(N + 1) ** al
    c = h**al / gamma(al + 1)
    logA = np.zeros(N + 1)             # work with a rescaled recursion to avoid overflow
    u = np.ones(N + 1)
    scale = 0.0
    out_G = {}
    marks = [4, 10, 20, 36, 60, 100, 200, 500, 1000]
    for n in range(1, N + 1):
        u[n] = np.exp(-scale) + c * np.dot(b[n - 1::-1], L[:n] * u[:n])
        if u[n] > 1e100:
            u[: n + 1] /= 1e100
            scale += np.log(1e100)
        for T in marks:
            if n == int(round(T / h)):
                out_G[T] = float(np.log10(u[n]) + scale / np.log(10))
    # (R) J-resolvent kernel: ||Psi_J(s)||_inf on the grid (cell averages via psi at midpoints)
    lam = np.linalg.eigvals(J)
    lam = lam[np.argmax(lam.imag)]
    V = np.linalg.eig(J)[1][:, np.argmax(np.linalg.eigvals(J).imag)]
    S = np.column_stack([V.real, -V.imag])
    Si = np.linalg.inv(S)
    smid = (np.arange(N) + 0.5) * h
    # psi on a log grid, interpolated
    sg = np.geomspace(smid[0], smid[-1], 500)
    pg = np.array([complex(psi_scalar(al, complex(lam), float(s), dps=18)) for s in sg])
    nrm = np.empty(len(sg))
    for i, p in enumerate(pg):
        R = np.array([[p.real, -p.imag], [p.imag, p.real]])
        nrm[i] = np.max(np.abs(S @ R @ Si).sum(1))
    kern = np.exp(np.interp(np.log(smid), np.log(sg), np.log(nrm))) * h
    kern[0] = h**al / gamma(al + 1)     # integrable singularity of the first cell
    u2 = np.ones(N + 1)
    scale2 = 0.0
    out_R = {}
    for n in range(1, N + 1):
        u2[n] = np.exp(-scale2) + np.dot(kern[n - 1::-1], a_res[:n] * u2[:n])
        if u2[n] > 1e100:
            u2[: n + 1] /= 1e100
            scale2 += np.log(1e100)
        for T in marks:
            if n == int(round(T / h)):
                out_R[T] = float(np.log10(u2[n]) + scale2 / np.log(10))
    print(f"{'T':>6}{'x(T)':>10}{'||Dg||':>9}{'||Dg-J||':>10}{'log10 A_G(T)':>14}{'log10 A_R(T)':>14}")
    for T in marks:
        n = int(round(T / h))
        print(f"{T:6d}{x[n,0]:10.4f}{L[n]:9.3f}{a_res[n]:10.4f}{out_G[T]:14.2f}{out_R[T]:14.2f}")
    rec = RunRecorder("t4_stageC_amplification", ROOT)
    rec.add("log10_amplification_power_kernel", out_G)
    rec.add("log10_amplification_J_resolvent_kernel", out_R)
    rec.add("note", "TASK-0002 certified W1 at T=4 (A ~ 10^3.6) and B2 at T=36 with L ~ 1.1")
    rec.add("evidence_class", "NUMERICAL EXPLORATION")
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
