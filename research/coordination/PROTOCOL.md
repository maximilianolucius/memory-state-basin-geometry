# Chief ↔ Compute ↔ Deep Web Search Coordination Protocol

## Repository isolation

All agents have access only to this project repository for project context.

No request may require an agent to read or modify another repository.

All decisive work must be committed here.

## Ownership

### Chief Researcher
Owns:
- scientific direction;
- novelty decisions;
- theorem statements and proofs;
- research/CLAIMS.md;
- research/NOVELTY_MATRIX.md;
- research/SCOPE_MATRIX.md;
- integration of compute and literature evidence;
- paper/;
- final research and publication decisions.

### Compute Agent
Owns, unless directed otherwise:
- computations/;
- tests/;
- generated numerical/certified data;
- generated figures;
- compute return reports.

### Deep Web Search Agent
Owns, unless directed otherwise:
- research/web-search/;
- web-search return reports;
- source-verification notes;
- bibliography/reference corrections arising from assigned searches.

The Search Agent may propose novelty/scope changes, but the Chief owns authoritative matrices and claims.

## Compute task paths

Chief request:
research/coordination/chief-to-compute/TASK-NNNN_<slug>_REQUEST.md

Compute return:
research/coordination/compute-to-chief/TASK-NNNN_<slug>_RETURN.md

## Web-search paths

Chief request:
research/coordination/chief-to-web/ROUND-NNNN_<slug>_REQUEST.md

Web Search return:
research/coordination/web-to-chief/ROUND-NNNN_<slug>_RETURN.md

Substantial report:
research/web-search/YYYY-MM-DD_<slug>.md

## Chief decisions

When a return changes project direction:
research/coordination/chief-decisions/<TASK-or-ROUND>_<slug>_DECISION.md

## Compute request requirements
State:
- mathematical question;
- evidence class;
- exact inputs/ranges;
- allowed methods;
- required tests;
- expected artifacts;
- stop conditions.

## Compute return requirements
State:
- task ID;
- branch/final commit SHA;
- environment/dependency versions;
- reproduction commands;
- code/output paths;
- tests;
- result;
- evidence label;
- caveats;
- next suggested question.

## Web-search request requirements
State:
- precise mathematical claim/question;
- why it matters;
- current believed novelty;
- known closest prior already local;
- mandatory search families;
- adjacent killer theories;
- freshness horizon if relevant;
- required verdicts;
- deliverables.

## Web-search return requirements
State:
- round ID;
- final commit SHA;
- search date;
- coverage;
- strongest direct prior;
- strongest adjacent killer;
- theorem/hypothesis extraction;
- publication status;
- exact residual;
- negative-search limitations;
- bibliography changes;
- recommended next search.

## Evidence hierarchy

- analytic proof in project: THEOREM
- rigorous inclusion/exact machine result: CERTIFIED COMPUTATION
- floating-point experiment: NUMERICAL CORROBORATION
- primary published theorem: PUBLISHED PRIOR
- recent preprint: INTERNAL NOVELTY THREAT, not final manuscript citation
- unresolved: OPEN

## Scientific discipline

A compute return may suggest a conjecture but cannot promote it to a theorem.

A Search return may suggest that a gap survives but cannot declare the project's new theorem novel by fiat.

Failure to find an example is not proof of impossibility.

Failure to find a paper is not proof of absence.

A finite-horizon attractor label is not proof of basin membership without a rigorous trapping argument.

The Chief must explicitly assimilate decisive returns into authoritative project files.
