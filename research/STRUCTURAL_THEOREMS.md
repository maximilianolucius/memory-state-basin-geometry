# Structural Theorems — Basin Entry Geometry

**Owner:** Chief Researcher  
**Date:** 2026-09-29  
**Status:** E1/E2/E3 PROVED ABSTRACTLY; MODEL-SPECIFIC SURVIVAL CONVERGENCE OPEN

## 1. Setup

Let
\[
(\mathfrak C,T_t),\qquad
\iota:X_{\rm phys}\to\mathfrak C,\qquad
e_0:\mathfrak C\to X_{\rm phys}
\]
be the audited continuation-state semidynamical system.

Define
\[
\mathcal R_\alpha=\{T_t\iota(p):t\ge0,\ p\in X_{\rm phys}\},
\qquad
\mathcal F_z=e_0^{-1}(z)\cap\mathcal R_\alpha.
\]

Let
\[
P(p,t)=e_0(T_t\iota(p)).
\]

## 2. THEOREM E1 — basin-entry criterion

Let \(A_-\neq A_+\) be two asymptotic states.

Assume
\[
\iota(U_-)\subseteq\mathcal B(A_-)
\]
for a physical set \(U_-\subset X_{\rm phys}\).

If
\[
\iota(p)\in\mathcal B(A_+)
\]
and for some \(t_*>0\),
\[
z=P(p,t_*)\in U_-,
\]
then
\[
\mathcal F_z
\]
is multibasin.

### Proof

Both
\[
T_{t_*}\iota(p),\qquad \iota(z)
\]
are physically reachable and satisfy
\[
e_0(T_{t_*}\iota(p))=z=e_0(\iota(z)).
\]

Positive invariance of basins gives
\[
T_{t_*}\iota(p)\in\mathcal B(A_+),
\]
while
\[
\iota(z)\in\mathcal B(A_-).
\]

Therefore the common fiber contains two distinct basin labels. \(\square\)

## 3. COROLLARY E1-A — arc of multibasin fibers

If
\[
J=\{t>0:P(p,t)\in U_-\}
\]
contains a nondegenerate interval, then every
\[
\mathcal F_{P(p,t)},\qquad t\in J,
\]
is multibasin.

## 4. THEOREM E2 — open persistence criterion

For a parameter family \(\mu\), suppose E1 holds at \(\mu_*\) with strict entry
\[
P_{\mu_*}(p_*,t_*)\in U_-(\mu_*).
\]

Assume near \(\mu_*\):

1. \((\mu,p,t)\mapsto P_\mu(p,t)\) is continuous on the finite horizon;
2. the cold-start basin region persists openly;
3. survival-basin membership of \(p_*\), or of a continuous choice \(p(\mu)\), persists.

Then nearby parameter values also possess a multibasin reachable present-state fiber.

The proof is continuity + openness + E1. No collision transversality is required.

## 5. THEOREM E3 — physical convergence lifts to continuation-state convergence

Consider a standard point IVP
\[
{}^CD^\alpha x=g(x),
\qquad x(0)=p,
\]
with physical solution \(x(t;p)\).

Assume
\[
x(t;p)\to x^*,
\qquad g(x^*)=0.
\]

Then
\[
T_t\iota(p)\to\iota(x^*)
\]
in the compact-open topology of \(\mathfrak C\).

Consequently,
\[
\iota(p)\in\mathcal B(\iota(x^*)).
\]

### Proof

Let \(\eta\ge0\) denote memory age.

For the constant input \(\iota(p)\),
\[
(T_t\iota(p))(\eta)
=
p+
\frac1{\Gamma(\alpha)}
\int_0^t
(t+\eta-s)^{\alpha-1}g(x(s))\,ds.
\]

The physical trajectory satisfies
\[
x(t+\eta)
=
p+
\frac1{\Gamma(\alpha)}
\int_0^{t+\eta}
(t+\eta-s)^{\alpha-1}g(x(s))\,ds.
\]

Subtract:
\[
x(t+\eta)-(T_t\iota(p))(\eta)
=
\frac1{\Gamma(\alpha)}
\int_t^{t+\eta}
(t+\eta-s)^{\alpha-1}g(x(s))\,ds.
\]

For fixed \(N>0\),
\[
\sup_{0\le\eta\le N}
\left\|
x(t+\eta)-(T_t\iota(p))(\eta)
\right\|
\le
\frac{N^\alpha}{\Gamma(\alpha+1)}
\sup_{s\in[t,t+N]}\|g(x(s))\|.
\]

Since
\[
x(t)\to x^*
\]
and \(g\) is continuous with \(g(x^*)=0\), the right side tends to zero.

Also,
\[
\sup_{0\le\eta\le N}
\|x(t+\eta)-x^*\|
\to0.
\]

Hence
\[
\sup_{0\le\eta\le N}
\|(T_t\iota(p))(\eta)-x^*\|
\to0
\]
for every \(N\), which is exactly compact-open convergence:
\[
T_t\iota(p)\to\iota(x^*).
\]
\(\square\)

### Classification

- proof: PROVED directly from the audited transfer formula;
- novelty: supporting bridge, not principal novelty;
- role: reduces the survival-basin problem to physical convergence of a standard IVP.

## 6. Model-specific theorem template after ROUND-0003

For the project model:

1. X1 already proves
   \[
   \iota(R_{\rm ext})\subseteq\mathcal B(\iota(0,0));
   \]
2. prove one standard IVP
   \[
   x(t;p)\to E^*;
   \]
3. E3 gives
   \[
   \iota(p)\in\mathcal B(\iota(E^*));
   \]
4. certify
   \[
   x(t_*;p)\in R_{\rm ext};
   \]
5. E1 gives TARGET-A20.

This is now the shortest rigorous route.
