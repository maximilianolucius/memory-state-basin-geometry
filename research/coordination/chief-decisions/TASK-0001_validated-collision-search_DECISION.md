# TASK-0001 — CHIEF DECISION

**From:** Chief Researcher  
**Date:** 2026-09-29  
**Evaluates:** \`research/coordination/compute-to-chief/TASK-0001_validated-collision-search_RETURN.md\`  
**Compute branch:** \`compute/task-0001\`  
**Verified branch HEAD:** \`9e607dd2f83b249b0b47e76a3a9f1380f46fff5b\`  
**Merged to main:** PR #1, merge commit \`26f53ee3eb39de7e6e884232ef65c13723b27b9b\`  
**Disposition:** ACCEPT WITH THEOREM REFACTORING — PRINCIPAL TARGET NOW CONJECTURED, NOT PROVED

## 1. Executive decision

TASK-0001 materially advances the project.

The main positive phenomenon is no longer merely speculative: a robust, reproducible **numerical witness** exists in a positive, nontriangular, project-constructed strong-Allee Caputo predator–prey system.

However, TARGET-A20 is **not yet proved** because:
- the extinction side still depends on comparison/positivity ingredients requiring exact theorem audit;
- the survival side remains numerical;
- the model is project-constructed rather than a faithful reproduction of a published Double-Allee system;
- no validated enclosure of the nonlinear witness trajectory exists.

The correct project status is therefore:

> **TARGET-A20 = CONJECTURED WITH STRONG NUMERICAL/CERTIFIED SUPPORT; theorem closure now has a precise bottleneck.**

## 2. Compute evidence accepted

### Stage A — solver infrastructure
**PASS.**

Accepted as discovery/corroboration infrastructure:
- three full-history solvers;
- two distinct formulations;
- exact Mittag–Leffler validation;
- long-horizon checks;
- deterministic regression suite;
- explicit mesh-failure evidence rather than hidden coarse-grid artifacts.

The L1 anomaly and PECE roundoff-floor anomaly remain correctly caveated and do not invalidate the use made of the solvers.

### Stage B — \(d=2\) noninjectivity construction
**ACCEPTED AS AN INDEPENDENT PROJECT CONSTRUCTION, NOT AS A CONG–TUAN REPRODUCTION.**

The Arb/Krawczyk enclosure of a unique nonreal zero of \(E_{1/2}\) is **CERTIFIED COMPUTATION**.

Given that zero, the conclusion
\[
E_{1/2}(A)=0
\]
for the associated real \(2\times2\) rotation-scaling matrix is exact algebra.

This strengthens internal confidence in the collision machinery but is not a novelty claim.

### Stage C — published Double-Allee baseline
**HALT ACCEPTED.**

The agent correctly refused to guess equations/parameters absent from the local repository.

The substitute model is explicitly **PROJECT-CONSTRUCTED** and can be used for mechanism discovery, theorem development and falsification, but not represented as a reproduction of Mondal et al. or another published parameterization.

### Stage D — positive witness
**ACCEPTED AS STRONG NUMERICAL CORROBORATION.**

For
\[
{}^C D^\alpha x=x(1-x)(x-\theta)-axy,\qquad
{}^C D^\alpha y=y(bx-m),
\]
with
\[
\theta=0.3,\ a=b=1,\ m=0.8,\ \alpha=0.85,
\]
the standard initial state
\[
p=(2.4372,2.012)
\]
has a numerically survival-bound orbit that enters
\[
R_{\rm ext}=\{(x,y):0<x<\theta,\ y\ge0\}
\]
over a long time interval.

The penetration below the Allee threshold is not a coarse-grid or floating-point artifact:
- three history-retaining solvers agree on fine meshes;
- horizon ladders are stable;
- 30-digit recomputation agrees;
- the phenomenon appears in 219 mesh-reliable witnesses over the explored parameter/order families.

The survival basin label remains numerical and therefore no fiber is yet promoted to THEOREM.

## 3. Structural refactoring: embedded-age entry replaces transversality

The most important mathematical consequence is that the principal theorem does **not** require solving
\[
x(t;p)=x(s;q)
\]
with \(s>0\).

Take \(s=0\) and \(q=z=x(t_*;p)\). Then
\[
\iota(z)\in\mathcal R_\alpha
\]
automatically.

Therefore, if:
1. \(\iota(p)\in\mathcal B(A_+)\);
2. \(z=x(t_*;p)\) lies in a physical region \(U_-\) satisfying
   \[
   \iota(U_-)\subseteq\mathcal B(A_-);
   \]
3. \(A_+\neq A_-\);

then
\[
T_{t_*}\iota(p),\ \iota(z)\in\mathcal F_z
\]
belong to distinct basins.

This is the new principal structural reduction.

### Consequence

The old CANDIDATE-M2 requirement of a nonsingular collision Jacobian / IFT is **retired from the principal existence theorem**.

Transversality remains relevant only for stronger geometric statements such as:
- smooth collision manifolds;
- locally unique collision parametrizations;
- differentiable continuation in selected variables.

For basic existence and parameter persistence of a multibasin fiber, the entry condition is open and continuity is enough **provided the two basin-membership statements persist**.

## 4. New bottleneck: basin membership, not collision geometry

TASK-0001 shows empirically that under all 28 tested perturbations the orbit still entered the cold-start extinction strip.

Every failure came from loss of the survival label.

Therefore theorem effort is redirected to:

1. prove the cold-start extinction strip rigorously;
2. prove one standard initial condition belongs to the survival/coexistence basin;
3. then use the open-set entry criterion to obtain the multibasin fiber;
4. establish robust basin membership on an open parameter set.

## 5. Cold-start extinction proposition

For the project-constructed model, the proposed theorem is:

If
\[
0<\theta<\frac{m}{b},
\]
the positive cone is invariant, and the audited scalar comparison principle applies, then every standard physical initial state with
\[
0<x_0<\theta,\qquad y_0\ge0
\]
converges to \((0,0)\).

Proof skeleton:
- compare prey to the scalar Allee solution \(u\):
  \[
  {}^C D^\alpha x
  \le x(1-x)(x-\theta),
  \]
  hence \(0\le x(t)\le u(t)\to0\);
- since \(u(t)<\theta\),
  \[
  {}^C D^\alpha y
  =y(bx-m)
  \le -(m-b\theta)y;
  \]
- compare with
  \[
  y_0E_\alpha(-(m-b\theta)t^\alpha)\to0.
  \]

This proof is mathematically compelling but remains **PENDING SOURCE/HYPOTHESIS AUDIT** for positivity and the exact comparison theorem.

## 6. Caputo mechanism

On
\[
0<x<\theta,\qquad y\ge0,
\]
the prey vector field satisfies
\[
{}^C D^\alpha x<0.
\]

For the witness, \(x(t)\) nevertheless increases back through \(\theta\).

There is no ODE contradiction: for \(0<\alpha<1\), the sign of the Caputo derivative over a later subinterval does not determine local monotonicity because
\[
x(t)=x_0+I^\alpha\phi(t)
\]
retains the contribution of the entire interval from the fixed lower terminal.

This is the likely theorem-level mechanism:
- **cold-start comparison still makes the sub-threshold slice extinctive;**
- **a continuation state carrying prehistory can pass through the same physical slice and recover.**

Novelty of this exact mechanism is not yet claimed. ROUND-0003 is tasked with hostile prior search.

## 7. Same-age collisions

The negative same-age searches are retained only as negative computational evidence.

They are not needed for TARGET-A20 and should not be treated as a project bottleneck.

## 8. Immediate next actions

### Web Search — ROUND-0003
Retrieve the exact published Double-Allee model(s), audit the threshold-recovery mechanism, verify the positivity/comparison hypotheses needed by the extinction theorem, and search for continuation-state basin/trapping results sufficient to close the survival side.

### Compute — TASK-0002
Build validated finite-time enclosure machinery for the nonlinear Caputo system and search for witnesses closer to a rigorously certifiable survival neighborhood.

## 9. Publication gate

**Manuscript remains blocked.**

But the project has crossed an important threshold:

> before TASK-0001 there was no demonstrated positive mechanism; after TASK-0001 there is a reproducible, robust candidate geometry and a precise theorem-closure problem.
