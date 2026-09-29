# Agent Directives for a Publication-Ready Mathematical Paper on the First Submission

## Purpose

This document is an operating manual for producing a submission-ready mathematical manuscript whose mathematical claims, novelty positioning, evidence hierarchy, numerical experiments, visual presentation, scope statements, and internal reproducibility checks have already survived the objections that a demanding referee is likely to raise.

No workflow can guarantee acceptance on the first submission. The objective is to **maximize first-submission acceptability by moving reviewer criticism into the pre-submission workflow**.

The directives below are distilled from the gap between an early manuscript centered on a fixed rational benchmark and its substantially strengthened published form. The final manuscript must satisfy the following non-negotiable editorial constraints.

---

# 0. Hard publication constraints

These constraints override every later recommendation. The manuscript is not submission-ready unless all of them are satisfied simultaneously.

1. **Maximum length: 25 pages total.** Treat 25 pages as a hard ceiling for the complete journal-formatted article, including title/abstract, figures, tables, references, declarations, and any material printed with the article. Draft toward **22--23 pages** whenever possible to preserve a typesetting buffer.
2. **No reference to AI, language models, automated drafting, or machine-generated authorship in the manuscript.** The article must read as a conventional mathematical research paper. Do not mention the drafting workflow, prompts, agents, or tool-assisted prose generation.
3. **No supplementary material.** No theorem, proof dependency, dataset description, proof object, figure, or numerical claim required for the paper's conclusions may be deferred to a supplementary PDF, external appendix, online supplement, or separate supporting document. Everything load-bearing must be contained in the main article within the 25-page ceiling.
4. **The paper must be visually rich.** Use numerous high-quality academic figures as part of the mathematical exposition, not as decoration. Target **8--12 figure environments** or roughly **12--20 informative panels**, preferably through compact multi-panel figures. Figures should compress information that would otherwise require long prose or tables.
5. **Figures must be publication-grade.** Prefer vector output (PDF/SVG/EPS according to journal requirements), consistent typography, mathematically meaningful annotations, readable legends, restrained styling, and resolution suitable for print. Avoid decorative effects, 3-D charting, screenshots, low-resolution raster plots, or visually noisy layouts.
6. **Every figure must earn its space.** Each figure must answer a specific theorem-level, robustness, convergence, comparison, or interpretation question and must be explicitly discussed in the text.
7. **Essential reproducibility may exist internally, but it must not become required supplementary material.** Scripts, tests, manifests, and proof-object tooling may be used during research and internal validation; the final article must remain logically complete without asking the reader to consult them.
8. **Do not use unpublished references in the submitted paper.** The bibliography and in-text citations must use formally published sources only. Do not cite arXiv, other preprint servers, working papers, unpublished manuscripts, submitted manuscripts, technical drafts, or personal communications as references supporting the paper. When an unpublished version and a peer-reviewed journal or conference version both exist, cite only the published version and verify its DOI/publisher metadata. If a result is available only in an unpublished form (including arXiv), it must not appear as a bibliographic reference and no manuscript claim may depend on it. Unpublished material may be used internally for literature search and novelty auditing, but never as a final manuscript reference.

### Page-budget discipline

Use an explicit page budget before drafting. A suitable target for a 25-page paper is:

- title + abstract + keywords: ~1 page;
- introduction + related work: ~2.5--3 pages;
- model, nondimensionalization, well-posedness: ~3 pages;
- exact local theory + general atlas: ~4 pages;
- discretization/failure theorem: ~4 pages;
- global results: ~2.5--3 pages;
- numerical/visual corroboration + compact verification discussion: ~4 pages;
- discussion + conclusions: ~1--1.5 pages;
- references + required declarations: ~2--2.5 pages.

If the manuscript exceeds the budget, **compress exposition before weakening mathematics**. Prefer theorem consolidation, compact proofs, multi-panel figures, and deletion of repeated motivation over moving content to supplemental material.

---

# 1. Prime Directive: Find the theorem before writing the paper

Do **not** begin by polishing the introduction, abstract, figures, or prose.

Before drafting, identify the strongest mathematical statement that is:

1. genuinely new relative to the closest literature;
2. stated with explicit hypotheses and quantifiers;
3. valid on a nontrivial parameter set, preferably an open family rather than a single benchmark;
4. analytically proved or rigorously certified;
5. strong enough that the title and abstract can be built around it.

A benchmark, exact rational slice, illustrative parameter set, or attractive figure is **evidence/example**, not the central novelty unless the problem is intrinsically benchmark-specific.

### Mandatory pre-draft question

> If the benchmark values were removed, what theorem would remain?

If the answer is “almost nothing”, the agent must attempt a generalization **before** writing the final manuscript.

---

# 2. Novelty must be mathematical, not cosmetic or combinatorial

Never claim novelty merely because:

- a familiar model contains a slightly different biological mechanism;
- two known ingredients have not previously been placed in exactly the same equation;
- a different parameter set is used;
- a numerical plot looks different;
- a standard stability criterion is applied to a new example;
- a common numerical method is used on a new model.

Instead, seek novelty of one or more of the following forms:

- a general theorem over a parameter family;
- an exact classification or atlas;
- a closed-form threshold/boundary with monotonicity or geometry;
- an impossibility/failure theorem;
- a structural dichotomy;
- a sharpness result;
- a rigorous equivalence or separation between mathematical formulations;
- a proof that a phenomenon occupies an open/non-fine-tuned region of parameter space;
- a theorem explaining why a numerical phenomenon occurs rather than merely displaying it.

### Contribution hierarchy

Every claimed contribution must be tagged internally as one of:

- **NEW THEOREM** - principal novelty;
- **NEW REDUCTION / STRUCTURAL LEMMA** - enables the theorem;
- **COMPLETENESS RESULT** - mathematically useful but based on standard methods;
- **CERTIFIED COMPUTATION** - machine-audited statement with rigorous inclusion semantics;
- **NUMERICAL CORROBORATION** - evidence, never proof;
- **INTERPRETATION** - scientific/methodological meaning;
- **OPEN** - unresolved question.

The manuscript must not blur these categories.

---

# 3. Generalize first; specialize second

A strong workflow is:

1. derive the model for generic admissible parameters;
2. derive equilibrium existence conditions generically;
3. reduce the local stability problem to the smallest number of scalar invariants possible;
4. characterize how those invariants depend on the principal bifurcation/threshold parameter;
5. prove the qualitative structure for a parameter family;
6. identify an explicit open condition under which the desired structure occurs;
7. only then instantiate a benchmark with rational values for exact arithmetic and exposition.

### Required benchmark discipline

A benchmark must be described as:

- exact and reproducible;
- chosen for arithmetic or explanatory convenience;
- **not** evidence of empirical realism unless calibrated;
- an instance of the general theorem, not a substitute for it.

Whenever possible, prove that the benchmark lies in an **open set** of parameter vectors sharing the same structure. This converts “special example” into “robust phenomenon”.

---

# 4. Build a claim registry before prose

Create `CLAIMS.md` or an equivalent machine-readable registry before the manuscript draft.

For every theorem/proposition/lemma/corollary, record:

- claim ID;
- exact statement;
- parameter scope;
- boundary cases;
- dependency list;
- proof status;
- source theorem used from literature;
- whether that source theorem's hypotheses have been checked;
- evidence type: analytic / exact symbolic / certified interval / numerical;
- unresolved equality cases;
- script/test that audits the claim, if applicable.

Example schema:

```text
CLAIM: THM-GENERAL-ATLAS
scope: whole admissible parameter family satisfying H1-H3
status: PROVED
proof_dependencies:
  - EQ-COEXISTENCE
  - TRACE-DETERMINANT-REDUCTION
  - FRACTIONAL-LINEARIZATION-THEOREM
boundary_cases:
  - trace = 0
  - discriminant = 0
  - coexistence endpoint
machine_audit: symbolic/check_atlas.py
numerics_required: no
```

No claim may enter the abstract or conclusion unless it is in this registry.

---

# 5. Audit every theorem imported from the literature

For each external theorem used, the agent must record:

- theorem name/reference;
- exact parameter range;
- regularity hypotheses;
- strict vs. non-strict inequalities;
- dimensional restrictions;
- whether it yields stability, asymptotic stability, instability, existence, uniqueness, etc.;
- whether it applies to the **nonlinear** system or only the linearized one;
- whether the endpoint case must be treated separately.

### Non-negotiable rule

Do not write “by the standard theorem” unless the exact theorem has been checked.

A mathematically correct paper can still be rejected if it invokes a familiar result outside its hypotheses.

---

# 6. Treat critical/equality cases explicitly

A referee will inspect boundaries first.

For every inequality-based classification, enumerate:

- `<` case;
- `=` case;
- `>` case.

If the linear theorem is silent at equality, write **critical / not decided here**, not stable or unstable by continuity or numerical appearance.

Do not turn a linear stability-boundary crossing into a nonlinear bifurcation theorem unless the required nonlinear coefficient or bifurcation hypotheses have been proved.

Examples of forbidden overreach:

- “Hopf bifurcation” from a spectral crossing alone;
- “Neimark-Sacker bifurcation” from a unit-circle crossing alone;
- “periodic orbit” from an oscillatory trajectory;
- “chaos” from irregular numerical output;
- “basin boundary” from a finite grid.

---

# 7. For fractional/nonlocal dynamics, do not import ODE intuition silently

When working with Caputo or other nonlocal derivatives:

1. state the solution concept;
2. state local existence/uniqueness before using trajectories;
3. establish the regularity needed by the Caputo derivative or extremum principle;
4. use a fractional first-contact/extremum argument rather than an unjustified local ODE crossing argument;
5. obtain a priori bounds **before** claiming global continuation;
6. distinguish lack of a semiflow from classical autonomous ODE behavior where relevant.

### Anti-circularity gate

The manuscript must never assume global existence in order to prove the bound that is then used to justify global existence.

Correct order:

`local solution -> invariant/sign bounds on maximal interval -> a priori bound -> continuation theorem -> global existence`.

---

# 8. Nondimensionalization is part of the mathematics

If a fractional order changes, dimensional coefficients may change units with that order. Therefore:

- derive the nondimensional variables explicitly;
- show how each coefficient transforms;
- explain which effective parameters are independent;
- identify any gauge choice that would accidentally constrain the parameter family;
- state exactly what it means to compare different fractional orders at fixed dimensionless coefficients.

Do not merely say “the model is nondimensional” if the validity of an order scan depends on it.

---

# 9. Reduce the stability problem before calculating examples

For a two-dimensional coexistence equilibrium, seek a reduction to invariants such as:

- trace `T`;
- determinant `D`;
- discriminant `Delta = T^2 - 4D`;
- argument of complex eigenvalues;
- algebraic dependence of `T`, `D`, `Delta` on the key parameter.

Then classify the parameter plane symbolically.

Prefer:

> “The classification changes only at the zeros of these algebraic quantities.”

instead of:

> “A dense numerical scan suggests these regions.”

A plot should visualize a theorem, not create one.

---

# 10. If a benchmark yields a clean formula, ask whether the formula reveals a general structure

The agent must attempt the following escalation:

### Level 0 - benchmark observation
A phenomenon occurs at one chosen parameter point.

### Level 1 - benchmark exact theorem
The phenomenon is proved exactly for the benchmark.

### Level 2 - one-parameter exact atlas
The phenomenon is classified over a full interval of a control parameter.

### Level 3 - family theorem
The algebraic mechanism is derived for generic parameters.

### Level 4 - robustness theorem
An explicit open condition is found under which the qualitative atlas persists.

### Level 5 - prevalence/corroboration
Additional generic/irrational parameter sets and a broad ensemble show that the theorem is not a numerical curiosity.

Do not stop at Level 1 or 2 if Level 3 or 4 is realistically attainable.

---

# 11. Separate a surrogate mathematical object from a faithful numerical method

If the paper studies a memoryless map derived from a fractional system, the manuscript must say explicitly whether it is:

- a numerical discretization intended to approximate the fractional problem; or
- an independent surrogate/map studied for comparison.

Do not let readers infer that an inconsistent memoryless map is a faithful fractional integrator.

### Stronger research direction

If the surrogate gives a different stability verdict, do not stop at documenting disagreement. Ask:

1. Is the disagreement true for every step size or only some?
2. Does it extend from Euler to every consistent memoryless one-step method?
3. Is the defect caused by step size/accuracy or by loss of memory?
4. What happens for a history-retaining scheme?
5. Can a faithful scheme reproduce both the correct stability sector and asymptotic decay?

The strongest paper turns an observed discrepancy into a **structural dichotomy theorem**.

---

# 12. Distinguish structural error from numerical error

If a method gives the wrong qualitative verdict, determine whether refining the mesh fixes it.

If no sufficiently small step can recover the correct verdict, the paper should state clearly:

> This is not a coarse-step accuracy defect; it is a structural mismatch between mathematical objects.

Conversely, for a history-retaining method, prove or cite an appropriate stability region and convergence result. Numerical experiments should then corroborate the theorem rather than substitute for it.

---

# 13. Global results must be strengthened until their scope is reviewer-proof

For positivity, boundedness, extinction, and global existence, the agent must ask:

- Are initial conditions unnecessarily restricted?
- Can the bound be made uniform in the initial state?
- Is the extinction region merely sufficient, or can sharpness be proved on an invariant face?
- Does predator extinction actually follow, or is only prey extinction shown?
- Is bistability correctly identified where two equilibria are locally stable?
- Is the basin boundary known? If not, say so.

A stronger global section should ideally contain:

- positivity;
- an upper bound valid on the maximal interval;
- a uniform ultimate bound based only on vector-field parameters;
- global continuation after the bound;
- an extinction strip/funnel;
- extinction of all relevant components;
- a sharpness statement where available;
- a proposition explicitly listing what remains unproved.

---

# 14. Create an explicit “what is and is not proved” proposition

Referees often reject papers for implications the authors never intended but accidentally suggested.

Create a proposition or boxed scope statement that records:

- what local stability implies;
- what it does **not** imply globally;
- whether the basin boundary is known;
- whether global asymptotic stability is proved;
- whether exact periodic orbits are possible under the model class;
- whether asymptotically periodic/long transient behavior is addressed;
- whether control/chaos/bifurcation classification is in scope.

The manuscript should never require the referee to infer the limits of a theorem.

---

# 15. Literature review: build a comparison matrix, not a citation paragraph

Before drafting the related-work section, create a table whose rows are the closest papers and whose columns are the axes on which the present work may differ.

Typical axes:

- model class;
- Allee mechanism;
- derivative/operator;
- local stability criterion;
- parameter-family vs. benchmark analysis;
- exact vs. numerical boundary;
- discretization type;
- memoryless vs. history-retaining;
- global analysis;
- certified computation;
- empirical calibration.

Then write novelty conservatively.

### Required phrasing discipline

Prefer:

> “We do not claim novelty for X, Y, or Z. The new mathematics is A and B.”

This is stronger than an inflated “to the best of our knowledge, this is the first...” claim.

---

# 16. The title must foreground the strongest theorem

The title should name the distinctive result, not the standard machinery.

Weak title pattern:

> Stability, boundedness, and extinction in [model]

Stronger title pattern:

> Exact [structural object] and a [failure/dichotomy/generalization] theorem for [model]

The title should tell an editor why the manuscript is more than another application of a standard criterion.

---

# 17. Abstract architecture

The abstract should contain, in this order:

1. the mathematical object/model;
2. the **general** structural theorem;
3. the key condition or scope of that theorem;
4. the second principal theorem/dichotomy;
5. the strongest global result, briefly;
6. the verification/numerical layer, clearly marked as corroboration/audit;
7. no claim that depends only on a figure.

Avoid spending most of the abstract on benchmark constants.

A benchmark may appear only after the general theorem has been stated.

---

# 18. Numerical experiments and figures must answer theorem-level questions

The paper must be visually rich, but visual density must serve mathematical communication. Every figure/table must have a question.

Examples:

- Does the trajectory change qualitative behavior at the analytically predicted critical order?
- Is the apparent disagreement due to horizon length rather than discretization error?
- Does mesh refinement show the expected convergence order?
- Does the memoryless surrogate remain wrong under refinement?
- Does a history-retaining method recover the analytic verdict?
- Does the mechanism persist for a generic rational set?
- Does it persist for irrational parameters?
- Is the structural condition seen across a large synthetic ensemble?

### Visual-design requirements

Use **8--12 figure environments** when the mathematics supports them, ideally grouped as informative multi-panel figures so that the entire manuscript still fits within 25 pages. Prefer figures such as:

- parameter-plane stability atlases;
- exact boundaries overlaid with numerical corroboration;
- phase portraits or state trajectories for representative regimes;
- time-series comparisons on both linear and logarithmic scales when decay laws matter;
- memoryless-versus-history-retaining comparisons;
- mesh-convergence or error-order plots;
- near-critical horizon-sensitivity panels;
- robustness plots for several parameter sets;
- compact ensemble summaries or heatmaps when they reveal structural prevalence.

Each figure must:

- be legible at final journal column width;
- use consistent fonts and mathematical notation;
- use a coherent, colorblind-aware palette and remain interpretable in grayscale where feasible;
- avoid unnecessary 3-D effects, gradients, oversized legends, chartjunk, and decorative backgrounds;
- use vector graphics whenever practical;
- place units, parameters, thresholds, and critical values directly where they help interpretation;
- have a caption that states the mathematical point, not merely what is plotted;
- distinguish analytic boundaries from numerical samples by line style, markers, or annotation;
- avoid duplicating information already obvious from another figure.

### Mandatory numerical controls

Where applicable:

- self-test the solver on equations with known solutions;
- report observed convergence order;
- perform mesh refinement;
- perform horizon sensitivity near critical boundaries;
- show several initial conditions;
- keep raw machine-readable plot data internally;
- state all parameters, initial conditions, time horizon, and step size in the figure/table or caption.

Never call a finite-horizon simulation “proof of stability”. Figures are corroboration and exposition; the theorem remains the theorem.

---

# 19. Do not use numerics where exact arithmetic decides the issue

If a claim is algebraic, use exact symbolic/rational arithmetic.

Examples:

- exact zero of a trace;
- exact equilibrium coordinate;
- exact rational determinant/discriminant;
- exact factorization;
- exact parameter breakpoint.

An interval containing zero does **not** prove that the value equals zero.

Use certified interval arithmetic only for genuinely non-algebraic quantities or irrational/transcendental enclosures.

---

# 20. Evidence hierarchy must be explicit

Use four labels throughout the project:

## A. Theorem
Analytic proof in the manuscript.

## B. Certified computation
Rigorous enclosure/inclusion with a documented arithmetic backend and checker.

## C. Numerical corroboration
Floating-point simulation/experiment that illustrates or stress-tests a theorem.

## D. Open
Not proved or certified.

Never allow evidence of type C to be described with language belonging to A or B.

---

# 21. Internal verification should strengthen the paper without creating supplementary dependencies

Where feasible, use machine-audited checks internally for delicate constants, algebraic identities, interval inclusions, regression tests, and numerical pipelines. These checks improve reliability, but **the submitted paper must not depend on a supplementary proof-object package**.

For internally audited claims, maintain records containing:

- primitive model parameters;
- claim ID;
- declared parameter interval/box;
- exact or outward-rounded enclosure;
- expected verdict;
- version/schema;
- regression-test status.

### Internal checker requirements

- recompute derived quantities from primitive data;
- do not trust precomputed derived fields;
- use rigorous inclusion semantics when interval arithmetic is invoked;
- return `UNDECIDED`, never false certainty, when an interval straddles a boundary;
- include negative fixtures/tests;
- whenever practical, cross-check key quantities using an independent formulation.

A failed parser, wide interval, missing field, or checker exception is **not** mathematical evidence for the negation of a claim.

The article itself must contain enough mathematics to establish every load-bearing conclusion. Internal verification may be described briefly as an audit or reproducibility check only if journal style permits and space remains, but the reader must not be sent to supplementary material to complete an argument.

---

# 22. Reproducibility must be internal, compact, and non-supplementary

The research project should permit a fresh environment to:

1. re-derive symbolic identities;
2. run internal verification checks;
3. regenerate numerical datasets;
4. rebuild all figures and tables;
5. rebuild the paper.

Keep this workflow in the research repository or working directory. It is a quality-control requirement for the authors, **not a mandatory external supplement to the article**.

A compact internal project structure may be:

```text
paper/
  manuscript.tex
  references.bib
research/
  CLAIMS.md
  NOVELTY_MATRIX.md
  SCOPE_MATRIX.md
computations/
  symbolic/
  numerical/
  validation/
tests/
figures/
data/
README.md
```

Do not refer in the manuscript to unavailable supplemental files, hidden appendices, or external proof objects as necessary support for the results. If a result cannot be justified within the 25-page article, either compress its proof sufficiently to include it or remove/downgrade the claim.

---

# 23. Maintain a scope matrix

Create a table with one row per important statement and columns:

- whole parameter family;
- family under extra condition;
- one-parameter slice;
- benchmark only;
- certified box only;
- numerical observation only.

This prevents accidental promotion of a benchmark fact into a general claim.

---

# 24. Distinguish mathematical interpretation from empirical interpretation

If parameters are not calibrated, say so early and repeatedly enough that no applied claim can be inferred.

The manuscript may explain the mathematical/ecological meaning of a condition, but must separate:

- structural model interpretation;
- empirically measured quantities;
- phenomenological parameters;
- management recommendations.

Do not assign empirical significance to exact rational breakpoints chosen for arithmetic convenience.

---

# 25. Manuscript architecture recommended for this class of paper

The architecture must be designed **for a 25-page ceiling from the start**. Avoid writing a 35-page manuscript and attempting to compress it at the end. Use figures as information-dense mathematical exposition.

A strong default structure is:

## 1. Introduction and closest related work
- problem and conceptual tension/gap;
- closest literature;
- explicit non-novel components;
- exact novelty;
- numbered contributions;
- one compact comparison table only if it saves prose.

## 2. Model, nondimensionalization, and well-posedness
- model and domain;
- nondimensionalization;
- coexistence condition;
- benchmark definition;
- local existence/regularity;
- extremum/first-contact lemma if needed.

## 3. Exact local theory and general stability atlas
- generic equilibrium;
- Jacobian invariants;
- general classification theorem;
- boundary cases;
- parameter-family atlas theorem;
- openness/robustness corollary;
- benchmark as corollary/instance;
- **at least one strong visual atlas figure**, preferably multi-panel.

## 4. Numerical-method/surrogate structural theorem
- precise definition of compared objects;
- failure/inversion theorem;
- parameter-region corollary;
- history-retaining comparison;
- generalization to method class;
- statement of what is not claimed;
- **2--3 compact visual comparisons** where they materially sharpen the theorem.

## 5. Global behavior
- positivity/invariance;
- uniform bound;
- global continuation;
- extinction;
- sharpness/bistability;
- explicit open questions;
- use one phase-plane/time-series figure if it compresses multiple cases effectively.

## 6. Numerical corroboration and compact internal-validation summary
- solver self-tests stated concisely;
- critical-boundary experiments;
- convergence/horizon sensitivity;
- structural dichotomy visualized;
- multiple initial states;
- additional parameter sets;
- broad ensemble summary if it provides meaningful robustness evidence;
- no supplementary-material dependency.

## 7. Discussion and conclusions
- what is new vs. completeness;
- methodological meaning;
- applied interpretation limits;
- evidence boundaries;
- open problems;
- concise conclusion.

### Compression rules

- Prefer theorem consolidation over many tiny propositions.
- Prefer a 2x2 or 1x3 multi-panel figure over three separate pages of plots.
- Move derivational algebra into compact displayed identities when it remains readable.
- Delete repeated explanations after a theorem has been established.
- Keep only tables that replace substantial prose.
- Do not create a supplementary appendix as a pressure-release valve.
- If an appendix is unavoidable, it must remain part of the main 25-page article and contain only essential material.

---

# 26. Referee attack simulation

Before submission, perform at least three independent adversarial referee passes.

## Referee A - Mathematical rigor
Ask:

- Is any theorem used outside its hypotheses?
- Are equality cases mishandled?
- Is global existence circular?
- Are nonlocal dynamics treated as if they were ODEs?
- Are quantifiers correct?
- Is every “if and only if” proved both ways?
- Is the claimed uniqueness local or global?
- Is a numerical zero being treated as exact?

## Referee B - Novelty and literature
Ask:

- Which exact theorem is new?
- Does a close paper already contain the same mechanism?
- Is this only a parameter change?
- Is the benchmark special/fine-tuned?
- Are standard results being marketed as contributions?
- Is the literature comparison fair and sufficiently close?

## Referee C - Computation/reproducibility
Ask:

- Can every figure be regenerated?
- Are solver convergence and horizon effects separated?
- Are proof objects independently checkable?
- Can a certificate fail safely?
- Are raw data and scripts consistent with captions?
- Are random experiments reproducible from a seed/specification?

No final submission until all three referee reports are answered in `PRE_SUBMISSION_RESPONSE.md`.

---

# 27. Red-team the abstract and conclusion separately

For every sentence in the abstract and conclusion, attach one of:

- theorem/proposition ID;
- certified-object ID;
- numerical-figure/table ID;
- literature citation;
- interpretation label.

Delete any sentence that cannot be traced to one of those objects.

The abstract and conclusion must not contain stronger claims than the body.

---

# 28. Editorial quality gates

Before submission verify:

- complete journal-formatted manuscript is **<= 25 pages**;
- target draft length was kept near 22--23 pages to absorb final typesetting changes;
- the manuscript contains no reference to AI, language models, automated drafting, agents, prompts, or machine-generated authorship;
- no essential claim depends on supplementary material or an external appendix;
- the visual program is substantial: typically 8--12 figure environments / 12--20 informative panels when scientifically justified;
- every figure is publication-grade, legible at final size, mathematically motivated, and explicitly discussed;

- title foregrounds the strongest theorem;
- abstract states the general result before benchmark values;
- all notation is introduced once and used consistently;
- theorem statements are readable without searching several pages backward;
- every figure is cited and discussed;
- captions state what is analytic vs. numerical;
- related work identifies the closest competitors, not just broad background;
- novelty claims are conservative;
- limitations/open problems are explicit;
- no placeholder DOI, author metadata, anonymous-review artifact, or draft-only language remains;
- **no bibliography entry or in-text citation uses an unpublished source (including arXiv/preprints, working papers, submitted manuscripts, technical drafts, or personal communications); all cited works are formally published and use verified journal/conference/publisher metadata and DOI where available;**
- journal template, bibliography style, MSC/keywords/data statement/funding statement are complete where required.

---

# 29. Forbidden failure modes

The agent must not:

1. write the paper around a single attractive benchmark before attempting generalization;
2. equate “not previously combined” with mathematical novelty;
3. use a memoryless map as if it were a faithful Caputo integrator;
4. claim a Hopf/Neimark-Sacker bifurcation from a linear crossing alone;
5. infer a continuum theorem from a finite parameter grid;
6. infer exact equality from floating point or an interval containing zero;
7. treat rejected/failed certificate output as a mathematical counterexample;
8. call simulations “proof”;
9. assert global existence before proving an a priori bound;
10. hide unresolved boundary cases;
11. describe a benchmark statistic as ecologically meaningful without calibration;
12. claim “first” without a close-literature comparison;
13. bury the actual novelty under standard boundedness/stability calculations;
14. add computation that does not answer a theorem-level question;
15. submit with a reproducibility promise that substitutes for a proof that should be present in the article;
16. exceed the 25-page ceiling and attempt to repair the excess by moving mathematics to supplementary material;
17. refer in the manuscript to AI, language models, drafting agents, prompts, or automated authorship;
18. use low-resolution, decorative, redundant, or poorly annotated graphics;
19. underuse figures when a precise atlas, phase portrait, convergence plot, or multi-panel comparison would communicate the mathematics more efficiently;
20. make any principal conclusion depend on material not contained in the main article;
21. cite unpublished material in the submitted manuscript or bibliography, including arXiv/preprints, working papers, submitted or unpublished manuscripts, technical drafts, or personal communications. If a required result exists only in unpublished form, replace it with a published source or remove/downgrade the dependent claim.

---

# 30. Definition of Done

The manuscript is ready for first submission only when all of the following are true.

## Hard constraints
- [ ] Final journal-formatted article is **<= 25 pages total**.
- [ ] No reference to AI, language models, automated drafting, agents, prompts, or machine-generated authorship appears in the manuscript.
- [ ] No supplementary material is required or presented as necessary support for the paper.
- [ ] Every bibliography entry and in-text citation points to a formally published source; no arXiv/preprint, working paper, unpublished/submitted manuscript, technical draft, or personal communication is cited. DOI/publisher metadata are verified where available.
- [ ] Every load-bearing theorem, definition, methodological qualification, and numerical specification required to understand the conclusions is contained in the main paper.
- [ ] The paper contains a strong visual program, normally 8--12 figure environments / 12--20 informative panels when justified by the mathematics.
- [ ] Figures are publication-grade, visually coherent, legible at final size, and each answers a specific scientific or mathematical question.

## Mathematics
- [ ] Principal novelty exists as at least one explicit theorem.
- [ ] Benchmark results are generalized as far as reasonably possible.
- [ ] All theorem hypotheses are audited.
- [ ] Boundary/equality cases are explicit.
- [ ] No circular existence/boundedness reasoning remains.
- [ ] Scope of every claim is recorded.
- [ ] Open problems are separated from proved statements.

## Novelty
- [ ] Closest-work comparison matrix exists.
- [ ] Standard/known ingredients are explicitly acknowledged as such.
- [ ] New mathematics can be stated in <= 3 sentences.
- [ ] Title and abstract foreground that new mathematics.

## Computation
- [ ] Exact claims use exact arithmetic where possible.
- [ ] Certified claims use rigorous inclusion semantics.
- [ ] Numerical figures are corroboration, not proof.
- [ ] Solver has self-tests and convergence checks.
- [ ] Critical-boundary experiments include horizon sensitivity.
- [ ] Additional parameter sets test robustness.
- [ ] Broad ensemble experiments, if used, have a declared sampling measure and no false empirical interpretation.

## Reproducibility
- [ ] One fresh-run workflow regenerates symbolic results.
- [ ] Figures/tables regenerate from saved machine-readable data.
- [ ] Internal validation records are complete for all audited claims.
- [ ] Negative fixtures exist for internal checkers.
- [ ] A fresh internal environment can rebuild the manuscript and all figures.
- [ ] None of these internal artifacts is required as supplementary material for logical completeness.

## Editorial
- [ ] Journal formatting is complete.
- [ ] Related work is current and specific.
- [ ] Abstract/conclusion claims are traceable.
- [ ] Limitations are explicit but do not obscure the main theorem.
- [ ] No draft-only metadata or placeholders remain.

---

# 31. Final operating prompt for the writing agent

Use the following as the controlling instruction:

> **Produce a submission-ready mathematical paper, not a polished draft. The final journal-formatted article must be complete in no more than 25 pages, must contain no reference to AI, language models, automated drafting, prompts, agents, or machine-generated authorship, must not rely on or present supplementary material, and must contain no unpublished references in its citations or bibliography—including arXiv/preprints, working papers, submitted or unpublished manuscripts, technical drafts, or personal communications; cite only formally published sources with verified journal/conference/publisher metadata and DOI where available, and do not rely on an unpublished source for any manuscript claim. Begin by identifying and proving the strongest general theorem supported by the project. Treat benchmark calculations as instances, not novelty, unless generalization is impossible and you can justify why. Build a claim registry, theorem-dependency graph, novelty matrix, and scope matrix before final prose. Audit every imported theorem and every equality/critical case. For nonlocal fractional dynamics, justify solution regularity and use appropriate fractional first-contact/comparison arguments; never import ODE intuition silently. Separate analytic proof, internally certified computation, numerical corroboration, interpretation, and open problems. If a numerical surrogate disagrees with the continuous model, determine whether the discrepancy is structural, generalize it to the largest method class you can prove, and compare against a faithful history-retaining method. Use exact arithmetic for algebraic claims and rigorous interval arithmetic only where genuinely needed. Make the paper visually rich: target approximately 8--12 publication-quality figure environments or 12--20 informative panels, using compact multi-panel designs where possible. Every figure must answer a theorem-level, convergence, robustness, comparison, or interpretation question; figures must be high-resolution/vector where practical, consistently styled, visually clear, and fully legible at final journal size. Use figures to compress exposition and help remain inside the 25-page ceiling. Perform solver self-tests, mesh convergence, and horizon sensitivity near critical boundaries. Position novelty through a closest-work comparison matrix and explicitly state which familiar ingredients are not new. The title and abstract must foreground the strongest new theorem. Before submission, run independent adversarial referee audits for rigor, novelty, computation, page economy, and visual quality, then resolve every substantive objection in the manuscript or scope statements. Do not submit until every abstract/conclusion claim has a traceable proof, internal validation record, numerical object, citation, or clearly labeled interpretation, and until the complete article satisfies the 25-page/no-supplement/no-AI-reference constraints.**

---

# 32. The central lesson

The difference between an early technically competent manuscript and a publishable version is often **not more prose**. It is a change in the mathematical center of gravity:

- from **one benchmark** to **a parameter-family theorem**;
- from **an observed discrepancy** to **a structural failure theorem**;
- from **a surrogate warning** to **a memoryless/history-retaining dichotomy**;
- from **restricted bounds** to **scope-clean global results**;
- from **future verification plans** to **strong internal validation with a self-contained main text**;
- from **one illustrative plot** to **a dense, publication-grade visual program that communicates the theorems efficiently**;
- from **broad novelty language** to **a precise closest-work comparison**;
- from **implicit caveats** to **explicit evidence and scope boundaries**.

That transformation should happen **before** the first submission, not during peer review. It must also be achieved **inside a self-contained article of at most 25 pages**, without supplementary dependencies and with figures treated as first-class mathematical exposition.
