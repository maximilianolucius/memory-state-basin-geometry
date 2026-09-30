#!/usr/bin/env python
"""Generate data-dependent manuscript figures from the committed TASK-0006 certificate.

Inputs are existing repository artifacts.  No theorem constant is recomputed or
changed here; the script regenerates the numerical center and visualizes the
already certified tube/mesh.

Outputs (default paper/figures/generated):
  fig02_phase_plane.{pdf,svg,png}
  fig03_time_series.{pdf,svg,png}
  fig05_cap_tube.{pdf,svg,png}
  fig07_mesh_defect.{pdf,svg,png}

Evidence rule:
- center curves are numerical visualizations;
- shaded error envelopes use the certified TASK-0006 state-radius arrays;
- theorem statements continue to rely on the manifests, not pixels.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
REPO = HERE.parents[2]
sys.path.insert(0, str(ROOT))

from msbg.aposteriori import collocation
from msbg.models import AlleePredatorPrey
from msbg.validated_res import Setup


ENTRY = (5.857677414299934, 13.727538858047476)
REP_CELL = (8.983919537032376, 8.992793262447533)
E_STAR = np.array([4.0 / 5.0, 3.0 / 25.0])
P = np.array([277.0 / 100.0, 467.0 / 1000.0])


def _save(fig, outdir: Path, stem: str) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "svg", "png"):
        kwargs = {"bbox_inches": "tight"}
        if ext == "png":
            kwargs["dpi"] = 240
        fig.savefig(outdir / f"{stem}.{ext}", **kwargs)
    plt.close(fig)


def _load(tag: str):
    cert_path = ROOT / "data" / f"t6_stageD_{tag}_certificate_weights.npz"
    cert = np.load(cert_path)
    tm = np.asarray(cert["tm"], float)
    omega = np.asarray(cert["omega"], float)
    theta = np.asarray(cert["theta"], float)
    beta = np.asarray(cert["beta"], float)
    Omega = np.asarray(cert["Omega"], float)

    st = Setup("1/2", "1/2", "1", "4/5", "17/20", ("277/100", "467/1000"))
    fl, pf = st.floats()
    model = AlleePredatorPrey(theta=fl["theta"], a=fl["a"], b=fl["b"], m=fl["m"])
    X, PHI, M = collocation(model, np.array(pf), fl["alpha"], tm)

    # Omega is an adapted-norm state error bound per cell.
    # Convert to a physical Euclidean pad using the same norm factor as Stage E.
    pad_cell = float(st.normS) * Omega
    pad_node = np.empty_like(tm)
    pad_node[0] = pad_cell[0]
    pad_node[-1] = pad_cell[-1]
    if len(tm) > 2:
        pad_node[1:-1] = np.maximum(pad_cell[:-1], pad_cell[1:])

    return st, tm, X, omega, theta, beta, Omega, pad_node


def fig02_phase_plane(outdir: Path, tag: str) -> None:
    _, tm, X, *_ = _load(tag)
    mask = (tm >= ENTRY[0]) & (tm <= ENTRY[1])

    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    ax.axvspan(0.0, 0.5, alpha=0.12, label=r"cold-start extinction strip $0<x<1/2$")
    ax.plot(X[:, 0], X[:, 1], linewidth=1.4, label="numerical center")
    ax.plot(X[mask, 0], X[mask, 1], linewidth=3.0, label="certified-entry time segment")
    ax.scatter([P[0]], [P[1]], marker="o", zorder=4, label=r"$p$")
    ax.scatter([E_STAR[0]], [E_STAR[1]], marker="x", zorder=4, label=r"$E^*$")
    ax.axvline(0.5, linewidth=1.0, linestyle="--")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_title("B215 physical excursion")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.2)
    _save(fig, outdir, "fig02_phase_plane")


def fig03_time_series(outdir: Path, tag: str) -> None:
    _, tm, X, _, _, _, _, pad = _load(tag)
    show = tm <= 40.0

    fig, ax = plt.subplots(figsize=(7.1, 4.1))
    ax.plot(tm[show], X[show, 0], linewidth=1.4, label=r"$x(t)$ center")
    ax.fill_between(
        tm[show],
        X[show, 0] - pad[show],
        X[show, 0] + pad[show],
        alpha=0.20,
        label="certified physical pad",
    )
    ax.axhline(0.5, linestyle="--", linewidth=1.0, label=r"threshold $\theta=1/2$")
    ax.axvspan(*ENTRY, alpha=0.12, label="certified entry interval")
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$x$")
    ax.set_title("Certified prey threshold excursion")
    ax.grid(alpha=0.2)
    ax.legend(fontsize=8)
    _save(fig, outdir, "fig03_time_series")


def fig05_cap_tube(outdir: Path, tag: str) -> None:
    _, tm, _, omega, theta, beta, Omega, _ = _load(tag)
    tc = tm[:-1]

    fig, ax = plt.subplots(figsize=(7.1, 4.1))
    ax.semilogy(tc, omega, linewidth=1.0, label=r"$\omega_n$: source sup")
    ax.semilogy(tc, theta, linewidth=1.0, label=r"$\vartheta_n$: source oscillation")
    ax.semilogy(tc, beta, linewidth=1.0, label=r"$\beta_n$: interpolation bubble")
    ax.semilogy(tc, Omega, linewidth=1.4, label=r"$\Omega_n$: adapted state tube")
    ax.set_xlabel(r"$t_n$")
    ax.set_ylabel("certified bound")
    ax.set_title("Cellwise TASK-0006 certificate")
    ax.grid(alpha=0.2, which="both")
    ax.legend(fontsize=8)
    _save(fig, outdir, "fig05_cap_tube")


def fig07_mesh_defect(outdir: Path, tag: str) -> None:
    _, tm, _, omega, theta, beta, Omega, _ = _load(tag)
    h = np.diff(tm)
    tc = tm[:-1]

    # The certificate weights are the committed output of the defect-equidistributed
    # validation.  We plot h and the final source sup bound; this avoids inventing a
    # "defect" quantity not explicitly stored in the final certificate.
    fig, ax1 = plt.subplots(figsize=(7.1, 4.1))
    ax1.semilogy(tc, h, linewidth=1.2, label=r"mesh width $h_n$")
    ax1.set_xlabel(r"$t_n$")
    ax1.set_ylabel(r"$h_n$")
    ax1.grid(alpha=0.2, which="both")

    ax2 = ax1.twinx()
    ax2.semilogy(tc, omega, linewidth=1.0, label=r"source bound $\omega_n$")
    ax2.set_ylabel(r"$\omega_n$")

    lines = ax1.get_lines() + ax2.get_lines()
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, fontsize=8, loc="best")
    ax1.set_title("Adaptive mesh and final cellwise source bound")
    _save(fig, outdir, "fig07_mesh_defect")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="adaptT300_N12000")
    ap.add_argument(
        "--outdir",
        default=str(REPO / "paper" / "figures" / "generated"),
    )
    args = ap.parse_args()
    outdir = Path(args.outdir)

    fig02_phase_plane(outdir, args.tag)
    fig03_time_series(outdir, args.tag)
    fig05_cap_tube(outdir, args.tag)
    fig07_mesh_defect(outdir, args.tag)

    meta = {
        "tag": args.tag,
        "entry_interval": ENTRY,
        "representative_cell": REP_CELL,
        "outputs": [
            "fig02_phase_plane",
            "fig03_time_series",
            "fig05_cap_tube",
            "fig07_mesh_defect",
        ],
        "note": (
            "Center curves are numerical visualization; shaded state pads and "
            "cellwise certificate arrays come from the committed TASK-0006 certificate."
        ),
    }
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "paper_figure_manifest.json").write_text(
        json.dumps(meta, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
