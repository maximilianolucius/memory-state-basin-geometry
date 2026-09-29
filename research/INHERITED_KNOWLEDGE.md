# Inherited Knowledge

## Origin
This project descends from maximilianolucius/fractional-stability-front. The parent project mapped theorem-level fractional dynamical-systems theory and performed the novelty/fertility audit that selected this gap.

It did not prove the new theorem.

## Core inherited facts

### Physical state is not the whole state
For
\[
{}^C D^\alpha x(t)=g(x(t)),\qquad 0<\alpha<1,
\]
Doan and Kloeden (2021) embed the Caputo IVP into a Volterra semidynamical system on a function space.

For a standard physical IVP, the canonical initial embedding is constant, but after positive time the continuation state is generally nonconstant.

Use:
\[
\mathcal R_\alpha=\{T_t\iota(x_0):t\ge0,\ x_0\in X_{\rm phys}\},
\qquad
e_0(f)=f(0).
\]

Do not confuse arbitrary ambient memory states with physically reachable states.

### Reachable present-state observation is non-injective in d>=2
Cong and Tuan (2017) prove scalar nonintersection but construct higher-dimensional autonomous Caputo systems where trajectories from distinct standard initial data intersect at finite time.

Together with the continuation-state lift, this means
\[
e_0:\mathcal R_\alpha\to X_{\rm phys}
\]
need not be injective.

Thus same-present/different-reachable-memory is known and not novel.

### The unresolved residual is basin membership
The parent search did not identify a published theorem proving or forbidding
\[
\exists\phi,\psi\in\mathcal R_\alpha:
e_0(\phi)=e_0(\psi),\quad
\phi\in\mathcal B(A_1),\quad
\psi\in\mathcal B(A_2),\quad
A_1\neq A_2
\]
for a natural positive multistable Caputo system.

This is a search-qualified residual, not proof of absence.

### Hereditary basin theory is a serious adjacent threat
Huang, Yang, Yi and Zou (2014) study basins in bistable delay equations with an Allee-type population application. History-space basin geometry is not uniquely fractional.

The new project must isolate what is specifically nontrivial about the Caputo reachable set, present-state projection and singular power-law memory.

### Comparison theory narrows possible examples
Scalar, triangular and strongly ordered/monotone subclasses may force purity or prevent the desired geometry. Treat these as theorem opportunities.

### Double Allee is a natural testbed
Integer-order Double-Allee basin geometry is already rich, and direct fractional Double-Allee models already exist.

Mondal et al. (2025) provide a positive predator-prey model with Double Allee, group defense, multistability, basin calculations and commensurate/incommensurate orders.

The open structural object is not the basin plot. It is fiber geometry in the full reachable memory state.

### Scalar threshold movement is not the opportunity
Changing alpha does not move equilibrium roots when the RHS is unchanged. Under standard scalar separation assumptions, the unstable Allee equilibrium remains a barrier.

## Inherited recommendation
Characterize when physically reachable present-state fibers are basin-pure or multibasin, with extinction versus survival in strong/Double-Allee dynamics as the preferred applied realization.

## Main inherited risk
The parent project never proved that a natural Double-Allee model actually contains a multibasin fiber. Constructive realizability is the first major risk.
