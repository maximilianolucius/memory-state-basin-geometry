# Journal Targeting — 2026-09-30

**Status:** Chief recommendation before final template conversion.

## Primary target — Fractional Calculus and Applied Analysis (FCAA)

### Why it fits

FCAA explicitly lists as primary topics:
- fractional calculus;
- fractional-order differential and integral equations and systems;
- mathematical models described by fractional-calculus tools;
- numerical/approximation/computational methods when related to the primary FC topics.

The paper is theorem-centered fractional dynamics, with the ecological model used only as a certified realization.  This matches FCAA more naturally than a journal requiring the application itself to be the main novelty.

### Current submission constraints

Official 2026 author guidance states:
- Original Papers: recommended size up to about 24–30 pages;
- concise presentation is explicitly required;
- LaTeX is obligatory;
- FCAA uses Springer `svjour3`, one-column style;
- abstract: 150–250 words;
- keywords: 4–6;
- references should be placed directly in the LaTeX file in Springer/FCAA style;
- a Data Availability Statement is required for original research;
- hybrid publication model: subscription publication is available without publication fee; OA is optional;
- the journal warns that acceptance is highly selective and processing may be long.

The current generic build is 23 pages, so the manuscript is already in the correct size regime before template conversion.

### Ranking check

External 2025/2024 journal-metrics services report FCAA as Q1.  Re-verify the relevant JCR/Scopus category at the actual submission date.

## Second target — Nonlinear Dynamics

### Why it fits

The official 2026 scope explicitly welcomes:
- fractional-order systems;
- multistability and global transitions;
- ecosystem/population dynamics;
- theoretical analysis;
- computational and numerical methods;
- reproducibility/open-science practices.

This is an excellent dynamics-facing alternative if FCAA rejects on editorial priority.

### Important cost/publishing change

The journal states that submissions received from 11 August 2026 are subject to an APC if accepted because the journal becomes fully open access on 1 January 2027, unless a waiver applies.

Current Scimago 2024 data places Nonlinear Dynamics Q1 in Applied Mathematics and several engineering categories.

## Third target — Journal of Mathematical Analysis and Applications (JMAA)

Official scope includes:
- applied mathematics;
- dynamical systems;
- mathematical biology;
- numerical analysis;
- analytical treatment of novel problems arising in science/engineering.

Strength: high theorem/analysis compatibility.

Risk: the paper must foreground the abstract state-space theorem and analytic chain; the ecological benchmark/computer-assisted proof should remain a certified realization rather than dominate the narrative.

Current Scimago 2024 data reports Q1.

## Fourth target — Chaos, Solitons & Fractals

Scope includes nonlinear dynamics, applied mathematics, systems biology, and computational biology.

However, its current editorial guidance warns that mathematically oriented papers need a clear physical insight/new qualitative feature and that numerical computation should only assist the developed results.  Our paper can satisfy this, but the abstract continuation-state geometry is less naturally positioned here than at FCAA or Nonlinear Dynamics.

Use only after the more natural theorem/fractional venues.

## Chief recommendation

Submission order:

1. **FCAA**
2. **Nonlinear Dynamics**
3. **JMAA**
4. **Chaos, Solitons & Fractals**

Do not convert the only manuscript source destructively.  Keep `paper/manuscript_core.tex` as the neutral theorem source and create a journal-specific FCAA wrapper/template after TASK-0007 freezes the arithmetic wording.

## FCAA conversion checklist

Before submission:
- convert to `svjour3` AuthorsKit;
- reduce keywords from the current list to 4–6;
- keep abstract between 150 and 250 words;
- convert bibliography to FCAA/Springer in-file `thebibliography` format;
- add Data Availability Statement;
- add Competing Interests/Funding declarations as applicable;
- provide author/affiliation/ORCID/corresponding-author metadata;
- export vector artwork in an accepted format and ensure lettering is 8–12 pt at final size;
- preserve the current <=25-page internal target even though FCAA allows approximately 24–30 pages.

## Publication-policy compliance gate

Springer/FCAA's current author guidance contains an explicit policy on LLM use: uses beyond AI-assisted copy editing are subject to disclosure/documentation requirements.  The project must not submit a declaration that conflicts with the target journal's policy.  The authors must resolve the final disclosure wording during the submission-metadata pass.

This compliance item is separate from the scientific content and does not alter TARGET-A20.
