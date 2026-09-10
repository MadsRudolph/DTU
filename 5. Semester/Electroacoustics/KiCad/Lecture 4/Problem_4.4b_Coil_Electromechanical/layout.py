#!/usr/bin/env python3
"""Problem 4.4b (Lecture 4A) - coil in a magnetic field, mobility analogy.

Electrical loop:  V1 (1 V AC) -> R1 = Re -> L1 = Le -> E1 (back-EMF, Bl*u) -> GND
Mechanical node u (mobility analogy: u = voltage, f = current):
    G1 injects f = Bl*i  (i sensed as V(vin)-V(n1) across Re, gain Bl/Re)
    C1 = Mmc (mass), L2 = Cms (compliance), R2 = 1/Rms (damper) - all to ground
Z_E = V(vin)/I(V1) = Re + jwLe + (Bl)^2 / (jwMmc + Rms + 1/(jwCms))
"""
import sys, json, shutil, re
from pathlib import Path
SKILL = "/home/mads/.claude/skills/kicad-schematic/scripts"
sys.path.insert(0, SKILL)
from schdraw import Sheet
from simfields import set_sim

G = lambda n: round(n * 1.27, 2)
HERE = Path(__file__).resolve().parent
NAME = "Problem_4.4b_Coil_Electromechanical"

# --- physical values (Problem 4.4b) ---
l, B = 3.0, 0.7            # m, T
Bl = l * B                 # 2.1 Tm
Mmc, Cms, Rms = 10e-3, 1e-3, 2.0
Re, Le = 5.0, 0.3e-3
AC_CMD = ".ac dec 200 1 10k"

sh = Sheet(paper="A4", title="Problem 4.4b - Coil in magnetic field (mobility analogy)", project=NAME)

def pins(part): return {p.name: p for p in part.pins}

# ---------- electrical block ----------
TOP = G(28); BOT = G(52)
v1 = sh.place("Simulation_SPICE:VDC", "V1", at=(G(20), G(40)), rot=0, value="1")
r1 = sh.place("Device:R", "R1", at=(G(34), TOP), rot=90, value=f"{Re:g}")
l1 = sh.place("Device:L", "L1", at=(G(48), TOP), rot=90, value=f"{Le*1e3:g}m")
e1 = sh.place("Simulation_SPICE:ESOURCE", "E1", at=(G(64), G(40)), rot=0, value="ESOURCE")
ep = pins(e1)

sh.wire(v1.pin(1), (v1.pin(1).x, TOP), r1.pin(1))
sh.label((G(26), TOP), "vin")
sh.wire(r1.pin(2), l1.pin(1))
sh.label((G(42), TOP), "n1")
sh.wire(l1.pin(2), (ep["N+"].x, TOP), ep["N+"])
# back-EMF sense: C+ = node u (via label), C- = GND
sh.wire(ep["C+"], (ep["C+"].x, G(32)))
sh.label((ep["C+"].x, G(32)), "u")
sh.wire(ep["C-"], (ep["C-"].x, BOT))
sh.wire(v1.pin(2), (v1.pin(2).x, BOT))
sh.wire(ep["N-"], (ep["N-"].x, BOT))
sh.wire((v1.pin(2).x, BOT), (ep["N-"].x, BOT))
sh.gnd((G(40), BOT), drop=G(4))

# ---------- mechanical block (mobility) ----------
g1 = sh.place("Simulation_SPICE:GSOURCE", "G1", at=(G(90), G(40)), rot=180, value="GSOURCE")
gp = pins(g1)       # rot=180: N- top, N+ bottom, C- top-right, C+ bottom-right
c1 = sh.place("Device:C", "C1", at=(G(106), G(40)), rot=0, value=f"{Mmc*1e3:g}m")
l2 = sh.place("Device:L", "L2", at=(G(118), G(40)), rot=0, value=f"{Cms*1e3:g}m")
r2 = sh.place("Device:R", "R2", at=(G(130), G(40)), rot=0, value=f"{1/Rms:g}")

# force source output: N- (top) -> node u rail, N+ (bottom) -> ground rail
sh.wire(gp["N-"], (gp["N-"].x, TOP))
sh.wire((gp["N-"].x, TOP), (r2.pin(1).x, TOP))
sh.label((G(98), TOP), "u")
for part in (c1, l2, r2):
    sh.wire(part.pin(1), (part.pin(1).x, TOP))
    sh.wire(part.pin(2), (part.pin(2).x, BOT))
sh.wire(gp["N+"], (gp["N+"].x, BOT))
sh.wire((gp["N+"].x, BOT), (r2.pin(2).x, BOT))
sh.gnd((G(112), BOT), drop=G(4))
# current sense: C+ = vin, C- = n1  (V(vin)-V(n1) = i*Re)
sh.wire(gp["C+"], (gp["C+"].x, G(48)))
sh.label((gp["C+"].x, G(48)), "vin")
sh.wire(gp["C-"], (gp["C-"].x, G(32)))
sh.label((gp["C-"].x, G(32)), "n1")

# PWR_FLAG stubs
for x in (G(30), G(124)):
    sh.wire((x, BOT), (x, BOT + G(4)))
    sh.power("power:PWR_FLAG", (x, BOT + G(4)))

# ---------- notes ----------
sh.note((G(14), G(8)), "Problem 4.4b - coil in magnetic field, mechanical side in MOBILITY analogy", size=1.6)
sh.note((G(14), G(12)), f"Electrical: V1 = 1 V AC, R1 = Re = {Re} ohm, L1 = Le = {Le*1e3:g} mH, E1 = back-EMF = Bl*u (Bl = {Bl:g} Tm)", size=1.3)
sh.note((G(14), G(15)), f"Mechanical (u = voltage, f = current): C1 = Mmc = {Mmc*1e3:g} g, L2 = Cms = {Cms*1e3:g} mm/N, R2 = 1/Rms = {1/Rms:g} ohm", size=1.3)
sh.note((G(14), G(18)), f"G1 = f = Bl*i, sensed across Re -> gain Bl/Re = {Bl/Re:g}", size=1.3)
sh.note((G(14), G(21)), "Plot: Z_E = V(/vin)/I(V1) -> motional peak ~ Re + Bl^2/Rms = 7.2 ohm at f0 = 50.3 Hz", size=1.3)
sh.note((G(150), G(12)), "SPICE directive (read automatically):", size=1.4)
sh.note((G(150), G(16)), AC_CMD, size=1.8)

problems = sh.check(); print("check():", problems)
for n, m in sh.netlist().items(): print(n, sorted(m))
out = HERE / f"{NAME}.kicad_sch"
sh.emit(str(out))

def ctrl(t, gain): return {"Sim.Device": "SPICE", "Sim.Params": 'type=\\"%s\\" model=\\"%s\\"' % (t, gain)}
set_sim(out, {
    "V1": {"Sim.Device": "V", "Sim.Type": "DC", "Sim.Pins": "1=+ 2=-", "Sim.Params": "dc=1 ac=1"},
    "E1": ctrl("E", f"{Bl:g}"),
    "G1": ctrl("G", f"{Bl/Re:g}"),
})

# project file: clone the structure of the Problem 2.3 project
src = HERE.parent.parent / "Lecture 3" / "Problem_2.3_Two_Tube_Network" / "Problem_2.3_Two_Tube_Network.kicad_pro"
pro = json.loads(src.read_text(encoding="utf-8"))
pro["meta"]["filename"] = f"{NAME}.kicad_pro"
(HERE / f"{NAME}.kicad_pro").write_text(json.dumps(pro, indent=2) + "\n", encoding="utf-8")

# workbook (AC analysis, gain + phase of the drive-point voltage and coil velocity)
wb = {"custom_cursors": 2, "last_sch_text_sim_command": AC_CMD,
      "tabs": [{"analysis": "AC",
                "commands": [AC_CMD, ".kicad adjustpaths", ".save all", ".probe alli", ".probe allp"],
                "dottedSecondary": False,
                "margins": {"bottom": 45, "left": 70, "right": 70, "top": 30},
                "measurements": [], "showGrid": True,
                "traces": [{"color": "rgb(228, 26, 28)", "signal": "V(/u) (gain)", "trace_type": 521},
                           {"color": "rgb(55, 126, 184)", "signal": "I(V1) (gain)", "trace_type": 521}]}],
      "user_defined_signals": [], "version": 7}
(HERE / f"{NAME}.wbk").write_text(json.dumps(wb, indent=2) + "\n", encoding="utf-8")
print("emitted", out)
