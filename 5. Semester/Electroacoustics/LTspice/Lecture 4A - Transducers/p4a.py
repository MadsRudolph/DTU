#!/usr/bin/env python3
"""34870 Lecture 4A problem solving (transducers): LTspice circuits for Problems
4.1 (bass-reflex box) and 4.4 a-c (piston + box, voice coil, both combined), each
4.4 part drawn in BOTH analogies on one sheet so they can be compared directly.

    python3 p4a.py            # print the hand numbers, write the .asc/.plt files
    python3 p4a.py --verify   # also run LTspice headless and compare with the closed form
    python3 p4a.py --preview  # draw the .asc files to preview/*.png and lint the layout

Conventions (as in the official solution, 34870_Solutions4A):
  acoustic side  IMPEDANCE analogy: pressure = voltage, volume velocity = current.
  The piston is a volume-velocity source U = S*u that sits BETWEEN the front node
  pf and the back node pb, so V(pf) - V(pb) = p is the pressure difference that
  pushes back on the piston. Front radiation Z_ar from pf to ground, the back
  chain (tube, box, vent) from pb to ground.
  mechanical side, impedance analogy: force = voltage, velocity = current
     (mass = L, compliance = C, damper = R, all in series; couplings E + F, H + H).
  mechanical side, mobility analogy: velocity = voltage, force = current
     (mass = C to ground, compliance = L, damper = R of 1/R_M; couplings G + G, E + F).
Needs the Lab A builder: ../../Labs/Lab A/LTspice/gen_ltspice.py (the labs repo).
"""
import cmath, math, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
LABA = HERE.parents[1] / "Labs" / "Lab A" / "LTspice"
sys.path.insert(0, str(LABA))
import gen_ltspice as g                      # noqa: E402

g.PINS["h"] = [(0, 16), (0, 96)]
BY = 320                                     # the back rail pb sits this far below the front rail pf


# =====================================================================  numbers
def rad(rho, c, a):
    """baffled-piston radiation network (lecture 3): M_A1 || [R_A2 + (R_A1 || C_A1)]"""
    S = math.pi * a ** 2
    return dict(Ma1=8 * rho / (3 * math.pi ** 2 * a), Ra1=0.441 * rho * c / S, Ra2=rho * c / S, Ca1=5.94 * a ** 3 / (rho * c ** 2))


def zar(r, jw):
    return 1 / (1 / (jw * r["Ma1"]) + 1 / (r["Ra2"] + 1 / (1 / r["Ra1"] + jw * r["Ca1"])))


# 4.1: the lecture-3 box (vent 12 cm x 10 cm, 23 L), massless piston as big as the vent
P41 = dict(rho=1.18, c=344.0, a=0.05, l=0.12, V=0.023)
P41["S"] = math.pi * P41["a"] ** 2
P41["Ma"] = P41["rho"] * P41["l"] / P41["S"]
P41["Ca"] = P41["V"] / (P41["rho"] * P41["c"] ** 2)
R41 = rad(P41["rho"], P41["c"], P41["a"])

# 4.4: the official .params (rho = 1.2, c = 343)
P44 = dict(rho=1.2, c=343.0, S=0.01, Mmp=0.02, V=0.04, d=0.02, Re=5.0, Le=0.3e-3, Mm=10e-3, Cm=1e-3, Rm=2.0, l=3.0, B=0.7)
P44["a"] = math.sqrt(P44["S"] / math.pi)
P44["Ma"] = P44["rho"] * P44["d"] / P44["S"]
P44["Ca"] = P44["V"] / (P44["rho"] * P44["c"] ** 2)
P44["Bl"] = P44["l"] * P44["B"]
R44 = rad(P44["rho"], P44["c"], P44["a"])


def za_41(f):
    """acoustic impedance seen by the piston: front Z_ar + (C_A || (M_A + Z_ar))"""
    jw = 2j * math.pi * f; z = zar(R41, jw)
    zb = 1 / (jw * P41["Ca"] + 1 / (jw * P41["Ma"] + z))
    return z + zb, z, zb


def zm_44a(f):
    """mechanical impedance of the baffled piston with tube d and box V on the back"""
    p = P44; jw = 2j * math.pi * f
    return jw * p["Mmp"] + p["S"] ** 2 * (zar(R44, jw) + jw * (p["Ma"] + R44["Ma1"]) + 1 / (jw * p["Ca"]))


def zm_coil(f):
    p = P44; jw = 2j * math.pi * f
    return jw * p["Mm"] + p["Rm"] + 1 / (jw * p["Cm"])


def ze_44(f, with_piston):
    p = P44; jw = 2j * math.pi * f
    zm = zm_coil(f) + (zm_44a(f) if with_piston else 0)
    return p["Re"] + jw * p["Le"] + p["Bl"] ** 2 / zm


def hand():
    p = P41
    print(f"4.1  S = {p['S']:.4g} m2, M_A = {p['Ma']:.2f} kg/m4, C_A = {p['Ca']:.4g} m5/N, f_B = {1/(2*math.pi*math.sqrt(p['Ma']*p['Ca'])):.1f} Hz"
          f" (vent mass only), {1/(2*math.pi*math.sqrt((p['Ma']+R41['Ma1'])*p['Ca'])):.1f} Hz with the outer radiation mass M_A1 = {R41['Ma1']:.2f}")
    p = P44
    print(f"4.4a a = {p['a']*100:.2f} cm, M_A1 = {R44['Ma1']:.3f}, M_A = rho d/S = {p['Ma']:.3f} kg/m4, C_A = {p['Ca']:.4g} m5/N; "
          f"moving mass {1e3*(p['Mmp']+p['S']**2*(2*R44['Ma1']+p['Ma'])):.2f} g on C_A/S^2 = {p['Ca']/p['S']**2*1e3:.3f} mm/N")
    print(f"4.4b Bl = {p['Bl']:.2f} Tm, f_0 = {1/(2*math.pi*math.sqrt(p['Mm']*p['Cm'])):.2f} Hz, |Z_E| peak ~ R_E + (Bl)^2/R_M = {p['Re']+p['Bl']**2/p['Rm']:.3f} ohm")


# =====================================================================  drawing helpers
def ctrl_leads(s, pins, names, dx=-64):
    """short leads from the two control pins of an E/G symbol to named flags"""
    for (cx, cy), n in zip(pins, names):
        s.wire(cx, cy, cx + dx, cy); s.flag(cx + dx, cy, n)


def float_g(s, x, y, name, gain, ctrl):
    """VCCS between pb (bottom, y+BY) and pf (top, y): pushes gain*V(ctrl) from pb into pf"""
    pins = s.sym("g", "R0", x, y - 16, name, gain)
    s.wire(pins[0][0], pins[0][1], x, y + BY)
    ctrl_leads(s, [pins[2]], [ctrl]); s.gnd(*pins[3])


def float_f(s, x, y, name, vsense, gain):
    """CCCS between pb (bottom) and pf (top): pushes gain*I(vsense) from pb into pf"""
    s.sym("f", "R180", x, y + 80, name, f"{vsense} {gain}")
    s.wire(x, y + 80, x, y + BY)


def e_diff(s, x, y, name, gain, cp, cn):
    """VCVS from the rail (x, y) to ground, value gain*(V(cp) - V(cn))"""
    pins = s.sym("e", "R0", x, y - 16, name, gain)
    s.gnd(*pins[1])
    (px, py), (nx, ny) = pins[2], pins[3]     # leads go down and out to the left, clear of the rail
    s.wire(px, py, px - 96, py); s.wire(px - 96, py, px - 96, py + 144); s.wire(px - 96, py + 144, px - 160, py + 144)
    s.flag(px - 160, py + 144, cp)
    s.wire(nx, ny, nx - 48, ny); s.wire(nx - 48, ny, nx - 48, ny + 160); s.wire(nx - 48, ny + 160, nx - 160, ny + 160)
    s.flag(nx - 160, ny + 160, cn)


def g_draw_diff(s, x, y, name, gain, cp, cn):
    """VCCS drawing gain*(V(cp) - V(cn)) out of the node (x, y) to ground (reaction force)"""
    pins = s.sym("g", "R180", x, y + 96, name, gain)
    s.gnd(*pins[1])
    ctrl_leads(s, [pins[2], pins[3]], [cp, cn], dx=64)


def zar_shunt(s, x, y, sfx, pre=""):
    """baffled-piston radiation impedance from the rail (x, y) to ground; returns the right end x"""
    s.vshunt("ind", x, y, f"L_Ma1{sfx}", "{%sMa1}" % pre, g.NOLOSS)
    xr = x + g.PITCH + 32
    s.radnet(xr, y, (f"R_Ra2{sfx}", "{%sRa2}" % pre), (f"R_Ra1{sfx}", "{%sRa1}" % pre), (f"C_Ca1{sfx}", "{%sCa1}" % pre))
    return xr


def acoustic_44(s, x, y, sfx):
    """front: Z_ar on pf.  back: tube (M_A + end correction M_A1) in series, then the box C_A to ground"""
    s.flag(x + 96, y, f"pf{sfx}"); s.flag(x + 96, y + BY, f"pb{sfx}")
    xr = zar_shunt(s, x + 224, y, f"f{sfx}")
    s.wire(x, y, xr, y)
    yb = y + BY
    xm = s.hser("ind", x + 176, yb, f"L_MaMa1{sfx}", "{Ma+Ma1}", g.NOLOSS)
    s.wire(x, yb, x + 176, yb); s.wire(xm, yb, xm + 96, yb)
    s.vshunt("cap", xm + 96, yb, f"C_Ca{sfx}", "{Ca}")


def acoustic_41(s, x, y):
    """front: Z_ar on pf.  back: box C_A to ground and the vent M_A -> its own outer Z_ar"""
    s.flag(x + 96, y, "pf"); s.flag(x + 96, y + BY, "pb")
    xr = zar_shunt(s, x + 224, y, "_f")
    s.wire(x, y, xr, y)
    yb = y + BY
    s.vshunt("cap", x + 224, yb, "C_Ca", "{Ca}")
    xm = s.hser("ind", x + 336, yb, "L_Ma", "{Ma}", g.NOLOSS)
    s.flag(xm + 64, yb, "pv")
    xr = zar_shunt(s, xm + 144, yb, "_v")
    s.wire(x, yb, x + 336, yb); s.wire(xm, yb, xr, yb)


# =====================================================================  4.1
def build_41():
    s = g.Sch(); p = P41
    s.text(0, -352, "Problem 4.1 - bass-reflex box (lecture-3 box: vent 12 cm long, 10 cm diameter, 23 L) driven by a massless baffled piston of the vent's size")
    s.text(0, -320, "mechanical MOBILITY (V_u = velocity u = 1 m/s), acoustic IMPEDANCE.  G1 pushes U = S*u from the back node pb into the front node pf")
    s.text(0, -272, f".param rho={p['rho']} c={p['c']:g} a={p['a']} l={p['l']} V={p['V']} S={{pi*a**2}}", directive=True)
    s.text(0, -240, ".param Ma={rho*l/S} Ca={V/(rho*c**2)} Ma1={8*rho/(3*pi**2*a)} Ra1={0.441*rho*c/S} Ra2={rho*c/S} Ca1={5.94*a**3/(rho*c**2)}", directive=True)
    s.vsrc(0, 0, "V_u")
    s.flag(64, 0, "u"); s.wire(0, 0, 320, 0)
    g_draw_diff(s, 320, 0, "G2", "{S}", "pf", "pb")
    s.text(256, 208, "G2: f = S*p (reaction force;")
    s.text(256, 240, "no effect, u is imposed)")
    float_g(s, 704, 0, "G1", "{S}", "u")
    acoustic_41(s, 704, 0)
    s.text(0, 640, ".ac dec 2000 10 20k", directive=True)
    s.text(0, 688, "c) Z_A = p/U seen by the piston: plot (V(pf)-V(pb))/I(G1).  Peak (box-vent anti-resonance) near 79 Hz, not 92 Hz: the vent's outer radiation mass adds to M_A")
    s.text(0, 720, "front pressure V(pf), box pressure V(pb), vent mouth V(pv).  Vent volume velocity = V(pv) through the outer Z_ar;  official: Z_A,max = 995e3 Pa s/m^3")
    s.dump(HERE / "P4-1_BassReflex_Box.asc")
    g.plt(HERE / "P4-1_BassReflex_Box.plt", [(["(V(pf)-V(pb))/I(G1)"], (1e2, 1e7)), (["V(pf)", "V(pb)"], (1e-2, 1e4))], (10, 20000))
    return HERE / "P4-1_BassReflex_Box.asc"


# =====================================================================  4.4
def params_44(s, y, parts):
    p = P44
    s.text(0, y, f".param rho={p['rho']} c={p['c']:g} S={p['S']} Mmp={p['Mmp']} V={p['V']} d={p['d']} a={{sqrt(S/pi)}}", directive=True)
    s.text(0, y + 32, ".param Ma={rho*d/S} Ca={V/(rho*c**2)} Ma1={8*rho/(3*pi**2*a)} Ra1={0.441*rho*c/S} Ra2={rho*c/S} Ca1={5.94*a**3/(rho*c**2)}", directive=True)
    if "coil" in parts:
        s.text(0, y + 64, f".param Re={p['Re']} Le={p['Le']} Mm={p['Mm']} Cm={p['Cm']} Rm={p['Rm']} l={p['l']} B={p['B']} Bl={{l*B}}", directive=True)


def elec_imp(s, y, sfx, hcol):
    """impedance analogy, electrical loop: i -> R_E -> L_E -> H_emf = Bl*u (u = I(Vu))"""
    s.isrc(0, y, f"I_i{sfx}")
    s.flag(0, y, f"v{sfx}"); s.wire(0, y, 96, y)
    x = s.vsense(96, y, f"Vi{sfx}"); s.wire(x, y, x + 48, y)
    x = s.hser("res", x + 48, y, f"R_Re{sfx}", "{Re}"); s.wire(x, y, x + 48, y)
    x = s.hser("ind", x + 48, y, f"L_Le{sfx}", "{Le}", g.NOLOSS); s.wire(x, y, hcol, y)
    s.sym("h", "R0", hcol, y - 16, f"H_emf{sfx}", f"Vu{sfx} {{Bl}}", win=["WINDOW 0 24 40 Left 2", "WINDOW 3 24 72 Left 2"]); s.gnd(hcol, y + 80)


def elec_mob(s, y, sfx, ecol):
    """mobility analogy, electrical loop: i -> R_E -> L_E -> E_emf = Bl*V(u)"""
    s.isrc(0, y, f"I_i{sfx}")
    s.flag(0, y, f"v{sfx}"); s.wire(0, y, 96, y)
    x = s.vsense(96, y, f"Vi{sfx}"); s.wire(x, y, x + 48, y)
    x = s.hser("res", x + 48, y, f"R_Re{sfx}", "{Re}"); s.wire(x, y, x + 48, y)
    x = s.hser("ind", x + 48, y, f"L_Le{sfx}", "{Le}", g.NOLOSS); s.wire(x, y, ecol, y)
    s.e_src(ecol, y, f"E_emf{sfx}", "{Bl}", f"u{sfx}")


def build_44(part):
    """part 'a': piston + box, 'b': voice coil, 'c': coil rigidly on the piston"""
    s = g.Sch()
    names = {"a": "P4-4a_Piston_Box", "b": "P4-4b_Voice_Coil", "c": "P4-4c_Coil_on_Piston"}
    titles = {"a": "Problem 4.4a - Problem 4.2 in LTspice: baffled piston (S = 100 cm^2, 20 g), 2 cm thick baffle (tube d), 40 L box on the back",
              "b": "Problem 4.4b - Problem 4.3 in LTspice: voice coil on a suspension (l = 3 m, B = 0.7 T, 10 g, 1 mm/N, 2 Ns/m, 5 ohm, 0.3 mH)",
              "c": "Problem 4.4c - coil of b) rigidly glued to the piston of a): same velocity, so the mechanical impedances add"}
    s.text(0, -416, titles[part])
    s.text(0, -384, "TOP: mechanical IMPEDANCE analogy (force = voltage, velocity = current).   BOTTOM: mechanical MOBILITY analogy (velocity = voltage, force = current)")
    params_44(s, -336, "coil" if part in "bc" else "")
    yi, ym = 0, 832
    s.text(0, yi - 112, "impedance analogy")
    s.text(0, ym - 112, "mobility analogy")
    ac_x = None
    # ---------------- impedance analogy (top)
    if part == "a":
        s.isrc(0, yi, "I_u"); s.flag(0, yi, "f"); s.wire(0, yi, 96, yi)
        x = s.vsense(96, yi, "Vu"); s.wire(x, yi, x + 48, yi)
        x = s.hser("ind", x + 48, yi, "L_Mmp", "{Mmp}", g.NOLOSS); s.wire(x, yi, x + 256, yi)
        e_diff(s, x + 256, yi, "E_Sp", "{S}", "pf", "pb")
        ac_x = 1024
        float_f(s, ac_x, yi, "F_Su", "Vu", "{S}")
        acoustic_44(s, ac_x, yi, "")
    else:
        hcol = 720
        elec_imp(s, yi, "", hcol)
        mx = hcol + 400
        s.sym("h", "R0", mx, yi - 16, "H_Bli", "Vi {Bl}", win=["WINDOW 0 24 40 Left 2", "WINDOW 3 24 72 Left 2"]); s.gnd(mx, yi + 80)
        s.wire(mx, yi, mx + 96, yi); s.flag(mx + 64, yi, "fBl")
        x = s.vsense(mx + 96, yi, "Vu"); s.wire(x, yi, x + 48, yi); s.flag(x + 24, yi, "m1")
        x = s.hser("ind", x + 48, yi, "L_Mm", "{Mm}", g.NOLOSS); s.wire(x, yi, x + 48, yi); s.flag(x + 24, yi, "m2")
        x = s.hser("cap", x + 48, yi, "C_Cm", "{Cm}"); s.wire(x, yi, x + 48, yi); s.flag(x + 24, yi, "m3")
        x = s.hser("res", x + 48, yi, "R_Rm", "{Rm}")
        if part == "b":
            s.wire(x, yi, x + 48, yi); s.gnd(x + 48, yi + 16); s.wire(x + 48, yi, x + 48, yi + 16)
        else:
            s.wire(x, yi, x + 48, yi)
            x = s.hser("ind", x + 48, yi, "L_Mmp", "{Mmp}", g.NOLOSS); s.wire(x, yi, x + 256, yi)
            e_diff(s, x + 256, yi, "E_Sp", "{S}", "pf", "pb")
            ac_x = 2784
            float_f(s, ac_x, yi, "F_Su", "Vu", "{S}")
            acoustic_44(s, ac_x, yi, "")
    # ---------------- mobility analogy (bottom)
    if part == "a":
        s.isrc(0, ym, "I_f"); s.flag(80, ym, "u_m")
        s.vshunt("cap", 208, ym, "C_Mmp_m", "{Mmp}")
        s.wire(0, ym, 560, ym)
        g_draw_diff(s, 560, ym, "G_Sp", "{S}", "pf_m", "pb_m")
        float_g(s, ac_x, ym, "G_Su", "{S}", "u_m")
        acoustic_44(s, ac_x, ym, "_m")
    else:
        ecol = 720
        elec_mob(s, ym, "_m", ecol)
        mx = ecol + 400
        s.f_inject(mx, ym, "F_Bli", "Vi_m", "{Bl}")
        s.flag(mx + 80, ym, "u_m")
        items = [("cap", "C_Mm_m", "{Mm}"), ("ind", "L_Cm_m", "{Cm}", g.NOLOSS), ("res", "R_Rm_m", "{1/Rm}")]
        if part == "c":
            items.append(("cap", "C_Mmp_m", "{Mmp}"))
        end = s.shunts(mx + 176, ym, items)
        if part == "c":
            end += 336
            g_draw_diff(s, end, ym, "G_Sp", "{S}", "pf_m", "pb_m")
            float_g(s, ac_x, ym, "G_Su", "{S}", "u_m")
            acoustic_44(s, ac_x, ym, "_m")
        s.wire(mx, ym, end, ym)
    # ---------------- analysis + what to plot
    yt = ym + BY + 256
    s.text(0, yt, ".ac dec 10000 1 20k", directive=True)
    if part == "a":
        s.text(0, yt + 48, "a) f/u: 1 m/s drives the top circuit, so V(f) = Z_M;  1 N drives the bottom one, so 1/V(u_m) = Z_M.  The two curves must lie on top of each other.")
        s.text(0, yt + 80, "Z_M = j w Mmp + S^2 [Z_ar + j w (Ma + Ma1) + 1/(j w Ca)]:  sharp minimum at 20.4 Hz (official: 20.4 Hz), then mass line.  I(Vu) = u, V(pf)-V(pb) = p")
        panes = [(["V(f)", "1/V(u_m)"], (1e-4, 1e4))]
    else:
        s.text(0, yt + 48, "Z_E = v/i with i = 1 A: plot V(v) (impedance analogy) and V(v_m) (mobility analogy); they must be identical.  Velocity u = I(Vu) = V(u_m)")
        if part == "b":
            s.text(0, yt + 80, "forces: coil mass V(m1)-V(m2), suspension spring V(m2)-V(m3), damper V(m3); they add up to V(fBl) = Bl*i.  Official: peak 7.2 ohm at 51 Hz")
        else:
            s.text(0, yt + 80, "the heavier, softer system moves the motional peak down to 33 Hz (official: 33.0 Hz, 7.2 ohm).  Compare with V(v) of P4-4b_Voice_Coil.asc")
        panes = [(["V(v)", "V(v_m)"], (1, 100)), (["I(Vu)", "V(u_m)"], (1e-5, 1))]
    s.dump(HERE / f"{names[part]}.asc")
    g.plt(HERE / f"{names[part]}.plt", panes, (1, 20000))
    return HERE / f"{names[part]}.asc"


# =====================================================================  verify
def verify(files):
    ok = True

    def dev(label, worst, tol=1e-3):
        nonlocal ok
        good = worst < tol; ok &= good
        print(f"  {'OK ' if good else 'BAD'} {label}: {worst:.1e}")

    def chk(label, got, want, tol):
        nonlocal ok
        good = abs(got - want) <= tol * abs(want); ok &= good
        print(f"  {'OK ' if good else 'BAD'} {label}: {got:.5g} (expected {want:.5g})")

    def ext(f, y, lo, hi, kind):
        idx = [j for j in range(len(f)) if lo <= f[j] <= hi]
        j = (max if kind == "max" else min)(idx, key=lambda k: abs(y[k]))
        return f[j], abs(y[j])

    print("4.1 bass-reflex box")
    d = g.run_ltspice(files["41"]); f = [v.real for v in d["frequency"]]
    za = [(d["v(pf)"][j] - d["v(pb)"][j]) / d["i(g1)"][j] for j in range(len(f))]
    dev("Z_A vs closed form Z_ar + (C_A || (M_A + Z_ar))", max(abs(za[j] / za_41(f[j])[0] - 1) for j in range(len(f))))
    dev("front pressure V(pf) vs Z_ar*S*u", max(abs(d["v(pf)"][j] / (za_41(f[j])[1] * P41["S"]) - 1) for j in range(len(f))))
    fr, zmax = ext(f, za, 30, 300, "max")
    print(f"      Z_A peak {zmax:.4g} Pa s/m^3 at {fr:.2f} Hz on this sweep (official: 995e3, 'not 995 kOhm')")
    fx = [10 * 10 ** (k / 200000) for k in range(int(200000 * math.log10(30)) + 1)]
    zx = max(fx, key=lambda q: abs(za_41(q)[0]))
    print(f"      closed form on a very fine grid: {abs(za_41(zx)[0]):.4g} at {zx:.3f} Hz")
    for part, key in (("a", "4a"), ("b", "4b"), ("c", "4c")):
        print(f"4.4{part}")
        d = g.run_ltspice(files[key]); f = [v.real for v in d["frequency"]]
        if part == "a":
            zi = d["v(f)"]; zm = [1 / v for v in d["v(u_m)"]]
            dev("impedance analogy vs closed form", max(abs(zi[j] / zm_44a(f[j]) - 1) for j in range(len(f))))
            dev("mobility analogy vs impedance analogy", max(abs(zm[j] / zi[j] - 1) for j in range(len(f))))
            fr, zmin = ext(f, zi, 5, 100, "min")
            chk("minimum of |f/u| Hz (official 20.4)", fr, 20.4, 5e-3)
            print(f"      |Z_M| at the minimum = {zmin:.3g} Ns/m = {20*math.log10(zmin):.1f} dB (official marker: -40.5 dB)")
        else:
            wp = part == "c"
            dev("impedance analogy vs closed form", max(abs(d["v(v)"][j] / ze_44(f[j], wp) - 1) for j in range(len(f))))
            dev("mobility analogy vs impedance analogy", max(abs(d["v(v_m)"][j] / d["v(v)"][j] - 1) for j in range(len(f))))
            dev("velocity I(Vu) vs V(u_m)", max(abs(d["v(u_m)"][j] / d["i(vu)"][j] - 1) for j in range(len(f))))
            fr, zpk = ext(f, d["v(v)"], 10, 200, "max")
            chk("motional peak Hz (official %s)" % ("51" if part == "b" else "33.0"), fr, 50.2 if part == "b" else 33.0, 1e-2)
            chk("motional peak ohm (official 7.2)", zpk, 7.2, 2e-3)
            if part == "b":
                j = min(range(len(f)), key=lambda k: abs(f[k] - 50))
                tot = (d["v(m1)"][j] - d["v(m2)"][j]) + (d["v(m2)"][j] - d["v(m3)"][j]) + d["v(m3)"][j]
                dev("forces at 50 Hz add up to Bl*i", abs(tot / d["v(fbl)"][j] - 1))
    print("ALL OK" if ok else "MISMATCH")
    return ok


if __name__ == "__main__":
    hand()
    files = {"41": build_41(), "4a": build_44("a"), "4b": build_44("b"), "4c": build_44("c")}
    if "--preview" in sys.argv:
        import preview_asc as pv
        pv.HERE = HERE
        [pv.main(str(p)) for p in files.values()]
    if "--verify" in sys.argv:
        sys.exit(0 if verify(files) else 1)
