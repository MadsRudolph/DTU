#!/usr/bin/env python3
"""In-class Problem 4.2 implemented with the 4.4a values - piston in a thick
baffle with a closed box on the back, BOTH analogies on one sheet (4.4a: they
must agree).

Values: S = 100 cm^2 (a = 5.64 cm), M_mp = 20 g, box V = 40 l, baffle d = 2 cm.
Drive: f = 1 N. Acoustic chain (impedance analogy, identical in both blocks):
  p -> Z_Af (baffled-piston network, 4.2e) -> pb -> L(M_Ad = rho*d/S, 4.2c)
  -> pc -> C(C_AB, 4.2d) to ground (+ 1T DC leak).

Block 1 - mechanical MOBILITY: I1 = f (1 A) into node u, C = M_mp to ground
  (+ 1T leak, the node is otherwise capacitor-only), G2 draws f_ac = S*p,
  G1 injects U = S*u.
Block 2 - mechanical IMPEDANCE: loop V2 = f (1 V) -> R6 = 1 uOhm current sense
  -> L4 = M_mp -> E1 = S*p_i (the reaction force as a series voltage) -> gnd;
  the loop current IS u. G3 (the F-source trick: sense u as V(fa)-V(fb) across
  R6, gain S/1u) injects U = S*u into p_i.
Agreement check in sim.py: V(u) vs (V(fa)-V(fb))/1u.
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
NAME = "Problem_4.2-4.4a_Piston_Box"

rho, c = 1.18, 344.0
S = 100e-4
a = np.sqrt(S / np.pi)
MMP = 20e-3
V, D = 40e-3, 0.02
MA1 = 8 * rho / (3 * np.pi**2 * a)
RA1 = 0.441 * rho * c / S
RA2 = rho * c / S
CA1 = 5.94 * a**3 / (rho * c**2)
MAD = rho * D / S
CAB = V / (rho * c**2)
RS = 1e-6
f0 = 1 / (2 * np.pi * np.sqrt((MMP + S**2 * (MA1 + MAD)) * CAB / S**2))
AC_CMD = ".ac dec 500 5 5k"

sh = Sheet(paper="A4", title="Problem 4.2 / 4.4a - piston + baffle tube + box, both analogies", project=NAME)
def pins(part): return {p.name: p for p in part.pins}

# ================= block 1: mobility =================
TOP, MID, BOT = G(40), G(58), G(74)
i1 = sh.place("Simulation_SPICE:IDC", "I1", at=(G(12), G(49)), rot=180, value="1")
sh.wire(i1.pin(2), (i1.pin(2).x, TOP))     # rot=180: pin 2 (-) on top, current into u
sh.wire(i1.pin(1), (i1.pin(1).x, BOT))
c5 = sh.place("Device:C", "C5", at=(G(19), G(49)), rot=0, value=f"{MMP:g}")
r10 = sh.place("Device:R", "R10", at=(G(26), G(49)), rot=0, value="1T")
for part in (c5, r10):
    sh.wire(part.pin(1), (part.pin(1).x, TOP))
    sh.wire(part.pin(2), (part.pin(2).x, BOT))
g2 = sh.place("Simulation_SPICE:GSOURCE", "G2", at=(G(34), G(49)), rot=0, value="GSOURCE")
g2p = pins(g2)
sh.wire(g2p["N+"], (g2p["N+"].x, TOP))
sh.wire(g2p["N-"], (g2p["N-"].x, BOT))
sh.wire((i1.pin(2).x, TOP), (g2p["N+"].x, TOP))
sh.label((G(16), TOP), "u")
sh.wire(g2p["C+"], (g2p["C+"].x, G(43)))
sh.label((g2p["C+"].x, G(43)), "p")
sh.wire(g2p["C-"], (g2p["C-"].x, BOT))

g1 = sh.place("Simulation_SPICE:GSOURCE", "G1", at=(G(48), G(32)), rot=0, value="GSOURCE")
g1p = pins(g1)
sh.wire(g1p["N+"], (g1p["N+"].x, G(25)))
sh.power("power:GND", (g1p["N+"].x, G(25)), rot=180)
sh.wire(g1p["N-"], (g1p["N-"].x, TOP))
sh.wire(g1p["C+"], (g1p["C+"].x, G(25)))
sh.label((g1p["C+"].x, G(25)), "u")
sh.gnd(g1p["C-"], drop=G(3))

SUB = G(51)
l1 = sh.place("Device:L", "L1", at=(G(58), G(49)), rot=0, value=f"{MA1:.6g}")
sh.wire(l1.pin(1), (l1.pin(1).x, TOP))
sh.wire(l1.pin(2), (l1.pin(2).x, MID))
r1 = sh.place("Device:R", "R1", at=(G(74), G(45)), rot=0, value=f"{RA2:.6g}")
sh.wire(r1.pin(1), (r1.pin(1).x, TOP))
sh.wire(r1.pin(2), (r1.pin(2).x, SUB))
r2 = sh.place("Device:R", "R2", at=(G(70), G(54)), rot=0, value=f"{RA1:.6g}")
c1 = sh.place("Device:C", "C1", at=(G(78), G(54)), rot=0, value=f"{CA1:.6g}")
for part in (r2, c1):
    sh.wire(part.pin(1), (part.pin(1).x, SUB))
    sh.wire(part.pin(2), (part.pin(2).x, MID))
sh.wire((r2.pin(1).x, SUB), (c1.pin(1).x, SUB))
sh.wire((g1p["N-"].x, TOP), (r1.pin(1).x, TOP))
sh.label((G(54), TOP), "p")
sh.wire((l1.pin(2).x, MID), (c1.pin(2).x, MID))
sh.label((G(82), MID), "pb")
l3 = sh.place("Device:L", "L3", at=(G(88), MID), rot=90, value=f"{MAD:.6g}")
sh.wire((c1.pin(2).x, MID), l3.pin(1))
c2 = sh.place("Device:C", "C2", at=(G(98), G(66)), rot=0, value=f"{CAB:.6g}")
r3 = sh.place("Device:R", "R3", at=(G(106), G(66)), rot=0, value="1T")
for part in (c2, r3):
    sh.wire(part.pin(1), (part.pin(1).x, MID))
    sh.wire(part.pin(2), (part.pin(2).x, BOT))
sh.wire(l3.pin(2), (c2.pin(1).x, MID))
sh.wire((c2.pin(1).x, MID), (r3.pin(1).x, MID))
sh.label((G(94), MID), "pc")
sh.wire((i1.pin(1).x, BOT), (r3.pin(2).x, BOT))
sh.gnd((G(30), BOT), drop=G(4))
sh.wire((G(22), BOT), (G(22), BOT + G(4)))
sh.power("power:PWR_FLAG", (G(22), BOT + G(4)))

# ================= block 2: impedance =================
TOP2, MID2, BOT2 = G(92), G(110), G(126)
v2 = sh.place("Simulation_SPICE:VDC", "V2", at=(G(12), G(101)), rot=0, value="1")
sh.wire(v2.pin(1), (v2.pin(1).x, TOP2))
sh.wire(v2.pin(2), (v2.pin(2).x, BOT2))
sh.label((G(15), TOP2), "fa")
r6 = sh.place("Device:R", "R6", at=(G(24), TOP2), rot=90, value=f"{RS:g}")
sh.wire((v2.pin(1).x, TOP2), r6.pin(1))
sh.label((G(30), TOP2), "fb")
l4 = sh.place("Device:L", "L4", at=(G(36), TOP2), rot=90, value=f"{MMP:g}")
sh.wire(r6.pin(2), l4.pin(1))
e1 = sh.place("Simulation_SPICE:ESOURCE", "E1", at=(G(48), G(101)), rot=180, value="ESOURCE")
e1p = pins(e1)                             # rot=180: N- top, N+ bottom, C- top-right, C+ bottom-right
sh.wire(l4.pin(2), (e1p["N-"].x, TOP2), e1p["N-"])
sh.wire(e1p["N+"], (e1p["N+"].x, BOT2))
sh.wire(e1p["C-"], (e1p["C-"].x, G(95)))
sh.label((e1p["C-"].x, G(95)), "pi")
sh.wire(e1p["C+"], (e1p["C+"].x, BOT2))

g3 = sh.place("Simulation_SPICE:GSOURCE", "G3", at=(G(66), G(84)), rot=0, value="GSOURCE")
g3p = pins(g3)
sh.wire(g3p["N+"], (g3p["N+"].x, G(77)))
sh.power("power:GND", (g3p["N+"].x, G(77)), rot=180)
sh.wire(g3p["N-"], (g3p["N-"].x, TOP2))
sh.wire(g3p["C+"], (g3p["C+"].x, G(77)))
sh.label((g3p["C+"].x, G(77)), "fa")
sh.wire(g3p["C-"], (g3p["C-"].x, G(90)))
sh.label((g3p["C-"].x, G(90)), "fb")

SUB3 = G(103)
l5 = sh.place("Device:L", "L5", at=(G(76), G(101)), rot=0, value=f"{MA1:.6g}")
sh.wire(l5.pin(1), (l5.pin(1).x, TOP2))
sh.wire(l5.pin(2), (l5.pin(2).x, MID2))
r7 = sh.place("Device:R", "R7", at=(G(92), G(97)), rot=0, value=f"{RA2:.6g}")
sh.wire(r7.pin(1), (r7.pin(1).x, TOP2))
sh.wire(r7.pin(2), (r7.pin(2).x, SUB3))
r8 = sh.place("Device:R", "R8", at=(G(88), G(106)), rot=0, value=f"{RA1:.6g}")
c3 = sh.place("Device:C", "C3", at=(G(96), G(106)), rot=0, value=f"{CA1:.6g}")
for part in (r8, c3):
    sh.wire(part.pin(1), (part.pin(1).x, SUB3))
    sh.wire(part.pin(2), (part.pin(2).x, MID2))
sh.wire((r8.pin(1).x, SUB3), (c3.pin(1).x, SUB3))
sh.wire((g3p["N-"].x, TOP2), (r7.pin(1).x, TOP2))
sh.label((G(70), TOP2), "pi")
sh.wire((l5.pin(2).x, MID2), (c3.pin(2).x, MID2))
sh.label((G(80), MID2), "pb2")
l6 = sh.place("Device:L", "L6", at=(G(102), MID2), rot=90, value=f"{MAD:.6g}")
sh.wire((c3.pin(2).x, MID2), l6.pin(1))
c4 = sh.place("Device:C", "C4", at=(G(110), G(118)), rot=0, value=f"{CAB:.6g}")
r9 = sh.place("Device:R", "R9", at=(G(118), G(118)), rot=0, value="1T")
for part in (c4, r9):
    sh.wire(part.pin(1), (part.pin(1).x, MID2))
    sh.wire(part.pin(2), (part.pin(2).x, BOT2))
sh.wire(l6.pin(2), (c4.pin(1).x, MID2))
sh.wire((c4.pin(1).x, MID2), (r9.pin(1).x, MID2))
sh.label((G(106), MID2), "pc2")
sh.wire((v2.pin(2).x, BOT2), (r9.pin(2).x, BOT2))
sh.gnd((G(30), BOT2), drop=G(4))

# ---------- notes ----------
sh.note((G(12), G(6)), "Problem 4.2 / 4.4a - baffled piston (S = 100 cm^2, M_mp = 20 g), baffle tube d = 2 cm, closed box V = 40 l; f = 1 N", size=1.6)
sh.note((G(12), G(10)), f"Top: MOBILITY block (u = V, f = I). Bottom: IMPEDANCE block (loop current = u, R6 = 1 uOhm sense for the F-source trick). Both must agree (4.4a).", size=1.2)
sh.note((G(12), G(13)), f"Z_Af (a = {a*100:.2f} cm): M_A1 = {MA1:.3g}, R_A2 = {RA2:.3g}, R_A1 = {RA1:.3g}, C_A1 = {CA1:.3g}; tube M_Ad = {MAD:.3g}; box C_AB = {CAB:.3g}", size=1.2)
sh.note((G(12), G(16)), f"Referred to mech: air load S^2*M_A1 = {S*S*MA1*1e3:.2f} g, tube {S*S*MAD*1e3:.2f} g, box compliance C_AB/S^2 = {CAB/S**2*1e3:.2f} mm/N -> f0 = {f0:.1f} Hz", size=1.2)
sh.note((G(12), G(19)), "Damped ONLY by the front radiation resistance -> very high Q at 20 Hz (Re Z_rad ~ (ka)^2). E1 = -S*pi (rot 180 flips polarity: C- = pi, C+ = gnd)", size=1.2)
sh.note((G(150), G(10)), "SPICE directive (read automatically):", size=1.4)
sh.note((G(150), G(14)), AC_CMD, size=1.8)
sh.note((G(150), G(18)), ".options abstol=1e-14 vntol=1e-12", size=1.4)

problems = sh.check(); print("check():", problems)
for n, m in sh.netlist().items(): print(n, sorted(m))
out = HERE / f"{NAME}.kicad_sch"
sh.emit(str(out))
def ctrl(t, gain): return {"Sim.Device": "SPICE", "Sim.Params": 'type=\\"%s\\" model=\\"%s\\"' % (t, gain)}
set_sim(out, {
    "I1": {"Sim.Device": "I", "Sim.Type": "DC", "Sim.Pins": "1=+ 2=-", "Sim.Params": "dc=0 ac=1"},
    "V2": {"Sim.Device": "V", "Sim.Type": "DC", "Sim.Pins": "1=+ 2=-", "Sim.Params": "dc=0 ac=1"},
    "G1": ctrl("G", f"{S:.6g}"),
    "G2": ctrl("G", f"{S:.6g}"),
    "G3": ctrl("G", f"{S/RS:.6g}"),
    "E1": ctrl("E", f"{S:.6g}"),
})
src = HERE.parent.parent / "Lecture 3" / "Problem_2.3_Two_Tube_Network" / "Problem_2.3_Two_Tube_Network.kicad_pro"
pro = json.loads(src.read_text(encoding="utf-8")); pro["meta"]["filename"] = f"{NAME}.kicad_pro"
(HERE / f"{NAME}.kicad_pro").write_text(json.dumps(pro, indent=2) + "\n", encoding="utf-8")
wb = {"custom_cursors": 2, "last_sch_text_sim_command": AC_CMD,
      "tabs": [{"analysis": "AC", "commands": [AC_CMD, ".options abstol=1e-14 vntol=1e-12", ".kicad adjustpaths", ".save all", ".probe alli", ".probe allp"],
                "dottedSecondary": False, "margins": {"bottom": 45, "left": 70, "right": 70, "top": 30},
                "measurements": [], "showGrid": True,
                "traces": [{"color": "rgb(228, 26, 28)", "signal": "V(/u) (gain)", "trace_type": 521}]}],
      "user_defined_signals": [], "version": 7}
(HERE / f"{NAME}.wbk").write_text(json.dumps(wb, indent=2) + "\n", encoding="utf-8")
print("emitted", out)
