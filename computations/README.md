# Computations — TASK-0001

Compute-agent work for
`research/coordination/chief-to-compute/TASK-0001_validated-collision-search_REQUEST.md`.

Nothing here proves a theorem. Every result carries an evidence label from
`research/coordination/PROTOCOL.md`:
**THEOREM/analytic**, **CERTIFIED COMPUTATION**, **NUMERICAL CORROBORATION**,
**OPEN/CONJECTURE** — plus one project-local refinement,
**CERTIFIED-CONDITIONAL**, meaning "follows by exact algebra from results already
audited in `research/CLAIMS.md` and `research/REFERENCES.md`, but the Compute
Agent does not promote it; the Chief owns the promotion".

## Layout

```
msbg/                  library
  mittag_leffler.py    arbitrary-precision E_alpha (two independent routes) + 2x2 matrix form
  solvers.py           three history-retaining Caputo solvers, batched
  models.py            vector fields, each with an explicit provenance string
  basins.py            conservative outcome classification + certified extinction predicate
  collisions.py        same-age / cross-age collision detection, refinement, Jacobian SVD
  certify.py           Arb ball arithmetic: E_alpha enclosures + Krawczyk root certification
  provenance.py        environment capture, hashing, manifests, fixed seed
scripts/               one script per stage; each writes data/ + manifests/
tests/                 pytest regression suite
data/                  raw machine-readable outputs (json / npz)
manifests/             per-run manifest: environment, parameters, artifact sha256
figures/               figures, each answering one theorem-level question
```

## Solvers

Three solvers, deliberately from two different formulations, none of them a
memoryless one-step surrogate; all retain the full discrete history.

| key | formulation | scheme | nominal order | observed order (Stage A) |
|---|---|---|---|---|
| `pi_rect` | Volterra integral | product-integration rectangle, explicit | `O(h)` | ~1.00 |
| `pece` | Volterra integral | Diethelm-Ford-Freed fractional Adams PECE | `O(h^min(2,1+a))` | 1.27-2.52 |
| `l1` | Caputo derivative | classical L1, implicit (batched Newton) | `O(h^(2-a))` | ~1.00 |

`pi_rect`/`pece` discretise the weakly singular integral; `l1` discretises the
fractional derivative itself. Agreement between the two families is what makes
the cross-check informative.

Batching: M initial conditions are advanced simultaneously with the same weight
vectors, so each history convolution is a single BLAS call. Cost `O(N^2 M d)`,
memory `O(N M d)`.

## Reproducing

```bash
python3 -m venv venv && ./venv/bin/pip install numpy scipy mpmath python-flint matplotlib
export OMP_NUM_THREADS=1                    # one thread per worker process
python scripts/stage_a_validate.py          # solver validation gate
python scripts/stage_b_intersection.py      # certified d=2 non-injectivity
python scripts/stage_c_baseline.py          # baseline + Stage-C halt report
python scripts/stage_d_regime_scan.py       # coarse regime scan  (superseded)
python scripts/stage_d_focus_scan.py        # focused scan        (superseded)
python scripts/stage_d_scan_v2.py           # mesh-validated scan (authoritative)
python scripts/stage_d_witness.py --p <x0> <y0>
python scripts/stage_d_sameage.py --p <x0> <y0>
python scripts/make_figures.py
pytest tests/ -q
```

`scripts/sync_orion.sh` and `scripts/run_orion.sh` push the tree to the ORION
compute host and launch a stage there with one BLAS thread per worker.

### Superseded runs are kept on purpose

`stage_d_regime_scan.py` and `stage_d_focus_scan.py` ran at `h = 0.1`. For
initial states well above the carrying capacity that step is far too coarse:
the reported "margins" of up to 3.35 are discretisation artefacts, and every one
of them leaves the positive cone (`min x < 0`). A direct mesh ladder on the best
of them moved `min x` from 0.118 at `h = 0.1` to 0.369 at `h <= 0.02`. Those runs
and their data are kept in the repository so the correction is auditable;
`stage_d_scan_v2.py` is the authoritative scan.

## Seeds and determinism

`msbg.provenance.SEED = 20260929` is the single project seed. The solvers are
deterministic: `tests/test_solvers.py::test_determinism_bitwise` asserts bitwise
equality across repeated runs, and every manifest records the host, the package
versions, the BLAS build and the artifact hashes.
