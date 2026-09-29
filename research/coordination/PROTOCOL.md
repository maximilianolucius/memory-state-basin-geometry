# Chief ↔ Compute Coordination Protocol

## Ownership
Chief owns:
- scientific direction;
- literature and novelty judgments;
- CLAIMS, NOVELTY_MATRIX, SCOPE_MATRIX;
- theorem statements and proofs;
- paper/.

Compute owns unless otherwise directed:
- computations/;
- tests/;
- generated data;
- generated figures;
- computational return reports.

## Paths
Chief request:
research/coordination/chief-to-compute/TASK-NNNN_<slug>_REQUEST.md

Compute return:
research/coordination/compute-to-chief/TASK-NNNN_<slug>_RETURN.md

Chief decision:
research/coordination/chief-decisions/TASK-NNNN_<slug>_DECISION.md

## Request requirements
Every request states:
- mathematical question;
- required evidence class;
- exact inputs/parameter ranges;
- allowed methods;
- tests;
- expected artifacts;
- stop conditions.

## Return requirements
Every return states:
- task ID;
- branch and final commit SHA;
- environment/dependency versions;
- exact reproduction commands;
- code/output paths;
- tests;
- result;
- evidence label: exact / certified / numerical;
- caveats;
- suggested next question.

## Scientific discipline
A compute return may suggest a conjecture but cannot promote it to a theorem.

Failure to find an example is not proof of impossibility.

A finite-horizon attractor label is not proof of basin membership without a rigorous trapping argument.
