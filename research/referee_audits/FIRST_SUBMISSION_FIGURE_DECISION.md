# First-Submission Figure Decision

**Date:** 2026-09-30

## Decision

Use at most **6 figure environments** in the first submission.

### Keep

1. reachable present-state fiber geometry — conceptual definition;
2. certified threshold-entry interval — theorem evidence;
3. same-present extinction/coexistence split — principal theorem;
4. CAP architecture — proof logic;
5. sign-aware amplification diagnostic — method motivation;
6. memory-tail budget — infinite-time survival certificate.

### Do not include by default

- raw/numerical phase-plane trajectory;
- adaptive-mesh / defect-distribution figure;
- separate time-series figure duplicating the certified-entry figure;
- detailed CAP component plots.

These remain reproducible through `computations/scripts/make_paper_figures.py` and can replace, rather than supplement, a manuscript figure if the journal/referee requests them.

## Rationale

The successful pre-cutoff LaTeX build is already 23 pages.  The first submission must foreground the theorem and proof, not numerical diagnostics.  Every retained figure either defines the new geometric object, certifies a load-bearing inequality, or explains an indispensable proof mechanism.

## Compression fallback

If the post-cutoff journal-formatted manuscript exceeds 25 pages, remove the amplification diagnostic first.  Its content is numerical motivation and is not load-bearing.
