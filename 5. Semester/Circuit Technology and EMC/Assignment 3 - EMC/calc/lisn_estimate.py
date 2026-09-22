#!/usr/bin/env python3
"""Pen-and-paper estimate of the conducted emission of the TPS40200EVM-001 at the LISN.

Model (as simple as it can be, per Arnold's hint):

  1. The buck draws its input current in trapezoidal pulses: I_out for D*T, zero otherwise
     (the inductor ripple is ignored, the MOSFET edges are t_r long).
  2. Fourier series of that pulse train -> harmonic currents I_n at n*f_s.
  3. Each I_n splits between the on-board input capacitors (C1 100 uF OS-CON with its ESR,
     C2 1 uF ceramic) and the LISN. The LISN is the CISPR 16 50 ohm / 50 uH V-network,
     one per line, and the differential loop goes through both lines in series.
  4. The receiver reads the voltage on the 50 ohm port of ONE line -> dBuV, RMS of the tone.

    python3 lisn_estimate.py            # table + plot (results/lisn_estimate.png)
    python3 lisn_estimate.py --esr 0.03 # try the OS-CON datasheet ESR instead of the BOM's 0.3 ohm
"""
import argparse, math, pathlib
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "results"

# ---------------- operating point (assignment) --------------------------------------
VIN, VOUT, RLOAD, FS = 12.0, 3.3, 1.65, 300e3
IOUT = VOUT / RLOAD                              # 2.0 A
VF_D2, RDS_Q2, R_SENSE, R_L1 = 0.40, 0.075, 0.020, 0.039   # MBRS330, FDC654P, R2, L1 (BOM)
D = (VOUT + VF_D2 + IOUT * R_L1) / (VIN - IOUT * (RDS_Q2 + R_SENSE))   # duty incl. the drops ~0.32
T = 1 / FS
T_R = 30e-9                                     # MOSFET edge time (guess, sets the roll-off above ~10 MHz)

# ---------------- on-board input capacitors (EVM BOM) ------------------------------
C1, ESL1 = 100e-6, 5e-9                         # Sanyo 20SVP100M, 8x10 mm can
C2, ESR2, ESL2 = 0.6e-6, 0.010, 0.6e-9          # 1 uF 0603 X7R at 12 V bias ~ 0.6 uF

# ---------------- LISN, CISPR 16-1-2 50 ohm / 50 uH, per line ----------------------
L_LISN, C_LISN, R_MEAS = 50e-6, 0.1e-6, 50.0


def z_series_rlc(f, r, l, c):
    w = 2 * math.pi * f
    return r + 1j * w * l + 1 / (1j * w * c)


def z_lisn_line(f):
    """impedance the DUT sees looking into one LISN line (supply side is an AC short)"""
    w = 2 * math.pi * f
    z_l = 1j * w * L_LISN
    z_meas = R_MEAS + 1 / (1j * w * C_LISN)
    return z_l * z_meas / (z_l + z_meas)


def harmonic_current(n):
    """peak amplitude of the n-th harmonic of a trapezoidal pulse train, height IOUT, width D*T"""
    a = 2 * IOUT * abs(math.sin(n * math.pi * D)) / (n * math.pi)
    x = n * math.pi * T_R / T                    # edge roll-off, sin(x)/x
    return a * (abs(math.sin(x) / x) if x else 1.0)


def lisn_dbuv(n, esr1):
    f = n * FS
    z_c1 = z_series_rlc(f, esr1, ESL1, C1)
    z_c2 = z_series_rlc(f, ESR2, ESL2, C2)
    z_cap = z_c1 * z_c2 / (z_c1 + z_c2)
    z_dm = 2 * z_lisn_line(f)                    # out on one line, back on the other
    i_n = harmonic_current(n)
    i_lisn = i_n * abs(z_cap / (z_cap + z_dm))   # current divider
    # that current flows through the 50 uH || (0.1 uF + 50 ohm) of one line; the receiver sees the 50 ohm
    w = 2 * math.pi * f
    z_meas = R_MEAS + 1 / (1j * w * C_LISN)
    v_line = i_lisn * abs(z_lisn_line(f))
    v_meas = v_line * abs(R_MEAS / z_meas)
    return 20 * math.log10(v_meas / math.sqrt(2) / 1e-6), i_n, abs(z_cap), abs(z_dm)


def en55022_class_b(f, which="qp"):
    """EN 55022 / CISPR 22 class B conducted limit at the mains port, dBuV"""
    if f < 150e3 or f > 30e6:
        return float("nan")
    hi, lo = (66, 56) if which == "qp" else (56, 46)
    if f <= 500e3:                               # linear in log(f) from 66 (56) at 150 kHz to 56 (46) at 500 kHz
        return hi - (hi - lo) * math.log10(f / 150e3) / math.log10(500e3 / 150e3)
    if f <= 5e6:
        return lo
    return lo + 4                                # 60 (50) from 5 MHz to 30 MHz


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--esr", type=float, default=0.3, help="ESR of C1 in ohm (BOM says 0.3, OS-CON datasheet ~0.03)")
    ap.add_argument("--no-plot", action="store_true")
    a = ap.parse_args()

    print(f"D = {D:.3f}  (V_out + V_F + I R_L) / (V_in - I (R_DS + R_sense)),  I_out = {IOUT:.2f} A,  t_r = {T_R*1e9:.0f} ns")
    print(f"C1 ESR = {a.esr} ohm\n")
    rows = list(range(1, 9)) + list(range(95, 101))
    print(f"{'n':>3} {'f / MHz':>8} {'I_n / A':>8} {'|Z_cap|':>8} {'|Z_LISN,DM|':>11} {'V / dBuV':>9} {'QP limit':>9} {'margin':>7}")
    tab = []
    for n in rows:
        v, i_n, zc, zl = lisn_dbuv(n, a.esr)
        lim = en55022_class_b(n * FS)
        tab.append((n, n * FS, i_n, v, lim))
        print(f"{n:3d} {n*FS/1e6:8.2f} {i_n:8.3f} {zc:8.3f} {zl:11.1f} {v:9.1f} {lim:9.1f} {lim - v:+7.1f}")

    OUT.mkdir(exist_ok=True)
    np.savetxt(OUT / f"lisn_estimate_esr{a.esr:g}.csv", np.array([(n, f, i, v, l) for n, f, i, v, l in tab]),
               delimiter=",", header="n,f_Hz,I_n_peak_A,V_lisn_dBuV,EN55022B_QP_dBuV", comments="", fmt="%g")
    if a.no_plot:
        return
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ns = np.arange(1, 101)
    f = ns * FS
    v = np.array([lisn_dbuv(n, a.esr)[0] for n in ns])
    fl = np.logspace(math.log10(150e3), math.log10(30e6), 400)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(fl / 1e6, [en55022_class_b(x) for x in fl], "r-", lw=1.6, label="EN 55022 class B, quasi-peak")
    ax.plot(fl / 1e6, [en55022_class_b(x, "av") for x in fl], "r--", lw=1.2, label="EN 55022 class B, average")
    ax.stem(f / 1e6, v, linefmt="C0-", markerfmt="C0o", basefmt=" ", label=f"estimate, C1 ESR = {a.esr:g} Ω")
    ax.set_xscale("log"); ax.set_xlim(0.15, 30); ax.set_ylim(0, 120)
    ax.set_xlabel("f / MHz"); ax.set_ylabel("V at LISN 50 Ω port / dBµV")
    ax.set_title("TPS40200EVM-001 without filter: hand estimate of the conducted emission")
    ax.grid(True, which="both", alpha=.3); ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout(); fig.savefig(OUT / f"lisn_estimate_esr{a.esr:g}.png", dpi=150)
    print(f"\nplot: {OUT / f'lisn_estimate_esr{a.esr:g}.png'}")


if __name__ == "__main__":
    main()
