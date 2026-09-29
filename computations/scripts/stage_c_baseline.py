#!/usr/bin/env python3
r"""TASK-0001 Stage C — Double-Allee baseline.

STOP CONDITION TRIGGERED FOR THE REQUESTED SOURCE
-------------------------------------------------
Stage C of the task asks for a reproduction of one published fractional
Double-Allee multistable model, "preferably Mondal et al. (2025), using
parameter values traceable to the paper/local bibliography", and states:

    "If exact equations/parameters cannot be recovered from the locally
     available sources, stop Stage C and report the missing information rather
     than guessing."

Everything this repository contains about Mondal, R.; Pal, D.; Takeuchi, Y.;
Mukherjee, D.; Kesh, D.; Saha, A. (2025), *Dynamics of a Fractional Order
Predator-Prey System with Double Allee Effect and Group Defense*, Chinese
Journal of Physics 98, 613-632, DOI 10.1016/j.cjph.2025.09.020, is:

  * the bibliography entry ``MondalEtAl2025DoubleAlleeFractional``;
  * one-line role descriptions in research/REFERENCES.md, research/LITERATURE_MAP.md,
    research/INHERITED_KNOWLEDGE.md, research/NOVELTY_MATRIX.md and
    research/source/*.

No equations, no functional forms (the group-defense response is not even
specified), and no parameter values.  The same holds for Rahmi et al. (2021),
Pal & Saha (2015) and Contreras Julio & Aguirre (2018).  The Compute Agent is
repository-isolated and is not the literature-retrieval agent, so Stage C as
literally specified is **HALTED** and the missing information is itemised in the
return report.

WHAT IS DELIVERED INSTEAD (labelled, not substituted silently)
--------------------------------------------------------------
A baseline on a *project-constructed* positive planar strong-Allee Caputo
predator-prey system whose prey growth term is exactly the published Area-Nieto
(2023) cubic recorded in research/CLAIMS.md, plus the standard Lotka-Volterra
predation pair, and its double-Allee variant.  This keeps Stage D on the critical
path while making the provenance gap explicit.  Everything Stage C was supposed
to certify about the baseline is still done here:

  C1  equilibria in exact rational/symbolic arithmetic;
  C2  Jacobian eigenvalues and the Caputo local-stability sector test
      |arg lambda| > alpha pi / 2, symbolically where possible;
  C3  positivity of the positive cone along tested trajectories;
  C4  at least two long-run outcome classes;
  C5  two-solver (in fact three-solver) cross-check;
  C6  mesh and horizon sensitivity;
  C7  raw machine-readable data.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.basins import Outcome, classify, positivity_report      # noqa: E402
from msbg.models import AlleePredatorPrey, DoubleAlleePredatorPrey  # noqa: E402
from msbg.provenance import RunRecorder, set_seed                 # noqa: E402
from msbg.solvers import METHODS, solve                           # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MISSING_INFORMATION = [
    "Mondal et al. (2025) DOI 10.1016/j.cjph.2025.09.020: the state equations, "
    "including the explicit double-Allee factor and the group-defence functional response.",
    "Mondal et al. (2025): the parameter values (and which figure/table they belong to) "
    "for the multistable regime whose basins the paper computes.",
    "Mondal et al. (2025): the fractional orders used, commensurate and incommensurate, "
    "for that regime.",
    "Mondal et al. (2025): the coordinates of the attractors reported in the multistable regime, "
    "so that a reproduction can be checked rather than asserted.",
    "Fallback sources with the same gap: Rahmi et al. (2021) Fractal Fract. 5(3) 84; "
    "Pal & Saha (2015); Contreras Julio & Aguirre (2018) - equations/parameters not stored locally.",
]


def c1_c2_symbolic(theta_v, a_v, b_v, m_v, alphas):
    """Exact equilibria and Caputo sector test.

    ``x`` and ``y`` are declared real (not positive), so the three boundary
    equilibria (0,0), (theta,0) and (1,0) are returned alongside the interior
    coexistence point.  Declaring them positive silently drops every equilibrium
    on an axis, including the extinction state, which is the one the whole task
    is about.
    """
    x, y = sp.symbols("x y", real=True)
    th, a, b, m = sp.symbols("theta a b m", positive=True)
    gx = x * (1 - x) * (x - th) - a * x * y
    gy = y * (b * x - m)
    sub = {th: sp.Rational(str(theta_v)), a: sp.Rational(str(a_v)),
           b: sp.Rational(str(b_v)), m: sp.Rational(str(m_v))}
    sols = sp.solve([sp.Eq(gx.subs(sub), 0), sp.Eq(gy.subs(sub), 0)], [x, y], dict=True)
    J = sp.Matrix([[sp.diff(gx, x), sp.diff(gx, y)], [sp.diff(gy, x), sp.diff(gy, y)]]).subs(sub)
    out = []
    for s in sols:
        xv, yv = s.get(x, sp.Integer(0)), s.get(y, sp.Integer(0))
        if xv.is_negative or yv.is_negative:
            continue
        Je = sp.simplify(J.subs({x: xv, y: yv}))
        ev = [sp.nsimplify(e) for e in Je.eigenvals().keys()]
        evn = [complex(sp.N(e, 30)) for e in ev]
        rec = {
            "equilibrium_exact": [str(sp.nsimplify(xv)), str(sp.nsimplify(yv))],
            "equilibrium_float": [float(sp.N(xv)), float(sp.N(yv))],
            "jacobian_exact": [[str(Je[i, j]) for j in range(2)] for i in range(2)],
            "eigenvalues_exact": [str(e) for e in ev],
            "eigenvalues_float": [[e.real, e.imag] for e in evn],
            "trace_exact": str(sp.nsimplify(Je.trace())),
            "det_exact": str(sp.nsimplify(Je.det())),
        }
        # Caputo local asymptotic stability: all eigenvalues in |arg lambda| > alpha pi/2
        rec["stable_for_alpha"] = {}
        for al in alphas:
            need = al * np.pi / 2
            args = [abs(np.angle(e)) for e in evn]
            rec["stable_for_alpha"][str(al)] = bool(all(t > need + 1e-12 for t in args))
        rec["min_abs_arg"] = float(min(abs(np.angle(e)) for e in evn))
        rec["alpha_stability_bound"] = float(2 * min(abs(np.angle(e)) for e in evn) / np.pi)
        out.append(rec)
    return out


def main():
    set_seed()
    np.seterr(all="ignore")
    rec = RunRecorder("stage_c", ROOT)
    rec.add("stage_c_as_specified", "HALTED")
    rec.add("halt_reason",
            "Mondal et al. (2025) equations and parameters are not recoverable from this "
            "repository; task stop rule forbids guessing them.")
    rec.add("missing_information", MISSING_INFORMATION)
    print("Stage C as specified (Mondal et al. 2025): HALTED — missing information:")
    for it in MISSING_INFORMATION:
        print("  -", it)

    alphas = [0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 0.99]
    for tag, (theta_v, a_v, b_v, m_v) in {
        "baseline_th0.2_a1_m0.7": (0.2, 1.0, 1.0, 0.7),
        "witness_th0.2_a2_m0.8": (0.2, 2.0, 1.0, 0.8),
        "witness_th0.3_a1_m0.75": (0.3, 1.0, 1.0, 0.75),
        "witness_th0.4_a1_m0.8": (0.4, 1.0, 1.0, 0.8),
    }.items():
        print(f"\nC1/C2 exact equilibria + Caputo sector test [{tag}]")
        eqs = c1_c2_symbolic(theta_v, a_v, b_v, m_v, alphas)
        for e in eqs:
            print(f"    E={e['equilibrium_exact']} eigs={e['eigenvalues_exact']} "
                  f"Caputo-stable for alpha < {e['alpha_stability_bound']:.4f}")
        rec.add(f"C1_C2_{tag}", eqs)

    model = AlleePredatorPrey(theta=0.2, a=2.0, b=1.0, m=0.8)
    E = np.array([model.x_star, model.y_star])
    print(f"\nsurvival attractor of the Stage-D regime: E* = {E}")

    # ---- C3/C4/C5: outcome classes and three-solver cross-check ------------
    X0 = np.array([[0.10, 0.10],     # inside the certified extinction region
                   [0.50, 2.50],     # predator-driven collapse
                   [1.00, 0.30],     # coexistence
                   [1.45, 0.75],     # the Stage-D witness candidate
                   [2.50, 0.10]])
    T, N = 800.0, 8000
    cross = {}
    for method in METHODS:
        r = solve(model, X0, 0.9, T / N, N, method=method, store=True, store_stride=4)
        lab = classify(r.x, E, r_coex=0.05, r_ext=0.05)
        pr = positivity_report(r.x)
        cross[method] = {
            "labels": [Outcome.NAMES[int(v)] for v in lab],
            "x_final": r.x_final.tolist(),
            "min_x": pr.min_x, "min_y": pr.min_y, "n_traj_negative": pr.n_negative,
            "newton_failures": r.newton_failures,
        }
        print(f"C3/C4/C5 {method:8} labels={cross[method]['labels']} "
              f"min(x,y)=({pr.min_x:.3e},{pr.min_y:.3e})")
    rec.add("C3_C4_C5_cross_solver", cross)
    agree = len({tuple(v["labels"]) for v in cross.values()}) == 1
    rec.add("C5_all_three_solvers_agree_on_labels", agree)
    print(f"    all three solvers agree on labels: {agree}")

    # ---- C6: mesh and horizon sensitivity ---------------------------------
    mesh = []
    for N2 in (2000, 4000, 8000, 16000, 32000):
        r = solve(model, X0, 0.9, T / N2, N2, method="pece", store=False)
        mesh.append({"N": N2, "h": T / N2, "x_final": r.x_final.tolist()})
    ref = np.array(mesh[-1]["x_final"])
    for m in mesh:
        m["max_abs_diff_vs_finest"] = float(np.max(np.abs(np.array(m["x_final"]) - ref)))
        print(f"C6 mesh   N={m['N']:6d} max|diff vs finest| = {m['max_abs_diff_vs_finest']:.3e}")
    rec.save_json("C6_mesh_sensitivity", mesh)

    hor = []
    for T2 in (200.0, 400.0, 800.0, 1600.0, 3200.0):
        N2 = int(T2 / 0.1)
        r = solve(model, X0, 0.9, T2 / N2, N2, method="pece", store=True, store_stride=8)
        lab = classify(r.x, E, r_coex=0.05, r_ext=0.05)
        hor.append({"T": T2, "N": N2, "labels": [Outcome.NAMES[int(v)] for v in lab],
                    "x_final": r.x_final.tolist()})
        print(f"C6 horizon T={T2:7.1f} labels={hor[-1]['labels']}")
    rec.save_json("C6_horizon_sensitivity", hor)
    stable = len({tuple(h["labels"]) for h in hor if h["T"] >= 800.0}) == 1
    rec.add("C6_labels_stable_for_T_ge_800", stable)

    # ---- double-Allee variant ---------------------------------------------
    dmodel = DoubleAlleePredatorPrey(theta=0.2, c=0.5, a=2.0, b=1.0, m=0.8)
    Ed = np.array([dmodel.x_star, dmodel.y_star])
    rd = solve(dmodel, X0, 0.9, T / N, N, method="pece", store=True, store_stride=4)
    labd = classify(rd.x, Ed, r_coex=0.05, r_ext=0.05)
    rec.add("double_allee_variant", {
        "equilibrium": Ed.tolist(),
        "labels": [Outcome.NAMES[int(v)] for v in labd],
        "provenance": dmodel.provenance,
    })
    print(f"\ndouble-Allee variant E*={Ed}  labels={[Outcome.NAMES[int(v)] for v in labd]}")

    rec.add("provenance_single", model.provenance)
    rec.add("provenance_double", dmodel.provenance)
    rec.add("evidence_class",
            "C1/C2 exact symbolic (CERTIFIED by exact rational arithmetic); "
            "C3-C6 NUMERICAL CORROBORATION. Stage C as specified is HALTED.")
    print("\nmanifest:", rec.finish())


if __name__ == "__main__":
    main()
