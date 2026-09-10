#!/usr/bin/env python3
"""In-class Problem 4.1 - loudspeaker box with bass reflex.

Vented box from Problem 2.3: vent l = 12 cm, D 10 cm, V = 23 l. Driver = baffled
massless piston, same diameter as the vent, prescribed velocity u.

Mechanical (MOBILITY, u = voltage, f = current):
    V1 = u (1 m/s) -> node u;  G2 draws the reaction force f = S_D*p from u.
Acoustic (IMPEDANCE, p = voltage, U = current):
    G1 injects U = S_D*u into node p. Front and back carry the same U (series):
      Z_Af (baffled piston a = 5 cm): L1(M_A1) || [R1(R_A2) + (R2(R_A1) || C1(C_A1))]
      -> node pbox: C2 = C_A (box, to ground)
      -> L2 = M_Av (vent air mass) -> node pv
      -> vent radiation (same network, same a): L5 || [R4 + (R5 || C3)] -> gnd
    The all-inductor path p -> pbox -> pv -> gnd is the DC path (no leak needed).
Z_A seen by the piston = V(p)/U; vent volume velocity = current through L2.
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
NAME = "Problem_4.1_BassReflex_Box"

rho, c = 1.18, 344.0
a = 0.05                                   # vent AND piston radius
S = np.pi * a**2                           # S_D = S_v = 7.854e-3 m^2
V = 23e-3
LV = 0.12
MA1 = 8 * rho / (3 * np.pi**2 * a)         # radiation mass, both openings
RA1 = 0.441 * rho * c / S
RA2 = rho * c / S
CA1 = 5.94 * a**3 / (rho * c**2)
MAV = rho * LV / S
CA = V / (rho * c**2)
fB = 1 / (2 * np.pi * np.sqrt((MAV + MA1) * CA))
AC_CMD = ".ac dec 200 10 10k"

sh = Sheet(paper="A4", title="Problem 4.1 - bass reflex box, Z_A and far field", project=NAME)
def pins(part): return {p.name: p for p in part.pins}

TOP, MID, BOT = G(40), G(58), G(74)        # u/p rails, pbox rail, ground rail

# ---------- mechanical block (mobility): V1 = u, G2 = f = S_D*p ----------
v1 = sh.place("Simulation_SPICE:VDC", "V1", at=(G(12), G(49)), rot=0, value="1")
sh.wire(v1.pin(1), (v1.pin(1).x, TOP))
sh.wire(v1.pin(2), (v1.pin(2).x, BOT))
g2 = sh.place("Simulation_SPICE:GSOURCE", "G2", at=(G(26), G(49)), rot=0, value="GSOURCE")
g2p = pins(g2)                             # rot=0: N+ top, N- bottom, C+/C- left
sh.wire(g2p["N+"], (g2p["N+"].x, TOP))
sh.wire(g2p["N-"], (g2p["N-"].x, BOT))
sh.wire((v1.pin(1).x, TOP), (g2p["N+"].x, TOP))
sh.label((G(18), TOP), "u")
sh.wire(g2p["C+"], (g2p["C+"].x, G(43)))
sh.label((g2p["C+"].x, G(43)), "p")
sh.wire(g2p["C-"], (g2p["C-"].x, BOT))

# ---------- coupling into the acoustic domain: G1 = U = S_D*u ----------
g1 = sh.place("Simulation_SPICE:GSOURCE", "G1", at=(G(44), G(32)), rot=0, value="GSOURCE")
g1p = pins(g1)                             # rot=0: N+ top, N- bottom, C+/C- left
sh.wire(g1p["N+"], (g1p["N+"].x, G(25)))
sh.power("power:GND", (g1p["N+"].x, G(25)), rot=180)
sh.wire(g1p["N-"], (g1p["N-"].x, TOP))
sh.wire(g1p["C+"], (g1p["C+"].x, G(25)))
sh.label((g1p["C+"].x, G(25)), "u")
sh.gnd(g1p["C-"], drop=G(3))

# ---------- Z_Af (front radiation): L || [R_A2 + (R_A1 || C_A1)], p -> pbox ----------
SUB = G(51)
l1 = sh.place("Device:L", "L1", at=(G(56), G(49)), rot=0, value=f"{MA1:.6g}")
sh.wire(l1.pin(1), (l1.pin(1).x, TOP))
sh.wire(l1.pin(2), (l1.pin(2).x, MID))
r1 = sh.place("Device:R", "R1", at=(G(72), G(45)), rot=0, value=f"{RA2:.6g}")
sh.wire(r1.pin(1), (r1.pin(1).x, TOP))
sh.wire(r1.pin(2), (r1.pin(2).x, SUB))
r2 = sh.place("Device:R", "R2", at=(G(68), G(54)), rot=0, value=f"{RA1:.6g}")
c1 = sh.place("Device:C", "C1", at=(G(76), G(54)), rot=0, value=f"{CA1:.6g}")
for part in (r2, c1):
    sh.wire(part.pin(1), (part.pin(1).x, SUB))
    sh.wire(part.pin(2), (part.pin(2).x, MID))
sh.wire((r2.pin(1).x, SUB), (c1.pin(1).x, SUB))
sh.wire((g1p["N-"].x, TOP), (r1.pin(1).x, TOP))
sh.label((G(50), TOP), "p")
sh.wire((l1.pin(2).x, MID), (c1.pin(2).x, MID))

# ---------- box + vent: C_A at pbox, M_Av -> pv -> vent radiation ----------
c2 = sh.place("Device:C", "C2", at=(G(84), G(66)), rot=0, value=f"{CA:.6g}")
sh.wire(c2.pin(1), (c2.pin(1).x, MID))
sh.wire(c2.pin(2), (c2.pin(2).x, BOT))
sh.wire((c1.pin(2).x, MID), (c2.pin(1).x, MID))
sh.label((G(80), MID), "pbox")
l2 = sh.place("Device:L", "L2", at=(G(93), MID), rot=90, value=f"{MAV:.6g}")
sh.wire((c2.pin(1).x, MID), l2.pin(1))
SUB2 = G(65)
l5 = sh.place("Device:L", "L5", at=(G(102), G(66)), rot=0, value=f"{MA1:.6g}")
sh.wire(l5.pin(1), (l5.pin(1).x, MID))
sh.wire(l5.pin(2), (l5.pin(2).x, BOT))
r4 = sh.place("Device:R", "R4", at=(G(112), G(61)), rot=0, value=f"{RA2:.6g}")
sh.wire(r4.pin(1), (r4.pin(1).x, MID))
sh.wire(r4.pin(2), (r4.pin(2).x, SUB2))
r5 = sh.place("Device:R", "R5", at=(G(108), G(70)), rot=0, value=f"{RA1:.6g}")
c3 = sh.place("Device:C", "C3", at=(G(116), G(70)), rot=0, value=f"{CA1:.6g}")
for part in (r5, c3):
    sh.wire(part.pin(1), (part.pin(1).x, SUB2))
    sh.wire(part.pin(2), (part.pin(2).x, BOT))
sh.wire((r5.pin(1).x, SUB2), (c3.pin(1).x, SUB2))
sh.wire(l2.pin(2), (l5.pin(1).x, MID))
sh.wire((l5.pin(1).x, MID), (r4.pin(1).x, MID))
sh.label((G(98), MID), "pv")

# ---------- ground rail ----------
sh.wire((v1.pin(2).x, BOT), (c3.pin(2).x, BOT))
sh.gnd((G(34), BOT), drop=G(4))
sh.wire((G(20), BOT), (G(20), BOT + G(4)))
sh.power("power:PWR_FLAG", (G(20), BOT + G(4)))

# ---------- notes ----------
sh.note((G(12), G(6)), "Problem 4.1 - bass reflex box: vent l = 12 cm, D 10 cm, V = 23 l; massless piston driver, same D, velocity u", size=1.6)
sh.note((G(12), G(10)), f"Mechanical (mobility): V1 = u = 1 m/s, G2 = reaction f = S_D*p, S_D = S_v = {S:.4g} m^2", size=1.2)
sh.note((G(12), G(13)), f"Front + back carry the same U (series): Z_Af (baffled, a = 5 cm): M_A1 = {MA1:.3g}, R_A2 = {RA2:.3g}, R_A1 = {RA1:.3g}, C_A1 = {CA1:.3g}", size=1.2)
sh.note((G(12), G(16)), f"Box: C_A = {CA:.3g} m^5/N; vent: M_Av = rho*l/S = {MAV:.3g} kg/m^4 + same radiation network at pv (DC path is all-inductor)", size=1.2)
sh.note((G(12), G(19)), f"Z_A seen by piston = V(p)/U. Box-port resonance with vent radiation mass: fB = {fB:.0f} Hz (92 Hz without M_A1). U_vent = I(L2)", size=1.2)
sh.note((G(150), G(10)), "SPICE directive (read automatically):", size=1.4)
sh.note((G(150), G(14)), AC_CMD, size=1.8)

problems = sh.check(); print("check():", problems)
for n, m in sh.netlist().items(): print(n, sorted(m))
out = HERE / f"{NAME}.kicad_sch"
sh.emit(str(out))
def ctrl(t, gain): return {"Sim.Device": "SPICE", "Sim.Params": 'type=\\"%s\\" model=\\"%s\\"' % (t, gain)}
set_sim(out, {
    "V1": {"Sim.Device": "V", "Sim.Type": "DC", "Sim.Pins": "1=+ 2=-", "Sim.Params": "dc=1 ac=1"},
    "G1": ctrl("G", f"{S:.6g}"),
    "G2": ctrl("G", f"{S:.6g}"),
})
src = HERE.parent.parent / "Lecture 3" / "Problem_2.3_Two_Tube_Network" / "Problem_2.3_Two_Tube_Network.kicad_pro"
pro = json.loads(src.read_text(encoding="utf-8")); pro["meta"]["filename"] = f"{NAME}.kicad_pro"
(HERE / f"{NAME}.kicad_pro").write_text(json.dumps(pro, indent=2) + "\n", encoding="utf-8")
wb = {"custom_cursors": 2, "last_sch_text_sim_command": AC_CMD,
      "tabs": [{"analysis": "AC", "commands": [AC_CMD, ".kicad adjustpaths", ".save all", ".probe alli", ".probe allp"],
                "dottedSecondary": False, "margins": {"bottom": 45, "left": 70, "right": 70, "top": 30},
                "measurements": [], "showGrid": True,
                "traces": [{"color": "rgb(228, 26, 28)", "signal": "V(/p) (gain)", "trace_type": 521},
                           {"color": "rgb(159, 228, 85)", "signal": "V(/pbox) (gain)", "trace_type": 521}]}],
      "user_defined_signals": [], "version": 7}
(HERE / f"{NAME}.wbk").write_text(json.dumps(wb, indent=2) + "\n", encoding="utf-8")
print("emitted", out)
