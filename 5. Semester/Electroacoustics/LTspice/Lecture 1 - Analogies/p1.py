#!/usr/bin/env python3
"""34870 Lecture 1 problem solving (analogies, introduction): LTspice versions of the
three problems in 34870_Solutions1.pdf.

    python3 p1.py            # print the hand results, write the .asc/.plt files
    python3 p1.py --verify   # also run LTspice headless and compare with the closed form
    python3 p1.py --preview  # draw the .asc files to preview/*.png and lint the layout

Problem 1.1  DC duality: V1 = 10 V, R1 = 100, R2 = 2k, R3 = 500 (.op) and its dual,
             I1 = 10 A, "G1" = 10m, "G2" = 0.5m, "G3" = 2m. LTspice only knows
             resistances, so the dual's conductances are typed in as resistor values:
             the numbers stay, the units swap (V <-> A).
Problem 1.2  AC duality: V1 (AC 2) - L1 1m - (C3 2u || L2 4m), dual I1 (AC 2) || C1 1m -
             L3 2u - C2 4m. The sheet's warning is about LTspice's default Rser = 1 mOhm
             in every inductor. It is kept here on L1 and L2 (a V source + inductor loop
             needs it anyway), and its exact dual, Rpar = 1/1m = 1 kOhm, is put on C1
             and C2. Then V(vout) and I(C2) are the same curve to every digit.
Problem 1.3  series resonator R = 10, L = 10m, C = 2u driven by AC 1, plus the
             mechanical and the acoustical resonator with the same numbers (impedance
             analogy: mass = L, compliance = C, damper = R).
Needs the Lab A builder: ../../Labs/Lab A/LTspice/gen_ltspice.py (the labs repo).
"""
import cmath, math, pathlib, struct, sys

HERE = pathlib.Path(__file__).resolve().parent
LABA = HERE.parents[1] / "Labs" / "Lab A" / "LTspice"
sys.path.insert(0, str(LABA))
import gen_ltspice as g                      # noqa: E402


def read_raw(path):
    """Lab A's reader only knows complex (.ac) raw files. The .op of problem 1.1 writes a
    real one: first variable as double, the rest as float32."""
    b = path.read_bytes(); key = "Binary:\n".encode("utf-16le"); i = b.find(key)
    head = b[:i].decode("utf-16le"); data = b[i + len(key):]
    if "Flags:" not in head:
        raise SystemExit(f"LTspice wrote no data for {path.name} (see its .log)")
    cplx = "complex" in head.split("Flags:")[1].splitlines()[0]
    names, invars, npts = [], False, 0
    for ln in head.splitlines():
        if ln.startswith("No. Points:"): npts = int(ln.split(":")[1])
        if ln.startswith("Variables:"): invars = True; continue
        if invars and ln.strip(): names.append(ln.split()[1].lower())
    nv = len(names); cols = {n: [] for n in names}
    if cplx:
        vals = struct.unpack(f"<{npts*nv*2}d", data[:npts * nv * 16])
        for p in range(npts):
            for v, n in enumerate(names):
                k = 2 * (p * nv + v); cols[n].append(complex(vals[k], vals[k + 1]))
    else:
        rec = 8 + 4 * (nv - 1)
        for p in range(npts):
            r = data[p * rec:(p + 1) * rec]
            cols[names[0]].append(struct.unpack("<d", r[:8])[0])
            for v, x in enumerate(struct.unpack(f"<{nv-1}f", r[8:])):
                cols[names[v + 1]].append(x)
    return cols


g.read_raw = read_raw                        # run_ltspice looks the reader up at call time

# ---------------------------------------------------------------- values from the sheet
P11 = dict(V1=10.0, R1=100.0, R2=2e3, R3=500.0)
P12 = dict(V=2.0, L1=1e-3, C3=2e-6, L2=4e-3, Rser=1e-3)
P13 = dict(R=10.0, L=10e-3, C=2e-6, V=1.0)


# =====================================================================  closed forms
def p11():
    v0, Z1, Z2, Z3 = P11["V1"], P11["R1"], P11["R2"], P11["R3"]
    v3 = v0 * Z2 * Z3 / (Z1 * (Z2 + Z3) + Z2 * Z3)
    i1 = (v0 - v3) / Z1
    return dict(i1=i1, v1=v0 - v3, v3=v3, i2=v3 / Z2, i3=v3 / Z3)


def p12(f):
    s = 2j * math.pi * f; p = P12; r = p["Rser"]
    ZL1, ZL2, ZC3 = s * p["L1"] + r, s * p["L2"] + r, 1 / (s * p["C3"])
    Zp = 1 / (1 / ZC3 + 1 / ZL2)
    return p["V"] * Zp / (ZL1 + Zp)          # = V(vout) = I(C2) of the dual


def p13(f):
    s = 2j * math.pi * f; p = P13
    Z = p["R"] + s * p["L"] + 1 / (s * p["C"])
    return Z, p["V"] / Z


def hand():
    r = p11()
    print(f"P1.1 i1 = {r['i1']*1e3:.2f} mA, v1 = {r['v1']:.2f} V, v3 = {r['v3']:.2f} V, i2 = {r['i2']*1e3:.2f} mA, i3 = {r['i3']*1e3:.2f} mA"
          f"   (dual: v = {r['i1']*1e3:.0f} mV, {r['i3']*1e3:.0f} mV; i = {r['v1']:.0f} A, {r['v3']:.0f} A)")
    p = P12
    f0 = math.sqrt((1 + p["L1"] / p["L2"]) / (p["L1"] * p["C3"])) / (2 * math.pi)
    lf = p["V"] * p["L2"] / (p["L1"] + p["L2"])
    print(f"P1.2 low-frequency level = 2*L2/(L1+L2) = {lf:.2f} V = {20*math.log10(lf):.2f} dB, resonance = {f0:.1f} Hz")
    p = P13
    w0 = 1 / math.sqrt(p["L"] * p["C"]); Q = math.sqrt(p["L"] / p["C"]) / p["R"]
    print(f"P1.3 f0 = {w0/2/math.pi:.2f} Hz, i_max = {p['V']/p['R']*1e3:.0f} mA, Z_min = {p['R']:.0f} ohm, Q = {Q:.3f}, "
          f"BW = R/(2 pi L) = {p['R']/(2*math.pi*p['L']):.1f} Hz;  mechanical: R_M = 10 kg/s, M_M = 10 g, "
          f"k = 1/C_M = {1/p['C']/1e6:.2f} MN/m;  acoustical: R_A = 10 Pa s/m^3, M_A = 10 g/m^4, C_A = {p['C']*1e5:.1f} dm^5/N")


# =====================================================================  schematics
def build11():
    s = g.Sch()
    s.text(-96, -256, "Problem 1.1 - duality of DC circuits.  Top: the circuit with impedances Z = R.  Bottom: its dual, with admittances Y = 1/R.")
    s.text(-96, -224, "LTspice only has resistors, so the dual's conductances are typed in as resistor values (G1 = 1/R1 = 10m ...): same numbers, units swap V <-> A.")
    # ---- original: V1 - R1 - (R2 || R3)
    s.vsrc(0, 0, "V1", "10"); s.flag(0, 0, "v0")
    s.wire(0, 0, 96, 0)
    x = s.hser("res", 96, 0, "R1", "100")
    s.wire(x, 0, 512, 0); s.flag(400, 0, "v3")
    s.shunts(288, 0, [("res", "R2", "2k"), ("res", "R3", "500")])
    s.text(640, -32, "v3 = v0 Z2 Z3 / (Z1 (Z2+Z3) + Z2 Z3) = 8 V")
    s.text(640, 0, "i1 = I(R1) = 20 mA,  v1 = 2 V,  i2 = 4 mA,  i3 = 16 mA")
    # ---- dual: I1 || G1 - G2 - G3
    y = 400
    s.isrc(0, y, "I1", "10"); s.flag(0, y, "d_i1")
    s.wire(0, y, 288, y)
    s.vshunt("res", 176, y, "R_G1", "10m")
    x = s.hser("res", 288, y, "R_G2", "0.5m")
    s.wire(x, y, 512, y); s.flag(512, y, "d_i3")
    s.vshunt("res", 512, y, "R_G3", "2m")
    s.text(640, y - 32, "dual: every current above is a voltage here and vice versa")
    s.text(640, y, "V(d_i1) = 20 mV (= i1),  I(R_G2) = 8 A (= v3),  I(R_G1) = 2 A (= v1),  V(d_i3) = 16 mV (= i3)")
    s.text(-96, 640, ".op", directive=True)
    s.text(-96, 688, "Run, then hover the wires / resistors (or View > SPICE Error Log) to read the operating point.")
    s.dump(HERE / "P1_1_DC_Duality.asc")
    return HERE / "P1_1_DC_Duality.asc"


def build12():
    s = g.Sch()
    s.text(-96, -256, "Problem 1.2 - duality of AC circuits.  Top: V1 - L1 - (C3 || L2).  Bottom, the dual: I1 || C1 - L3 - C2.")
    s.text(-96, -224, "Series <-> parallel, L <-> C, V source <-> I source.  L1, L2 keep LTspice's default Rser = 1m; the dual of that is Rpar = 1/1m = 1k on C1, C2.")
    s.vsrc(0, 0, "V1", "AC 2"); s.flag(0, 0, "vin")
    s.wire(0, 0, 96, 0)
    x = s.hser("ind", 96, 0, "L1", "1m", "Rser=1m")
    s.wire(x, 0, 512, 0); s.flag(400, 0, "vout")
    s.shunts(288, 0, [("cap", "C3", "2u"), ("ind", "L2", "4m", "Rser=1m")])
    y = 400
    s.isrc(0, y, "I1", "AC 2"); s.flag(0, y, "d_in")
    s.wire(0, y, 288, y)
    s.vshunt("cap", 176, y, "C1", "1m", "Rpar=1k")
    x = s.hser("ind", 288, y, "L3", "2u", g.NOLOSS)
    s.wire(x, y, 512, y); s.flag(512, y, "d_out")
    s.vshunt("cap", 512, y, "C2", "4m", "Rpar=1k")
    s.text(-96, 640, ".ac dec 1000 20 20k", directive=True)
    s.text(-96, 688, "Plot V(vout) and I(C2): the same curve.  Flat at 2*L2/(L1+L2) = 1.6 (4.1 dB), resonance at sqrt((1+L1/L2)/(L1 C3))/2pi = 3979 Hz, then -40 dB/decade.")
    s.dump(HERE / "P1_2_AC_Duality.asc")
    g.plt(HERE / "P1_2_AC_Duality.plt", [(["V(vout)", "I(C2)"], (0.03, 3e4))], (20, 20000))
    return HERE / "P1_2_AC_Duality.asc"


def build13():
    s = g.Sch()
    s.text(-96, -256, "Problem 1.3 - series resonator, and the mechanical and acoustical resonator with the same behaviour (impedance analogy).")
    s.text(-96, -224, ".param R=10 L=10m C=2u", directive=True)
    rows = [("electrical", "V1", "vin", "Vi", "R1", "L1", "C1", "10 ohm, 10 mH, 2 uF  ->  current i = I(Vi), impedance V(vin)/I(Vi)"),
            ("mechanical", "V_F", "f_in", "Vu", "R_RM", "L_MM", "C_CM", "R_M = 10 kg/s, M_M = 10 g, C_M = 2 um/N (k = 0.5 MN/m)  ->  velocity u = I(Vu)"),
            ("acoustical", "V_p", "p_in", "VUa", "R_RA", "L_MA", "C_CA", "R_A = 10 Pa s/m^3, M_A = 10 g/m^4, C_A = 2u m^5/N = 0.2 dm^5/N  ->  U = I(VUa)")]
    for k, (dom, vs, node, vi, rn, ln, cn, note) in enumerate(rows):
        y = k * 320
        s.vsrc(0, y, vs, "AC 1"); s.flag(0, y, node)
        s.wire(0, y, 96, y)
        x = s.vsense(96, y, vi); s.wire(x, y, x + 64, y)
        x = s.hser("res", x + 64, y, rn, "{R}")
        s.wire(x, y, x + 64, y)
        x = s.hser("ind", x + 64, y, ln, "{L}", g.NOLOSS)
        s.wire(x, y, x + 64, y)
        x = s.hser("cap", x + 64, y, cn, "{C}")
        s.wire(x, y, x + 64, y); s.wire(x + 64, y, x + 64, y + 96); s.gnd(x + 64, y + 96)
        s.text(784, y - 32, dom + ":")
        s.text(784, y, note)
    s.text(-96, 880, ".ac dec 1000 10 100k", directive=True)
    s.text(-96, 928, "Plot I(Vi) and V(vin)/I(Vi): current peaks at f0 = 1/(2 pi sqrt(LC)) = 1125.4 Hz with 1/R = 100 mA, |Z| dips to R = 10 ohm, bandwidth R/(2 pi L) = 159 Hz.")
    s.dump(HERE / "P1_3_Series_Resonator.asc")
    g.plt(HERE / "P1_3_Series_Resonator.plt", [(["I(Vi)", "V(vin)/I(Vi)"], (3e-5, 3e4))], (10, 100000))
    return HERE / "P1_3_Series_Resonator.asc"


# =====================================================================  verify
def chk(label, got, want, tol):
    ok = abs(got - want) <= tol * max(abs(want), 1e-30)
    print(f"  {'OK ' if ok else 'BAD'} {label}: LTspice {got:.6g}, expected {want:.6g}")
    return ok


def verify(files):
    ok = True
    # 1.1 - operating point
    d = g.run_ltspice(files["11"]); r = p11()
    ok &= chk("1.1 v3 = V(v3)", d["v(v3)"][0], r["v3"], 1e-5)
    ok &= chk("1.1 i1 = |I(R1)|", abs(d["i(r1)"][0]), r["i1"], 1e-5)
    ok &= chk("1.1 i2 = |I(R2)|", abs(d["i(r2)"][0]), r["i2"], 1e-5)
    ok &= chk("1.1 i3 = |I(R3)|", abs(d["i(r3)"][0]), r["i3"], 1e-5)
    ok &= chk("1.1 dual V(d_i1) = i1 [V]", d["v(d_i1)"][0], r["i1"], 1e-5)
    ok &= chk("1.1 dual V(d_i3) = i3 [V]", d["v(d_i3)"][0], r["i3"], 1e-5)
    ok &= chk("1.1 dual |I(R_G2)| = v3 [A]", abs(d["i(r_g2)"][0]), r["v3"], 1e-5)
    ok &= chk("1.1 dual |I(R_G1)| = v1 [A]", abs(d["i(r_g1)"][0]), r["v1"], 1e-5)
    # 1.2 - both circuits against each other and the closed form
    d = g.run_ltspice(files["12"]); f = [x.real for x in d["frequency"]]
    worst_cf = max(abs(d["v(vout)"][j] / p12(fi) - 1) for j, fi in enumerate(f))
    worst_du = max(abs(d["i(c2)"][j] / d["v(vout)"][j] - 1) for j in range(len(f)))
    jp = max(range(len(f)), key=lambda j: abs(d["v(vout)"][j]))
    print(f"  {'OK ' if worst_cf < 1e-6 else 'BAD'} 1.2 V(vout) vs closed form: worst {worst_cf:.1e}")
    print(f"  {'OK ' if worst_du < 1e-6 else 'BAD'} 1.2 I(C2) vs V(vout) (duality): worst {worst_du:.1e}")
    ok &= worst_cf < 1e-6 and worst_du < 1e-6
    ok &= chk("1.2 level at 20 Hz [dB]", 20 * math.log10(abs(d["v(vout)"][0])), 20 * math.log10(1.6), 2e-3)
    ok &= chk("1.2 peak frequency [Hz]", f[jp], 3978.9, 3e-3)
    print(f"      peak height {20*math.log10(abs(d['v(vout)'][jp])):.1f} dB (finite only because of the 1 mOhm Rser / 1 kOhm Rpar)")
    # 1.3
    d = g.run_ltspice(files["13"]); f = [x.real for x in d["frequency"]]
    worst = 0
    for j, fi in enumerate(f):
        Z, i = p13(fi)
        for got, want in ((d["i(vi)"][j], i), (d["i(vu)"][j], i), (d["i(vua)"][j], i), (d["v(vin)"][j] / d["i(vi)"][j], Z)):
            worst = max(worst, abs(got / want - 1))
    print(f"  {'OK ' if worst < 1e-6 else 'BAD'} 1.3 all three resonators vs closed form: worst {worst:.1e}")
    ok &= worst < 1e-6
    mag = [abs(x) for x in d["i(vi)"]]; jp = max(range(len(f)), key=lambda j: mag[j])
    ok &= chk("1.3 f0 [Hz]", f[jp], 1125.395, 2e-3)
    ok &= chk("1.3 i_max [A]", mag[jp], 0.1, 1e-4)
    ok &= chk("1.3 Z_min [ohm]", abs(d["v(vin)"][jp] / d["i(vi)"][jp]), 10.0, 1e-4)
    half = mag[jp] / math.sqrt(2)
    def cross(rng):
        for j in rng:
            a, b = mag[j], mag[j + 1]
            if (a - half) * (b - half) <= 0:
                return f[j] * (f[j + 1] / f[j]) ** ((half - a) / (b - a))
    bw = cross(range(jp, len(f) - 1)) - cross(range(0, jp))
    ok &= chk("1.3 -3 dB bandwidth [Hz]", bw, 159.15, 3e-3)
    print("ALL OK" if ok else "MISMATCH")
    return ok


if __name__ == "__main__":
    hand()
    files = {"11": build11(), "12": build12(), "13": build13()}
    if "--preview" in sys.argv:
        import preview_asc as pv
        pv.HERE = HERE
        [pv.main(str(p)) for p in files.values()]
    if "--verify" in sys.argv:
        sys.exit(0 if verify(files) else 1)
