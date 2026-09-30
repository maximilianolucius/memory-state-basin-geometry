#!/usr/bin/env python
"""TASK-0006 post-processing of a closed certificate:
 (a) rigorous ||B|| in the certificate's weighted norm (B = L_h^{-1} pi + (I - pi));
 (b) NON-rigorous cross-check: the certified tube must contain an independent numerical
     solution (collocation on a different mesh), sampled at common times."""
import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msbg.aposteriori import collocation, graded_mesh, xhat_eval             # noqa: E402
from msbg.cap import COMPONENTS, Geometry, _B_source_vectors, cap_vectors, lipschitz_A_cells, up, z2_vectors   # noqa: E402
from msbg.models import AlleePredatorPrey                                    # noqa: E402
from msbg.provenance import RunRecorder                                      # noqa: E402
from msbg.validated_res import Setup                                         # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ap = argparse.ArgumentParser()
ap.add_argument("--tag", required=True)
ap.add_argument("--Nref", type=int, default=9000)
a = ap.parse_args()
np.seterr(all="ignore")
B = np.load(os.path.join(ROOT, "data", f"t6_stageBD_{a.tag}_blocks.npz"))
C = np.load(os.path.join(ROOT, "data", f"t6_stageD_{a.tag}_certificate_weights.npz"))
tm, Rn, Dn = B["tm"], B["Rn"], B["Dn"]
om, th, be, Om = C["omega"], C["theta"], C["beta"], C["Omega"]
N = len(tm) - 1
# (a) ||B s|| for s in the unit ball of the weighted norm: |s| <= omega, osc <= theta, bubble <= beta
om_node = np.concatenate([[om[0]], np.minimum(om[:-1], om[1:])])
om_node = np.concatenate([om_node[:-1], [om[-1]]]) if len(om_node) == N + 1 else np.concatenate([om_node, [om[-1]]])
sup, osc, bub = _B_source_vectors(Rn, Dn, om_node, om, th, th)
bub = np.minimum(bub, be)                                  # (I - pi) B s = (I - pi) s
out = {"B_norm_sup": float(np.max(sup / om)), "B_norm_osc": float(np.max(osc / th)),
       "B_norm_bub": float(np.max(bub / be)), "Linv_block_rowsum_max": float(Rn.sum(1).max()),
       "Linv_block_rowsum_T": float(Rn[-1].sum())}
out["B_norm"] = max(out["B_norm_sup"], out["B_norm_osc"], out["B_norm_bub"])
# (b) cross-check against an independent collocation
st = Setup("1/2", "1/2", "1", "4/5", "17/20", ("277/100", "467/1000"))
fl, pf = st.floats()
al = fl["alpha"]
model = AlleePredatorPrey(theta=fl["theta"], a=fl["a"], b=fl["b"], m=fl["m"])
X, PHI, M = collocation(model, np.array(pf), al, tm)
tr = graded_mesh(float(tm[-1]), a.Nref, 3.0)
Xr, PHIr, Mr = collocation(model, np.array(pf), al, tr)
ts = np.array([0.5, 2.0, 5.0, 8.99, 13.0, 28.3, 60.0, 150.0, float(tm[-1])])
ts = ts[ts <= tm[-1]]
x1 = xhat_eval(ts, tm, PHI[0], M, np.array(pf), al)
x2 = xhat_eval(ts, tr, PHIr[0], Mr, np.array(pf), al)
Si = np.array([[float(v.mid()) for v in row] for row in st.Si_arb])
rows = []
for k, t in enumerate(ts):
    n = min(np.searchsorted(tm, t, side="right") - 1, N - 1)
    dS = float(np.linalg.norm(Si @ (x1[k] - x2[k])))
    rows.append({"t": float(t), "xhat": x1[k].tolist(), "diff_adapted": dS, "certified_radius_adapted": float(Om[n]),
                 "ratio": dS / float(Om[n])})
out["crosscheck_vs_independent_mesh"] = {"Nref": a.Nref, "rows": rows,
                                         "note": "NON-rigorous; the reference has its own error"}
# (c) classical radii polynomial (Church-Queirolo convention) in the Perron-weighted norm
#     ||h||_q = max_c max_n h_c[n]/q_c[n]  (q = contraction weights of the certificate):
#     p(r) = Y0 + (Z1 + Z2a r - 1) r  with  Y0 >= ||B rho||_q, Z1 >= ||I - B(I-K)||_q,
#     Z2a r >= sup_{||f||_q <= r} ||B(K_f - K)||_q  (D2 valid on the tube of the largest r used).
Q = np.load(os.path.join(ROOT, "data", f"t6_stageD_{a.tag}_contraction_weights.npz"))
q0 = [Q["q_sup"], Q["q_osc"], Q["q_bub"]]
xbox = dict(theta=fl["theta"], a=fl["a"], b=fl["b"], x_lo=float(B["x_lo"].min()), x_hi=float(B["x_hi"].max()))
geo = Geometry(tm, al, PHI, float(st.normS), float(st.normSi), xbox, B["diam"])
geo.Qn, geo.DQn = B["Qn"], B["DQn"]
nSi2 = float(up(float(st.normSi) * np.sqrt(2.0)))
C2 = np.load(os.path.join(ROOT, "data", f"t6_stageD_{a.tag}_certificate_weights.npz"))
bvec = [C2["omega"], C2["theta"], C2["beta"]]
bmax = max(float(x.max()) for x in bvec)
best = None
for floor in (0.3, 0.1, 0.03, 0.01, 3e-3, 1e-3):
    # the Perron vector vanishes where nothing feeds (early cells); any positive weight vector
    # gives a valid norm: mix it with the certificate weights b (which are positive everywhere)
    q = [np.maximum(x, floor * y / bmax * max(float(z.max()) for z in q0)) for x, y in zip(q0, bvec)]
    vq = cap_vectors(geo, Rn, Dn, B["rho"], B["R"], B["drho"], B["normA"], B["oscA"], q[0], q[1], 0.0, nSi2, beta=q[2])
    Y0 = max(float(np.max(vq["Y" + c] / q[i])) for i, c in enumerate(COMPONENTS))
    Z1 = max(float(np.max((vq["T1" + c] + vq["T2" + c]) / q[i])) for i, c in enumerate(COMPONENTS))
    print("RADII mix", floor, "Y0", Y0, "Z1", Z1)
    if Z1 >= 1:
        continue
    Om_q, V_q = vq["Omega"], vq["_V"]
    r_max = 4.0 * Y0 / (1.0 - Z1)
    D2 = lipschitz_A_cells(st, B["x_lo"], B["x_hi"], float(up(float(st.normS) * r_max * float(Om_q.max()))))
    z = z2_vectors(geo, Rn, Dn, D2, Om_q, V_q, Om_q, V_q)
    Z2a = max(float(np.max(z[i] / q[i])) for i in range(3))
    rs = np.linspace(0.0, r_max, 200001)[1:]
    p = Y0 + (Z1 + Z2a * rs - 1.0) * rs
    neg = rs[p < 0]
    cand = {"norm": f"Perron-weighted (q) norm of the certificate, floored at {floor} of max q", "Y0": Y0, "Z1": Z1,
            "Z2a": Z2a, "r_max_tube": r_max, "D2_max_on_tube": float(D2.max()),
            "negative_interval": [float(neg.min()), float(neg.max())] if len(neg) else None,
            "p_min": float(p.min()), "r_at_p_min": float(rs[int(np.argmin(p))]),
            "state_err_adapted_at_r_min": float(rs[int(np.argmin(p))] * Om_q.max()),
            "note": "all constants are upper bounds; Z2(r) <= Z2a r valid for r <= r_max_tube"}
    print("RADII floor", floor, json.dumps({k: cand[k] for k in ("Y0", "Z1", "Z2a", "negative_interval", "p_min")}))
    if len(neg) and (best is None or cand["p_min"] / cand["Y0"] < best["p_min"] / best["Y0"]):
        best = cand
radii = best if best is not None else {"negative_interval": None, "note": "no floor gave p(r) < 0"}
out["radii_polynomial_q_norm"] = radii
print("RADII best", json.dumps(radii, indent=1))
rec = RunRecorder(f"t6_summary_{a.tag}", ROOT)
rec.add("result", out)
print(json.dumps(out, indent=1))
print("manifest:", rec.finish())
