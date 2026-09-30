# Related-Work Positioning Map

**Status:** locked for Introduction/Related Work draft  
**Date:** 2026-09-30

The purpose of this file is to prevent novelty drift while drafting.

## 1. Continuation-state architecture

### Doan--Kloeden
\cite{DoanKloeden2021Semidynamical,DoanKloeden2024Attractors}

Already establishes:
- autonomous Caputo continuation-state semidynamical systems;
- infinite-dimensional state representation;
- attractor framework.

Our paper must treat this as foundational background.

Our contribution begins only after defining the reachable present-state fiber
\[
\mathcal F_z=e_0^{-1}(z)\cap\mathcal R_\alpha.
\]

## 2. Fractional trajectory intersections

### Deshpande--Daftardar-Gejji--Vellaisamy
\cite{DeshpandeDaftardarGejjiVellaisamy2019}

Already establishes:
- trajectory intersections/self-intersections in linear fractional systems.

Therefore do not claim:
- first same-present coincidence;
- first fractional nonintersection failure;
- first projected-state collision.

Our theorem is about **basin membership inside a physically reachable fiber**, not intersection geometry alone.

## 3. Closest hereditary/headpoint analogue

### Szaksz--Stepan--Habib
\cite{SzakszStepanHabib2024DynamicalIntegrity}

Already emphasizes:
- a delay-system future depends on the whole history, not only the headpoint;
- constrained histories with the same headpoint can evolve differently;
- restarting at a previously visited headpoint changes the inherited history.

Why it is not the same theorem:
- no proof that the same-headpoint states lie in distinct asymptotic basins;
- delay-state architecture differs from the Doan--Kloeden Caputo continuation state;
- our theorem is restricted to physically reachable Caputo continuation states.

Manuscript wording:
> The closest conceptual analogue occurs in dynamical-integrity methods for delay systems, where histories sharing a headpoint need not reproduce the inherited trajectory; the present result instead certifies opposite basin membership at the identical current value in an autonomous Caputo continuation-state system.

## 4. Fractional ecological memory and Allee effects

### Ramesh et al. 2025
\cite{RameshEtAl2025MemoryDoubleAllee}

### Mondal et al. 2025
\cite{MondalEtAl2025Consequences}

### Wang--Han 2025
\cite{WangHan2025Allee}

### Saha et al. 2026
\cite{SahaEtAl2026AlleeBasin}

### Pippal--Sati 2026
\cite{PippalSati2026}

These collectively cover substantial parts of:
- fractional predator--prey memory;
- Allee effects;
- extinction/coexistence states;
- stability/bifurcation;
- explicit fractional ecological basins.

Therefore do not claim novelty for any of those ingredients individually.

The distinction to state explicitly:
> Existing ecological basin analyses classify outcomes by their chosen initial-data representation.  Our theorem compares two continuation states with the identical present physical value and proves that their different inherited memories place them in different basins.

## 5. Exact ecological vector field

### Ye et al. 2019
\cite{YeEtAl2019StrongAlleePredatorPrey}

The integer-order vector field is prior.

Use wording such as:
> We use the Caputo fractionalization of a previously studied strong-Allee predator--prey vector field as a transparent positive testbed for the state-space theorem.

Do not imply a new biological mechanism.

## 6. Validated numerics / CAP

Relevant published framework:
\cite{Becker2011WeaklySingularResolvents,BrunnerPedasVainikko1999WeaklySingularCollocation,BredenLessard2018PolynomialCAP,ChurchQueirolo2024HopfCAP,YazdaniHadizadeh2012IntervalVolterraFredholm,SalasAltamiranoMartinez2026CertifiedML}.

Position:
- sophisticated enabling proof technology;
- no broad claim of first rigorous fractional computation;
- exact combination may be unusual, but numerical-method novelty is not needed for the paper.

## 7. Defensible novelty paragraph template

The manuscript may say, after the above boundaries are established:

> These lines of work separately establish Caputo continuation-state dynamics, fractional trajectory intersections, history-sensitive headpoint dynamics in delay systems, and multistable fractional ecological basins.  The question addressed here is narrower: can two physically reachable continuation states of an autonomous Caputo system have exactly the same current physical value while belonging to different asymptotic basins?  Our certified strong-Allee example answers this affirmatively for extinction versus coexistence over a nondegenerate interval of reached times.  No formally published theorem establishing this same-present-value, physically reachable Caputo basin split was identified in our targeted literature audit.

Do not strengthen this paragraph to an absolute priority claim.
