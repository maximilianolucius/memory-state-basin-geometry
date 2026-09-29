# Status

**Phase:** ACTIVE — WITNESS FOUND; PRINCIPAL THEOREM CLOSURE

## TASK-0001 assimilated — 2026-09-29

Compute branch:
\`compute/task-0001\`

Verified HEAD:
\`9e607dd2f83b249b0b47e76a3a9f1380f46fff5b\`

Merged:
PR #1 -> main at \`26f53ee3eb39de7e6e884232ef65c13723b27b9b\`.

## Main result

A reproducible numerical witness now exists in the project-constructed strong-Allee Caputo predator–prey model:
\[
{}^C D^\alpha x=x(1-x)(x-\theta)-axy,
\]
\[
{}^C D^\alpha y=y(bx-m).
\]

At
\[
\theta=0.3,\quad a=b=1,\quad m=0.8,\quad \alpha=0.85,
\]
the standard initial state
\[
p=(2.4372,2.012)
\]
has a numerically survival-bound orbit that enters deeply into
\[
R_{\rm ext}=\{0<x<\theta,\ y\ge0\},
\]
then recovers.

The event survives fine-mesh, multi-solver, long-horizon and 30-digit checks.

## Structural simplification

The target multibasin fiber does **not** require two advanced trajectories to intersect.

If a survival-basin orbit reaches
\[
z\in R_{\rm ext},
\]
then the two reachable states
\[
T_t\iota(p),\qquad \iota(z)
\]
already share present state \(z\).

Thus the theorem reduces to:
- cold start at \(z\) goes extinct;
- continuation state carrying prehistory survives.

This is formalized in \`research/STRUCTURAL_THEOREMS.md\`.

Transversality/IFT is retired from the principal existence/persistence theorem.

## Evidence status

### Strong
- solver infrastructure: PASS;
- Stage-B Mittag-Leffler zero: CERTIFIED COMPUTATION;
- equilibrium spectra: exact/certified algebra;
- nonlinear threshold entry: very strong NUMERICAL CORROBORATION.

### Not yet proved
- positive-cone/comparison hypotheses needed for the full extinction-strip theorem;
- survival-basin membership of the witness;
- nonlinear interval enclosure of the witness trajectory;
- faithful published Double-Allee realization.

Therefore:
**TARGET-A20 = CONJECTURED, NOT PROVED.**

## Active next gates

### ROUND-0003 — Web Search
Exact published Double-Allee model, exact-vector-field prior, Caputo threshold-recovery mechanism, extinction-strip theorem audit, and continuation-state basin/trapping theorem search.

### TASK-0002 — Compute
Validated finite-time entry certification and search for near-equilibrium witnesses that may be easier to place rigorously in a survival basin.

## Paper

**NOT STARTED.**

The project now has a credible theorem mechanism, but manuscript mode remains blocked until survival basin membership and exact novelty/model provenance are closed.
