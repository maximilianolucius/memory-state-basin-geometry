# Manuscript Static and Algebra Audit

**Date:** 2026-09-30  
**Scope:** theorem-first LaTeX core, Sections 1--8.

## Static LaTeX audit

Files checked:
- \`paper/manuscript_core.tex\`;
- all \`paper/sections/01_*.tex\` through \`08_*.tex\`;
- \`bibliography/references.bib\`.

Latest automated consistency pass before figure integration:
- labels: 55;
- internal references: 29;
- citations: 38;
- missing labels: 0;
- duplicate labels: 0;
- missing BibTeX keys: 0;
- missing \`\\input\` files: 0;
- unbalanced LaTeX environments: 0.

A minimal local TeX smoke test confirms the required packages and theorem environment setup are installed and compile under the available \`pdflatex\`.

Full-repository compilation was not executed in the local container because that container cannot resolve GitHub; the manuscript files themselves remain audited directly from the repository through the GitHub connector.

## Independent exact algebra audit

The exact B215 algebra was independently recomputed with symbolic arithmetic.

Parameters:
\[
\theta=1/2,\quad a=1/2,\quad b=1,\quad m=4/5.
\]

Equilibrium:
\[
E^*=(4/5,3/25).
\]

Verified Jacobian:
\[
J=
\begin{pmatrix}
-2/25 & -2/5\\
3/25 & 0
\end{pmatrix}.
\]

Verified characteristic polynomial:
\[
\lambda^2+\frac{2}{25}\lambda+\frac{6}{125}=0.
\]

Verified eigenvalues:
\[
\lambda_\pm
=
\frac{-1\pm i\sqrt{29}}{25}.
\]

Verified exact nonlinear remainder for
\[
U=(\xi,\eta)=X-E^*:
\]
\[
N_1
=
-\xi^3-\frac9{10}\xi^2-\frac12\xi\eta,
\qquad
N_2=\xi\eta.
\]

These match the manuscript.

## Logical dependency audit

Principal theorem dependencies are acyclic:

\[
\text{published continuation architecture}
\to
\text{E3/E1}
\]

\[
\text{published viability/comparison}
\to
\text{X1}
\]

\[
\text{published ML/resolvent theory}
\to
\text{M1}
\]

\[
\text{TASK-0006 CAP}
\to
\text{finite entry + M1 constants}
\]

\[
\text{X1 + E3 + E1 + M1}
\to
\text{principal multibasin-fiber theorem}.
\]

No numerical basin label is used as proof.

## Wording audit

The manuscript explicitly avoids:
- a topological arc of distinct fibers;
- parameter-open persistence;
- generic memory novelty;
- trajectory-intersection novelty;
- ecological-model novelty;
- end-to-end interval wording before TASK-0007.

## Next audit trigger

Repeat the static/citation/constant audit after:
1. TASK-0007 arithmetic hardening;
2. insertion of data-dependent figures;
3. journal-template conversion.
