"""P1 — Models: ODE → TF and state-space → TF."""
from __future__ import annotations
import control
import numpy as np


def solve_ode_to_tf(y_coeffs: list[float], u_coeffs: list[float]) -> control.TransferFunction:
    """Build G(s) = u_coeffs(s) / y_coeffs(s).

    Coefficients are highest-degree-first, matching control.tf convention.
    Example: 5y'' + y' + 0.5y = 3u  →  y_coeffs=[5,1,0.5], u_coeffs=[3].
    """
    return control.tf(list(u_coeffs), list(y_coeffs))
