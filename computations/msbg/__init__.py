"""Memory-State Basin Geometry — compute package (TASK-0001).

Modules
-------
mittag_leffler : arbitrary-precision Mittag-Leffler function E_alpha and 2x2 matrix version
solvers        : three independent history-retaining Caputo solvers (batched, float64 and mpmath)
models         : vector fields used by TASK-0001
basins         : conservative long-run outcome classification and certified extinction predicate
collisions     : physical-state collision detection, refinement and Jacobian diagnostics
provenance     : environment capture, hashing, manifests

Evidence discipline (COMPUTE_AGENT_INITIAL_PROMPT.md): nothing in this package
proves a theorem.  Functions return labelled evidence objects only.
"""

__version__ = "0.1.0"
