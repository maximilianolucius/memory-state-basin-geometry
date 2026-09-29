#!/usr/bin/env python3
r"""TASK-0002 Stage A — independent reference in the initial singular layer.

For an autonomous Caputo system with polynomial g, the solution has the
generalised power series  x(t) = sum_{k>=0} a_k u^k,  u = t^alpha,  a_0 = p,  with

    a_k = Gamma((k-1) alpha + 1) / Gamma(k alpha + 1) * [g(x)]_{k-1},

because  ^C D^alpha t^{k alpha} = Gamma(k alpha+1)/Gamma((k-1) alpha+1) t^{(k-1) alpha}
and g(x(t)) is a power series in u (Cauchy products).  This method shares NOTHING
with product integration, so it is an independent check of the float solvers and
of the rigorous boxes in the layer where the float solvers are least accurate.

Series truncation is monitored by the size of the last terms; points where the
tail is not negligible are reported as unusable, not used.
"""
import os
import sys

import mpmath as mp
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.models import AlleePredatorPrey          # noqa: E402
from msbg.provenance import RunRecorder            # noqa: E402
from msbg.solvers import METHODS, solve            # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def series_coeffs(theta, a, b, m, alpha, p, K, dps=60):
    mp.mp.dps = dps
    al = mp.mpf(alpha)
    X = [[mp.mpf(p[0])], [mp.mpf(p[1])]]

    def conv(u, v, k):
        return mp.fsum(u[i] * v[k - i] for i in range(k + 1))

    for k in range(1, K + 1):
        j = k - 1
        x, y = X[0], X[1]
        xx = conv(x, x, j)
        # need x^2 and x^3 coefficients up to j
        x2 = [conv(x, x, i) for i in range(j + 1)]
        x3j = mp.fsum(x2[i] * x[j - i] for i in range(j + 1))
        xyj = conv(x, y, j)
        # g_x = x(1-x)(x-theta) - a x y = -x^3 + (1+theta) x^2 - theta x - a x y
        gx = -x3j + (1 + mp.mpf(theta)) * xx - mp.mpf(theta) * x[j] - mp.mpf(a) * xyj
        gy = mp.mpf(b) * xyj - mp.mpf(m) * y[j]
        fac = mp.gamma(j * al + 1) / mp.gamma(k * al + 1)
        X[0].append(fac * gx)
        X[1].append(fac * gy)
    return X


def evaluate(X, alpha, t):
    u = mp.mpf(t) ** mp.mpf(alpha)
    vals, tails = [], []
    for c in range(2):
        terms = [X[c][k] * u**k for k in range(len(X[c]))]
        vals.append(mp.fsum(terms))
        tails.append(max(abs(v) for v in terms[-5:]))
    return [float(v) for v in vals], float(max(tails))


def main():
    theta, a, b, m, alpha = 0.3, 1.0, 1.0, 0.8, 0.85
    p = [2.4372, 2.012]
    K = 120
    X = series_coeffs(theta, a, b, m, alpha, p, K)
    model = AlleePredatorPrey(theta=theta, a=a, b=b, m=m)
    d = np.load(os.path.join(ROOT, "data", "t2_stageA_certify_N4000_arrays.npz"))
    tm, U = d["tm"], d["U"]
    lo_x, hi_x = d["x_lo"] - U, d["x_hi"] + U
    lo_y, hi_y = d["y_lo"] - U, d["y_hi"] + U
    rec = RunRecorder("t2_stageA_series", ROOT)
    ts = np.concatenate([np.geomspace(1e-6, 0.05, 40)])
    floats = {}
    for meth in METHODS:
        h = 2e-4
        r = solve(model, np.array([p]), alpha, h, int(round(0.06 / h)), method=meth, store=True)
        floats[meth] = (r.t, r.x[:, 0, :])
    rows = []
    print(f"{'t':>10}{'series x':>14}{'tail':>10}{'in box':>8}"
          + "".join(f"{'|'+k+'-series|':>18}" for k in METHODS))
    for t in ts:
        v, tail = evaluate(X, alpha, t)
        if tail > 1e-12:
            continue
        n = int(np.clip(np.searchsorted(tm, t, side="right") - 1, 0, len(tm) - 2))
        inside = (lo_x[n] <= v[0] <= hi_x[n]) and (lo_y[n] <= v[1] <= hi_y[n])
        errs = {}
        for meth, (tt, xx) in floats.items():
            xi = np.array([np.interp(t, tt, xx[:, 0]), np.interp(t, tt, xx[:, 1])])
            errs[meth] = float(np.max(np.abs(xi - np.array(v))))
        rows.append({"t": float(t), "series": v, "tail": tail, "inside_rigorous_box": inside,
                     "box_x": [float(lo_x[n]), float(hi_x[n])],
                     "box_y": [float(lo_y[n]), float(hi_y[n])], "float_errors": errs})
        print(f"{t:10.2e}{v[0]:14.8f}{tail:10.1e}{str(inside):>8}"
              + "".join(f"{errs[k]:18.2e}" for k in METHODS))
    usable = len(rows)
    ok = all(r["inside_rigorous_box"] for r in rows)
    print(f"\nusable series points: {usable};  series value inside the rigorous box at all of them: {ok}")
    rec.add("rows", rows)
    rec.add("series_terms", K)
    rec.add("all_series_points_inside_rigorous_boxes", ok)
    rec.add("evidence_class", "independent consistency check (generalised power series), not part of the proof")
    print("manifest:", rec.finish())


if __name__ == "__main__":
    main()
