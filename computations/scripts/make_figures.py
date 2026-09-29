#!/usr/bin/env python3
"""TASK-0001 — figures.

Every figure answers one theorem-level question and regenerates from committed
data only (COMPUTE_AGENT_INITIAL_PROMPT.md: "Generate figures only when each
answers a theorem-level question", "Every figure and table must regenerate from
code and saved data").

F1  Does a survival-bound orbit of the positive Caputo system enter the
    CERTIFIED-CONDITIONAL extinction region {0 <= x < theta}?
F2  What is the Caputo-specific mechanism?  (x rises while ^C D^a x < 0.)
F3  Are the solvers trustworthy?  (observed convergence orders against exact
    Mittag-Leffler solutions.)
F4  Is reachable present-state observation non-injective in d = 2?
    (Stage-B collapse at a zero of E_alpha.)
F5  Over which fractional orders does the witness persist?
"""
from __future__ import annotations

import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
FIGS = os.path.join(ROOT, "figures")
os.makedirs(FIGS, exist_ok=True)
plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.25,
                     "figure.dpi": 150, "savefig.bbox": "tight"})


def _load(name):
    p = os.path.join(DATA, name)
    if not os.path.exists(p):
        print(f"  [skip] missing {name}")
        return None
    return np.load(p, allow_pickle=True) if name.endswith(".npz") else json.load(open(p))


def fig1_witness_orbit(manifest):
    d = _load("stage_d_witness_witness_orbit.npz")
    if d is None:
        return
    t, x, E, p = d["t"], d["x"], d["E"], d["p"]
    theta = manifest["payload"]["model"]["theta"]
    idx = d["arc_index"]
    fig, ax = plt.subplots(1, 2, figsize=(9.2, 3.6))
    ax[0].axvspan(0, theta, color="0.85", zorder=0)
    ax[0].text(theta / 2, ax[0].get_ylim()[1], "", ha="center")
    ax[0].plot(x[:, 0], x[:, 1], lw=0.8, color="C0", label="orbit of $p$")
    ax[0].plot(x[idx, 0], x[idx, 1], lw=2.0, color="C3",
               label=r"inside $\{0\leq x<\theta\}$")
    ax[0].plot(*p, "ko", ms=5, label="$p$ (constant history)")
    ax[0].plot(E[0], E[1], "*", color="C2", ms=12, label="$E^*$ (coexistence)")
    ax[0].plot(0, 0, "s", color="C3", ms=6, label="extinction")
    ax[0].axvline(theta, color="C3", lw=0.8, ls="--")
    ax[0].set_xlabel("$x$ (prey)"); ax[0].set_ylabel("$y$ (predator)")
    ax[0].set_title(r"survival orbit enters the certified extinction region")
    ax[0].legend(fontsize=7, loc="center right", framealpha=0.9)
    ax[1].plot(t, x[:, 0], lw=0.9, color="C0", label="$x(t)$")
    ax[1].axhline(theta, color="C3", ls="--", lw=0.8, label=r"$\theta$")
    ax[1].axhline(E[0], color="C2", ls=":", lw=0.8, label="$x^*$")
    ax[1].fill_between(t, 0, theta, where=x[:, 0] < theta, color="C3", alpha=0.25)
    ax[1].set_xscale("symlog", linthresh=10)
    ax[1].set_xlabel("$t$"); ax[1].set_ylabel("$x(t)$")
    ax[1].set_title("prey component")
    ax[1].legend(fontsize=7)
    fig.savefig(os.path.join(FIGS, "F1_witness_orbit.png"))
    plt.close(fig)
    print("  F1 written")


def fig2_mechanism(manifest):
    d = _load("stage_d_witness_witness_mechanism.npz")
    if d is None:
        return
    t, x, g, win = d["t"], d["x"], d["g_x"], d["window"]
    theta = manifest["payload"]["model"]["theta"]
    pad = max(1, len(win) // 12)
    lo = max(0, win[0] - pad)
    hi = min(len(t) - 1, win[-1] + pad)
    sl = slice(lo, hi + 1)
    gw = g[win]
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ax.plot(t[sl], x[sl, 0], color="C0", lw=1.4, label="$x(t)$")
    ax.axhline(theta, color="C3", ls="--", lw=0.8, label=r"$\theta$")
    ax.axvspan(t[win[0]], t[win[-1]], color="C1", alpha=0.13)
    ax.set_xlabel("$t$")
    ax.set_ylabel("$x(t)$", color="C0")
    ax.tick_params(axis="y", labelcolor="C0")
    ax.set_xlim(t[lo], t[hi])
    ax2 = ax.twinx()
    ax2.plot(t[sl], g[sl], color="C4", lw=1.2, label=r"$^{C}\!D^{\alpha}x(t)$")
    ax2.axhline(0.0, color="0.35", lw=0.7)
    lo_g = float(gw.min())
    ax2.set_ylim(1.15 * lo_g, -0.10 * lo_g)
    ax2.set_ylabel(r"$^{C}\!D^{\alpha}x(t)=g_x(x,y)$", color="C4")
    ax2.tick_params(axis="y", labelcolor="C4")
    ax2.grid(False)
    ax.set_title(r"$x$ rises through $\theta$ while $^{C}\!D^{\alpha}x<0$ throughout")
    ax.annotate(
        rf"$\max_t\,{{}}^{{C}}\!D^{{\alpha}}x = {gw.max():.3g}$",
        xy=(0.42, 0.06), xycoords="axes fraction", fontsize=8, color="C4",
    )
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=7, loc="upper left")
    fig.savefig(os.path.join(FIGS, "F2_caputo_mechanism.png"))
    plt.close(fig)
    print("  F2 written")


def fig3_solver_orders():
    a2 = _load("stage_a_A2_scalar_linear.json")
    a3 = _load("stage_a_A3_planar_linear.json")
    if a2 is None:
        return
    fig, ax = plt.subplots(1, 2, figsize=(9.0, 3.4))
    colors = {"pi_rect": "C0", "pece": "C1", "l1": "C2"}
    for r in a2:
        if r["alpha"] != 0.6 or r["lam"] != -1.0:
            continue
        ax[0].loglog(r["h"], r["abs_err"], "o-", ms=3, color=colors[r["method"]],
                     label=f"{r['method']} (order {r['observed_order']:.2f})")
    hh = np.array(a2[0]["h"])
    ax[0].loglog(hh, 3e-3 * hh / hh[0], "k--", lw=0.7, label=r"$O(h)$")
    ax[0].set_title(r"scalar $^{C}\!D^{0.6}x=-x$ vs exact $E_{0.6}$")
    for r in (a3 or []):
        ax[1].loglog(r["h"], r["max_abs_err"], "o-", ms=3, color=colors[r["method"]],
                     label=f"{r['method']} (order {r['observed_order']:.2f})")
    ax[1].set_title(r"planar $^{C}\!D^{0.5}x=Ax$ vs exact matrix $E_{0.5}$")
    for a in ax:
        a.set_xlabel("$h$"); a.set_ylabel("absolute error"); a.legend(fontsize=7)
    fig.savefig(os.path.join(FIGS, "F3_solver_convergence.png"))
    plt.close(fig)
    print("  F3 written")


def fig4_stage_b():
    b4 = _load("stage_b_B4_collapse_convergence.json")
    if b4 is None:
        return
    fig, ax = plt.subplots(figsize=(5.0, 3.4))
    for r in b4:
        h = 1.0 / np.array(r["N"], float)
        ax.loglog(h, r["max_abs_x_at_t1"], "o-", ms=3,
                  label=f"{r['method']} (order {r['observed_order']:.2f})")
    ax.set_xlabel("$h$")
    ax.set_ylabel(r"$\max_{x_0}\;\|x(1;x_0)\|$")
    ax.set_title(r"all orbits collapse to $0$ at $t=1$:  $E_{1/2}(A)=0$")
    ax.legend(fontsize=7)
    fig.savefig(os.path.join(FIGS, "F4_stageB_collapse.png"))
    plt.close(fig)
    print("  F4 written")


def fig5_alpha_dependence():
    res = _load("stage_d_scan_v2_phase2_results.json")
    p1 = _load("stage_d_scan_v2_phase1_summary.json")
    if res is None:
        return
    rel = [
        r for r in res
        if r.get("witness")
        and r.get("mesh_diff_minx") is not None
        and r["mesh_diff_minx"] < 0.05 * r["margin"]
    ]
    if not rel:
        print("  [skip] F5: no mesh-reliable witnesses recorded")
        return
    alphas = sorted({r["alpha"] for r in res})
    data = [[r["margin"] for r in rel if r["alpha"] == a] for a in alphas]
    counts = [len(d) for d in data]

    # candidates that even reached the long-horizon test, per alpha
    tried = [sum(1 for r in res if r["alpha"] == a) for a in alphas]
    recovered = {}
    for row in (p1 or []):
        a = float(row["key"].rsplit("_al", 1)[1])
        recovered[a] = recovered.get(a, 0) + row.get("n_recovered_candidates", 0)

    fig, ax = plt.subplots(1, 2, figsize=(9.2, 3.5))
    pos = np.arange(len(alphas))
    nonempty = [i for i, d in enumerate(data) if d]
    ax[0].boxplot([data[i] for i in nonempty], positions=pos[nonempty], widths=0.35,
                  showfliers=False)
    for i in nonempty:
        ax[0].scatter(np.full(len(data[i]), pos[i]) + np.random.RandomState(0).uniform(
            -0.11, 0.11, len(data[i])), data[i], s=6, alpha=0.45, color="C0", zorder=3)
    ax[0].set_xticks(pos)
    ax[0].set_xticklabels([f"{a:g}" for a in alphas])
    ax[0].set_xlabel(r"fractional order $\alpha$")
    ax[0].set_ylabel(r"$\theta-\min_t x(t)$")
    ax[0].set_title("depth inside the certified extinction region")

    w = 0.38
    ax[1].bar(pos - w / 2, [recovered.get(a, 0) for a in alphas], w,
              label=r"phase 1: recovered above $\theta$", color="C1")
    ax[1].bar(pos + w / 2, counts, w, label="phase 2: mesh-reliable witnesses", color="C0")
    ax[1].set_yscale("symlog", linthresh=1)
    ax[1].set_xticks(pos)
    ax[1].set_xticklabels([f"{a:g}" for a in alphas])
    ax[1].set_xlabel(r"fractional order $\alpha$")
    ax[1].set_ylabel("count (symlog)")
    ax[1].set_title("witnesses found per order")
    ax[1].legend(fontsize=7)
    fig.suptitle("persistence of the multibasin witness in the fractional order", y=1.02,
                 fontsize=10)
    fig.savefig(os.path.join(FIGS, "F5_alpha_dependence.png"))
    plt.close(fig)
    print(f"  F5 written (witness counts per alpha: "
          f"{dict(zip([f'{a:g}' for a in alphas], counts))})")


def main():
    man = os.path.join(ROOT, "manifests", "stage_d_witness_manifest.json")
    manifest = json.load(open(man)) if os.path.exists(man) else {"payload": {"model": {"theta": 0.4}}}
    print("figures ->", FIGS)
    fig1_witness_orbit(manifest)
    fig2_mechanism(manifest)
    fig3_solver_orders()
    fig4_stage_b()
    fig5_alpha_dependence()


if __name__ == "__main__":
    main()
