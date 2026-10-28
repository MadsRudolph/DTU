#!/usr/bin/env python3
"""Lecture 11 (Finn Agerkvist, Mon 2-Nov-2026): radiation, acoustic environment, micro-speakers
and nonlinear circuit models. Written BEFORE the lecture from the course plan's reading
(Beranek & Mellow 2019: 6.18, 8.1-8.3, 13.7) and the System D woofer we measured in Lab D.

    python3 p11.py                   # print every number used in the pre-read note
    python3 p11.py --verify          # also run the nonlinear LTspice netlist headless and compare
    python3 p11.py --verify --plots  # + figures in the vault Images/Lecture11/

Part A  piston in an infinite baffle: directivity, beamwidth, first null, axial near field.
Part B  acoustic environment: solid angle (4pi/2pi/pi/pi/2), baffle step, room critical distance.
Part C  micro-speaker: why the bass is gone, back volume, front-cavity Helmholtz low-pass.
Part D  nonlinear lumped model of the Scan-Speak 26W/8534G00 (Bl(x), K(x), Le(x)), integrated
        in Python (RK4) and in LTspice (B-sources, P11_Nonlinear_Woofer.cir); harmonics,
        DC offset, intermodulation.

The driver values are the Lab D fit (Project/ltspice/task1/box_model.py): Bl 8.28 Tm,
M_MD 36.7 g, C_MS 1.174 mm/N, R_MS 0.61 kg/s, L_E 1.50 mH, R_E 5.7 ohm. The data sheet gives
coil height 18 mm and gap height 6 mm, so X_max = (18 - 6)/2 = 6 mm (overhung, "linear
excursion +/-6 mm"). The SHAPES of Bl(x), K(x), Le(x) are assumptions (no Klippel data for
this unit): Bl falls to 82 % and C_MS to 75 % at X_max (Klippel's X_max criteria).
"""
import math, os, pathlib, struct, subprocess, sys
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
VAULT_IMG = pathlib.Path.home() / "DTU/Obsidian/Courses/34870 Electroacoustics/Images/Lecture11"
RHO, C = 1.204, 343.2            # 20 C, same as the project fit


def J1(x, n=400):
    """Bessel J1 by its integral (no scipy on this PC): (1/pi) int_0^pi cos(t - x sin t) dt."""
    t = (np.arange(n) + 0.5) * math.pi / n
    return np.cos(t[None, :] - np.atleast_1d(x)[:, None] * np.sin(t[None, :])).mean(axis=1)


def H1(x, n=400):
    """Struve H1: (2x/pi) int_0^1 sqrt(1-t^2) sin(x t) dt."""
    t = (np.arange(n) + 0.5) / n
    x = np.atleast_1d(x)
    return 2 * x / math.pi * (np.sqrt(1 - t[None, :] ** 2) * np.sin(x[:, None] * t[None, :])).mean(axis=1)


def db(x): return 20 * np.log10(np.abs(x))


# =====================================================================  part A: piston
A_W = math.sqrt(0.0350 / math.pi)  # woofer, S_D = 350 cm^2 -> a = 105.5 mm


def directivity(ka, th):
    """Far-field pressure of a baffled piston relative to on-axis: 2 J1(v)/v, v = ka sin(theta)."""
    v = ka * np.sin(th)
    v = np.where(np.abs(v) < 1e-9, 1e-9, v)
    return 2 * J1(v.ravel()).reshape(v.shape) / v


def part_a():
    print("\n=== A. piston in an infinite baffle (Beranek 13.7), woofer a = %.1f mm" % (A_W * 1e3))
    f1 = C / (2 * math.pi * A_W)
    print(f"ka = 1 at f = c/(2 pi a) = {f1:.0f} Hz   (lambda = {C / f1 * 100:.0f} cm = circumference)")
    print(f"first null on the side (ka sin90 = 3.832) appears above f = {3.832 * f1:.0f} Hz")
    th = np.radians(np.linspace(0, 90, 9001))
    for f in (100, 500, 1000, 1500, 2000, 3000):
        ka = 2 * math.pi * f / C * A_W
        d = db(directivity(ka, th))
        i6 = np.argmax(d < -6.0)
        bw = f"+/-{np.degrees(th[i6]):.0f} deg" if d.min() < -6 else "wider than 180 deg"
        print(f"  {f:5d} Hz  ka = {ka:4.2f}   -6 dB beamwidth {bw:18s}  at 90 deg {d[-1]:6.1f} dB")
    # low-frequency radiation impedance (front face)
    MA1 = 8 * RHO / (3 * math.pi ** 2 * A_W)
    print(f"M_A1 = 8 rho/(3 pi^2 a) = {MA1:.2f} kg/m^4 -> mechanical {MA1 * 0.035 ** 2 * 1e3:.2f} g per face"
          f" (x2 faces in a baffle = {2 * MA1 * 0.035 ** 2 * 1e3:.1f} g)")
    # Rayleigh distance and axial near field
    for f in (1000, 3000, 5000, 10000):
        lam = C / f
        rmax = (A_W ** 2 - lam ** 2 / 4) / lam  # last axial max: sqrt(r^2+a^2) - r = lambda/2
        nz = int(A_W // lam)                    # axial zeros: sqrt(r^2+a^2) - r = n lambda <= a
        last = f"last axial max at r = {rmax * 100:.1f} cm" if rmax > 0 else "no axial max (lambda > 2a)"
        print(f"  {f} Hz: Rayleigh distance pi a^2/lambda = {math.pi * A_W ** 2 / lam * 100:.1f} cm, {last}, {nz} axial zero(s)")
    return f1


# =====================================================================  part B: environment
def part_b():
    print("\n=== B. acoustic environment")
    print("small source with fixed volume velocity U into solid angle Omega:")
    print("   p = j w rho U / (Omega r),   R_A = rho c k^2 / Omega,   W = |U|^2 R_A")
    for name, om in (("free field 4pi", 4 * math.pi), ("one wall 2pi", 2 * math.pi),
                     ("wall+floor pi", math.pi), ("corner pi/2", math.pi / 2)):
        print(f"  {name:15s}  SPL {20 * math.log10(4 * math.pi / om):+5.1f} dB   power {10 * math.log10(4 * math.pi / om):+5.1f} dB")
    W = 0.45
    print(f"baffle step for the System D box (front {W * 100:.0f} cm wide): f ~ c/(pi W) = {C / (math.pi * W):.0f} Hz"
          f"  (Lab E: box 5.7 dB under the screens at 250-600 Hz)")
    V, T = 100.0, 0.5
    A = 0.161 * V / T
    for Q in (1, 2, 4):
        print(f"  room V = {V:.0f} m^3, T60 = {T} s: A = {A:.1f} m^2 sabine,"
              f" critical distance (Q = {Q}) r_c = sqrt(Q A / 16 pi) = {math.sqrt(Q * A / (16 * math.pi)):.2f} m")


# =====================================================================  part C: micro-speaker
MS = dict(RE=7.0, Bl=0.75, Mms=0.11e-3, fs=800.0, a=0.0062, Vb=1.0e-6,  # typical 15x11 mm unit,
          Vf=0.10e-6, ah=0.6e-3, lh=0.8e-3, nh=1)                       # illustrative values


def part_c():
    print("\n=== C. micro-speaker (illustrative values, Beranek ch. 8)")
    m = MS
    Sd = math.pi * m["a"] ** 2
    Cms = 1 / ((2 * math.pi * m["fs"]) ** 2 * m["Mms"])
    Cab = m["Vb"] / (RHO * C ** 2)
    Cmb = Cab / Sd ** 2
    Ctot = 1 / (1 / Cms + 1 / Cmb)
    fc = 1 / (2 * math.pi * math.sqrt(m["Mms"] * Ctot))
    Vas = Cms * Sd ** 2 * RHO * C ** 2
    print(f"S_D = {Sd * 1e4:.2f} cm^2, V_AS = {Vas * 1e6:.2f} cm^3, back volume {m['Vb'] * 1e6:.1f} cm^3"
          f" -> alpha = V_AS/V_B = {Vas / m['Vb']:.2f}, f_c = {fc:.0f} Hz (f_s {m['fs']:.0f} Hz)")
    for f in (100, 200, 500, 1000):
        r, Lp = 0.10, 90.0
        prms = 20e-6 * 10 ** (Lp / 20)
        w = 2 * math.pi * f
        U = prms * 2 * math.pi * r / (RHO * w)     # half space (phone on a table)
        x = U / (w * Sd) * math.sqrt(2) * 1e3      # peak, mm
        print(f"  {Lp:.0f} dB SPL at {r * 100:.0f} cm, {f:4d} Hz, 2pi space: x_peak = {x:6.3f} mm")
    # front cavity + sound hole = Helmholtz low-pass (Beranek eq. 8.1-8.3, flanged both ends 1.7)
    zeta = 1.7
    Mah = RHO * (m["lh"] + zeta * m["ah"]) / (m["nh"] * math.pi * m["ah"] ** 2)
    Caf = m["Vf"] / (RHO * C ** 2)
    f0 = 1 / (2 * math.pi * math.sqrt(Mah * Caf))
    print(f"front cavity {m['Vf'] * 1e6:.2f} cm^3 + hole r {m['ah'] * 1e3:.1f} mm, l {m['lh'] * 1e3:.1f} mm:"
          f" M_AH = {Mah:.0f} kg/m^4, C_AF = {Caf:.2e} m^5/N, f_0 = {f0:.0f} Hz")


# =====================================================================  part D: nonlinear woofer
RE, LE0, BL0, MMD, CMS0, RMS = 5.7, 1.50e-3, 8.28, 36.7e-3, 1.174e-3, 0.61
SD = 0.0350
MA1 = 8 * RHO / (3 * math.pi ** 2 * A_W)
MMS = MMD + 2 * SD ** 2 * MA1         # infinite baffle: both faces carry the air mass
K0 = 1 / CMS0
XMAX = 6e-3
# shapes (assumed): Bl falls to 82 % at +/-X_max, centred 0.5 mm off (coil rest position offset)
#                   K rises to 1/0.75 at +/-X_max, slightly harder outward (spider asymmetry)
#                   Le grows inward (coil into the iron), shrinks outward (Beranek fig. 6.23)
XOFF = 0.5e-3
B2 = (1 / 0.82 - 1) / XMAX ** 2
K1, K2 = 0.08 / XMAX, (1 / 0.75 - 1) / XMAX ** 2
L1 = -0.20 / XMAX


def bl(x): return BL0 / (1 + B2 * (x - XOFF) ** 2)
def kms(x): return K0 * (1 + K1 * x + K2 * x ** 2)
def le(x): return LE0 * (1 + L1 * x)


def rhs(t, s, src):
    """State: flux linkage psi = Le(x) i, velocity u, displacement x."""
    psi, u, x = s
    L = le(x); i = psi / L
    v = src(t)
    dpsi = v - RE * i - bl(x) * u
    du = (bl(x) * i - RMS * u - kms(x) * x) / MMS
    return np.array([dpsi, du, u])


def simulate(src, fsamp, T, sub=8):
    """Classic RK4 at fsamp*sub, keep every sub-th sample (a = du/dt also returned)."""
    h = 1 / (fsamp * sub)
    n = int(round(T * fsamp))
    s = np.zeros(3)
    out = np.zeros((n, 4))
    t = 0.0
    for k in range(n):
        for _ in range(sub):
            k1 = rhs(t, s, src); k2 = rhs(t + h / 2, s + h / 2 * k1, src)
            k3 = rhs(t + h / 2, s + h / 2 * k2, src); k4 = rhs(t + h, s + h * k3, src)
            s = s + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); t += h
        out[k, :3] = s
        out[k, 3] = rhs(t, s, src)[1]
    return out


def harmonics(sig, fsamp, f0, nh=5):
    """Amplitudes of the DC and first nh harmonics over an integer number of periods (rect window)."""
    N = len(sig)
    X = np.fft.rfft(sig) / N * 2
    df = fsamp / N
    amps = [abs(X[0]) / 2 * np.sign(X[0].real)] + [abs(X[int(round(k * f0 / df))]) for k in range(1, nh + 1)]
    return np.array(amps)


def tone_run(f0, V, periods_settle=40, periods_keep=10, fsamp_per=256):
    fsamp = f0 * fsamp_per
    T = (periods_settle + periods_keep) / f0
    out = simulate(lambda t: V * math.sin(2 * math.pi * f0 * t), fsamp, T, sub=4)
    keep = out[-periods_keep * fsamp_per:]
    return keep, fsamp


def part_d():
    print("\n=== D. nonlinear woofer (Scan-Speak 26W/8534G00, Lab D fit, infinite baffle)")
    fs = 1 / (2 * math.pi * math.sqrt(MMS * CMS0))
    print(f"M_MS = M_MD + 2 S_D^2 M_A1 = {MMS * 1e3:.1f} g, f_s(baffle) = {fs:.1f} Hz, X_max = {XMAX * 1e3:.0f} mm")
    print(f"assumed: Bl(+/-Xmax) = {bl(XMAX + XOFF) / BL0 * 100:.0f} %, C_MS(+Xmax) = {1 / (kms(XMAX) / K0) * 100:.0f} %,"
          f" C_MS(-Xmax) = {1 / (kms(-XMAX) / K0) * 100:.0f} %, Le(-Xmax) = {le(-XMAX) * 1e3:.2f} mH,"
          f" Le(+Xmax) = {le(XMAX) * 1e3:.2f} mH")
    xs = BL0 * CMS0 / RE
    print(f"static displacement per volt below f_s: Bl C_MS / R_E = {xs * 1e3:.2f} mm/V"
          f" -> X_max reached by ~{XMAX / xs:.1f} V (peak) below resonance")
    rows = []
    print(f"{'f':>5s} {'V pk':>5s} {'x pk mm':>8s} {'DC mm':>7s} {'H2 %':>6s} {'H3 %':>6s} {'THD %':>6s}   (of the cone acceleration = far-field pressure)")
    for f0 in (20, 40, 100):
        for V in (1, 5, 10, 20):
            keep, fsamp = tone_run(f0, V)
            a = harmonics(keep[:, 3], fsamp, f0)
            xh = harmonics(keep[:, 2], fsamp, f0)
            thd = math.sqrt((a[2:] ** 2).sum()) / a[1] * 100
            xpk = (keep[:, 2].max() - keep[:, 2].min()) / 2
            rows.append((f0, V, xpk, xh[0], a[2] / a[1] * 100, a[3] / a[1] * 100, thd))
            print(f"{f0:5d} {V:5d} {xpk * 1e3:8.2f} {xh[0] * 1e3:+7.2f} {a[2] / a[1] * 100:6.2f} {a[3] / a[1] * 100:6.2f} {thd:6.2f}")
    # two-tone: 40 Hz (large) + 1 kHz (small) -> Le(x) and Bl(x) modulate the 1 kHz tone
    f1, f2, V1, V2 = 40.0, 1000.0, 10.0, 2.0
    fsamp = 25600.0
    T = 1.5
    out = simulate(lambda t: V1 * math.sin(2 * math.pi * f1 * t) + V2 * math.sin(2 * math.pi * f2 * t), fsamp, T, sub=4)
    keep = out[-int(fsamp * 0.5):, 3]          # last 0.5 s = 20 periods of 40 Hz, 500 of 1 kHz
    N = len(keep); X = np.abs(np.fft.rfft(keep)) / N * 2; df = fsamp / N
    amp = lambda f: X[int(round(f / df))]
    im2 = (amp(f2 - f1) + amp(f2 + f1)) / amp(f2) * 100
    im3 = (amp(f2 - 2 * f1) + amp(f2 + 2 * f1)) / amp(f2) * 100
    print(f"two-tone {V1:.0f} V @ {f1:.0f} Hz + {V2:.0f} V @ {f2:.0f} Hz: sidebands f2 +/- f1 = {im2:.2f} %,"
          f" f2 +/- 2 f1 = {im3:.2f} % of the 1 kHz tone")
    return rows, (X, df)


# =====================================================================  LTspice
NETLIST = """* Lecture 11: nonlinear lumped loudspeaker (26W/8534G00, Lab D fit), written by p11.py
* state variables as node voltages: V(psi) = flux linkage Le(x)*i, V(u) = velocity, V(x) = displacement
.param RE={RE} LE0={LE0} BL0={BL0} MMS={MMS} K0={K0} RMS={RMS}
.param XOFF={XOFF} B2={B2} K1={K1} K2={K2} L1={L1} Vpk={V} f0={F0}
.func Bl(x) {{BL0/(1+B2*(x-XOFF)**2)}}
.func Kms(x) {{K0*(1+K1*x+K2*x**2)}}
.func Le(x) {{LE0*(1+L1*x)}}
Vg  in 0 SINE(0 {{Vpk}} {{f0}})
* electrical loop: d(psi)/dt = v_g - R_E i - Bl(x) u, i = psi/Le(x)
Bpsi 0 psi I=V(in) - RE*V(psi)/Le(V(x)) - Bl(V(x))*V(u)
Cpsi psi 0 1
* mechanics: M_MS du/dt = Bl(x) i - R_MS u - K(x) x
Bu   0 u  I=Bl(V(x))*V(psi)/Le(V(x)) - RMS*V(u) - Kms(V(x))*V(x)
Cu   u 0  {{MMS}}
* dx/dt = u
Bx   0 x  I=V(u)
Cx   x 0  1
.ic V(psi)=0 V(u)=0 V(x)=0
.tran 0 {{{TSTOP}}} {{{TSTART}}} {{{DT}}} uic
.save V(x) V(u)
.options plotwinsize=0 numdgt=15 reltol=1e-6
.end
"""


def write_netlist(f0, V, settle=40, keep=10):
    p = HERE / "P11_Nonlinear_Woofer.cir"
    p.write_text(NETLIST.format(RE=RE, LE0=LE0, BL0=BL0, MMS=MMS, K0=K0, RMS=RMS, XOFF=XOFF, B2=B2, K1=K1,
                                K2=K2, L1=L1, V=V, F0=f0, TSTOP=(settle + keep) / f0, TSTART=settle / f0,
                                DT=1 / (f0 * 2048)))
    return p


def read_raw(path):
    b = path.read_bytes(); key = "Binary:\n".encode("utf-16le"); i = b.find(key)
    head = b[:i].decode("utf-16le"); data = b[i + len(key):]
    names = []; invars = False; npts = 0
    for ln in head.splitlines():
        if ln.startswith("No. Points:"): npts = int(ln.split(":")[1])
        if ln.startswith("Variables:"): invars = True; continue
        if invars and ln.strip() and not ln.startswith("Binary"): names.append(ln.split()[1].lower())
    nv = len(names)
    # transient raw: time is always double; the rest float32, or double when numdgt > 6
    wide = len(data) >= npts * nv * 8
    rec = np.dtype([("t", "<f8")] + [(f"v{j}", "<f8" if wide else "<f4") for j in range(nv - 1)])
    arr = np.frombuffer(data[:npts * rec.itemsize], dtype=rec)
    cols = {"time": np.abs(arr["t"])}
    for j, n in enumerate(names[1:]):
        cols[n] = arr[f"v{j}"].astype(float)
    return cols


def run_ltspice(cir):
    import shutil, tempfile
    env = dict(os.environ, WINEARCH="win64", WINEPREFIX=os.path.expanduser("~/.local/share/wineprefixes/ltspice"), WINEDEBUG="-all")
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="lt11_"))
    work = tmp / cir.name; shutil.copy(cir, work)
    wp = subprocess.run(["winepath", "-w", str(work)], env=env, capture_output=True, text=True).stdout.strip()
    subprocess.run(["wine", "/usr/share/ltspice/LTspice.exe", "-b", wp], env=env, capture_output=True, timeout=300)
    raw = work.with_suffix(".raw")
    if not raw.exists():
        log = work.with_suffix(".log")
        raise SystemExit("LTspice failed:\n" + (log.read_bytes().decode("utf-16le", "ignore") if log.exists() else "no log"))
    cols = read_raw(raw)
    shutil.rmtree(tmp, ignore_errors=True)
    return cols


def verify():
    print("\n=== LTspice cross-check (B-source state-variable netlist)")
    worst = 0.0
    for f0, V in ((20, 10), (40, 20)):
        cols = run_ltspice(write_netlist(f0, V))
        t, x, u = cols["time"], cols["v(x)"], cols["v(u)"]
        n = 10 * 2048
        tu = np.linspace(t[0], t[-1], n, endpoint=False)
        xs = np.interp(tu, t, x)
        us = np.interp(tu, t, u)
        a = np.gradient(us, tu)
        fsamp = 1 / (tu[1] - tu[0])
        hl = harmonics(a, fsamp, f0); xl = harmonics(xs, fsamp, f0)
        keep, fsp = tone_run(f0, V)
        hp = harmonics(keep[:, 3], fsp, f0); xp = harmonics(keep[:, 2], fsp, f0)
        for k, lab in ((1, "fund"), (2, "H2"), (3, "H3")):
            d = 20 * math.log10(hl[k] / hp[k])
            worst = max(worst, abs(d))
            print(f"  {f0} Hz {V} V {lab}: LTspice {hl[k]:.4g}  Python {hp[k]:.4g}  ({d:+.3f} dB)")
        print(f"  {f0} Hz {V} V DC offset: LTspice {xl[0] * 1e3:+.3f} mm  Python {xp[0] * 1e3:+.3f} mm")
    write_netlist(20, 10)                       # leave the file at a sensible default
    print(f"worst harmonic mismatch {worst:.3f} dB -> {'OK' if worst < 0.2 else 'CHECK'}")


# =====================================================================  plots
def plots(f1, rows, spec):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    VAULT_IMG.mkdir(parents=True, exist_ok=True)
    # 1 directivity
    fig = plt.figure(figsize=(6.4, 5.2)); ax = fig.add_subplot(projection="polar")
    th = np.radians(np.linspace(-90, 90, 721))
    for f in (200, 500, 1000, 2000, 3000):
        ka = 2 * math.pi * f / C * A_W
        ax.plot(th, np.clip(db(directivity(ka, th)), -40, 0), label=f"{f} Hz (ka {ka:.1f})")
    ax.set_thetamin(-90); ax.set_thetamax(90); ax.set_theta_zero_location("N"); ax.set_rlim(-40, 0)
    ax.set_title("Baffled piston a = 105.5 mm (System D woofer): 2J1(v)/v", fontsize=10)
    ax.legend(loc="lower left", fontsize=8, bbox_to_anchor=(-0.15, -0.12))
    fig.savefig(VAULT_IMG / "L11_directivity.png", dpi=130, bbox_inches="tight"); plt.close(fig)
    # 2 radiation impedance
    ka = np.logspace(-1.3, 1.3, 400)
    R = 1 - J1(2 * ka) / ka; X = H1(2 * ka) / ka
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.loglog(ka, R, label="R / (rho c S) = 1 - J1(2ka)/ka"); ax.loglog(ka, X, label="X / (rho c S) = H1(2ka)/ka")
    ax.loglog(ka, ka ** 2 / 2, "--", lw=0.8, color="gray", label="(ka)^2/2 (low-frequency R)")
    ax.loglog(ka, 8 * ka / (3 * math.pi), ":", lw=0.8, color="gray", label="8ka/3pi (mass M_A1)")
    ax.set_ylim(1e-3, 3); ax.set_xlabel("ka"); ax.grid(True, which="both", alpha=0.3); ax.legend(fontsize=8)
    ax.set_title("Radiation impedance of a piston in an infinite baffle", fontsize=10)
    fig.savefig(VAULT_IMG / "L11_radiation_impedance.png", dpi=130, bbox_inches="tight"); plt.close(fig)
    # 3 nonlinear parameter curves
    x = np.linspace(-10e-3, 10e-3, 401)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(x * 1e3, bl(x) / BL0, label="Bl(x)/Bl0")
    ax.plot(x * 1e3, K0 / kms(x), label="C_MS(x)/C_MS0")
    ax.plot(x * 1e3, le(x) / LE0, label="Le(x)/Le0")
    for xx in (-6, 6): ax.axvline(xx, color="gray", ls=":", lw=0.8)
    ax.axhline(0.82, color="C0", ls="--", lw=0.6); ax.axhline(0.75, color="C1", ls="--", lw=0.6)
    ax.set_xlabel("x (mm), + = outward"); ax.set_ylim(0.3, 1.4); ax.grid(alpha=0.3); ax.legend(fontsize=8)
    ax.set_title("Assumed large-signal parameters (X_max = 6 mm: Bl 82 %, C_MS 75 %)", fontsize=10)
    fig.savefig(VAULT_IMG / "L11_nonlinear_params.png", dpi=130, bbox_inches="tight"); plt.close(fig)
    # 4 THD vs level
    fig, ax = plt.subplots(figsize=(7, 4))
    for f0 in (20, 40, 100):
        rr = [r for r in rows if r[0] == f0]
        ax.plot([r[1] for r in rr], [r[6] for r in rr], "o-", label=f"{f0} Hz THD")
        ax.plot([r[1] for r in rr], [r[4] for r in rr], "x--", lw=0.8, label=f"{f0} Hz H2")
    ax.set_xlabel("drive voltage (V peak)"); ax.set_ylabel("% of fundamental (cone acceleration)")
    ax.set_yscale("log"); ax.grid(True, which="both", alpha=0.3); ax.legend(fontsize=8, ncol=2)
    ax.set_title("Harmonic distortion of the nonlinear woofer model", fontsize=10)
    fig.savefig(VAULT_IMG / "L11_thd.png", dpi=130, bbox_inches="tight"); plt.close(fig)
    # 5 two-tone spectrum
    X, df = spec
    f = np.arange(len(X)) * df
    fig, ax = plt.subplots(figsize=(7, 4))
    m = (f > 800) & (f < 1200)
    ax.plot(f[m], db(X[m] / X.max() + 1e-12))
    ax.set_xlabel("frequency (Hz)"); ax.set_ylabel("dB re largest line"); ax.set_ylim(-100, 5); ax.grid(alpha=0.3)
    ax.set_title("Two-tone 10 V @ 40 Hz + 2 V @ 1 kHz: sidebands at 1 kHz +/- n*40 Hz", fontsize=10)
    fig.savefig(VAULT_IMG / "L11_intermod.png", dpi=130, bbox_inches="tight"); plt.close(fig)
    print(f"figures -> {VAULT_IMG}")


if __name__ == "__main__":
    f1 = part_a(); part_b(); part_c(); rows, spec = part_d()
    write_netlist(20, 10)
    if "--verify" in sys.argv: verify()
    if "--plots" in sys.argv: plots(f1, rows, spec)
