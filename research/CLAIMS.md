# Claim Registry

**Status:** ACTIVE CONSTRUCTIVE FEASIBILITY — principal novelty remains OPEN.

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

### KNOWN-A03 — scalar strict separation
status: PUBLISHED PRIOR  
source: Cong & Tuan 2017, Theorem 4  
scope:
continuous \(f\), global-in-state Lipschitz bound with continuous \(L(t)\).  
warning:
do not use Diethelm & Ford 2012 as load-bearing proof.

### KNOWN-A04 — scalar/triangular attractor classification
status: PUBLISHED PRIOR  
source: Doan & Kloeden 2022  
role:
intervalwise scalar asymptotics and special product-triangular global attractors.

### KNOWN-A05 — adjacent hereditary/projected basin geometry
status: PUBLISHED PRIOR  
sources:
Huang et al. 2014; Daza et al. 2017; Szaksz et al. 2024.

### KNOWN-A06 — comparison principles do not imply endpoint factorization
status: LITERATURE BOUNDARY  
sources:
Wu 2020; Wu 2023; Cheng & Wu 2026.  
consequence:
generic monotonicity is not sufficient for reachable endpoint-fiber purity.

## Proved project results / reductions

### REDUCTION-M1 — collision-to-multibasin lift
status: PROVED / STANDARD CONSEQUENCE  
contribution class: PROJECT REDUCTION, NOT NOVELTY  
statement:
If standard physical IVPs \(p,q\) lie in distinct memory-state basins and
\[
x(t;p)=x(s;q)=x,
\]
then
\[
T_t\iota(p),T_s\iota(q)\in\mathcal F_x
\]
belong to those distinct basins; hence \(\mathcal F_x\) is multibasin.

### COMPLETENESS-S1 — scalar equilibrium-partition fiber purity
status: PROVED AS CONDITIONAL THEOREM  
contribution class: COMPLETENESS RESULT  
statement:
If scalar equilibrium solutions are noncrossable and every equilibrium-separated interval has one basin label, every physically reachable present-state fiber is basin-pure.

proof:
\`research/PURITY_THEOREMS.md\`

novelty audit:
ROUND-0002 = STANDARD CONSEQUENCE.

### COROLLARY-S1A — strong-Allee scalar fiber purity
status: PROVED FROM PUBLISHED HYPOTHESES  
contribution class: COMPLETENESS / APPLICATION COROLLARY  
model:
\[
{}^C D^\alpha x=x(1-x)(x-\theta),
\quad 0<\theta<1.
\]
published model:
Area & Nieto 2023.  
global threshold theorem:
Doan & Kloeden 2022.

conclusion:
\[
0<x<\theta\Rightarrow\mathcal F_x\subseteq\mathcal B(0),
\]
\[
x>\theta\Rightarrow\mathcal F_x\subseteq\mathcal B(1),
\]
\[
\mathcal F_\theta=\{\iota(\theta)\}.
\]

### COMPLETENESS-P2 — triangular basin-determining-coordinate purity
status: VALID CONDITIONAL COROLLARY / NON-PRINCIPAL  
statement:
If a closed scalar coordinate satisfies S1 and its scalar interval determines the full-system asymptotic basin, then reachable full-state fibers are pure.

novelty audit:
ROUND-0002 = USEFUL COMPLETENESS.

## Rejected generalization

### P3 — generic monotone/comparison purity
status: NOT PROMOTED  
reason:
order preservation alone does not make basin membership factor through \(e_0\). Extra endpoint-determining structure is required.

## Structural candidate

### CANDIDATE-M2 — Caputo-specific persistence of inter-basin collision
status: OPEN / NARROWED  
desired:
A nondegenerate inter-basin physical collision persists on an open parameter family after proving exact Caputo solution-map regularity and robust basin-trapping hypotheses.

known-standard component:
parameterized IFT/transversality.

nonstandard burden:
- fixed-lower-terminal Caputo memory;
- exact collision-map regularity;
- basin persistence;
- order regularity if \(\alpha\) varies.

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
natural autonomous continuous multidimensional Caputo family.

### TARGET-A21 — Double-Allee extinction/survival realization
status: OPEN  
desired:
TARGET-A20 in a natural positive strong/Double-Allee system with rigorous basin membership.

### TARGET-A30 — open-family persistence
status: OPEN  
desired:
promote a certified witness to an open parameter/order family via a precisely stated Caputo-specific CANDIDATE-M2.

### TARGET-A40 — fiber geometry beyond existence
status: OPEN / DEFERRED UNTIL A20.

### TARGET-A50 — fractional-order dependence
status: OPEN / DEFERRED.

## Rule

No TARGET claim may enter title, abstract or conclusion until proved/certified at claimed scope and after a model-specific hostile novelty audit.
