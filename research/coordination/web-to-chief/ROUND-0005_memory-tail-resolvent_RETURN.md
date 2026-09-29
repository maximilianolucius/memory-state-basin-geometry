# ROUND-0005 — RETURN TO CHIEF

**Round ID:** ROUND-0005  
**Request:** `research/coordination/chief-to-web/ROUND-0005_memory-tail-resolvent_REQUEST.md`  
**Search date:** 2026-09-29  
**Agent:** Deep Web Search Agent  
**Final substantive evidence commit before this return:** `285dbed41c36482c36640d77cd02c7de57704b7e`

## Required verdicts

- **Resolvent identity:** **VERIFIED**
- **(L^1) matrix Mittag-Leffler kernel:** **VERIFIED**
- **Inherited-memory input / (v_T\to0):** **VERIFIED**
- **CANDIDATE-M1:** **VERIFIED**
- **Direct published equivalent theorem:** **NOT FOUND IN SEARCHED CORPUS**

## 1. Exact resolvent identity

For
[
u=h+I^alpha(Ju+N(u)),
qquad
k_alpha(t)=rac{t^{alpha-1}}{Gamma(alpha)},
]
write
[
u=h+k_alpha*(Ju+N(u)).
]

The standard convolution-resolvent equation gives
[
v=h+R_J*h,
]
for the linear problem (v=h+k_alpha*Jv), with
[
R_J(t)=JPsi_J(t),
qquad
Psi_J(t)=t^{alpha-1}E_{alpha,alpha}(Jt^alpha).
]

Hence
[
oxed{
mathcal L_Jh
=
h+(JPsi_J)*h
}
]
and
[
oxed{
u
=
mathcal L_Jh
+
Psi_J*N(u).
}
]

Equivalently,
[
u(t)=
mathcal L_Jh(t)
+
int_0^t
s^{alpha-1}E_{alpha,alpha}(Js^alpha)
N(u(t-s)),ds.
]

Published support:

- Gripenberg–Londen–Staffans, *Volterra Integral and Functional Equations*, Cambridge UP (1990), linear convolution/resolvent theory;
- Cong–Doan–Tuan (2017), *EJDE* 2017(142), Theorem 2.1, matrix Caputo variation-of-constants formula;
- Cong–Doan–Siegmund–Tuan (2016), DOI `10.14232/ejqtde.2016.1.39`, Theorem 3.4, Lyapunov–Perron representation with the same Mittag-Leffler kernel.

### Assumptions sufficient for the project

- (0<alpha<1);
- (J) constant finite-dimensional matrix;
- (h) continuous;
- (N) locally Lipschitz on the radius-(r) ball.

### Verdict

**VERIFIED.**

## 2. (L^1)-integrability of the matrix kernel

The exact stability condition is the Matignon sector:
[
oxed{
sigma(J)subset
left{
lambda
e0:
|arglambda|>rac{alphapi}{2}
ight}.
}
]

Hurwitz stability is stronger and automatically implies this condition for every (0<alpha<1).

Cong et al. 2016, **Proposition 2.4(i)** proves, for every stable scalar mode,
[
|t^{alpha-1}E_{alpha,alpha}(lambda t^alpha)|
le
rac{M(alpha,lambda)}{t^{alpha+1}}
]
for sufficiently large (t).

Near (t=0),
[
Psi_J(t)
=
rac{t^{alpha-1}}{Gamma(alpha)}I
+
O(t^{2alpha-1}),
]
which is integrable.

For the matrix function, stable-sector Jordan/matrix functional calculus gives
[
E_{alpha,alpha}(Jt^alpha)=O(t^{-2alpha}),
]
so
[
oxed{
|Psi_J(t)|=O(t^{-alpha-1}).
}
]

Therefore
[
oxed{
K_J:=int_0^infty|Psi_J(s)|,ds<infty.
}
]

This holds for every induced finite-dimensional matrix norm.

### Useful computational identities

A rigorous (K_J) upper bound can be obtained from:
- validated quadrature on ([0,S]);
- a certified tail estimate
  [
  |Psi_J(t)|le C_Jt^{-alpha-1},
  ]
  giving
  [
  int_S^infty|Psi_J(t)|dt
  le
  rac{C_J}{alpha S^alpha}.
  ]

Also,
[
oxed{
int_0^inftyPsi_J(s),ds=-J^{-1},
}
]
so
[
K_Jge|J^{-1}|.
]

This is an important lower-bound sanity check for TASK-0004.

### Verdict

**VERIFIED.**

## 3. Exact inherited-memory input

For the actual standard trajectory,
[
u(t)=x(t)-E^*,
]
the original Volterra equation splits exactly at (T):
[
u(t)
=
h_T(t)
+
rac1{Gamma(alpha)}
int_T^t
(t-s)^{alpha-1}
[Ju(s)+N(u(s))],ds,
]
where
[
oxed{
h_T(t)
=
p-E^*
+
rac1{Gamma(alpha)}
int_0^T
(t-s)^{alpha-1}F(x(s)),ds.
}
]

This is an exact algebraic split. It is **not** a Caputo restart.

For ordinary convolution notation, define
[
	au=t-T,
qquad
H_T(	au)=h_T(T+	au).
]

Then the tail equation starts at (	au=0) with the inherited forcing (H_T).

### Crucial asymptotic fact

If the prehistory is bounded on ([0,T]),
[
h_T(t)	o p-E^*.
]

Thus the Chief's warning is correct:

> **do not require (h_T(t)	o0).**

The linear response nevertheless decays.

Since
[
rac{d}{dt}E_alpha(Jt^alpha)
=
JPsi_J(t),
]
the stable-sector limit
[
E_alpha(Jt^alpha)	o0
]
gives
[
Jint_0^inftyPsi_J(s),ds=-I.
]

Hence
[
int_0^inftyPsi_J(s),ds=-J^{-1}.
]

For an (L^1) kernel and a bounded (h_T) with limit (h_infty=p-E^*),
[
(Psi_J*h_T)(t)
	o
left(int_0^inftyPsi_Jight)h_infty.
]

Therefore
[
(JPsi_J*h_T)(t)	o-(p-E^*),
]
which cancels the constant tail of (h_T):
[
oxed{
v_T(t)=mathcal L_Jh_T(t)	o0.
}
]

### Verdict

**VERIFIED.**

For the actual W1 history, (v_T	o0) follows from bounded finite prehistory plus Matignon stability of (J).

## 4. Exact audit of CANDIDATE-M1

Assume
[
K_J<infty,
]
[
|N(u)|_wle C_r|u|_w^2
quad(|u|_wle r),
]
[
M_T:=sup_{tge T}|v_T(t)|_w<infty,
qquad
v_T(t)	o0,
]
and
[
oxed{
M_T+K_JC_rr^2<r.
}
]

The variation-of-constants formula is
[
u(t)
=
v_T(t)+
int_T^t
Psi_J(t-s)N(u(s)),ds.
]

### First-exit step

At (t=T),
[
u(T)=v_T(T),
]
so
[
|u(T)|le M_T<r.
]

If (t_e) were the first exit,
[
|u(t_e)|_w=r.
]

Before (t_e),
[
|N(u)|_wle C_rr^2.
]

Therefore
[
|u(t_e)|_w
le
M_T+
K_JC_rr^2
<r,
]
contradiction.

Thus the tail remains inside the nonlinear radius globally. Standard Caputo/Volterra continuation then prevents finite-time termination.

### Limsup step

Inside the ball,
[
|N(u)|_w
le
C_rr|u|_w.
]

Let
[
L=limsup_{t	oinfty}|u(t)|_w.
]

Split the convolution at a fixed large (S):
- the early part ([T,S]) tends to zero because (Psi_J(t-s)	o0);
- the late part is bounded by
  [
  K_JC_rr(L+arepsilon).
  ]

Since (v_T(t)	o0),
[
Lle K_JC_rr(L+arepsilon).
]

Letting (arepsilondownarrow0),
[
Lle K_JC_rrL.
]

The strict invariance inequality already gives
[
K_JC_rr^2<r
quadRightarrowquad
K_JC_rr<1.
]

Hence
[
oxed{L=0}.
]

Therefore
[
oxed{u(t)	o0}.
]

This is the same stable-kernel/early-late limsup mechanism used in the published Lyapunov–Perron proof of Cong et al. 2016.

### Verdict

[
oxed{	ext{CANDIDATE-M1 VERIFIED}}
]

Recommended minor exposition fix only:
- state explicitly that tail convolution is written after the time shift (tmapsto t-T);
- cite the standard continuation theorem once boundedness is obtained.

No change to the smallness inequality is required.

## 5. Direct prior / novelty

The closest published ingredients are:

- Cong et al. 2016: stable Mittag-Leffler Lyapunov–Perron nonlinear asymptotic stability;
- Cong–Doan–Tuan 2017: matrix inhomogeneous Caputo variation of constants;
- Gripenberg–Londen–Staffans 1990: general Volterra forcing/resolvent theory;
- Cong–Tuan–Trinh 2020: Caputo asymptotic behavior and Mittag-Leffler stability;
- **Salas–Altamirano–Martínez 2026**, DOI `10.3389/fams.2026.1899674`: exact matrix Mittag-Leffler propagation plus explicit residual-to-solution error certification for weakly nonlinear Caputo systems.

The 2026 Salas et al. paper is important current novelty pressure: the project must not claim generic novelty for “error-certified matrix Mittag-Leffler propagation” or for using resolvent kernels around a stable fractional linearization.

Recent 2026 memory-control work also explicitly studies nonzero inherited post-(T) memory signals. Thus “memory survives a cut time” is not a novelty claim.

However, no published source was found that combines:

1. a finite validated autonomous nonlinear excursion;
2. a cut preserving the exact inherited Caputo memory;
3. a resolvent-based nonlinear tail certificate proving survival of that continuation state;
4. an earlier physical state whose canonical cold start is rigorously extinction-bound;
5. the resulting same-present-state / different-basin conclusion.

### Verdict

**NO DIRECT PRIOR FOUND IN SEARCHED CORPUS.**

This is search-qualified, not proof of absence.

## 6. Consequence for TARGET-A20

The imported mathematics of the memory-tail route is now closed.

For the exact-rational W1 witness, TASK-0004 only has to certify a late cut (T) and numbers
[
M_T,quad K_J,quad C_r,quad r
]
with
[
oxed{
M_T+K_JC_rr^2<r.
}
]

If successful:

1. M1 proves
   [
   x(t)	o E^*;
   ]
2. E3 gives
   [
   T_tiota(p)	oiota(E^*);
   ]
3. W1 already has certified entry into (R_{m ext});
4. X1 puts the canonical cold start at the reached state in the extinction basin;
5. E1 yields the physically reachable multibasin fiber.

Thus **TASK-0004 is now the only principal gate**.

## 7. Bibliography/reference changes

Added/recorded:

- Cong–Doan–Tuan 2017, *Electronic Journal of Differential Equations* 2017(142), 1–12;
- Gripenberg–Londen–Staffans 1990, *Volterra Integral and Functional Equations*, Cambridge UP;
- Cong–Tuan–Trinh 2020, DOI `10.1016/j.jmaa.2019.123759`;
- Salas–Altamirano–Martínez 2026, DOI `10.3389/fams.2026.1899674`.

Cong–Doan–Siegmund–Tuan 2016 was already present and is the main load-bearing kernel/limsup source.

No unpublished source is required.

## 8. Files produced/modified

- `research/web-search/2026-09-29_ROUND-0005_memory-tail-resolvent_REPORT.md`
- `research/coordination/web-to-chief/ROUND-0005_memory-tail-resolvent_RETURN.md`
- `bibliography/references.bib`
- `research/REFERENCES.md`
- `research/LITERATURE_MAP.md`

## 9. Recommended next trigger

Do not open another generic resolvent round.

Wait for TASK-0004.

If TASK-0004 certifies W1 survival, the next web task should be the **final theorem-specific novelty audit**, keyed to the exact rational model, exact cut-time certificate, exact memory-tail inequalities, and exact reachable-fiber theorem statement.
