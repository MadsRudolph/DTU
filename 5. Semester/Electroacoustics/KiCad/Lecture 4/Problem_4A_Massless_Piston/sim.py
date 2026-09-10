#!/usr/bin/env python3
"""Run the massless-piston circuit (Lecture 4A slide 9) and reproduce its plot:
|Z_M| total, only front radiation, only back cavity - plus the analytic lumped
network and the exact baffled-piston impedance (Bessel/Struve) as cross-checks."""
import sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
from ngspice_ac import run_ac

rho, c = 1.18, 344.0
a = 0.10
S = np.pi * a**2
V = 10e-3
MA1 = 8 * rho / (3 * np.pi**2 * a)
RA1 = 0.441 * rho * c / S
RA2 = rho * c / S
CA1 = 5.94 * a**3 / (rho * c**2)
CAB = V / (rho * c**2)

f, v = run_ac(HERE / "Problem_4A_Massless_Piston.kicad_sch", ["v(/p)", "v(/pm)"])
# u = 1 m/s, f = S*p  ->  Z_M = S*V(p); the series split gives the two shares
Zm = S * v["v(/p)"]
Zm_front = S * (v["v(/p)"] - v["v(/pm)"])
Zm_back = S * v["v(/pm)"]

# analytic lumped network
w = 2 * np.pi * f
Zaf = 1 / (1 / (1j * w * MA1) + 1 / (RA2 + 1 / (1 / RA1 + 1j * w * CA1)))
Zab = 1 / (1j * w * CAB)
Zm_th = S**2 * (Zaf + Zab)
print(f"max rel diff sim vs lumped analytic: {abs((Zm - Zm_th) / Zm_th).max():.2e}")

# exact baffled piston: Z_Af = (rho c / S) [1 - J1(2ka)/(ka) + j H1(2ka)/(ka)]
from scipy.special import j1, struve
ka = w / c * a
Zaf_ex = rho * c / S * (1 - j1(2 * ka) / ka + 1j * struve(1, 2 * ka) / ka)
Zm_ex = S**2 * (Zaf_ex + Zab)

f0 = 1 / (2 * np.pi * np.sqrt(MA1 * CAB))
i0 = np.argmin(abs(Zm))
print(f"dip: sim {f[i0]:.0f} Hz, |Z_M| = {abs(Zm[i0]):.2f} Ns/m  (theory f0 = 1/2pi sqrt(M_A1 C_AB) = {f0:.0f} Hz)")
print(f"plateau: sim {abs(Zm[-1]):.2f} Ns/m  (theory S^2 R_A2 = S rho c = {S**2 * RA2:.2f} Ns/m)")

fig, ax = plt.subplots(figsize=(7, 5))
ax.loglog(f, abs(Zm), "C0", lw=2, label="Mech. impedance $Z_M$ (ngspice)")
ax.loglog(f, abs(Zm_front), "C1:", lw=2, label="only front radiation")
ax.loglog(f, abs(Zm_back), "C8--", lw=2, label="only back cavity")
ax.loglog(f, abs(Zm_ex), "k-.", lw=1, alpha=.6, label="exact (Bessel/Struve) + cavity")
ax.set_xlabel("Frequency $f$ / Hz"); ax.set_ylabel("Mech. Impedance $Z_M$ / Ns/m")
ax.set_title("Lecture 4A slide 9 — massless piston, a = 10 cm, V = 10 l")
ax.grid(True, which="both", alpha=.3); ax.legend()
ax.set_xlim(20, 20e3)
fig.tight_layout()
for outdir in (HERE, Path("/home/mads/DTU/Obsidian/Courses/34870 Electroacoustics/Images/Lecture4")):
    fig.savefig(outdir / "Problem_4A_MasslessPiston_Zm.png", dpi=150)
print("saved")
