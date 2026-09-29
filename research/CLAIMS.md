# Claim Registry

**Status:** TARGET-A20 CLOSURE ATTEMPT.

## Proved / certified core

### THEOREM-X1 — cold-start extinction strip
status: PROVED FROM PUBLISHED HYPOTHESES.

### STRUCTURAL-E1 — basin-entry criterion
status: PROVED.

### STRUCTURAL-E2 — open persistence criterion
status: PROVED ABSTRACTLY.

### STRUCTURAL-E3 — physical convergence -> continuation-state convergence
status: PROVED.

### STRUCTURAL-E4 — tail anchoring / failure of global-sup convergence
status: PROVED.

### CERT-A2 — finite-time entry of TASK-0001 witness
status: CERTIFIED COMPUTATION  
statement:
the exact binary64-parameter IVP is rigorously enclosed inside \(R_{\rm ext}\) on a nondegenerate time interval, with a representative certified margin about \(0.09848\).

publication caveat:
recertify with exact rational parameters before manuscript.

### CERT-A2B2 / CERT-A2B3 — near-equilibrium entry
status: CERTIFIED COMPUTATION  
role:
proof-oriented candidate search; survival membership still open.

## Principal candidate

### CANDIDATE-L1 — explicit quadratic local survival basin
status: OPEN / ROUND-0004 AUDIT ACTIVE  
statement:
for Hurwitz coexistence Jacobian \(J\), an explicit ellipsoidal local basin follows from a quadratic Caputo Lyapunov inequality plus a rigorous quadratic remainder bound.

file:
\`research/LOCAL_SURVIVAL_BASIN.md\`.

## Principal target

### TARGET-A20 — physically reachable multibasin fiber
status: CONJECTURED / ALL BUT SURVIVAL CLASSIFICATION CLOSED

closed:
- extinction cold start: X1;
- finite-time entry: certified;
- structural lift: E1;
- topology bridge: E3.

remaining:
- rigorous survival-basin membership for one entering standard IVP.

Preferred closure:
CANDIDATE-L1 + TASK-0003 exact-rational witness.

## Novelty discipline

No novelty claimed for:
- ecological vector field;
- fixed-sign Caputo derivative phenomenon;
- validated-integration lemma by itself;
- abstract E1/E3/E4.

Residual novelty remains the rigorous extinction/survival split inside one physically reachable present-state fiber.
