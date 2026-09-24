#!/usr/bin/env python3
"""34870 Lecture 3 problem solving (acoustic systems): LTspice circuits for the
problems whose official solution shows a simulation.

    python3 p3.py            # print the hand numbers, write the .asc/.plt files
    python3 p3.py --verify   # also run LTspice headless and compare with the closed form
    python3 p3.py --preview  # draw the .asc files to preview/*.png and lint the layout

Numbering: the lecture slides call these Problems 2.1-2.4, the official solution
sheet (34870_Solutions3.pdf) calls them 3.1-3.4. The file names use the solution
sheet's numbers.

Acoustic IMPEDANCE analogy throughout (pressure = voltage, volume velocity =
current): an open tube is an acoustic mass M_A = rho*l/S (inductor), a closed
volume is an acoustic compliance C_A = V/(rho*c^2) (capacitor to ground). The
source is a 1 A current source = 1 m^3/s volume velocity, so the voltage at the
drive node reads directly as the acoustic impedance Z_A = p/U in Pa*s/m^3.
Needs the Lab A builder: ../../Labs/Lab A/LTspice/gen_ltspice.py (the labs repo).
"""
import math, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
LABA = HERE.parents[1] / "Labs" / "Lab A" / "LTspice"
sys.path.insert(0, str(LABA))
import gen_ltspice as g                      # noqa: E402

RHO, C0 = 1.18, 344.0                        # the problem sheet's air

# ---------------------------------------------------------------- 3.2: Helmholtz resonator tuned to 100 Hz
MA_32 = 100.0                                                    # official example: M_A = 100 kg/m^4
CA_32 = 1 / ((2 * math.pi * 100) ** 2 * MA_32)                   # -> C_A = 2.53e-8 m^5/N

# ---------------------------------------------------------------- 3.3: tube(s) in a 23 L box
L_EFF, R1, R2, VBOX = 0.12, 0.05, 0.005, 0.023
MA1 = RHO * L_EFF / (math.pi * R1 ** 2)                          # wide tube   18.03 kg/m^4
MA2 = RHO * L_EFF / (math.pi * R2 ** 2)                          # narrow tube 1803 kg/m^4
CAV = VBOX / (RHO * C0 ** 2)                                     # box         1.65e-7 m^5/N


def hand():
    print(f"3.2  M_A = {MA_32:g} kg/m4, C_A = {CA_32:.4g} m5/N -> f_0 = {1/(2*math.pi*math.sqrt(MA_32*CA_32)):.2f} Hz  (official: 2.53e-8, 100)")
    print(f"3.3a M_A1 = {MA1:.2f} kg/m4, C_A = {CAV:.4g} m5/N  (official: 18.03, 1.65e-7)")
    print(f"3.3b f_A = {1/(2*math.pi*math.sqrt(MA1*CAV)):.2f} Hz  (official: 92.4)")
    print(f"3.3c M_A2 = {MA2:.1f} kg/m4  (official: 1803)")
    print(f"3.3d f_B = {1/(2*math.pi*math.sqrt(MA2*CAV)):.3f} Hz  (official: 9.2)")
    fres = math.sqrt((MA1 + MA2) / (MA1 * MA2 * CAV)) / (2 * math.pi)
    print(f"3.3e resonance with both tubes (Z_in = 0) at {fres:.3f} Hz")


# ---------------------------------------------------------------- closed forms
def z_32(f):
    jw = 2j * math.pi * f
    return jw * MA_32 + 1 / (jw * CA_32)


def z_33(f, drive, other=None):
    """impedance seen from the tube 'drive'; 'other' = tube to ground in parallel with the box (or None)"""
    jw = 2j * math.pi * f
    zb = 1 / (jw * CAV)
    if other:
        zb = 1 / (1 / zb + 1 / (jw * other))
    return jw * drive + zb, zb


# ---------------------------------------------------------------- LTspice
def helmholtz():
    s = g.Sch()
    s.text(0, -256, "Problem 3.2 (slides: 2.2) - tube in a box = Helmholtz resonator, tuned to 100 Hz")
    s.text(0, -224, "acoustic IMPEDANCE analogy: p = voltage, U = current.  tube = acoustic mass M_A (L), box = compliance C_A (C to ground)")
    s.text(0, -176, ".param MA=100 CA={1/((2*pi*100)**2*MA)}", directive=True)
    s.isrc(0, 0, "I_U")
    s.flag(0, 0, "p_in"); s.wire(0, 0, 128, 0)
    x = s.hser("ind", 128, 0, "L_MA", "{MA}", g.NOLOSS)
    s.wire(x, 0, x + 176, 0); s.flag(x + 96, 0, "p_box")
    s.vshunt("cap", x + 176, 0, "C_CA", "{CA}")
    s.text(0, 192, ".ac dec 2000 1 10k", directive=True)
    s.text(0, 240, "U = 1 m^3/s, so V(p_in) = Z_A = p/U [Pa s/m^3].  Plot V(p_in) in dB: V-shaped dip to (almost) zero at 100 Hz,")
    s.text(0, 272, "-90 deg below (the box spring wins), +90 deg above (the tube mass wins).  Official: C_A = 2.53e-8 m^5/N, M_A = 100 kg/m^4")
    s.dump(HERE / "P3-2_Helmholtz_100Hz.asc")
    g.plt(HERE / "P3-2_Helmholtz_100Hz.plt", [(["V(p_in)"], (1, 1e8))], (1, 10000))
    return HERE / "P3-2_Helmholtz_100Hz.asc"


def row(s, y, sfx, drive, other, title):
    """one volume-velocity-driven branch: U -> drive tube (L) -> box node -> C_A (and the other tube) to ground"""
    s.text(0, y - 112, title)
    s.isrc(0, y, f"I_U{sfx}")
    s.flag(0, y, f"p_in{sfx}"); s.wire(0, y, 128, y)
    x = s.hser("ind", 128, y, f"L_{drive[0]}{sfx}", "{%s}" % drive[1], g.NOLOSS)
    s.flag(x + 96, y, f"p_box{sfx}")
    shunts = [("cap", f"C_Cav{sfx}", "{Cav}")] + ([("ind", f"L_{other[0]}{sfx}", "{%s}" % other[1], g.NOLOSS)] if other else [])
    end = s.shunts(x + 176, y, shunts)
    s.wire(x, y, end, y)


def tubes():
    s = g.Sch()
    s.text(0, -320, "Problem 3.3 (slides: 2.3) - tubes in a 23 L box.  Acoustic IMPEDANCE analogy, U = 1 m^3/s, so V(p_in..) = Z_A [Pa s/m^3]")
    s.text(0, -272, ".param rho=1.18 c=344 l=0.12 r1=0.05 r2=0.005 V=0.023", directive=True)
    s.text(0, -240, ".param Ma1={rho*l/(pi*r1**2)} Ma2={rho*l/(pi*r2**2)} Cav={V/(rho*c**2)}", directive=True)
    row(s, 0, "_f", ("Ma1", "Ma1"), None, "f) wide tube + box only: plot V(p_in_f), minimum at f_A = 92.4 Hz")
    row(s, 448, "_de", ("Ma1", "Ma1"), ("Ma2", "Ma2"), "c-e) narrow tube added, driven from the WIDE tube: V(p_box_de) peaks at f_B = 9.2 Hz; V(p_in_de) peak 9.2 Hz, dip 92.8 Hz")
    row(s, 896, "_g", ("Ma2", "Ma2"), ("Ma1", "Ma1"), "g) driven from the NARROW tube: V(p_in_g) peak (Ma1 || Cav) at 92.4 Hz right next to the dip at 92.8 Hz")
    s.text(0, 1088, ".ac dec 5000 1 1000", directive=True)
    s.text(0, 1136, "the box compliance always goes to ground (it is the pressure inside the box, measured against the outside);")
    s.text(0, 1168, "a tube that opens to the outside also ends on ground (p_outside ~ 0, radiation impedance neglected)")
    s.dump(HERE / "P3-3_Tubes_in_Box.asc")
    g.plt(HERE / "P3-3_Tubes_in_Box.plt",
          [(["V(p_in_f)"], (1, 1e8)), (["V(p_in_de)", "V(p_box_de)"], (1e2, 1e10)), (["V(p_in_g)"], (1e2, 1e10))], (1, 1000))
    return HERE / "P3-3_Tubes_in_Box.asc"


def extreme(f, y, lo, hi, kind):
    idx = [j for j in range(len(f)) if lo <= f[j] <= hi]
    j = (max if kind == "max" else min)(idx, key=lambda k: abs(y[k]))
    return f[j], abs(y[j])


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

    d = g.run_ltspice(files[0]); f = [v.real for v in d["frequency"]]
    worst = max(abs(d["v(p_in)"][j] / z_32(f[j]) - 1) for j in range(len(f)))
    print("3.2 Helmholtz"); dev("worst deviation from j*w*MA + 1/(j*w*CA)", worst)
    fr, _ = extreme(f, d["v(p_in)"], 50, 200, "min"); chk("dip Hz", fr, 100.0, 2e-3)

    d = g.run_ltspice(files[1]); f = [v.real for v in d["frequency"]]
    worst = 0
    for j, fi in enumerate(f):
        for got, want in ((d["v(p_in_f)"][j], z_33(fi, MA1)[0]), (d["v(p_in_de)"][j], z_33(fi, MA1, MA2)[0]),
                          (d["v(p_box_de)"][j], z_33(fi, MA1, MA2)[1]), (d["v(p_in_g)"][j], z_33(fi, MA2, MA1)[0])):
            worst = max(worst, abs(got / want - 1))
    print("3.3 tubes in a box"); dev("worst deviation from the closed forms", worst)
    fres = math.sqrt((MA1 + MA2) / (MA1 * MA2 * CAV)) / (2 * math.pi)
    fr, _ = extreme(f, d["v(p_in_f)"], 50, 200, "min"); chk("f) dip Hz (official 92.4)", fr, 92.4, 2e-3)
    fr, _ = extreme(f, d["v(p_box_de)"], 2, 50, "max"); chk("d) box pressure peak Hz (official 9.2)", fr, 9.2, 1e-2)
    fr, _ = extreme(f, d["v(p_in_de)"], 50, 200, "min"); chk("e) Z_in dip Hz", fr, fres, 2e-3)
    fr, _ = extreme(f, d["v(p_in_g)"], 50, 200, "max"); chk("g) Z_in peak Hz (Ma1 || Cav)", fr, 92.4, 2e-3)
    fr, _ = extreme(f, d["v(p_in_g)"], 92.6, 200, "min"); chk("g) Z_in dip Hz", fr, fres, 2e-3)
    print("ALL OK" if ok else "MISMATCH")
    return ok


if __name__ == "__main__":
    hand()
    files = [helmholtz(), tubes()]
    if "--preview" in sys.argv:
        import preview_asc as pv
        pv.HERE = HERE
        [pv.main(str(p)) for p in files]
    if "--verify" in sys.argv:
        sys.exit(0 if verify(files) else 1)
