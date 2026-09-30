# Core Mathematics Draft

**Status:** manuscript prose draft v1 — Sections 2--5 only  
**Date:** 2026-09-30  
**Note:** introduction, abstract, title, figures and related-work prose remain intentionally deferred.

---

# 2. Continuation states and present-state fibers

A point value \(x(t)\in\mathbb R^d\) is not, by itself, a Markov state for a Caputo equation.  We therefore formulate basin membership on the continuation-state space used for autonomous Caputo semidynamical systems.  Let
\[
{}^CD^\alpha x(t)=g(x(t)),\qquad 0<\alpha<1,
\]
and let
\[
\mathfrak C=C(\mathbb R_+,\mathbb R^d)
\]
carry the compact-open topology.  Following the continuation-state construction of Doan and Kloeden \cite{DoanKloeden2021Semidynamical,DoanKloeden2024Attractors}, the canonical state associated with a point initial value \(z\) is the constant function
\[
\iota(z)(\tau)\equiv z,
\]
while
\[
e_0(f)=f(0)
\]
extracts the current physical value from a continuation state \(f\in\mathfrak C\).

Let \(T_t\) denote the resulting semidynamical system and define the physically reachable subset
\[
\mathcal R_\alpha
=
\{T_t\iota(p):p\in X_{\rm phys},\ t\ge0\}.
\]
For \(z\in X_{\rm phys}\), we call
\[
\mathcal F_z
=
e_0^{-1}(z)\cap\mathcal R_\alpha
\]
the reachable present-state fiber above \(z\).  The central question of this paper is whether \(\mathcal F_z\) can intersect more than one asymptotic basin.

The next observation provides the bridge between ordinary point-IVP convergence and basin membership in the continuation-state space.

### Proposition 2.1. Physical convergence implies continuation-state convergence

Suppose the standard point-IVP solution \(x(\cdot;p)\) satisfies
\[
x(t;p)\to x^*,
\qquad
g(x^*)=0.
\]
Then
\[
T_t\iota(p)\to\iota(x^*)
\]
in the compact-open topology of \(\mathfrak C\).

#### Proof

For fixed \(N>0\) and \(0\le\eta\le N\), the continuation state generated at time \(t\) is
\[
(T_t\iota(p))(\eta)
=
p+
\frac1{\Gamma(\alpha)}
\int_0^t(t+\eta-s)^{\alpha-1}g(x(s;p))\,ds.
\]
The physical solution at \(t+\eta\) satisfies
\[
x(t+\eta;p)
=
p+
\frac1{\Gamma(\alpha)}
\int_0^{t+\eta}(t+\eta-s)^{\alpha-1}g(x(s;p))\,ds.
\]
Subtracting gives
\[
(T_t\iota(p))(\eta)-x^*
=
x(t+\eta;p)-x^*
-
\frac1{\Gamma(\alpha)}
\int_t^{t+\eta}(t+\eta-s)^{\alpha-1}g(x(s;p))\,ds.
\]
The first term tends uniformly to zero for \(0\le\eta\le N\).  Since \(g(x(t;p))\to g(x^*)=0\), the second term is bounded by
\[
\frac{N^\alpha}{\Gamma(\alpha+1)}
\sup_{s\ge t}\|g(x(s;p))\|,
\]
which also tends to zero.  Therefore
\[
\sup_{0\le\eta\le N}
\|(T_t\iota(p))(\eta)-x^*\|\to0
\]
for every \(N\), which is precisely compact-open convergence. \(\square\)

The basin-splitting mechanism can now be stated abstractly.

### Proposition 2.2. Basin-entry criterion

Let \(A_-\neq A_+\) be invariant asymptotic states in \(\mathfrak C\).  Assume that a physical set \(U_-\subset X_{\rm phys}\) satisfies
\[
\iota(U_-)\subset\mathcal B(A_-),
\]
and that
\[
\iota(p)\in\mathcal B(A_+).
\]
If the standard orbit reaches
\[
z=x(t_*;p)\in U_-,
\]
then the reachable fiber \(\mathcal F_z\) intersects both basins:
\[
T_{t_*}\iota(p)\in\mathcal F_z\cap\mathcal B(A_+),
\]
and
\[
\iota(z)\in\mathcal F_z\cap\mathcal B(A_-).
\]

#### Proof

The two states have the same present value,
\[
e_0(T_{t_*}\iota(p))=x(t_*;p)=z=e_0(\iota(z)),
\]
and both are physically reachable.  Basin positive invariance gives
\[
T_{t_*}\iota(p)\in\mathcal B(A_+),
\]
whereas the defining property of \(U_-\) gives
\[
\iota(z)\in\mathcal B(A_-).
\]
Thus \(\mathcal F_z\) is multibasin. \(\square\)

A direct corollary is useful later: if the same standard orbit remains inside \(U_-\) throughout a nondegenerate time interval \(I\), then \(\mathcal F_{x(t;p)}\) is multibasin for every \(t\in I\).  We stress that this conclusion is indexed by time; no injectivity of the map \(t\mapsto x(t;p)\) is required.

---

# 3. Scalar purity as a contrast

The multibasin-fiber mechanism is not automatic in fractional dynamics.  In a broad scalar threshold class, the current scalar value still determines the basin label on the physically reachable state set.

Consider
\[
{}^CD^\alpha x=g(x)
\]
with ordered equilibrium values separating the physical domain into intervals.  Suppose non-equilibrium standard trajectories cannot cross or reach an equilibrium at positive time, and suppose every such interval carries a single asymptotic basin label.  If
\[
\phi=T_t\iota(x_0)\in\mathcal F_x,
\]
then \(x_0\) and \(x\) lie in the same equilibrium interval.  Since the basin of the standard initial state is fixed on that interval and basins are positively invariant under \(T_t\), every reachable state in \(\mathcal F_x\) has the same basin label.  At an equilibrium value \(c\), finite-time nonattainment implies
\[
\mathcal F_c=\{\iota(c)\}.
\]

For the scalar strong-Allee equation
\[
{}^CD^\alpha x=x(1-x)(x-\theta),
\qquad
0<\theta<1,
\]
the global scalar classification available from published Caputo attractor theory \cite{AreaNieto2023AlleeCaputo,DoanKloeden2022Attractors} therefore gives
\[
0<x<\theta
\quad\Longrightarrow\quad
\mathcal F_x\subset\mathcal B(\iota(0)),
\]
while
\[
x>\theta
\quad\Longrightarrow\quad
\mathcal F_x\subset\mathcal B(\iota(1)).
\]
Thus the target phenomenon requires genuinely coupled multidimensional dynamics rather than the mere presence of fractional memory.

---

# 4. A strong-Allee predator--prey system

Writing the physical vector state as
\[
X(t)=(x(t),y(t)),
\]
we consider
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
The underlying ecological vector field is not new; its integer-order version appears in Ye et al. \cite{YeEtAl2019StrongAlleePredatorPrey}.  Here it is used as a concrete positive system in which the continuation-state basin geometry can be resolved rigorously.

If
\[
\theta<\frac mb<1,
\]
then the positive coexistence equilibrium is
\[
E^*=(x^*,y^*),
\qquad
x^*=\frac mb,
\qquad
y^*=\frac{(1-x^*)(x^*-\theta)}a.
\]
Its Jacobian is
\[
J=
\begin{pmatrix}
x^*(1+\theta-2x^*) & -ax^*\\
by^* & 0
\end{pmatrix}.
\]

We first identify a physical region whose canonical cold starts are necessarily extinction-bound.

### Theorem 4.1. Cold-start extinction strip

Assume
\[
\theta<\frac mb
\]
and set
\[
R_{\rm ext}
=
\{(x,y):0<x<\theta,\ y\ge0\}.
\]
Then every standard point initial condition in \(R_{\rm ext}\) generates a global nonnegative solution satisfying
\[
(x(t),y(t))\to(0,0).
\]
Equivalently,
\[
\iota(R_{\rm ext})
\subset
\mathcal B(\iota(0,0)).
\]

#### Proof

The vector field is locally Lipschitz and quasi-positive on the coordinate axes.  Caputo viability and extremum results \cite{GirejkoMozyrskaWyrwas2011Viability,AlRefai2012ExtremePoints} therefore preserve the nonnegative cone.

Let \(u\) solve the scalar strong-Allee problem
\[
{}^CD^\alpha u=u(1-u)(u-\theta),
\qquad
u(0)=x_0.
\]
Because \(y(t)\ge0\),
\[
{}^CD^\alpha x
\le
x(1-x)(x-\theta).
\]
The scalar comparison principle \cite{Wu2020Comparison} gives
\[
0\le x(t)\le u(t).
\]
For \(0<x_0<\theta\), the scalar strong-Allee solution remains below \(\theta\) and converges to zero.  Hence
\[
x(t)\to0
\]
and, for every \(t\),
\[
x(t)<\theta.
\]

Let
\[
\delta=m-b\theta>0.
\]
Then
\[
{}^CD^\alpha y
=
y(bx-m)
\le
-\delta y.
\]
Comparison with the exact Mittag--Leffler solution of
\[
{}^CD^\alpha v=-\delta v,\qquad v(0)=y_0,
\]
gives
\[
0\le y(t)\le y_0E_\alpha(-\delta t^\alpha)\to0.
\]
The resulting uniform bounds exclude finite-time blow-up by the continuation theorem of Wu and Liu \cite{WuLiu2020Continuation}.  Therefore the solution is global and tends to \((0,0)\). \(\square\)

The survival side cannot be proved by restarting the fractional system once the physical trajectory returns near coexistence, because such a restart discards the inherited memory.  We instead retain the prehistory explicitly.

### Theorem 4.2. Memory-tail survival criterion

Let
\[
u=x-E^*
\]
and write
\[
{}^CD^\alpha u=Ju+N(u).
\]
Assume the Matignon sector condition for \(J\) and define
\[
\Psi_J(t)=t^{\alpha-1}E_{\alpha,\alpha}(Jt^\alpha),
\qquad
K_J=\int_0^\infty\|\Psi_J(s)\|\,ds.
\]
Stable Mittag--Leffler estimates imply \(K_J<\infty\) \cite{CongDoanTuan2017Perron,CongTuanTrinh2020Asymptotic}.  Suppose also that
\[
\|N(u)\|\le C_r\|u\|^2
\qquad
(\|u\|\le r).
\]

For a finite cut \(T\), define
\[
v_T(t)
=
E_\alpha(Jt^\alpha)u_0+
\int_0^T\Psi_J(t-s)N(u(s))\,ds,
\qquad
t\ge T,
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
u(t)\to0.
\]

#### Proof

The exact variation-of-constants split is
\[
u(t)=v_T(t)+\int_T^t\Psi_J(t-s)N(u(s))\,ds.
\]
This is a decomposition of the original trajectory, not a restart at \(T\): the entire pre-\(T\) history is retained in \(v_T\).

If \(t_e\) were a first exit from the radius-\(r\) ball after \(T\), then
\[
\|u(t_e)\|
\le
M_T+
\int_T^{t_e}
\|\Psi_J(t_e-s)\|C_rr^2\,ds
\le
M_T+K_JC_rr^2<r,
\]
a contradiction.  Thus the trajectory remains in the ball.

Inside that ball,
\[
\|N(u)\|\le C_rr\|u\|,
\]
and the strict invariance inequality implies
\[
K_JC_rr<1.
\]
Moreover \(v_T(t)\to0\): the homogeneous term decays by Mittag--Leffler stability and the finite-history convolution tends to zero because the kernel decays for every fixed history point.  Let
\[
L=\limsup_{t\to\infty}\|u(t)\|.
\]
Splitting the remaining convolution at a large fixed time and using \(K_J<\infty\) gives
\[
L\le K_JC_rr\,L.
\]
Since \(K_JC_rr<1\), one obtains \(L=0\). \(\square\)

---

# 5. Certified same-present basin splitting

We now fix the exact rational benchmark
\[
\alpha=\frac{17}{20},\qquad
\theta=\frac12,\qquad
a=\frac12,\qquad
b=1,\qquad
m=\frac45,
\]
with initial point
\[
p=
\left(
\frac{277}{100},
\frac{467}{1000}
\right).
\]
The coexistence equilibrium is
\[
E^*=
\left(
\frac45,\frac3{25}
\right).
\]
At this equilibrium,
\[
J=
\begin{pmatrix}
-\frac2{25} & -\frac25\\
\frac3{25} & 0
\end{pmatrix},
\]
whose eigenvalues are
\[
\lambda_\pm
=
\frac{-1\pm i\sqrt{29}}{25}.
\]
Thus the Matignon sector condition holds for \(\alpha=17/20\).

With \(u=(\xi,\eta)=x-E^*\), the nonlinear remainder is
\[
N_1(\xi,\eta)
=
-\frac9{10}\xi^2-\frac12\xi\eta-\xi^3,
\qquad
N_2(\xi,\eta)=\xi\eta.
\]

The finite part of the orbit is validated by the computer-assisted construction described in Section 6.  Under the arithmetic model stated there, the exact trajectory is enclosed on \([0,300]\) with physical state error at most
\[
2.2193\times10^{-4}.
\]
The enclosure proves
\[
0<x(t)<\frac12,\qquad y(t)>0
\]
for every
\[
t\in
I_*=
[5.8576774143,\ 13.7275388580].
\]
In particular, the entire certified time interval lies inside the cold-start extinction strip of Theorem 4.1.

The same validated history supplies the memory-tail quantities of Theorem 4.2.  At
\[
T=300
\]
we obtain
\[
K_J\le11.3499043,
\qquad
M_T\le0.043232414,
\]
and
\[
C_r\le0.3695518+0.1627353r.
\]
For
\[
r=\frac{2221}{20000},
\]
the certified inequality is
\[
r-K_JC_rr^2-M_T
\ge0.0135626>0,
\]
with
\[
K_JC_rr\le0.48857<1.
\]
Hence Theorem 4.2 yields
\[
X(t;p)\to E^*.
\]

We can now state the main result.

### Theorem 5.1. Multibasin reachable present-state fibers

For the exact Caputo system and initial point above, write
\[
z_*=X(t_*;p).
\]
For every
\[
t_*\in I_*=
[5.8576774143,\ 13.7275388580],
\]
the physically reachable fiber \(\mathcal F_{z_*}\) intersects both the extinction basin and the coexistence basin:
\[
\mathcal F_{z_*}
\cap
\mathcal B(\iota(0,0))
\neq\varnothing,
\]
and
\[
\mathcal F_{z_*}
\cap
\mathcal B(\iota(E^*))
\neq\varnothing.
\]

More explicitly,
\[
\iota(z_*)
\in
\mathcal B(\iota(0,0)),
\]
whereas
\[
T_{t_*}\iota(p)
\in
\mathcal B(\iota(E^*)),
\]
although
\[
e_0(\iota(z_*))
=
e_0(T_{t_*}\iota(p))
=
z_*.
\]

#### Proof

The certified finite-orbit enclosure gives
\[
z_*\in R_{\rm ext}
\]
for every \(t_*\in I_*\).  Theorem 4.1 therefore implies
\[
\iota(z_*)
\in
\mathcal B(\iota(0,0)).
\]

The certified memory-tail inequality proves
\[
X(t;p)\to E^*.
\]
By Proposition 2.1,
\[
T_t\iota(p)\to\iota(E^*)
\]
in the continuation-state topology.  Therefore
\[
\iota(p)\in\mathcal B(\iota(E^*)),
\]
and basin positive invariance yields
\[
T_{t_*}\iota(p)
\in
\mathcal B(\iota(E^*)).
\]

Finally,
\[
e_0(T_{t_*}\iota(p))
=
x(t_*;p)
=
z_*
=
e_0(\iota(z_*)).
\]
Thus both states lie in the same reachable present-state fiber and in distinct asymptotic basins. \(\square\)

The theorem does not assert generic history dependence, trajectory-intersection novelty, or a parameter-open family.  Its content is narrower: in this autonomous Caputo system, the same reached physical value supports two physically reachable continuation states whose inherited memories place them in opposite extinction/coexistence basins.
