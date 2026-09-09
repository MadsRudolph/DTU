#!/usr/bin/env python3
"""Problems 4 (Lecture 4B) section 2a - dynamic pressure microphone, three domains.

Acoustic (impedance analogy, p = voltage, U = current):
    V1 = p_i (1 Pa) -> L1 = M_A1 (front air mass) -> node pf -> [diaphragm] -> node pb
    -> R1 = R_AF (felt) -> C1 = C_AB (back volume) -> GND        (R3 = 100 Meg DC leak)
    The diaphragm is G1: it carries U = S_D*u from pf to pb (VCCS sensing u).
Mechanical (MOBILITY analogy, u = voltage, f = current), node u:
    G2 injects f = S_D*(pf - pb);  C2 = M_MD, L2 = C_MS, R4 = 1/R_MS to ground;
    G3 draws the electromagnetic reaction force Bl*i (i = V(out)/R_L).
Electrical: E1 = Bl*u -> R5 = R_E -> node out -> R6 = R_L -> GND.  Sensitivity = V(out)/p_i.
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
NAME = "Problem_4B_Dynamic_Microphone"

rho, c = 1.18, 344.0
MMD, RMS, CMS = 0.2e-3, 1.0, 0.21e-3
a = 0.0254 / 2; SD = np.pi * a**2
Bl, RE, RL = 20.0, 200.0, 47e3
V, RAF = 5e-6, 2e7
MA1 = 8 * rho / (3 * np.pi**2 * a)
CAB = V / (rho * c**2)
AC_CMD = ".ac dec 200 10 100k"

sh = Sheet(paper="A4", title="Problems 4 (2a) - Dynamic pressure microphone, three domains", project=NAME)
def pins(part): return {p.name: p for p in part.pins}
TOP, BOT = G(28), G(52)

# ---------- acoustic block ----------
v1 = sh.place("Simulation_SPICE:VDC", "V1", at=(G(16), G(40)), rot=0, value="1")
l1 = sh.place("Device:L", "L1", at=(G(28), TOP), rot=90, value=f"{MA1:.3g}")
g1 = sh.place("Simulation_SPICE:GSOURCE", "G1", at=(G(44), G(40)), rot=0, value="GSOURCE")
g1p = pins(g1)                                   # rot=0: N+ top, N- bottom, C+/C- to the left
r1 = sh.place("Device:R", "R1", at=(G(58), BOT), rot=90, value=f"{RAF:.3g}")
c1 = sh.place("Device:C", "C1", at=(G(68), G(60)), rot=0, value=f"{CAB:.3g}")
r3 = sh.place("Device:R", "R3", at=(G(76), G(60)), rot=0, value="1T")

sh.wire(v1.pin(1), (v1.pin(1).x, TOP), l1.pin(1))
sh.wire(l1.pin(2), (g1p["N+"].x, TOP), g1p["N+"])
sh.label((G(36), TOP), "pf")
sh.wire(g1p["N-"], (g1p["N-"].x, BOT), r1.pin(1))
sh.label((G(50), BOT), "pb")
sh.wire(r1.pin(2), (c1.pin(1).x, BOT), c1.pin(1))
sh.wire((c1.pin(1).x, BOT), (r3.pin(1).x, BOT), r3.pin(1))
ARAIL = G(66)
for p in (v1.pin(2), c1.pin(2), r3.pin(2)):
    sh.wire(p, (p.x, ARAIL))
sh.wire((v1.pin(2).x, ARAIL), (r3.pin(2).x, ARAIL))
sh.gnd((G(30), ARAIL), drop=G(4))
# diaphragm volume velocity: G1 senses u
sh.wire(g1p["C+"], (g1p["C+"].x, G(32)))
sh.label((g1p["C+"].x, G(32)), "u")
sh.wire(g1p["C-"], (g1p["C-"].x, ARAIL))

# ---------- mechanical block (mobility) ----------
g2 = sh.place("Simulation_SPICE:GSOURCE", "G2", at=(G(96), G(40)), rot=180, value="GSOURCE")
g2p = pins(g2)                                   # rot=180: N- top, N+ bottom, C- top-right, C+ bottom-right
c2 = sh.place("Device:C", "C2", at=(G(112), G(40)), rot=0, value=f"{MMD:.3g}")
l2 = sh.place("Device:L", "L2", at=(G(122), G(40)), rot=0, value=f"{CMS:.3g}")
r4 = sh.place("Device:R", "R4", at=(G(132), G(40)), rot=0, value=f"{1/RMS:g}")
g3 = sh.place("Simulation_SPICE:GSOURCE", "G3", at=(G(148), G(40)), rot=0, value="GSOURCE")
g3p = pins(g3)

sh.wire(g2p["N-"], (g2p["N-"].x, TOP))
sh.wire((g2p["N-"].x, TOP), (g3p["N+"].x, TOP), g3p["N+"])
sh.label((G(104), TOP), "u")
for part in (c2, l2, r4):
    sh.wire(part.pin(1), (part.pin(1).x, TOP))
    sh.wire(part.pin(2), (part.pin(2).x, BOT))
sh.wire(g2p["N+"], (g2p["N+"].x, BOT))
sh.wire(g3p["N-"], (g3p["N-"].x, BOT))
sh.wire((g2p["N+"].x, BOT), (g3p["N-"].x, BOT))
sh.gnd((G(117), BOT), drop=G(4))
# G2 senses the pressure across the diaphragm: C+ = pf, C- = pb
sh.wire(g2p["C+"], (g2p["C+"].x, G(48)))
sh.label((g2p["C+"].x, G(48)), "pf")
sh.wire(g2p["C-"], (g2p["C-"].x, G(32)))
sh.label((g2p["C-"].x, G(32)), "pb")
# G3 senses the output voltage (coil current = V(out)/RL): C+ = out, C- = GND
sh.wire(g3p["C+"], (g3p["C+"].x, G(32)))
sh.label((g3p["C+"].x, G(32)), "out")
sh.wire(g3p["C-"], (g3p["C-"].x, BOT))

# ---------- electrical block ----------
e1 = sh.place("Simulation_SPICE:ESOURCE", "E1", at=(G(172), G(40)), rot=0, value="ESOURCE")
e1p = pins(e1)
r5 = sh.place("Device:R", "R5", at=(G(186), TOP), rot=90, value=f"{RE:g}")
r6 = sh.place("Device:R", "R6", at=(G(198), G(40)), rot=0, value=f"{RL:g}")
sh.wire(e1p["N+"], (e1p["N+"].x, TOP), r5.pin(1))
sh.wire(r5.pin(2), (r6.pin(1).x, TOP), r6.pin(1))
sh.label((G(194), TOP), "out")
sh.wire(e1p["N-"], (e1p["N-"].x, BOT))
sh.wire(r6.pin(2), (r6.pin(2).x, BOT))
sh.wire((e1p["C-"].x, BOT), (r6.pin(2).x, BOT))
sh.gnd((G(185), BOT), drop=G(4))
sh.wire(e1p["C+"], (e1p["C+"].x, G(32)))
sh.label((e1p["C+"].x, G(32)), "u")
sh.wire(e1p["C-"], (e1p["C-"].x, BOT))

for x in (G(22), G(127), G(192)):
    y = ARAIL if x == G(22) else BOT
    sh.wire((x, y), (x, y + G(4)))
    sh.power("power:PWR_FLAG", (x, y + G(4)))

# ---------- notes ----------
sh.note((G(14), G(6)), "Problems 4 / 2a - dynamic pressure microphone (Leach fig. 5.x), 1 Pa in -> V(out) = sensitivity", size=1.6)
sh.note((G(14), G(10)), f"Acoustic (p = V, U = I): V1 = p_i = 1 Pa, L1 = M_A1 = {MA1:.3g} kg/m^4 (baffled piston, a = 12.7 mm), R1 = R_AF = {RAF:.3g}, C1 = C_AB = {CAB:.3g} (V = 5 cm^3), R3 = 1 TOhm DC leak (>> 1/wC_AB even at 10 Hz)", size=1.2)
sh.note((G(14), G(13)), f"G1 = diaphragm: U = S_D*u through pf->pb, gain S_D = {SD:.3g} m^2", size=1.2)
sh.note((G(14), G(16)), f"Mechanical (mobility, u = V, f = I): G2 = f = S_D*(pf-pb); C2 = M_MD = {MMD:.3g} kg, L2 = C_MS = {CMS:.3g} m/N, R4 = 1/R_MS = {1/RMS:g}; G3 = -Bl*i (gain Bl/R_L = {Bl/RL:.3g})", size=1.2)
sh.note((G(14), G(19)), f"Electrical: E1 = Bl*u (Bl = {Bl:g} Tm), R5 = R_E = {RE:g}, R6 = R_L = {RL:g}. Expect band-pass, f0 ~ 1.2 kHz, M ~ -56 dB re 1 V/Pa", size=1.2)
sh.note((G(150), G(10)), "SPICE directive (read automatically):", size=1.4)
sh.note((G(150), G(14)), AC_CMD, size=1.8)

problems = sh.check(); print("check():", problems)
for n, m in sh.netlist().items(): print(n, sorted(m))
out = HERE / f"{NAME}.kicad_sch"
sh.emit(str(out))
def ctrl(t, gain): return {"Sim.Device": "SPICE", "Sim.Params": 'type=\\"%s\\" model=\\"%s\\"' % (t, gain)}
set_sim(out, {
    "V1": {"Sim.Device": "V", "Sim.Type": "DC", "Sim.Pins": "1=+ 2=-", "Sim.Params": "dc=1 ac=1"},
    "G1": ctrl("G", f"{SD:.6g}"),
    "G2": ctrl("G", f"{SD:.6g}"),
    "G3": ctrl("G", f"{Bl/RL:.6g}"),
    "E1": ctrl("E", f"{Bl:g}"),
})
src = HERE.parent / "Problem_2.3_Two_Tube_Network" / "Problem_2.3_Two_Tube_Network.kicad_pro"
pro = json.loads(src.read_text(encoding="utf-8")); pro["meta"]["filename"] = f"{NAME}.kicad_pro"
(HERE / f"{NAME}.kicad_pro").write_text(json.dumps(pro, indent=2) + "\n", encoding="utf-8")
wb = {"custom_cursors": 2, "last_sch_text_sim_command": AC_CMD,
      "tabs": [{"analysis": "AC", "commands": [AC_CMD, ".kicad adjustpaths", ".save all", ".probe alli", ".probe allp"],
                "dottedSecondary": False, "margins": {"bottom": 45, "left": 70, "right": 70, "top": 30},
                "measurements": [], "showGrid": True,
                "traces": [{"color": "rgb(228, 26, 28)", "signal": "V(/out) (gain)", "trace_type": 521},
                           {"color": "rgb(159, 228, 85)", "signal": "V(/out) (phase)", "trace_type": 517}]}],
      "user_defined_signals": [], "version": 7}
(HERE / f"{NAME}.wbk").write_text(json.dumps(wb, indent=2) + "\n", encoding="utf-8")
print("emitted", out)
