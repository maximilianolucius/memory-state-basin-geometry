# Status

**Phase:** MANUSCRIPT CORE BUILT — TASK-0007 PUBLICATION HARDENING ACTIVE

## Scientific theorem

TARGET-A20 is proved by certified computation under the currently declared arithmetic model.

Final novelty verdict:
\[
\boxed{\text{NOVELTY SURVIVES WITH CLAIM NARROWING}.}
\]

## Locked principal contribution

For every
\[
t\in I_*=[5.8576774143,13.7275388580],
\]
the reached physical value \(X(t;p)\) has a physically reachable present-state fiber that intersects both extinction and coexistence basins.

This is a nondegenerate time-interval statement. Injectivity of
\[
t\mapsto X(t;p)
\]
is not claimed.

## Manuscript state

The theorem-first manuscript now has:
- title/abstract/keywords draft;
- Sections 1--9 in modular LaTeX;
- explicit compact-open basin definition;
- cutoff localization putting the polynomial B215 witnesses inside the published Doan--Kloeden global-Lipschitz framework;
- X1, M1, principal theorem, and self-contained CAP criterion;
- certified-entry, same-present, CAP-architecture, amplification, and memory-tail figures;
- prior-art and certificate tables;
- reproducibility statement.

A successful GitHub Actions LaTeX/BibTeX build at manuscript commit
`0d96a99c5ac5d9a75ef1aa4431150b981cf460fc`
produced **23 pages**.

The post-cutoff / visual-cleanup build is the current CI target and must remain \(\le25\) pages.

## Referee passes

- Pass 1 — theorem chain: **PASS WITH MINOR FIXES**, all fixes incorporated.
- Pass 2 — imported theorem hypotheses: cutoff issue identified and now **RESOLVED / PASS**.
- Pass 3 — deferred until TASK-0007 and final data-dependent figures.

## Bibliography

Current manuscript citation set:
- 24 unique references;
- formally published only;
- no arXiv/preprints/unpublished citations.

## Active compute

TASK-0007 hardens the arithmetic of the primary
\[
T=300,\quad N=12000
\]
certificate.

This is submission robustness, not a theorem or novelty gate.

## Chief next steps

1. verify post-cutoff LaTeX build and page count;
2. visually inspect cleaned manuscript PDF;
3. generate committed-data figures after TASK-0007;
4. incorporate hardened arithmetic wording;
5. run Referee Pass 3;
6. freeze final title/abstract and journal template.
