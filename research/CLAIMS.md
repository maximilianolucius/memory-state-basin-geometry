# Claim Registry

**Status:** TARGET-A20 OPEN — M1 FEASIBLE, VALIDATED HISTORY REMAINS.

## Closed theory / certification

- X1: PROVED.
- E1–E4: PROVED.
- O1: PROVED.
- O2: PROVED for its declared certificate class.
- M1: PROVED.
- exact-rational W1 entry: CERTIFIED COMPUTATION.
- THEOREM-R: PROVED A-POSTERIORI REDUCTION.

## TASK-0004

### NUM-M1-W1
status: STRONG NUMERICAL CORROBORATION  
result:
M1 is feasible for W1 from \(T=500\) in adapted norms; at \(T=1000\) observed \(M_T\) is well below the certified-threshold scale.

### CERT-KC-W1
status: CERTIFIED COMPUTATION / SPECIFIC ML-CONTOUR REPRESENTATION STILL TO BE SOURCE-AUDITED  
values:
\[
K_J\le5.803469,
\]
\[
C_r\le1.078088+0.706762r,
\]
and corresponding admissible
\[
M_T<0.038078.
\]

### OBSTRUCTION-H1
status: COMPUTATIONAL OBSTRUCTION, NOT A THEOREM OF IMPOSSIBILITY  
current normwise history verifier incurs at least \(10^5\)-scale amplification on all M1-feasible witnesses scanned and much larger amplification on W1.

## Active method

### CANDIDATE-V1
status: OPEN / ROUND-0006 + TASK-0005  
method:
validate the entire finite excursion using an approximate inverse of the orbit-linearized Volterra operator instead of absolute-value Gronwall amplification.

## TARGET-A20

status: OPEN.

Only missing fact:
rigorous survival classification of one entering continuation orbit.

M1 shows that a sufficiently accurate certified history bound will close it.
