#!/usr/bin/env python3
"""Run the extended dynamic microphone (Problems 4, 2c+2d) in ngspice and
compare with the 2a baseline and the analytic back-network model."""
import sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
from ngspice_ac import run_ac

rho, c = 1.18, 344.0
MMD, RMS, CMS = 0.2e-3, 1.0, 0.21e-3
a = 0.0254 / 2; SD = np.pi * a**2
Bl, RE, RL = 20.0, 200.0, 47e3
MA1 = 8 * rho / (3 * np.pi**2 * a)
RAF = 2e7
V1V, MAt, RAt = 0.1e-6, 300.0, 3e7
MAv, RAv = 10000.0, 1.5e7
CA1 = V1V / (rho * c**2)
CA2 = (5e-6 - V1V) / (rho * c**2)
CAB = 5e-6 / (rho * c**2)

f, v = run_ac(HERE / "Problem_4.2bcd_Mic_Extensions.kicad_sch", ["v(/out)"])
e = v["v(/out)"]
dB = 20 * np.log10(abs(e))

w = 2 * np.pi * f
Zm = 1j * w * MMD + RMS + 1 / (1j * w * CMS)
Zel = Bl**2 / (RE + RL)
par = lambda *z: 1 / sum(1 / zi for zi in z)
def vout(Zab):
    u = SD / (Zm + Zel + SD**2 * (1j * w * MA1 + Zab))
    return RL * Bl * u / (RE + RL)
ana = vout(RAF + par(1 / (1j * w * CA1), RAt + 1j * w * MAt + par(1 / (1j * w * CA2), 1j * w * MAv + RAv)))
base = vout(RAF + 1 / (1j * w * CAB))
print(f"max |dB diff| ngspice vs analytic = {abs(dB - 20*np.log10(abs(ana))).max():.2e} dB")

mask = (f >= 100) & (f <= 10e3)
print(f"midband {dB[mask].mean():.1f} dB re 1 V/Pa ({10**(dB[mask].mean()/20)*1e3:.2f} mV/Pa), "
      f"ripple 100 Hz - 10 kHz: {dB[mask].max() - dB[mask].min():.2f} dB")

fig, ax = plt.subplots(figsize=(7, 5))
ax.semilogx(f, 20 * np.log10(abs(base)), "k:", label="2a baseline (V = 5 cm³, R_AF = 2e7)")
ax.semilogx(f, dB, "C0", lw=2, label="2c+2d extended (ngspice)")
ax.semilogx(f, 20 * np.log10(abs(ana)), "C3--", lw=1, label="analytic back-network model")
ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("Sensitivity [dB re 1 V/Pa]")
ax.set_title("Problems 4 / 2c+2d — split cavity + damped tube + vented large cavity")
ax.grid(True, which="both", alpha=.3); ax.legend(fontsize=8)
ax.set_xlim(20, 40e3); ax.set_ylim(-85, -45)
fig.tight_layout()
for outdir in (HERE, Path("/home/mads/DTU/Obsidian/Courses/34870 Electroacoustics/Images/Lecture4")):
    fig.savefig(outdir / "Problem_4.2cd_extended_response.png", dpi=150)
print("saved")
