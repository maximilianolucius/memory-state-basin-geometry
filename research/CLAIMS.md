# Claim Registry

**Status:** PRINCIPAL THEOREM CLOSURE.

## Published prior

### KNOWN-A01 — memory-state semidynamical representation
status: PUBLISHED PRIOR / VERIFIED  
source: Doan & Kloeden 2021.

### KNOWN-A02 — reachable present-state noninjectivity in \(d\ge2\)
status: PUBLISHED PRIOR.

### KNOWN-A03 — scalar strict separation
status: PUBLISHED PRIOR  
source: Cong & Tuan 2017, Theorem 4.

### KNOWN-A04 — scalar/triangular attractor classification
status: PUBLISHED PRIOR  
source: Doan & Kloeden 2022.

### KNOWN-A05 — exact integer-order ecological vector field
status: PUBLISHED PRIOR  
source: Ye et al. 2019.  
statement:
the system
\[
\dot x=x(1-x)(x-\theta)-axy,\qquad
\dot y=y(bx-m)
\]
is already published up to parameter renaming.

### KNOWN-A06 — fixed-order Caputo derivative sign does not determine monotonicity
status: PUBLISHED PRIOR  
source: Diethelm 2016.  
consequence:
the bare sign-vs-monotonicity mechanism is not novelty.

## Proved project results

### COMPLETENESS-S1 — scalar equilibrium-partition fiber purity
status: PROVED AS CONDITIONAL COMPLETENESS RESULT.

### COROLLARY-S1A — scalar strong-Allee fiber purity
status: PROVED FROM PUBLISHED HYPOTHESES.

### STRUCTURAL-E1 — basin-entry criterion
status: PROVED.

### STRUCTURAL-E1A — arc of multibasin fibers
status: PROVED CONDITIONAL ON E1 HYPOTHESES.

### STRUCTURAL-E2 — open persistence criterion
status: PROVED ABSTRACTLY.

### STRUCTURAL-E3 — physical convergence implies continuation-state convergence
status: PROVED.  
statement:
\[
x(t;p)\to x^*,\quad g(x^*)=0
\Longrightarrow
T_t\iota(p)\to\iota(x^*)
\]
in compact-open topology.

### THEOREM-X1 — cold-start extinction strip
status: PROVED FROM PUBLISHED HYPOTHESES  
statement:
for
\[
\theta<m/b,
\]
\[
R_{\rm ext}=\{0<x<\theta,\ y\ge0\}
\]
satisfies
\[
\iota(R_{\rm ext})\subseteq\mathcal B(\iota(0,0)).
\]

dependencies:
Girejko–Mozyrska–Wyrwas 2011; Al-Refai 2012; Wu 2020; Doan–Kloeden 2022; Area–Nieto 2023; Wu–Liu 2020.

## Compute evidence

### CERT-B1 — Mittag-Leffler collapse root
status: CERTIFIED COMPUTATION.

### NUM-W1 — strong-Allee basin-entry witness
status: NUMERICAL CORROBORATION / PRINCIPAL CONJECTURE GENERATOR  
parameters:
\[
\theta=0.3,\ a=b=1,\ m=0.8,\ \alpha=0.85,
\]
\[
p=(2.4372,2.012).
\]
limitation:
survival convergence and finite-time interval certification remain open.

## Principal targets

### TARGET-A20 — physically reachable multibasin-fiber existence
status: CONJECTURED / ONE BASIN HALF NOW PROVED

closed:
- structural E1;
- cold-start extinction X1;
- continuation-state bridge E3.

remaining:
1. prove one standard IVP converges physically to \(E^*\);
2. certify or analytically prove finite-time entry into \(R_{\rm ext}\);
3. final exact theorem-specific novelty audit.

### TARGET-A21 — published Double-Allee realization
status: OPEN / MODEL EQUATIONS VERIFIED  
Mondal 2025:
exact equations recovered; basin parameter table only partially recovered.

### TARGET-A30 — open-family persistence
status: OPEN  
mechanism:
E2 + persistent extinction/survival basin memberships.

### TARGET-A50 — fractional-order dependence
status: NUMERICALLY SUPPORTED / THEOREM OPEN.

## Novelty discipline

Do not claim novelty for:
- the ecological vector field;
- the fixed-sign Caputo derivative phenomenon;
- Double-Allee fractional modeling;
- E1 as abstract logic.

The residual novelty is the rigorous Caputo reachable-fiber extinction/survival theorem.
