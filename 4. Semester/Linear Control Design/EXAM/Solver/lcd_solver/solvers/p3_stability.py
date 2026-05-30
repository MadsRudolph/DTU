"""P3 — Stability: stable-K range and Bode margins."""
from __future__ import annotations
import math

import control
import numpy as np


def _has_rhp_pole(G) -> bool:
    return any(float(p.real) > 1e-9 for p in control.poles(G))


def _nyquist_neg_real_crossings(G, omegas: np.ndarray) -> list[float]:
    """Return list of negative-real-axis x-values where G(jw) crosses, ascending |x|.

    Includes the DC value G(0) if it is real-negative — this is the "ω→0" crossing
    that an unstable plant with no other phase-180 crossing relies on for stabilization.
    """
    H = control.evalfr(G, 1j * omegas)
    H = np.asarray(H).squeeze()
    im = H.imag
    re = H.real
    crossings: list[float] = []

    # DC (ω→0) crossing: if G(0) is real-negative, treat it as a crossing.
    try:
        dc = float(np.real(control.dcgain(G)))
        if math.isfinite(dc) and dc < 0:
            crossings.append(dc)
    except Exception:
        pass

    for i in range(len(omegas) - 1):
        if im[i] == 0 or im[i] * im[i + 1] < 0:  # sign change in imag
            denom = (im[i] - im[i + 1])
            t = im[i] / denom if denom != 0 else 0
            re_cross = re[i] + t * (re[i + 1] - re[i])
            if re_cross < 0:
                crossings.append(float(re_cross))
    return sorted(crossings, key=abs)


def solve_stable_K_range(G) -> tuple[float, float]:
    """Return (K_low, K_high) such that 1+K*G is stable for K in (K_low, K_high).

    Stable plant -> (0, GM).  Unstable plant -> (1/|x_nearest_origin|, math.inf).
    """
    if _has_rhp_pole(G):
        omegas = np.logspace(-3, 5, 200_000)
        crossings = _nyquist_neg_real_crossings(G, omegas)
        if not crossings:
            raise ValueError("Could not find Nyquist negative-real-axis crossing for unstable plant")
        x = crossings[0]  # smallest |x|
        K_min = 1.0 / abs(x)
        return (K_min, math.inf)

    # Stable plant
    gm, _pm, _wpc, _wgc = control.margin(G)
    return (0.0, float(gm))
