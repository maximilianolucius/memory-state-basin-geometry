# Status

**Phase:** MANUSCRIPT CORE WRITTEN — TARGET-A20 PROVED; NOVELTY AUDIT PASSED; TASK-0007 HARDENING ACTIVE

## Scientific theorem

TARGET-A20 is proved by certified computation under the currently declared arithmetic model.

Final novelty verdict:
[
\boxed{\text{NOVELTY SURVIVES WITH CLAIM NARROWING}.}
]

## Locked principal contribution

For every certified entry time
[
t\in I_*=[5.8576774143,13.7275388580],
]
the reachable present-state fiber
[
\mathcal F_{X(t;p)}
]
intersects both extinction and coexistence basins.

The statement is indexed by a nondegenerate time interval. Injectivity of
[
t\mapsto X(t;p)
]
is not claimed.

## Manuscript progress

The theorem-first body now exists in modular LaTeX:

- `paper/sections/01_introduction.tex`
- `paper/sections/02_state_space.tex`
- `paper/sections/03_scalar_purity.tex`
- `paper/sections/04_model_and_analytic_certificates.tex`
- `paper/sections/05_principal_theorem.tex`
- `paper/sections/06_computer_assisted_validation.tex`
- `paper/sections/07_geometry_and_interpretation.tex`
- `paper/sections/08_discussion_limitations.tex`
- `paper/manuscript_core.tex`

Static manuscript audit:
- 55 labels;
- 29 internal references;
- 38 citations;
- no missing refs;
- no missing BibTeX keys;
- no missing inputs;
- no unbalanced LaTeX environments.

The exact B215 Jacobian/eigenvalues/remainder were independently rechecked symbolically.

## Editorial state

Provisional title/abstract:
`paper/PROVISIONAL_TITLE_ABSTRACT.md`.

Scientific figure plan:
`paper/FIGURE_SPECIFICATIONS.md`.

Referee-facing novelty/evidence boundary:
`paper/REFEREE_POSITIONING.md`.

Target 22--23 pages; hard maximum 25.

## Active compute

TASK-0007:
publication arithmetic hardening of the primary
[
T=300,quad N=12000
]
certificate.

This is a submission-robustness task, not a theorem or novelty gate.

## Next Chief work

- theorem-level figure production;
- final LaTeX integration/page-budget pass;
- incorporate TASK-0007 evidence wording;
- only then freeze title/abstract.
