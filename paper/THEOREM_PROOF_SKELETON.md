# Theorem / Proof Skeleton

**Status:** manuscript-core skeleton v1  
**Date:** 2026-09-30  
**Purpose:** lock the mathematical order, theorem statements, proof dependencies, and evidence classes before introduction/abstract prose.

---

## Global notation

Let
\[
{}^CD^\alpha x(t)=g(x(t)),\qquad 0<\alpha<1,
\]
be an autonomous Caputo system on a physical state domain \(X_{\rm phys}\subset\mathbb R^d\).

Use the Doan--Kloeden continuation-state space
\[
\mathfrak C=C(\mathbb R_+,\mathbb R^d)
\]
with the compact-open topology.  The canonical cold-start embedding and present evaluation are
\[
\iota(z)(\tau)\equiv z,\qquad e_0(f)=f(0).
\]

Let \(T_t\) denote the continuation-state semidynamical system.  Define the physically reachable set
\[
\mathcal R_\alpha
=
\{T_t\iota(p):p\in X_{\rm phys},\ t\ge0\}
\]
and, for a present physical value \(z\),
\[
\mathcal F_z
=
e_0^{-1}(z)\cap\mathcal R_\alpha.
\]

For a compact invariant set \(A\subset\mathfrak C\), write
\[
\mathcal B(A)
\]
for its basin in the continuation-state semidynamical system.

**Citation anchors:** \cite{DoanKloeden2021Semidynamical,DoanKloeden2024Attractors,CongTuan2017}.

---

# Section 2. Continuation-state basin geometry

## Definition 2.1 — reachable present-state fiber

The set
\[
\mathcal F_z=e_0^{-1}(z)\cap\mathcal R_\alpha
\]
is the physically reachable present-state fiber above \(z\).

A fiber is **multibasin** if it intersects at least two distinct asymptotic basins.

### Editorial note
This definition is the paper's geometric object.  Do not claim the state-space construction itself is new.

---

## Proposition 2.2 — physical convergence lifts to continuation-state convergence (E3)

Let \(x(\cdot;p)\) be a standard point-IVP solution and suppose
\[
x(t;p)\to x^*,
\qquad
g(x^*)=0.
\]
Then
\[
T_t\iota(p)\to\iota(x^*)
\]
in the compact-open topology on \(\mathfrak C\).

### Proof skeleton

For every fixed \(N>0\) and \(0\le\eta\le N\),
\[
(T_t\iota(p))(\eta)
=
p+
\frac1{\Gamma(\alpha)}
\int_0^t(t+\eta-s)^{\alpha-1}g(x(s;p))\,ds.
\]

Using the physical Volterra equation at \(t+\eta\),
\[
x(t+\eta;p)
=
p+
\frac1{\Gamma(\alpha)}
\int_0^{t+\eta}(t+\eta-s)^{\alpha-1}g(x(s;p))\,ds,
\]
hence
\[
(T_t\iota(p))(\eta)-x^*
=
[x(t+\eta;p)-x^*]
-
\frac1{\Gamma(\alpha)}
\int_t^{t+\eta}(t+\eta-s)^{\alpha-1}g(x(s;p))\,ds.
\]

The first term tends uniformly to zero for \(0\le\eta\le N\) because \(x(t)\to x^*\).
For the second,
\[
\sup_{0\le\eta\le N}
\left\|
\frac1{\Gamma(\alpha)}
\int_t^{t+\eta}(t+\eta-s)^{\alpha-1}g(x(s;p))\,ds
\right\|
\le
\frac{N^\alpha}{\Gamma(\alpha+1)}
\sup_{s\ge t}\|g(x(s;p))\|\to0.
\]

Thus
\[
\sup_{0\le\eta\le N}
\|(T_t\iota(p))(\eta)-x^*\|\to0
\]
for every \(N\), which is compact-open convergence. \(\square\)

### Evidence
ANALYTIC.

---

## Proposition 2.3 — basin-entry fiber criterion (E1)

Let \(A_-\ne A_+\) be invariant asymptotic states/attractors.  Suppose
\[
\iota(U_-)\subset\mathcal B(A_-),
\qquad
\iota(p)\in\mathcal B(A_+).
\]
If the standard physical orbit reaches
\[
z=x(t_*;p)\in U_-,
\]
then
\[
T_{t_*}\iota(p),\ \iota(z)\in\mathcal F_z,
\]
with
\[
T_{t_*}\iota(p)\in\mathcal B(A_+),
\qquad
\iota(z)\in\mathcal B(A_-).
\]
Therefore \(\mathcal F_z\) is multibasin.

### Proof skeleton

By the defining property of the continuation state,
\[
e_0(T_{t_*}\iota(p))=x(t_*;p)=z.
\]
Also
\[
e_0(\iota(z))=z.
\]
Both states are physically reachable, so both lie in \(\mathcal F_z\).

Positive invariance of basins gives
\[
T_{t_*}\iota(p)\in\mathcal B(A_+),
\]
while the hypothesis on \(U_-\) gives
\[
\iota(z)\in\mathcal B(A_-).
\]
Since \(A_-\ne A_+\), the fiber intersects two distinct basins. \(\square\)

### Evidence
ANALYTIC.

---

## Corollary 2.4 — nondegenerate time-interval criterion (E1-A)

Under Proposition 2.3, if there is a nondegenerate interval \(I\) such that
\[
x(t;p)\in U_-
\qquad
\forall t\in I,
\]
then for every \(t\in I\),
\[
\mathcal F_{x(t;p)}
\]
is multibasin.

### Precision note
This corollary is indexed by a nondegenerate **time interval**.  We do not claim that
\(t\mapsto x(t;p)\) is injective on \(I\), hence we do not call the image a topological arc of distinct fibers unless injectivity is separately certified.

---

## Proposition 2.5 — finite-time continuation states are not globally close to the terminal equilibrium (E4)

For fixed \(T>0\), if \(x(\cdot;p)\) is bounded on \([0,T]\), then
\[
(T_T\iota(p))(\tau)\to p
\qquad
(\tau\to\infty).
\]
Consequently, if \(p\ne x^*\),
\[
\sup_{\tau\ge0}
\|(T_T\iota(p))(\tau)-x^*\|
\ge\|p-x^*\|.
\]

### Role
One-paragraph remark explaining why the compact-open topology, not the unweighted global sup norm, is structurally correct.

---

# Section 3. Scalar purity contrast

## Theorem 3.1 — scalar equilibrium-partition fiber purity (S1)

For a scalar autonomous Caputo equation, assume:
1. equilibrium values are barriers for non-equilibrium standard trajectories;
2. each connected component between equilibrium values has a single basin label;
3. equilibrium lifts are stationary and cannot be reached in finite positive time by non-equilibrium standard trajectories.

Then every physically reachable present-state fiber is basin-pure.

### Proof
Use the no-crossing barrier to show that the initial point and the reached present value belong to the same equilibrium interval; basin positive invariance then fixes the basin label of every reachable continuation state above that present value.

### Specialization
For
\[
{}^CD^\alpha x=x(1-x)(x-\theta),
\qquad 0<\theta<1,
\]
the standard positive-domain fibers below \(\theta\) are extinction-pure and those above \(\theta\) are survival-pure.

**Citation anchors:** \cite{AreaNieto2023AlleeCaputo,DoanKloeden2022Attractors,CongTuan2017}.

### Manuscript role
Completeness/contrast only.  Keep to roughly one page.

---

# Section 4. Strong-Allee predator--prey model

## Model 4.1

Consider
\[
{}^CD^\alpha x
=
x(1-x)(x-\theta)-axy,
\]
\[
{}^CD^\alpha y
=
y(bx-m),
\]
with
\[
0<\alpha<1,\qquad
a,b,m>0,\qquad
0<\theta<1.
\]

This is the Caputo fractionalization of the ecological vector field studied at integer order by Ye et al.  Do not claim novelty of the vector field.

**Citation anchor:** \cite{YeEtAl2019StrongAlleePredatorPrey}.

---

## Proposition 4.2 — equilibria and coexistence Jacobian

If
\[
\theta<\frac mb<1,
\]
the positive coexistence equilibrium is
\[
E^*=(x^*,y^*),
\qquad
x^*=\frac mb,
\qquad
y^*=\frac{(1-x^*)(x^*-\theta)}a.
\]

The Jacobian at \(E^*\) is
\[
J=
\begin{pmatrix}
x^*(1+\theta-2x^*) & -ax^*\\
by^* & 0
\end{pmatrix}.
\]

For the exact B215 values
\[
\theta=\frac12,\quad
a=\frac12,\quad
b=1,\quad
m=\frac45,
\]
\[
E^*=
\left(\frac45,\frac3{25}\right),
\]
and
\[
J=
\begin{pmatrix}
-\frac2{25} & -\frac25\\[2mm]
\frac3{25} & 0
\end{pmatrix},
\]
with eigenvalues
\[
\lambda_\pm
=
\frac{-1\pm i\sqrt{29}}{25}.
\]

Thus the Matignon sector condition holds for \(\alpha=17/20\).

---

## Theorem 4.3 — cold-start extinction strip (X1)

Assume
\[
\theta<\frac mb.
\]
Define
\[
R_{\rm ext}
=
\{(x,y):0<x<\theta,\ y\ge0\}.
\]

Then every canonical standard initial state \(z\in R_{\rm ext}\) has a global nonnegative solution satisfying
\[
(x(t),y(t))\to(0,0).
\]
Equivalently,
\[
\iota(R_{\rm ext})
\subset
\mathcal B(\iota(0,0)).
\]

### Proof skeleton

1. **Positivity:** quasi-positivity plus Caputo viability/extremum theory.
2. **Prey comparison:** if \(u\) solves
   \[
   {}^CD^\alpha u=u(1-u)(u-\theta),\quad u(0)=x_0,
   \]
   then \(0\le x(t)\le u(t)\), and scalar strong-Allee theory yields \(u(t)\to0\) for \(0<x_0<\theta\).
3. **Predator comparison:** with
   \[
   \delta=m-b\theta>0,
   \]
   \[
   {}^CD^\alpha y\le-\delta y,
   \]
   so
   \[
   y(t)\le y_0E_\alpha(-\delta t^\alpha)\to0.
   \]
4. **Continuation:** the obtained bounds exclude finite-time blow-up.

**Citation anchors:** \cite{GirejkoMozyrskaWyrwas2011Viability,AlRefai2012ExtremePoints,Wu2020Comparison,WuLiu2020Continuation,DoanKloeden2022Attractors}.

### Evidence
ANALYTIC FROM PUBLISHED HYPOTHESES.

---

## Theorem 4.4 — memory-tail survival criterion (M1)

Write
\[
u=x-E^*,
\qquad
{}^CD^\alpha u=Ju+N(u),
\]
and
\[
\Psi_J(t)=t^{\alpha-1}E_{\alpha,\alpha}(Jt^\alpha).
\]

Assume:
\[
K_J:=\int_0^\infty\|\Psi_J(s)\|\,ds<\infty,
\]
and for some \(r>0\),
\[
\|N(u)\|\le C_r\|u\|^2
\qquad
(\|u\|\le r).
\]

For a finite cut \(T\), define the inherited linear-memory response
\[
v_T(t)
=
E_\alpha(Jt^\alpha)u_0
+
\int_0^T\Psi_J(t-s)N(u(s))\,ds,
\qquad t\ge T,
\]
and
\[
M_T=\sup_{t\ge T}\|v_T(t)\|.
\]

If
\[
M_T+K_JC_rr^2<r,
\]
then
\[
\|u(t)\|<r
\qquad(t\ge T)
\]
and
\[
u(t)\to0.
\]

### Proof skeleton

The exact split is
\[
u(t)
=
v_T(t)+
\int_T^t\Psi_J(t-s)N(u(s))\,ds.
\]

A first-exit argument gives tail invariance:
\[
\|u(t_e)\|
\le M_T+K_JC_rr^2<r,
\]
contradicting a first exit.

Within the invariant ball,
\[
\|N(u)\|\le C_rr\|u\|,
\]
and strict invariance implies
\[
K_JC_rr<1.
\]

Since \(v_T(t)\to0\), an \(L^1\)-kernel limsup argument yields
\[
L:=\limsup_{t\to\infty}\|u(t)\|
\le K_JC_rr\,L,
\]
hence \(L=0\).

**Citation anchors:** \cite{CongDoanTuan2017Perron,GripenbergLondenStaffans1990,CongTuanTrinh2020Asymptotic,Becker2011WeaklySingularResolvents}.

### Important interpretation
M1 does not restart the Caputo system at \(T\).  The entire pre-\(T\) history is contained in \(v_T\).

---

# Section 5. Certified B215 theorem

## Proposition 5.1 — exact benchmark algebra

Fix
\[
\alpha=\frac{17}{20},\quad
\theta=\frac12,\quad
a=\frac12,\quad
b=1,\quad
m=\frac45,
\]
and
\[
p=
\left(
\frac{277}{100},
\frac{467}{1000}
\right).
\]

Around
\[
E^*=\left(\frac45,\frac3{25}\right),
\qquad
u=(\xi,\eta),
\]
the nonlinear remainder is exactly
\[
N_1(\xi,\eta)
=
-\frac9{10}\xi^2-\frac12\xi\eta-\xi^3,
\]
\[
N_2(\xi,\eta)=\xi\eta.
\]

---

## Proposition 5.2 — certified finite excursion

Under the arithmetic model declared in the CAP section, the exact B215 solution with initial state \(p\) is uniquely enclosed on
\[
[0,300].
\]

The physical enclosure error is at most
\[
2.2193\times10^{-4}.
\]

Moreover,
\[
0<x(t)<\frac12,\qquad y(t)>0
\]
for every
\[
t\in
I_*=
[5.8576774143,\ 13.7275388580].
\]

A representative certified cell is
\[
t\in[8.9839195370,\ 8.9927932624],
\]
\[
x\in[0.468938793,\ 0.469058899],
\]
\[
y\ge0.248262346.
\]

### Evidence
CERTIFIED COMPUTATION under the stated arithmetic model.

---

## Proposition 5.3 — certified survival of the same standard orbit

For the exact same standard IVP, at cut
\[
T=300
\]
the certified constants satisfy
\[
K_J\le11.3499043,
\]
\[
M_T\le0.043232414,
\]
and, at
\[
r=\frac{2221}{20000},
\]
\[
C_r\le0.3695518+0.1627353r.
\]

Therefore
\[
r-K_JC_rr^2-M_T
\ge
0.0135626>0
\]
and
\[
K_JC_rr\le0.48857<1.
\]

By Theorem 4.4,
\[
X(t;p)\to E^*
\qquad(t\to\infty).
\]

### Redundancy
A second independent cut at \(T=1000\) yields
\[
M_T\le0.0154786,
\]
and M1 margin
\[
\ge0.0413364.
\]

Use \(T=300\) in the main proof; report \(T=1000\) as robustness redundancy.

---

## Theorem 5.4 — principal multibasin reachable-fiber theorem

For the exact B215 Caputo system and initial point \(p\) above, let
\[
z(t)=x(t;p).
\]

For every
\[
t_*\in I_*=
[5.8576774143,\ 13.7275388580],
\]
the reachable present-state fiber
\[
\mathcal F_{z_*}
\]
intersects both
\[
\mathcal B(\iota(0,0))
\]
and
\[
\mathcal B(\iota(E^*)).
\]

More precisely,
\[
\iota(z_*)
\in
\mathcal B(\iota(0,0)),
\]
while
\[
T_{t_*}\iota(p)
\in
\mathcal B(\iota(E^*)),
\]
and
\[
e_0(\iota(z_*))
=
e_0(T_{t_*}\iota(p))
=
z_*.
\]

Hence the present physical value does not determine the asymptotic basin on the physically reachable continuation-state set.

### Proof skeleton

From Proposition 5.2,
\[
z_*\in R_{\rm ext}
\]
for every \(t_*\in I_*\).  Theorem 4.3 gives
\[
\iota(z_*)
\in\mathcal B(\iota(0,0)).
\]

Proposition 5.3 gives physical convergence of the original standard orbit:
\[
X(t;p)\to E^*.
\]
By Proposition 2.2,
\[
T_t\iota(p)\to\iota(E^*)
\]
in the continuation-state topology, hence
\[
\iota(p)\in\mathcal B(\iota(E^*)).
\]
Basin positive invariance gives
\[
T_{t_*}\iota(p)\in\mathcal B(\iota(E^*)).
\]

Finally,
\[
e_0(T_{t_*}\iota(p))=x(t_*;p)=z_*
=e_0(\iota(z_*)).
\]
Proposition 2.3 completes the proof. \(\square\)

### Evidence
NEW THEOREM / CERTIFIED REALIZATION.

### Novelty wording
Use only the ROUND-0007-qualified statement:
no formally published theorem establishing this same-present-value, physically reachable Caputo basin split was identified in the targeted literature audit.

---

# Section 6. CAP theorem needed in the paper

## Proposition 6.1 — cellwise fixed-point validation principle

Let \(\hat x=p+I^\alpha\phi\) and define the source equation
\[
\mathcal H(f)
=
f-
[g(\hat x+I^\alpha f)-g(\hat x)]
+\rho,
\qquad
\rho=\phi-g(\hat x).
\]

Let \(T(f)=f-B\mathcal H(f)\).

On a finite mesh \(C_n\), define a closed cellwise set \(S_b\) by bounds on:
- \(\sup_{C_n}|f|\);
- \(\operatorname{osc}_{C_n}f\);
- \(\sup_{C_n}|(I-\pi)f|\).

If the certified positive bound map satisfies
\[
F(b)<b
\]
componentwise and there exist strictly positive weights \(q\) such that
\[
\operatorname{Lip}_{\|\cdot\|_q}(T|_{S_b})\le\kappa<1,
\]
then \(T\) has a unique fixed point in \(S_b\).  If \(B\) is injective, that fixed point solves
\[
\mathcal H(f)=0,
\]
and therefore
\[
x=\hat x+I^\alpha f
\]
is the exact Caputo solution on the validation interval.

### Proof
Closedness + equivalence of the positive finite-mesh weighted norm with the sup topology give completeness; \(F(b)<b\) gives self-mapping; Banach gives the fixed point; injectivity of \(B\) converts \(B\mathcal H(f)=0\) to \(\mathcal H(f)=0\).

### Primary certificate values
For \(T=300,N=12000\):
\[
\kappa\le0.083612,
\]
relative componentwise self-map slack
\[
\ge6.036\times10^{-4}.
\]

### Important wording
The scalar one-radius Church--Queirolo radii polynomial does **not** close for this benchmark.  The proof uses the stronger cellwise vector inequality plus Perron-weighted contraction.

**Methodological citation anchors:** \cite{ChurchQueirolo2024HopfCAP,BredenLessard2018PolynomialCAP,BrunnerPedasVainikko1999WeaklySingularCollocation,LiangBrunner2019WeaklySingularCollocation,Becker2011WeaklySingularResolvents}.

---

# Dependency graph

\[
\boxed{
\text{CAP finite history}
\Longrightarrow
\text{certified entry}
}
\]

\[
\boxed{
\text{CAP history}
+
\text{M1 constants}
\Longrightarrow
X(t;p)\to E^*
}
\]

\[
\boxed{
X(t;p)\to E^*
\overset{E3}{\Longrightarrow}
\iota(p)\in\mathcal B(\iota(E^*))
}
\]

\[
\boxed{
z_*\in R_{\rm ext}
\overset{X1}{\Longrightarrow}
\iota(z_*)\in\mathcal B(\iota(0,0))
}
\]

\[
\boxed{
E1
\Longrightarrow
\mathcal F_{z_*}\text{ multibasin}
}
\]

for every \(t_*\in I_*\).

---

# Statements deliberately excluded from the theorem skeleton

Do not promote:
- injectivity of \(t\mapsto z(t)\) on \(I_*\);
- a topological arc of **distinct** fibers;
- parameter-open persistence;
- novelty of generic memory dependence;
- novelty of trajectory intersection;
- novelty of the ecological vector field;
- novelty of generic validated numerics;
- end-to-end interval arithmetic unless TASK-0007 changes the evidence class.
