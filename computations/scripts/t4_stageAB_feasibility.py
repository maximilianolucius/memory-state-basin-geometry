#!/usr/bin/env python3
r"""TASK-0004 Stage A/B — numerical feasibility of CANDIDATE M1 for the witness W1.

Stage B (done first, because everything else leans on it).  For each cut time T,
    z := v_T + Psi_J * N(u)
is computed WITHOUT forming Psi_J, as the solution of the linear Volterra equation
z = h_T + I_T^alpha[ J z + N(u) ] with N(u) taken from the full-history orbit.
The variation-of-constants identity says z = u.  The defect  sup |z - u|  is
reported for two step sizes; it must shrink at the mesh convergence order.

Stage A.  h_T, v_T = L_J h_T, M_T = sup_{T <= t <= T_end} ||v_T||, K_J and the best
radius for  M_T + K_J C_r r^2 < r,  in
  * the Euclidean norm,
  * diagonal weighted max-norms (weight ratio optimised),
  * the eigenvector-adapted norm |xi|_2, u = S xi, J S = S [[mu,-nu],[nu,mu]],
    in which ||Psi_J(s)|| = |psi_lambda(s)| exactly, so K_J is a scalar integral.

M_T is a supremum over a FINITE window [T, T_end]; the statement on [T_end, inf)
is not covered numerically.

Evidence class: NUMERICAL EXPLORATION.
"""
from __future__ import annotations

import argparse
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from math import gamma

import mpmath as mp
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.memory_tail import inherited_input, linear_volterra, psi_scalar   # noqa: E402
from msbg.models import AlleePredatorPrey                                   # noqa: E402
from msbg.provenance import RunRecorder                                     # noqa: E402
from msbg.solvers import solve                                              # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TH, A_, B_, M_, AL = 0.3, 1.0, 1.0, 0.8, 0.85          # binary64 images of 3/10,1,1,4/5,17/20
P0 = np.array([2.4372, 2.012])
E = np.array([0.8, 0.1])
J = np.array([[-6 / 25, -4 / 5], [1 / 10, 0.0]])
C2 = 3 * 0.8 - 1 - 0.3


def N_of(u):
    u1, u2 = u[:, 0], u[:, 1]
    return np.stack([-C2 * u1**2 - A_ * u1 * u2 - u1**3, B_ * u1 * u2], axis=1)


def orbit(job):
    np.seterr(all="ignore")
    method, h, T_end = job
    model = AlleePredatorPrey(theta=TH, a=A_, b=B_, m=M_)
    N = int(round(T_end / h))
    r = solve(model, P0[None, :], AL, h, N, method=method, store=True)
    return method, h, r.t, r.x[:, 0, :]


def adapted_basis():
    lam, V = np.linalg.eig(J)
    k = int(np.argmax(lam.imag))
    l, v = lam[k], V[:, k]
    S = np.column_stack([v.real, -v.imag])          # J S = S [[mu,-nu],[nu,mu]]
    return l, S


def kernel_norms(job):
    """||Psi_J(s)|| in the three norm families at one s (arbitrary precision psi)."""
    s, omegas = job
    lam, S = adapted_basis()
    psi = complex(psi_scalar(AL, complex(lam), s, dps=20))
    R = np.array([[psi.real, -psi.imag], [psi.imag, psi.real]])
    Psi = S @ R @ np.linalg.inv(S)
    eu = float(np.linalg.norm(Psi, 2))
    wm = [float(np.max((np.abs(Psi) @ np.array([1.0, om])) / np.array([1.0, om]))) for om in omegas]
    return s, abs(psi), eu, wm


def tail_job(job):
    np.seterr(all="ignore")
    tag, t, x, T, H, T_end = job
    h = t[1] - t[0]
    k = int(round(H / h))
    nT = int(round(T / h))
    model = AlleePredatorPrey(theta=TH, a=A_, b=B_, m=M_)
    F = model.g(x)
    idx = np.arange(nT, len(t), k)
    te = t[idx]
    hT = inherited_input(t, F, P0 - E, AL, nT, te)
    u = x[idx] - E
    zero = np.zeros_like(u)
    v = linear_volterra(hT, zero, J, AL, H)
    z = linear_volterra(hT, N_of(u), J, AL, H)
    lam, S = adapted_basis()
    Si = np.linalg.inv(S)
    xi = v @ Si.T
    return {"tag": tag, "T": T, "H": H, "h": h, "T_end": float(te[-1]),
            "identity_defect": float(np.max(np.abs(z - u))),
            "hT_at_T": hT[0].tolist(), "u_at_T": u[0].tolist(),
            "hT_minus_u_at_T": float(np.max(np.abs(hT[0] - u[0]))),
            "hT_end": hT[-1].tolist(),
            "sup_hT_inf": float(np.max(np.abs(hT))),
            "sup_u_inf": float(np.max(np.abs(u))),
            "v_minus_u_sup": float(np.max(np.abs(v - u))),
            "M_euclid": float(np.max(np.linalg.norm(v, axis=1))),
            "M_adapted": float(np.max(np.linalg.norm(xi, axis=1))),
            "v_abs_max": np.max(np.abs(v), axis=0).tolist(),
            "v_end": v[-1].tolist(),
            "t_of_sup_euclid": float(te[int(np.argmax(np.linalg.norm(v, axis=1)))]),
            "v_series_t": te[::max(1, len(te) // 400)].tolist(),
            "v_series": v[::max(1, len(te) // 400)].tolist()}


def best_radius(M, K, C0, c3):
    """min over r of  M + K (C0 + c3 r) r^2 - r ;  feasible iff negative."""
    rs = np.geomspace(1e-5, 1.0, 4000)
    f = M + K * (C0 + c3 * rs) * rs**2 - rs
    i = int(np.argmin(f))
    return float(f[i]), float(rs[i]), float(K * (C0 + c3 * rs[i]) * rs[i])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=60)
    ap.add_argument("--T-end", type=float, default=6000.0)
    args = ap.parse_args()
    rec = RunRecorder("t4_stageAB", ROOT)

    # ---------------- K_J ------------------------------------------------------
    omegas = np.geomspace(0.05, 5.0, 41)
    sgrid = np.concatenate([np.geomspace(1e-8, 1.0, 120), np.geomspace(1.0, 3000.0, 360)[1:]])
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        kr = list(ex.map(kernel_norms, [(float(s), omegas) for s in sgrid], chunksize=4))
    kr.sort(key=lambda r: r[0])
    s = np.array([r[0] for r in kr])
    lam, S = adapted_basis()
    Si = np.linalg.inv(S)
    Jinv2 = np.linalg.inv(J) @ np.linalg.inv(J)

    def integrate(vals, tail_norm):
        # log-grid trapezoid in the variable ln s, plus the analytic head and tail
        y_, x_ = vals * s, np.log(s)
        body = float(np.sum(0.5 * (y_[1:] + y_[:-1]) * np.diff(x_)))   # trapezoid in ln s
        head = vals[0] * s[0] / AL                       # psi ~ s^{alpha-1}/Gamma(alpha) near 0
        tail = tail_norm * s[-1] ** (-AL) / gamma(1 - AL)
        return body + head + tail, body, head, tail

    ad = np.array([r[1] for r in kr])
    eu = np.array([r[2] for r in kr])
    K_ad, *parts_ad = integrate(ad, abs(lam) ** -2)
    K_eu, *parts_eu = integrate(eu, float(np.linalg.norm(Jinv2, 2)))
    K_wm = []
    for j, om in enumerate(omegas):
        w = np.array([1.0, om])
        tn = float(np.max((np.abs(Jinv2) @ w) / w))
        K_wm.append(integrate(np.array([r[3][j] for r in kr]), tn)[0])
    asym = abs(lam) ** -2 * s[-1] ** (-AL - 1) / abs(gamma(-AL))
    print(f"eigenvalue lambda = {lam:.6f}, |arg| = {abs(np.angle(lam)):.4f} rad "
          f"(Matignon needs > {AL*np.pi/2:.4f})")
    print(f"K_J adapted  = {K_ad:.4f}  (body {parts_ad[0]:.4f}, head {parts_ad[1]:.2e}, "
          f"tail {parts_ad[2]:.4f});  lower bound |1/lambda| = {1/abs(lam):.4f}")
    print(f"K_J euclid   = {K_eu:.4f};  lower bound ||J^-1||_2 = "
          f"{np.linalg.norm(np.linalg.inv(J), 2):.4f}")
    print(f"K_J wmax     = min over omega {min(K_wm):.4f} at omega = "
          f"{omegas[int(np.argmin(K_wm))]:.3f}")
    print(f"asymptote check at s = {s[-1]:.0f}: |psi| = {ad[-1]:.4e}, "
          f"|lambda|^-2 s^(-a-1)/|Gamma(-a)| = {asym:.4e}, ratio {ad[-1]/asym:.4f}")

    # nonlinearity constants
    ang = np.linspace(0, 2 * np.pi, 3601)
    xi = np.stack([np.cos(ang), np.sin(ang)], axis=1)
    u = xi @ S.T
    N2 = np.stack([-C2 * u[:, 0] ** 2 - A_ * u[:, 0] * u[:, 1], B_ * u[:, 0] * u[:, 1]], axis=1)
    N3 = np.stack([-u[:, 0] ** 3, np.zeros(len(u))], axis=1)
    C0_ad = float(np.max(np.linalg.norm(N2 @ Si.T, axis=1)))
    c3_ad = float(np.max(np.linalg.norm(N3 @ Si.T, axis=1)))
    ue = xi
    N2e = np.stack([-C2 * ue[:, 0] ** 2 - A_ * ue[:, 0] * ue[:, 1], B_ * ue[:, 0] * ue[:, 1]], 1)
    C0_eu = float(np.max(np.linalg.norm(N2e, axis=1)))
    c3_eu = 1.0
    print(f"C_r adapted = {C0_ad:.4f} + {c3_ad:.4f} r ;  C_r euclid = {C0_eu:.4f} + r ; "
          f"cond(S) = {np.linalg.cond(S):.3f}")

    # ---------------- orbits and tails ------------------------------------------
    ojobs = [("pece", 0.02, args.T_end), ("pece", 0.01, args.T_end), ("pi_rect", 0.02, args.T_end)]
    with ProcessPoolExecutor(max_workers=3) as ex:
        orbits = list(ex.map(orbit, ojobs))
    print("orbits done", flush=True)
    Ts = [50.0, 100.0, 200.0, 500.0, 1000.0, 2000.0]
    tjobs = []
    for method, h, t, x in orbits:
        for T in Ts:
            for H in ((0.1, 0.2) if (method == "pece" and h == 0.02) else (0.1,)):
                tjobs.append((f"{method}_h{h}", t, x, T, H, args.T_end))
    with ProcessPoolExecutor(max_workers=min(args.workers, len(tjobs))) as ex:
        tails = list(ex.map(tail_job, tjobs))

    print(f"\nStage B: variation-of-constants identity  sup|v_T + Psi*N(u) - u|")
    print(f"{'T':>7}" + "".join(f"{k:>22}" for k in ("pece_h0.02 H=0.2", "pece_h0.02 H=0.1",
                                                     "pece_h0.01 H=0.1", "pi_rect_h0.02 H=0.1")))
    for T in Ts:
        def g(tag, H):
            return next(r["identity_defect"] for r in tails
                        if r["tag"] == tag and r["T"] == T and r["H"] == H)
        print(f"{T:7.0f}{g('pece_h0.02',0.2):22.3e}{g('pece_h0.02',0.1):22.3e}"
              f"{g('pece_h0.01',0.1):22.3e}{g('pi_rect_h0.02',0.1):22.3e}")

    print(f"\nStage A: M1 inequality  M_T + K_J C_r r^2 < r   (reference orbit pece h=0.01)")
    print(f"{'T':>7}{'|u(T)|inf':>11}{'sup|h_T|':>10}{'norm':>10}{'M_T':>11}{'K_J':>9}"
          f"{'min f(r)':>11}{'r*':>10}{'K C r*':>8}{'feasible':>9}")
    rows = []
    for T in Ts:
        r = next(q for q in tails if q["tag"] == "pece_h0.01" and q["T"] == T)
        spread = max(abs(q["M_euclid"] - r["M_euclid"]) for q in tails if q["T"] == T)
        # weighted max: optimise omega
        vmax = np.array(r["v_abs_max"])
        best_w = None
        for j, om in enumerate(omegas):
            Mw = max(vmax[0], vmax[1] / om)
            Cw0, c3w = max(abs(C2) + A_ * om, B_), 1.0
            f, rs, kc = best_radius(Mw, K_wm[j], Cw0, c3w)
            if best_w is None or f < best_w[0]:
                best_w = (f, rs, kc, Mw, K_wm[j], om)
        for name, M, K, C0, c3 in (("euclid", r["M_euclid"], K_eu, C0_eu, c3_eu),
                                   ("adapted", r["M_adapted"], K_ad, C0_ad, c3_ad)):
            f, rs, kc = best_radius(M, K, C0, c3)
            rows.append({"T": T, "norm": name, "M_T": M, "K_J": K, "C0": C0, "c3": c3,
                         "min_f": f, "r_star": rs, "KCr": kc, "feasible": bool(f < 0),
                         "M_spread_over_solvers": spread})
            print(f"{T:7.0f}{np.max(np.abs(r['u_at_T'])):11.3e}{r['sup_hT_inf']:10.3f}{name:>10}"
                  f"{M:11.3e}{K:9.3f}{f:11.3e}{rs:10.3e}{kc:8.3f}{str(f<0):>9}")
        f, rs, kc, Mw, Kw, om = best_w
        rows.append({"T": T, "norm": f"wmax(omega={om:.3f})", "M_T": Mw, "K_J": Kw,
                     "min_f": f, "r_star": rs, "KCr": kc, "feasible": bool(f < 0)})
        print(f"{T:7.0f}{'':11}{'':10}{'wmax':>10}{Mw:11.3e}{Kw:9.3f}{f:11.3e}{rs:10.3e}"
              f"{kc:8.3f}{str(f<0):>9}   omega={om:.3f}")
    rec.save_json("tails", tails)
    rec.save_json("feasibility", rows)
    rec.save_npz("kernel", s=s, psi_abs=ad, psi_euclid=eu, omegas=omegas, K_wmax=np.array(K_wm))
    rec.add("K_J", {"adapted": K_ad, "euclid": K_eu, "wmax_min": min(K_wm),
                    "adapted_parts_body_head_tail": parts_ad})
    rec.add("C_r", {"adapted": [C0_ad, c3_ad], "euclid": [C0_eu, c3_eu]})
    rec.add("T_end", args.T_end)
    rec.add("evidence_class", "NUMERICAL EXPLORATION")
    print("\nmanifest:", rec.finish())


if __name__ == "__main__":
    main()
