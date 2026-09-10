#!/usr/bin/env python3
"""Problem 4.1 c+d: acoustic impedance seen by the piston, and the far field
of the bass-reflex box as a point source."""
import sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
from ngspice_ac import run_ac

rho, c = 1.18, 344.0
a = 0.05
S = np.pi * a**2
V, LV = 23e-3, 0.12
MA1 = 8 * rho / (3 * np.pi**2 * a)
RA1 = 0.441 * rho * c / S
RA2 = rho * c / S
CA1 = 5.94 * a**3 / (rho * c**2)
MAV = rho * LV / S
CA = V / (rho * c**2)

f, v = run_ac(HERE / "Problem_4.1_BassReflex_Box.kicad_sch", ["v(/p)", "v(/pbox)", "v(/pv)"])
w = 2 * np.pi * f
U = S                                     # u = 1 m/s -> U_D = S_D
Za = v["v(/p)"] / U                       # total, seen by the piston
Zaf = (v["v(/p)"] - v["v(/pbox)"]) / U    # front radiation share
Zab = v["v(/pbox)"] / U                   # back (box + vent) share

# analytic cross-check (same lumped networks)
par = lambda *z: 1 / sum(1 / zi for zi in z)
Zrad = par(1j * w * MA1, RA2 + par(RA1, 1 / (1j * w * CA1)))
Za_th = Zrad + par(1 / (1j * w * CA), 1j * w * MAV + Zrad)
print(f"max rel diff sim vs analytic Z_A: {abs((Za - Za_th) / Za_th).max():.2e}")

iB = np.argmax(abs(Zab))
fB = 1 / (2 * np.pi * np.sqrt((MAV + MA1) * CA))
print(f"back-impedance peak (box-port antiresonance): sim {f[iB]:.1f} Hz "
      f"(theory with vent radiation mass {fB:.1f} Hz; 92.4 Hz without)")

# d) far field: U_tot = U_D - U_vent(chain sign); box small -> point source, free space
Uv = (v["v(/pbox)"] - v["v(/pv)"]) / (1j * w * MAV)
Utot = U - Uv
i0 = np.argmin(abs(Utot))
print(f"|U_tot| minimum at {f[i0]:.1f} Hz (vent and piston cancel below/at tuning)")
p1 = w * rho * abs(Utot) / (4 * np.pi * 1.0)          # |p| at r = 1 m
p1_nobox = w * rho * U / (4 * np.pi * 1.0)            # piston alone (monopole U_D)

fig, ax = plt.subplots(1, 3, figsize=(13, 4.4))
ax[0].loglog(f, abs(Za), "C0", lw=2, label="$Z_A$ total (ngspice)")
ax[0].loglog(f, abs(Zab), "C1--", label="back: box + vent")
ax[0].loglog(f, abs(Zaf), "C2:", label="front radiation")
ax[0].axvline(fB, color="gray", ls=":", lw=1)
ax[0].text(fB * 1.1, abs(Za).min() * 2, f"$f_B$ = {fB:.0f} Hz", fontsize=8)
ax[0].set_xlabel("Frequency [Hz]"); ax[0].set_ylabel(r"$|Z_A|$ [Pa·s/m³]")
ax[0].set_title("c) acoustic impedance seen by the piston")
ax[1].semilogx(f, 20 * np.log10(p1), "C0", lw=2, label="box: $U_D + U_v$")
ax[1].semilogx(f, 20 * np.log10(p1_nobox), "k:", label="piston alone ($U_D$)")
ax[1].set_xlabel("Frequency [Hz]"); ax[1].set_ylabel("|p(1 m)| [dB re 1 Pa] (u = 1 m/s)")
ax[1].set_title("d) far-field pressure at 1 m")
r = np.logspace(np.log10(0.5), np.log10(20), 100)
for fq, col in ((100.0, "C0"), (1000.0, "C3")):
    i = np.argmin(abs(f - fq))
    ax[2].loglog(r, w[i] * rho * abs(Utot[i]) / (4 * np.pi * r), col, label=f"{fq:.0f} Hz")
ax[2].set_xlabel("Distance r [m]"); ax[2].set_ylabel("|p| [Pa]")
ax[2].set_title("d) pressure over distance: $\\propto 1/r$ (−6 dB per doubling)")
for axx in ax:
    axx.grid(True, which="both", alpha=.3); axx.legend(fontsize=8)
fig.suptitle("Problem 4.1 — bass reflex box (massless piston, u = 1 m/s)")
fig.tight_layout()
for outdir in (HERE, Path("/home/mads/DTU/Obsidian/Courses/34870 Electroacoustics/Images/Lecture4")):
    fig.savefig(outdir / "Problem_4.1_BassReflex.png", dpi=150)
print("saved")
