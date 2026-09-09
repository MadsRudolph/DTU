#!/usr/bin/env python3
"""Run the dynamic microphone (Problems 4, 2a) in ngspice and plot the sensitivity."""
import sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ngspice_ac import run_ac

f, v = run_ac(HERE / "Problem_4B_Dynamic_Microphone.kicad_sch", ["v(/out)", "v(/u)", "v(/pf)", "v(/pb)"])
e = v["v(/out)"]
dB = 20*np.log10(abs(e))
# analytic (Leach 5.27-style) check
rho, c = 1.18, 344.0
MMD, RMS, CMS = 0.2e-3, 1.0, 0.21e-3
a = 0.0254/2; SD = np.pi*a**2; Bl, RE, RL = 20.0, 200.0, 47e3; V, RAF = 5e-6, 2e7
MA1 = 8*rho/(3*np.pi**2*a); CAB = V/(rho*c**2)
MMT = MMD + SD**2*MA1; RMT = RMS + SD**2*RAF + Bl**2/(RE+RL); CMT = 1/(1/CMS + SD**2/CAB)
w = 2*np.pi*f
H = RL/(RE+RL) * Bl*SD / (1j*w*MMT + RMT + 1/(1j*w*CMT))
f0 = 1/(2*np.pi*np.sqrt(MMT*CMT)); Q = np.sqrt(MMT/CMT)/RMT; M = RL/(RE+RL)*Bl*SD/RMT
i0 = np.argmax(abs(e))
print(f"sim peak: {dB[i0]:.2f} dB re 1 V/Pa ({abs(e[i0])*1e3:.3f} mV/Pa) at {f[i0]:.0f} Hz")
print(f"theory: f0 = {f0:.0f} Hz, Q = {Q:.3f}, M = {M*1e3:.3f} mV/Pa = {20*np.log10(M):.2f} dB")
print(f"max |dB diff| sim vs analytic = {abs(dB - 20*np.log10(abs(H))).max():.2e} dB")
# -3 dB points
mask = dB >= dB[i0] - 3
fa, fb = f[mask][0], f[mask][-1]
print(f"-3 dB band: {fa:.0f} Hz .. {fb:.0f} Hz  (theory fa,fb = {f0*(np.sqrt(1+1/(4*Q*Q))-1/(2*Q)):.0f}, {f0*(np.sqrt(1+1/(4*Q*Q))+1/(2*Q)):.0f})")

fig, ax = plt.subplots(2, 1, figsize=(7, 6.5), sharex=True)
ax[0].semilogx(f, dB, label="ngspice V(out)/p_i")
ax[0].semilogx(f, 20*np.log10(abs(H)), "--", label="analytic band-pass (M_MT, R_MT, C_MT)")
ax[0].axhline(20*np.log10(M), color="gray", ls=":", label=f"M = {M*1e3:.2f} mV/Pa = {20*np.log10(M):.1f} dB")
ax[0].set_ylabel("Sensitivity [dB re 1 V/Pa]"); ax[0].legend(); ax[0].grid(True, which="both", alpha=.3)
ax[0].set_title("Problems 4 / 2a — dynamic microphone, V = 5 cm³, R_AF = 2e7 Ns/m⁵")
ax[1].semilogx(f, np.degrees(np.angle(e))); ax[1].set_ylabel("Phase [deg]"); ax[1].set_xlabel("Frequency [Hz]")
ax[1].grid(True, which="both", alpha=.3)
fig.tight_layout()
for outdir in (HERE, Path("/home/mads/DTU/Obsidian/Courses/34870 Electroacoustics/Images/Lecture4")):
    fig.savefig(outdir / "Problem_4B_DynamicMic_sensitivity.png", dpi=150)
print("saved")
