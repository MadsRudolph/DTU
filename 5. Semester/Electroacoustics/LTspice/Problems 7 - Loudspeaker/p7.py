#!/usr/bin/env python3
"""34870 Problems 7 (Loudspeakers 1): hand calculations for problems 1-3 and the
LTspice model of the 315 SWR on an infinite baffle for problem 4.

    python3 p7.py            # print problems 1-3, write the two .asc/.plt files
    python3 p7.py --verify   # also run LTspice headless and compare with the closed form
    python3 p7.py --plots    # (with --verify) write the figures into the vault Images/Lecture7/
    python3 p7.py --preview  # draw the .asc files to preview/*.png and lint the layout

The circuit follows the lecture's slide 27 (Leach): IMPEDANCE analogy in all three
domains, so every domain is a loop and the couplings are controlled sources.
    electrical: e_g -> R_E -> [lossy L_E] -> H_emf = Bl*u          (current i = I(Vd1))
    mechanical: H_Bli = Bl*i -> M_MD -> R_MS -> C_MS -> E = S_D*p_D (velocity u = I(Vd2))
    acoustical: F = S_D*u injected into BOTH radiation impedances (front + back, each a
                baffled piston, drawn as one network with every element doubled)
Only the baffled data-sheet values are used: M_MD = M_MS(baffled) - 2 S_D^2 M_A1.
Needs the Lab A builder: ../../Labs/Lab A/LTspice/gen_ltspice.py (the labs repo).
"""
import cmath, math, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
LABA = HERE.parents[1] / "Labs" / "Lab A" / "LTspice"
sys.path.insert(0, str(LABA))
import gen_ltspice as g                      # noqa: E402

g.PINS["h"] = [(0, 16), (0, 96)]
RHO, C0, PREF = 1.2, 344.0, 20e-6            # the problem sheet's air
VAULT_IMG = pathlib.Path.home() / "DTU/Obsidian/Courses/34870 Electroacoustics/Images/Lecture7"


# =====================================================================  problems 1-3
def ts(Mms, Cms, Rms, Bl, Re, Sd):
    ws = 1 / math.sqrt(Mms * Cms)
    Qms, Qes = ws * Mms / Rms, Re * ws * Mms / Bl ** 2
    return dict(fs=ws / 2 / math.pi, Qms=Qms, Qes=Qes, Qts=Qms * Qes / (Qms + Qes), Vas=RHO * C0 ** 2 * Sd ** 2 * Cms)


def ma1(a):
    return 8 * RHO / (3 * math.pi ** 2 * a)


def problem1():
    a = 0.10; Sd = math.pi * a ** 2
    t = ts(38e-3, 0.9e-3, 1.5, 5.0, 6.0, Sd)
    print(f"P1a  fs = {t['fs']:.2f} Hz  Qms = {t['Qms']:.2f}  Qes = {t['Qes']:.3f}  Qts = {t['Qts']:.3f}  Vas = {t['Vas']*1e3:.1f} L")
    # b) free air, Qes = 1.5 measured, Cms, Bl, Re unchanged -> Qes = Re/Bl^2 sqrt(M/C)
    Mf = (1.5 * 5.0 ** 2 / 6.0) ** 2 * 0.9e-3
    Qmf = math.sqrt(Mf / 0.9e-3) / 1.5
    print(f"P1b  M_MS(free) = {Mf*1e3:.2f} g  Qms(free) = {Qmf:.3f}   "
          f"[check: 38 g - S_D^2 M_A1 = {(38e-3 - Sd**2*ma1(a))*1e3:.2f} g, fs(free) = {1/(2*math.pi*math.sqrt(Mf*0.9e-3)):.2f} Hz]")


SWR = dict(Bl=11.6, Rms=3.25, Cms=0.55e-3, D=0.257, Vas=0.210, Le=2.8e-3,
           Mms_free=80.2e-3, Qes_free=0.49, Qms_free=3.72, Mms_baf=88.2e-3, fs_baf=22.9, hvc=26e-3, hmg=8e-3)


def problem2():
    s = SWR
    fs_free = 1 / (2 * math.pi * math.sqrt(s["Mms_free"] * s["Cms"]))
    Sd = math.sqrt(s["Vas"] / (RHO * C0 ** 2 * s["Cms"]))
    Re = s["Qes_free"] * s["Bl"] ** 2 / (2 * math.pi * fs_free * s["Mms_free"])
    fs_baf = 1 / (2 * math.pi * math.sqrt(s["Mms_baf"] * s["Cms"]))
    Qes_baf = Re * 2 * math.pi * fs_baf * s["Mms_baf"] / s["Bl"] ** 2
    print(f"P2   fs(free) = {fs_free:.2f} Hz  S_D = {Sd*1e4:.1f} cm2 (pi D^2/4 = {math.pi*s['D']**2/4*1e4:.1f})  "
          f"R_E = {Re:.3f} ohm  Qes(baffled) = {Qes_baf:.3f}  [fs(baffled) from M,C = {fs_baf:.2f} Hz, "
          f"Qms(baffled) = {2*math.pi*fs_baf*s['Mms_baf']/s['Rms']:.2f}, Qts = {1/(s['Rms']/(2*math.pi*fs_baf*s['Mms_baf']) + 1/Qes_baf):.3f}, "
          f"Z_max = R_E + Bl^2/R_MS = {Re + s['Bl']**2/s['Rms']:.1f} ohm]")
    return dict(Sd=Sd, Re=Re, fs=fs_baf, Qes=Qes_baf)


def problem3(d):
    s = SWR; Sd, Re, M = d["Sd"], d["Re"], s["Mms_baf"]
    eta = RHO / (2 * math.pi * C0) / Re * (s["Bl"] * Sd / M) ** 2
    p1 = RHO / (2 * math.pi) * s["Bl"] * Sd / (Re * M)
    print(f"P3.1 efficiency = {eta*100:.3f} %")
    print(f"P3.2 p(1 m, 1 V) = {p1:.4f} Pa = {20*math.log10(p1):.2f} dB re 1 Pa/V = {20*math.log10(p1/PREF):.1f} dB SPL; "
          f"at 2.83 V: {20*math.log10(2.83*p1/PREF):.1f} dB (data sheet, measured: 89.3)")
    Rmt = s["Rms"] + s["Bl"] ** 2 / Re; Qts = 2 * math.pi * d["fs"] * M / Rmt
    x0 = s["Bl"] * s["Cms"] / Re
    for f in (50, 200):
        r = f / d["fs"]; x = x0 * 4 / abs(complex(1 - r * r, r / Qts))
        print(f"P3.3 x_D({f} Hz, 4 V) = {x*1e3:.4f} mm   (Qts = {Qts:.3f})")
    xmax = (s["hvc"] - s["hmg"]) / 2
    for f in (50, 200):
        pk = (2 * math.pi * f) ** 2 * RHO * Sd * xmax / (2 * math.pi)
        print(f"P3.4 x_max,lin = {xmax*1e3:.0f} mm -> p({f} Hz, 1 m) = {pk:.2f} Pa peak = {20*math.log10(pk/math.sqrt(2)/PREF):.1f} dB SPL (rms)"
              f"; needs e_g = {xmax/(x0/abs(complex(1-(f/d['fs'])**2, f/d['fs']/Qts))):.0f} V")
    return eta, p1


# =====================================================================  problem 4: closed form
def model(d, lossy):
    s = SWR; Sd = d["Sd"]; a = math.sqrt(Sd / math.pi)
    MA1, RA1, RA2, CA1 = ma1(a), 0.441 * RHO * C0 / Sd, RHO * C0 / Sd, 5.94 * a ** 3 / (RHO * C0 ** 2)
    Mmd = s["Mms_baf"] - 2 * Sd ** 2 * MA1
    return dict(Sd=Sd, a=a, MA1=MA1, RA1=RA1, RA2=RA2, CA1=CA1, Mmd=Mmd, Re=d["Re"], lossy=lossy)


def response(m, f, Lstar=0.0106, n=0.76):
    s = SWR; w = 2 * math.pi * f; jw = 1j * w
    Zar = 1 / (1 / (jw * m["MA1"]) + 1 / (m["RA2"] + 1 / (1 / m["RA1"] + jw * m["CA1"])))
    ZL = Lstar * jw ** n if m["lossy"] else 0
    ZM = jw * m["Mmd"] + s["Rms"] + 1 / (jw * s["Cms"]) + m["Sd"] ** 2 * 2 * Zar
    ZE = m["Re"] + ZL + s["Bl"] ** 2 / ZM
    i = 1 / ZE; u = s["Bl"] * i / ZM; U = m["Sd"] * u
    return dict(ZE=ZE, u=u, x=u / jw, pff=jw * RHO * U / (2 * math.pi), pnf=Zar * U)


# =====================================================================  problem 4: LTspice
def build(m, lossy):
    name = "P7_315SWR_Baffle_LossyLe" if lossy else "P7_315SWR_Baffle"
    s = g.Sch()
    s.text(0, -448, "Problems 7.4 - 315 SWR on an infinite baffle (Leach, lecture 7 slide 27).  IMPEDANCE analogy in all three domains:")
    s.text(0, -416, "electrical V = voltage, I = current  |  mechanical V = force, I = velocity  |  acoustical V = pressure, I = volume velocity")
    s.text(0, -368, f".param Re={m['Re']:.4g} Bl={SWR['Bl']} Mmd={m['Mmd']:.5g} Rms={SWR['Rms']} Cms={SWR['Cms']} Sd={m['Sd']:.5g}", directive=True)
    s.text(0, -336, f".param MA1={m['MA1']:.5g} RA1={m['RA1']:.5g} RA2={m['RA2']:.5g} CA1={m['CA1']:.5g}" +
           ("  Lstar=0.0106 n=0.76" if lossy else ""), directive=True)
    # ---- electrical loop
    s.vsrc(0, 0, "V_eg", "AC 1")
    s.flag(64, 0, "eg"); s.wire(0, 0, 144, 0)
    x = s.vsense(144, 0, "Vd1"); s.wire(x, 0, x + 48, 0)
    x = s.hser("res", x + 48, 0, "R_Re", "{Re}")
    if lossy:                                          # Z = Lstar*(jw)^n as a G source: I = V/Z, + pin on the left
        s.wire(x, 0, x + 64, 0); s.flag(x + 64, 0, "vc1"); s.wire(x + 64, 0, x + 112, 0)
        ox = x + 112 + 96
        pins = s.sym("g", "R90", ox, 0, "G_Le", "Laplace=1/(Lstar*s**n)", win=["WINDOW 0 48 56 VTop 2", "WINDOW 3 80 56 VTop 2"])
        (ncpx, ncpy), (ncmx, ncmy) = pins[2], pins[3]
        s.wire(ncpx, ncpy, ncpx, ncpy - 32); s.flag(ncpx, ncpy - 32, "vc1")
        s.wire(ncmx, ncmy, ncmx, ncmy - 32); s.flag(ncmx, ncmy - 32, "vc2")
        x = pins[1][0]; s.flag(x + 48, 0, "vc2"); s.wire(x, 0, x + 48, 0)
        x += 48
    s.wire(x, 0, x + 128, 0); x += 128
    s.sym("h", "R0", x, -16, "H_emf", "Vd2 {Bl}", win=["WINDOW 0 24 40 Left 2", "WINDOW 3 24 72 Left 2"]); s.gnd(x, 80)
    # ---- mechanical loop
    mx = x + 400
    s.sym("h", "R0", mx, -16, "H_Bli", "Vd1 {Bl}", win=["WINDOW 0 24 40 Left 2", "WINDOW 3 24 72 Left 2"]); s.gnd(mx, 80)
    s.wire(mx, 0, mx + 192, 0)
    x = s.vsense(mx + 192, 0, "Vd2"); s.wire(x, 0, x + 48, 0)
    x = s.hser("ind", x + 48, 0, "L_Mmd", "{Mmd}", g.NOLOSS); s.wire(x, 0, x + 48, 0)
    x = s.hser("res", x + 48, 0, "R_Rms", "{Rms}"); s.wire(x, 0, x + 48, 0)
    x = s.hser("cap", x + 48, 0, "C_Cms", "{Cms}"); s.wire(x, 0, x + 304, 0)
    s.e_src(x + 304, 0, "E_SdpD", "{Sd}", "pD")
    # ---- acoustical: F injects U = Sd*u into front + back radiation impedance (each baffled piston, doubled)
    ay = 480
    s.text(0, ay - 128, "acoustic load: front + back face, each a baffled piston (Z_AF = Z_AB = Z_ar), drawn as ONE network with every element doubled")
    s.text(0, ay - 96, "V(pD) = p_F + p_B = 2 Z_ar U drives the reaction force;  near-field (front) pressure p_near = V(pD)/2")
    s.f_inject(128, ay, "F_SdUd", "Vd2", "{Sd}")
    s.wire(128, ay, 128 + 2 * g.PITCH + 32, ay)
    s.flag(224, ay, "pD")
    s.vshunt("ind", 128 + g.PITCH, ay, "L_2MA1", "{2*MA1}", g.NOLOSS)
    s.radnet(128 + 2 * g.PITCH + 32, ay, ("R_2RA2", "{2*RA2}"), ("R_2RA1", "{2*RA1}"), ("C_CA1h", "{CA1/2}"))
    # ---- outputs
    oy, ox = ay, 1440
    s.text(ox - 96, oy - 176, "outputs for e_g = 1 V (plot in dB: V(SPLff), V(SPLnf) read directly as dB SPL)")
    s.sym("h", "R0", ox, oy - 16, "H_u", "Vd2 1", win=["WINDOW 0 24 40 Left 2", "WINDOW 3 24 72 Left 2"]); s.gnd(ox, oy + 80); s.flag(ox, oy, "uD")
    k = RHO / (2 * math.pi * 1.0 * PREF)
    s.e_src(ox + 400, oy, "E_ff", f"Laplace={k*m['Sd']:.5g}*s", "uD"); s.flag(ox + 400, oy, "SPLff")
    s.e_src(ox + 880, oy, "E_nf", f"{1/(2*PREF):g}", "pD"); s.flag(ox + 880, oy, "SPLnf")
    s.e_src(ox + 1280, oy, "E_x", "Laplace=1/s", "uD"); s.flag(ox + 1280, oy, "xD")
    s.text(0, 880, ".ac dec 200 5 20k", directive=True)
    s.text(0, 928, "far field (1 m) p = j*w*rho/(2*pi*r) * Sd*u  -> E_ff = rho*Sd/(2 pi r 20u) * s.   Z_E = V(eg)/I(Vd1).   displacement: V(xD) [m per V]")
    s.text(0, 960, "check: |Z_E| peaks at f_s = 22.9 Hz with R_E + Bl^2/R_MS = 46.9 ohm;  mid-band V(SPLff) = 81.5 dB (sensitivity -12.4 dB re 1 Pa/V)")
    s.dump(HERE / f"{name}.asc")
    g.plt(HERE / f"{name}.plt", [(["V(SPLff)", "V(SPLnf)"], (1, 1e6)), (["V(eg)/I(Vd1)"], (1, 100)), (["V(xD)"], (1e-7, 1e-2))], (5, 20000))
    return HERE / f"{name}.asc"


def verify(m_by, plots=False):
    ok = True; runs = {}
    for lossy, asc in m_by.items():
        m = model(D, lossy); d = g.run_ltspice(asc); f = [v.real for v in d["frequency"]]; runs[lossy] = (f, d)
        worst = 0
        for j, fi in enumerate(f):
            r = response(m, fi)
            ze = d["v(eg)"][j] / d["i(vd1)"][j]
            for got, want in ((ze, r["ZE"]), (d["v(splff)"][j], r["pff"] / PREF), (d["v(splnf)"][j], r["pnf"] / PREF), (d["v(xd)"][j], r["x"])):
                worst = max(worst, abs(got / want - 1))
        zmag = [abs(d["v(eg)"][j] / d["i(vd1)"][j]) for j in range(len(f))]
        jp = max((j for j in range(len(f)) if f[j] < 100), key=lambda j: zmag[j])
        at = lambda fx: min(range(len(f)), key=lambda j: abs(f[j] - fx))
        good = worst < 2e-3; ok &= good
        print(f"  {'OK ' if good else 'BAD'} {asc.name}: worst deviation from the closed form {worst:.1e}; |Z_E| peak {zmag[jp]:.2f} ohm at {f[jp]:.2f} Hz; "
              f"SPL_ff(150 Hz) = {20*math.log10(abs(d['v(splff)'][at(150)])):.2f} dB; x(50 Hz, 4 V) = {4*abs(d['v(xd)'][at(50)])*1e3:.3f} mm; "
              f"x(200 Hz, 4 V) = {4*abs(d['v(xd)'][at(200)])*1e6:.1f} um; near/far at 100 Hz = {20*math.log10(abs(d['v(splnf)'][at(100)]/d['v(splff)'][at(100)])):.2f} dB; "
              f"|Z_E(1 kHz)| = {zmag[at(1000)]:.2f} ohm")
    print("ALL OK" if ok else "MISMATCH")
    if plots:
        make_plots(runs)
    return ok


def make_plots(runs):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    VAULT_IMG.mkdir(parents=True, exist_ok=True)
    f, d = runs[False]; fl, dl = runs[True]
    db = lambda v: [20 * math.log10(abs(x)) for x in v]
    m = model(D, False); a = m["a"]; fs = 1 / (2 * math.pi * math.sqrt(SWR["Mms_baf"] * SWR["Cms"]))
    # 1. far vs near field
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.semilogx(f, db(d["v(splff)"]), label="far field, 1 m", color="#1f5fa8")
    ax.semilogx(f, db(d["v(splnf)"]), label="near field (on the cone)", color="#c0392b")
    ax.semilogx(f, [x - 20 * math.log10(16 / (3 * math.pi * a)) for x in db(d["v(splnf)"])], "--", color="#c0392b", lw=1,
                label=f"near field − 20 log(16r/3πa) = −{20*math.log10(16/(3*math.pi*a)):.1f} dB")
    ax.axvline(fs, color="grey", lw=0.8, ls=":"); ax.text(fs * 1.05, 45, f"$f_s$ = {fs:.1f} Hz", color="grey")
    ax.axvline(C0 / (2 * math.pi * a), color="grey", lw=0.8, ls=":"); ax.text(C0 / (2 * math.pi * a) * 1.05, 45, "ka = 1", color="grey")
    ax.set(xlabel="Frequency [Hz]", ylabel="SPL [dB re 20 µPa] for 1 V", title="315 SWR on an infinite baffle (LTspice, Problems 7.4)", ylim=(40, 110), xlim=(5, 20e3))
    ax.grid(True, which="both", alpha=0.3); ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout(); fig.savefig(VAULT_IMG / "P7_315SWR_SPL_far_near.png", dpi=130); plt.close(fig)
    # 2. impedance, R_E only vs lossy inductor vs ideal 2.8 mH
    ideal = [abs(response(m, x)["ZE"] + 1j * 2 * math.pi * x * SWR["Le"]) for x in f]
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.semilogx(f, [abs(d["v(eg)"][j] / d["i(vd1)"][j]) for j in range(len(f))], label="voice coil = $R_E$ only (4.1)", color="#1f5fa8")
    ax.semilogx(fl, [abs(dl["v(eg)"][j] / dl["i(vd1)"][j]) for j in range(len(fl))], label="lossy $L_E$: 0.0106·(jω)$^{0.76}$ (4.3)", color="#c0392b")
    ax.semilogx(f, ideal, "--", lw=1, color="grey", label="ideal $L_E$ = 2.8 mH (data sheet)")
    ax.set(xlabel="Frequency [Hz]", ylabel="|Z$_E$| [Ω]", title="315 SWR electrical input impedance", ylim=(0, 60), xlim=(5, 20e3))
    ax.grid(True, which="both", alpha=0.3); ax.legend(loc="upper center", fontsize=8)
    fig.tight_layout(); fig.savefig(VAULT_IMG / "P7_315SWR_impedance.png", dpi=130); plt.close(fig)
    # 3. displacement at 4 V
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.loglog(f, [4 * abs(x) * 1e3 for x in d["v(xd)"]], color="#1f5fa8", label="$x_D$ for $e_g$ = 4 V")
    ax.axhline(9, color="#c0392b", ls="--", lw=1, label="$x_{max,lin}$ = (26 − 8)/2 = 9 mm")
    for fx in (50, 200):
        j = min(range(len(f)), key=lambda i: abs(f[i] - fx)); ax.plot(fx, 4 * abs(d["v(xd)"][j]) * 1e3, "ko", ms=4)
        ax.annotate(f"{4*abs(d['v(xd)'][j])*1e3:.3g} mm @ {fx} Hz", (fx, 4 * abs(d["v(xd)"][j]) * 1e3), textcoords="offset points", xytext=(6, 6), fontsize=8)
    ax.set(xlabel="Frequency [Hz]", ylabel="Cone displacement [mm, peak]", title="315 SWR cone displacement (baffled)", xlim=(5, 2000), ylim=(1e-3, 20))
    ax.grid(True, which="both", alpha=0.3); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(VAULT_IMG / "P7_315SWR_displacement.png", dpi=130); plt.close(fig)
    print("figures ->", VAULT_IMG)


if __name__ == "__main__":
    problem1(); D = problem2(); problem3(D)
    files = {False: build(model(D, False), False), True: build(model(D, True), True)}
    m = model(D, False)
    print(f"P4   S_D = {m['Sd']*1e4:.1f} cm2, a = {m['a']*100:.2f} cm, M_A1 = {m['MA1']:.4g} kg/m4, 2 S_D^2 M_A1 = {2*m['Sd']**2*m['MA1']*1e3:.2f} g "
          f"-> M_MD = {m['Mmd']*1e3:.2f} g (free-air M_MS would be {(m['Mmd']+m['Sd']**2*m['MA1'])*1e3:.1f} g vs 80.2 on the sheet); "
          f"near/far = 16r/(3 pi a) = {20*math.log10(16/(3*math.pi*m['a'])):.2f} dB")
    if "--preview" in sys.argv:
        import preview_asc as pv
        pv.HERE = HERE
        [pv.main(str(p)) for p in files.values()]
    if "--verify" in sys.argv:
        sys.exit(0 if verify(files, "--plots" in sys.argv) else 1)
