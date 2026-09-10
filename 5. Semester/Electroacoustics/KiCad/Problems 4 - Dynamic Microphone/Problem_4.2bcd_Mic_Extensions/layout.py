#!/usr/bin/env python3
"""Problems 4 (Lecture 4B) sections 2c+2d - dynamic microphone with the
extended back network (values picked in experiments.py, ripple +/-2 dB
100 Hz - 10 kHz):

Acoustic (impedance analogy, p = voltage, U = current):
    V1 = p_i (1 Pa) -> L1 = M_A1 -> pf -> [diaphragm G1: U = S_D*u] -> pb
    -> R1 = R_AF (felt) -> ps -> C1 = C_A1 (small cavity, 0.1 cm^3)
    ps -> R7 = R_At + L3 = M_At (damped tube) -> pc -> C4 = C_A2 (4.9 cm^3)
    pc -> L4 = M_Av + R8 = R_Av (vent, 2d) -> gnd   (also the DC path)
Mechanical (mobility) and electrical blocks identical to Problem_4B.
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
NAME = "Problem_4.2bcd_Mic_Extensions"

rho, c = 1.18, 344.0
MMD, RMS, CMS = 0.2e-3, 1.0, 0.21e-3
a = 0.0254 / 2; SD = np.pi * a**2
Bl, RE, RL = 20.0, 200.0, 47e3
MA1 = 8 * rho / (3 * np.pi**2 * a)
RAF = 2e7
V1V, MAt, RAt = 0.1e-6, 300.0, 3e7
MAv, RAv = 10000.0, 1.5e7
CA1 = V1V / (rho * c**2)
CA2 = (5e-6 - V1V) / (rho * c**2)
AC_CMD = ".ac dec 200 10 100k"

sh = Sheet(paper="A4", title="Problems 4 (2c+2d) - dynamic microphone, extended back network", project=NAME)
def pins(part): return {p.name: p for p in part.pins}
TOP, BOT = G(28), G(52)
ARAIL = G(74)

# ---------- acoustic block ----------
v1 = sh.place("Simulation_SPICE:VDC", "V1", at=(G(16), G(40)), rot=0, value="1")
l1 = sh.place("Device:L", "L1", at=(G(28), TOP), rot=90, value=f"{MA1:.3g}")
g1 = sh.place("Simulation_SPICE:GSOURCE", "G1", at=(G(44), G(40)), rot=0, value="GSOURCE")
g1p = pins(g1)                                   # rot=0: N+ top, N- bottom, C+/C- left
r1 = sh.place("Device:R", "R1", at=(G(58), BOT), rot=90, value=f"{RAF:.3g}")
c1 = sh.place("Device:C", "C1", at=(G(68), G(62)), rot=0, value=f"{CA1:.3g}")
r7 = sh.place("Device:R", "R7", at=(G(78), BOT), rot=90, value=f"{RAt:.3g}")
l3 = sh.place("Device:L", "L3", at=(G(90), BOT), rot=90, value=f"{MAt:.3g}")
c4 = sh.place("Device:C", "C4", at=(G(100), G(62)), rot=0, value=f"{CA2:.3g}")
l4 = sh.place("Device:L", "L4", at=(G(108), G(58)), rot=0, value=f"{MAv:.3g}")
r8 = sh.place("Device:R", "R8", at=(G(108), G(68)), rot=0, value=f"{RAv:.3g}")

sh.wire(v1.pin(1), (v1.pin(1).x, TOP), l1.pin(1))
sh.wire(l1.pin(2), (g1p["N+"].x, TOP), g1p["N+"])
sh.label((G(36), TOP), "pf")
sh.wire(g1p["N-"], (g1p["N-"].x, BOT), r1.pin(1))
sh.label((G(50), BOT), "pb")
sh.wire(r1.pin(2), (c1.pin(1).x, BOT), c1.pin(1))
sh.wire((c1.pin(1).x, BOT), r7.pin(1))
sh.label((G(70), BOT), "ps")
sh.wire(r7.pin(2), l3.pin(1))
sh.wire(l3.pin(2), (c4.pin(1).x, BOT), c4.pin(1))
sh.wire((c4.pin(1).x, BOT), (l4.pin(1).x, BOT))
sh.wire(l4.pin(1), (l4.pin(1).x, BOT))
sh.label((G(104), BOT), "pc")
sh.wire(l4.pin(2), r8.pin(1))
sh.wire(r8.pin(2), (r8.pin(2).x, ARAIL))
for p in (v1.pin(2), c1.pin(2), c4.pin(2)):
    sh.wire(p, (p.x, ARAIL))
sh.wire((v1.pin(2).x, ARAIL), (r8.pin(2).x, ARAIL))
sh.gnd((G(30), ARAIL), drop=G(4))
# diaphragm volume velocity: G1 senses u
sh.wire(g1p["C+"], (g1p["C+"].x, G(32)))
sh.label((g1p["C+"].x, G(32)), "u")
sh.wire(g1p["C-"], (g1p["C-"].x, ARAIL))

# ---------- mechanical block (mobility) ----------
g2 = sh.place("Simulation_SPICE:GSOURCE", "G2", at=(G(122), G(40)), rot=180, value="GSOURCE")
g2p = pins(g2)                                   # rot=180: N- top, N+ bottom, C- top-right, C+ bottom-right
c2 = sh.place("Device:C", "C2", at=(G(136), G(40)), rot=0, value=f"{MMD:.3g}")
l2 = sh.place("Device:L", "L2", at=(G(145), G(40)), rot=0, value=f"{CMS:.3g}")
r4 = sh.place("Device:R", "R4", at=(G(154), G(40)), rot=0, value=f"{1/RMS:g}")
g3 = sh.place("Simulation_SPICE:GSOURCE", "G3", at=(G(168), G(40)), rot=0, value="GSOURCE")
g3p = pins(g3)

sh.wire(g2p["N-"], (g2p["N-"].x, TOP))
sh.wire((g2p["N-"].x, TOP), (g3p["N+"].x, TOP), g3p["N+"])
sh.label((G(130), TOP), "u")
for part in (c2, l2, r4):
    sh.wire(part.pin(1), (part.pin(1).x, TOP))
    sh.wire(part.pin(2), (part.pin(2).x, BOT))
sh.wire(g2p["N+"], (g2p["N+"].x, BOT))
sh.wire(g3p["N-"], (g3p["N-"].x, BOT))
sh.wire((g2p["N+"].x, BOT), (g3p["N-"].x, BOT))
sh.gnd((G(141), BOT), drop=G(4))
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
e1 = sh.place("Simulation_SPICE:ESOURCE", "E1", at=(G(188), G(40)), rot=0, value="ESOURCE")
e1p = pins(e1)
r5 = sh.place("Device:R", "R5", at=(G(200), TOP), rot=90, value=f"{RE:g}")
r6 = sh.place("Device:R", "R6", at=(G(210), G(40)), rot=0, value=f"{RL:g}")
sh.wire(e1p["N+"], (e1p["N+"].x, TOP), r5.pin(1))
sh.wire(r5.pin(2), (r6.pin(1).x, TOP), r6.pin(1))
sh.label((G(206), TOP), "out")
sh.wire(e1p["N-"], (e1p["N-"].x, BOT))
sh.wire(r6.pin(2), (r6.pin(2).x, BOT))
sh.wire((e1p["C-"].x, BOT), (r6.pin(2).x, BOT))
sh.gnd((G(199), BOT), drop=G(4))
sh.wire(e1p["C+"], (e1p["C+"].x, G(32)))
sh.label((e1p["C+"].x, G(32)), "u")
sh.wire(e1p["C-"], (e1p["C-"].x, BOT))

for x in (G(22), G(151), G(204)):
    y = ARAIL if x == G(22) else BOT
    sh.wire((x, y), (x, y + G(4)))
    sh.power("power:PWR_FLAG", (x, y + G(4)))

# ---------- notes ----------
sh.note((G(14), G(6)), "Problems 4 / 2c+2d - dynamic microphone with extended back network, 1 Pa in -> V(out)", size=1.6)
sh.note((G(14), G(10)), f"Acoustic: V1 = p_i = 1 Pa, L1 = M_A1 = {MA1:.3g}, G1 = diaphragm U = S_D*u (S_D = {SD:.3g} m^2), R1 = R_AF = {RAF:.3g}", size=1.2)
sh.note((G(14), G(13)), f"2c split cavity: C1 = C_A1 = {CA1:.3g} (V1 = 0.1 cm^3), damped tube R7 = R_At = {RAt:.3g} + L3 = M_At = {MAt:.3g}, C4 = C_A2 = {CA2:.3g} (V2 = 4.9 cm^3)", size=1.2)
sh.note((G(14), G(16)), f"2d vent in the large cavity: L4 = M_Av = {MAv:.3g} + R8 = R_Av = {RAv:.3g} to ground (Helmholtz f_H = {1/(2*np.pi*np.sqrt(MAv*CA2)):.0f} Hz; also the DC path)", size=1.2)
sh.note((G(14), G(19)), "Mechanical (mobility) + electrical blocks = Problem_4B. Expect approx. -62.5 dB re 1 V/Pa (0.75 mV/Pa) flat +/-2 dB 100 Hz - 10 kHz", size=1.2)
sh.note((G(160), G(10)), "SPICE directive (read automatically):", size=1.4)
sh.note((G(160), G(14)), AC_CMD, size=1.8)

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
src = HERE.parent.parent / "Lecture 3" / "Problem_2.3_Two_Tube_Network" / "Problem_2.3_Two_Tube_Network.kicad_pro"
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
