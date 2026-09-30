# Manuscript Plan

**Status:** ACTIVE  
**Target length:** 22–23 pages; hard maximum 25 pages.

## Working title candidates

Preferred:

**Reachable Present-State Fibers Crossing Extinction and Coexistence Basins in an Autonomous Caputo System**

Alternatives:

- **Memory-State Basin Geometry in an Autonomous Caputo System: A Certified Extinction–Coexistence Fiber Split**
- **Same Present, Different Basins: Certified Memory-State Geometry in a Caputo Predator–Prey System**

The final title should avoid “first” and should foreground the basin theorem rather than the ecological model alone.

## Core theorem statement

For the exact B215 system

\[
{}^CD^{17/20}x=x(1-x)(x-1/2)-\tfrac12xy,
\qquad
{}^CD^{17/20}y=y(x-4/5),
\]

with
\[
p=(277/100,467/1000),
\]
the exact standard trajectory enters the cold-start extinction strip over a nondegenerate certified interval while the inherited trajectory converges to
\[
E^*=(4/5,3/25).
\]

Thus for every reached present \(z\) along that interval, the reachable continuation state and canonical cold start at the identical present \(z\) lie in distinct asymptotic basins.

## Proposed section architecture

### 1. Introduction and precise contribution — 2.0–2.5 pp
- physical-state ambiguity versus memory-state basin membership;
- closest prior;
- exact theorem contribution;
- no broad priority claims.

### 2. Caputo continuation state and basin fibers — 2.5 pp
- Doan–Kloeden state space;
- \(T_t\), \(e_0\), \(\iota\);
- reachable set and fiber \(F_z\);
- E1 structural lemma.

### 3. Why scalar threshold intuition is insufficient — 2.0 pp
- scalar purity result;
- cold-start interpretation;
- contrast motivating two-dimensional mechanism.

### 4. Strong-Allee model and analytic basin certificates — 3.0 pp
- generic model;
- equilibria;
- X1 extinction region;
- coexistence linearization;
- M1 tail theorem.

### 5. Certified multibasin fiber theorem — 3.0 pp
- exact B215 data;
- certified entry interval;
- certified survival;
- TARGET-A20 theorem and corollary for the reached arc.

### 6. Computer-assisted validation — 4.0–4.5 pp
- Volterra source equation;
- orbit-linearized inverse;
- cellwise sup/oscillation/bubble bounds;
- \(F(b)<b\);
- Perron contraction;
- primary \(T=300\) certificate;
- \(T=1000\) redundancy;
- arithmetic model stated explicitly.

### 7. Geometry, diagnostics, and interpretation — 2.5–3.0 pp
- physical trajectory;
- threshold excursion;
- present-state fiber schematic;
- why scalar Gronwall bounds fail;
- sign-aware amplification;
- memory-tail decomposition.

### 8. Discussion and limitations — 1.0–1.5 pp
- no claim of generic memory novelty;
- no parameter-open family yet;
- ecological interpretation bounded;
- computational-proof boundary.

### References/declarations — 2.0–2.5 pp

## Figure plan

Target 8 figure environments / approximately 12–16 panels:

1. memory-state fiber geometry schematic;
2. B215 physical trajectory and extinction strip;
3. time series with certified entry interval;
4. inherited continuation versus cold-start future from same \(z\);
5. CAP tube over the excursion;
6. sign-aware versus absolute-value amplification;
7. cellwise CAP quantities / adaptive mesh and defect distribution;
8. M1 tail budget and independent \(T=300/T=1000\) certificate comparison.

Every figure must support a theorem/proof/interpretation point.

## Tables

Keep to 2–3 compact tables:
- theorem/certificate constants;
- closest-prior comparison;
- evidence hierarchy or redundancy summary.

## Citation boundaries

Formally published sources only.

Mandatory conceptual positioning:
- Doan–Kloeden continuation-state framework;
- Deshpande et al. trajectory intersections;
- Szaksz–Stepan–Habib same-headpoint delay analogue;
- strongest recent fractional ecological basin papers;
- published validated-numerics precedents.

## Drafting rule

Do not write title/abstract first.

Build theorem/proof sections before introduction prose.


## Precision lock added 2026-09-30

The manuscript must distinguish a nondegenerate **time interval of certified multibasin fibers** from a topological arc of distinct physical states.  Injectivity of (t\mapsto x(t;p)) on (I_*) is not currently part of the certificate.
