#!/usr/bin/env python3
"""Problems 5 (Lecture 5), Q1/Q2a-c - condenser microphone, three domains, T(s)=1 (ignored).

Acoustic (impedance analogy, p = voltage, U = current), mirrors Problems4/Problem_4B's
front/back split exactly:
    Vpi = p_i (1 Pa) -> L1 = M_A1 (front air mass) -> node pf -> [diaphragm] -> node pb
    -> R1 = R_AS -> L2 = M_AS -> C1 = C_AB2 -> GND  (C_AB1 dropped: C_AB1 << C_AB2, given)
    The diaphragm is G1: it carries U = S_D*u from pf to pb (VCCS sensing u).
Mechanical (MOBILITY analogy, u = voltage, f = current), node u:
    C2 = M_MD (cap to gnd), L3 = C_MD (inductor to gnd, with a tiny sense resistor R2
    to gnd so its own branch current u/(jwC_MD) is probeable as a voltage), R3 = 1/R_MD.
    G2 senses (pf-pb) and injects f = S_D*(pf-pb) into node u (plain, no 1/jw - matches
    the piston law f=Sp, same as every other diaphragm coupling in this course).
    G3 injects the ELECTROSTATIC reaction f = -(E*C_E0/x0)*V(node across C_E0) into u -
    this is the frequency-independent Norton form from Lecture 5 slide 20/section 4f.
Electrical (series loop, current i flows through C_E0, E1, R_L'):
    GND -> C_E0 -> node ce0 -> E1 (=(E/(x0*jw))*u, realised frequency-independently as
    gain (E*C_MD)/(x0*Rsense) * V(mech_sense), where mech_sense = the sense-resistor
    voltage on L3's branch, i.e. u/(jwC_MD)*Rsense) -> node out -> R_L' -> GND.
    e = V(out).

Validated analytically (see sim.py) against Problem 5.1's totals:
    M_MT = M_MD + S_D^2*(M_A1+M_AS), R_MT = R_MD + S_D^2*R_AS, 1/C_MT = 1/C_MD + S_D^2/C_AB2
in the R_L' -> large limit.
"""
import sys, json
from pathlib import Path
import numpy as np
SKILL = "/home/mads/.claude/skills/kicad-schematic/scripts"
sys.path.insert(0, SKILL)
from schdraw import Sheet
from simfields import set_sim

G = lambda n: round(n * 1.27, 2)
HERE = Path(__file__).resolve().parent
NAME = "Problem_5_Condenser_Microphone"

# ---------- Problem 5.1 values ----------
rho, c = 1.18, 344.0
CMD, MMD, RMD = 4e-6, 0.050e-3, 1.0
a = 0.009
SD = np.pi * a**2
MA1 = 8 * rho / (3 * np.pi**2 * a)
MAS, RAS = 100.0, 1e7
VAB2 = 1e-6
CAB2 = VAB2 / (rho * c**2)
E, x0, RLp = 200.0, 20e-6, 500e6
eps0 = 8.85e-12
CE0 = eps0 * SD / x0
RSENSE = 1e-6            # tiny sense resistor, negligible vs |jw*C_MD| ~ O(0.1-1) in-band
AC_CMD = ".ac dec 200 100 100k"

sh = Sheet(paper="A4", title="Problems 5 (Q1/2a-c) - Condenser microphone, three domains", project=NAME)
def pins(part): return {p.name: p for p in part.pins}
TOP, BOT = G(28), G(52)

# ---------- acoustic block ----------
v1 = sh.place("Simulation_SPICE:VDC", "V1", at=(G(16), G(40)), rot=0, value="1")
l1 = sh.place("Device:L", "L1", at=(G(28), TOP), rot=90, value=f"{MA1:.6g}")
g1 = sh.place("Simulation_SPICE:GSOURCE", "G1", at=(G(44), G(40)), rot=0, value="GSOURCE")
g1p = pins(g1)                                   # rot=0: N+ top, N- bottom, C+/C- to the left
r1 = sh.place("Device:R", "R1", at=(G(58), BOT), rot=90, value=f"{RAS:.6g}")
l2 = sh.place("Device:L", "L2", at=(G(70), BOT), rot=90, value=f"{MAS:.6g}")
c1 = sh.place("Device:C", "C1", at=(G(82), G(60)), rot=0, value=f"{CAB2:.6g}")
r4 = sh.place("Device:R", "R4", at=(G(90), G(60)), rot=0, value="1T")   # DC bias leak

sh.wire(v1.pin(1), (v1.pin(1).x, TOP), l1.pin(1))
sh.wire(l1.pin(2), (g1p["N+"].x, TOP), g1p["N+"])
sh.label((G(36), TOP), "pf")
sh.wire(g1p["N-"], (g1p["N-"].x, BOT), r1.pin(1))
sh.label((G(50), BOT), "pb")
sh.wire(r1.pin(2), l2.pin(1))
sh.wire(l2.pin(2), (c1.pin(1).x, BOT), c1.pin(1))
sh.wire((c1.pin(1).x, BOT), (r4.pin(1).x, BOT), r4.pin(1))
ARAIL = G(76)
for p in (v1.pin(2), c1.pin(2), r4.pin(2)):
    sh.wire(p, (p.x, ARAIL))
sh.wire((v1.pin(2).x, ARAIL), (r4.pin(2).x, ARAIL))
sh.gnd((G(30), ARAIL), drop=G(4))
# diaphragm volume velocity: G1 senses u
sh.wire(g1p["C+"], (g1p["C+"].x, G(32)))
sh.label((g1p["C+"].x, G(32)), "u")
sh.wire(g1p["C-"], (g1p["C-"].x, ARAIL))

# ---------- mechanical block (mobility) ----------
g2 = sh.place("Simulation_SPICE:GSOURCE", "G2", at=(G(112), G(40)), rot=180, value="GSOURCE")
g2p = pins(g2)                                   # rot=180: N- top, N+ bottom, C- top-right, C+ bottom-right
g3 = sh.place("Simulation_SPICE:GSOURCE", "G3", at=(G(128), G(40)), rot=180, value="GSOURCE")
g3p = pins(g3)
c2 = sh.place("Device:C", "C2", at=(G(144), G(40)), rot=0, value=f"{MMD:.6g}")
l3 = sh.place("Device:L", "L3", at=(G(156), G(40)), rot=0, value=f"{CMD:.6g}")
r3 = sh.place("Device:R", "R3", at=(G(168), G(40)), rot=0, value=f"{1/RMD:g}")
rsm = sh.place("Device:R", "R2", at=(G(156), G(52)), rot=0, value=f"{RSENSE:g}")

sh.wire(g2p["N-"], (g2p["N-"].x, TOP))
sh.wire(g3p["N-"], (g3p["N-"].x, TOP))
for part in (c2, l3, r3):
    sh.wire(part.pin(1), (part.pin(1).x, TOP))
sh.wire((g2p["N-"].x, TOP), (r3.pin(1).x, TOP))
sh.label((G(120), TOP), "u")
sh.wire(c2.pin(2), (c2.pin(2).x, BOT))
sh.wire(r3.pin(2), (r3.pin(2).x, BOT))
sh.wire(l3.pin(2), (rsm.pin(1).x, l3.pin(2).y), rsm.pin(1))
sh.wire(rsm.pin(2), (rsm.pin(2).x, BOT))
sh.wire(g2p["N+"], (g2p["N+"].x, BOT))
sh.wire(g3p["N+"], (g3p["N+"].x, BOT))
sh.wire((g2p["N+"].x, BOT), (r3.pin(2).x, BOT))
sh.gnd((G(150), BOT), drop=G(4))
# G2 senses pf - pb (acoustic reaction, f = S_D*(pf-pb))
sh.wire(g2p["C+"], (g2p["C+"].x, G(48)))
sh.label((g2p["C+"].x, G(48)), "pf")
sh.wire(g2p["C-"], (g2p["C-"].x, G(32)))
sh.label((g2p["C-"].x, G(32)), "pb")
# G3 senses V(ce0) (electrostatic reaction, gain -E*CE0/x0).  C+/C- share an
# x-column, so route each sideways off it before running to its rail --
# otherwise one pin's straight wire passes right through the other pin.
CE0_TAP_X = g3p["C+"].x + G(4)
sh.wire(g3p["C+"], (CE0_TAP_X, g3p["C+"].y), (CE0_TAP_X, G(48)))
sh.label((CE0_TAP_X, G(48)), "ce0")
CMINUS_X = g3p["C-"].x + G(8)
sh.wire(g3p["C-"], (CMINUS_X, g3p["C-"].y), (CMINUS_X, BOT))
# mechanical sense node (for E1's control, feeding back to the electrical block)
sh.label((rsm.pin(1).x, l3.pin(2).y), "mech_sense")

# ---------- electrical block ----------
c_e0 = sh.place("Device:C", "CE0", at=(G(200), G(40)), rot=0, value=f"{CE0:.6g}")
e1 = sh.place("Simulation_SPICE:ESOURCE", "E1", at=(G(214), G(40)), rot=0, value="ESOURCE")
e1p = pins(e1)
r5 = sh.place("Device:R", "R5", at=(G(228), G(40)), rot=0, value=f"{RLp:.6g}")

sh.wire(c_e0.pin(1), (c_e0.pin(1).x, TOP), e1p["N+"])
sh.label((c_e0.pin(1).x, TOP), "ce0")
sh.wire(c_e0.pin(2), (c_e0.pin(2).x, BOT))
MIDX = round((e1p["N-"].x + r5.pin(1).x) / 2, 2)
sh.wire(e1p["N-"], (MIDX, e1p["N-"].y), (MIDX, TOP), (r5.pin(1).x, TOP), r5.pin(1))
sh.label((G(222), TOP), "out")
sh.wire(r5.pin(2), (r5.pin(2).x, BOT))
sh.wire((c_e0.pin(2).x, BOT), (r5.pin(2).x, BOT))
sh.gnd((G(214), BOT), drop=G(4))
# E1 control: mech_sense (the tiny sense resistor's own voltage, since its far end is GND)
sh.wire(e1p["C+"], (e1p["C+"].x, G(32)))
sh.label((e1p["C+"].x, G(32)), "mech_sense")
sh.wire(e1p["C-"], (e1p["C-"].x, BOT))

# PWR_FLAG stubs (one per isolated ground rail so ngspice is happy)
for x in (G(30), G(150), G(200)):
    sh.wire((x, BOT), (x, BOT + G(4)))
    sh.power("power:PWR_FLAG", (x, BOT + G(4)))

# ---------- notes ----------
sh.note((G(14), G(8)), "Problems 5 (Q1 / 2a-c) - condenser microphone, three domains, T(s)=1 ignored", size=1.6)
sh.note((G(14), G(12)), f"Acoustic: V1=p_i (AC 1 Pa), L1=M_A1={MA1:.4g}, R1=R_AS={RAS:.3g}, L2=M_AS={MAS:g}, C1=C_AB2={CAB2:.4g} (C_AB1<<C_AB2, dropped)", size=1.2)
sh.note((G(14), G(15)), f"Mechanical (mobility): C2=M_MD={MMD:.3g}, L3=C_MD={CMD:.3g}, R3=1/R_MD={1/RMD:g}, R2=sense={RSENSE:g}", size=1.2)
sh.note((G(14), G(18)), f"G1: U=S_D*u (S_D={SD:.5g}).  G2: f=S_D*(pf-pb).  G3: f=-(E*C_E0/x0)*V(ce0), gain={-(E*CE0/x0):.5g}", size=1.2)
sh.note((G(14), G(21)), f"Electrical: CE0={CE0:.5g} F, E1=(E*C_MD/(x0*Rsense))*V(mech_sense), R5=R_L'={RLp:.3g}", size=1.2)
sh.note((G(150), G(12)), "SPICE directive (read automatically):", size=1.4)
sh.note((G(150), G(16)), AC_CMD, size=1.8)

problems = sh.check(); print("check():", problems)
for n, m in sh.netlist().items(): print(n, sorted(m))
out = HERE / f"{NAME}.kicad_sch"
sh.emit(str(out))

def ctrl(t, gain): return {"Sim.Device": "SPICE", "Sim.Params": 'type=\\"%s\\" model=\\"%s\\"' % (t, gain)}
set_sim(out, {
    "V1": {"Sim.Device": "V", "Sim.Type": "DC", "Sim.Pins": "1=+ 2=-", "Sim.Params": "dc=1 ac=1"},
    "G1": ctrl("G", f"{SD:.8g}"),
    "G2": ctrl("G", f"{SD:.8g}"),
    "G3": ctrl("G", f"{-(E*CE0/x0):.8g}"),
    "E1": ctrl("E", f"{(E*CMD)/(x0*RSENSE):.8g}"),
})

# project file: clone the structure of an existing Lecture 4 project
src = HERE.parent.parent / "Lecture 4" / "Problem_4.4b_Coil_Electromechanical" / "Problem_4.4b_Coil_Electromechanical.kicad_pro"
pro = json.loads(src.read_text(encoding="utf-8"))
pro["meta"]["filename"] = f"{NAME}.kicad_pro"
(HERE / f"{NAME}.kicad_pro").write_text(json.dumps(pro, indent=2) + "\n", encoding="utf-8")

wb = {"custom_cursors": 2, "last_sch_text_sim_command": AC_CMD,
      "tabs": [{"analysis": "AC",
                "commands": [AC_CMD, ".kicad adjustpaths", ".save all", ".probe alli", ".probe allp"],
                "dottedSecondary": False,
                "margins": {"bottom": 45, "left": 70, "right": 70, "top": 30},
                "measurements": [], "showGrid": True,
                "traces": [{"color": "rgb(228, 26, 28)", "signal": "V(/out) (gain)", "trace_type": 521}]}],
      "user_defined_signals": [], "version": 7}
(HERE / f"{NAME}.wbk").write_text(json.dumps(wb, indent=2) + "\n", encoding="utf-8")
print("emitted", out)
