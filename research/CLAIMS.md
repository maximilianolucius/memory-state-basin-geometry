# Claim Registry

**Status:** THEOREM CLOSURE — principal positive claim CONJECTURED WITH STRONG EVIDENCE.

Promotion path:
OPEN -> CONJECTURED -> PROVED/CERTIFIED -> MANUSCRIPT-ELIGIBLE.

## Published prior

### KNOWN-A01 — memory-state semidynamical representation
status: PUBLISHED PRIOR / VERIFIED  
source: Doan & Kloeden 2021.

### KNOWN-A02 — reachable present-state noninjectivity in \(d\ge2\)
status: PUBLISHED PRIOR  
source: Cong & Tuan 2017 + Doan–Kloeden 2021.

### KNOWN-A03 — scalar strict separation
status: PUBLISHED PRIOR  
source: Cong & Tuan 2017, Theorem 4.

### KNOWN-A04 — scalar/triangular attractor classification
status: PUBLISHED PRIOR  
source: Doan & Kloeden 2022.

### KNOWN-A05 — adjacent hereditary/projected basin geometry
status: PUBLISHED PRIOR  
sources: Huang et al. 2014; Daza et al. 2017; Szaksz et al. 2024.

## Proved project reductions / completeness results

### COMPLETENESS-S1 — scalar equilibrium-partition fiber purity
status: PROVED AS CONDITIONAL THEOREM  
class: COMPLETENESS RESULT.

### COROLLARY-S1A — scalar strong-Allee fiber purity
status: PROVED FROM PUBLISHED HYPOTHESES  
class: COMPLETENESS / APPLICATION COROLLARY.

### REDUCTION-M1 — general two-state collision lift
status: PROVED / STANDARD CONSEQUENCE.

### STRUCTURAL-E1 — basin-entry criterion
status: PROVED  
class: STRUCTURAL REDUCTION  
statement:
If
\[
\iota(U_-)\subseteq\mathcal B(A_-),
\]
\[
\iota(p)\in\mathcal B(A_+),\quad A_+\neq A_-,
\]
and
\[
P(p,t_*)\in U_-,
\]
then the reachable fiber at
\[
z=P(p,t_*)
\]
is multibasin.

proof:
\`research/STRUCTURAL_THEOREMS.md\`.

novelty:
not claimed by itself.

### STRUCTURAL-E1A — arc of multibasin fibers
status: PROVED CONDITIONAL ON E1 HYPOTHESES  
statement:
Every time along a nondegenerate orbit interval lying inside \(U_-\) generates a multibasin present-state fiber.

### STRUCTURAL-E2 — open persistence criterion
status: PROVED AS ABSTRACT TOPOLOGICAL CRITERION  
burden:
persistent basin membership, not transversality.

## Model-specific supporting candidate

### CANDIDATE-X1 — cold-start extinction strip
status: PROOF DRAFT COMPLETE / SOURCE-HYPOTHESIS AUDIT PENDING  
model:
\[
{}^C D^\alpha x=x(1-x)(x-\theta)-axy,
\qquad
{}^C D^\alpha y=y(bx-m).
\]

desired:
if
\[
\theta<m/b,
\]
then
\[
R_{\rm ext}=\{0<x<\theta,\ y\ge0\}
\]
satisfies
\[
\iota(R_{\rm ext})\subseteq\mathcal B((0,0)).
\]

proof:
\`research/EXTINCTION_STRIP.md\`.

gate:
ROUND-0003 positivity/comparison/global-continuation audit.

## Compute evidence

### CERT-B1 — Mittag-Leffler collapse root
status: CERTIFIED COMPUTATION  
result:
unique nonreal zero of \(E_{1/2}\) enclosed by Arb/Krawczyk; associated real \(2\times2\) linear system satisfies \(E_{1/2}(A)=0\) exactly.

role:
infrastructure / noninjectivity validation, not principal novelty.

### NUM-W1 — strong-Allee basin-entry witness
status: NUMERICAL CORROBORATION / PRINCIPAL CONJECTURE GENERATOR  
model:
project-constructed positive nontriangular strong-Allee predator–prey system.

parameters:
\[
\theta=0.3,\ a=b=1,\ m=0.8,\ \alpha=0.85.
\]

initial state:
\[
p=(2.4372,2.012).
\]

observed:
the orbit penetrates \(R_{\rm ext}\) with prey margin about \(0.103\) and numerically returns to the coexistence equilibrium.

validation:
three history-retaining solvers, mesh/horizon ladders, 30-digit recomputation, 219 mesh-reliable witnesses in broader scans.

limitation:
survival basin membership is not proved; nonlinear trajectory is not interval-certified.

## Retired principal hypothesis

### OLD CANDIDATE-M2 — transversal collision persistence
status: RETIRED AS PRINCIPAL REQUIREMENT  
reason:
for embedded-age entry \(s=0\), collision equality is automatic and its persistence follows from continuity plus open entry. IFT/transversality matters only for stronger collision-manifold geometry.

## Principal targets

### TARGET-A20 — physically reachable multibasin-fiber existence
status: CONJECTURED — STRONG NUMERICAL WITNESS, NOT PROVED  
remaining proof burden:
1. promote X1;
2. prove survival basin membership for at least one standard initial state;
3. certify or analytically prove entry into \(R_{\rm ext}\);
4. run exact model-specific novelty audit.

### TARGET-A21 — Double-Allee extinction/survival realization
status: OPEN  
TASK-0001:
28 numerical witnesses found in a project-constructed Double-Allee variant, but no published Double-Allee parameterization was reproduced.

ROUND-0003:
recover exact published model(s).

### TARGET-A30 — open-family persistence
status: OPEN / REFACTORED  
correct mechanism:
STRUCTURAL-E2 + persistent extinction/survival basin membership.

transversality:
not required for basic persistence.

### TARGET-A40 — fiber geometry beyond existence
status: DEFERRED.

### TARGET-A50 — fractional-order dependence
status: NUMERICALLY SUPPORTED / THEOREM OPEN  
TASK-0001:
mesh-reliable witnesses observed for \(\alpha\in[0.65,0.92]\); no impossibility conclusion at smaller order.

## Rule

No principal TARGET claim enters manuscript title/abstract/conclusion until basin membership and model-specific novelty are rigorously closed.
