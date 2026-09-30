# Claim-to-Evidence Matrix — Manuscript v1

**Date:** 2026-09-30  
**Purpose:** one-to-one map from manuscript claims to load-bearing evidence.  
**Rule:** a claim must not be strengthened in prose unless this matrix is updated and re-audited.

| ID | Manuscript claim | Evidence class | Load-bearing support | Status |
|---|---|---|---|---|
| C-01 | Autonomous Caputo dynamics admits the continuation-state semidynamical representation used in the paper | PUBLISHED PRIOR + localization | Doan--Kloeden 2021/2024; cutoff lemma for polynomial B215 | CLOSED |
| C-02 | Physical convergence to an equilibrium implies compact-open convergence of continuation states | ANALYTIC | Proposition E3 / manuscript Prop. physical-to-continuation | CLOSED |
| C-03 | A physically reached point inside a cold-start basin can generate a multibasin fiber when the inherited state belongs to a disjoint basin | ANALYTIC | Basin-entry proposition E1 with disjoint basin hypothesis | CLOSED |
| C-04 | Scalar reachable fibers are basin-pure under equilibrium-barrier / interval-basin hypotheses | ANALYTIC + PUBLISHED PRIOR | S1; Cong--Tuan / Doan--Kloeden scalar theory | CLOSED / supporting only |
| C-05 | For the strong-Allee system, every canonical cold start with \(0<x<\theta,\ y\ge0\) tends to extinction if \(\theta<m/b\) | ANALYTIC + PUBLISHED PRIOR | X1; viability, scalar comparison, continuation | CLOSED |
| C-06 | The memory-tail inequality \(M_T+K_JC_rr^2<r\) proves convergence of the inherited trajectory to \(E^*\) | ANALYTIC + PUBLISHED PRIOR | M1; matrix Mittag--Leffler / Volterra resolvent theory | CLOSED |
| C-07 | B215 exact algebra is \(E^*=(4/5,3/25)\), stated \(J\), eigenvalues and remainder | EXACT SYMBOLIC | independent Chief algebra audit | CLOSED |
| C-08 | Exact B215 trajectory is validated on \([0,300]\) | CERTIFIED COMPUTATION | TASK-0006 cellwise self-map + Perron contraction | CLOSED under declared arithmetic model |
| C-09 | Exact B215 trajectory satisfies \(0<x<1/2,\ y>0\) for every \(t\in I_*\) | CERTIFIED COMPUTATION | TASK-0006 tube + Arb cell boxes | CLOSED |
| C-10 | Same B215 standard trajectory converges to \(E^*\) | ANALYTIC + CERTIFIED COMPUTATION | M1 + certified \(K_J,C_r,M_T,r\) | CLOSED |
| C-11 | For every \(t_*\in I_*\), \(\mathcal F_{X(t_*;p)}\) intersects extinction and coexistence basins | NEW THEOREM / CERTIFIED REALIZATION | C-02 + C-03 + C-05 + C-09 + C-10 | CLOSED |
| C-12 | The result holds over a nondegenerate time interval | CERTIFIED COMPUTATION | 836 consecutive certified cells at primary cut | CLOSED |
| C-13 | The map \(t\mapsto X(t;p)\) is injective on \(I_*\) | NONE | not certified | **NOT CLAIMED** |
| C-14 | The basin split persists on an open parameter neighborhood | NONE / deferred | E2 abstract only; no quantitative B215 persistence | **NOT CLAIMED** |
| C-15 | The CAP is end-to-end interval arithmetic | NONE at current stage | TASK-0007 pending | **NOT CLAIMED** |
| C-16 | No formally published theorem matching the same-present physically reachable Caputo basin split was found | TARGETED LITERATURE AUDIT | ROUND-0007 | CLOSED as qualified literature statement |
| C-17 | The ecological vector field is new | CONTRADICTED BY PRIOR | Ye et al. 2019 | **PROHIBITED CLAIM** |
| C-18 | Generic memory dependence / fractional trajectory intersection is new | CONTRADICTED BY PRIOR | Doan--Kloeden; Deshpande et al.; delay literature | **PROHIBITED CLAIM** |

## Principal theorem dependency

\[
\boxed{
\mathrm{C\!-\!09}
+\mathrm{C\!-\!05}
+\mathrm{C\!-\!10}
+\mathrm{C\!-\!02}
+\mathrm{C\!-\!03}
\Longrightarrow
\mathrm{C\!-\!11}.
}
\]

The computer-assisted component establishes finite-orbit facts and constants; the basin conclusion itself is an analytic consequence of the state-space theorems.

## Arithmetic update hook

When TASK-0007 returns, update only:
- C-08 evidence wording;
- C-09 evidence wording if arithmetic backend changes;
- C-10 certified-constant provenance;
- C-15 status.

No scientific claim should change unless TASK-0007 exposes a defect.
