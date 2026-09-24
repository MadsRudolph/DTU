#!/usr/bin/env python3
"""34870 Lecture 2 problem solving (mechanical systems): LTspice versions of the problems
in 34870_Solutions2.pdf.

    python3 p2.py            # print the hand results, write the .asc/.plt files
    python3 p2.py --verify   # also run LTspice headless and compare with the closed form
    python3 p2.py --preview  # draw the .asc files to preview/*.png and lint the layout

Problem 2.1  graphical conversion: the sheet's impedance-analogy ladder (velocity source
             u1 || C_M1, then M_M1 + R_M1, R_M2, M_M2, C_M3, M_M3 + R_M3) and its dual in
             the mobility analogy, with the solution's .param values. Every current on one
             side is a voltage on the other: velocities, forces swap between I and V.
Problem 2.2  mass on a spring, M_M = 20 g, k = 1000 N/m (C_M = 1 mm/N), R_M = 0.5 Ns/m,
             driven by 10 N and by 1 m/s, in both analogies (four circuits).
Problem 2.3  the same driver as a source: Thevenin and Norton in both analogies. The
             frequency-dependent equivalent sources (u_No = f/Z_M, u_Th = Y_M f) are
             Laplace-controlled sources; all four give the same load velocity, 20 m/s at
             resonance.
Problem 2.4  two masses coupled by a spring || damper, force-driven, both analogies, with
             the solution's .param values. --verify also runs the five limiting cases.

Conventions: IMPEDANCE analogy = force is a voltage, velocity a current, mass = L,
compliance = C, damper = R. MOBILITY analogy = velocity is a voltage, force a current,
mass = C, compliance = L, damper = resistor 1/R_M.
Needs the Lab A builder: ../../Labs/Lab A/LTspice/gen_ltspice.py (the labs repo).
"""
import math, pathlib, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
LABA = HERE.parents[1] / "Labs" / "Lab A" / "LTspice"
sys.path.insert(0, str(LABA))
import gen_ltspice as g                      # noqa: E402

TINY = "Rser=1u"   # a voltage source in a loop of ideal inductors is an over-defined matrix in LTspice

# ---------------------------------------------------------------- values from the solutions
P21 = dict(u1=2.0, Rm1=1.0, Rm2=2.0, Rm3=3.0, Mm1=10e-3, Cm1=1e-3)
P21.update(Mm2=2.5 * P21["Mm1"], Mm3=4 * P21["Mm1"], Cm2=1.5 * P21["Cm1"], Cm3=P21["Cm1"] * 0.3)
P22 = dict(Mm=20e-3, Cm=1 / 1000, Rm=0.5, F=10.0, U=1.0)
P24 = dict(f=1.0, Rm1=0.3, Mm1=1e-3, Mm2=2e-3, Cm1=10e-3)


def par(*z):
    return 1 / sum(1 / x for x in z)


# =====================================================================  closed forms
def cf21(f):
    """ladder, impedance analogy: returns the three mass velocities and the force on C_M1"""
    s = 2j * math.pi * f; p = P21
    Z4 = s * p["Mm3"] + p["Rm3"]                  # M_M3 + R_M3
    Z3 = par(1 / (s * p["Cm3"]), Z4)              # C_M3 || (M_M3 + R_M3)
    Zb = s * p["Mm2"] + Z3
    Z2 = par(p["Rm2"], Zb)
    Za = s * p["Mm1"] + p["Rm1"] + Z2
    Zin = par(1 / (s * p["Cm1"]), Za)
    f1 = p["u1"] * Zin
    u_M1 = f1 / Za; f2 = u_M1 * Z2; u_M2 = f2 / Zb; f3 = u_M2 * Z3; u_M3 = f3 / Z4
    return dict(f1=f1, u_M1=u_M1, u_M2=u_M2, u_M3=u_M3, fC1=p["u1"] - u_M1)


def cf22(f):
    s = 2j * math.pi * f; p = P22
    Z = p["Rm"] + s * p["Mm"] + 1 / (s * p["Cm"])
    return Z


def cf24(f, p):
    s = 2j * math.pi * f
    Zc = p["Rm1"] + 1 / (s * p["Cm1"])            # spring + damper (same relative velocity)
    Z2 = s * p["Mm2"]
    Zin = s * p["Mm1"] + par(Zc, Z2)
    u1 = p["f"] / Zin
    return u1, u1 * Zc / (Zc + Z2)


def hand():
    p = P22
    w0 = 1 / math.sqrt(p["Mm"] * p["Cm"]); Q = math.sqrt(p["Mm"] / p["Cm"]) / p["Rm"]
    print(f"P2.2 w0 = {w0:.1f} rad/s, f0 = {w0/2/math.pi:.2f} Hz, Q = {Q:.2f}, u(f0) = F/R_M = {p['F']/p['Rm']:.0f} m/s "
          f"({20*math.log10(p['F']/p['Rm']):.1f} dB), force for 1 m/s at f0 = R_M = {p['Rm']} N ({20*math.log10(p['Rm']):.1f} dB)")
    print(f"P2.3 Z_M(w0) = {p['Rm']} kg/s, Y_M(w0) = {1/p['Rm']:.0f} s/kg, u(w0) = 10 N * 2 s/kg = {p['F']/p['Rm']:.0f} m/s")
    p = P24
    fa = 1 / (2 * math.pi * math.sqrt(p["Mm2"] * p["Cm1"]))
    Mr = p["Mm1"] * p["Mm2"] / (p["Mm1"] + p["Mm2"])
    fr = 1 / (2 * math.pi * math.sqrt(Mr * p["Cm1"]))
    print(f"P2.4 u1 dip (M2 on C1, anti-resonance) at {fa:.1f} Hz, coupled resonance (reduced mass {Mr*1e3:.3f} g on C1) at {fr:.1f} Hz undamped (u1 peak lands at ~71 Hz, Q = {math.sqrt(Mr/p['Cm1'])/p['Rm1']:.2f}), "
          f"low f: u = f/(jw(M1+M2)) = {20*math.log10(p['f']/(2*math.pi*1*(p['Mm1']+p['Mm2']))):.1f} dB at 1 Hz")


# =====================================================================  schematics
def build21():
    s = g.Sch()
    s.text(-96, -288, "Problem 2.1 - graphical conversion.  Top: the sheet's circuit in the IMPEDANCE analogy (force = V, velocity = I, mass = L, compliance = C).")
    s.text(-96, -256, "Bottom: its dual in the MOBILITY analogy (velocity = V, force = I, mass = C, compliance = L, damper = 1/R).  Series <-> parallel, V <-> I.")
    s.text(-96, -208, ".param u1=2 Rm1=1 Rm2=2 Rm3=3 Mm1=10m Mm2=2.5*Mm1 Mm3=4*Mm1 Cm1=1m Cm2=1.5*Cm1 Cm3=Cm1*0.3", directive=True)
    # ---- impedance analogy
    s.isrc(0, 0, "I_u1", "AC {u1}"); s.flag(0, 0, "f1")
    s.wire(0, 0, 256, 0)
    s.vshunt("cap", 160, 0, "C1", "{Cm1}")
    x = s.vsense(256, 0, "Vu_M1"); s.wire(x, 0, x + 48, 0)
    x = s.hser("ind", x + 48, 0, "L1", "{Mm1}", g.NOLOSS); s.wire(x, 0, x + 48, 0)
    x = s.hser("res", x + 48, 0, "R1", "{Rm1}"); s.wire(x, 0, x + 96, 0)
    xa = x + 96; s.vshunt("res", xa, 0, "R2", "{Rm2}"); s.flag(xa, 0, "f2")
    s.wire(xa, 0, xa + 96, 0)
    x = s.vsense(xa + 96, 0, "Vu_M2"); s.wire(x, 0, x + 48, 0)
    x = s.hser("ind", x + 48, 0, "L2", "{Mm2}", g.NOLOSS); s.wire(x, 0, x + 96, 0)
    xb = x + 96; s.vshunt("cap", xb, 0, "C3", "{Cm3}"); s.flag(xb, 0, "f3")
    s.wire(xb, 0, xb + 96, 0)
    x = s.vsense(xb + 96, 0, "Vu_M3"); s.wire(x, 0, x + 48, 0)
    x = s.hser("ind", x + 48, 0, "L3", "{Mm3}", g.NOLOSS); s.wire(x, 0, x + 96, 0)
    s.vshunt("res", x + 96, 0, "R3", "{Rm3}"); s.flag(x + 96, 0, "f4")
    s.text(1760, -32, "velocities of the masses:")
    s.text(1760, 0, "I(Vu_M1), I(Vu_M2), I(Vu_M3)")
    # ---- mobility analogy
    y = 480
    s.vsrc(0, y, "V_u1", "AC {u1}"); s.flag(0, y, "u_in")
    s.wire(0, y, 96, y)
    x = s.vsense(96, y, "Vf_C1"); s.wire(x, y, x + 48, y)
    x = s.hser("ind", x + 48, y, "L1x", "{Cm1}", g.NOLOSS); s.wire(x, y, x + 96, y)
    xa = x + 96; s.flag(xa, y, "u_M1")
    s.shunts(xa, y, [("cap", "C1x", "{Mm1}"), ("res", "R1x", "{1/Rm1}")])
    s.wire(xa, y, xa + 320, y)
    x = s.hser("res", xa + 320, y, "R2x", "{1/Rm2}"); s.wire(x, y, x + 96, y)
    xb = x + 96; s.flag(xb, y, "u_M2"); s.vshunt("cap", xb, y, "C2x", "{Mm2}")
    s.wire(xb, y, xb + 96, y)
    x = s.hser("ind", xb + 96, y, "L3x", "{Cm3}", g.NOLOSS); s.wire(x, y, x + 96, y)
    xc = x + 96; s.flag(xc, y, "u_M3")
    s.shunts(xc, y, [("cap", "C3x", "{Mm3}"), ("res", "R3x", "{1/Rm3}")])
    s.wire(xc, y, xc + g.PITCH, y)
    s.text(1760, y - 32, "the same velocities as node voltages:")
    s.text(1760, y, "V(u_M1), V(u_M2), V(u_M3)")
    s.text(-96, 800, ".ac dec 1000 1 10k", directive=True)
    s.text(-96, 848, "Plot I(Vu_M1) with V(u_M1) (and M2, M3): identical.  The force in spring C_M1 is V(f1) on top and I(Vf_C1) below.  (Cm2 is defined on the sheet but not used.)")
    s.dump(HERE / "P2_1_Graphical_Conversion.asc")
    g.plt(HERE / "P2_1_Graphical_Conversion.plt",
          [(["I(Vu_M1)", "V(u_M1)"], (1e-4, 10)), (["I(Vu_M2)", "V(u_M2)", "I(Vu_M3)", "V(u_M3)"], (1e-6, 10))], (1, 10000))
    return HERE / "P2_1_Graphical_Conversion.asc"


def series_rlc(s, x, y, names, vals):
    """R, L, C in a row from (x, y), then down to ground"""
    x = s.hser("res", x, y, names[0], vals[0]); s.wire(x, y, x + 48, y)
    x = s.hser("ind", x + 48, y, names[1], vals[1], g.NOLOSS); s.wire(x, y, x + 48, y)
    x = s.hser("cap", x + 48, y, names[2], vals[2]); s.wire(x, y, x + 48, y)
    s.wire(x + 48, y, x + 48, y + 96); s.gnd(x + 48, y + 96)
    return x + 48


def build22():
    s = g.Sch()
    s.text(-96, -288, "Problem 2.2 - mass on a spring: M_M = 20 g, k = 1000 N/m -> C_M = 1/k = 1 mm/N, R_M = 0.5 Ns/m.  Left: impedance analogy.  Right: mobility analogy.")
    s.text(-96, -256, "Top row: driven by a 10 N force.  Bottom row: driven by a 1 m/s velocity.")
    s.text(-96, -208, ".param Mm=20m Cm=1m Rm=0.5", directive=True)
    # impedance, force source
    s.vsrc(0, 0, "F0", "AC 10"); s.flag(0, 0, "fA")
    s.wire(0, 0, 96, 0)
    x = s.vsense(96, 0, "Vu_A"); s.wire(x, 0, x + 48, 0)
    series_rlc(s, x + 48, 0, ("R1", "L1", "C1"), ("{Rm}", "{Mm}", "{Cm}"))
    s.text(-96, 160, "velocity for 10 N:  I(Vu_A)")
    # impedance, velocity source: the force it needs is the voltage across it
    y = 400
    s.isrc(0, y, "U0", "AC 1"); s.flag(0, y, "fB")
    s.wire(0, y, 96, y)
    series_rlc(s, 96, y, ("R2", "L2", "C2"), ("{Rm}", "{Mm}", "{Cm}"))
    s.text(-96, y + 160, "force for 1 m/s:  V(fB)")
    # mobility, force source
    X = 1120
    s.isrc(X, 0, "F0x", "AC 10"); s.flag(X, 0, "uC")
    s.shunts(X + 160, 0, [("res", "R1x", "{1/Rm}"), ("cap", "C1x", "{Mm}"), ("ind", "L1x", "{Cm}", g.NOLOSS)])
    s.wire(X, 0, X + 160 + 2 * g.PITCH, 0)
    s.text(X - 96, 160, "velocity for 10 N:  V(uC)")
    # mobility, velocity source: the force it delivers is the current out of it
    s.vsrc(X, y, "U0x", "AC 1"); s.flag(X, y, "uD")
    s.wire(X, y, X + 96, y)
    x = s.vsense(X + 96, y, "Vf_D"); s.wire(x, y, x + 64, y)
    s.shunts(x + 64, y, [("res", "R2x", "{1/Rm}"), ("cap", "C2x", "{Mm}"), ("ind", "L2x", "{Cm}", TINY)])
    s.wire(x + 64, y, x + 64 + 2 * g.PITCH, y)
    s.text(X - 96, y + 160, "force for 1 m/s:  I(Vf_D)   (L2x has Rser=1u: an ideal L across a V source is a short at DC)")
    s.text(-96, 720, ".ac dec 1000 1 1k", directive=True)
    s.text(-96, 768, "Force drive: the velocity PEAKS at f0 = 35.6 Hz with F/R_M = 20 m/s (26 dB).  Velocity drive: the force DIPS to R_M * 1 m/s = 0.5 N (-6 dB) at the same f0.")
    s.dump(HERE / "P2_2_Mass_Spring.asc")
    g.plt(HERE / "P2_2_Mass_Spring.plt", [(["I(Vu_A)", "V(fB)", "V(uC)", "I(Vf_D)"], (0.03, 300))], (1, 1000))
    return HERE / "P2_2_Mass_Spring.asc"


def par_net(s, xl, y, r, c, l, labels_c=None):
    """R || C || L between (xl, y) and (xl + 80, y): L on the rail, R above, C below"""
    xr = s.hser("ind", xl, y, l[0], l[1], g.NOLOSS, win=g.WIN_BELOW)
    s.hser("res", xl, y - 128, r[0], r[1], win=g.WIN_ABOVE)
    s.sym("cap", "R90", xl + 72, y + 112, c[0], c[1], win=["WINDOW 0 44 32 VTop 2", "WINDOW 3 72 32 VTop 2"])
    s.wire(xl, y - 128, xl, y + 128); s.wire(xr, y - 128, xr, y + 128)
    s.wire(xl, y + 128, xl + 8, y + 128); s.wire(xl + 72, y + 128, xr, y + 128)
    return xr


def build23():
    s = g.Sch()
    s.text(-96, -352, "Problem 2.3 - the driver of 2.2 as a source, pushed by a 10 N Lorentz force.  Left: impedance analogy.  Right: mobility analogy.")
    s.text(-96, -320, "Top row: force source (Thevenin / Norton), bottom row: the equivalent velocity source.  The load is a damper R_L; RL = 1u is a free cone.")
    s.text(-96, -272, ".param Mm=20m Cm=1m Rm=0.5 F=10 RL=1u", directive=True)
    YM = "Laplace=1/(Rm+s*Mm+1/(s*Cm))"          # 1/Z_M = Y_M, applied to V(fTh) = 10 V
    below = lambda: s.syms.__setitem__(-1, s.syms[-1].replace("WINDOW 3 40 72 Left 2", "WINDOW 3 -16 136 Right 2"))
    # (A) impedance, Thevenin: f_Th in series with Z_M
    s.vsrc(0, 0, "V_fTh", "AC {F}"); s.flag(0, 0, "fTh")
    s.wire(0, 0, 96, 0)
    x = s.hser("res", 96, 0, "R1", "{Rm}"); s.wire(x, 0, x + 48, 0)
    x = s.hser("ind", x + 48, 0, "L1", "{Mm}", g.NOLOSS); s.wire(x, 0, x + 48, 0)
    x = s.hser("cap", x + 48, 0, "C1", "{Cm}"); s.wire(x, 0, x + 64, 0)
    x = s.vsense(x + 64, 0, "Vu_A"); s.wire(x, 0, x + 64, 0)
    s.vshunt("res", x + 64, 0, "R_LA", "{RL}")
    s.text(-96, 176, "(A) Thevenin: f_Th = 10 N in series with Z_M.  u = I(Vu_A)")
    # (B) impedance, Norton: u_No = f_Th / Z_M in parallel with Z_M
    y = 560
    s.g_inject(96, y, "G_uNo", YM, "fTh"); below(); s.flag(96, y, "fB")
    s.wire(96, y, 544, y)
    b = s.vert("res", 320, y, "R2", "{Rm}")
    b = s.vert("ind", b[0], b[1], "L2", "{Mm}", g.NOLOSS)
    s.vshunt("cap", b[0], b[1], "C2", "{Cm}")
    x = s.vsense(544, y, "Vu_B"); s.wire(x, y, x + 64, y)
    s.vshunt("res", x + 64, y, "R_LB", "{RL}")
    s.text(-96, y + 336, "(B) Norton: u_No = f_Th/Z_M (G source, Laplace) in parallel with Z_M.  u = I(Vu_B);  u_No(f0) = 10/0.5 = 20 m/s")
    # (C) mobility, Norton: f_No in parallel with Y_M
    X = 1440
    s.isrc(X, 0, "I_fNo", "AC {F}"); s.flag(X, 0, "uC")
    s.shunts(X + 160, 0, [("res", "R1x", "{1/Rm}"), ("cap", "C1x", "{Mm}"), ("ind", "L1x", "{Cm}", g.NOLOSS), ("res", "R_LC", "{1/RL}")])
    s.wire(X, 0, X + 160 + 3 * g.PITCH, 0)
    s.text(X - 96, 176, "(C) Norton: f_No = 10 N in parallel with Y_M.  u = V(uC)")
    # (D) mobility, Thevenin: u_Th = Y_M f_No in series with Y_M
    s.e_src(X + 96, y, "E_uTh", YM, "fTh"); below(); s.flag(X + 96, y, "uTh")
    s.wire(X + 96, y, X + 224, y)
    x = par_net(s, X + 224, y, ("R2x", "{1/Rm}"), ("C2x", "{Mm}"), ("L2x", "{Cm}"))
    s.wire(x, y, x + 160, y); s.flag(x + 160, y, "uD")
    s.vshunt("res", x + 160, y, "R_LD", "{1/RL}")
    s.text(X - 96, y + 336, "(D) Thevenin: u_Th = Y_M f_No (E source, Laplace) in series with Y_M.  u = V(uD)")
    s.text(-96, 1008, ".ac dec 1000 1 1k", directive=True)
    s.text(-96, 1056, "Plot I(Vu_A), I(Vu_B), V(uC), V(uD) on a LINEAR axis: four identical curves, 20 m/s at f0 = 35.6 Hz.  Change RL: they stay identical.")
    s.dump(HERE / "P2_3_Equivalent_Sources.asc")
    g.plt(HERE / "P2_3_Equivalent_Sources.plt", [(["I(Vu_A)", "I(Vu_B)", "V(uC)", "V(uD)"], (0.03, 30))], (1, 1000))
    return HERE / "P2_3_Equivalent_Sources.asc"


def build24(p=P24, path=None):
    s = g.Sch()
    s.text(-96, -352, "Problem 2.4 - two masses, M1 pushed by the force f, coupled to M2 by a spring C1 || damper R1.")
    s.text(-96, -320, "Top: impedance analogy (the spring and damper share one relative velocity u1 - u2, so they are in SERIES here).  Bottom: mobility analogy.")
    s.text(-96, -272, ".param f={f:g} Rm1={Rm1:g} Mm1={Mm1:g} Mm2={Mm2:g} Cm1={Cm1:g}".format(**p), directive=True)
    s.vsrc(0, 0, "V1", "AC {f}"); s.flag(0, 0, "f_in")
    s.wire(0, 0, 96, 0)
    x = s.vsense(96, 0, "Vu1"); s.wire(x, 0, x + 48, 0)
    x = s.hser("ind", x + 48, 0, "L1", "{Mm1}", TINY); s.wire(x, 0, x + 256, 0)
    b = s.vert("res", x + 128, 0, "R2", "{Rm1}")
    s.vshunt("cap", b[0], b[1], "C1", "{Cm1}")
    x = s.vsense(x + 256, 0, "Vu2"); s.wire(x, 0, x + 96, 0)
    s.vshunt("ind", x + 96, 0, "L2", "{Mm2}", TINY)
    s.text(1024, -32, "u1 = I(Vu1),  u2 = I(Vu2)")
    s.text(1024, 0, "(L1, L2 have Rser=1u: V source + inductor loop)")
    y = 560
    s.isrc(0, y, "I1", "AC {f}"); s.flag(0, y, "u1")
    s.wire(0, y, 400, y)
    s.vshunt("cap", 176, y, "C2", "{Mm1}")
    xr = s.link(400, y, "L3", "{Cm1}", "R1", "{1/Rm1}")
    s.wire(xr, y, xr + 176, y); s.flag(xr + 176, y, "u2")
    s.vshunt("cap", xr + 176, y, "C3", "{Mm2}")
    s.text(1024, y - 32, "u1 = V(u1),  u2 = V(u2)")
    s.text(1024, y, "mass = C to ground, spring || damper = L || 1/R in the link")
    s.text(-96, 800, ".ac dec 1000 1 10k", directive=True)
    s.text(-96, 848, "Plot I(Vu1), I(Vu2), V(u1), V(u2): u1 dips at 1/(2 pi sqrt(Mm2 Cm1)) = 35.6 Hz (M2 on the spring holds M1 still), u1 peaks at 71 Hz (reduced mass M1M2/(M1+M2) on C1 gives 61.6 Hz undamped; Q = 0.86 only, so the peak moves).")
    s.text(-96, 880, "Limiting cases: set Mm1 or Mm2 = 1e6 (infinite mass), Cm1 = 1e-12 (rigid spring), Rm1 = 1e9 (rigid damper), Rm1 = 1e-9 with Cm1 = 1e6 (no coupling) and compare.")
    path = path or HERE / "P2_4_Two_Mass.asc"
    s.dump(path)
    if path.parent == HERE:
        g.plt(HERE / "P2_4_Two_Mass.plt", [(["I(Vu1)", "I(Vu2)", "V(u1)", "V(u2)"], (3e-5, 100))], (1, 10000))
    return path


# =====================================================================  verify
def worst(pairs):
    return max(abs(a / b - 1) for a, b in pairs)


def report(label, w, tol=1e-4):
    print(f"  {'OK ' if w < tol else 'BAD'} {label}: worst deviation {w:.1e}")
    return w < tol


def at(f, fx):
    return min(range(len(f)), key=lambda j: abs(f[j] - fx))


def verify(files):
    ok = True
    # 2.1
    d = g.run_ltspice(files["21"]); f = [x.real for x in d["frequency"]]
    pr = []
    for j, fi in enumerate(f):
        r = cf21(fi)
        pr += [(d["i(vu_m1)"][j], r["u_M1"]), (d["i(vu_m2)"][j], r["u_M2"]), (d["i(vu_m3)"][j], r["u_M3"]),
               (d["v(u_m1)"][j], r["u_M1"]), (d["v(u_m2)"][j], r["u_M2"]), (d["v(u_m3)"][j], r["u_M3"]),
               (d["v(f1)"][j], r["f1"]), (d["i(vf_c1)"][j], r["f1"])]
    ok &= report("2.1 velocities (both analogies) and the spring force vs the ladder formula", worst(pr), 1e-6)
    # 2.2
    d = g.run_ltspice(files["22"]); f = [x.real for x in d["frequency"]]
    pr = []
    for j, fi in enumerate(f):
        Z = cf22(fi)
        pr += [(d["i(vu_a)"][j], 10 / Z), (d["v(uc)"][j], 10 / Z), (d["v(fb)"][j], Z), (d["i(vf_d)"][j], Z)]
    ok &= report("2.2 four circuits vs u = F/Z_M and f = u Z_M (L2x Rser=1u -> 1e-4 at 1 Hz)", worst(pr), 1e-3)
    mag = [abs(x) for x in d["i(vu_a)"]]; jp = max(range(len(f)), key=lambda j: mag[j])
    print(f"      velocity peak {mag[jp]:.3f} m/s ({20*math.log10(mag[jp]):.2f} dB) at {f[jp]:.2f} Hz (sheet: 20 m/s, 35.6 Hz); "
          f"force dip {min(abs(x) for x in d['v(fb)']):.4f} N; u(1 Hz) = {20*math.log10(mag[0]):.1f} dB, f(1 Hz) = {20*math.log10(abs(d['v(fb)'][0])):.1f} dB")
    ok &= abs(mag[jp] - 20) < 0.01 and abs(f[jp] - 35.588) < 0.1
    # 2.3
    d = g.run_ltspice(files["23"]); f = [x.real for x in d["frequency"]]
    pr = []
    for j, fi in enumerate(f):
        u = 10 / (cf22(fi) + 1e-6)
        pr += [(d["i(vu_a)"][j], u), (d["i(vu_b)"][j], u), (d["v(uc)"][j], u), (d["v(ud)"][j], u)]
    ok &= report("2.3 Thevenin/Norton, both analogies, vs u = f/(Z_M + R_L)", worst(pr), 1e-4)
    j0 = at(f, 35.588)
    print(f"      |u| at f0: A {abs(d['i(vu_a)'][j0]):.3f}, B {abs(d['i(vu_b)'][j0]):.3f}, C {abs(d['v(uc)'][j0]):.3f}, D {abs(d['v(ud)'][j0]):.3f} m/s (sheet: 20 m/s)")
    # 2.4 + limiting cases
    cases = [("reference", {}), ("M1 -> inf", dict(Mm1=1e6)), ("M2 -> inf", dict(Mm2=1e6)), ("C1 -> 0", dict(Cm1=1e-12)),
             ("R1 -> inf", dict(Rm1=1e9)), ("R1 -> 0 & C1 -> inf", dict(Rm1=1e-9, Cm1=1e6))]
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="p2_"))
    ref = None
    for k, (name, over) in enumerate(cases):
        p = dict(P24, **over)
        path = files["24"] if not over else build24(p, tmp / f"P2_4_case{k}.asc")
        d = g.run_ltspice(path); f = [x.real for x in d["frequency"]]
        pr = []
        for j, fi in enumerate(f):
            u1, u2 = cf24(fi, p)
            pr += [(d["i(vu1)"][j], u1), (d["v(u1)"][j], u1)]
            if abs(u2) > 1e-12:
                pr += [(d["i(vu2)"][j], u2), (d["v(u2)"][j], u2)]
        w = worst(pr)
        u1db = lambda fx: 20 * math.log10(abs(d["v(u1)"][at(f, fx)]))
        u2db = lambda fx: 20 * math.log10(abs(d["v(u2)"][at(f, fx)]) + 1e-30)
        vals = [u1db(fx) for fx in (10, 35.6, 61.6, 1000)] + [u2db(fx) for fx in (10, 35.6, 61.6, 1000)]
        if ref is None:
            ref = vals
            jd = min((j for j in range(len(f)) if 20 < f[j] < 50), key=lambda j: abs(d["v(u1)"][j]))
            jq = max((j for j in range(len(f)) if 45 < f[j] < 100), key=lambda j: abs(d["v(u1)"][j]))
            print(f"      2.4 reference: u1 dip at {f[jd]:.1f} Hz, u1 peak at {f[jq]:.1f} Hz, u1(1 Hz) = {20*math.log10(abs(d['v(u1)'][0])):.1f} dB")
        ok &= report(f"2.4 {name}: both analogies vs closed form (Rser=1u in L1, L2)", w, 1e-3)
        print("        dB at 10/35.6/61.6/1000 Hz   u1: " + " ".join(f"{v:7.1f}" for v in vals[:4]) +
              "   u2: " + " ".join(f"{v:7.1f}" if v > -400 else "   -inf" for v in vals[4:]))
    print("ALL OK" if ok else "MISMATCH")
    return ok


if __name__ == "__main__":
    hand()
    files = {"21": build21(), "22": build22(), "23": build23(), "24": build24()}
    if "--preview" in sys.argv:
        import preview_asc as pv
        pv.HERE = HERE
        [pv.main(str(p)) for p in files.values()]
    if "--verify" in sys.argv:
        sys.exit(0 if verify(files) else 1)
