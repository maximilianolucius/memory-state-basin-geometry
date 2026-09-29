# Structural Theorems — Basin Entry Geometry

**Owner:** Chief Researcher  
**Date:** 2026-09-29  
**Status:** PROVED ABSTRACT REDUCTIONS / MODEL-SPECIFIC BASIN HYPOTHESES OPEN

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
P(p,t)=e_0(T_t\iota(p))
\]
denote the physical observation of the standard IVP.

## 2. THEOREM E1 — basin-entry criterion for a multibasin reachable fiber

Let \(A_-\neq A_+\) be two asymptotic states.

Assume there exists a physical set \(U_-\subset X_{\rm phys}\) such that
\[
\iota(U_-)\subseteq\mathcal B(A_-).
\]

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

By reachability,
\[
T_{t_*}\iota(p)\in\mathcal R_\alpha.
\]
Also
\[
\iota(z)=T_0\iota(z)\in\mathcal R_\alpha.
\]

Both have present observation \(z\):
\[
e_0(T_{t_*}\iota(p))=z=e_0(\iota(z)).
\]

Since \(\iota(p)\in\mathcal B(A_+)\) and basins are positively invariant,
\[
T_{t_*}\iota(p)\in\mathcal B(A_+).
\]

Since \(z\in U_-\),
\[
\iota(z)\in\mathcal B(A_-).
\]

Therefore
\[
T_{t_*}\iota(p),\ \iota(z)\in\mathcal F_z
\]
lie in distinct basins. \(\square\)

### Classification

- proof status: PROVED;
- novelty: not claimed by itself;
- role: principal structural reduction after TASK-0001;
- important point: no same-age collision, transversality, or IFT is required.

## 3. COROLLARY E1-A — an arc of multibasin fibers

Under the hypotheses of E1, suppose
\[
J=\{t>0:P(p,t)\in U_-\}
\]
contains a nondegenerate interval.

Then for every \(t\in J\),
\[
\mathcal F_{P(p,t)}
\]
is multibasin.

Thus one survival-basin orbit entering an open cold-start basin region generates a continuous one-parameter family of multibasin present-state fibers.

### Classification

PROVED conditional on the basin memberships in E1.

## 4. THEOREM E2 — open persistence criterion

Consider a parameter family indexed by \(\mu\).

Suppose at \(\mu_*\) there exist \(p_*,t_*\) and an open physical set \(U_-(\mu_*)\) satisfying E1 with
\[
z_*=P_{\mu_*}(p_*,t_*)\in U_-(\mu_*).
\]

Assume in a neighborhood \(V\) of \(\mu_*\):

1. the solution observation map
   \[
   (\mu,p,t)\mapsto P_\mu(p,t)
   \]
   is continuous on the finite horizon of interest;

2. there is a persistent cold-start basin region in the sense that the set
   \[
   \mathcal U_-=
   \{(\mu,z):\iota(z)\in\mathcal B_\mu(A_-(\mu))\}
   \]
   contains an open neighborhood of \((\mu_*,z_*)\);

3. the survival-basin membership persists:
   \[
   \iota(p_*)\in\mathcal B_\mu(A_+(\mu))
   \]
   for all \(\mu\) in a neighborhood of \(\mu_*\), or more generally there is a continuous choice \(p(\mu)\) with this property.

Then for all sufficiently nearby \(\mu\), some reachable present-state fiber is multibasin.

### Proof

By openness of \(\mathcal U_-\) and continuity of \(P_\mu\), the strict entry
\[
P_\mu(p(\mu),t_*)\in U_-(\mu)
\]
persists for nearby \(\mu\). Apply E1 parameterwise. \(\square\)

### Classification

- proof: PROVED as an abstract topological criterion;
- novelty: not claimed for the topology;
- research burden: verify assumptions 2 and 3 for a natural Caputo family.

## 5. Why the old transversality program is secondary

For the embedded-age representation
\[
q=z=P(p,t_*),\qquad s=0,
\]
the equality
\[
P(p,t_*)=P(q,0)
\]
is automatic once \(z\) is defined.

Therefore a nonsingular collision Jacobian is irrelevant to existence.

Transversality/IFT becomes useful only if the project later studies:
- same-age collisions;
- smooth collision manifolds;
- uniqueness/multiplicity of collision branches;
- differentiable parameterizations of the fiber-intersection geometry.

Those are secondary to TARGET-A20.

## 6. Model-specific theorem template

For a positive strong-Allee predator–prey system, a paper-grade theorem can now have the form:

1. prove an open physical region \(R_{\rm ext}\) of cold starts satisfies
   \[
   \iota(R_{\rm ext})\subseteq\mathcal B(A_{\rm ext});
   \]
2. prove one standard initial condition \(p\) lies in
   \[
   \mathcal B(A_{\rm surv});
   \]
3. prove/certify its physical orbit enters \(R_{\rm ext}\);
4. conclude by E1 that the reached physical state has at least two reachable memory states with different asymptotic fates;
5. verify persistent basin membership to obtain E2 on an open family.

The only genuinely difficult steps are now basin membership and model-specific existence.
