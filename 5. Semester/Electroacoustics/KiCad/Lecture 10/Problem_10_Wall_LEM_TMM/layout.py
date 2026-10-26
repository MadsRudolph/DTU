#!/usr/bin/env python3
"""Lecture 10 (Advanced topics, 26-Oct-2026), slides 4-6 - sound transmission through a
five-layer wall, the KiCad/ngspice twin of ../../../LTspice/Lecture 10 - Mixed Models/p10.py.

Layers (slide 4, left to right): drywall 1 cm | insulation 3 cm | brick 5 cm | air gap 1 cm |
wood 2 cm. Per unit area, IMPEDANCE analogy: node voltage = pressure [Pa], current = particle
velocity [m/s], impedances in Pa s/m.

Three rows, each driven by its own 1 V (= 1 Pa) source, so V(poutN) is the transmission:
    row 1 (slide 5, LEM):          solids = series L = rho*l, soft layers = shunt C = l/(rho c^2)
    row 2 (slide 6 top, mixed):    solids as L, insulation + air gap as lossless lines (TLINE)
    row 3 (slide 6 bottom, TMM):   every layer a line, Z0 = rho*c, td = l/c
Each row ends in R_out = rho0*c0 (the radiation impedance of the air behind the wall).
The TLINE return pins (2, 4) go to ground, like LTspice's tline in p10.py.
"""
import sys, json
from pathlib import Path
SKILL = "/home/mads/.claude/skills/kicad-schematic/scripts"
sys.path.insert(0, SKILL)
from schdraw import Sheet
from simfields import set_sim

G = lambda n: round(n * 1.27, 2)
HERE = Path(__file__).resolve().parent
NAME = "Problem_10_Wall_LEM_TMM"

RHO0, C0 = 1.2, 343.0
LAYERS = [  # name, rho, c, l
    ("drywall 1 cm", 600.0, 6000.0, 0.01),
    ("insulation 3 cm", 200.0, 500.0, 0.03),
    ("brick 5 cm", 2000.0, 3600.0, 0.05),
    ("air gap 1 cm", 1.2, 343.0, 0.01),
    ("wood 2 cm", 550.0, 4000.0, 0.02),
]
ROUT = RHO0 * C0
AC_CMD = ".ac dec 2000 20 20k"
KINDS = {"1": ["L", "C", "L", "C", "L"], "2": ["L", "T", "L", "T", "L"], "3": ["T"] * 5}
TITLES = {"1": "Row 1 - LEM (slide 5)", "2": "Row 2 - LEM + TMM (slide 6 top)",
          "3": "Row 3 - full TMM (slide 6 bottom)"}

sh = Sheet(paper="A4", title="Lecture 10 - five-layer wall: LEM, mixed and TMM", project=NAME)
sim = {}
X0, W = G(26), G(22)                 # first slot start, slot width per layer

for tag, Y in (("1", G(40)), ("2", G(76)), ("3", G(112))):
    sh.note((G(10), Y - G(10)), TITLES[tag], size=1.6)
    v = sh.place("Simulation_SPICE:VDC", f"V{tag}", at=(G(14), Y + G(4)), rot=0, value="AC 1")
    sim[f"V{tag}"] = {"Sim.Device": "V", "Sim.Type": "DC", "Sim.Pins": "1=+ 2=-", "Sim.Params": "dc=0 ac=1"}
    sh.wire(v.pin(1), (X0, Y))
    sh.label((G(20), Y), f"pin{tag}")
    sh.gnd(v.pin(2), drop=G(2))
    for k, kind in enumerate(KINDS[tag]):
        name, rho, c, l = LAYERS[k]
        sx, mid = X0 + k * W, X0 + k * W + W / 2
        ref = f"{kind}{k + 1}{tag}" if kind != "T" else f"T{k + 1}{tag}"
        if kind == "L":
            p = sh.place("Device:L", ref, at=(mid, Y), rot=90, value=f"{rho * l:.6g}")
            sh.wire((sx, Y), p.pin(1)); sh.wire(p.pin(2), (sx + W, Y))
            what = f"M = rho*l = {rho * l:g}"
        elif kind == "C":
            p = sh.place("Device:C", ref, at=(mid, Y + G(3)), rot=0, value=f"{l / (rho * c ** 2):.6g}")
            sh.wire((sx, Y), (mid, Y)); sh.wire((mid, Y), (sx + W, Y))
            sh.gnd(p.pin(2), drop=G(2))
            what = f"C = l/(rho c^2) = {l / (rho * c ** 2):.4g}"
        else:
            p = sh.place("Simulation_SPICE:TLINE", ref, at=(mid, Y), rot=0, value="TLINE")
            pp = {q.number: q for q in p.pins}
            sh.wire((sx, Y), pp["1"]); sh.wire(pp["3"], (sx + W, Y))
            sh.gnd(pp["2"], pp["4"], drop=G(3))
            sim[ref] = {"Sim.Device": "TLINE", "Sim.Pins": "1=1+ 2=1- 3=2+ 4=2-",
                        "Sim.Params": f"z0={rho * c:.6g} td={l / c:.6g}"}
            what = f"Z0 = {rho * c:g}, td = {l / c * 1e6:.4g} us"
        sh.note((sx + G(1), Y - G(6)), name, size=1.1)
        sh.note((sx + G(1), Y - G(4)), what, size=0.9)
    xe = X0 + 5 * W
    r = sh.place("Device:R", f"Rout{tag}", at=(xe + G(6), Y + G(3)), rot=0, value=f"{ROUT:.6g}")
    sh.wire((xe, Y), r.pin(1))
    sh.label((xe + G(3), Y), f"pout{tag}")
    sh.gnd(r.pin(2), drop=G(2))

sh.wire((G(190), G(40)), (G(190), G(42)))
sh.power("power:PWR_FLAG", (G(190), G(40)))
sh.gnd((G(190), G(42)), drop=G(1))

sh.note((G(10), G(12)), "Lecture 10 (26-Oct-2026), slides 4-6: plane-wave transmission through a five-layer wall", size=1.6)
sh.note((G(10), G(16)), "Per unit area, impedance analogy: V = pressure [Pa], I = particle velocity [m/s]. "
        f"R_out = rho0*c0 = {ROUT:g} Pa s/m. Plot V(/pout1..3) in dB.", size=1.2)
sh.note((G(10), G(19)), "Twin of LTspice/Lecture 10 - Mixed Models/p10.py; sim.py checks all three rows against the closed form.", size=1.2)
sh.note((G(170), G(16)), "SPICE directive (read automatically):", size=1.4)
sh.note((G(170), G(20)), AC_CMD, size=1.8)

problems = sh.check(); print("check():", problems)
out = HERE / f"{NAME}.kicad_sch"
sh.emit(str(out))
set_sim(out, sim)

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
                "traces": [{"color": col, "signal": f"V(/pout{t}) (gain)", "trace_type": 521}
                           for t, col in (("1", "rgb(228, 26, 28)"), ("2", "rgb(55, 126, 184)"),
                                          ("3", "rgb(77, 175, 74)"))]}],
      "user_defined_signals": [], "version": 7}
(HERE / f"{NAME}.wbk").write_text(json.dumps(wb, indent=2) + "\n", encoding="utf-8")
print("emitted", out)
