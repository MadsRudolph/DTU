#!/usr/bin/env python3
"""34870 Problems 9 (Loudspeakers 3: crossovers): problems 1-2 by hand, and the
LTspice model of problem 3 (Peerless SLS-P830669 woofer in 40 L + NE123W-08
midrange in 2 L, passive crossover at 250 Hz).

    python3 p9.py            # print problems 1-3, write the .asc/.plt files
    python3 p9.py --verify   # also run LTspice headless and compare with the closed form
    python3 p9.py --plots    # (with --verify) write the figures into the vault Images/Lecture9/
    python3 p9.py --preview  # draw the .asc files to preview/*.png and lint the layout

Driver model (lectures 7-8, impedance analogy, closed box with M_AB = M_A1 and no
filling, so M_MC = M_MS and the box only stiffens the spring, C_MT = C_MS/(1+alpha)):
    electrical: v -> R_E -> L_E -> H_emf = Bl*u            (current i = I(Vdx))
    mechanical: H_Bli = Bl*i -> M_MS -> R_MS -> C_MT -> 0  (velocity u = I(Vmx))
    far field:  p(1 m) = j*w*rho*S_D*u/(2*pi)              (baffled, as on slide 34)
The filters are designed on R_E (the lecture's "ideal resistive load"), which is
exactly the assumption the problem wants you to break: the circuit also carries a
copy of each filter loaded by R_E alone, so V(vw)/V(vw_id) shows the damage.
Needs the Lab A builder: ../../Labs/Lab A/LTspice/gen_ltspice.py (the labs repo).
"""
import math, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
LABA = HERE.parents[1] / "Labs" / "Lab A" / "LTspice"
sys.path.insert(0, str(LABA))
import gen_ltspice as g                      # noqa: E402

g.PINS["h"] = [(0, 16), (0, 96)]
RHO, C0, PREF = 1.2, 344.0, 20e-6
VAULT_IMG = pathlib.Path.home() / "DTU/Obsidian/Courses/34870 Electroacoustics/Images/Lecture9"
SQ2 = math.sqrt(2)


# =====================================================================  problems 1-2
def bw2(R, fc, Q=1 / SQ2):
    """slides 11-12: same L and C for the low-pass (series L, shunt C) and the high-pass (series C, shunt L)"""
    w = 2 * math.pi * fc
    return R / (w * Q), Q / (w * R)


def problem1():
    Lw, Cw = bw2(5.0, 2500); Lt, Ct = bw2(6.0, 2500)
    print(f"P1a  woofer (R_E 5 ohm): L = {Lw*1e3:.3f} mH  C = {Cw*1e6:.2f} uF   [0.45 mH, 9 uF]")
    print(f"     tweeter (R_E 6 ohm): L = {Lt*1e3:.3f} mH  C = {Ct*1e6:.2f} uF   [0.54 mH, 7.5 uF]")
    # b) LR2 = BW1 squared; L - H = (1 - s^2)/(1 + s)^2 = (1 - s)/(1 + s): an all-pass
    worst = max(abs(abs(lr2(x)[0] - lr2(x)[1]) - 1) for x in (0.01, 0.3, 1, 3, 100))
    print(f"P1b  |L_LR2 - H_LR2| = |(1-s)/(1+s)| = 1 at every frequency (numerical check: worst deviation {worst:.1e})")


def bw2tf(x, Q=1 / SQ2):
    s = 1j * x; d = 1 + s / Q + s * s
    return 1 / d, s * s / d


def lr2(x):
    s = 1j * x
    return 1 / (1 + s) ** 2, s * s / (1 + s) ** 2


def lr4(x):
    lo, hi = bw2tf(x)
    return lo * lo, hi * hi


def problem2():
    db = lambda z: 20 * math.log10(max(abs(z), 1e-12))
    ph = lambda z: math.degrees(math.atan2(z.imag, z.real))
    print("P2   total response at f/fc = 0.1 / 0.5 / 1 / 2 / 10   (dB, phase)")
    for name, fn, sgn in (("BW2 same polarity     ", bw2tf, 1), ("BW2 tweeter inverted  ", bw2tf, -1),
                          ("LR2 same polarity     ", lr2, 1), ("LR2 tweeter inverted  ", lr2, -1),
                          ("LR4 same polarity     ", lr4, 1)):
        row = []
        for x in (0.1, 0.5, 1, 2, 10):
            lo, hi = fn(x); t = lo + sgn * hi
            row.append(f"{db(t):+7.2f} dB {ph(t):+7.1f}°")
        print(f"     {name}" + " | ".join(row))
    print("     -> LR2 needs the tweeter inverted (flat, phase turns 0 -> -180°); LR4 is flat with SAME polarity (phase 0 -> -360°)")


# =====================================================================  problem 3: the drivers
# data sheets (Tymphany), Problems 9 pages 3-4
WOOF = dict(name="SLS-P830669", Re=5.6, Le=1.12e-3, Mms=74.1e-3, Cms=345e-6, Qms=7.07, Bl=11.88, Sd=522.8e-4, Vas=132.42e-3, Vb=40e-3, sens=89.85)
MID = dict(name="NE123W-08", Re=6.27, Le=0.06e-3, Mms=4.7e-3, Cms=1433.2e-6, Qms=4.98, Bl=5.53, Sd=54.1e-4, Vas=5.89e-3, Vb=2e-3, sens=87.23)


def boxed(d):
    """closed-box numbers (lecture 8): alpha = V_AS/V_AB, f_C = f_S sqrt(1+alpha), Q_TC = Q_TS sqrt(1+alpha)"""
    ws = 1 / math.sqrt(d["Mms"] * d["Cms"])
    Rms = ws * d["Mms"] / d["Qms"]; Qes = d["Re"] * ws * d["Mms"] / d["Bl"] ** 2
    Qts = Qes * d["Qms"] / (Qes + d["Qms"]); a = d["Vas"] / d["Vb"]
    Cmt = d["Cms"] / (1 + a)
    k = RHO * d["Bl"] * d["Sd"] / (2 * math.pi * d["Re"] * d["Mms"])          # Pa per V at 1 m, mid band
    return dict(d, fs=ws / 2 / math.pi, Rms=Rms, Qes=Qes, Qts=Qts, alpha=a, Cmt=Cmt,
                fc=ws * math.sqrt(1 + a) / 2 / math.pi, Qtc=Qts * math.sqrt(1 + a), spl=20 * math.log10(2.83 * k / PREF),
                Zmax=d["Re"] + d["Bl"] ** 2 / Rms)


def ZE(d, f):
    jw = 2j * math.pi * f
    zm = jw * d["Mms"] + d["Rms"] + 1 / (jw * d["Cmt"])
    return d["Re"] + jw * d["Le"] + d["Bl"] ** 2 / zm, zm


def ladder(els, Zload):
    """els = [('s'|'p', Z), ...] from the source to the load. Returns V_load/V_in."""
    Zs, Z = [], Zload
    for k, z in reversed(els):
        Zs.append(Z); Z = Z + z if k == "s" else 1 / (1 / Z + 1 / z)
    H = 1
    for (k, z), Za in zip(els, Zs[::-1]):
        if k == "s":
            H *= Za / (Za + z)
    return H


def filt(kind, order, R, fc, Q, f):
    """element list of the textbook filter designed on R (slides 8-15); order 0 = no filter"""
    if order == 0:
        return []
    jw = 2j * math.pi * f; w0 = 2 * math.pi * fc
    zl = lambda L: jw * L; zc = lambda C: 1 / (jw * C)
    if order == 2:
        L, C = bw2(R, fc, Q)
        return [("s", zl(L)), ("p", zc(C))] if kind == "lp" else [("s", zc(C)), ("p", zl(L))]
    if kind == "lp":   # LR4, slide 15
        return [("s", zl(1.886 * R / w0)), ("p", zc(1.591 / (w0 * R))), ("s", zl(0.943 * R / w0)), ("p", zc(0.354 / (w0 * R)))]
    return [("s", zc(1 / (w0 * 1.886 * R))), ("p", zl(R / (w0 * 1.591))), ("s", zc(1 / (w0 * 0.943 * R))), ("p", zl(R / (w0 * 0.354)))]


def system(W, M, f, order=2, fc=250.0, Q=1 / SQ2, pol=1, eg=2.83):
    """closed form of the whole circuit: filter voltages, cone velocities, pressures at 1 m"""
    out = {}
    for tag, d, kind in (("w", W, "lp"), ("m", M, "hp")):
        ze, zm = ZE(d, f)
        els = filt(kind, order, d["Re"], fc, Q, f)
        v = eg * ladder(els, ze); vid = eg * ladder(els, d["Re"])
        i = v / ze; u = d["Bl"] * i / zm
        p = 2j * math.pi * f * RHO * d["Sd"] * u / (2 * math.pi)
        out.update({f"v{tag}": v, f"v{tag}_id": vid, f"i{tag}": i, f"u{tag}": u, f"p{tag}": p})
    out["ptot"] = out["pw"] + pol * out["pm"]
    return out


def problem3():
    W, M = boxed(WOOF), boxed(MID)
    for d in (W, M):
        print(f"P3a  {d['name']:12s} f_S {d['fs']:5.1f} Hz  Q_ES {d['Qes']:.3f}  Q_TS {d['Qts']:.3f}  R_MS {d['Rms']:.3f} Ns/m  "
              f"| box {d['Vb']*1e3:.0f} L: alpha {d['alpha']:.2f}  f_C {d['fc']:.1f} Hz  Q_TC {d['Qtc']:.2f}  "
              f"| model SPL(2.83 V, 1 m) {d['spl']:.1f} dB (sheet {d['sens']})  |Z| peak {d['Zmax']:.0f} ohm")
    Lw, Cw = bw2(W["Re"], 250); Lm, Cm = bw2(M["Re"], 250)
    print(f"P3a  BW2 at 250 Hz on R_E:  woofer low-pass L = {Lw*1e3:.2f} mH, C = {Cw*1e6:.1f} uF;  "
          f"midrange high-pass C = {Cm*1e6:.1f} uF, L = {Lm*1e3:.2f} mH")
    for f in (100, 250, 500):
        ze_w, _ = ZE(W, f); ze_m, _ = ZE(M, f)
        print(f"     |Z_E| at {f} Hz: woofer {abs(ze_w):5.2f} ohm, midrange {abs(ze_m):5.2f} ohm")
    db = lambda z: 20 * math.log10(abs(z))
    spl = lambda f, **k: db(system(W, M, f, **k)["ptot"] / PREF)
    print(f"P3   levels on their own (no filter, 2.83 V): woofer {db(system(W, M, 125, order=0)['pw']/PREF):.1f} dB at 125 Hz, "
          f"{db(system(W, M, 250, order=0)['pw']/PREF):.1f} dB at 250 Hz; midrange {db(system(W, M, 250, order=0)['pm']/PREF):.1f} dB at 250 Hz, {db(system(W, M, 500, order=0)['pm']/PREF):.1f} at 500 Hz -> the woofer is ~4 dB louder at the crossover")
    fs = [125 * 2 ** (k / 48) for k in range(0, 97)]                  # 125-500 Hz: one octave either side of 250 Hz
    print("P3b/c  summed SPL (2.83 V, 1 m) at 125 / 177 / 250 / 354 / 500 Hz, and the ripple over 125-500 Hz")
    rows = []
    for order, Q, label in ((2, 1 / SQ2, "BW2"), (2, 0.5, "LR2"), (4, 0.707, "LR4")):
        for fc in (250, 300, 350):
            for pol in (1, -1):
                lv = [spl(f, order=order, fc=fc, Q=Q, pol=pol) for f in fs]
                rows.append((max(lv) - min(lv), label, fc, pol, [lv[i] for i in (0, 24, 48, 72, 96)], fs[lv.index(min(lv))]))
    for rip, label, fc, pol, pts, fmin in rows:
        if fc == 250 or rip < 4:
            print(f"     {label} fc {fc} Hz, midrange {'normal  ' if pol > 0 else 'INVERTED'}: " + " / ".join(f"{v:5.1f}" for v in pts) +
                  f"   ripple {rip:5.2f} dB (lowest at {fmin:.0f} Hz)")
    b = min(rows)
    print(f"     flattest: {b[1]} at {b[2]} Hz, midrange {'normal' if b[3] > 0 else 'inverted'} ({b[0]:.2f} dB over 125-500 Hz)")
    return W, M


# =====================================================================  problem 3: LTspice
def driver(s, x, y, tag, d, title):
    """driver from the filter output node v<tag> at (x, y): electrical loop then mechanical loop"""
    t = tag.upper()
    s.text(x, y - 176, title)
    x = s.vsense(x, y, f"Vd{tag}"); s.wire(x, y, x + 48, y)
    x = s.hser("res", x + 48, y, f"R_E{tag}", f"{{Re{tag}}}"); s.wire(x, y, x + 48, y)
    x = s.hser("ind", x + 48, y, f"L_E{tag}", f"{{Le{tag}}}", g.NOLOSS); s.wire(x, y, x + 112, y)
    x += 112
    s.sym("h", "R0", x, y - 16, f"H_emf{tag}", f"Vm{tag} {{Bl{tag}}}", win=["WINDOW 0 24 40 Left 2", "WINDOW 3 24 72 Left 2"]); s.gnd(x, y + 80)
    mx = x + 352
    s.sym("h", "R0", mx, y - 16, f"H_Bli{tag}", f"Vd{tag} {{Bl{tag}}}", win=["WINDOW 0 24 40 Left 2", "WINDOW 3 24 72 Left 2"]); s.gnd(mx, y + 80)
    s.wire(mx, y, mx + 160, y)
    x = s.vsense(mx + 160, y, f"Vm{tag}"); s.wire(x, y, x + 48, y)
    x = s.hser("ind", x + 48, y, f"L_Mms{tag}", f"{{Mms{tag}}}", g.NOLOSS); s.wire(x, y, x + 48, y)
    x = s.hser("res", x + 48, y, f"R_Rms{tag}", f"{{Rms{tag}}}"); s.wire(x, y, x + 48, y)
    x = s.hser("cap", x + 48, y, f"C_Cmt{tag}", f"{{Cmt{tag}}}"); s.wire(x, y, x + 64, y)
    s.wire(x + 64, y, x + 64, y + 80); s.gnd(x + 64, y + 80)


def filter_values(order, tag):
    """the filter elements as .param expressions (slides 11-15), so the symbols only carry short names"""
    R, w = f"Re{tag}", "(2*pi*fc)"
    if order == 2:
        return [(f"L{tag}", f"{R}/({w}*Q)"), (f"C{tag}", f"Q/({w}*{R})")]
    if tag == "w":
        return [("L1w", f"1.886*{R}/{w}"), ("C1w", f"1.591/({w}*{R})"), ("L2w", f"0.943*{R}/{w}"), ("C2w", f"0.354/({w}*{R})")]
    return [("C1m", f"1/({w}*1.886*{R})"), ("L1m", f"{R}/({w}*1.591)"), ("C2m", f"1/({w}*0.943*{R})"), ("L2m", f"{R}/({w}*0.354)")]


def filter_chain(s, x, y, kind, order, tag, node):
    """textbook filter from the 'in' rail at (x, y); returns the x of its output node (flagged `node`)"""
    names = [n for n, _ in filter_values(order, tag)]
    if order == 2:
        names = names if kind == "lp" else names[::-1]
    s.wire(x, y, x + 64, y); x += 64
    for i in range(0, len(names), 2):
        n1, n2 = names[i], names[i + 1]
        k1, k2 = ("ind", "cap") if n1[0] == "L" else ("cap", "ind")
        x = s.hser(k1, x, y, f"{n1}_{node}", f"{{{n1}}}", g.NOLOSS if k1 == "ind" else None); s.wire(x, y, x + 96, y); x += 96
        s.vshunt(k2, x, y, f"{n2}_{node}", f"{{{n2}}}", g.NOLOSS if k2 == "ind" else None)
        s.wire(x, y, x + 176, y); x += 176
    s.flag(x - 64, y, node)
    return x


def params(s, W, M, order, y):
    pw = lambda d, t: (f"Re{t}={d['Re']} Le={d['Le']:g} Bl{t}={d['Bl']} Mms{t}={d['Mms']:g} Rms{t}={d['Rms']:.5g} "
                       f"Cms{t}={d['Cms']:g} Sd{t}={d['Sd']:g} Vas{t}={d['Vas']:g} Vb{t}={d['Vb']:g}").replace("Le=", f"Le{t}=")
    s.text(0, y, ".param " + pw(W, "w") + " Cmtw={Cmsw/(1+Vasw/Vbw)}", directive=True)
    s.text(0, y + 32, ".param " + pw(M, "m") + " Cmtm={Cmsm/(1+Vasm/Vbm)}", directive=True)
    s.text(0, y + 64, ".param fc=250 pol=1" + (" Q={1/sqrt(2)}" if order == 2 else ""), directive=True)
    s.text(0, y + 96, ".param " + " ".join(f"{n}={{{e}}}" for t in "wm" for n, e in filter_values(order, t)), directive=True)


def build(W, M, order):
    name = "P9_3_BW2_250Hz" if order == 2 else "P9_3_LR4_250Hz"
    s = g.Sch()
    s.text(0, -704, f"Problems 9.3 - {'2nd-order Butterworth' if order == 2 else '4th-order Linkwitz-Riley (slide 15)'} crossover at fc for "
                    f"Peerless SLS-P830669 (40 L closed box) + NE123W-08 midrange (2 L closed box)")
    s.text(0, -672, "IMPEDANCE analogy: electrical V = voltage, I = current | mechanical V = force, I = velocity. "
                    "Closed box: M_AB = M_A1 so M_MC = M_MS, and C_MT = C_MS/(1 + V_AS/V_B).  Filters designed on R_E.")
    params(s, W, M, order, -608)
    s.text(0, -448, ("b) set pol=-1 (midrange inverted) or try Q=0.5 (= LR2, slide 14):  ;.step param pol list 1 -1"
                     if order == 2 else "c) LR4 must be summed with the SAME polarity (pol=1); try fc = 300 or 350"))
    # ---- woofer row
    yw = 0
    s.vsrc(0, yw, "V_in", "AC 2.83"); s.flag(64, yw, "in"); s.wire(0, yw, 144, yw)
    x = filter_chain(s, 144, yw, "lp", order, "w", "vw")
    driver(s, x + 48, yw, "w", W, "woofer: electrical loop (I(Vdw) = i)          mechanical loop (I(Vmw) = u)")
    s.wire(x, yw, x + 48, yw)
    # ---- midrange row
    ym = 480
    s.flag(144, ym, "in")
    x = filter_chain(s, 144, ym, "hp", order, "m", "vm")
    driver(s, x + 48, ym, "m", M, "midrange: electrical loop (I(Vdm) = i)        mechanical loop (I(Vmm) = u)")
    s.wire(x, ym, x + 48, ym)
    # ---- the same filters loaded by R_E only (the lecture's ideal case, slide 26)
    yi = 960
    s.text(0, yi - 144, "the same two filters loaded by R_E only (what the textbook formulas assume): compare V(vw_id) with V(vw), V(vm_id) with V(vm)")
    s.flag(144, yi, "in"); x = filter_chain(s, 144, yi, "lp", order, "w", "vw_id"); s.wire(x, yi, x + 64, yi); s.vshunt("res", x + 64, yi, "R_idw", "{Rew}")
    xi = x + 256
    s.flag(xi, yi, "in"); x = filter_chain(s, xi, yi, "hp", order, "m", "vm_id"); s.wire(x, yi, x + 64, yi); s.vshunt("res", x + 64, yi, "R_idm", "{Rem}")
    # ---- outputs: velocity -> far-field pressure at 1 m, sum with the midrange polarity
    yo, xo = 1440, 160
    s.text(0, yo - 176, "far field at 1 m: p = j w rho S_D u / (2 pi r)  ->  E = rho*S_D/(2 pi) * s on the velocity.  "
                        "Sum p_tot = p_w + pol * p_m.  SPL in dB: plot V(pw)*5e4, V(pm)*5e4, V(ptot)*5e4")
    for i, (t, d) in enumerate((("w", W), ("m", M))):
        x0 = xo + i * 1040
        s.sym("h", "R0", x0, yo - 16, f"H_u{t}", f"Vm{t} 1", win=["WINDOW 0 24 40 Left 2", "WINDOW 3 24 72 Left 2"]); s.gnd(x0, yo + 80); s.flag(x0, yo, f"u{t}")
        s.e_src(x0 + 400, yo, f"E_p{t}", f"Laplace={RHO*d['Sd']/(2*math.pi):.6g}*s", f"u{t}"); s.flag(x0 + 400, yo, f"p{t}")
    xs = xo + 2160
    s.e_src(xs, yo, "E_pol", "{-pol}", "pm"); s.flag(xs, yo, "pmn")
    xt = xs + 400
    pins = s.sym("e", "R0", xt, yo - 16, "E_sum", "1")       # V(ptot) = V(pw) - V(pmn) = pw + pol*pm
    s.gnd(*pins[1]); s.flag(xt, yo, "ptot")
    (cpx, cpy), (cmx, cmy) = pins[2], pins[3]
    s.wire(cpx, cpy, cpx - 96, cpy); s.flag(cpx - 96, cpy, "pw")
    s.wire(cmx, cmy, cmx - 96, cmy); s.flag(cmx - 96, cmy, "pmn")
    s.text(0, yo + 208, ".ac dec 200 20 20k", directive=True)
    s.text(0, yo + 256, f"check: woofer |Z_E| peak {W['Zmax']:.0f} ohm at f_C = {W['fc']:.1f} Hz, midrange {M['Zmax']:.0f} ohm at {M['fc']:.1f} Hz.  "
                        f"Mid-band SPL at 2.83 V: woofer {W['spl']:.1f} dB, midrange {M['spl']:.1f} dB.  Z_in of a branch: V(in)/I(Vdw) is NOT it (the filter shunt draws current too)")
    s.dump(HERE / f"{name}.asc")
    g.plt(HERE / f"{name}.plt", [(["V(pw)*5e4", "V(pm)*5e4", "V(ptot)*5e4"], (1, 1e6)),
                                 (["V(vw)", "V(vw_id)", "V(vm)", "V(vm_id)"], (1e-3, 10))], (20, 20000))
    return HERE / f"{name}.asc"


def verify(files, W, M, plots=False):
    ok = True; runs = {}
    for order, asc in files.items():
        d = g.run_ltspice(asc); f = [v.real for v in d["frequency"]]; runs[order] = (f, d)
        worst = 0
        for j, fi in enumerate(f):
            r = system(W, M, fi, order)
            for key in ("vw", "vm", "vw_id", "vm_id", "pw", "pm", "ptot"):
                worst = max(worst, abs(d[f"v({key})"][j] / r[key] - 1))
        at = lambda fx: min(range(len(f)), key=lambda j: abs(f[j] - fx))
        good = worst < 2e-3; ok &= good
        k = at(250)
        print(f"  {'OK ' if good else 'BAD'} {asc.name}: worst deviation from the closed form {worst:.1e}; at 250 Hz: "
              f"|V(vw)| {abs(d['v(vw)'][k]):.3f} V vs ideal {abs(d['v(vw_id)'][k]):.3f} V, |V(vm)| {abs(d['v(vm)'][k]):.3f} V vs ideal {abs(d['v(vm_id)'][k]):.3f} V, "
              f"SPL total {20*math.log10(abs(d['v(ptot)'][k])/PREF):.1f} dB")
    print("ALL OK" if ok else "MISMATCH")
    if plots:
        make_plots(runs, W, M)
    return ok


def make_plots(runs, W, M):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    VAULT_IMG.mkdir(parents=True, exist_ok=True)
    db = lambda z: 20 * math.log10(max(abs(z), 1e-12))
    ph = lambda z: math.degrees(math.atan2(z.imag, z.real))
    COL = dict(w="#b4632c", m="#1f5fa8", t="#222222", alt="#c0392b")
    x = [10 ** (k / 100) for k in range(-200, 201)]
    # 1. Problem 2: the three crossover families, each summed both ways
    fig, axs = plt.subplots(2, 3, figsize=(12, 6), sharex=True)
    for c, (title, fn, best) in enumerate((("2nd-order Butterworth (Q = 0.707)", bw2tf, None), ("2nd-order Linkwitz-Riley (LR2)", lr2, -1),
                                           ("4th-order Linkwitz-Riley (LR4)", lr4, 1))):
        lo = [fn(v)[0] for v in x]; hi = [fn(v)[1] for v in x]
        ax = axs[0, c]
        ax.semilogx(x, [db(v) for v in lo], color=COL["w"], label="low-pass"); ax.semilogx(x, [db(v) for v in hi], color=COL["m"], label="high-pass")
        ax.semilogx(x, [db(a + b) for a, b in zip(lo, hi)], color=COL["t"], lw=2, label="sum, same polarity")
        ax.semilogx(x, [db(a - b) for a, b in zip(lo, hi)], color=COL["alt"], lw=2, ls="--", label="sum, high-pass inverted")
        ax.set(title=title, ylim=(-30, 6)); ax.grid(True, which="both", alpha=0.3)
        ax = axs[1, c]
        ax.semilogx(x, [ph(a + b) for a, b in zip(lo, hi)], color=COL["t"], lw=2)
        ax.semilogx(x, [ph(a - b) for a, b in zip(lo, hi)], color=COL["alt"], lw=2, ls="--")
        ax.set(xlabel="f / f$_c$", ylim=(-190, 190), yticks=range(-180, 181, 90)); ax.grid(True, which="both", alpha=0.3)
    axs[0, 0].set_ylabel("Magnitude [dB]"); axs[1, 0].set_ylabel("Phase of the sum [°]"); axs[0, 0].legend(fontsize=7, loc="lower left")
    fig.suptitle("Problems 9.1–9.2: ideal crossovers on a resistive load, summed with and without inverting the high-pass", fontsize=10)
    fig.tight_layout(); fig.savefig(VAULT_IMG / "P9_crossover_families.png", dpi=130); plt.close(fig)
    # 2. Problem 3: SPL for both polarities, BW2 and LR4
    for order, fname, title in ((2, "P9_3_BW2_SPL.png", "BW2 at 250 Hz"), (4, "P9_3_LR4_SPL.png", "LR4 at 250 Hz")):
        f, d = runs[order]
        fig, ax = plt.subplots(figsize=(8, 4.2))
        ax.semilogx(f, [db(v / PREF) for v in d["v(pw)"]], color=COL["w"], label="woofer (40 L)")
        ax.semilogx(f, [db(v / PREF) for v in d["v(pm)"]], color=COL["m"], label="midrange (2 L)")
        ax.semilogx(f, [db(v / PREF) for v in d["v(ptot)"]], color=COL["t"], lw=2, label="sum, same polarity (LTspice)")
        ax.semilogx(f, [db(system(W, M, fi, order, pol=-1)["ptot"] / PREF) for fi in f], color=COL["alt"], lw=1.6, ls="--", label="sum, midrange inverted")
        ax.axvline(250, color="grey", lw=0.8, ls=":")
        ax.set(xlabel="Frequency [Hz]", ylabel="SPL at 1 m for 2.83 V [dB]", title=f"Problems 9.3: {title}, filters designed on R$_E$", xlim=(20, 20000), ylim=(50, 110))
        ax.grid(True, which="both", alpha=0.3); ax.legend(fontsize=8, loc="lower center")
        fig.tight_layout(); fig.savefig(VAULT_IMG / fname, dpi=130); plt.close(fig)
    # 3. filter output voltage: real driver load vs R_E (slides 26-28)
    f, d = runs[2]
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.semilogx(f, [db(v / 2.83) for v in d["v(vw_id)"]], color=COL["w"], ls="--", lw=1, label="low-pass into R$_E$ (ideal)")
    ax.semilogx(f, [db(v / 2.83) for v in d["v(vw)"]], color=COL["w"], lw=2, label="low-pass into the woofer")
    ax.semilogx(f, [db(v / 2.83) for v in d["v(vm_id)"]], color=COL["m"], ls="--", lw=1, label="high-pass into R$_E$ (ideal)")
    ax.semilogx(f, [db(v / 2.83) for v in d["v(vm)"]], color=COL["m"], lw=2, label="high-pass into the midrange")
    ax.axvline(M["fc"], color=COL["m"], lw=0.8, ls=":"); ax.text(M["fc"] * 1.04, 5, f"mid f$_C$ {M['fc']:.0f} Hz", color=COL["m"], fontsize=8)
    ax.axvline(W["fc"], color=COL["w"], lw=0.8, ls=":"); ax.text(W["fc"] / 1.04, 5, f"woofer f$_C$ {W['fc']:.0f} Hz", color=COL["w"], fontsize=8, ha="right")
    ax.set(xlabel="Frequency [Hz]", ylabel="V$_{driver}$ / V$_{in}$ [dB]", title="Problems 9.3: the drivers are not resistors (BW2 at 250 Hz)", xlim=(20, 20000), ylim=(-40, 10))
    ax.grid(True, which="both", alpha=0.3); ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout(); fig.savefig(VAULT_IMG / "P9_3_filter_voltage.png", dpi=130); plt.close(fig)
    print("figures ->", VAULT_IMG)


if __name__ == "__main__":
    problem1(); problem2(); W, M = problem3()
    files = {2: build(W, M, 2), 4: build(W, M, 4)}
    if "--preview" in sys.argv:
        import preview_asc as pv
        pv.HERE = HERE
        [pv.main(str(p)) for p in files.values()]
    if "--verify" in sys.argv:
        sys.exit(0 if verify(files, W, M, "--plots" in sys.argv) else 1)
