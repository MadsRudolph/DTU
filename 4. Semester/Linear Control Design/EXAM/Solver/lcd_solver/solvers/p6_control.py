"""P6 — Controller design: PI-Lead three-way solver, P-for-PM."""
from __future__ import annotations
import math

import control
import numpy as np


def _phi_PI(N_i: float) -> float:
    """PI phase lag at the design crossover frequency, in degrees."""
    return -math.degrees(math.atan(1 / N_i))


def _phi_lead(alpha: float) -> float:
    """Lead phase max, in degrees."""
    return math.degrees(math.asin((1 - alpha) / (1 + alpha)))


def _plant_phase_deg(G, omegas: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return (omegas, plant phase in deg, monotonically aligned)."""
    H = control.evalfr(G, 1j * omegas)
    H = np.squeeze(np.asarray(H))
    phase = np.unwrap(np.angle(H)) * 180.0 / math.pi
    return omegas, phase


def solve_pi_lead(*, unknown: str, omega_c=None, gamma_M_deg=None, phi_G_deg=None,
                   N_i=None, alpha=None, G=None) -> float:
    """Three modes via the phase-budget equation:

        -180 + gamma_M = phi_G + phi_Lead + phi_PI

    unknown='alpha': needs (omega_c, gamma_M_deg, phi_G_deg, N_i).
    unknown='Ni':    needs (omega_c, gamma_M_deg, phi_G_deg, alpha).
    unknown='KP':    needs (G, gamma_M_deg, alpha, N_i).
    """
    if unknown == "alpha":
        phi_pi = _phi_PI(N_i)
        phi_lead_required = -180 + gamma_M_deg - phi_G_deg - phi_pi
        s = math.sin(math.radians(phi_lead_required))
        return (1 - s) / (1 + s)

    if unknown == "Ni":
        phi_lead = _phi_lead(alpha)
        # -180 + gamma_M = phi_G + phi_lead + phi_PI
        # phi_PI = -atan(1/N_i) [deg]   →   -atan(1/N_i) = -180 + gamma_M - phi_G - phi_lead
        # So atan(1/N_i) = 180 - gamma_M + phi_G + phi_lead
        atan_deg = 180 - gamma_M_deg + phi_G_deg + phi_lead
        return 1.0 / math.tan(math.radians(atan_deg))

    if unknown == "KP":
        if G is None:
            raise ValueError("KP mode requires plant G")
        phi_pi = _phi_PI(N_i)
        phi_lead = _phi_lead(alpha)
        phi_G_required = -180 + gamma_M_deg - phi_lead - phi_pi
        # Find omega_c where plant phase = phi_G_required
        omegas = np.logspace(-2, 4, 200_000)
        ws, phases = _plant_phase_deg(G, omegas)
        order = np.argsort(phases)
        omega_c = float(np.interp(phi_G_required, phases[order], ws[order]))
        # Build PI and Lead at omega_c
        tau_i = N_i / omega_c
        tau_d = 1.0 / (omega_c * math.sqrt(alpha))
        s = control.tf("s")
        C_PI = (tau_i * s + 1) / (tau_i * s)
        C_d = (tau_d * s + 1) / (alpha * tau_d * s + 1)
        L = G * C_PI * C_d
        H = control.evalfr(L, 1j * omega_c)
        H = complex(np.squeeze(np.asarray(H)))
        return float(1.0 / abs(H))

    raise ValueError(f"unknown must be 'alpha', 'Ni', or 'KP', got {unknown!r}")


def solve_P_for_PM(G, target_PM_deg: float) -> dict[str, float]:
    """P-controller that achieves target phase margin.

    Find omega where ∠G(jw) = -180 + gamma_M, set K_P = 1/|G(jw)|.
    """
    omegas = np.logspace(-3, 4, 500_000)
    H = control.evalfr(G, 1j * omegas)
    H = np.squeeze(np.asarray(H))
    phases = np.unwrap(np.angle(H)) * 180.0 / math.pi
    target_phase = -180 + target_PM_deg

    order = np.argsort(phases)
    omega_c = float(np.interp(target_phase, phases[order], omegas[order]))
    H_at = control.evalfr(G, 1j * omega_c)
    H_at = complex(np.squeeze(np.asarray(H_at)))
    K_P = float(1.0 / abs(H_at))
    return {"K_P": K_P, "omega_c": omega_c}
