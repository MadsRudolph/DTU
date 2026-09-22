#!/usr/bin/env python3
"""TPS40200EVM-001 buck converter on a CISPR 16 LISN, as LTspice schematics.

    python3 gen_emc_ltspice.py          # write the .asc files next to this script
    python3 gen_emc_ltspice.py --run    # also batch-run LTspice (wine) and write results/*.png + *.csv

Schematics written:
    Buck_LISN_noFilter.asc    EVM straight on the LISN            (assignment step 1: calculate)
    Buck_LISN_withFilter.asc  the proposed input filter in between (assignment step 3: design)
    Filter_S21.asc            the filter alone in a 50 ohm system  (assignment step 4: what the network analyser will show)

The converter is open loop: the P-MOSFET is a voltage-controlled switch with a fixed duty
cycle D chosen so that V_out lands at 3.3 V. Nothing in the conducted-emission
spectrum depends on the control loop (its bandwidth is far below 300 kHz), so the
TPS40200 itself is not modelled. Keep it simple.
"""
import argparse, math, os, pathlib, shutil, struct, subprocess, sys, tempfile
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
RESULTS = HERE.parent / "results"
sys.path.insert(0, str(HERE.parent / "calc"))
import lisn_estimate as hand                                   # the pen-and-paper model, for comparison

# ---------------------------------------------------------------- operating point
FS = 300e3
T = 1 / FS
D = hand.D                                                     # ~0.32, includes the diode/RDS/DCR drops
T_START, N_PER = 2e-3, 40                                      # settle, then 40 periods for the FFT
T_EDGE = 30e-9                                                 # MOSFET switching edge
ESR1_BOM, ESR1_DS = 0.3, 0.03                                  # C1: BOM says 0.3 ohm, OS-CON datasheet ~0.03 ohm

# ---------------------------------------------------------------- the proposed filter (line side of the EVM)
FILTER = dict(Cf1="5u", Cf1_line="Rser=5m Lser=1n",           # a 10 uF X7R 1210 25 V part: ~5 uF left at 12 V bias, so 5 uF is what is simulated
              Cf2="100n", Cf2_line="Rser=20m Lser=0.5n",       # 100 nF 0603 for the top of the band
              Lf="22u", Lf_line="Rser=100m Cpar=5p Rpar=5k",   # 22 uH shielded power inductor, >= 1 A; Cpar/Rpar = its self-resonance (~15 MHz)
              Rd="2.2", Cd="47u", Cd_line="Rser=0.5")          # damping: cheap electrolytic + resistor
CPAR_HI, CPAR_LO = 10e-12, 1e-12                               # switch node to the reference plane: unknown, bracketed

# ---------------------------------------------------------------- LTspice .asc writer
PINS = {"res": [(16, 16), (16, 96)], "ind": [(16, 16), (16, 96)], "cap": [(16, 0), (16, 64)],
        "voltage": [(0, 16), (0, 96)], "schottky": [(16, 0), (16, 64)],
        "sw": [(0, 16), (0, 96), (-48, 80), (-48, 32)]}
ROT = {"R0": lambda x, y: (x, y), "R90": lambda x, y: (-y, x), "R180": lambda x, y: (-x, -y), "R270": lambda x, y: (y, -x)}
WIN_ABOVE = ["WINDOW 0 -30 56 VBottom 2", "WINDOW 3 -2 56 VBottom 2"]
WIN_BELOW = ["WINDOW 0 38 56 VTop 2", "WINDOW 3 66 56 VTop 2"]


class Sch:
    def __init__(self):
        self.lines = []

    def wire(self, x1, y1, x2, y2):
        if (x1, y1) != (x2, y2):
            self.lines.append(f"WIRE {x1} {y1} {x2} {y2}")

    def flag(self, x, y, name):
        self.lines.append(f"FLAG {x} {y} {name}")

    def gnd(self, x, y):
        self.flag(x, y, "0")

    def sym(self, kind, rot, ox, oy, name, value, spiceline=None, win=None):
        out = [f"SYMBOL {kind} {ox} {oy} {rot}"] + (win or [])
        out.append(f"SYMATTR InstName {name}")
        out.append(f"SYMATTR Value {value}")
        if spiceline:
            out.append(f"SYMATTR SpiceLine {spiceline}")
        self.lines += out
        r = ROT[rot]
        return [(ox + r(*p)[0], oy + r(*p)[1]) for p in PINS[kind]]

    def text(self, x, y, txt, directive=False, size=2):
        self.lines.append(f"TEXT {x} {y} Left {size} {'!' if directive else ';'}" + txt.replace("\n", "\\n"))

    # vertical element with its top pin at (x, y); returns the bottom pin
    def vcap(self, x, y, name, value, spiceline=None):
        return self.sym("cap", "R0", x - 16, y, name, value, spiceline)[1]

    def vres(self, x, y, name, value, spiceline=None):
        return self.sym("res", "R0", x - 16, y - 16, name, value, spiceline)[1]

    # horizontal element with its left pin at (xl, y); returns the right pin
    def hind(self, xl, y, name, value, spiceline=None, win=WIN_ABOVE):
        self.sym("ind", "R90", xl + 96, y - 16, name, value, spiceline, win)
        return (xl + 80, y)

    def hres(self, xl, y, name, value, spiceline=None, win=WIN_ABOVE):
        self.sym("res", "R90", xl + 96, y - 16, name, value, spiceline, win)
        return (xl + 80, y)

    def dump(self, path):
        pathlib.Path(path).write_text("\n".join(["Version 4", "SHEET 1 2200 1000"] + self.lines) + "\n")


def tran_directives(s, x, y, esr1):  # placed below the LISN return branch
    s.text(x, y, f".param Fs={FS:g} D={D:.4f} ESR1={esr1:g} Cpar={CPAR_HI:g}", True)
    s.text(x, y + 32, f".tran 0 {T_START + N_PER / FS:.7g} {T_START:g} 2n", True)
    s.text(x, y + 64, ".options plotwinsize=0 numdgt=7", True)
    s.text(x, y + 96, ".model MYSW SW(Ron=75m Roff=10Meg Vt=0.5 Vh=-0.4)", True)
    s.text(x, y + 128, ".model MBRS330 D(Is=1.7u Rs=30m N=1.05 Cjo=250p Vj=0.4 M=0.5 Eg=0.69 Xti=2 Bv=30)", True)
    s.text(x, y + 160, ".save V(meas1) V(meas2) V(dut_p) V(dut_n) V(sw) V(out) I(L1) I(L_lisn1) I(S1) I(Cpar)", True)


def lisn(s):
    """CISPR 16-1-2 50 ohm / 50 uH V-network, one per line. Line 1 on y=0, the return on y=320."""
    s.sym("voltage", "R0", 0, -16, "V_supply", "12", win=["WINDOW 0 -24 16 Right 2", "WINDOW 3 -24 96 Right 2"])
    s.gnd(0, 80)
    s.wire(0, 0, 64, 0)
    s.hind(64, 0, "L_lisn1", "50u", "Rser=10m")
    s.wire(144, 0, 240, 0)
    b = s.vcap(176, 0, "C_lisn1", "0.1u")
    s.wire(b[0], b[1], b[0] - 48, b[1]); s.flag(b[0] - 48, b[1], "meas1")
    r = s.vres(b[0], b[1], "R_meas1", "50")
    s.gnd(*r)
    s.gnd(64, 320)                                              # supply return = earth
    s.hind(64, 320, "L_lisn2", "50u", "Rser=10m")
    s.wire(144, 320, 240, 320)
    b = s.vcap(176, 320, "C_lisn2", "0.1u")
    s.wire(b[0], b[1], b[0] - 48, b[1]); s.flag(b[0] - 48, b[1], "meas2")
    r = s.vres(b[0], b[1], "R_meas2", "50")
    s.gnd(*r)
    s.text(-8, -260, "CISPR 16 LISN, 50 ohm / 50 uH per line\nreceiver on meas1 (other line terminated in 50 ohm)")
    return 240                                                  # x where the line continues


def input_filter(s, x):
    """line-side caps + damping, then the series inductor. Returns the x after the filter."""
    s.wire(x, 0, x + 336, 0); s.wire(x, 320, x + 464, 320)
    b = s.vcap(x + 48, 0, "C_f2", FILTER["Cf2"], FILTER["Cf2_line"]); s.wire(b[0], b[1], b[0], 320)
    b = s.vcap(x + 160, 0, "C_f1", FILTER["Cf1"], FILTER["Cf1_line"]); s.wire(b[0], b[1], b[0], 320)
    b = s.vres(x + 272, 0, "R_d", FILTER["Rd"]); b = s.vcap(b[0], b[1], "C_d", FILTER["Cd"], FILTER["Cd_line"]); s.wire(b[0], b[1], b[0], 320)
    s.hind(x + 336, 0, "L_f", FILTER["Lf"], FILTER["Lf_line"])
    s.wire(x + 416, 0, x + 464, 0)
    s.text(x + 128, 400, "proposed input filter\n(pi with the EVM's own C1 as the converter-side capacitor)")
    return x + 464


def evm(s, x):
    """the TPS40200EVM-001 power stage, from the input terminals at x."""
    s.wire(x, 0, x + 336, 0); s.wire(x, 320, x + 832, 320)
    s.flag(x, 0, "dut_p"); s.flag(x, 320, "dut_n")
    b = s.vcap(x + 64, 0, "C1", "100u", "Rser={ESR1} Lser=5n"); s.wire(b[0], b[1], b[0], 320)
    b = s.vcap(x + 176, 0, "C2", "0.6u", "Rser=10m Lser=0.6n"); s.wire(b[0], b[1], b[0], 320)
    s.hres(x + 256, 0, "R2", "0.02")
    p = s.sym("sw", "R0", x + 416, -16, "S1", "MYSW", win=["WINDOW 0 24 16 Left 2", "WINDOW 3 24 48 Left 2"])   # A on the rail, B = switch node
    s.wire(x + 336, 0, x + 416, 0)
    nc_p, nc_m = p[2], p[3]                                     # control pins, left of the switch
    s.wire(nc_p[0], nc_p[1], nc_p[0], 224); s.flag(nc_p[0], 224, "gate")
    s.wire(nc_m[0], nc_m[1], nc_m[0] - 32, nc_m[1]); s.wire(nc_m[0] - 32, nc_m[1], nc_m[0] - 32, 160); s.gnd(nc_m[0] - 32, 160)
    sw = p[1]
    s.wire(sw[0], sw[1], x + 672, 80)
    s.flag(x + 432, 80, "sw")
    b = s.vcap(x + 480, 80, "Cpar", "{Cpar}"); s.gnd(*b)       # switch node to the reference plane: the CM source
    d = s.sym("schottky", "R180", x + 576, 144, "D2", "MBRS330", win=["WINDOW 0 -24 64 Right 2", "WINDOW 3 -24 32 Right 2"])
    s.wire(d[0][0], d[0][1], d[0][0], 320)                       # cathode up on the switch node, anode to the return
    s.hind(x + 672, 80, "L1", "33u", "Rser=39m")
    s.wire(x + 752, 80, x + 912, 80)
    s.flag(x + 768, 80, "out")
    b = s.vcap(x + 800, 80, "C12", "220u", "Rser=0.4 Lser=5n"); s.wire(b[0], b[1], b[0], 320)
    b = s.vcap(x + 912, 80, "C11", "1u", "Rser=10m Lser=0.6n"); s.wire(b[0], b[1], b[0], 320)
    s.wire(x + 912, 80, x + 1024, 80); s.wire(x + 832, 320, x + 1024, 320)
    b = s.vres(x + 1024, 80, "R_load", "1.65"); s.wire(b[0], b[1], b[0], 320)
    # gate drive, referenced to earth (the switch only cares about V(NC+) - V(NC-))
    g = s.sym("voltage", "R0", x + 1136, 64, "V_gate", f"PULSE(0 1 0 {T_EDGE:g} {T_EDGE:g} {{D/Fs-{T_EDGE:g}}} {{1/Fs}})")
    s.wire(g[0][0], g[0][1], g[0][0], g[0][1] - 32); s.flag(g[0][0], g[0][1] - 32, "gate"); s.gnd(*g[1])
    s.text(x, -170, "TPS40200EVM-001 power stage, open loop (fixed duty cycle D)\nC1 ESR: BOM 0.3 ohm, OS-CON datasheet ~0.03 ohm -> .param ESR1")
    s.text(x + 1104, 200, "gate pulse: D*T high, 30 ns edges")
    return x + 1136


def buck_on_lisn(with_filter, esr1=ESR1_BOM):
    s = Sch()
    x = lisn(s)
    if with_filter:
        x = input_filter(s, x)
    x_end = evm(s, x)
    tran_directives(s, 0, 520, esr1)
    return s


def filter_s21():
    """the filter as a 2-port in a 50 ohm system, port 1 = line side, port 2 = converter side"""
    s = Sch()
    v = s.sym("voltage", "R0", 0, -16, "V1", "AC 1", "Rser=50")
    s.gnd(*v[1])
    s.wire(0, 0, 64, 0)
    s.flag(64, 0, "in")
    x = 64
    s.wire(x, 0, x + 336, 0)
    b = s.vcap(x + 48, 0, "C_f2", FILTER["Cf2"], FILTER["Cf2_line"]); s.gnd(*b)
    b = s.vcap(x + 160, 0, "C_f1", FILTER["Cf1"], FILTER["Cf1_line"]); s.gnd(*b)
    b = s.vres(x + 272, 0, "R_d", FILTER["Rd"]); b = s.vcap(b[0], b[1], "C_d", FILTER["Cd"], FILTER["Cd_line"]); s.gnd(*b)
    s.hind(x + 336, 0, "L_f", FILTER["Lf"], FILTER["Lf_line"])
    s.wire(x + 416, 0, x + 512, 0)
    s.flag(x + 448, 0, "out")
    b = s.vres(x + 512, 0, "R_port2", "50"); s.gnd(*b)
    s.text(0, 240, ".ac dec 200 1k 100Meg", True)
    s.text(0, 272, ".save V(out)", True)
    s.text(0, -170, "S21 of the input filter in a 50 ohm system = 2*V(out)   (what the network analyser measures)\nnote: the real attenuation on the LISN is larger, the converter side is not 50 ohm")
    return s


def write_all():
    buck_on_lisn(False).dump(HERE / "Buck_LISN_noFilter.asc")
    buck_on_lisn(True).dump(HERE / "Buck_LISN_withFilter.asc")
    filter_s21().dump(HERE / "Filter_S21.asc")
    print("wrote Buck_LISN_noFilter.asc, Buck_LISN_withFilter.asc, Filter_S21.asc")


# ---------------------------------------------------------------- run LTspice headless
def run_ltspice(asc, param_override=None):
    env = dict(os.environ, WINEARCH="win64", WINEPREFIX=os.path.expanduser("~/.local/share/wineprefixes/ltspice"), WINEDEBUG="-all")
    exe = "/usr/share/ltspice/LTspice.exe"
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="ltemc_"))
    work = tmp / asc.name
    txt = asc.read_text()
    if param_override:
        for k, v in param_override.items():
            import re
            txt = re.sub(rf"\b{k}=[-+0-9.eEgu]+", f"{k}={v:g}", txt)
    work.write_text(txt)
    wp = lambda q: subprocess.run(["winepath", "-w", str(q)], env=env, capture_output=True, text=True).stdout.strip()
    subprocess.run(["wine", exe, "-netlist", wp(work)], env=env, capture_output=True, timeout=120)
    net = work.with_suffix(".net")
    if not net.exists():
        raise SystemExit(f"netlisting failed for {asc.name}")
    subprocess.run(["wine", exe, "-b", wp(net)], env=env, capture_output=True, timeout=900)
    raw = work.with_suffix(".raw")
    if not raw.exists():
        log = work.with_suffix(".log")
        raise SystemExit(f"simulation failed for {asc.name}:\n" + (log.read_bytes().decode("utf-16le", "ignore") if log.exists() else "no log"))
    cols = read_raw(raw)
    shutil.rmtree(tmp, ignore_errors=True)
    return cols


def read_raw(path):
    b = path.read_bytes(); key = "Binary:\n".encode("utf-16le"); i = b.find(key)
    head = b[:i].decode("utf-16le"); data = b[i + len(key):]
    names, invars, npts, is_ac, offset = [], False, 0, False, 0.0
    for ln in head.splitlines():
        if ln.startswith("No. Points:"): npts = int(ln.split(":")[1])
        if ln.startswith("Offset:"): offset = float(ln.split(":")[1])   # a late-starting .tran stores time relative to this
        if ln.startswith("Plotname:") and "AC" in ln: is_ac = True
        if ln.startswith("Variables:"): invars = True; continue
        if invars and ln.strip(): names.append(ln.split()[1].lower())
    nv = len(names)
    if is_ac:
        vals = np.frombuffer(data[:npts * nv * 16], dtype="<f8").reshape(npts, nv, 2)
        arr = vals[:, :, 0] + 1j * vals[:, :, 1]
    elif len(data) >= npts * nv * 8:                             # numdgt > 6: everything double
        arr = np.frombuffer(data[:npts * nv * 8], dtype="<f8").reshape(npts, nv).astype(float)
    else:                                                        # default: time double, the rest float32
        rec = np.dtype([("t", "<f8")] + [(f"v{k}", "<f4") for k in range(nv - 1)])
        r = np.frombuffer(data[:npts * rec.itemsize], dtype=rec)
        arr = np.column_stack([r["t"]] + [r[f"v{k}"] for k in range(nv - 1)])
    cols = {n: arr[:, k] for k, n in enumerate(names)}
    if not is_ac:
        cols["time"] = np.abs(cols["time"]) + offset
    return cols


def harmonics(t, v, nmax=100):
    """RMS amplitude of the harmonics of FS from the last N_PER periods, resampled to a uniform grid"""
    t0 = T_START; t1 = T_START + N_PER / FS
    n = int(round((t1 - t0) / 1e-9)); tu = t0 + np.arange(n) * 1e-9
    vu = np.interp(tu, t, v)
    w = np.hanning(n)                                        # exact for on-bin tones (coherent gain 0.5), kills the leakage of any slow settling
    X = np.fft.rfft((vu - vu.mean()) * w) * 2 / w.sum()
    return np.array([abs(X[k * N_PER]) / math.sqrt(2) for k in range(1, nmax + 1)])


def dbuv(v):
    return 20 * np.log10(np.maximum(v, 1e-12) / 1e-6)


def report(label, ns, sim, est=None):
    print(f"\n{label}")
    print(f"{'n':>3} {'f/MHz':>7} {'sim dBuV':>9} " + (f"{'hand dBuV':>10} " if est is not None else "") + f"{'QP limit':>9} {'margin':>7}")
    for n in ns:
        lim = hand.en55022_class_b(n * FS)
        row = f"{n:3d} {n*FS/1e6:7.2f} {sim[n-1]:9.1f} "
        if est is not None:
            row += f"{est[n-1]:10.1f} "
        print(row + f"{lim:9.1f} {lim - sim[n-1]:+7.1f}")


def run_all():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    RESULTS.mkdir(exist_ok=True)
    ns_tab = list(range(1, 9)) + list(range(95, 101))
    nall = np.arange(1, 101); fall = nall * FS
    fl = np.logspace(math.log10(150e3), math.log10(30e6), 400)
    qp = [hand.en55022_class_b(x) for x in fl]; av = [hand.en55022_class_b(x, "av") for x in fl]

    def limits(ax):
        ax.plot(fl / 1e6, qp, "r-", lw=1.6, label="EN 55022 B quasi-peak")
        ax.plot(fl / 1e6, av, "r--", lw=1.2, label="EN 55022 B average")
        ax.set_xscale("log"); ax.set_xlim(0.15, 30); ax.set_ylim(-20, 120)
        ax.set_xlabel("f / MHz"); ax.set_ylabel("V(meas1) / dBµV"); ax.grid(True, which="both", alpha=.3)

    # ---- the transient cases: (schematic, C1 ESR, Cpar)
    cases = [("noFilter", ESR1_BOM, CPAR_HI), ("noFilter", ESR1_DS, CPAR_HI), ("noFilter", ESR1_BOM, CPAR_LO),
             ("withFilter", ESR1_BOM, CPAR_HI), ("withFilter", ESR1_BOM, CPAR_LO)]
    out = {}
    for kind, esr, cpar in cases:
        d = run_ltspice(HERE / f"Buck_LISN_{kind}.asc", {"ESR1": esr, "Cpar": cpar})
        t = d["time"]; vout = d["v(out)"] - d["v(dut_n)"]; vin = d["v(dut_p)"] - d["v(dut_n)"]
        sel = t >= T_START
        first, last = (t >= T_START) & (t < T_START + 5 * T), t >= T_START + (N_PER - 5) * T
        tag = f"{kind}, C1 ESR = {esr:g} ohm, Cpar = {cpar*1e12:g} pF"
        print(f"\n{tag}: settling V_out {vout[first].mean():.4f} -> {vout[last].mean():.4f} V, V_in {vin[first].mean():.4f} -> {vin[last].mean():.4f} V")
        print(f"   V_out mean {vout[sel].mean():.3f} V, ripple {np.ptp(vout[sel])*1e3:.0f} mVpp, I_in mean {-d['i(l_lisn1)'][sel].mean():.3f} A, "
              f"V(meas1) {np.ptp(d['v(meas1)'][sel])*1e3:.0f} mVpp")
        h = dbuv(harmonics(t, d["v(meas1)"]))
        est = np.array([hand.lisn_dbuv(n, esr)[0] for n in nall]) if kind == "noFilter" else None
        report(tag + (" (LTspice vs hand estimate)" if est is not None else ""), ns_tab, h, est)
        out[(kind, esr, cpar)] = (d, h)
        cols = [nall, fall, h] + ([est] if est is not None else [])
        np.savetxt(RESULTS / f"spectrum_{kind}_esr{esr:g}_cpar{cpar*1e12:g}p.csv", np.column_stack(cols), delimiter=",",
                   header="n,f_Hz,ltspice_dBuV" + (",hand_dBuV" if est is not None else ""), comments="", fmt="%g")

    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    limits(ax)
    for (esr, cpar), c in (((ESR1_BOM, CPAR_HI), "C0"), ((ESR1_DS, CPAR_HI), "C1"), ((ESR1_BOM, CPAR_LO), "C4")):
        d, h = out[("noFilter", esr, cpar)]
        ax.stem(fall / 1e6, h, linefmt=c + "-", markerfmt=c + "o", basefmt=" ", label=f"LTspice, C1 ESR = {esr:g} Ω, Cpar = {cpar*1e12:g} pF")
        if cpar == CPAR_HI:
            est = np.array([hand.lisn_dbuv(n, esr)[0] for n in nall])
            ax.plot(fall / 1e6, est, c + "x", ms=5, alpha=.7, label=f"hand estimate, ESR = {esr:g} Ω")
    ax.set_title("TPS40200EVM-001 on the LISN, no filter: predicted conducted emission")
    ax.legend(loc="upper right", fontsize=8); fig.tight_layout(); fig.savefig(RESULTS / "spectrum_nofilter.png", dpi=150)

    # ---- time domain, for the slides
    d = out[("noFilter", ESR1_BOM, CPAR_HI)][0]; t = d["time"]; sel = (t >= T_START) & (t <= T_START + 3 * T)
    fig, axs = plt.subplots(3, 1, figsize=(8.5, 6.5), sharex=True)
    tt = (t[sel] - T_START) * 1e6
    axs[0].plot(tt, d["v(sw)"][sel] - d["v(dut_n)"][sel]); axs[0].set_ylabel("V(sw) / V")
    axs[1].plot(tt, -d["i(s1)"][sel], label="MOSFET current"); axs[1].plot(tt, -d["i(l_lisn1)"][sel], label="current from the LISN")
    axs[1].set_ylabel("I / A"); axs[1].legend(fontsize=8)
    axs[2].plot(tt, (d["v(meas1)"][sel]) * 1e3); axs[2].set_ylabel("V(meas1) / mV"); axs[2].set_xlabel("t / µs")
    axs[0].set_title("no filter: the MOSFET draws 2 A pulses, C1 supplies them, the LISN sees the ripple + the edge spikes", fontsize=10)
    for a in axs: a.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(RESULTS / "waveforms_nofilter.png", dpi=150)

    # ---- with the filter
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    limits(ax)
    ax.stem(fall / 1e6, out[("noFilter", ESR1_BOM, CPAR_HI)][1], linefmt="C0-", markerfmt="C0o", basefmt=" ", label="no filter (ESR 0.3 Ω, Cpar 10 pF)")
    for cpar, c in ((CPAR_HI, "C2"), (CPAR_LO, "C8")):
        ax.stem(fall / 1e6, out[("withFilter", ESR1_BOM, cpar)][1], linefmt=c + "-", markerfmt=c + "o", basefmt=" ",
                label=f"with filter, Cpar = {cpar*1e12:g} pF")
    ax.set_title(f"With the proposed filter: L = {FILTER['Lf']}H, {FILTER['Cf1']}F (10 µF X7R derated) ‖ {FILTER['Cf2']}F ‖ {FILTER['Rd']} Ω + {FILTER['Cd']}F", fontsize=10)
    ax.legend(loc="upper right", fontsize=8); fig.tight_layout(); fig.savefig(RESULTS / "spectrum_withfilter.png", dpi=150)

    # ---- the filter alone, 50 ohm system
    d = run_ltspice(HERE / "Filter_S21.asc")
    f = d["frequency"].real; s21 = 20 * np.log10(np.abs(2 * d["v(out)"]))
    np.savetxt(RESULTS / "filter_s21.csv", np.column_stack([f, s21]), delimiter=",", header="f_Hz,S21_dB", comments="", fmt="%g")
    fig, ax = plt.subplots(figsize=(8.5, 4))
    ax.semilogx(f / 1e6, s21, "C2")
    for n in (1, 2, 4, 5):
        k = np.argmin(abs(f - n * FS)); ax.plot(f[k] / 1e6, s21[k], "ko", ms=4); ax.annotate(f"{s21[k]:.0f} dB", (f[k] / 1e6, s21[k]), textcoords="offset points", xytext=(5, 5), fontsize=8)
    ax.set_xlim(1e-3, 100); ax.set_xlabel("f / MHz"); ax.set_ylabel("S21 / dB"); ax.grid(True, which="both", alpha=.3)
    ax.set_title("Input filter alone, 50 Ω source and load (network-analyser view)")
    fig.tight_layout(); fig.savefig(RESULTS / "filter_s21.png", dpi=150)
    k = [np.argmin(abs(f - x)) for x in (FS, 1e6, 10e6, 30e6)]
    print("\nfilter S21 in 50 ohm: " + ", ".join(f"{f[i]/1e6:g} MHz: {s21[i]:.1f} dB" for i in k))
    print(f"\nplots in {RESULTS}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true", help="batch-run LTspice under wine and make the plots")
    a = ap.parse_args()
    write_all()
    if a.run:
        run_all()
