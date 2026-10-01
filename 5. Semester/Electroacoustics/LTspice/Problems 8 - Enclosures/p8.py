#!/usr/bin/env python3
"""34870 Problems 8 (Loudspeakers 2: enclosures): hand calculations for problems 1-2,
the slide-14 Scan-Speak design example, and the figures for the Lecture 8 note.

    python3 p8.py            # print every answer next to the sheet's bracket
    python3 p8.py --plots    # also write the figures into the vault Images/Lecture8/

Vented-box alignments come from the course's own lookup tables (Niels Iversen's
ventbox.m / QB3.m / cheby2.m in VentedBox_Matlab.zip, handed out with lecture 8),
parsed here so no MATLAB is needed. The sheet's brackets were read off Leach's graph
(Q_L = 5), so they differ from the tables by a few percent.

Circuit used for the figures (slides 6 and 19, impedance analogy, L_E ignored):
    u_D = (Bl e_g / R_E) / (Z_M + Bl^2/R_E + S_D^2 Z_A2),  Z_M = jw M_MS + R_MS + 1/(jw C_MS)
    closed box: Z_A2 = 1/(jw C_AB)          vented: Y_A2 = 1/(jw M_AP) + 1/R_AL + jw C_AB
    radiated volume velocity: closed U_D, vented U_0 = jw C_AB Z_A2 U_D
    far field p(1 m) = rho jw U / (2 pi)
"""
import math, pathlib, re, sys, zipfile
import numpy as np

RHO, C0, PREF = 1.2, 344.0, 20e-6
HERE = pathlib.Path(__file__).resolve().parent
VAULT = pathlib.Path.home() / "DTU/Obsidian/Courses/34870 Electroacoustics"
ZIP = VAULT / "_Learn/Lecture 8 - Loudspeaker enclosures/VentedBox_Matlab.zip"
IMG = VAULT / "Images/Lecture8"

WOOFERS = [("CSX 217C", 34.0, 0.47, 49.0), ("SWR 263", 27.8, 0.52, 88.0), ("SWR 308", 18.1, 0.20, 140.0)]
SHEET_1A = [(51.2, 38.8), (37.8, 104), (64, 12.2)]
SHEET_1B = [51.2, 40.5, 75.0]
SHEET_2A = [(31, 90), (22, 250), (40, 18)]
SHEET_2B = [10.4, 6.0, 42.2]

# Scan-Speak 22W/8857T00, slide 14
SS = dict(Re=6.2, Bl=10.1, Cms=1.29e-3, Mms=37e-3, Rms=1.1, Sd=220e-4)


# =====================================================================  closed box
def f3_closed(fc, Qtc):
    """-3 dB frequency of a 2nd-order high-pass (slide 9)."""
    x = 1 / (2 * Qtc ** 2) - 1
    return fc * math.sqrt(x + math.sqrt(x * x + 1))


def closed_opt(fs, Qts, Vas, Qtc=1 / math.sqrt(2)):
    a = (Qtc / Qts) ** 2 - 1
    fc = fs * math.sqrt(1 + a)
    return dict(alpha=a, Vab=Vas / a, fc=fc, Qtc=Qtc, f3=f3_closed(fc, Qtc))


def closed_vol(fs, Qts, Vas, Vab):
    a = Vas / Vab
    fc, Qtc = fs * math.sqrt(1 + a), Qts * math.sqrt(1 + a)
    return dict(alpha=a, Vab=Vab, fc=fc, Qtc=Qtc, f3=f3_closed(fc, Qtc))


# =====================================================================  vented box
def _tables():
    """Parse the four lookup tables (rows = Q_L 5..20) out of QB3.m and cheby2.m."""
    out = {}
    with zipfile.ZipFile(ZIP) as z:
        for name in ("QB3", "cheby2"):
            src = z.read(f"VentedBox_Matlab/{name}.m").decode()
            out[name] = {k: np.array([[float(v) for v in row.split()] for row in body.split(";") if row.strip()])
                         for k, body in re.findall(r"(\w+)_arr\s*=\s*\[(.*?)\]", src, re.S)}
    with zipfile.ZipFile(ZIP) as z:
        src = z.read("VentedBox_Matlab/ventbox.m").decode()
    out["split"] = np.array([float(v) for v in re.search(r"Qts_arr\s*=\s*\[(.*?)\]", src, re.S).group(1).replace(";", " ").split()])
    return out


_T = None


def ventbox(fs, Qts, Vas, QL):
    """Python port of ventbox.m: QB3 below the B4 Q_TS, Chebyshev above it."""
    global _T
    _T = _T or _tables()
    kind = "cheby2" if Qts > _T["split"][QL - 5] else "QB3"
    t = _T[kind]
    i = int(np.argmin(abs(t["Qts"][QL - 5] - Qts)))
    a, h, q = t["alpha"][QL - 5, i], t["h"][QL - 5, i], t["q"][QL - 5, i]
    return dict(kind="C4" if kind == "cheby2" else "QB3", alpha=a, h=h, q=q, Vab=Vas / a, fb=h * fs, fl=q * fs)


def vent_poly(f, fs, Qts, alpha, h, QL):
    """Normalised 4th-order high-pass of slide 20."""
    s = 1j * f / (math.sqrt(h) * fs)
    a1 = 1 / (QL * math.sqrt(h)) + math.sqrt(h) / Qts
    a2 = (alpha + 1) / h + h + 1 / (QL * Qts)
    a3 = 1 / (Qts * math.sqrt(h)) + math.sqrt(h) / QL
    return s ** 4 / (s ** 4 + a3 * s ** 3 + a2 * s ** 2 + a1 * s + 1)


def vent_length(fb, Vab_L, a):
    """Physical tube length for a vent of radius a (slide 28)."""
    Cab = Vab_L / 1e3 / (RHO * C0 ** 2)
    Map = 1 / ((2 * math.pi * fb) ** 2 * Cab)
    Sp = math.pi * a ** 2
    return Map * Sp / RHO - 1.46 * a


def first_below(f, HdB, level=-3.0):
    return f[int(np.argmax(HdB > level))]


# =====================================================================  full circuit
def ts(d):
    ws = 1 / math.sqrt(d["Mms"] * d["Cms"])
    Qms, Qes = ws * d["Mms"] / d["Rms"], d["Re"] * ws * d["Mms"] / d["Bl"] ** 2
    return dict(fs=ws / 2 / math.pi, Qms=Qms, Qes=Qes, Qts=Qms * Qes / (Qms + Qes),
                Vas=RHO * C0 ** 2 * d["Sd"] ** 2 * d["Cms"] * 1e3)


def driver(d, f, box=None, eg=2.83):
    """box: None (infinite baffle), ('closed', V_L) or ('vented', V_L, fb, QL).
    Returns far-field p(1 m) total / driver / vent, and Z_E."""
    w = 2 * np.pi * f
    s = 1j * w
    ZM = s * d["Mms"] + d["Rms"] + 1 / (s * d["Cms"])
    Sd = d["Sd"]
    if box is None:
        ZA2 = np.zeros_like(s)
    else:
        Cab = box[1] / 1e3 / (RHO * C0 ** 2)
        if box[0] == "closed":
            ZA2 = 1 / (s * Cab)
        else:
            Map = 1 / ((2 * np.pi * box[2]) ** 2 * Cab)
            Ral = box[3] * math.sqrt(Map / Cab)
            ZA2 = 1 / (1 / (s * Map) + 1 / Ral + s * Cab)
    u = d["Bl"] * eg / d["Re"] / (ZM + d["Bl"] ** 2 / d["Re"] + Sd ** 2 * ZA2)
    UD = Sd * u
    ZE = d["Re"] + d["Bl"] ** 2 / (ZM + Sd ** 2 * ZA2)
    k = RHO * s / (2 * np.pi)
    if box is not None and box[0] == "vented":
        Uvent = -UD * ZA2 / (s * Map)
        return dict(total=k * (UD + Uvent), driver=k * UD, vent=k * Uvent, ZE=ZE)
    return dict(total=k * UD, driver=k * UD, ZE=ZE)


def spl(p):
    return 20 * np.log10(abs(p) / PREF)          # e_g and p both rms


# =====================================================================  print
def main(plots):
    print("== Problem 1a: closed box, Q_TC = 1/sqrt2 (lowest f3)")
    for (n, fs, Q, V), (sf, sV) in zip(WOOFERS, SHEET_1A):
        r = closed_opt(fs, Q, V)
        print(f"  {n:9s} alpha={r['alpha']:.3f}  V_AB={r['Vab']:6.1f} L [{sV}]  f3=f_c={r['f3']:5.1f} Hz [{sf}]")
    print("== Problem 1b: 40 L box")
    for (n, fs, Q, V), sf in zip(WOOFERS, SHEET_1B):
        r = closed_vol(fs, Q, V, 40)
        print(f"  {n:9s} alpha={r['alpha']:.3f}  f_c={r['fc']:5.1f}  Q_TC={r['Qtc']:.3f}  f3={r['f3']:5.1f} Hz [{sf}]")
    f = np.logspace(0, 3, 30000)
    print("== Problem 2a: vented box, Q_L = 5 (course tables vs sheet)")
    for (n, fs, Q, V), (sfb, sV) in zip(WOOFERS, SHEET_2A):
        r = ventbox(fs, Q, V, 5)
        f3 = first_below(f, 20 * np.log10(abs(vent_poly(f, fs, Q, r["alpha"], r["h"], 5))))
        print(f"  {n:9s} {r['kind']:3s} alpha={r['alpha']:.3f} h={r['h']:.3f}  V_AB={r['Vab']:6.1f} L [{sV}]"
              f"  f_B={r['fb']:5.1f} Hz [{sfb}]  f3={r['fl']:5.1f} (poly {f3:5.1f}) Hz")
    print("== Problem 2b: vent length, a = 3.75 cm")
    for (n, *_), (sfb, sV), sL, (_, fs, Q, V) in zip(WOOFERS, SHEET_2A, SHEET_2B, WOOFERS):
        r = ventbox(fs, Q, V, 5)
        print(f"  {n:9s} sheet f_B/V: L={100 * vent_length(sfb, sV, 0.0375):5.1f} cm [{sL}]"
              f"   tables: L={100 * vent_length(r['fb'], r['Vab'], 0.0375):5.1f} cm")
    t = ts(SS)
    print("== Slide 14: Scan-Speak 22W/8857T00 (T-S from the raw parameters)")
    print("  fs={fs:.2f} Hz  Qms={Qms:.2f}  Qes={Qes:.3f}  Qts={Qts:.3f}  Vas={Vas:.1f} L".format(**t))
    c1 = closed_opt(t["fs"], t["Qts"], 88)
    c2 = closed_vol(t["fs"], t["Qts"], 88, 10)
    print(f"  case 1: alpha={c1['alpha']:.2f} V_AB={c1['Vab']:.1f} L f_c={c1['fc']:.1f} f3={c1['f3']:.1f} Hz  [4.3, 20.2 L, 53.2, 53.2]")
    print(f"  case 2: alpha={c2['alpha']:.2f} f_c={c2['fc']:.1f} Q_TC={c2['Qtc']:.2f} f3={c2['f3']:.1f} Hz  [8.8, 72.2, 0.96, 58.0]")
    v = ventbox(t["fs"], t["Qts"], 88, 7)
    print(f"  vented, Q_L = 7: {v['kind']} alpha={v['alpha']:.2f} V_AB={v['Vab']:.1f} L f_B={v['fb']:.1f} Hz f3={v['fl']:.1f} Hz")
    p1m = RHO / (2 * math.pi) * SS["Bl"] * SS["Sd"] / (SS["Re"] * SS["Mms"])
    eta = RHO / (2 * math.pi * C0) / SS["Re"] * (SS["Bl"] * SS["Sd"] / SS["Mms"]) ** 2
    print(f"  sensitivity {20 * math.log10(p1m * 2.83 / PREF):.1f} dB SPL @ 2.83 V rms, 1 m, eta={100 * eta:.2f} %")
    # efficiency check, slide 10: eta = 4 pi^2 fc^3 V_AT / (c^3 Q_EC)
    a = c1["alpha"]; Vat = 88e-3 * c1["Vab"] * 1e-3 / (88e-3 + c1["Vab"] * 1e-3)
    Qec = t["Qes"] * math.sqrt(1 + a)
    print(f"  slide 10 check (case 1): 4pi^2 fc^3 V_AT/(c^3 Q_EC) = {100 * 4 * math.pi ** 2 * c1['fc'] ** 3 * Vat / (C0 ** 3 * Qec):.2f} %")
    if plots:
        make_plots(t, c1, c2, v)


# =====================================================================  plots
def make_plots(t, c1, c2, v):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    IMG.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": .35})
    f = np.logspace(np.log10(5), np.log10(1000), 2000)
    cols = ["#b5651d", "#2f6690", "#2a9d8f"]

    # 1. Problem 1: three woofers, optimum box and 40 L
    fig, ax = plt.subplots(figsize=(8, 4.2))
    for (n, fs, Q, V), col in zip(WOOFERS, cols):
        for r, ls in ((closed_opt(fs, Q, V), "-"), (closed_vol(fs, Q, V, 40), "--")):
            s = 1j * f / r["fc"]
            H = s ** 2 / (s ** 2 + s / r["Qtc"] + 1)
            lab = f"{n}: {r['Vab']:.0f} L, $Q_{{TC}}$={r['Qtc']:.2f}, $f_3$={r['f3']:.1f} Hz"
            ax.semilogx(f, 20 * np.log10(abs(H)), ls, color=col, label=lab)
    ax.axhline(-3, color="k", lw=.8, ls=":")
    ax.set(xlim=(10, 500), ylim=(-24, 4), xlabel="Frequency [Hz]", ylabel="Relative response [dB]",
           title="Problem 1: closed box. Solid = optimum box ($Q_{TC}=1/\\sqrt{2}$), dashed = 40 L")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout(); fig.savefig(IMG / "P8_closed_box.png", dpi=150); plt.close(fig)

    # 2. Problem 2: vented designs (course tables, Q_L = 5) vs the optimum closed box
    fig, ax = plt.subplots(figsize=(8, 4.2))
    for (n, fs, Q, V), col in zip(WOOFERS, cols):
        r = ventbox(fs, Q, V, 5)
        H = vent_poly(f, fs, Q, r["alpha"], r["h"], 5)
        ax.semilogx(f, 20 * np.log10(abs(H)), color=col,
                    label=f"{n} vented ({r['kind']}): {r['Vab']:.0f} L, $f_B$={r['fb']:.0f} Hz, $f_3$={r['fl']:.0f} Hz")
        c = closed_opt(fs, Q, V)
        s = 1j * f / c["fc"]
        ax.semilogx(f, 20 * np.log10(abs(s ** 2 / (s ** 2 + s / c["Qtc"] + 1))), ":", color=col,
                    label=f"{n} closed: {c['Vab']:.0f} L, $f_3$={c['f3']:.0f} Hz")
    ax.axhline(-3, color="k", lw=.8, ls=":")
    ax.set(xlim=(10, 500), ylim=(-30, 4), xlabel="Frequency [Hz]", ylabel="Relative response [dB]",
           title="Problem 2: vented (solid, 24 dB/oct) vs closed (dotted, 12 dB/oct)")
    ax.legend(fontsize=7.5, loc="lower right")
    fig.tight_layout(); fig.savefig(IMG / "P8_vented_box.png", dpi=150); plt.close(fig)

    # 3. Scan-Speak: baffle vs closed (cases 1, 2) vs vented, absolute SPL at 2.83 V
    fig, ax = plt.subplots(figsize=(8, 4.2))
    for box, lab, col, ls in ((None, "infinite baffle", "0.4", "-"),
                              (("closed", c1["Vab"]), f"closed {c1['Vab']:.1f} L (case 1, $Q_{{TC}}$=0.71)", cols[0], "-"),
                              (("closed", 10), "closed 10 L (case 2, $Q_{TC}$=0.96)", cols[0], "--"),
                              (("vented", v["Vab"], v["fb"], 7), f"vented {v['Vab']:.0f} L, $f_B$={v['fb']:.0f} Hz ({v['kind']}, $Q_L$=7)", cols[2], "-")):
        ax.semilogx(f, spl(driver(SS, f, box)["total"]), ls, color=col, label=lab)
    ax.set(xlim=(10, 500), ylim=(55, 95), xlabel="Frequency [Hz]", ylabel="SPL at 1 m, 2.83 V [dB]",
           title="Slide 14 driver (Scan-Speak 22W/8857T00) in four mountings")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout(); fig.savefig(IMG / "L8_scanspeak_mountings.png", dpi=150); plt.close(fig)

    # 4. Vented box: driver/vent contributions and the two-peak impedance (slides 24-27)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4))
    r = driver(SS, f, ("vented", v["Vab"], v["fb"], 7))
    a1.semilogx(f, spl(r["total"]), color="#c0392b", label="total")
    a1.semilogx(f, spl(r["driver"]), color="#2a9d8f", label="driver (front of cone)")
    a1.semilogx(f, spl(r["vent"]), color="#2f6690", label="vent")
    a1.axvline(v["fb"], color="k", lw=.8, ls=":")
    a1.set(xlim=(10, 1000), ylim=(50, 95), xlabel="Frequency [Hz]", ylabel="SPL at 1 m, 2.83 V [dB]",
           title=f"Contributions, $f_B$ = {v['fb']:.0f} Hz")
    a1.legend(fontsize=8)
    for fb, col in ((v["fb"], cols[2]), (0.75 * v["fb"], cols[0]), (1.3 * v["fb"], cols[1])):
        a2.semilogx(f, abs(driver(SS, f, ("vented", v["Vab"], fb, 7))["ZE"]), color=col, label=f"$f_B$ = {fb:.0f} Hz")
    a2.semilogx(f, abs(driver(SS, f)["ZE"]), color="0.5", ls="--", label="infinite baffle")
    a2.axvline(t["fs"], color="k", lw=.8, ls=":")
    a2.set(xlim=(10, 1000), xlabel="Frequency [Hz]", ylabel="|Z_E| [Ω]",
           title="Input impedance: two peaks, $f_B$ at the dip")
    a2.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(IMG / "L8_vented_contrib_impedance.png", dpi=150); plt.close(fig)
    print(f"figures -> {IMG}")


if __name__ == "__main__":
    main("--plots" in sys.argv)
