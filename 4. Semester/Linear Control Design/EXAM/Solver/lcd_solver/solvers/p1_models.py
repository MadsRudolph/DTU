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


def solve_state_space_to_tf(A, B, C, D) -> control.TransferFunction:
    """G(s) = C (sI - A)^{-1} B + D, via control.ss2tf.

    A, B, C, D may be lists or numpy arrays. Shapes:
      A: (n, n), B: (n, 1), C: (1, n), D: (1, 1)
    """
    A_arr = np.atleast_2d(np.asarray(A, dtype=float))
    B_arr = np.atleast_2d(np.asarray(B, dtype=float))
    C_arr = np.atleast_2d(np.asarray(C, dtype=float))
    D_arr = np.atleast_2d(np.asarray(D, dtype=float))
    n = A_arr.shape[0]
    if A_arr.shape != (n, n):
        raise ValueError(f"A must be square, got {A_arr.shape}")
    if B_arr.shape != (n, 1):
        raise ValueError(f"B must be ({n},1), got {B_arr.shape}")
    if C_arr.shape != (1, n):
        raise ValueError(f"C must be (1,{n}), got {C_arr.shape}")
    if D_arr.shape != (1, 1):
        raise ValueError(f"D must be (1,1), got {D_arr.shape}")
    return control.ss2tf(control.ss(A_arr, B_arr, C_arr, D_arr))
