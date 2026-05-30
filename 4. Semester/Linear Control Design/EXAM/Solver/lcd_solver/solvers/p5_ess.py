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


import control
import numpy as np


def _system_type(G) -> int:
    """Number of poles at the origin (within numerical tolerance)."""
    return sum(1 for p in control.poles(G) if abs(p) < 1e-9)


def solve_ess_table(G) -> dict:
    """Compute system type and ess for step / ramp / parabola under unity feedback."""
    t = _system_type(G)
    # Construct s*G, s^2*G via series with TF(s) factors.
    # python-control's dcgain on s^k * G can return NaN due to uncancelled
    # pole-zero pairs at the origin → use minreal to cancel them first.
    s_tf = control.tf("s")
    K_p = float(np.real(control.dcgain(G))) if t == 0 else math.inf
    K_v = float(np.real(control.dcgain(control.minreal(s_tf * G, verbose=False)))) if t == 1 else (math.inf if t > 1 else 0.0)
    K_a = float(np.real(control.dcgain(control.minreal(s_tf * s_tf * G, verbose=False)))) if t == 2 else (math.inf if t > 2 else 0.0)

    ess_step = 0.0 if t >= 1 else 1 / (1 + K_p)
    ess_ramp = 0.0 if t >= 2 else (1 / K_v if t == 1 else math.inf)
    ess_para = 0.0 if t >= 3 else (1 / K_a if t == 2 else math.inf)
    return {
        "type": t,
        "K_p": K_p, "K_v": K_v, "K_a": K_a,
        "ess_step": ess_step, "ess_ramp": ess_ramp, "ess_parabola": ess_para,
    }
