#!/usr/bin/env python3
"""34870 Problems 5 (condenser microphone) and Problems 6 Q2 (sensitivity coefficients in
LTspice): the course circuit of the official solution, generated as LTspice schematics.

    python3 p5.py            # print the hand results, write the .asc/.plt files
    python3 p5.py --verify   # also run LTspice headless and compare with the closed form
    python3 p5.py --preview  # draw the .asc files to preview/*.png and lint the layout

Topology = the official solution (Problems 5 solution p.2 / Problems 6 solution fig. 1):
    electrical  : F_ECe0u = (E*Ce0/x0)*u pushed into Ce0 || RL      (Norton form of E*x/x0 in series with Ce0)
                  Vd2 senses the current i into RL, V(out) = output voltage per Pa
    mechanical  : IMPEDANCE analogy loop  Cmd -> Vd1 -> Mmd -> Rmd -> E_SdPd = -Sd*(pF - pB)
                  F_ECmi = (E*Cmd/x0)*i across Cmd (Norton form of the electrostatic force E*q/x0)
                  loop current I(Vd1) = diaphragm velocity u (positive = pushed in)
    acoustical  : IMPEDANCE analogy.  F_SdUd takes U = Sd*u out of the front node pF into the back node pB
                  front: radiation impedance of a piston in an unflanged tube to the source Vpi (1 Pa)
                  back : Cab1 (air between diaphragm and backplate), Mas + Ras (backplate holes), Cab2 (back volume)
                  Gpb  = Tsw * V(p_i)/Ra2 into pF: the diaphragm-reflection term, pF = T(s)*p_i for a blocked diaphragm
Needs the Lab A builder: ../../Labs/Lab A/LTspice/gen_ltspice.py (the labs repo).
"""
import cmath, math, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
LABA = HERE.parents[1] / "Labs" / "Lab A" / "LTspice"
sys.path.insert(0, str(LABA))
import gen_ltspice as g                      # noqa: E402

RHO, C0, EPS0 = 1.18, 344.0, 8.85e-12        # the sheet's air and the official solution's epsilon_0
SHEET = dict(r=9e-3, E=200.0, x0=20e-6, RL=500e6, Mmd=50e-6, Rmd=1.0, Cmd=4e-6, Mas=100.0, Ras=1e7, Vab=1e-6)
OPT = dict(SHEET, RL=1e9, Ras=80e6)          # the official optimised circuit (Problems 5 solution p.2)


# =====================================================================  closed form
def derived(p):
    Sd = math.pi * p["r"] ** 2
    d = dict(Sd=Sd, Ce0=EPS0 * Sd / p["x0"], Cab2=p["Vab"] / (RHO * C0 ** 2),
             Ma1=0.6133 * RHO / (math.pi * p["r"]), Ra1=0.5045 * RHO * C0 / (math.pi * p["r"] ** 2),
             Ra2=RHO * C0 / (math.pi * p["r"] ** 2), Ca1=0.55 * math.pi ** 2 * p["r"] ** 3 / (RHO * C0 ** 2))
    d["Cab1"] = d["Cab2"] / 200
    d["Kel"] = p["E"] * d["Ce0"] / p["x0"]
    d["Kmech"] = p["E"] * p["Cmd"] / p["x0"]
    d["Mmt"] = p["Mmd"] + Sd ** 2 * (d["Ma1"] + p["Mas"])
    d["Cmt"] = 1 / (1 / p["Cmd"] + Sd ** 2 / d["Cab2"])
    d["Rmt"] = p["Rmd"] + Sd ** 2 * p["Ras"]
    d["f0"] = 1 / (2 * math.pi * math.sqrt(d["Mmt"] * d["Cmt"]))
    d["Q"] = 2 * math.pi * d["f0"] * d["Mmt"] / d["Rmt"]
    d["M"] = p["E"] * d["Cmt"] * Sd / p["x0"]
    return d


def response(p, f, tsw, mass_only=False):
    """V(out)/p_i of exactly the drawn circuit (every element, incl. Cab1, Ra1/Ca1, RL and the i feedback).
    mass_only=True replaces the radiation impedance by its low-frequency mass j*w*Ma1 (the Problem 1 model)."""
    d = derived(p); jw = 2j * math.pi * f; Sd = d["Sd"]
    Zar = jw * d["Ma1"] if mass_only else 1 / (1 / (jw * d["Ma1"]) + 1 / (d["Ra2"] + 1 / (1 / d["Ra1"] + jw * d["Ca1"])))
    ZB = 1 / (jw * d["Cab1"] + 1 / (p["Ras"] + jw * p["Mas"] + 1 / (jw * d["Cab2"])))
    T = 1 + tsw * Zar / d["Ra2"]
    Ye = jw * d["Ce0"] + 1 / p["RL"]
    Zm = jw * p["Mmd"] + p["Rmd"] + 1 / (jw * p["Cmd"])
    u = Sd * T / (Zm + Sd ** 2 * (Zar + ZB) - d["Kmech"] * d["Kel"] / (p["RL"] * Ye * jw * p["Cmd"]))
    return d["Kel"] * u / Ye


# =====================================================================  LTspice
def params(s, y, p, extra=""):
    s.text(0, y, f".param rho0={RHO} c0={C0} rd={p['r']:g} Epol={p['E']:g} x0={p['x0']:g} RL={p['RL']:g} "
                 f"Vab={p['Vab']:g}" + extra, directive=True)
    s.text(0, y + 32, ".param Sd=pi*rd**2 Ce0=8.85e-12*Sd/x0 Kel=Epol*Ce0/x0 Kmech=Epol*Cmd/x0 Cab2=Vab/(rho0*c0**2) Cab1=Cab2/200", directive=True)
    s.text(0, y + 64, ".param Ma1=0.6133*rho0/(pi*rd) Ra1=0.5045*rho0*c0/(pi*rd**2) Ra2=rho0*c0/(pi*rd**2) "
                      "Ca1=0.55*pi**2*rd**3/(rho0*c0**2) Kpb=Tsw/Ra2", directive=True)


def circuit(s):
    # ---- electrical (top left): Norton source into Ce0 || RL
    s.text(0, -176, "ELECTRICAL: V(out) = output voltage [V] per 1 Pa", size=2)
    s.f_inject(0, 0, "F_ECe0u", "Vd1", "{Kel}")
    s.wire(0, 0, 352, 0); s.flag(96, 0, "e")
    s.vshunt("cap", 224, 0, "C_Ce0", "{Ce0}")
    x = s.vsense(352, 0, "Vd2"); s.wire(x, 0, x + 224, 0)
    s.flag(x + 80, 0, "out")
    s.vshunt("res", x + 224, 0, "R_RL", "{RL}")
    # ---- mechanical (top right): impedance-analogy loop, loop current = velocity
    mx = 1152
    s.text(mx - 96, -176, "MECHANICAL (impedance analogy): I(Vd1) = diaphragm velocity u [m/s]", size=2)
    s.f_inject(mx, 0, "F_ECmi", "Vd2", "{Kmech}")
    s.wire(mx, 0, mx + 352, 0); s.flag(mx + 96, 0, "m1")
    s.vshunt("cap", mx + 224, 0, "C_Cmd", "{Cmd}")
    x = s.vsense(mx + 352, 0, "Vd1"); s.wire(x, 0, x + 48, 0)
    x = s.hser("ind", x + 48, 0, "L_Mmd", "{Mmd}", g.NOLOSS); s.wire(x, 0, x + 48, 0)
    x = s.hser("res", x + 48, 0, "R_Rmd", "{Rmd}")
    ex = x + 320
    s.wire(x, 0, ex, 0)
    pins = s.sym("e", "R0", ex, -16, "E_SdPd", "{Sd}")          # V = Sd*(pB - pF): the net force pushes the diaphragm IN
    s.gnd(*pins[1])
    (cpx, cpy), (cmx, cmy) = pins[2], pins[3]
    s.wire(cpx, cpy, cpx - 48, cpy); s.wire(cpx - 48, cpy, cpx - 48, cpy + 128); s.wire(cpx - 48, cpy + 128, cpx - 112, cpy + 128)
    s.flag(cpx - 112, cpy + 128, "pB")
    s.wire(cmx, cmy, cmx - 16, cmy); s.wire(cmx - 16, cmy, cmx - 16, cmy + 128); s.wire(cmx - 16, cmy + 128, cmx - 112, cmy + 128)
    s.flag(cmx - 112, cmy + 128, "pF")
    # ---- acoustical (bottom): back chain | diaphragm | front radiation + source
    ay = 704
    s.text(0, ay - 400, "ACOUSTICAL (impedance analogy): V = pressure [Pa], I = volume velocity [m3/s].  back of the diaphragm (left) | front (right)", size=2)
    s.wire(64, ay, 224, ay)
    s.vshunt("cap", 64, ay, "C_Cab2", "{Cab2}")
    x = s.hser("res", 224, ay, "R_Ras", "{Ras}"); s.wire(x, ay, x + 48, ay)
    x = s.hser("ind", x + 48, ay, "L_Mas", "{Mas}", g.NOLOSS)
    s.wire(x, ay, 736, ay)
    s.vshunt("cap", 544, ay, "C_Cab1", "{Cab1}")
    s.flag(640, ay, "pB")
    s.sym("f", "R90", 816, ay, "F_SdUd", "Vd1 {Sd}", win=["WINDOW 0 -32 40 VBottom 2", "WINDOW 3 32 40 VTop 2"])
    s.wire(816, ay, 1232, ay)
    s.flag(912, ay, "pF")
    gp = s.sym("g", "R0", 1088, ay - 16, "G_pb", "{Kpb}")        # pushes Kpb*V(p_i) into pF
    s.gnd(*gp[0]); s.gnd(*gp[3])
    cx, cy = gp[2]
    s.wire(cx, cy, cx - 32, cy); s.wire(cx - 32, cy, cx - 32, cy + 112); s.wire(cx - 32, cy + 112, cx - 96, cy + 112)
    s.flag(cx - 96, cy + 112, "p_i")
    x = s.hser("ind", 1232, ay, "L_Ma1", "{Ma1}", g.NOLOSS)
    s.wire(x, ay, 1552, ay)
    s.vsrc(1552, ay, "V_pi", "AC 1")
    s.flag(1488, ay, "p_i")
    # radiation branch above LMa1: (Ra1 || Ca1) + Ra2
    ry = ay - 176
    s.wire(1232, ay, 1232, ry)
    x = s.hser("res", 1232, ry, "R_Ra1", "{Ra1}")
    s.wire(1232, ry, 1232, ry - 128); s.wire(1232, ry - 128, 1240, ry - 128)
    xc = s.hser("cap", 1240, ry - 128, "C_Ca1", "{Ca1}"); s.wire(xc, ry - 128, x, ry - 128); s.wire(x, ry - 128, x, ry)
    s.wire(x, ry, x + 64, ry)
    x2 = s.hser("res", x + 64, ry, "R_Ra2", "{Ra2}"); s.wire(x2, ry, 1552, ry); s.wire(1552, ry, 1552, ay)


def build(name, p, tsw, title, notes, step=None, extra_param=""):
    s = g.Sch()
    s.text(0, -416, title)
    s.text(0, -384, "course circuit from the official solution: electrical and acoustical in the impedance analogy, "
                    "electrostatic coupling as Norton current sources across Ce0 and Cmd")
    circuit(s)
    py = 1024
    if step:
        params(s, py, p, extra_param)
        s.text(0, py + 96, step, directive=True)
        py += 32 * step.count("\n")
    else:
        params(s, py, p, f" Mmd={p['Mmd']:g} Rmd={p['Rmd']:g} Cmd={p['Cmd']:g} Mas={p['Mas']:g} Ras={p['Ras']:g} Tsw={tsw}")
    s.text(0, py + 176, ".ac dec 1000 1 100k", directive=True)
    s.text(0, py + 208, ".meas AC M250 FIND mag(V(out)) AT 250", directive=True)
    for k, t in enumerate(notes):
        s.text(0, py + 272 + 32 * k, t)
    s.dump(HERE / f"{name}.asc")
    g.plt(HERE / f"{name}.plt", [(["V(out)"], (1e-3, 0.1)), (["V(pF)"], (0.3, 3))], (1, 100000))
    return HERE / f"{name}.asc"


P6_STEP = ("* run 1 = nominal, 2/3 = M_MD x0.9/x1.1, 4/5 = R_MD x0.9/x1.1, 6/7 = C_MD x0.9/x1.1; runs 8-14 repeat with Gpb switched on\n"
           ".step param run 1 14 1\n"
           ".param Tsw=if(run>7,1,0) idx=run-7*Tsw\n"
           ".param kM=table(idx,1,1,2,0.9,3,1.1,4,1) kR=table(idx,3,1,4,0.9,5,1.1,6,1) kC=table(idx,5,1,6,0.9,7,1.1)\n"
           ".param Mmd=50u*kM Rmd=1*kR Cmd=4u*kC Mas=100 Ras=10Meg")


def build_all():
    files = {}
    files["2b"] = build("P5_2b_Pressure", SHEET, 0, "Problems 5 Q2a/b - condenser microphone with the Problem 1 values, T(s) = 1 (Gpb off: Tsw = 0)",
                        ["plot V(out): flat 9.82 mV/Pa (-40.2 dB re 1 V/Pa), peak at about 10 kHz (f0 = 10.62 kHz, Q = 2.36), then -12 dB/octave",
                         "f0 = where the phase of V(out) has dropped 90 deg from its 250 Hz value;  Q = |V(out)| at f0 / |V(out)| at 250 Hz (linear)",
                         "the official figure shows the Kel source as 1.1m: that is E*Ce0/x0 = 1.126m rounded, and it is why the official M250 reads 9.6 mV/Pa"])
    files["2d"] = build("P5_2d_FreeField", SHEET, 1, "Problems 5 Q2d - the same microphone in a free field: T(s) switched on (Gpb = V(p_i)/Ra2, Tsw = 1)",
                        ["plot V(out) and V(pF): V(pF) = T(s) = 1 + Zar/Ra2 for a blocked diaphragm, rising from 1 to 2 (+6 dB) above ka = 1 (6.1 kHz)",
                         "the free-field response is the pressure response times T(s): the resonance peak gets lifted by up to 6 dB"])
    files["2ce"] = build("P5_2ce_Optimised", OPT, None, "Problems 5 Q2c/e - optimised: RL = 1 GOhm (flat to 1 Hz), Ras = 80 MOhm (more damping), both with and without T(s)",
                         ["run 1: Tsw = 0, pressure response (2c).  run 2: Tsw = 1, free-field response (2e, the official optimised curve)",
                          "2c alone (no T(s)): the flattest pressure response is Q = 0.707, i.e. Ras = 69 MOhm;  with T(s) the official choice is 80 MOhm",
                          "the free-field curve (run 2) stays within 0 to +1.5 dB from 20 Hz to 8 kHz, -3 dB at 17 kHz: a compromise between top-end sensitivity and ripple"],
                         step=".step param Tsw list 0 1",
                         extra_param=f" Mmd={OPT['Mmd']:g} Rmd={OPT['Rmd']:g} Cmd={OPT['Cmd']:g} Mas={OPT['Mas']:g} Ras={OPT['Ras']:g}")
    files["p6"] = build("P6_Q2_Sensitivity", SHEET, None, "Problems 6 Q2 - sensitivity coefficients: +/-10 % on M_MD, R_MD and C_MD (Problems 5 Q2b circuit), .step over 14 runs",
                        ["View > SPICE Error Log (Ctrl+L) lists M250 for every run: only runs 6/7 and 13/14 (C_MD) move it, by about +/-0.95 mV/Pa",
                         "M_MD and R_MD only change the response around and above resonance; Gpb (runs 8-14) changes nothing at 250 Hz",
                         "sensitivity coefficient dM/dC_MD ~ (M(1.1 C_MD) - M(0.9 C_MD)) / (0.2 C_MD)"],
                        step=P6_STEP)
    return files


# =====================================================================  verify
def split_runs(d):
    f = [x.real for x in d["frequency"]]; starts = [0] + [j for j in range(1, len(f)) if f[j] < f[j - 1]]
    ends = starts[1:] + [len(f)]
    return [{k: v[a:b] for k, v in d.items() if isinstance(v, list)} for a, b in zip(starts, ends)]


def at(f, fx):
    return min(range(len(f)), key=lambda j: abs(f[j] - fx))


def slide_f0_Q(f, h):
    """6B slide 20: f0 = phase dropped 90 deg from the 250 Hz value; Q = |H(f0)|/|H(250 Hz)|"""
    j0 = at(f, 250); ref = cmath.phase(h[j0])
    drop = [math.degrees((ref - cmath.phase(v)) % (2 * math.pi)) for v in h]
    j = next(k for k in range(j0, len(f)) if drop[k] >= 90)
    t = (90 - drop[j - 1]) / (drop[j] - drop[j - 1])           # interpolate between the two sweep points
    f0 = f[j - 1] * (f[j] / f[j - 1]) ** t
    return f0, abs(h[j]) / abs(h[j0])


def compare(d, p, tsw, label):
    f = [x.real for x in d["frequency"]]
    worst = max(abs(v / response(p, fi, tsw) - 1) for fi, v in zip(f, d["v(out)"]))
    good = worst < 1e-3
    print(f"  {'OK ' if good else 'BAD'} {label}: worst deviation from the closed form {worst:.1e}")
    return good


def verify(files):
    ok = True
    D = derived(SHEET)
    # --- 2b
    d = g.run_ltspice(files["2b"]); f = [x.real for x in d["frequency"]]; h = d["v(out)"]
    ok &= compare(d, SHEET, 0, "P5_2b_Pressure")
    f0, Q = slide_f0_Q(f, h); j = at(f, 250)
    print(f"      M(250 Hz) = {abs(h[j])*1e3:.3f} mV/Pa (sheet 9.8; official LTspice 9.6 = with Kel typed as 1.1m: "
          f"{abs(h[j])*1e3*1.1e-3/D['Kel']:.2f})   f0 (-90 deg) = {f0:.0f} Hz (theory {D['f0']:.0f})   "
          f"Q = |H(f0)|/|H(250)| = {Q:.3f} (theory {D['Q']:.3f})   peak {max(abs(v) for v in h)*1e3:.2f} mV/Pa at {f[max(range(len(f)), key=lambda k: abs(h[k]))]:.0f} Hz")
    good = abs(abs(h[j]) * 1e3 / (D["M"] * 1e3) - 1) < 0.01; ok &= good
    print(f"  {'OK ' if good else 'BAD'} M250: LTspice {abs(h[j])*1e3:.3f} mV/Pa vs E*Sd*C_MT/x0 = {D['M']*1e3:.3f}")
    # the slide procedure on the Problem 1 model (radiation = pure mass Ma1) must give back f0 and Q exactly
    hm = [response(SHEET, fi, 0, mass_only=True) for fi in f]
    f0m, Qm = slide_f0_Q(f, hm)
    good = abs(f0m / D["f0"] - 1) < 0.005 and abs(Qm / D["Q"] - 1) < 0.02; ok &= good
    print(f"  {'OK ' if good else 'BAD'} slide method on the Problem 1 model (Zar = jw*Ma1): f0 = {f0m:.0f} Hz, Q = {Qm:.3f}  (theory {D['f0']:.0f} Hz, {D['Q']:.3f})")
    print(f"      full circuit: f0 +{(f0/D['f0']-1)*100:.1f} %, Q {(Q/D['Q']-1)*100:+.1f} %: at 10 kHz ka = {2*math.pi*1e4*SHEET['r']/C0:.2f}, so the radiation"
          f" load is no longer a pure mass (less mass, plus radiation resistance)")
    # --- 2d
    d = g.run_ltspice(files["2d"]); f = [x.real for x in d["frequency"]]
    ok &= compare(d, SHEET, 1, "P5_2d_FreeField")
    print(f"      T at 1 kHz / 6.1 kHz / 20 kHz / 100 kHz: " + " / ".join(f"{abs(d['v(pf)'][at(f, x)]):.3f}" for x in (1e3, 6.08e3, 2e4, 1e5))
          + f"   peak {max(abs(v) for v in d['v(out)'])*1e3:.2f} mV/Pa")
    # --- 2c/e
    d = g.run_ltspice(files["2ce"]); runs = split_runs(d)
    for tsw, r in zip((0, 1), runs):
        ok &= compare(r, OPT, tsw, f"P5_2ce_Optimised run Tsw={tsw}")
        f = [x.real for x in r["frequency"]]; h = r["v(out)"]; ref = abs(h[at(f, 250)])
        band = [20 * math.log10(abs(h[k]) / ref) for k in range(len(f)) if 20 <= f[k] <= 8000]
        print(f"      M(250) = {ref*1e3:.3f} mV/Pa, 20 Hz-8 kHz within {min(band):+.2f}/{max(band):+.2f} dB, "
              f"-3 dB at {next(f[k] for k in range(at(f, 250), len(f)) if abs(h[k]) < ref/math.sqrt(2)):.0f} Hz, M(2 Hz) {20*math.log10(abs(h[at(f, 2)])/ref):+.2f} dB")
    # --- Problems 6 Q2
    d = g.run_ltspice(files["p6"]); runs = split_runs(d)
    labels = ["nominal", "M_MD x0.9", "M_MD x1.1", "R_MD x0.9", "R_MD x1.1", "C_MD x0.9", "C_MD x1.1"]
    M250 = []
    for n, r in enumerate(runs):
        tsw, k = (1, n - 7) if n >= 7 else (0, n)
        p = dict(SHEET); p["Mmd"] *= (0.9, 1.1)[k - 1] if k in (1, 2) else 1
        p["Rmd"] *= (0.9, 1.1)[k - 3] if k in (3, 4) else 1; p["Cmd"] *= (0.9, 1.1)[k - 5] if k in (5, 6) else 1
        ok &= compare(r, p, tsw, f"P6 run {n+1:2d} Gpb {'on ' if tsw else 'off'} {labels[k]:10s}")
        f = [x.real for x in r["frequency"]]; M250.append(abs(r["v(out)"][at(f, 250)]))
    print(f"  {'':3s} Gpb off: dM250 for M_MD -/+10 %: {(M250[1]-M250[0])*1e3:+.4f}/{(M250[2]-M250[0])*1e3:+.4f}, R_MD: {(M250[3]-M250[0])*1e3:+.4f}/{(M250[4]-M250[0])*1e3:+.4f}, "
          f"C_MD: {(M250[5]-M250[0])*1e3:+.3f}/{(M250[6]-M250[0])*1e3:+.3f} mV/Pa  (official +0.922/-0.929 with the rounded Kel -> "
          f"here x1.1m/Kel: {(M250[6]-M250[0])*1e3*1.1e-3/D['Kel']:+.3f}/{(M250[5]-M250[0])*1e3*1.1e-3/D['Kel']:+.3f})")
    coef = (M250[6] - M250[5]) / (0.2 * SHEET["Cmd"])
    good = abs(coef / 2370.1 - 1) < 0.01; ok &= good
    print(f"  {'OK ' if good else 'BAD'} dM/dC_MD from +/-10 %: {coef:.1f} (V/Pa)/(m/N) vs GUM derivative 2370.1;  Gpb on changes M250 by "
          f"{max(abs(M250[k+7]/M250[k]-1) for k in range(7))*100:.3f} % at most")
    print("ALL OK" if ok else "MISMATCH")
    return ok


if __name__ == "__main__":
    D = derived(SHEET)
    print(f"S_D = {D['Sd']:.4e} m2  Ce0 = {D['Ce0']*1e12:.1f} pF  Ma1 = {D['Ma1']:.4f}  Cab2 = {D['Cab2']*1e12:.4f} pF  Cab1 = {D['Cab1']*1e15:.3f} fF")
    print(f"M_MT = {D['Mmt']:.4e} kg  C_MT = {D['Cmt']:.4e} m/N  R_MT = {D['Rmt']:.4f} Ns/m")
    print(f"P5 1a f0 = {D['f0']:.0f} Hz   1b Q = {D['Q']:.4f}   1c M = {D['M']*1e3:.3f} mV/Pa")
    print(f"P5 2  Kel = E*Ce0/x0 = {D['Kel']:.4e}  Kmech = E*Cmd/x0 = {D['Kmech']:.1f}  Ra1 = {D['Ra1']:.4e}  Ra2 = {D['Ra2']:.4e}  "
          f"Ca1 = {D['Ca1']:.4e}  1/Ra2 = {1/D['Ra2']:.4e}")
    q707 = (math.sqrt(D["Mmt"] / D["Cmt"]) / (1 / math.sqrt(2)) - SHEET["Rmd"]) / D["Sd"] ** 2
    print(f"P5 2c Ras for Q = 0.707: {q707/1e6:.1f} MOhm;  official optimum (with T): 80 MOhm -> Q = {derived(OPT)['Q']:.3f}")
    files = build_all()
    if "--preview" in sys.argv:
        import preview_asc as pv
        pv.HERE = HERE
        [pv.main(str(p)) for p in files.values()]
    if "--verify" in sys.argv:
        sys.exit(0 if verify(files) else 1)
