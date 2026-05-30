"""P4 — 2nd-order specs: bidirectional Mp <-> zeta and the time/freq spec set."""
from __future__ import annotations
import math


def _Mp_from_zeta(zeta: float) -> float:
    if zeta <= 0 or zeta >= 1:
        return 0.0
    return math.exp(-math.pi * zeta / math.sqrt(1 - zeta ** 2))


def _zeta_from_Mp(Mp: float) -> float:
    if Mp <= 0:
        return 1.0
    L = math.log(1 / Mp)
    return L / math.sqrt(math.pi ** 2 + L ** 2)


def solve_2nd_order(*, Mp=None, zeta=None, omega_n=None, t_p=None, t_s_2pct=None) -> dict:
    """Fill in whichever 2nd-order quantities are derivable.

    Accept any subset of {Mp, zeta} and any subset of {omega_n, t_p, t_s_2pct}.
    Inconsistent inputs raise ValueError.
    """
    # ---- damping ----
    if Mp is not None and zeta is not None:
        if abs(_zeta_from_Mp(Mp) - zeta) > 1e-2:
            raise ValueError(f"Mp={Mp} and zeta={zeta} are inconsistent")
    if zeta is None and Mp is not None:
        zeta = _zeta_from_Mp(Mp)
    elif zeta is not None and Mp is None:
        Mp = _Mp_from_zeta(zeta)
    elif zeta is None and Mp is None:
        raise ValueError("Provide at least one of {Mp, zeta}")

    # ---- omega_n ----
    if omega_n is None:
        if t_p is not None and zeta < 1:
            omega_n = math.pi / (t_p * math.sqrt(1 - zeta ** 2))
        elif t_s_2pct is not None:
            omega_n = 4.0 / (zeta * t_s_2pct)

    out = {"zeta": zeta, "Mp": Mp, "Mp_pct": 100 * Mp}
    if omega_n is None:
        return out

    out["omega_n"] = omega_n
    out["omega_d"] = omega_n * math.sqrt(max(0.0, 1 - zeta ** 2))
    out["t_p"] = math.pi / out["omega_d"] if out["omega_d"] > 0 else math.inf
    out["t_s_2pct"] = 4.0 / (zeta * omega_n) if zeta > 0 else math.inf
    out["t_s_5pct"] = 3.0 / (zeta * omega_n) if zeta > 0 else math.inf
    out["t_r"] = 1.8 / omega_n
    out["omega_BW"] = omega_n * math.sqrt(
        (1 - 2 * zeta ** 2) + math.sqrt(4 * zeta ** 4 - 4 * zeta ** 2 + 2)
    )
    if zeta < math.sqrt(2) / 2:
        out["omega_r"] = omega_n * math.sqrt(1 - 2 * zeta ** 2)
        out["M_r"] = 1 / (2 * zeta * math.sqrt(1 - zeta ** 2))
    return out
