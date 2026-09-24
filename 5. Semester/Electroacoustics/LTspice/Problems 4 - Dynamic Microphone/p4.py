#!/usr/bin/env python3
"""34870 Problems 4 (dynamic microphones, lecture 4B): hand answers to problem 1 and
the LTspice models for problem 2.

    python3 p4.py            # print problem 1 + the 2a prediction, write the .asc/.plt files
    python3 p4.py --verify   # also run LTspice headless and compare with the closed form
    python3 p4.py --preview  # draw the .asc files to preview/*.png and lint the layout

Topology = the official solution's (page 3): IMPEDANCE analogy in all three domains.
    electrical: H_Blu = Bl*u -> R_E -> R_L                 (i = I(Vd1), output e = V(out))
    mechanical: H_Bli = Bl*i -> M_MD -> R_MS -> C_MS -> E_SdpD = S_D*(p_f - p_b)   (u = I(Vd2))
    acoustical: p_i -> M_A1 -> [F_U: U = S_D*u carried from node pf to node pb] -> back network
The front air mass is the piston-in-a-tube value M_A1 = 0.6133 rho/(pi a) = 18.14 kg/m^4,
as in the official solution.
Needs the Lab A builder: ../../Labs/Lab A/LTspice/gen_ltspice.py (the labs repo).
"""
import cmath, math, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
LABA = HERE.parents[1] / "Labs" / "Lab A" / "LTspice"
sys.path.insert(0, str(LABA))
import gen_ltspice as g                      # noqa: E402

g.PINS["h"] = [(0, 16), (0, 96)]
RHO, C0 = 1.18, 344.0                        # the problem sheet's air

# ---------------------------------------------------------------- the sheet's microphone
a = 0.0254 / 2
Sd = math.pi * a ** 2
MIC = dict(Mmd=0.2e-3, Rms=1.0, Cms=0.21e-3, Bl=20.0, Re=200.0, Rl=47e3, Sd=Sd, MA1=0.6133 * RHO / (math.pi * a))
CA = lambda V: V / (RHO * C0 ** 2)           # compliance of a closed volume

# back networks (acoustic element values)
NET_2A = dict(Raf=2e7, Cab=CA(5e-6))                                   # sheet: V = 5 cm3, R_AF = 2e7
RAF_2B = [1.2708e8, 2e7, 9.173e6]                                      # 0.3, 1.64, 3.0 mV/Pa
NET_1C = dict(Raf=35.5e6, Cab=77.5e-12)                                # the official's uncompensated reference (1b/1c design)
NET_2C = dict(Cab1=0.3e-12, Rat=35.5e6, Mat=50.0, Cab2=76e-12)         # official compensated network, without the vent
NET_2D = dict(NET_2C, Map=80e3, Rap=3e6)                               # ... with the vent tube in V2 (to the outside)


def problem1():
    m = MIC; Mmt = m["Mmd"] + Sd ** 2 * m["MA1"]
    Cmt = 1 / (1 / m["Cms"] + Sd ** 2 / CA(30e-6))
    print(f"P1a  S_D = {Sd*1e4:.3f} cm2, M_A1 = {m['MA1']:.3f} kg/m4 -> M_MT = {Mmt*1e3:.4f} g, C_MT = {Cmt*1e3:.4f} mm/N  [0.205 g & 0.168 mm/N]")
    Cmt2 = 1 / ((2 * math.pi * 1e3) ** 2 * Mmt); Cab2 = Sd ** 2 / (1 / Cmt2 - 1 / m["Cms"])
    print(f"P1b  C_MT = {Cmt2:.4g} m/N -> C_AB = {Cab2:.4g} m5/N -> V_AB = {Cab2*RHO*C0**2*1e6:.2f} cm3  [10.8 cm3]")
    Rmt = m["Bl"] * Sd / 1e-3; Raf = (Rmt - m["Rms"] - m["Bl"] ** 2 / (m["Re"] + m["Rl"])) / Sd ** 2
    Q = 2 * math.pi * 1e3 * Mmt / Rmt; BW = 1e3 / Q
    print(f"P1c  R_MT = {Rmt:.3f} Ns/m -> R_AF = {Raf:.4g} Ns/m5, Q = {Q:.4f}, BW = {BW:.1f} Hz  [3.56e7 & 7.88 kHz]")
    a1 = (BW / 1e3 + math.sqrt((BW / 1e3) ** 2 + 4)) / 2
    print(f"P1d  f_a = {1e3/a1:.1f} Hz, f_b = {1e3*a1:.1f} Hz  [125 Hz & 8.01 kHz]")


# ---------------------------------------------------------------- closed form
def back(net, jw):
    """(Z_B, alpha): back-network impedance seen by the diaphragm, and the fraction of p_i
    that reaches the back of the diaphragm through the vent (0 without a vent)."""
    if "Cab" in net:
        return net["Raf"] + 1 / (jw * net["Cab"]), 0
    Zc1, Zc2, Zt = 1 / (jw * net["Cab1"]), 1 / (jw * net["Cab2"]), net["Rat"] + jw * net["Mat"]
    if "Map" not in net:
        return 1 / (1 / Zc1 + 1 / (Zt + Zc2)), 0
    Zv = net["Rap"] + jw * net["Map"]
    ZB = 1 / (1 / Zc1 + 1 / (Zt + 1 / (1 / Zc2 + 1 / Zv)))
    Z2 = 1 / (1 / Zc2 + 1 / (Zt + Zc1))
    return ZB, Z2 / (Zv + Z2) * Zc1 / (Zt + Zc1)


def sens(net, f):
    """e/p_i in V/Pa (complex), same sign convention as the circuit"""
    m = MIC; jw = 2j * math.pi * f
    ZB, alpha = back(net, jw)
    Zm = jw * m["Mmd"] + m["Rms"] + 1 / (jw * m["Cms"]) + m["Bl"] ** 2 / (m["Re"] + m["Rl"])
    U = (1 - alpha) / (Zm / Sd ** 2 + jw * m["MA1"] + ZB)       # volume velocity into the diaphragm per pascal
    return -m["Rl"] / (m["Re"] + m["Rl"]) * m["Bl"] * U / Sd


# ---------------------------------------------------------------- LTspice
def build(name, title, net, step=None, notes=()):
    m = MIC; s = g.Sch()
    s.text(0, -480, title)
    s.text(0, -448, "IMPEDANCE analogy in all three domains (as the official solution): electrical V = voltage, I = current  |  "
                    "mechanical V = force, I = velocity  |  acoustical V = pressure, I = volume velocity")
    s.text(0, -400, f".param Re={m['Re']:g} Rl={m['Rl']:g} Bl={m['Bl']:g} Mmd={m['Mmd']:g} Rms={m['Rms']:g} Cms={m['Cms']:g} "
                    f"Sd={Sd:.5g} MA1={m['MA1']:.5g}", directive=True)
    s.text(0, -368, ".param " + " ".join(f"{k}={v:.4g}" for k, v in net.items()), directive=True)
    # ---- electrical loop: out -> R_E -> Vd1 -> H_Blu (+ top), R_L from out to ground
    s.vshunt("res", 0, 0, "R_Rl", "{Rl}")
    s.flag(0, 0, "out"); s.wire(0, 0, 96, 0)
    x = s.hser("res", 96, 0, "R_Re", "{Re}"); s.wire(x, 0, x + 64, 0)
    x = s.vsense(x + 64, 0, "Vd1"); s.wire(x, 0, x + 144, 0); x += 144
    s.sym("h", "R0", x, -16, "H_Blu", "Vd2 {Bl}", win=["WINDOW 0 24 40 Left 2", "WINDOW 3 24 72 Left 2"]); s.gnd(x, 80)
    # ---- mechanical loop
    mx = x + 400
    s.sym("h", "R0", mx, -16, "H_Bli", "Vd1 {Bl}", win=["WINDOW 0 24 40 Left 2", "WINDOW 3 24 72 Left 2"]); s.gnd(mx, 80)
    s.wire(mx, 0, mx + 192, 0)
    x = s.vsense(mx + 192, 0, "Vd2"); s.wire(x, 0, x + 48, 0)
    x = s.hser("ind", x + 48, 0, "L_Mmd", "{Mmd}", g.NOLOSS); s.wire(x, 0, x + 48, 0)
    x = s.hser("res", x + 48, 0, "R_Rms", "{Rms}"); s.wire(x, 0, x + 48, 0)
    x = s.hser("cap", x + 48, 0, "C_Cms", "{Cms}"); s.wire(x, 0, x + 336, 0); x += 336
    pins = s.sym("e", "R0", x, -16, "E_SdpD", "{Sd}", win=["WINDOW 0 24 40 Left 2", "WINDOW 3 24 72 Left 2"])
    s.gnd(*pins[1])
    (cpx, cpy), (cmx, cmy) = pins[2], pins[3]
    s.wire(cpx, cpy, cpx - 64, cpy); s.wire(cpx - 64, cpy, cpx - 64, 160); s.wire(cpx - 64, 160, cpx - 160, 160)
    s.flag(cpx - 160, 160, "pf")
    s.wire(cmx, cmy, cmx - 32, cmy); s.wire(cmx - 32, cmy, cmx - 32, 224); s.wire(cmx - 32, 224, cmx - 160, 224)
    s.flag(cmx - 160, 224, "pb")
    # ---- acoustical loop: p_i -> M_A1 -> [pf] F_U [pb] -> back network
    ay = 560
    s.text(0, ay - 176, "acoustic loop: the diaphragm is F_U, which carries U = S_D*u from the front node pf to the back node pb.  "
                        "p_D = V(pf) - V(pb) is the pressure difference that drives the mechanical loop through E_SdpD")
    s.vsrc(0, ay, "V_pi", "AC 1")
    s.flag(64, ay, "pi"); s.wire(0, ay, 144, ay)
    x = s.hser("ind", 144, ay, "L_MA1", "{MA1}", g.NOLOSS); s.wire(x, ay, x + 160, ay); s.flag(x + 80, ay, "pf"); x += 160
    s.sym("f", "R270", x, ay, "F_U", "Vd2 {-Sd}", win=["WINDOW 0 -56 40 Center 2", "WINDOW 3 40 40 Center 2"])
    x += 80; s.wire(x, ay, x + 160, ay); s.flag(x + 80, ay, "pb"); x += 160
    if "Cab" in net:
        x = s.hser("res", x, ay, "R_Raf", "{Raf}"); s.wire(x, ay, x + 128, ay); x += 128
        s.flag(x - 64, ay, "pc"); s.vshunt("cap", x, ay, "C_Cab", "{Cab}")
        s.text(0, ay + 240, "back network: felt R_AF in series with the back volume C_AB = V/(rho c^2)")
    else:
        s.vshunt("cap", x, ay, "C_Cab1", "{Cab1}"); s.wire(x, ay, x + 176, ay); x += 176
        x = s.hser("res", x, ay, "R_Rat", "{Rat}"); s.wire(x, ay, x + 48, ay)
        x = s.hser("ind", x + 48, ay, "L_Mat", "{Mat}", g.NOLOSS); s.wire(x, ay, x + 160, ay); s.flag(x + 80, ay, "p2"); x += 160
        s.vshunt("cap", x, ay, "C_Cab2", "{Cab2}")
        txt = "back network: small cavity V1 = C_AB1 right behind the diaphragm, damped tube R_AT + M_AT into the large cavity V2 = C_AB2"
        if "Map" in net:
            s.wire(x, ay, x + 176, ay); x += 176
            x = s.hser("res", x, ay, "R_Rap", "{Rap}"); s.wire(x, ay, x + 48, ay)
            x = s.hser("ind", x + 48, ay, "L_Map", "{Map}", g.NOLOSS); s.wire(x, ay, x + 128, ay); s.flag(x + 128, ay, "pi")
            txt += "\nvent: tube R_AP + M_AP from V2 to the OUTSIDE air, i.e. back to the incident pressure node pi (2d)"
        else:
            s.text(0, ay + 304, "R_leak pb 0 1T", directive=True)
        s.text(0, ay + 240, txt)
    s.text(0, ay + 336, ".ac dec 200 10 100k", directive=True)
    if step:
        s.text(0, ay + 376, step, directive=True)
    s.text(0, ay + 424, "plot V(out): with p_i = 1 Pa it reads directly as the sensitivity in V/Pa (dB re 1 V/Pa).  "
                        "velocity u = -I(Vd2), coil current i = -I(Vd1)")
    for k, n in enumerate(notes):
        s.text(0, ay + 456 + 32 * k, n)
    s.dump(HERE / f"{name}.asc")
    g.plt(HERE / f"{name}.plt", [(["V(out)"], (1e-6, 1e-2))], (10, 100000))
    return HERE / f"{name}.asc"


FILES = {
    "P4_2a_Basic": ("Problems 4.2a - dynamic pressure microphone, V = 5 cm3 behind the diaphragm, R_AF = 2e7 Ns/m5", NET_2A, None,
                    ["check: peak 1.64 mV/Pa (-55.7 dB re 1 V/Pa) at f0 = 1.22 kHz, Q = 0.254, -3 dB band 291 Hz - 5.07 kHz"]),
    "P4_2b_Sensitivity": ("Problems 4.2b - sensitivity set by the felt: .step R_AF (0.3 mV/Pa, the 2a value, 3 mV/Pa)", NET_2A,
                          ".step param Raf list 1.2708e8 2e7 9.173e6",
                          ["check: peaks 0.300 mV/Pa (57 Hz - 25.8 kHz), 1.64 mV/Pa, 3.00 mV/Pa (480 Hz - 3.1 kHz): sensitivity x bandwidth stays constant"]),
    "P4_2c_TwoCavities": ("Problems 4.2c - high-frequency extension: back volume split into V1 + V2, joined by a damped tube (official values)", NET_2C, None,
                          ["compare with the 1b/1c design (R_AF = 35.5 Meg, C_AB = 77.5p): the same mid-band, but the roll-off above 5 kHz is pushed up",
                           "R_leak (1T from pb to ground) only gives LTspice a DC path through the two capacitors; it does nothing in the audio band"]),
    "P4_2d_Vent": ("Problems 4.2d - 2c plus a vent tube from the large cavity V2 to the outside (the official compensated microphone)", NET_2D, None,
                   ["check: the official red curve - flat from about 60 Hz to 7 kHz, a small bump near 55 Hz, falls fast below it"]),
}


def build_all():
    return {name: build(name, *spec) for name, spec in FILES.items()}


def split_steps(f):
    """indices where a .step run starts (the frequency axis restarts)"""
    starts = [0] + [j for j in range(1, len(f)) if f[j] < f[j - 1]]
    return list(zip(starts, starts[1:] + [len(f)]))


def band(f, v):
    mag = [abs(x) for x in v]; k = max(range(len(f)), key=lambda j: mag[j]); lim = mag[k] / math.sqrt(2)
    lo = next((f[j] for j in range(k, -1, -1) if mag[j] < lim), float("nan"))
    hi = next((f[j] for j in range(k, len(f)) if mag[j] < lim), float("nan"))
    return mag[k], f[k], lo, hi


def verify(files):
    ok = True
    for name, asc in files.items():
        net = FILES[name][1]
        d = g.run_ltspice(asc); f = [v.real for v in d["frequency"]]; v = d["v(out)"]
        runs = split_steps(f)
        nets = [dict(net, Raf=r) for r in RAF_2B] if len(runs) > 1 else [net]
        for i0, i1 in runs:
            ff, vv = f[i0:i1], v[i0:i1]
            dev = lambda nt: max(abs(vv[j] / sens(nt, ff[j]) - 1) for j in range(len(ff)))
            nt = min(nets, key=dev); worst = dev(nt)          # LTspice does not keep the .step list order
            pk, fpk, lo, hi = band(ff, vv)
            good = worst < 2e-3; ok &= good
            tag = f"{name}" + (f" (R_AF = {nt['Raf']:.4g})" if len(runs) > 1 else "")
            print(f"  {'OK ' if good else 'BAD'} {tag}: worst deviation from the closed form {worst:.1e}; peak {pk*1e3:.3f} mV/Pa "
                  f"({20*math.log10(pk):.2f} dB re 1 V/Pa) at {fpk:.0f} Hz; -3 dB band {lo:.0f} Hz - {hi/1e3:.2f} kHz")
    # the official's uncompensated reference, closed form only
    f = [10 * 10 ** (k / 200) for k in range(801)]
    pk, fpk, lo, hi = band(f, [sens(NET_1C, x) for x in f])
    print(f"  (closed form) 1b/1c design R_AF = 35.5 Meg, C_AB = 77.5p: peak {pk*1e3:.3f} mV/Pa at {fpk:.0f} Hz, band {lo:.0f} Hz - {hi/1e3:.2f} kHz")
    print("ALL OK" if ok else "MISMATCH")
    return ok


if __name__ == "__main__":
    problem1()
    m = MIC; Mmt = m["Mmd"] + Sd ** 2 * m["MA1"]; Cmt = 1 / (1 / m["Cms"] + Sd ** 2 / NET_2A["Cab"])
    Rmt = m["Rms"] + Sd ** 2 * NET_2A["Raf"] + m["Bl"] ** 2 / (m["Re"] + m["Rl"])
    f0 = 1 / (2 * math.pi * math.sqrt(Mmt * Cmt)); Q = 2 * math.pi * f0 * Mmt / Rmt
    print(f"P2a  C_AB = {NET_2A['Cab']:.4g}, C_MT = {Cmt:.4g} m/N, R_MT = {Rmt:.3f} Ns/m -> f0 = {f0:.0f} Hz, Q = {Q:.3f}, "
          f"M = {m['Rl']/(m['Re']+m['Rl'])*m['Bl']*Sd/Rmt*1e3:.3f} mV/Pa")
    files = build_all()
    if "--preview" in sys.argv:
        import preview_asc as pv
        pv.HERE = HERE
        [pv.main(str(p)) for p in files.values()]
    if "--verify" in sys.argv:
        sys.exit(0 if verify(files) else 1)
