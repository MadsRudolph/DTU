"""P5 — Steady-state error."""
from __future__ import annotations
import math


def solve_KP_from_ess(G0: float, G0_unit: str, ess_target: float) -> float:
    """Step input on type-0 plant: ess = 1/(1 + K_P G(0)) → K_P = (1/ess − 1)/G(0).

    G0_unit ∈ {'linear', 'dB'}.  Ramp/parabola variants are deferred.
    """
    if G0_unit == "dB":
        G0_lin = 10 ** (G0 / 20)
    elif G0_unit == "linear":
        G0_lin = G0
    else:
        raise ValueError(f"G0_unit must be 'linear' or 'dB', got {G0_unit!r}")
    if G0_lin == 0:
        raise ValueError("G(0) = 0 — cannot achieve any non-trivial ess with finite K_P")
    return ((1 / ess_target) - 1) / G0_lin
