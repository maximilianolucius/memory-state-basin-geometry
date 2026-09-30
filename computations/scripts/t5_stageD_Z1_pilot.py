#!/usr/bin/env python3
r"""TASK-0005 Stage D — the operator-tail term Z1, made explicit and estimated.

SOURCE FORMULATION.  Write the error as  e = I^alpha[f]  with source f.  The exact
fixed point for the source is
    f = G(f) := g(xhat + I^alpha f) - g(xhat) - rho = K f + R(I^alpha f) - rho,
    (K f)(t) = A(t) (I^alpha f)(t),   A = Dg(xhat).
The collocation solution has f_hat = 0 (rho vanishes at the nodes), and the natural
approximate inverse on C([0,T]) is
    B := L_h^{-1} pi + (I - pi),      pi = piecewise-linear nodal interpolation,
    L_h = I - A W  (nodal, W = hat-function weights).
Then, exactly,
    I - B (I - K) = L_h^{-1} pi K (I - pi) + (I - pi) K .                       (*)
Both terms vanish on piecewise-linear f and are controlled by the OSCILLATION of f
on the cells, not by its size.  In the plain sup norm they are not small: for a
general bounded f, |(I - pi) f| can equal 2|f| on every cell, and
|I^alpha[(I-pi) f](t)| can reach 2|f| t^alpha / Gamma(alpha+1) ~ 750|f| at t = 1000.
So the radii argument must live in a space that bounds cell oscillations.

PILOT ASSUMPTION (explicit).  f ranges over  { |f|_inf <= 1,  osc_n(f) <= theta_n }
with the oscillation profile theta_n taken from the computed source phi itself
(theta_n = osc_n(phi)/|phi|_inf).  Under that assumption the two terms of (*) are
bounded cellwise by
    T1_n = sum_k ||R_{n,k}|| ||A_k|| sum_j W_{k,j} theta_j ,
    T2_n = ||A_n|| 2 h_n^alpha / Gamma(alpha+1) + osc_n(A) t_{n+1}^alpha / Gamma(alpha+1),
and Z1 <= max_n (T1_n + T2_n).  T2 also needs the Hölder-alpha modulus of I^alpha f,
which is the standard 2 h^alpha |f|_inf / Gamma(alpha+1).

This is a pilot: it says whether Z1 can plausibly fit the budget, and which term
dominates.  It is not a theorem.  ROUND-0006 owns the functional setting.
"""
import argparse
import os
import sys
from math import gamma

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.aposteriori import collocation, graded_mesh                    # noqa: E402
from msbg.models import AlleePredatorPrey                               # noqa: E402
from msbg.orbit_linearized import hat_weights                           # noqa: E402
from msbg.provenance import RunRecorder                                 # noqa: E402
from msbg.validated_res import Setup                                    # noqa: E402
from scripts.t5_stageD_radii_pilot import dense_inverse                 # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cand", default="W1")
    ap.add_argument("--T", type=float, default=1000.0)
    ap.add_argument("--N", type=int, default=6000)
    args = ap.parse_args()
    np.seterr(all="ignore")
    specs = {"W1": ("3/10", "1", "1", "4/5", "17/20", ("6093/2500", "503/250")),
             "B215": ("1/2", "1/2", "1", "4/5", "17/20", ("277/100", "467/1000"))}
    st = Setup(*specs[args.cand])
    fl, pf = st.floats()
    al = fl["alpha"]
    model = AlleePredatorPrey(theta=fl["theta"], a=fl["a"], b=fl["b"], m=fl["m"])
    tm = graded_mesh(args.T, args.N, 3.0)
    N = args.N
    X, PHI, M = collocation(model, np.array(pf), al, tm)
    S = np.array([[float(v.mid()) for v in row] for row in st.S_arb])
    Si = np.linalg.inv(S)
    A = np.einsum("ij,njk,kl->nil", Si, model.jac(X), S)
    An = np.linalg.norm(A, ord=2, axis=(1, 2))
    W = hat_weights(tm, al)
    R = dense_inverse(W, A)
    Rn = np.sqrt(np.einsum("nikl->nk", R * R))
    h = np.diff(tm)
    # oscillation profile of the computed source (adapted coordinates)
    phi_a = PHI @ Si.T
    osc_phi = np.linalg.norm(np.diff(phi_a, axis=0), axis=1)
    theta = np.concatenate([osc_phi, [osc_phi[-1]]]) / np.max(np.linalg.norm(phi_a, axis=1))
    # T1: L_h^{-1} pi K (I - pi) f  with |(I-pi)f| <= theta on each cell
    inner = An * (W @ theta)                       # ||A_k|| sum_j W_kj theta_j
    T1 = Rn @ inner
    # T2: (I - pi) K f : oscillation of A(t) (I^a f)(t) on cell n
    oscA = np.linalg.norm(np.diff(A, axis=0), ord=2, axis=(1, 2))
    Ia_sup = np.concatenate([[0.0], tm[1:] ** al]) / gamma(al + 1)     # |I^a f| <= t^a/Gamma(a+1)
    T2 = np.concatenate([An[:-1] * 2 * h**al / gamma(al + 1) + oscA * Ia_sup[1:], [0.0]])
    Z1 = T1 + T2
    k = int(np.argmax(Z1))
    print(f"{args.cand}: pilot Z1 <= {Z1.max():.4f} at t = {tm[k]:.2f}  "
          f"(T1 = {T1[k]:.4f}, T2 = {T2[k]:.4f});  max T1 = {T1.max():.4f} at t = {tm[int(T1.argmax())]:.2f}, "
          f"max T2 = {T2.max():.4f} at t = {tm[int(T2.argmax())]:.2f}")
    print(f"   oscillation profile: max theta_n = {theta.max():.3e} at t = {tm[int(theta.argmax())]:.3e}, "
          f"median {np.median(theta):.2e};  h_max = {h.max():.3f}")
    # what the profile would need to be: scale theta until Z1 hits 0.5
    sc = 0.5 / max(T1.max(), 1e-300)
    print(f"   T1 alone reaches 0.5 if the oscillation profile is scaled by {sc:.2f}; "
          f"T2 alone = {T2.max():.4f} (mesh-only term)")
    rec = RunRecorder(f"t5_Z1pilot_{args.cand}", ROOT)
    rec.add("result", {"Z1_pilot": float(Z1.max()), "t": float(tm[k]), "T1_max": float(T1.max()),
                       "T2_max": float(T2.max()), "theta_max": float(theta.max()),
                       "assumption": "f in {|f|<=1, osc_n f <= theta_n}, theta from the computed source"})
    rec.add("evidence_class", "PILOT under an explicit, unproved assumption on the function class")
    rec.save_npz("arrays", tm=tm, T1=T1, T2=T2, theta=theta)
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
