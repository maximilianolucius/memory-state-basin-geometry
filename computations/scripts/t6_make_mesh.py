#!/usr/bin/env python
"""Defect-equidistributing mesh for TASK-0006 from the cell defects of a previous run.

c(t) = R_n / h_n^2 (defect density of the PL collocation); the mesh density is
d(t) = max(kappa c^{1/3}, 1/h_cap), limited to `refine` times the old density, with kappa
chosen so that the mesh has N cells on [0, T].  Non-rigorous: only proposes nodes."""
import argparse
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ap = argparse.ArgumentParser()
ap.add_argument("--src", required=True)
ap.add_argument("--T", type=float, required=True)
ap.add_argument("--N", type=int, required=True)
ap.add_argument("--hcap", type=float, default=0.12)
ap.add_argument("--refine", type=float, default=6.0)
ap.add_argument("--out", required=True)
a = ap.parse_args()
B = np.load(os.path.join(ROOT, "data", f"t6_stageBD_{a.src}_blocks.npz"))
tm, R = B["tm"], B["R"]
keep = tm[1:] <= a.T * (1 + 1e-12)
t0, t1, R = tm[:-1][keep], tm[1:][keep], R[keep]
h = t1 - t0
c = R / h**2
for _ in range(3):                                           # running max (robust to enclosure noise)
    c = np.maximum(c, np.maximum(np.roll(c, 1), np.roll(c, -1)))
lo, hi = 1e-12, 1e12
for _ in range(200):
    kap = np.sqrt(lo * hi)
    d = np.minimum(np.maximum(kap * c ** (1 / 3), 1.0 / a.hcap), a.refine / h)
    d = np.maximum(d, 1.0 / h * (t1 < 1e-3))                 # keep the graded start as it is
    n = float(np.sum(d * h))
    lo, hi = (kap, hi) if n < a.N else (lo, kap)
cum = np.concatenate([[0.0], np.cumsum(d * h)])
cum *= a.N / cum[-1]
edges = np.concatenate([[0.0], t1])
new = np.interp(np.arange(a.N + 1), cum, edges)
new[0], new[-1] = 0.0, a.T
assert np.all(np.diff(new) > 0)
np.save(a.out, new)
hn = np.diff(new)
print(f"mesh {a.out}: N={a.N} T={a.T} h_min={hn.min():.3g} h_max={hn.max():.3g}; "
      f"predicted int R dt: old {np.sum(R*h):.3e} -> new {np.sum(c*h/d**2):.3e}")
for t in (0.02, 0.5, 3, 10, 30, 100, a.T - 1):
    i = min(np.searchsorted(new, t), a.N - 1); j = min(np.searchsorted(t1, t), len(h) - 1)
    print(f"  t={t}: h_new={hn[i]:.3e}  h_old={h[j]:.3e}  R_old={R[j]:.2e}")
