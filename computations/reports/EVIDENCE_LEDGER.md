# TASK-0001 — evidence ledger

One line per assertion the compute work makes, with its evidence class and the
artifact that backs it. Classes follow `research/coordination/PROTOCOL.md`;
`CERTIFIED-CONDITIONAL` is a project-local refinement meaning "exact algebra on
top of results already audited in `research/CLAIMS.md` / `research/REFERENCES.md`,
awaiting the Chief's promotion".

| # | assertion | class | artifact |
|---|---|---|---|
| 1 | `E_alpha` implementation agrees with `exp`, `e^{z^2}erfc(-z)`, `cosh(sqrt z)`, with a second independent route and with the large-argument asymptote — 43 checks, worst discrepancy 0 at 30 digits | NUMERICAL CORROBORATION (closed-form cross-validation) | `data/stage_a_A1_mittag_leffler.json` |
| 2 | Three history-retaining solvers, two formulations, reach their nominal orders against exact Mittag-Leffler solutions | NUMERICAL CORROBORATION | `data/stage_a_A2_*.json`, `A3`, `A4` |
| 3 | Solvers are bitwise deterministic | NUMERICAL CORROBORATION | `manifests/stage_a_manifest.json` (A5), `tests/test_solvers.py` |
| 4 | Solvers agree with each other on the nonlinear model within their convergence orders | NUMERICAL CORROBORATION | `data/stage_a_A6_cross_solver.json` |
| 5 | `E_{1/2}` has a **unique** zero in an explicit box of radius 1.9e-27 | **CERTIFIED COMPUTATION** (Krawczyk, Arb balls, proved series tail bound) | `manifests/stage_b_manifest.json` (B2) |
| 6 | For `A = [[Re z, -Im z],[Im z, Re z]]` with `z` that zero, `x(1;x_0) = 0` for every `x_0` — present-state observation at `t=1` is constant | THEOREM/analytic (exact algebra), given #5 | `scripts/stage_b_intersection.py` docstring, confirmed in `data/stage_b_B4_*.json` |
| 7 | Equilibria and Caputo stability sectors of the Stage-C′ model | **CERTIFIED COMPUTATION** (exact rational/radical arithmetic) | `manifests/stage_c_manifest.json` (C1/C2) |
| 8 | Mondal et al. (2025) cannot be reproduced from this repository | fact about the repository | `manifests/stage_c_manifest.json` (`missing_information`) |
| 9 | `h <= 0.1` is required for this model class; at `h = 0.08` PECE flips the witness outcome to extinction | NUMERICAL CORROBORATION | `data/stage_c_C6_mesh_sensitivity.json`, `data/stage_d_witness_D1_mesh_ladder.json` |
| 10 | Every constant history in `{0 < x < theta, y >= 0}` goes extinct | **CERTIFIED-CONDITIONAL** (Wu 2020 comparison + COROLLARY-S1A + positivity + `theta < m/b`) | `msbg/basins.py`; falsification test `manifests/stage_d_certified_region_manifest.json` |
| 11 | A survival-bound orbit of the Stage-C′ model enters that region and stays in it for `t in [1.26, 35.74]` | NUMERICAL CORROBORATION (3 solvers x 4 meshes, 5 horizons, 30-digit recomputation) | `manifests/stage_d_witness_manifest.json`, `manifests/stage_d_highprec_manifest.json` |
| 12 | Hence a one-parameter family of multibasin reachable present-state fibres exists | NUMERICAL CORROBORATION, conditional on #10 and #11 | REDUCTION-M1 + #10 + #11 |
| 13 | On the recovery window `x` rises by 0.1034 while `^C D^a x <= -0.0108 < 0` | NUMERICAL CORROBORATION with an exact sign argument for `^C D^a x < 0` | `manifests/stage_d_witness_manifest.json` (D8) |
| 14 | The embedded-age collision map is a submersion in `(p, t)` (singular values 0.244, 0.079) | NUMERICAL CORROBORATION | `manifests/stage_d_witness_manifest.json` (D5) |
| 15 | Under 28 one-at-a-time parameter perturbations the collision is never lost; only basin membership fails (11 times) | NUMERICAL CORROBORATION | `data/stage_d_witness_D6_openness.json` |
| 16 | Witnesses exist for `alpha in [0.65, 0.92]` and in both Allee families; none found at `alpha = 0.55` | NUMERICAL CORROBORATION / **negative search** | `data/stage_d_scan_v2_phase2_results.json` |
| 17 | No same-age inter-basin collision found in two searches; smallest image gap 9.65e-3. The projected Newton was pinned at the trivial root in every wide-box age, so this rests on the grid image gap alone | **negative search**, weakened by two declared limitations | `manifests/stage_d_sameage_manifest.json`, `..._narrowbox_manifest.json` |
| 18 | No interval enclosure of any nonlinear trajectory exists | OPEN (C-A022 unfinished) | — |
