#!/usr/bin/env python3
"""Run Problem 4.4b in ngspice and plot Z_E and the coil velocity."""
import sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
from ngspice_ac import run_ac

f, v = run_ac(HERE / "Problem_4.4b_Coil_Electromechanical.kicad_sch", ["v(/vin)", "i(v1)", "v(/u)"])
Ze = -v["v(/vin)"] / v["i(v1)"]          # ngspice: i(v1) flows INTO the + terminal
u = v["v(/u)"]
# analytic check
Bl, Mmc, Cms, Rms, Re, Le = 2.1, 10e-3, 1e-3, 2.0, 5.0, 0.3e-3
w = 2*np.pi*f
Zm = 1j*w*Mmc + Rms + 1/(1j*w*Cms)
Ze_th = Re + 1j*w*Le + Bl**2/Zm
lo = f < 1000
i0 = np.argmax(abs(Ze[lo]))
print(f"motional peak |Z_E| = {abs(Ze[lo][i0]):.3f} ohm at {f[lo][i0]:.1f} Hz  (theory Re + Bl^2/Rms = {Re + Bl**2/Rms:.3f} ohm at {1/(2*np.pi*np.sqrt(Mmc*Cms)):.1f} Hz)")
print(f"phase of Z_E at motional peak = {np.degrees(np.angle(Ze[lo][i0])):.1f} deg")
print(f"|Z_E| at 1 Hz = {abs(Ze[0]):.3f}, at 10 kHz = {abs(Ze[-1]):.3f} ohm; max rel. error vs theory = {abs(abs(Ze)-abs(Ze_th)).max()/abs(Ze_th).max():.2e}")
iu = np.argmax(abs(u)); print(f"peak |u| = {abs(u[iu])*1e3:.3f} mm/s at {f[iu]:.1f} Hz (for 1 V drive)")

fig, ax = plt.subplots(2, 1, figsize=(7, 6.5), sharex=True)
ax[0].semilogx(f, abs(Ze), label="ngspice  |Z_E|"); ax[0].semilogx(f, abs(Ze_th), "--", label="analytic  R_e + jωL_e + (Bl)²/Z_M")
ax[0].semilogx(f, abs(Re + 1j*w*Le), ":", color="gray", label="blocked coil  R_e + jωL_e")
ax[0].set_ylabel("|Z_E|  [Ω]"); ax[0].legend(); ax[0].grid(True, which="both", alpha=.3)
ax[0].set_title("Problem 4.4b — electrical input impedance of the coil (Bl = 2.1 Tm)")
ax[1].semilogx(f, abs(u)*1e3); ax[1].set_ylabel("|u_coil|  [mm/s]  (1 V drive)"); ax[1].set_xlabel("Frequency [Hz]")
ax[1].grid(True, which="both", alpha=.3)
fig.tight_layout()
for outdir in (HERE, Path("/home/mads/DTU/Obsidian/Courses/34870 Electroacoustics/Images/Lecture4")):
    outdir.mkdir(parents=True, exist_ok=True)
    fig.savefig(outdir / "Problem_4.4b_Ze.png", dpi=150)
print("saved")
