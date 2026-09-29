r"""Conservative long-run outcome classification.

Evidence discipline
-------------------
A finite-horizon label is **never** a basin proof (PROTOCOL.md, "Scientific
discipline").  Two tiers are therefore kept strictly separate.

tier CERTIFIED-CONDITIONAL
    :func:`certified_extinction_predicate` returns the subset of the positive
    cone on which extinction follows from two results already recorded in this
    repository, with no numerics at all:

      (i)  the scalar Caputo comparison principle (Wu 2020, ref. 22 in
           research/REFERENCES.md): since y >= 0 and x >= 0,
               ^C D^a x = x(1-x)(x-theta) - a x y  <=  x(1-x)(x-theta),
           so x(t) <= u(t) where ^C D^a u = u(1-u)(u-theta), u(0) = x(0);
      (ii) COROLLARY-S1A in research/CLAIMS.md (Area-Nieto 2023 model with the
           Doan-Kloeden 2022 intervalwise threshold theorem): u(0) in (0,theta)
           implies u(t) -> 0.

    Hence x(0) < theta implies x(t) -> 0, and then ^C D^a y = y(bx - m) with
    x eventually below m/b forces y -> 0.  The Compute Agent does **not**
    promote this to a theorem; it is handed to the Chief as a proof sketch whose
    two ingredients are already audited.  Label: CERTIFIED-CONDITIONAL.

tier NUMERICAL
    :func:`classify` is a deliberately strict finite-horizon tail test that
    returns ``AMBIGUOUS`` whenever the tail evidence is weak.  Every label it
    produces must survive the mesh/horizon refinement harness before being used.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

__all__ = ["Outcome", "classify", "certified_extinction_predicate", "positivity_report"]


class Outcome:
    EXTINCTION = 0
    COEXISTENCE = 1
    AMBIGUOUS = 2
    DIVERGENT = 3
    NEGATIVE = 4
    NAMES = {0: "EXTINCTION", 1: "COEXISTENCE", 2: "AMBIGUOUS", 3: "DIVERGENT", 4: "NEGATIVE"}


def certified_extinction_predicate(model):
    """Return ``f(Z) -> bool array``: True where extinction is CERTIFIED-CONDITIONAL.

    ``Z`` is (M,2) with columns (x, y).  The predicate is the *open* set
    ``{0 <= x < theta, y >= 0}`` with a safety margin subtracted so that the
    conclusion is insensitive to the floating-point value being reported.
    """
    theta = float(model.theta)

    def pred(Z, margin: float = 0.0):
        Z = np.atleast_2d(np.asarray(Z, dtype=np.float64))
        return (Z[:, 0] >= 0.0) & (Z[:, 0] < theta - margin) & (Z[:, 1] >= 0.0)

    pred.theta = theta
    pred.label = "CERTIFIED-CONDITIONAL (Wu 2020 comparison + COROLLARY-S1A)"
    return pred


def classify(
    traj: np.ndarray,
    equilibrium,
    *,
    tail_frac: float = 0.35,
    r_coex: float = 0.02,
    r_ext: float = 0.02,
    shrink_factor: float = 0.7,
    big: float = 1e3,
):
    """Strict finite-horizon outcome labels for a batch of trajectories.

    Parameters
    ----------
    traj        : (K, M, 2) stored trajectory.
    equilibrium : (2,) coexistence equilibrium.

    Rules (all must hold, otherwise AMBIGUOUS)
      COEXISTENCE : the whole tail lies inside the ball ``r_coex`` around E*
                    **and** the tail's max distance to E* is at most
                    ``shrink_factor`` times the max distance over the preceding
                    window of equal length (still contracting, not a limit cycle
                    grazing the ball).
      EXTINCTION  : the whole tail lies inside the box ``r_ext`` around the
                    origin **and** the tail max norm is at most
                    ``shrink_factor`` times the preceding window's max norm.
    """
    traj = np.asarray(traj)
    K, M, _ = traj.shape
    E = np.asarray(equilibrium, dtype=np.float64)
    out = np.full(M, Outcome.AMBIGUOUS, dtype=np.int8)

    finite = np.isfinite(traj).all(axis=0).all(axis=1)
    toobig = np.nanmax(np.abs(traj), axis=(0, 2)) > big
    out[~finite | toobig] = Outcome.DIVERGENT
    neg = np.nanmin(traj, axis=(0, 2)) < -1e-6
    out[(out == Outcome.AMBIGUOUS) & neg] = Outcome.NEGATIVE

    k0 = int(K * (1.0 - tail_frac))
    k1 = max(0, 2 * k0 - K)              # preceding window of the same length
    tail = traj[k0:]
    prev = traj[k1:k0] if k0 > k1 else traj[:k0]

    dE_tail = np.linalg.norm(tail - E, axis=2)
    dE_prev = np.linalg.norm(prev - E, axis=2)
    n_tail = np.linalg.norm(tail, axis=2)
    n_prev = np.linalg.norm(prev, axis=2)

    live = out == Outcome.AMBIGUOUS
    coex = live & (dE_tail.max(axis=0) < r_coex) & (
        dE_tail.max(axis=0) <= shrink_factor * np.maximum(dE_prev.max(axis=0), 1e-300)
    )
    ext = live & (n_tail.max(axis=0) < r_ext) & (
        n_tail.max(axis=0) <= shrink_factor * np.maximum(n_prev.max(axis=0), 1e-300)
    )
    out[coex] = Outcome.COEXISTENCE
    out[ext & ~coex] = Outcome.EXTINCTION
    return out


@dataclass
class PositivityReport:
    min_x: float
    min_y: float
    n_negative: int
    tol: float

    @property
    def ok(self) -> bool:
        return self.n_negative == 0


def positivity_report(traj: np.ndarray, tol: float = 1e-9) -> PositivityReport:
    traj = np.asarray(traj)
    mn = np.nanmin(traj, axis=(0, 1))
    n_neg = int((np.nanmin(traj, axis=(0, 2)) < -tol).sum())
    return PositivityReport(float(mn[0]), float(mn[1]), n_neg, tol)
