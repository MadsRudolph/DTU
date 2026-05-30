"""P2 — Bode read-off composition.

Given the user's read-off of (DC dB, list of magnitude-slope corners, list of
phase events), build a candidate G(s).

Algorithm:
  - At each corner (omega, delta_slope_dB_per_dec):
      delta_slope = -20  ->  add a pole at -omega (LHP) or +omega (RHP)
      delta_slope = +20  ->  add a zero at -omega (LHP) or +omega (RHP)
      |delta_slope| = 40 ->  repeated factor
  - Sign of the phase event at the same omega disambiguates LHP vs RHP:
      pole: LHP -> phase -90, RHP -> phase +90
      zero: LHP -> phase +90, RHP -> phase -90
  - Static factor set so that |G(0)| in dB matches dc_gain_dB.
"""
from __future__ import annotations
import math
from collections import Counter

import control
import matplotlib
matplotlib.use("Agg")  # headless-safe for tests; UI overrides
import matplotlib.pyplot as plt
import numpy as np


def _factor_kind(delta_slope: int, phase_delta: int) -> tuple[str, str]:
    """Return ('pole'|'zero', 'LHP'|'RHP')."""
    pz = "pole" if delta_slope < 0 else "zero"
    if pz == "pole":
        side = "LHP" if phase_delta < 0 else "RHP"
    else:
        side = "LHP" if phase_delta > 0 else "RHP"
    return pz, side


def compose_tf_from_bode(dc_gain_dB: float, corners: list[tuple[float, int]],
                          phase_events: list[tuple[float, int]]):
    """Return (TransferFunction, matplotlib.figure.Figure)."""
    # Group phase events by omega so we can look up the sign at each corner.
    phase_at: dict[float, int] = {}
    for w, dphi in phase_events:
        phase_at[round(w, 9)] = phase_at.get(round(w, 9), 0) + dphi

    poles: list[float] = []
    zeros: list[float] = []

    # Combine multiple corners at the same omega (e.g. double pole)
    grouped: dict[float, int] = {}
    for w, ds in corners:
        grouped[round(w, 9)] = grouped.get(round(w, 9), 0) + ds

    for w, total_slope in grouped.items():
        # Number of pole-or-zero units at this corner
        n_units = abs(total_slope) // 20
        if n_units == 0:
            continue
        phase_delta = phase_at.get(w, -90 * n_units * (1 if total_slope < 0 else -1))
        kind, side = _factor_kind(total_slope // n_units, phase_delta // n_units)
        loc = (+w if side == "RHP" else -w)
        target = poles if kind == "pole" else zeros
        target.extend([loc] * n_units)

    # Build polynomials in s
    s = control.tf("s")
    num = control.tf([1], [1])
    for z in zeros:
        num = num * (s - z)
    den = control.tf([1], [1])
    for p in poles:
        den = den * (s - p)
    G_unscaled = num / den

    # Set static gain so |G(0)| matches dc_gain_dB
    dc_target = 10 ** (dc_gain_dB / 20)
    dc_now = abs(float(np.real(control.dcgain(G_unscaled))))
    if dc_now == 0 or not math.isfinite(dc_now):
        gain = dc_target
    else:
        gain = dc_target / dc_now
    G = control.tf([gain], [1]) * G_unscaled

    # Plot Bode for visual comparison
    fig, _ = plt.subplots(2, 1, figsize=(6, 4))
    try:
        control.bode_plot(G, dB=True, deg=True, plot=True)
    except TypeError:
        # Newer python-control API may not accept `plot` kwarg
        try:
            control.bode_plot(G, dB=True, deg=True)
        except TypeError:
            control.bode(G)
    fig.tight_layout()
    return G, fig
