#!/usr/bin/env python3
r"""TASK-0005 Stage A + E — sign-aware amplification of the discrete linearized operator.

For each candidate: graded mesh on [0, T], PL collocation xhat, A_j = Dg(xhat_j),
adapted similarity S (|u|_S = |S^{-1} u|_2).  With L_h = I - I^alpha[A .] discretised
by hat-function weights:

  (A1) state amplification   amp_state(n) = sum_j ||R_{n,j}||   (e_n = sum_j R_{n,j} d_j)
       sampled over n, supremum reported;
  (A2) initial-condition sensitivity  sup_n |e_n|  for a unit defect on cell 0;
  (E1) functional amplification to M_T:
       delta M_T <= sup_{t>=T} sum_j || (ell_t L_h^{-1})_j || * |d_j|,
       ell_t(e) = sum_j omega_j(t) Psi_J(t - t_j) DN(u_j) e_j
       (PL quadrature of int_0^T Psi_J(t-s) DN(u(s)) e(s) ds, in adapted coordinates);
  (Y)  the linear prediction of the error from the actual sampled defect, both for
       the state and for M_T.

Comparison columns: TASK-0004 Theorem-R amplification (norm-based) from the profile
study, and the M1 threshold.  Evidence class: NUMERICAL EXPLORATION (Stage-I surrogate).
"""
import argparse
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from math import gamma

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.aposteriori import collocation, graded_mesh, xhat_eval        # noqa: E402
from msbg.memory_tail import psi_scalar                                 # noqa: E402
from msbg.models import AlleePredatorPrey                               # noqa: E402
from msbg.orbit_linearized import OrbitLinearized, _F0, _F1             # noqa: E402
from msbg.provenance import RunRecorder                                 # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CANDS = {
    "W1":   dict(theta=0.3, a=1.0, b=1.0, m=0.8, alpha=0.85, p=[2.4372, 2.012]),
    "B54":  dict(theta=0.5, a=1.0, b=1.0, m=0.8, alpha=0.75, p=[1.554, 0.3344]),
    "B75":  dict(theta=0.5, a=2.0, b=1.0, m=0.8, alpha=0.75, p=[1.59, 0.1693]),
    "B215": dict(theta=0.5, a=0.5, b=1.0, m=0.8, alpha=0.85, p=[2.77, 0.467]),
    "B180": dict(theta=0.5, a=0.5, b=1.0, m=0.8, alpha=0.85, p=[2.5, 0.585]),
    "B154": dict(theta=0.5, a=0.5, b=1.0, m=0.8, alpha=0.85, p=[2.32, 1.016]),
    "B15":  dict(theta=0.4, a=1.0, b=1.0, m=0.7, alpha=0.75, p=[1.1016, 0.3219]),
    "B3":   dict(theta=0.2, a=1.0, b=1.0, m=0.4, alpha=0.75, p=[0.8821, 0.3983]),
}


def hat_row_at(tm, t, alpha, n_hist):
    """omega_j(t) = (1/Gamma(a)) int_0^{t_{n_hist}} (t-s)^{a-1} phi_j(s) ds  for t >= t_{n_hist}."""
    _F0.alpha = alpha
    j = np.arange(0, n_hist + 1)
    w = np.zeros(n_hist + 1)
    jr = j[1:]
    w[1:] += _F1(tm[jr - 1], tm[jr], t) / (tm[jr] - tm[jr - 1])
    jf = j[:-1]
    w[:-1] += _F0(tm[jf], tm[jf + 1], t) - _F1(tm[jf], tm[jf + 1], t) / (tm[jf + 1] - tm[jf])
    return w / gamma(alpha)


def one(job):
    np.seterr(all="ignore")
    label, c, T, N, grade = job
    model = AlleePredatorPrey(theta=c["theta"], a=c["a"], b=c["b"], m=c["m"])
    al = c["alpha"]
    E = np.array([model.x_star, model.y_star])
    J = model.jac(E[None, :])[0]
    lam, V = np.linalg.eig(J)
    k = int(np.argmax(lam.imag))
    l, v = lam[k], V[:, k]
    S = np.column_stack([v.real, -v.imag])
    Si = np.linalg.inv(S)
    tm = graded_mesh(T, N, grade)
    X, PHI, M = collocation(model, np.array(c["p"]), al, tm)
    A = model.jac(X)
    # sampled cell defect (float) as in the TASK-0002 prototype
    R = np.zeros(N)
    for n in range(N):
        ts = tm[n] + np.linspace(0, 1, 6)[1:-1] * (tm[n + 1] - tm[n])
        xs = xhat_eval(ts, tm, PHI[0], M, np.array(c["p"]), al)
        phis = PHI[n] + (ts - tm[n])[:, None] * M[n][None, :]
        R[n] = np.max(np.linalg.norm((phis - model.g(xs)) @ Si.T, axis=1))
    Rn = np.concatenate([R, [R[-1]]])              # nodal defect proxy
    out = {"label": label, "T": T, "N": N, "R_max": float(R.max()),
           "R_at": {"t<1": float(R[tm[:-1] < 1].max()), "1<t<60": float(R[(tm[:-1] >= 1) & (tm[:-1] < 60)].max()),
                    "t>60": float(R[tm[:-1] >= 60].max())}}
    for name, Sm in (("adapted", S), ("maxnorm", None)):
        L = OrbitLinearized(tm, A, al, S=Sm)
        # (A1) state amplification sampled in n
        samples = np.unique(np.concatenate([np.searchsorted(tm, np.geomspace(0.01, T, 40)), [N]]))
        amp, yl = [], []
        for n in samples:
            rn = L.row_block_norms(int(n))
            amp.append(float(rn.sum()))
            yl.append(float(np.dot(rn, Rn)))
        amp = np.array(amp)
        yl = np.array(yl)
        # (A2) sensitivity to a unit defect on cell 0
        d0 = np.zeros((N + 1, 2)); d0[0, 0] = 1.0
        e0 = L.solve(d0)
        sens = float(np.max(np.linalg.norm(e0, axis=1)))
        res = {"sup_amp_state": float(amp.max()), "t_of_sup": float(tm[samples[int(amp.argmax())]]),
               "amp_at_T": float(amp[-1]), "Y_state_linear": float(yl.max()),
               "sensitivity_cell0": sens}
        # (E1) functional amplification to M_T, adapted coordinates only
        if Sm is not None:
            u = X - E
            DN = np.zeros((N + 1, 2, 2))
            c2 = 3 * model.x_star - 1 - c["theta"]
            DN[:, 0, 0] = -2 * c2 * u[:, 0] - c["a"] * u[:, 1] - 3 * u[:, 0] ** 2
            DN[:, 0, 1] = -c["a"] * u[:, 0]
            DN[:, 1, 0] = c["b"] * u[:, 1]
            DN[:, 1, 1] = c["b"] * u[:, 0]
            DNa = np.einsum("ij,njk,kl->nil", Si, DN, S)
            fam, fy = [], []
            # psi_lambda on a log grid (arbitrary precision), interpolated in log|psi| and
            # phase: 30000 direct evaluations at |z| ~ 250 cost hours; 400 cost seconds.
            sg = np.geomspace(1e-6, 3.2 * T, 400)
            pg = np.array([complex(psi_scalar(al, complex(l), float(s), dps=14)) for s in sg])
            lg_abs = np.log(np.abs(pg))
            ph = np.unwrap(np.angle(pg))
            for tt in (T, 1.02 * T, 1.1 * T, 1.5 * T, 3.0 * T):
                om = hat_row_at(tm, tt, al, N)
                sig = np.clip(tt - tm, sg[0], sg[-1])
                psi = np.exp(np.interp(np.log(sig), np.log(sg), lg_abs)) * np.exp(
                    1j * np.interp(np.log(sig), np.log(sg), ph))
                Rpsi = np.stack([np.stack([psi.real, -psi.imag], -1), np.stack([psi.imag, psi.real], -1)], -2)
                ell = om[:, None, None] * np.einsum("nij,njk->nik", Rpsi, DNa)
                dual = L.functional_dual(ell)
                fam.append(float(dual.sum()))
                fy.append(float(np.dot(dual, Rn)))
            res.update({"functional_amp_sup": float(max(fam)), "functional_amp_by_t": fam,
                        "Y_MT_linear": float(max(fy)),
                        "M1_threshold": None})
        out[name] = res
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, default=1000.0)
    ap.add_argument("--N", type=int, default=6000)
    ap.add_argument("--grade", type=float, default=3.0)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    jobs = [(k, v, args.T, args.N, args.grade) for k, v in CANDS.items()]
    rec = RunRecorder("t5_stageA", ROOT)
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        rows = list(ex.map(one, jobs))
    prof = {"W1": 15.8, "B215": 6.7, "B54": 6.0, "B75": 6.0, "B180": 6.0, "B154": 5.4, "B15": 6.8}
    print(f"{'cand':>5}{'R_max':>10}{'sup amp(S)':>12}{'at t':>7}{'amp(T)':>10}{'sens0':>8}"
          f"{'Y_state':>10}{'func amp':>10}{'Y_MT':>10}{'ThmR log10':>11}")
    for r in rows:
        a = r["adapted"]
        print(f"{r['label']:>5}{r['R_max']:10.2e}{a['sup_amp_state']:12.3e}{a['t_of_sup']:7.1f}"
              f"{a['amp_at_T']:10.3e}{a['sensitivity_cell0']:8.3f}{a['Y_state_linear']:10.2e}"
              f"{a['functional_amp_sup']:10.3e}{a['Y_MT_linear']:10.2e}{prof.get(r['label'], float('nan')):11.1f}")
    print("\nmax-norm state amplification:",
          {r["label"]: f"{r['maxnorm']['sup_amp_state']:.2e}" for r in rows})
    rec.add("rows", rows)
    rec.add("evidence_class", "NUMERICAL EXPLORATION (Stage-I amplification surrogate)")
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
