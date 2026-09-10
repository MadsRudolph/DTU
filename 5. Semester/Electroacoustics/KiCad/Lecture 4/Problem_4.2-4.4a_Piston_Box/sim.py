#!/usr/bin/env python3
"""Problem 4.2 / 4.4a: run both analogy blocks, show they agree, and compare
with the closed form Z_M,tot = jwM_mp + S^2(Z_Af + jwM_Ad + 1/(jwC_AB))."""
import sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
from ngspice_ac import run_ac
OPTS = [".options abstol=1e-14 vntol=1e-12"]

rho, c = 1.18, 344.0
S = 100e-4
a = np.sqrt(S / np.pi)
MMP = 20e-3
V, D = 40e-3, 0.02
MA1 = 8 * rho / (3 * np.pi**2 * a)
RA1 = 0.441 * rho * c / S
RA2 = rho * c / S
CA1 = 5.94 * a**3 / (rho * c**2)
MAD = rho * D / S
CAB = V / (rho * c**2)
RS = 1e-6

f, v = run_ac(HERE / "Problem_4.2-4.4a_Piston_Box.kicad_sch",
              ["v(/u)", "i(v2)", "v(/p)", "v(/pi)"], extra_lines=OPTS)
w = 2 * np.pi * f
u_mob = v["v(/u)"]
u_imp = -v["i(v2)"]        # loop current; wrdata precision kills (fa-fb)/RS
print(f"analogy agreement: max rel diff |u_mob - u_imp|/|u| = {abs((u_mob - u_imp) / u_mob).max():.2e}")

par = lambda *z: 1 / sum(1 / zi for zi in z)
Zrad = par(1j * w * MA1, RA2 + par(RA1, 1 / (1j * w * CA1)))
Zm = 1j * w * MMP + S**2 * (Zrad + 1j * w * MAD + 1 / (1j * w * CAB))
u_th = 1 / Zm                                    # f = 1 N
print(f"vs closed form (4.2d): max rel diff = {abs((u_mob - u_th) / u_th).max():.2e}")

f0 = 1 / (2 * np.pi * np.sqrt((MMP + S**2 * (MA1 + MAD)) * CAB / S**2))
i0 = np.argmax(abs(u_mob))
print(f"resonance: sim {f[i0]:.1f} Hz, |u| = {abs(u_mob[i0]):.1f} m/s per N "
      f"(hand: f0 = {f0:.1f} Hz; only radiation damping -> very high Q)")

fig, ax = plt.subplots(1, 2, figsize=(11, 4.6))
ax[0].loglog(f, abs(u_mob), "C0", lw=2.5, label="mobility block: V(u)")
ax[0].loglog(f, abs(u_imp), "C3--", lw=1.2, label="impedance block: loop current")
ax[0].loglog(f, abs(u_th), "k:", lw=1, label="closed form $1/Z_{M,tot}$")
ax[0].axvline(f0, color="gray", ls=":", lw=1)
ax[0].text(f0 * 1.15, abs(u_mob).min() * 2, f"$f_0$ = {f0:.1f} Hz", fontsize=8)
ax[0].set_xlabel("Frequency [Hz]"); ax[0].set_ylabel("|u| [m/s] for f = 1 N")
ax[0].set_title("4.4a — both analogies give the same velocity")
ax[1].loglog(f, abs(1 / u_mob), "C0", lw=2, label="$|Z_{M,tot}| = f/u$ (ngspice)")
ax[1].loglog(f, 2 * np.pi * f * (MMP + S**2 * (MA1 + MAD)), "C2:", label="mass asymptote $\\omega M_{tot}$")
ax[1].loglog(f, S**2 / (2 * np.pi * f * CAB), "C1:", label="box-stiffness asymptote")
ax[1].set_xlabel("Frequency [Hz]"); ax[1].set_ylabel("$|Z_M|$ [Ns/m]")
ax[1].set_title("4.2b/d — total mechanical impedance")
for axx in ax:
    axx.grid(True, which="both", alpha=.3); axx.legend(fontsize=8)
fig.suptitle("Problem 4.2 / 4.4a — piston (20 g, 100 cm²), 2 cm baffle tube, 40 l box")
fig.tight_layout()
for outdir in (HERE, Path("/home/mads/DTU/Obsidian/Courses/34870 Electroacoustics/Images/Lecture4")):
    fig.savefig(outdir / "Problem_4.2_PistonBox.png", dpi=150)
print("saved")
