# ROUND-0005 — Memory-tail resolvent survival audit

**Agent:** Deep Web Search Agent  
**Search date:** 2026-09-29  
**Request:** `research/coordination/chief-to-web/ROUND-0005_memory-tail-resolvent_REQUEST.md`  
**Priority:** P0 / PRINCIPAL SURVIVAL GATE

## Executive verdict

| Item | Verdict | Reason |
|---|---|---|
| Resolvent / variation-of-constants identity | **VERIFIED** | Standard Volterra resolvent algebra plus the published Caputo matrix variation-of-constants formula yield exactly the proposed (\mathcal L_J h) and (\Psi_J*N) representation. |
| (L^1) matrix Mittag-Leffler kernel | **VERIFIED** | Under the Matignon sector condition (\sigma(J)\subset\{\lambda\ne0:|\arg\lambda|>\alpha\pi/2\}), (\Psi_J(t)=t^{\alpha-1}E_{\alpha,\alpha}(Jt^\alpha)) is locally integrable at zero and decays as (O(t^{-\alpha-1})) at infinity; hence (\Psi_J\in L^1) in every finite-dimensional induced norm. |
| Inherited-memory input and (v_T\to0) | **VERIFIED** | The cut-time split is exact. Although (h_T(t)\to p-E^*\), the linear resolvent cancels that constant because (\int_0^\infty\Psi_J=-J^{-1}\). |
| CANDIDATE-M1 | **VERIFIED** | The first-exit argument and the limsup convolution argument are correct. Add only the already-standard continuation step once the tail is bounded. |
| Direct published memory-tail survival theorem | **NOT FOUND** | General Volterra resolvent, Caputo Lyapunov-Perron and current error-certified Mittag-Leffler machinery are close prior, but no source located gives the exact finite-excursion + inherited-memory-tail + basin certification mechanism used here. |

The round therefore removes the imported-theorem uncertainty from the memory-tail route. TASK-0004 can now treat (K_J,M_T,C_r,r) as the only substantive certification quantities.

---

# Q1 — Resolvent identity

## 1.1 General convolution resolvent

For
[
u=h+k_\alpha*(Ju+N(u)),
\qquad
k_\alpha(t)=\frac{t^{\alpha-1}}{\Gamma(\alpha)},
]
the linear convolution equation
[
v=h+k_\alpha*Jv
]
has resolvent representation
[
v=h+R_J*h,
]
where the linear resolvent kernel satisfies
[
R_J=Jk_\alpha+Jk_\alpha*R_J.
]

For the fractional kernel,
[
\boxed{
R_J(t)=J\Psi_J(t),
\qquad
\Psi_J(t)=t^{\alpha-1}E_{\alpha,\alpha}(Jt^\alpha).
}
]

This is the standard linear Volterra resolvent formula; see Gripenberg, Londen & Staffans, *Volterra Integral and Functional Equations*, Cambridge University Press, 1990, Part I, especially Chapter 2 on linear convolution equations and variation of constants.

The identity follows directly from the Mittag-Leffler series:
[
\Psi_J
=
k_\alpha I
+
k_\alpha*J\Psi_J.
]

Hence the nonlinear equation can be written
[
u
=
\mathcal L_Jh
+
\Psi_J*N(u),
]
with
[
\boxed{
\mathcal L_Jh=h+(J\Psi_J)*h.
}
]

Equivalently,
[
\boxed{
u(t)=\mathcal L_Jh(t)
+
\int_0^t
s^{\alpha-1}E_{\alpha,\alpha}(Js^\alpha)
N(u(t-s))\,ds.
}
]

## 1.2 Published Caputo variation-of-constants support

**Cong, Doan & Tuan (2017)**, “Perron-type theorem for fractional differential systems,” *Electronic Journal of Differential Equations* 2017(142), 1–12, gives in Theorem 2.1 the matrix formula
[
x(t)
=
E_\alpha(At^\alpha)\xi
+
\int_0^t
(t-\tau)^{\alpha-1}
E_{\alpha,\alpha}(A(t-\tau)^\alpha)
f(\tau)\,d\tau
]
for linear inhomogeneous Caputo systems.

**Cong, Doan, Siegmund & Tuan (2016)**, DOI 10.14232/ejqtde.2016.1.39, Theorem 3.4, uses the same matrix/scalar Mittag-Leffler kernel in the Lyapunov-Perron representation of nonlinear Caputo systems.

## 1.3 Assumptions

For the exact project use:

- (0<\alpha<1);
- (J\in\mathbb R^{d\times d}) constant;
- (h\) continuous on the tail half-line;
- (N\) locally Lipschitz on the ball in which the argument is run.

On every finite interval, (k_\alpha\in L^1), so the linear resolvent and nonlinear Volterra equation are locally well posed under these hypotheses.

### Q1 verdict

**VERIFIED.**

---

# Q2 — (L^1) integrability of (\Psi_J)

## 2.1 Exact stability sector

The sharp linear asymptotic-stability condition is
[
\boxed{
\sigma(J)\subset
\left\{
\lambda\in\mathbb C\setminus\{0\}:
|\arg\lambda|>\frac{\alpha\pi}{2}
\right\}.
}
]

This is the Matignon sector.

Hurwitz stability is stronger and implies this condition for every (0<\alpha<1).

## 2.2 Published scalar kernel estimate

**Cong, Doan, Siegmund & Tuan (2016)**, Proposition 2.4(i), proves for
[
\frac{\alpha\pi}{2}<|\arg\lambda|\le\pi
]
that there exist (M(\alpha,\lambda)>0) and (t_0>0) such that
[
\boxed{
|t^{\alpha-1}E_{\alpha,\alpha}(\lambda t^\alpha)|
\le
\frac{M(\alpha,\lambda)}{t^{\alpha+1}}
\qquad (t\ge t_0).
}
]

Thus the stable scalar kernel is absolutely integrable at infinity.

At zero,
[
E_{\alpha,\alpha}(\lambda t^\alpha)
=
\Gamma(\alpha)^{-1}+O(t^\alpha),
]
so
[
t^{\alpha-1}E_{\alpha,\alpha}(\lambda t^\alpha)
=
\Gamma(\alpha)^{-1}t^{\alpha-1}+O(t^{2\alpha-1}),
]
which is integrable because (\alpha>0).

Proposition 2.4(ii) then gives a finite uniform convolution bound.

## 2.3 Matrix case

For a finite-dimensional matrix (J) satisfying the same sector condition, Jordan functional calculus gives
[
E_{\alpha,\alpha}(Jt^\alpha)
=
S\,E_{\alpha,\alpha}(Bt^\alpha)S^{-1},
]
where each Jordan block is assembled from scalar Mittag-Leffler functions and their spectral derivatives.

The stable-sector asymptotic expansion has a vanishing (k=1) term when (\beta=\alpha), because (1/\Gamma(0)=0). Therefore
[
E_{\alpha,\alpha}(Jt^\alpha)
=
O(t^{-2\alpha}),
]
and hence
[
\boxed{
\|\Psi_J(t)\|
=
\|t^{\alpha-1}E_{\alpha,\alpha}(Jt^\alpha)\|
=
O(t^{-\alpha-1}).
}
]

Consequently
[
\boxed{
K_J:=\int_0^\infty\|\Psi_J(s)\|\,ds<\infty.
}
]

This holds in every induced matrix norm because all norms are equivalent in finite dimensions.

A source directly recording the matrix statement is H. T. Tuan's Mittag-Leffler estimate work, but that item is available as a preprint only and is **not needed for final citation support**. The published Cong et al. 2016 argument already uses the stable-kernel estimates to control the full finite-dimensional Lyapunov-Perron operator after Jordan reduction.

## 2.4 Computationally usable bounds

A sharp closed form for (K_J) is generally unavailable.

A rigorous practical strategy is:

1. integrate (\|\Psi_J\|) by validated quadrature on ([0,S]);
2. bound the tail by
   [
   \|\Psi_J(t)\|\le C_J t^{-\alpha-1}
   quad(t\ge S),
   ]
   giving
   [
   \int_S^\infty\|\Psi_J(t)\|dt
   \le
   \frac{C_J}{\alpha S^\alpha}.
   ]

The contour estimate underlying Cong et al. Proposition 2.4 gives explicit scalar (M(\alpha,\lambda)); the matrix constant can be assembled from a Jordan/Schur representation with interval bounds.

Also,
[
\int_0^\infty \Psi_J(s)\,ds=-J^{-1}
]
under the stable-sector condition, hence
[
K_J\ge\|J^{-1}\|
]
for any induced norm. This is a useful lower-bound sanity check for computation.

### Q2 verdict

**VERIFIED.**

---

# Q3 — Inherited-memory input

Let the original standard Caputo trajectory satisfy
[
u(t)=p-E^*
+
\frac1{\Gamma(\alpha)}
\int_0^t(t-s)^{\alpha-1}
[J u(s)+N(u(s))],ds.
]

Fix a cut time (T>0). For (t\ge T),
[
u(t)
=
h_T(t)
+
\frac1{\Gamma(\alpha)}
\int_T^t
(t-s)^{\alpha-1}
[J u(s)+N(u(s))],ds,
]
where
[
\boxed{
h_T(t)
=
p-E^*
+
\frac1{\Gamma(\alpha)}
\int_0^T
(t-s)^{\alpha-1}F(x(s)),ds.
}
]

This is an algebraic split of the original Volterra equation and is exact. It is **not** a Caputo restart.

To place it in standard convolution notation, let
[
\tau=t-T,
\qquad
H_T(\tau):=h_T(T+\tau).
]
Then
[
y(\tau):=u(T+\tau)
]
satisfies a Volterra equation starting at (\tau=0) with forcing (H_T).

## 3.1 Asymptotic behavior of (h_T)

Since the prehistory interval is finite and (F(x(s))) is bounded on ([0,T]),
[
\left\|
\int_0^T
(t-s)^{\alpha-1}F(x(s))ds
\right\|
=
O(t^{\alpha-1}),
]
and (\alpha-1<0). Therefore
[
\boxed{
h_T(t)\to p-E^*.
}
]

Thus the request is correct: one must **not** impose (h_T\to0).

## 3.2 Why the linear response still decays

Define
[
v_T=\mathcal L_Jh_T
=
h_T+(J\Psi_J)*_T h_T.
]

Under the stable-sector condition,
[
E_\alpha(Jt^\alpha)\to0.
]
Using
[
\frac{d}{dt}E_\alpha(Jt^\alpha)
=
Jt^{\alpha-1}E_{\alpha,\alpha}(Jt^\alpha)
=
J\Psi_J(t),
]
integration over ([0,\infty)) gives
[
J\int_0^\infty\Psi_J(s)ds=-I,
]
hence
[
\boxed{
\int_0^\infty\Psi_J(s)ds=-J^{-1}.
}
]

Now use the standard (L^1)-convolution limit theorem: if (k\in L^1(\mathbb R_+)) and (h(t)\to h_\infty), then
[
(k*h)(t)\to
\left(\int_0^\infty k(s)ds\right)h_\infty.
]

Therefore
[
(J\Psi_J*h_T)(t)
\to
J(-J^{-1})(p-E^*)
=
-(p-E^*),
]
and the nonzero constant limit cancels:
[
\boxed{
v_T(t)\to0.
}
]

So for the actual inherited input, the required (v_T\to0) follows automatically once:

- the prehistory is bounded on ([0,T]);
- (J) is Matignon-stable.

No special assumption (p=E^*) is needed.

### Q3 verdict

**VERIFIED.**

---

# Q4 — Audit of CANDIDATE-M1

Assume
[
K_J=\int_0^\infty\|\Psi_J(s)\|_wds<\infty,
]
[
\|N(u)\|_w\le C_r\|u\|_w^2
\quad(\|u\|_w\le r),
]
[
M_T=\sup_{t\ge T}\|v_T(t)\|_w<\infty,
\qquad
v_T(t)\to0,
]
and
[
\boxed{
M_T+K_JC_rr^2<r.
}
]

The variation-of-constants identity is
[
u(t)
=
v_T(t)
+
\int_T^t\Psi_J(t-s)N(u(s))ds.
]

## 4.1 First-exit step

At (t=T), the convolution vanishes, so
[
\|u(T)\|=\|v_T(T)\|\le M_T<r.
]

Suppose (t_e>T) is the first time with (\|u(t_e)\|_w=r). For (T\le s\le t_e),
[
\|N(u(s))\|_w\le C_rr^2.
]
Hence
[
\|u(t_e)\|_w
\le
M_T+
C_rr^2
\int_T^{t_e}\|\Psi_J(t_e-s)\|_wds
\le
M_T+K_JC_rr^2<r,
]
a contradiction.

Therefore the actual tail never exits the ball.

The standard Caputo/Volterra continuation theorem then promotes this bounded tail to global existence.

## 4.2 Limsup convolution step

Inside the invariant ball,
[
\|N(u)\|_w
\le
C_rr\,\|u\|_w.
]

Set
[
L:=\limsup_{t\to\infty}\|u(t)\|_w.
]

For any (\varepsilon>0), choose (S) such that
[
\|u(s)\|_w\le L+\varepsilon
\qquad(s\ge S).
]

Split the nonlinear convolution into:

1. the fixed early interval ([T,S]);
2. the late interval ([S,t]).

For the early term, (N(u(s))) is bounded on a fixed finite interval and
[
\Psi_J(t-s)\to0
]
as (t\to\infty); the stable-kernel decay makes this term tend to zero.

For the late term,
[
\limsup_{t\to\infty}
\left\|
\int_S^t
\Psi_J(t-s)N(u(s))ds
\right\|_w
\le
K_JC_rr(L+\varepsilon).
]

Since (v_T(t)\to0),
[
L\le K_JC_rr(L+\varepsilon).
]
Letting (\varepsilon\downarrow0),
[
L\le K_JC_rrL.
]

The strict invariance condition implies
[
K_JC_rr^2<r
\quad\Longrightarrow\quad
K_JC_rr<1.
]
Therefore
[
\boxed{L=0}.
]

Hence
[
\boxed{u(t)\to0}.
]

## 4.3 Relation to published Lyapunov-Perron arguments

Cong et al. 2016 use precisely the same stable Mittag-Leffler kernel and the same type of limsup splitting in the proof of their linearized asymptotic-stability theorem. Their proof shows an early fixed interval vanishes using the (O(t^{-\alpha-1})) kernel estimate, while the late interval is bounded by the stable (L^1) convolution constant; see the argument following Lemma 3.6 / Theorem 3.1.

The project theorem differs by allowing a nonconstant inherited forcing (h_T), handled separately through (v_T=\mathcal L_Jh_T\to0).

### Q4 verdict

[
\boxed{\text{CANDIDATE-M1 VERIFIED}}
]

The proof draft is correct. For final theorem presentation, explicitly state:

- local existence/continuation of the tail Volterra equation;
- (h_T\) is understood in shifted coordinates when using ordinary convolution notation.

No numerical or theorem-level modification of the smallness inequality is required.

---

# Q5 — Direct prior / novelty audit

## 5.1 Strong adjacent prior

### Cong et al. 2016
Published linearized asymptotic stability for nonlinear Caputo systems via a Mittag-Leffler Lyapunov-Perron operator. It supplies the stable kernel, (L^1) convolution bounds, contraction logic and limsup decay mechanism.

### Cong, Doan & Tuan 2017
Published matrix variation-of-constants and bounded-forcing theory for inhomogeneous linear fractional systems.

### Gripenberg, Londen & Staffans 1990
General Volterra convolution-resolvent theory, including forcing-function resolvents and asymptotic convolution results.

### Salas, Altamirano & Martínez 2026
“An error-certified matrix Mittag-Leffler perturbation method for weakly nonlinear fractional systems,” *Frontiers in Applied Mathematics and Statistics* 12, 1899674, DOI **10.3389/fams.2026.1899674**, published 24 August 2026.

This recent paper is a relevant current novelty threat because it combines:
- exact matrix Mittag-Leffler propagators;
- weakly nonlinear Volterra variation of constants;
- explicit truncation estimates;
- residual-to-solution certification;
- independent fractional-solver validation.

It does **not** perform the project's cut-time inherited-memory basin classification, nor the cold-start-versus-continuation-state comparison.

### Current 2026 memory-control literature
Recent work on permanent hold in Caputo systems explicitly emphasizes that pre-(T) motion leaves an inherited post-(T) memory signal. This is strong prior against claiming “memory survives a cut time” as new, but its objective is controlled compensation/hold, not autonomous basin survival.

## 5.2 Exact mechanism search

No formally published source was located that combines all of:

1. a validated finite nonlinear excursion of an autonomous Caputo trajectory;
2. exact retention of the prehistory in an inherited Volterra forcing after a cut time;
3. a stable matrix Mittag-Leffler resolvent bound on the nonlinear tail;
4. a rigorous conclusion that this particular continuation state belongs to a survival basin;
5. use of that conclusion against a cold-start extinction theorem at an earlier reached present state.

### Q5 verdict

**NO DIRECT PRIOR FOUND IN SEARCHED CORPUS.**

The mathematical ingredients are standard/adjacent; the project-specific assembly remains the residual.

---

# 6. Consequence for TARGET-A20

ROUND-0005 closes the analytic uncertainty in the proposed memory-tail theorem.

For the exact-rational W1 witness, the remaining proof burden is now computational/certificational:

1. choose a cut time (T) after recovery;
2. rigorously enclose the prehistory-generated (h_T);
3. compute/certify
   [
   K_J,
   \quad
   M_T=\sup_{t\ge T}\|\mathcal L_Jh_T(t)\|_w,
   \quad
   C_r;
   ]
4. find (r>0) satisfying
   [
   M_T+K_JC_rr^2<r.
   ]

If TASK-0004 succeeds, then M1 proves
[
x(t)\to E^*.
]
STRUCTURAL-E3 then places the original standard IVP in the continuation-state survival basin. Together with the already proved X1, exact-rational certified threshold entry, and E1, this closes TARGET-A20.

---

# 7. Bibliography actions

Add/record as formally published support:

- Cong, Doan & Tuan 2017 — *Electronic Journal of Differential Equations* 2017(142), “Perron-type theorem for fractional differential systems”.
- Gripenberg, Londen & Staffans 1990 — *Volterra Integral and Functional Equations*, Cambridge University Press.
- Cong, Tuan & Trinh 2020 — DOI **10.1016/j.jmaa.2019.123759**, useful current published asymptotic-behavior support.
- Salas, Altamirano & Martínez 2026 — DOI **10.3389/fams.2026.1899674**, current adjacent error-certified matrix Mittag-Leffler prior.

Cong et al. 2016, DOI **10.14232/ejqtde.2016.1.39**, is already in the project bibliography and is the primary load-bearing kernel/limsup source.

Do not use Tuan's 2017 standalone Mittag-Leffler preprint as final citation support; the published sources above suffice.

---

# 8. Negative-search limitations

- No direct prior found is not proof of absence.
- General Volterra theory may encode equivalent tail criteria without Caputo terminology.
- Current 2026 certified Mittag-Leffler work materially raises the novelty bar for any claim based only on resolvent-based error certification.
- The defensible residual is the **autonomous inherited-memory survival classification tied to a cold-start extinction contradiction at the same reached present state**, not the resolvent technology itself.
