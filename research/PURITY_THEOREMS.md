# Purity / Impossibility Theorem Program

**Owner:** Chief Researcher  
**Date:** 2026-09-29  
**Status:** SCALAR CLOSED / TRIANGULAR COMPLETENESS / MONOTONE REQUIRES EXTRA STRUCTURE

## 1. Purpose

The purity program separates classes where current physical state is sufficient for basin membership from the genuinely multidimensional class sought by the main project.

The scalar result is retained as a rigorous completeness/impossibility statement, not as principal novelty.

## 2. COMPLETENESS-S1 — scalar equilibrium-partition fiber purity

Consider
\[
{}^C D_{0+}^{\alpha}x(t)=g(x(t)),
\qquad 0<\alpha<1,
\]
with standard point initial data and a well-defined continuation-state semigroup.

Let
\[
c_1<\cdots<c_m
\]
be equilibrium values, and let the open components of the complement of the equilibrium set be
\[
I_0=(-\infty,c_1),\qquad
I_j=(c_j,c_{j+1}),\qquad
I_m=(c_m,\infty),
\]
intersected with the physical domain when appropriate.

### Theorem S1

Assume:

**S1-H1 — equilibrium barriers.**  
For every \(x_0\neq c_k\),
\[
x(t;x_0)\neq c_k
\qquad\forall t>0,\ \forall k.
\]

**S1-H2 — intervalwise basin classification.**  
For each nonempty physical interval \(I_j\), there exists an asymptotic state/attractor \(A_{\sigma(j)}\) such that
\[
x_0\in I_j
\Longrightarrow
\iota(x_0)\in\mathcal B(A_{\sigma(j)}).
\]

**S1-H3 — stationary equilibrium lifts.**  
Each equilibrium \(c_k\) yields the stationary lifted state \(\iota(c_k)\), and no non-equilibrium standard trajectory reaches \(c_k\) at positive time.

Then every physically reachable present-state fiber is basin-pure:

- if \(x\in I_j\), then
\[
\mathcal F_x\subseteq\mathcal B(A_{\sigma(j)});
\]

- if \(x=c_k\), then
\[
\mathcal F_x=\{\iota(c_k)\}.
\]

Hence no reachable scalar present-state fiber can intersect two distinct basins under S1-H1--S1-H3.

### Proof

Take
\[
\phi=T_t\iota(x_0)\in\mathcal F_x.
\]

If \(x\in I_j\), then by S1-H1 the trajectory cannot cross an equilibrium separator. Therefore \(x_0\) and \(x\) belong to the same connected component \(I_j\). By S1-H2,
\[
\iota(x_0)\in\mathcal B(A_{\sigma(j)}).
\]
Basins are positively invariant under the continuation-state semigroup, so
\[
T_t\iota(x_0)\in\mathcal B(A_{\sigma(j)}).
\]
Since \(\phi\) was arbitrary,
\[
\mathcal F_x\subseteq\mathcal B(A_{\sigma(j)}).
\]

If \(x=c_k\) and
\[
T_t\iota(x_0)\in\mathcal F_{c_k},
\]
then
\[
x(t;x_0)=c_k.
\]
By S1-H3 this forces \(x_0=c_k\). Since the equilibrium lift is stationary,
\[
T_t\iota(c_k)=\iota(c_k),
\]
hence
\[
\mathcal F_{c_k}=\{\iota(c_k)\}.
\]
\(\square\)

### Evidence / novelty classification

- proof: analytic, complete under H1--H3;
- contribution class: COMPLETENESS RESULT;
- novelty: not claimed;
- ROUND-0002 verdict: STANDARD CONSEQUENCE.

## 3. Imported scalar separation — exact qualification

Cong & Tuan (2017), Theorem 4, prove strict scalar separation for
\[
{}^C D^\alpha x=f(t,x)
\]
when \(f\) is continuous and globally Lipschitz in \(x\) with a continuous time-dependent Lipschitz bound:
\[
|f(t,x)-f(t,y)|\le L(t)|x-y|.
\]

In particular, equilibrium solutions are strict barriers under those hypotheses.

Do not cite this theorem as automatically covering an arbitrary \(C^1\) or polynomial vector field on all of \(\mathbb R\).

Diethelm & Ford (2012) may be cited historically, but not as the load-bearing separation proof.

## 4. COROLLARY S1-A — rigorous Caputo strong-Allee fiber purity

Consider the published Area–Nieto model
\[
{}^C D^\alpha x
=
x(1-x)(x-\theta),
\qquad
0<\theta<1,\quad 0<\alpha<1.
\]

Let
\[
g(x)=x(1-x)(x-\theta).
\]

The equilibria are
\[
0,\quad\theta,\quad1,
\]
and are simple:
\[
g'(0)=-\theta<0,\qquad
g'(\theta)=\theta(1-\theta)>0,\qquad
g'(1)=\theta-1<0.
\]

Moreover \(xg(x)\) has negative quartic leading term, so the dissipativity condition used by Doan & Kloeden (2022) holds for suitable \(a,b>0\).

Their scalar attractor/interval classification yields:
\[
0<x_0<\theta
\Longrightarrow
x(t;x_0)\to0,
\]
\[
x_0>\theta
\Longrightarrow
x(t;x_0)\to1
\]
on the positive physical domain, while \(x_0=\theta\) is stationary.

Therefore:
\[
0<x<\theta
\Longrightarrow
\mathcal F_x\subseteq\mathcal B(0),
\]
\[
x>\theta
\Longrightarrow
\mathcal F_x\subseteq\mathcal B(1),
\]
and
\[
\mathcal F_\theta=\{\iota(\theta)\}.
\]

### Attribution discipline

Area & Nieto (2023) provide the exact published Caputo Allee model.

The rigorous global asymptotic classification used here comes from applying Doan & Kloeden (2022). Do not attribute that global theorem to Area & Nieto.

### Interpretation

For this standard scalar strong-Allee Caputo model, two populations with the same current scalar abundance cannot belong to extinction and survival basins solely because their physically reachable Caputo memory states differ.

This is a class-specific impossibility result, not a statement about every scalar fractional model imaginable.

## 5. Triangular completeness corollary

Consider a triangular or cascade system having a closed scalar coordinate \(x_1\).

A safe fiber-purity corollary follows if:

1. the scalar coordinate satisfies Theorem S1; and
2. the interval containing the current value of \(x_1\) determines the asymptotic basin of the full system.

Then equality of the full present state implies equality of the basin-determining coordinate and therefore equality of the basin label.

### Status

USEFUL COMPLETENESS.

General triangularity alone is not asserted to suffice.

Direct prior is substantial: Cong–Tuan (2017) gives triangular nonintersection under Lipschitz hypotheses, while Doan–Kloeden (2022) gives global attractor/convergence results for a special product-triangular class.

## 6. Monotone/comparison limitation

Published Caputo comparison principles provide order propagation for appropriate scalar, quasi-monotone, mixed quasi-monotone and related systems.

They do not imply
\[
e_0(\phi)=e_0(\psi)
\Longrightarrow
\omega(\phi)=\omega(\psi).
\]

Equal present endpoint does not imply ordered histories, and even ordered histories need not converge to the same attractor.

A genuine comparison-based fiber-purity theorem requires additional endpoint-determining structure, for example:
- a scalar threshold coordinate or functional;
- endpoint-defined invariant regions carrying one basin label; or
- an explicit factorization of basin membership through \(e_0\).

No generic monotone purity theorem is promoted.

## 7. Consequence for the main program

The scalar threshold class is closed as a source of the target phenomenon.

The main positive search should therefore remain multidimensional and nontrivially coupled.

This result does not prove that \(d=2\) is globally minimal; it proves only that the audited scalar equilibrium-partition class is impossible.
