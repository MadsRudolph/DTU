#!/usr/bin/env python3
"""Problems 4, 2b-d - experiment with the dynamic microphone's back network.

Analytic three-domain model (same equations the Problem_4B circuit solves,
verified there against ngspice to 0.001 dB):

    u     = S_D p_i / (Z_m + Bl^2/(R_E+R_L) + S_D^2 (jw M_A1 + Z_ab))
    V_out = R_L Bl u / (R_E + R_L)

with Z_m = jw M_MD + R_MS + 1/(jw C_MS) and Z_ab the back acoustic network:
    2a) R_AF + 1/(jw C_AB)                                       (single cavity)
    2c) (1/jwC_A1) || (R_AF + jw M_At + 1/(jw C_A2))             (cavity-tube-cavity)
    2d) ... with the large cavity vented: C_A2 -> C_A2 || (jw M_Av + R_Av)
"""
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
rho, c = 1.18, 344.0
MMD, RMS, CMS = 0.2e-3, 1.0, 0.21e-3
a = 0.0254 / 2; SD = np.pi * a**2
Bl, RE, RL = 20.0, 200.0, 47e3
MA1 = 8 * rho / (3 * np.pi**2 * a)
CA = lambda V: V / (rho * c**2)

f = np.logspace(np.log10(20), np.log10(40e3), 800)
w = 2 * np.pi * f
Zm = 1j * w * MMD + RMS + 1 / (1j * w * CMS)
Zel = Bl**2 / (RE + RL)

def vout(Zab):
    u = SD / (Zm + Zel + SD**2 * (1j * w * MA1 + Zab))
    return RL * Bl * u / (RE + RL)

def db(x): return 20 * np.log10(abs(x))
def band(e):
    dB = db(e); i0 = np.argmax(dB)
    m = dB >= dB[i0] - 3
    return f[m][0], f[m][-1], abs(e[i0]), f[i0]

par = lambda *z: 1 / sum(1 / zi for zi in z)

# ---------- b) sensitivity via R_AF ----------
CAB = CA(5e-6)
fig, ax = plt.subplots(2, 2, figsize=(11, 8), sharex=True, sharey=True)
for RAF, lab in ((2e7, "R_AF = 2e7 (2a baseline)"), (1.27e8, "R_AF = 1.27e8"), (9.2e6, "R_AF = 9.2e6")):
    e = vout(RAF + 1 / (1j * w * CAB))
    fa, fb, M, f0 = band(e)
    ax[0, 0].semilogx(f, db(e), label=f"{lab}: {M*1e3:.2f} mV/Pa, {fa:.0f} Hz-{fb/1e3:.1f} kHz")
    print(f"b) {lab}: M = {M*1e3:.3f} mV/Pa at {f0:.0f} Hz, band {fa:.0f} - {fb:.0f} Hz")
ax[0, 0].set_title("b) sensitivity vs $R_{AF}$ (single 5 cm³ cavity)")

# ---------- c) cavity-tube-cavity ----------
# R_AF (felt) stays directly behind the diaphragm, THEN the split:
#   pb -> R_AF -> ps{C_A1 small} -> (M_At + R_At tube) -> pc{C_A2 large}
# HF extension = second resonance of M_MT with the small cavity's stiffness,
# damped by R_AF; the tube keeps both cavities in play at low frequency.
base = vout(2e7 + 1 / (1j * w * CAB))
ax[0, 1].semilogx(f, db(base), "k:", label="2a baseline")
for V1, MAt, RAt in ((0.1e-6, 300.0, 3e7), (0.2e-6, 300.0, 3e7), (0.1e-6, 600.0, 5e6), (0.1e-6, 200.0, 5e7)):
    CA1, CA2 = CA(V1), CA(5e-6 - V1)
    Zab = 2e7 + par(1 / (1j * w * CA1), RAt + 1j * w * MAt + 1 / (1j * w * CA2))
    e = vout(Zab)
    fa, fb, M, _ = band(e)
    ax[0, 1].semilogx(f, db(e), label=f"V1={V1*1e6:.1f} cm³, M_At={MAt:.0f}, R_At={RAt:.0e}: {fa:.0f} Hz-{fb/1e3:.1f} kHz")
    print(f"c) V1={V1*1e6:.1f} MAt={MAt:.0f} RAt={RAt:.0e}: band {fa:.0f} - {fb:.0f} Hz, M={M*1e3:.2f} mV/Pa")
ax[0, 1].set_title("c) R_AF + [C_A1 || (tube + C_A2)], V1 + V2 = 5 cm³")

# ---------- d) vent tube in the large cavity ----------
V1, MAt, RAt = 0.1e-6, 300.0, 3e7
CA1, CA2 = CA(V1), CA(5e-6 - V1)
Zc = 2e7 + par(1 / (1j * w * CA1), RAt + 1j * w * MAt + 1 / (1j * w * CA2))
ax[1, 0].semilogx(f, db(vout(Zc)), "k:", label="c) unvented")
for MAv, RAv in ((10000.0, 1.5e7), (10000.0, 5e6), (23000.0, 1.5e7)):
    fH = 1 / (2 * np.pi * np.sqrt(MAv * CA2))
    Zab = 2e7 + par(1 / (1j * w * CA1), RAt + 1j * w * MAt + par(1 / (1j * w * CA2), 1j * w * MAv + RAv))
    e = vout(Zab)
    fa, fb, M, _ = band(e)
    ax[1, 0].semilogx(f, db(e), label=f"M_Av={MAv:.0f} (f_H={fH:.0f} Hz), R_Av={RAv:.0e}: {fa:.0f} Hz-{fb/1e3:.1f} kHz")
    print(f"d) MAv={MAv:.0f} RAv={RAv:.0e}: f_H={fH:.0f} Hz, band {fa:.0f} - {fb:.0f} Hz")
ax[1, 0].set_title("d) + vent in the large cavity (Helmholtz LF boost)")

# ---------- final pick: c) + d) combined vs baseline ----------
MAv, RAv = 10000.0, 1.5e7
Zab_fin = 2e7 + par(1 / (1j * w * CA1), RAt + 1j * w * MAt + par(1 / (1j * w * CA2), 1j * w * MAv + RAv))
e = vout(Zab_fin)
fa0, fb0, M0, _ = band(base); fa1, fb1, M1, _ = band(e)
ax[1, 1].semilogx(f, db(base), "k:", label=f"2a baseline: {fa0:.0f} Hz - {fb0/1e3:.1f} kHz")
ax[1, 1].semilogx(f, db(e), "C0", lw=2, label=f"extended (c+d): {fa1:.0f} Hz - {fb1/1e3:.1f} kHz")
ax[1, 1].set_title("final: extended design vs baseline")
print(f"final: V1={V1*1e6:.1f} cm³, M_At={MAt:.0f}, R_At={RAt:.0e}, M_Av={MAv:.0f}, R_Av={RAv:.0e}")
print(f"final: band {fa0:.0f}-{fb0:.0f} -> {fa1:.0f}-{fb1:.0f} Hz, M {M0*1e3:.2f} -> {M1*1e3:.2f} mV/Pa")

for axx in ax.flat:
    axx.grid(True, which="both", alpha=.3); axx.legend(fontsize=7)
    axx.set_ylim(-85, -45)
for axx in ax[1]: axx.set_xlabel("Frequency [Hz]")
for axx in ax[:, 0]: axx.set_ylabel("Sensitivity [dB re 1 V/Pa]")
fig.suptitle("Problems 4 / 2b-d — dynamic microphone back-network experiments")
fig.tight_layout()
fig.savefig(HERE / "Problem_4.2bcd_experiments.png", dpi=150)
print("saved")
