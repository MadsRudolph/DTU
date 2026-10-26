#!/usr/bin/env python3
"""Lecture 10 (Advanced topics, 26-Oct-2026), slides 4-6: sound transmission through
a five-layer wall, drawn in LTspice the way the slides do it.

    python3 p10.py                   # print the closed-form checks, write the .asc/.plt
    python3 p10.py --verify          # also run LTspice headless and compare with the closed form
    python3 p10.py --verify --plots  # + figure in the vault Images/Lecture10/
    python3 p10.py --preview         # render the .asc to PNG (LTspice cannot export pictures headless)

Layers (slide 4 sketch, left to right): drywall 1 cm | insulation 3 cm | brick 5 cm |
air gap 1 cm | wood 2 cm. Per unit area, IMPEDANCE analogy: node voltage = pressure,
current = particle velocity, impedances in Pa s/m.

Row 1, slide 5 (LEM):        L = rho*l of each solid in series, C = l/(rho c^2) of each
                             soft layer to ground, R_out = rho0 c0.
Row 2, slide 6 top (mixed):  solids as L, insulation and air gap as lossless lines
                             T (Td = l/c, Z0 = rho c).
Row 3, slide 6 bottom (TMM): every layer a line.
Each row is driven by its own 1 V (= 1 Pa) source, so V(poutN) is the transmission.
Needs the Lab A builder: ../../Labs/Lab A/LTspice/gen_ltspice.py (the labs repo).
"""
import cmath, math, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
LABA = HERE.parents[1] / "Labs" / "Lab A" / "LTspice"
sys.path.insert(0, str(LABA))
import gen_ltspice as g                      # noqa: E402

# the T-line symbol (lib/sym/tline.asy): I1 (-48,-16), R1 (-48,16), I2 (48,-16), R2 (48,16)
g.PINS["tline"] = [(-48, -16), (-48, 16), (48, -16), (48, 16)]
VAULT_IMG = pathlib.Path.home() / "DTU/Obsidian/Courses/34870 Electroacoustics/Images/Lecture10"

RHO0, C0 = 1.2, 343.0
LAYERS = [  # name, rho, c, l
    ("drywall", 600.0, 6000.0, 0.01),
    ("insulation", 200.0, 500.0, 0.03),
    ("brick", 2000.0, 3600.0, 0.05),
    ("air", 1.2, 343.0, 0.01),
    ("wood", 550.0, 4000.0, 0.02),
]
ROUT = RHO0 * C0


# =====================================================================  closed form
def mm(a, b):
    return [[a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
            [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]]


def ser(z): return [[1, z], [0, 1]]
def shu(y): return [[1, 0], [y, 1]]


def line(w, i):
    _, rho, c, l = LAYERS[i]
    kl, z0 = w * l / c, rho * c
    return [[math.cos(kl), 1j * z0 * math.sin(kl)], [1j * math.sin(kl) / z0, math.cos(kl)]]


def mass(w, i): return ser(1j * w * LAYERS[i][1] * LAYERS[i][3])
def comp(w, i): return shu(1j * w * LAYERS[i][3] / (LAYERS[i][1] * LAYERS[i][2] ** 2))


def chain(w, model):
    parts = {"lem": [mass(w, 0), comp(w, 1), mass(w, 2), comp(w, 3), mass(w, 4)],
             "mix": [mass(w, 0), line(w, 1), mass(w, 2), line(w, 3), mass(w, 4)],
             "tmm": [line(w, i) for i in range(5)]}[model]
    t = parts[0]
    for p in parts[1:]:
        t = mm(t, p)
    return 1 / (t[0][0] + t[0][1] / ROUT)


def summary():
    print("Lecture 10, five-layer wall (slides 4-6)")
    m_tot = sum(r * l for _, r, _, l in LAYERS)
    print(f"  total mass {m_tot:.1f} kg/m^2 -> mass law at 20 Hz {20*math.log10(ROUT/(2*math.pi*20*m_tot)):.1f} dB "
          f"(LEM {20*math.log10(abs(chain(2*math.pi*20, 'lem'))):.1f}, TMM {20*math.log10(abs(chain(2*math.pi*20, 'tmm'))):.1f}; slide: about -30 dB)")
    for model in ("lem", "mix", "tmm"):
        f = [20 * 10 ** (k / 4000) for k in range(int(4000 * math.log10(1000)) + 1)]
        h = [abs(chain(2 * math.pi * fi, model)) for fi in f]
        pk = [f[k] for k in range(1, len(f) - 1) if h[k] > h[k - 1] and h[k] > h[k + 1]]
        print(f"  {model.upper():3s} peaks: " + ", ".join(f"{p:.0f} Hz" for p in pk))


# =====================================================================  schematic
def row(s, y, model, tag):
    """one model on a horizontal rail at height y; returns nothing, flags pout<tag>"""
    s.vsrc(0, y, f"P{tag}", "AC 1"); s.wire(0, y, 96, y); s.flag(96, y, f"pin{tag}")
    x = 96
    kinds = {"lem": ["L", "C", "L", "C", "L"], "mix": ["L", "T", "L", "T", "L"], "tmm": ["T"] * 5}[model]
    for i, k in enumerate(kinds):
        name = LAYERS[i][0]
        if k == "L":
            s.wire(x, y, x + 48, y)
            x = s.hser("ind", x + 48, y, f"M{i+1}_{tag}", f"{{Mm{i+1}}}", g.NOLOSS)
            s.wire(x, y, x + 48, y); x += 48
        elif k == "C":
            s.wire(x, y, x + 96, y); x += 96
            s.vshunt("cap", x, y, f"C{i+1}_{tag}", f"{{Ca{i+1}}}")
            s.wire(x, y, x + 96, y); x += 96
        else:
            s.wire(x, y, x + 48, y); x += 48
            s.sym("tline", "R0", x + 48, y + 16, f"T{i+1}_{tag}", f"Td={{l{i+1}/c{i+1}}} Z0={{r{i+1}*c{i+1}}}",
                  win=["WINDOW 0 0 -40 Center 2", "WINDOW 3 0 48 Center 1"])
            s.gnd(x, y + 32); s.gnd(x + 96, y + 32)
            x += 96; s.wire(x, y, x + 48, y); x += 48
        s.text(x - 128, y - 112, name, size=1)
    s.wire(x, y, x + 96, y); x += 96
    s.flag(x, y, f"pout{tag}")
    s.vshunt("res", x, y, f"Rout{tag}", "{r0*c0}")


def build():
    s = g.Sch()
    s.text(0, -480, "Lecture 10 (26-Oct-2026), slides 4-6: plane-wave transmission through drywall 1 cm | insulation 3 cm | brick 5 cm | air 1 cm | wood 2 cm")
    s.text(0, -448, "Per unit area, impedance analogy: V = pressure [Pa], I = particle velocity [m/s]. Solids = series mass rho*l, soft layers = shunt compliance l/(rho c^2) or a lossless line.")
    p = " ".join(f"r{i+1}={r:g} c{i+1}={c:g} l{i+1}={l:g}" for i, (_, r, c, l) in enumerate(LAYERS))
    s.text(0, -400, f".param {p} r0={RHO0} c0={C0}", directive=True)
    s.text(0, -368, ".param " + " ".join(f"Mm{i}={{r{i}*l{i}}}" for i in (1, 3, 5)) + " " +
           " ".join(f"Ca{i}={{l{i}/(r{i}*c{i}**2)}}" for i in (2, 4)), directive=True)
    s.text(0, -320, ".ac dec 2000 20 20k", directive=True)
    s.text(0, -272, "plot V(pout1), V(pout2), V(pout3) in dB: row 1 = LEM (slide 5), row 2 = LEM + TMM (slide 6 top), row 3 = full TMM (slide 6 bottom)")
    row(s, 0, "lem", "1")
    row(s, 400, "mix", "2")
    row(s, 800, "tmm", "3")
    asc = HERE / "P10_Wall_LEM_TMM.asc"
    s.dump(asc)
    g.plt(HERE / "P10_Wall_LEM_TMM.plt", [(["V(pout1)", "V(pout2)", "V(pout3)"], (1e-10, 1))], (20, 20000))
    return asc


def verify(asc, plots=False):
    d = g.run_ltspice(asc)
    f = [v.real for v in d["frequency"]]
    ok = True
    for tag, model in (("1", "lem"), ("2", "mix"), ("3", "tmm")):
        worst = max(abs(20 * math.log10(abs(d[f"v(pout{tag})"][j])) - 20 * math.log10(abs(chain(2 * math.pi * fi, model))))
                    for j, fi in enumerate(f))
        good = worst < 0.05; ok &= good
        print(f"  {'OK ' if good else 'BAD'} row {tag} ({model}): worst deviation from the closed form {worst:.2e} dB over {len(f)} points")
    print("ALL OK" if ok else "MISMATCH")
    if plots:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        VAULT_IMG.mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots(figsize=(8, 4.2))
        for tag, lab, ls in (("1", "LEM (slide 5)", "-"), ("2", "LEM + TMM (slide 6 top)", "--"), ("3", "full TMM (slide 6 bottom)", ":")):
            ax.semilogx(f, [20 * math.log10(abs(v)) for v in d[f"v(pout{tag})"]], ls=ls, lw=1.6, label=lab)
        ax.set(xlabel="Frequency [Hz]", ylabel="Transmission p$_{out}$/p$_{in}$ [dB]", xlim=(20, 20000), ylim=(-200, 0),
               title="Five-layer wall in LTspice (lecture 10, slides 5-6)")
        ax.grid(True, which="both", alpha=0.3); ax.legend(fontsize=8, loc="lower left")
        fig.tight_layout(); fig.savefig(VAULT_IMG / "L10_wall_transmission.png", dpi=130); plt.close(fig)
        print("figure ->", VAULT_IMG / "L10_wall_transmission.png")
    return ok


if __name__ == "__main__":
    summary()
    asc = build()
    print("wrote", asc.name)
    if "--preview" in sys.argv:
        import preview_asc as pv
        pv.HERE = HERE
        pv.main(str(asc))
    if "--verify" in sys.argv:
        sys.exit(0 if verify(asc, "--plots" in sys.argv) else 1)
