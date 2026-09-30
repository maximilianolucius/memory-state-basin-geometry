# Figure Specifications

**Status:** locked scientific figure plan v1  
**Date:** 2026-09-30  
**Rule:** every figure must support a theorem, a certified inequality, or a precise interpretive claim.

## Figure 1 — continuation-state fiber geometry

**Purpose:** define the geometric object of the paper before the ecological model appears.

Panels:
- (a) continuation-state space \(\mathfrak C\) with present-evaluation fibers \(e_0^{-1}(z)\);
- (b) one reachable fiber \(\mathcal F_z\) containing \(\iota(z)\) and \(T_{t_*}\iota(p)\) in two distinct basins.

Must visually distinguish:
- physical present \(z\);
- inherited continuation state;
- canonical cold start;
- basin labels.

**Evidence type:** schematic of exact definitions, not numerical evidence.

## Figure 2 — B215 phase-plane excursion

**Purpose:** show the physical mechanism certified by Proposition 5.2.

Plot:
- physical trajectory \(X(t;p)=(x(t),y(t))\), preferably \(0\le t\le60\);
- shade the strip \(0<x<1/2,\ y>0\);
- mark \(p=(2.77,0.467)\);
- mark \(E^*=(0.8,0.12)\);
- highlight the certified time interval
  \[
  I_*=[5.8576774143,13.7275388580].
  \]

The highlighted segment must be based on the certified trajectory center and must not visually imply a theorem beyond the tube.

## Figure 3 — certified threshold crossing in time

Two panels:
- (a) prey \(x(t)\) with threshold \(1/2\), validated center and certified tube;
- (b) predator \(y(t)\) with positivity lower enclosure.

Highlight \(I_*\).

Include a zoom around the representative cell
\[
[8.9839195370,8.9927932624]
\]
where
\[
x\in[0.468938793,0.469058899],\qquad y\ge0.248262346.
\]

**Purpose:** make the cold-start extinction classification visually undeniable.

## Figure 4 — same present, different asymptotic futures

Choose one certified time \(t_*\) inside the representative cell and set
\[
z_*=X(t_*;p).
\]

Show two futures from the identical present physical point:
- inherited future: continuation of the original standard trajectory, tending to \(E^*\);
- cold-start future: standard point IVP initialized at \(z_*\), tending to \((0,0)\).

Important:
- numerical curves are visualization only;
- theorem labels must cite X1 + certified survival;
- do not imply that a Caputo restart represents the inherited state.

This figure should carry the central conceptual message of the paper.

## Figure 5 — finite-history CAP tube

Panels:
- state error radius versus time;
- source sup/oscillation/bubble certificate components.

Annotate:
\[
\|X-\widehat X\|_{\rm adapted}\le4.8661\times10^{-4},
\]
\[
\|X-\widehat X\|_2\le2.2193\times10^{-4}.
\]

**Purpose:** show that the threshold claim is made by a validated tube, not by a raw numerical trajectory.

## Figure 6 — why the orbit-linearized proof is necessary

Log-scale comparison of amplification:
- W1: normwise \(10^{15.8}\) versus sign-aware \(133\);
- B215: normwise \(10^{6.7}\) versus sign-aware \(8.9\);
- optionally B154: normwise \(10^{5.4}\) versus sign-aware \(4.0\).

Second panel:
goal-functional amplification toward \(M_T\):
- W1 \(\approx0.22\);
- B215 \(\approx0.09\).

**Evidence type:** numerical diagnostic, not theorem proof.

**Purpose:** explain method choice compactly and prevent a long textual discussion of failed Grönwall bounds.

## Figure 7 — adaptive mesh and defect localization

Panels:
- mesh width \(h_n\) versus \(t_n\);
- source/collocation defect versus time.

Highlight the early fractional singular layer around \(t\approx0.02\).

Primary mesh:
\[
T=300,\quad N=12000.
\]

**Purpose:** explain why defect-equidistribution, rather than late-time refinement alone, closes the nonlinear CAP.

## Figure 8 — memory-tail survival budget

Two panels, \(T=300\) and \(T=1000\).

Show decomposition of \(M_T\):
- linear flow;
- far-history term;
- near-history term.

For \(T=300\):
\[
M_T\le0.043232414,
\]
with terms approximately
\[
0.0401572,\quad0.00127068,\quad0.00180450.
\]

Show the M1 radius budget:
\[
r
>
M_T+K_JC_rr^2
\]
and the certified margin
\[
0.0135626.
\]

For \(T=1000\), show the independent larger margin
\[
0.0413364.
\]

**Purpose:** make explicit that survival is certified using inherited memory, not a late restart.

---

## Figure production rules

- vector PDF/SVG output;
- consistent mathematical typography;
- no screenshots;
- no decorative 3D;
- certified quantities visually separated from numerical corroboration;
- use the same notation as the theorem statements;
- each caption must state the evidence class where relevant.

## Data provenance

Primary certificate:
- \`t6_stageD_adaptT300_N12000_manifest.json\`;
- \`t6_stageE_adaptT300_N12000_manifest.json\`;
- committed certificate/mesh arrays.

Secondary redundancy:
- corresponding \(T=1000,N=20000\) manifests.

Raw large block files remain regenerable on ORION and are not required for plotting the principal manuscript figures.
