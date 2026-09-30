#!/usr/bin/env python
"""TASK-0007 D: compare the hardened T=300/N=12000 certificate (tag h7_T300_N12000) with the
TASK-0006 one (tag adaptT300_N12000), constant by constant.  Prints a Markdown table and
writes data/t7_comparison.json."""
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def P(name):
    with open(os.path.join(ROOT, "manifests", f"{name}_manifest.json")) as f:
        return json.load(f)["payload"]


def main():
    old, new = "adaptT300_N12000", sys.argv[1] if len(sys.argv) > 1 else "h7_T300_N12000"
    rows = []

    def add(label, a, b, fmt="{:.6g}"):
        try:
            rel = (b - a) / abs(a) if a else float("nan")
        except TypeError:
            rel = float("nan")
        rows.append((label, a, b, rel))

    bo, bn = P(f"t6_stageBD_{old}"), P(f"t6_stageBD_{new}")
    add("||E||_inf (Neumann residual)", bo["inverse"]["normE"], bn["inverse"]["normE"])
    add("max delta_n (inverse correction)", bo["inverse"]["delta_max"], bn["inverse"]["delta_max"])
    add("max_n sum_k ||R_nk|| (block row sum)", bo["inverse"]["rowsum_max"], bn["inverse"]["rowsum_max"])
    add("block row sum at T", bo["inverse"]["rowsum_T"], bn["inverse"]["rowsum_T"])
    add("Q row-sum max", bo["Q"]["rowsum_max"], bn["Q"]["rowsum_max"])
    add("rem row-sum max", bo["Q"]["rem_rowsum_max"], bn["Q"]["rem_rowsum_max"])
    add("c_alpha", bo["geometry"]["c_alpha"], bn["geometry"]["c_alpha"])
    add("c_loc", bo["geometry"]["c_loc"], bn["geometry"]["c_loc"])
    add("c_prev max", bo["geometry"]["c_prev_max"], bn["geometry"]["c_prev_max"])
    add("EA max", bo["geometry"]["EA_max"], bn["geometry"]["EA_max"])
    add("R_max (cell defect)", bo["cells"]["R_max"], bn["cells"]["R_max"])
    ro = bo["results"] if "results" in bo else P(f"t6_stageD_{old}")["results"]
    rn = bn["results"]
    add("rho(M) upper", ro["spectral_radius"]["cw_upper"], rn["spectral_radius"]["cw_upper"])
    add("rho(M) lower", ro["spectral_radius"]["cw_lower"], rn["spectral_radius"]["cw_lower"])
    co, cn = ro["certificate"], rn["certificate"]
    for k in ("min_slack", "eps", "omega_max", "omega_median", "omega_T", "theta_max", "beta_max",
              "state_err_adapted_max", "state_err_phys_max", "D2_max", "D2_at_T", "contraction_q_norm"):
        add(k, co.get(k), cn.get(k))
    add("b-iterations", ro["iteration"]["n_iter"], rn["iteration"]["n_iter"], "{}")
    eo, en = P(f"t6_stageE_{old}"), P(f"t6_stageE_{new}")
    add("pad max (physical)", eo["pad"]["max"], en["pad"]["max"])
    add("entry: n_cells", eo["entry"]["n_cells"], en["entry"]["n_cells"], "{}")
    add("entry: eta", eo["entry"]["eta"], en["entry"]["eta"])
    add("entry: t_lo of span", eo["entry"]["time_span_of_certified_cells"][0], en["entry"]["time_span_of_certified_cells"][0])
    add("entry: t_hi of span", eo["entry"]["time_span_of_certified_cells"][1], en["entry"]["time_span_of_certified_cells"][1])
    for k in ("K_J_upper", "M_T_upper", "C0", "c3", "margin_lower", "K_C_r_upper"):
        add(k, eo["m1"][k], en["m1"][k])
    add("M_T linear flow", eo["m1"]["M_T_terms"]["term_linear_flow"], en["m1"]["M_T_terms"]["term_linear_flow"])
    add("M_T far history", eo["m1"]["M_T_terms"]["term_far_history"], en["m1"]["M_T_terms"]["term_far_history"])
    add("M_T near history", eo["m1"]["M_T_terms"]["term_near_history"], en["m1"]["M_T_terms"]["term_near_history"])
    verdicts = dict(old_banach=co.get("banach"), new_banach=cn.get("banach"), old_entry=eo["entry"]["verdict"],
                    new_entry=en["entry"]["verdict"], old_m1=eo["m1"]["verdict"], new_m1=en["m1"]["verdict"])
    print("| constant | TASK-0006 (c9bc2f8) | TASK-0007 hardened | rel. change |\n|---|---|---|---|")
    for label, a, b, rel in rows:
        fa = f"{a:.6g}" if isinstance(a, float) else str(a)
        fb = f"{b:.6g}" if isinstance(b, float) else str(b)
        print(f"| {label} | {fa} | {fb} | {rel:+.2e} |" if isinstance(rel, float) and np.isfinite(rel) else f"| {label} | {fa} | {fb} | — |")
    print(verdicts)
    with open(os.path.join(ROOT, "data", "t7_comparison.json"), "w") as f:
        json.dump({"rows": [dict(label=l, old=a, new=b, rel=r) for l, a, b, r in rows], "verdicts": verdicts}, f, indent=1)


if __name__ == "__main__":
    main()
