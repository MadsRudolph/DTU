#!/usr/bin/env python3
"""Lecture 4A slide 9 - massless rigid piston (a = 10 cm), mobility form.

Front: baffled-piston radiation load Z_Af (one side).
Back:  acoustic compliance C_Ab = V/(rho*c^2), V = 10 l.
Plot   Z_M = f/u = S^2 (Z_Af + Z_Ab).

Mechanical (MOBILITY analogy, u = voltage, f = current):
    V1 = u (1 m/s) -> node u;  G2 draws the reaction force f = S*p from u.
Acoustic (IMPEDANCE analogy, p = voltage, U = current):
    G1 injects U = S*u into node p; from p to ground the two loads in SERIES
    (same U through both):
      Z_Af = L1(M_A1) || [ R1(R_A2) + ( R2(R_A1) || C1(C_A1) ) ]   (p -> pm)
      Z_Ab = C2(C_AB), with R3 = 1 TOhm DC leak                     (pm -> gnd)
With u = 1: f = S*V(p), so Z_M = S*V(p); the front/back shares are
S*(V(p)-V(pm)) and S*V(pm) - the three curves of the slide from one AC run.
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
NAME = "Problem_4A_Massless_Piston"

rho, c = 1.18, 344.0
a = 0.10
S = np.pi * a**2
V = 10e-3                                  # 10 l back cavity
MA1 = 8 * rho / (3 * np.pi**2 * a)
RA1 = 0.441 * rho * c / S
RA2 = rho * c / S
CA1 = 5.94 * a**3 / (rho * c**2)
CAB = V / (rho * c**2)
AC_CMD = ".ac dec 200 20 20k"

sh = Sheet(paper="A4", title="Lecture 4A slide 9 - massless piston, Z_M = S^2(Z_Af + Z_Ab)", project=NAME)
def pins(part): return {p.name: p for p in part.pins}

TOP, MID, BOT = G(40), G(58), G(74)        # u/p rails, pm rail, ground rail

# ---------- mechanical block (mobility): V1 = u, G2 = f = S*p ----------
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

# ---------- coupling into the acoustic domain: G1 = U = S*u ----------
# rot=0 above the p rail (Lab A G_a pattern): N+ up to GND, N- down into p,
# so the N+ -> N- current is injected into the p node.
g1 = sh.place("Simulation_SPICE:GSOURCE", "G1", at=(G(44), G(32)), rot=0, value="GSOURCE")
g1p = pins(g1)                             # rot=0: N+ top, N- bottom, C+/C- left
sh.wire(g1p["N+"], (g1p["N+"].x, G(25)))
sh.power("power:GND", (g1p["N+"].x, G(25)), rot=180)
sh.wire(g1p["N-"], (g1p["N-"].x, TOP))
sh.wire(g1p["C+"], (g1p["C+"].x, G(25)))
sh.label((g1p["C+"].x, G(25)), "u")
sh.gnd(g1p["C-"], drop=G(3))

# ---------- Z_Af: L(M_A1) || [R(R_A2) + (R(R_A1) || C(C_A1))], p -> pm ----------
SUB = G(51)                                # node between R_A2 and R_A1||C_A1
l1 = sh.place("Device:L", "L1", at=(G(56), G(49)), rot=0, value=f"{MA1:.3g}")
sh.wire(l1.pin(1), (l1.pin(1).x, TOP))
sh.wire(l1.pin(2), (l1.pin(2).x, MID))
r1 = sh.place("Device:R", "R1", at=(G(72), G(45)), rot=0, value=f"{RA2:.3g}")
sh.wire(r1.pin(1), (r1.pin(1).x, TOP))
sh.wire(r1.pin(2), (r1.pin(2).x, SUB))
r2 = sh.place("Device:R", "R2", at=(G(68), G(54)), rot=0, value=f"{RA1:.3g}")
c1 = sh.place("Device:C", "C1", at=(G(76), G(54)), rot=0, value=f"{CA1:.3g}")
for part in (r2, c1):
    sh.wire(part.pin(1), (part.pin(1).x, SUB))
    sh.wire(part.pin(2), (part.pin(2).x, MID))
sh.wire((r2.pin(1).x, SUB), (c1.pin(1).x, SUB))
sh.wire((g1p["N-"].x, TOP), (r1.pin(1).x, TOP))
sh.label((G(50), TOP), "p")
sh.wire((l1.pin(2).x, MID), (c1.pin(2).x, MID))

# ---------- Z_Ab: back cavity C_AB (+ 1T DC leak), pm -> gnd ----------
c2 = sh.place("Device:C", "C2", at=(G(82), G(66)), rot=0, value=f"{CAB:.3g}")
r3 = sh.place("Device:R", "R3", at=(G(90), G(66)), rot=0, value="1T")
for part in (c2, r3):
    sh.wire(part.pin(1), (part.pin(1).x, MID))
    sh.wire(part.pin(2), (part.pin(2).x, BOT))
sh.wire((c1.pin(2).x, MID), (r3.pin(1).x, MID))
sh.label((G(62), MID), "pm")

# ---------- ground rail ----------
sh.wire((v1.pin(2).x, BOT), (r3.pin(2).x, BOT))
sh.gnd((G(34), BOT), drop=G(4))
sh.wire((G(20), BOT), (G(20), BOT + G(4)))
sh.power("power:PWR_FLAG", (G(20), BOT + G(4)))

# ---------- notes ----------
sh.note((G(12), G(6)), "Lecture 4A slide 9 - massless rigid piston, a = 10 cm: plot Z_M = f/u = S^2 (Z_Af + Z_Ab)", size=1.6)
sh.note((G(12), G(10)), f"Mechanical (mobility, u = V, f = I): V1 = u = 1 m/s, G2 = reaction force f = S*p, S = pi*a^2 = {S:.4g} m^2", size=1.2)
sh.note((G(12), G(13)), f"Front Z_Af (baffled piston, one side): M_A1 = {MA1:.3g} kg/m^4, R_A2 = {RA2:.3g}, R_A1 = {RA1:.3g} Pa s/m^3, C_A1 = {CA1:.3g} m^5/N", size=1.2)
sh.note((G(12), G(16)), f"Back Z_Ab: C_AB = V/(rho c^2) = {CAB:.3g} m^5/N (V = 10 l), in SERIES with Z_Af (same U). R3 = 1T DC leak", size=1.2)
sh.note((G(12), G(19)), f"Z_M = S*V(p); front/back split = S*(V(p)-V(pm)) / S*V(pm). Expect dip at approx. {1/(2*np.pi*np.sqrt(MA1*CAB)):.0f} Hz, plateau S^2*R_A2 = {S*S*RA2:.1f} Ns/m", size=1.2)
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
                           {"color": "rgb(159, 228, 85)", "signal": "V(/p) (phase)", "trace_type": 517}]}],
      "user_defined_signals": [], "version": 7}
(HERE / f"{NAME}.wbk").write_text(json.dumps(wb, indent=2) + "\n", encoding="utf-8")
print("emitted", out)
