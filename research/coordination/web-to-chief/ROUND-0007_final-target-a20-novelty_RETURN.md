# ROUND-0007 — RETURN TO CHIEF

**Round ID:** ROUND-0007  
**Request:** `research/coordination/chief-to-web/ROUND-0007_final-target-a20-novelty_REQUEST.md`  
**Search date:** 2026-09-30  
**Agent:** Deep Web Search Agent  
**Final substantive evidence commit before this return:** `48cd7b686ac5e14cd83b4c7cf2499665aca4b9fd`

## Final verdict

[
oxed{	ext{NOVELTY SURVIVES WITH CLAIM NARROWING}}
]

### Manuscript gate

[
oxed{	ext{MANUSCRIPT MAY BE UNLOCKED}}
]

provided the principal contribution is stated at the narrow theorem level below and the broad claims listed in §7 are explicitly avoided.

No formally published direct prior was found that proves the completed TARGET-A20 conjunction:

1. autonomous continuous-time Caputo dynamics;
2. a physically reachable inherited continuation state of a standard point IVP;
3. a canonical cold start at the **identical present physical value**;
4. the two states lying in distinct asymptotic basins;
5. extinction versus coexistence in a positive strong-Allee ecological realization;
6. and, here, a nondegenerate certified physical-time interval of such fibers.

---

## 1. Narrowest defensible principal novelty statement

Recommended manuscript wording:

> We prove, by a computer-assisted argument under the stated arithmetic model, that a concrete autonomous two-dimensional Caputo system with strong-Allee prey dynamics possesses a nondegenerate physical-time interval of reached states (z) for which the physically reachable present-state fiber contains both (i) the inherited continuation state of a standard point IVP converging to coexistence and (ii) the canonical cold-start state at the identical present value (z) converging to extinction.

Abstract theorem formulation:

> A physically reachable current-state fiber of an autonomous continuous-time Caputo semidynamical system can intersect distinct asymptotic basins; in the certified strong-Allee example, an entire reached arc of fibers is split between extinction and coexistence.

Recommended novelty qualification:

> No formally published theorem establishing this same-present-value, physically reachable Caputo basin split was identified in our targeted literature audit.

Do **not** use an unqualified “first ever.”

---

## 2. Search A — direct theorem killer

### Fractional trajectory intersections are already known

**Deshpande, Daftardar-Gejji & Vellaisamy (2019)**  
*Chaos* 29(1), 013113.  
DOI `10.1063/1.5052067`.

They rigorously classify same-time intersections, different-time intersections and self-intersections of linear fractional trajectories.

Therefore the paper must not claim that projected-state coincidence or fractional trajectory intersection is new.

But that paper does not prove:

- mixed basin membership in one current-state fiber;
- a physically reachable Doan–Kloeden continuation state;
- an inherited-state/cold-start comparison;
- or extinction versus coexistence.

### Memory-state architecture is already known

Doan–Kloeden 2021/2024 supplies the Caputo continuation-state semigroup and attractor framework.

Therefore memory-state representation and the present-value projection (e_0) are background, not novelty.

### Direct-killer result

No formally published theorem was found matching or subsuming TARGET-A20.

[
oxed{	ext{DIRECT PRIOR: NOT FOUND IN SEARCHED CORPUS}}
]

---

## 3. Search B — hereditary/headpoint analogue

### Strongest conceptual prior

**Szaksz, Stepan & Habib (2024)**  
“Dynamical integrity estimation in time delayed systems: A rapid iterative algorithm.”  
*Journal of Sound and Vibration* 571, 118045.  
DOI `10.1016/j.jsv.2023.118045`.

This paper is extremely close conceptually.

It explicitly states that convergence in a DDE depends on the **entire initial function**, not only its headpoint.

It considers different constrained histories with the **same headpoint**:
- constant;
- linear;
- jump;
- free vibration.

Even more importantly, their algorithm sometimes selects a new initial-condition headpoint at a point already visited by a previous nonlinear trajectory. They explicitly note that:

- the new integration uses a constrained initial history;
- the old trajectory segment came from the full nonlinear DDE history;
- therefore the restarted trajectory will differ from the previous one.

That is the closest literature analogue to

[
T_tiota(p)
quad	ext{versus}quad
iota(x(t;p)).
]

### Why it is not a killer

They do **not** prove that the two same-headpoint histories lie in different asymptotic basins.

The discussion is algorithmic/probabilistic (“likely diverging”), not a theorem of opposite basin membership.

### 2026 continuation

**Szaksz & Habib (2026)**  
*International Journal of Non-Linear Mechanics* 185, 105337.  
DOI `10.1016/j.ijnonlinmec.2026.105337`.

This reinforces full-history/headpoint integrity methodology but still does not prove the exact same-headpoint/opposite-basin statement.

### Transfer to Caputo

Transfer is not routine:

- DDE state = finite-delay history segment;
- Doan–Kloeden Caputo state = Volterra continuation/forcing function on (mathbb R_+);
- TARGET-A20 restricts to the **physically reachable** Caputo state set;
- the inherited and canonical embeddings are specific to that architecture.

Verdict:

**CLOSE ADJACENT PRIOR — NOT DIRECT PRIOR.**

---

## 4. Search C — current fractional ecology

The broad application space is already crowded.

### Key competitors checked

**Ramesh et al. 2025**  
DOI `10.1371/journal.pone.0305179`  
Caputo memory + Double Allee + extinction/coexistence + stability.

**Mondal et al. 2025 — Journal of Biological Physics**  
DOI `10.1007/s10867-025-09670-0`  
Caputo double-Allee predator–prey dynamics and memory-dependent emergent states.

**Wang & Han 2025**  
DOI `10.1007/s12346-024-01212-8`  
Caputo Allee/refuge dynamics, global stability and bifurcation.

**Mondal et al. 2025 — Chinese Journal of Physics**  
DOI `10.1016/j.cjph.2025.09.020`  
Fractional Double Allee + group defense + multistability/basin stability.

**Saha et al. 2026**  
DOI `10.1007/s13540-026-00515-8`  
This is the strongest basin competitor found. It explicitly presents fractional ecological basins corresponding to extinction, predator extinction and coexistence.

**Pippal & Sati 2026**  
DOI `10.30538/oms2026.0339`  
Standard Caputo + strong Allee; extinction stable; coexistence has a basin-restricted Mittag–Leffler certificate.

**Baghel 2026**  
DOI `10.1016/j.chaos.2026.117880`  
Caputo strong-Allee age-structured/delayed predator–prey dynamics.

**Youssef & Dasumani 2026**  
DOI `10.3390/fractalfract10100664`  
Very recent strong-Allee/memory ecological model, but using the Atangana–Baleanu–Caputo operator rather than standard Caputo.

### Consequence

The manuscript must not claim novelty for:

- fractional ecological memory;
- Allee + fractional derivatives;
- extinction/coexistence multistability;
- basin plots;
- basin-restricted coexistence certificates.

None of the searched papers proves the **inherited continuation state versus canonical cold start at the identical physical state** basin reversal.

[
oxed{	ext{ECOLOGICAL DIRECT KILLER: NOT FOUND}}
]

---

## 5. Search D — novelty by theorem component

### D1. One multibasin physically reachable Caputo fiber

**SURVIVES.**

This is the principal theoretical novelty identified by the audit.

### D2. Nondegenerate time interval of such fibers

**SURVIVES**, but should be presented as a consequence of the certified excursion plus E1-A rather than as a separate foundational contribution.

### D3. Extinction versus coexistence strong-Allee realization

**SURVIVES AS APPLICATION-SPECIFIC NOVELTY.**

Extinction/coexistence multistability itself is not new; its occurrence as two labels on the same physically reached fiber is the new conjunction.

### D4. Inherited continuation versus cold start

**CORE CONCEPTUAL MECHANISM, BUT NARROW CLAIM REQUIRED.**

Generic restart/history dependence is known in DDE/hereditary systems.

The defensible novelty is the rigorous autonomous Caputo realization with physically reachable continuation states and opposite basin labels.

---

## 6. Search E — method overlap

The TASK-0006 certificate uses:

- cellwise source sup / oscillation / interpolation-bubble bounds;
- componentwise positive self-map (F(b)<b);
- Perron-weighted contraction;
- orbit-linearized weakly singular Volterra validation;
- memory-tail Mittag–Leffler certification.

No published direct method duplicate was found.

But all generic ingredients have substantial prior:
- validated integral equations;
- weakly singular Volterra resolvents;
- radii/fixed-point CAP;
- Perron/positive-operator estimates;
- certified fractional numerical propagation.

Therefore:

> treat the CAP as sophisticated enabling proof machinery, not as the principal novelty, unless a reusable numerical theorem is separately developed and compared against this literature.

Verdict:

**NO EXACT METHOD DUPLICATE FOUND — SECONDARY NOVELTY ONLY.**

---

## 7. Claims the manuscript must avoid

1. “First demonstration that memory gives different futures from the same present state.”
2. “First fractional trajectory intersection / failure of nonintersection.”
3. “First basin geometry in an infinite-dimensional history system.”
4. “First basin analysis in fractional predator–prey systems.”
5. “First extinction/coexistence bistability in a fractional Allee model.”
6. “First history/headpoint dependence of basin membership.”
7. “The predator–prey vector field is new.”
8. “First certified/validated numerical solution of a fractional system.”
9. “The generic radii/Perron/resolvent machinery is new.”
10. “End-to-end interval/Arb rigor” for the current certificate.
11. “Parameter-open family” unless a separate parameter-persistence theorem/certificate is added.
12. Scalar purity/completeness as principal novelty.

---

## 8. Search F — arithmetic/referee pressure

### Standard expectation

**Warwick Tucker (2011), _Validated Numerics_** reflects the normal referee expectation:

- rigorous control of rounding;
- interval/set-valued enclosures;
- accounting for all numerical error sources.

### Non-interval rigorous arithmetic is legitimate

**Mrozek (1996)**  
DOI `10.1006/jsco.1996.0061`.

Mrozek develops rigorous symbolic/a-priori floating-point error analysis explicitly as an alternative to interval arithmetic for computer-assisted proofs.

Therefore TASK-0006's binary64 layers are not automatically unacceptable if the bounds really cover all operations under the declared model.

### Main referee vulnerability

The weakest point is not binary64 itself.

It is the assumption that

[
	exttt{pow},	exttt{expm1},	exttt{log1p},	exttt{gamma}
]

are accurate to a few ulp.

Unless the exact libm implementation/platform and that ulp bound are independently certified, this remains an external arithmetic assumption.

### Recommendation

Strongly recommended before submission:

- replace load-bearing libm elementary-function evaluations with Arb/MPFR or verified directed interval wrappers;
- or produce a machine-specific audited bound that removes the unsupported “few ulp” assumption.

If not hardened, use the exact phrase:

> **computer-assisted theorem under the stated IEEE-754/libm arithmetic model**

and isolate the assumption conspicuously.

Do not describe it simply as an end-to-end interval proof.

This is a **referee robustness issue**, not a novelty failure.

---

## 9. Publication disposition

Final hostile-search result:

[
oxed{	ext{NOVELTY SURVIVES WITH CLAIM NARROWING}}
]

The manuscript can now be unlocked.

Recommended contribution hierarchy:

### Principal
Physically reachable autonomous Caputo present-state fiber intersecting extinction and coexistence basins at the same present value.

### Strong secondary
A certified nondegenerate physical-time arc of such fibers in a positive strong-Allee ecological system.

### Supporting
Scalar purity/completeness contrast, basin-entry structural theorem, and computer-assisted validation architecture.

### Background / not new
Memory-state representation, fractional intersections, ecological multistability/basins, generic validated numerics.

## 10. Files modified

- `research/web-search/2026-09-30_ROUND-0007_final-target-a20-novelty_REPORT.md`
- `research/coordination/web-to-chief/ROUND-0007_final-target-a20-novelty_RETURN.md`
- `bibliography/references.bib`
- `research/REFERENCES.md`
- `research/LITERATURE_MAP.md`

## 11. Final recommendation

Chief may move to manuscript mode.

Before submission, one targeted non-novelty task remains desirable but not required for theorem novelty:

> harden the few-ulp libm layer to end-to-end verified elementary-function enclosures.

No further generic web-search round is recommended unless the manuscript introduces a materially broader theorem claim than TARGET-A20.
