# TASK-0005 — CHIEF DECISION

**Date:** 2026-09-30  
**Branch:** \`compute/task-0005\`  
**Verified HEAD:** \`26d6755b4f843f7f5e5c481b93046497b61bebec\`  
**Integrated in main:** merge commit \`7d4171d9d992ae8fcbc69514911067054bba6b40\`  
**Disposition:** ACCEPT FEASIBILITY / NO CERTIFICATE YET / B215 PROMOTED AS PRIMARY BENCHMARK

## 1. Principal result

The sign-aware gate is passed decisively.

Compared with the absolute-value Theorem-R amplification:

- W1: \(10^{15.8}\to133\);
- B215: \(10^{6.7}\to8.9\);
- B154: \(10^{5.4}\to4.0\).

The goal-oriented amplification into \(M_T\) is smaller still:
- W1: about \(0.22\);
- B215: about \(0.09\).

Therefore the catastrophic amplification of TASK-0004 was primarily a bounding artifact, not the true variational response.

## 2. Benchmark decision

B215 becomes the primary benchmark:

\[
\theta=\frac12,\quad
a=\frac12,\quad
b=1,\quad
m=\frac45,\quad
\alpha=\frac{17}{20},
\]
\[
p=
\left(
\frac{277}{100},
\frac{467}{1000}
\right).
\]

It has:
- low sign-aware amplification;
- favorable goal-functional amplification;
- simple exact rational parameters;
- substantial numerical entry margin;
- strong M1 margin.

W1 remains archival/secondary.

## 3. What is accepted

Accepted as NUMERICAL EXPLORATION / strong feasibility evidence:
- state amplification values;
- goal-oriented amplification;
- B215 ranking;
- approximate \(Y,Z_2,Y_{M_T}\).

Accepted algebraically:
- the idea that off-grid interpolation is the sole remaining CAP term;
- the exact form of the source-space inverse defect after the source/state correction in the ROUND-0006 Chief decision.

## 4. What is not accepted

Not promoted:
- \(Z_1=0.27\) for B215;
- any radii-polynomial certificate;
- any rigorous \(M_T\);
- B215 survival;
- TARGET-A20.

The pilot \(Z_1\) used an empirical oscillation assumption and mixed a state-space \(I-WA\) inverse with a source-space \(I-AW\) identity.

Both issues are fixed in the specification of TASK-0006, not retroactively in TASK-0005.

## 5. Key insight retained

The functional \(M_T\) is vastly less sensitive to history error than a uniform state tube.

The final CAP should therefore certify both:
1. enough state control to identify the true trajectory and preserve the entry event;
2. a direct goal-oriented bound for \(M_T\), rather than deriving \(M_T\) from a worst-case uniform history tube.

## 6. Next gate

TASK-0006 is a rigorous source-space oscillation-Banach CAP for B215.

No manuscript work yet.
