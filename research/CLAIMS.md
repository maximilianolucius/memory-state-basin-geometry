# Claim Registry

**Status:** ACTIVE FEASIBILITY — principal novelty still OPEN.

Promotion path:
OPEN -> CONJECTURED -> PROVED/CERTIFIED -> MANUSCRIPT-ELIGIBLE.

## Published prior

### KNOWN-A01 — memory-state semidynamical representation
status: PUBLISHED PRIOR  
source: Doan & Kloeden 2021  
audit: ROUND-0001 VERIFIED.

### KNOWN-A02 — reachable present-state noninjectivity in \(d\ge2\)
status: PUBLISHED PRIOR  
source: Cong & Tuan 2017 + Doan & Kloeden 2021.

### KNOWN-A03 — scalar nonintersection
status: PUBLISHED PRIOR  
source: Cong & Tuan 2017; Diethelm & Ford 2012  
exact hypothesis audit: ROUND-0002 pending.

### KNOWN-A04 — adjacent hereditary/projected basin geometry
status: PUBLISHED PRIOR  
sources:
- Huang et al. 2014;
- Daza et al. 2017;
- Szaksz et al. 2024.
consequence:
No broad novelty claim may be based on history-space basins or headpoint/present-state basin projection alone.

### KNOWN-A05 — projected overlap/intersection in fractional maps
status: PUBLISHED PRIOR / NUMERICAL-ADJACENT  
source: Edelman 2011.
consequence:
No broad novelty claim may state merely that fractional memory can yield projected trajectory/attractor overlap.

## Proved reductions / completeness machinery

### REDUCTION-M1 — collision-to-multibasin lift
status: PROVED / STANDARD CONSEQUENCE  
contribution class: NEW PROJECT REDUCTION, NOT CLAIMED AS NOVEL THEOREM  
statement:
If standard physical IVPs \(p,q\) lie in distinct memory-state basins and
\[
x(t;p)=x(s;q)=x
\]
for some \(t,s\ge0\), then
\[
T_t\iota(p),T_s\iota(q)\in\mathcal F_x
\]
belong to those distinct basins. Hence \(\mathcal F_x\) is multibasin.

dependencies:
- Doan–Kloeden semigroup architecture;
- positive basin invariance.
novelty audit:
ROUND-0001 = STANDARD CONSEQUENCE.

### COMPLETENESS-S1 — scalar equilibrium-partition fiber purity
status: PROOF DRAFT COMPLETE / IMPORTED HYPOTHESES PENDING  
statement:
If scalar equilibrium solutions are noncrossable and the equilibrium-separated intervals of standard initial data each belong to a single asymptotic basin, then every physically reachable present-state fiber is basin-pure.

proof:
\`research/PURITY_THEOREMS.md\`

novelty:
not claimed; ROUND-0002 dispatched.

## Structural candidate

### CANDIDATE-M2 — Caputo-specific persistence of inter-basin collision
status: OPEN / NARROWED  
desired:
A nondegenerate inter-basin physical collision persists on an open parameter family after proving the exact Caputo solution-map regularity and robust basin-trapping hypotheses.

known-standard component:
parameterized implicit-function/transversality mechanism.

nonstandard burden:
- fixed-lower-terminal Caputo memory;
- exact regularity of the collision map;
- basin persistence;
- order regularity if \(\alpha\) varies.

novelty audit:
ROUND-0001 = ADJACENT SUBSUMPTION of method, no direct target theorem found.

## Purity candidates

### CANDIDATE-P2 — triangular observable-determining purity
status: OPEN  
desired:
A closed scalar coordinate satisfies COMPLETENESS-S1 and determines the full-system asymptotic basin.

ROUND-0002: dispatched.

### CANDIDATE-P3 — comparison-dominated purity
status: OPEN  
desired:
Identify additional order/comparison hypotheses under which basin membership factors through the present-state observation.

warning:
Order preservation alone is not assumed sufficient.

ROUND-0002: dispatched.

## Principal targets

### TARGET-A20 — physically reachable multibasin-fiber existence
status: OPEN — PRINCIPAL TARGET  
desired:
\[
e_0(\phi)=e_0(\psi)=x,\qquad
\phi\in\mathcal B(A_1),\qquad
\psi\in\mathcal B(A_2),\qquad A_1\neq A_2,
\]
with \(\phi,\psi\in\mathcal R_\alpha\).

scope target:
natural autonomous continuous Caputo family, not arbitrary ambient histories and not one isolated benchmark.

ROUND-0001:
no direct strict positive prior found in searched corpus.

### TARGET-A21 — Double-Allee extinction/survival realization
status: OPEN  
desired:
TARGET-A20 in a natural positive strong/Double-Allee system with rigorous basin membership.

### TARGET-A30 — open-family persistence
status: OPEN  
desired:
promote a certified positive witness to an open parameter/order family using a precisely stated Caputo-specific version of CANDIDATE-M2.

### TARGET-A40 — fiber geometry beyond existence
status: OPEN / DEFERRED UNTIL A20  
desired:
regularity/topology/multiplicity/local dimension under explicit hypotheses.

### TARGET-A50 — fractional-order dependence
status: OPEN / DEFERRED  
warning:
continuity in \(\alpha\) is not sufficient for every IFT formulation; derivative regularity must be established if used.

## Rule

No TARGET claim may enter title, abstract or conclusion until proved/certified at its stated scope and after a model-specific hostile novelty audit.
