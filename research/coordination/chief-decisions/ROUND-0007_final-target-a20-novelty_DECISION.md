# ROUND-0007 — CHIEF DECISION

**Date:** 2026-09-30  
**Disposition:** ACCEPT — NOVELTY SURVIVES WITH CLAIM NARROWING; MANUSCRIPT UNLOCKED

## 1. Final novelty verdict

The final hostile audit returns:

\[
\boxed{\text{NOVELTY SURVIVES WITH CLAIM NARROWING}.}
\]

No formally published direct prior was identified that proves the completed conjunction:

1. autonomous continuous-time Caputo dynamics;
2. a physically reachable inherited continuation state of a standard point IVP;
3. the canonical cold start at the identical present physical value;
4. distinct asymptotic basin membership;
5. extinction versus coexistence in a positive strong-Allee realization.

The certified nondegenerate interval of such fibers strengthens the result.

## 2. Locked principal claim

The manuscript principal claim is:

> A physically reachable present-state fiber of an autonomous continuous-time Caputo semidynamical system can intersect distinct asymptotic basins. In the certified strong-Allee example, an entire reached physical-time arc of fibers contains both an inherited continuation state converging to coexistence and the canonical cold start at the identical present value converging to extinction.

This is the strongest claim that may be foregrounded without further novelty work.

## 3. Required novelty qualification

Use a targeted qualification, not an absolute priority claim:

> No formally published theorem establishing this same-present-value, physically reachable Caputo basin split was identified in our targeted literature audit.

Do not write “first ever”.

## 4. Closest prior and positioning

The closest conceptual prior is Szaksz–Stepan–Habib (2024) for delay systems:
- full history matters beyond the headpoint;
- different constrained histories may share a headpoint;
- restarting from a visited headpoint need not reproduce the inherited trajectory.

But it does not prove opposite basin membership at that same headpoint.

Deshpande–Daftardar-Gejji–Vellaisamy (2019) already establishes fractional trajectory intersections. Therefore projected-state coincidence itself is not novel.

Doan–Kloeden provides the Caputo memory-state/continuation architecture. That architecture is background.

## 5. Claims explicitly prohibited in manuscript

Do not claim:
- first demonstration that memory gives different futures from the same present;
- first fractional trajectory intersection;
- first failure of trajectory nonintersection;
- first basin geometry in a history system;
- first basin analysis in fractional predator–prey dynamics;
- first extinction/coexistence bistability with Allee effects;
- first history/headpoint dependence of basin membership;
- novelty of the ecological vector field;
- first validated/certified fractional computation;
- novelty of generic radii/Perron/resolvent machinery;
- end-to-end interval rigor for the current TASK-0006 certificate;
- a parameter-open family unless separately proved and audited.

## 6. Contribution hierarchy

### Principal — NEW THEOREM / CERTIFIED REALIZATION
Same-present reachable Caputo fiber split between extinction and coexistence basins.

### Strong secondary
A certified nondegenerate physical-time interval of such multibasin fibers.

### Supporting theory
- scalar purity/completeness contrast;
- E1 basin-entry structural theorem;
- X1 cold-start extinction theorem;
- M1 memory-tail survival theorem.

### Enabling proof technology
Cellwise positive-operator CAP with Perron-weighted contraction and memory-tail certification.

Do not elevate the numerical method to principal novelty in this paper.

## 7. Arithmetic disposition

The current theorem is valid under the declared arithmetic model.

The main referee vulnerability is the load-bearing assumption that selected libm functions are accurate to a few ulp.

Before submission, harden those evaluations with Arb/MPFR or another verified directed enclosure where practical.

This is a proof-presentation robustness task, not a novelty gate.

## 8. Manuscript gate

\[
\boxed{\text{MANUSCRIPT MODE UNLOCKED}.}
\]

The final manuscript must remain theorem-centered and follow
\`agent_directives_publishable_first_submission.md\`.

Target 22–23 pages, hard maximum 25 pages.

Primary computational certificate: \(T=300,N=12000\).

Independent redundancy: \(T=1000,N=20000\).
