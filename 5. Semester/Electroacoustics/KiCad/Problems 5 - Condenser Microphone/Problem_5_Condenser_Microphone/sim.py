#!/usr/bin/env python3
"""Run the condenser microphone (Problems 5, Q1/Q2a-c) in ngspice and check it
against two independent references: (1) a small linear system built directly
from this circuit's own node/loop equations (no hand-simplification), and
(2) Problem 5.1's simple hand-calc totals M_MT, R_MT, C_MT (valid in the
R_L' -> large limit)."""
import sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
from ngspice_ac import run_ac

rho, c = 1.18, 344.0
CMD, MMD, RMD = 4e-6, 0.050e-3, 1.0
a = 0.009
SD = np.pi * a**2
MA1 = 8 * rho / (3 * np.pi**2 * a)
MAS, RAS = 100.0, 1e7
VAB2 = 1e-6
CAB2 = VAB2 / (rho * c**2)
E, x0, RLp = 200.0, 20e-6, 500e6
eps0 = 8.85e-12
CE0 = eps0 * SD / x0

f, v = run_ac(HERE / "Problem_5_Condenser_Microphone.kicad_sch",
              ["v(/out)", "v(/u)", "v(/pf)", "v(/pb)", "v(/ce0)"])
e_sim = v["v(/out)"]
w = 2 * np.pi * f


def reference(w):
    """Solve the circuit's own 4 equations (u, pf, i, out) exactly, no
    hand-simplification -- this is what the schematic *should* compute."""
    jw = 1j * w
    Zmech_own = jw * MMD + 1 / (jw * CMD) + RMD
    Zback = RAS + jw * MAS + 1 / (jw * CAB2)
    # pf = p_i - jw*MA1*SD*u ; pb = SD*u*Zback ; (pf-pb) injected into u with gain SD
    # u*Zmech_own = SD*(pf-pb) - (E/(x0*jw))*i
    # i*(1/(jw*CE0) + RLp) = (E/(x0*jw))*u
    K_i = (E / (x0 * jw)) / (1 / (jw * CE0) + RLp)
    # u*Zmech_own = SD*(p_i - jw*MA1*SD*u - SD*u*Zback) - (E/(x0*jw))*K_i*u
    denom = Zmech_own + SD**2 * (jw * MA1 + Zback) + (E / (x0 * jw)) * K_i
    u = SD * 1.0 / denom
    i = K_i * u
    out = i * RLp
    return out


e_ref = reference(w)

# Problem 5.1's simple totals (R_L' -> large limit)
MMT = MMD + SD**2 * (MA1 + MAS)
RMT = RMD + SD**2 * RAS
CMT = 1 / (1 / CMD + SD**2 / CAB2)
Zmt = 1j * w * MMT + RMT + 1 / (1j * w * CMT)
e_hand = -(E * SD) / (x0 * 1j * w * Zmt)
f0 = 1 / (2 * np.pi * np.sqrt(MMT * CMT))
Q = (1 / RMT) * np.sqrt(MMT / CMT)
M = E * SD * CMT / x0

dB_sim = 20 * np.log10(np.abs(e_sim))
dB_ref = 20 * np.log10(np.abs(e_ref))
dB_hand = 20 * np.log10(np.abs(e_hand))

i0 = np.argmax(dB_sim)
print(f"sim:   f0={f[i0]:.0f} Hz, peak={20*np.log10(abs(e_sim[i0])*1e3):.2f} dB re 1 mV/Pa "
      f"({abs(e_sim[i0])*1e3:.3f} mV/Pa)")
print(f"ref (4-eq linear system):  max |dB diff vs sim| = {np.max(np.abs(dB_sim - dB_ref)):.3e} dB")
print(f"hand (Problem 5.1 totals): f0={f0:.1f} Hz, Q={Q:.3f}, M={M*1e3:.3f} mV/Pa "
      f"({20*np.log10(M):.2f} dB)")
print(f"hand vs sim: max |dB diff| in-band (100 Hz-30 kHz) = "
      f"{np.max(np.abs(dB_sim - dB_hand)[(f>100)&(f<30e3)]):.3f} dB")

fig, ax = plt.subplots(2, 1, figsize=(7, 6.5), sharex=True)
ax[0].semilogx(f, dB_sim, label="ngspice V(out)")
ax[0].semilogx(f, dB_ref, "--", label="4-equation linear-system check")
ax[0].semilogx(f, dB_hand, ":", label="Problem 5.1 totals ($M_{MT},R_{MT},C_{MT}$)")
ax[0].axhline(20 * np.log10(M), color="gray", ls=":", alpha=.6,
              label=f"M = {M*1e3:.2f} mV/Pa = {20*np.log10(M):.1f} dB")
ax[0].axvline(f0, color="gray", ls=":", alpha=.6, label=f"$f_0$ = {f0:.0f} Hz")
ax[0].set_ylabel("Sensitivity [dB re 1 V/Pa]")
ax[0].legend(fontsize=8)
ax[0].grid(True, which="both", alpha=.3)
ax[0].set_title("Problems 5 (Q1/2a-c) - condenser microphone equivalent circuit")
ax[1].semilogx(f, np.degrees(np.unwrap(np.angle(e_sim))))
ax[1].set_ylabel("Phase [deg]")
ax[1].set_xlabel("Frequency [Hz]")
ax[1].grid(True, which="both", alpha=.3)
fig.tight_layout()
for outdir in (HERE, Path("/home/mads/DTU/Obsidian/Courses/34870 Electroacoustics/Images/Lecture5")):
    outdir.mkdir(parents=True, exist_ok=True)
    fig.savefig(outdir / "Problem_5.1_CondenserMic_sensitivity.png", dpi=150)
print("saved")
