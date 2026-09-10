#!/usr/bin/env python3
import sys
SKILL = "/home/mads/.claude/skills/kicad-schematic/scripts"
sys.path.insert(0, SKILL)
from schdraw import Sheet

G = lambda n: round(n * 1.27, 2)

def topbot(part):
    a, b = part.pin(1), part.pin(2)
    top = a if a.y < b.y else b
    bot = b if top is a else a
    return top, bot

sh = Sheet(paper="A4", title="Problem 2.1-2.2 - Helmholtz Resonator (Tube in a Box)",
           project="Problem_2.1-2.2_Helmholtz_Resonator")

# Left branch: AC current source I1 = U (volume velocity source)
i1 = sh.place("Simulation_SPICE:IDC", "I1", at=(G(20), G(40)), rot=0, value="1")
i1_top, i1_bot = topbot(i1)

# Right branch, top: L1 = M_A (tube mass)
l1 = sh.place("Device:L", "L1", at=(G(50), G(30)), rot=0, value="187.8")
l1_top, l1_bot = topbot(l1)

# Right branch, bottom: C1 = C_A (box compliance)
c1 = sh.place("Device:C", "C1", at=(G(50), G(50)), rot=0, value="13.49n")
c1_top, c1_bot = topbot(c1)

# DC leak resistor across C1 -- an ideal current source in series with a bare
# capacitor branch has no DC operating point (capacitor blocks the forced DC
# current -> singular matrix). 100 Meg is >>|Zc| over 10 Hz-1 kHz so it does
# not perturb the AC magnitude/phase, it only gives ngspice's .op a path.
rleak = sh.place("Device:R", "R1", at=(G(70), G(50)), rot=0, value="100Meg")
rl_top, rl_bot = topbot(rleak)

# top rail: I1 top -> L1 top (this node IS the drive-point / Zin node,
# since I1 = 1A AC, V(Zin) reads directly as |Z(f)| in ohms)
sh.wire(i1_top, (i1_top.x, l1_top.y), l1_top)
sh.label(i1_top, "Zin", kind="local")

# L1 bottom -> C1 top -> R1 top (parallel)
sh.wire(l1_bot, (l1_bot.x, c1_top.y), c1_top)
sh.wire(c1_top, (rl_top.x, c1_top.y), rl_top)

# bottom rail: I1 bottom -> down -> across -> up to C1/R1 bottom, with ground
BOTY = G(64)
sh.wire(i1_bot, (i1_bot.x, BOTY))
sh.wire((i1_bot.x, BOTY), (rl_bot.x, BOTY))
sh.wire(c1_bot, (c1_bot.x, BOTY))
sh.wire(rl_bot, (rl_bot.x, BOTY))
sh.gnd((i1_bot.x, BOTY), drop=G(4))

# PWR_FLAG on its own stub off the ground rail -- NOT stacked on the GND
# symbol itself, or the two symbols render on top of each other illegibly.
PWRTAP = (G(45), BOTY)
sh.wire(PWRTAP, (PWRTAP[0], BOTY + G(4)))
sh.power("power:PWR_FLAG", (PWRTAP[0], BOTY + G(4)))

sh.note((G(14), G(12)), "Problem 2.1/2.2 - Tube in a box (Helmholtz resonator)", size=1.6)
sh.note((G(14), G(16)), "L1 = M_A (tube, l*=5cm, a=1cm)   C1 = C_A (box, V~1.9L)", size=1.3)
sh.note((G(14), G(19)), "R1 = DC leak path for ngspice (100 Meg >> |Zc| in-band, negligible)", size=1.3)
sh.note((G(14), G(22)), "I1 = 1A AC -> V(Zin) reads directly as |Z(f)| in ohms", size=1.3)
sh.note((G(14), G(25)), "Expected series resonance f0 = 100 Hz (dip in V(Zin))", size=1.3)

# A plain schematic text item containing a recognized SPICE directive line
# (".AC ...", matched case-insensitively by KiCad's own ReadDirectives()) is
# picked up automatically as the simulation command even with NO workbook
# loaded at all -- this is the reliable path, independent of any .wbk quirks.
# Placed well clear of the circuit and the note block so it never crowds them.
sh.note((G(120), G(30)), "SPICE directive (read automatically, no workbook needed):", size=1.4)
sh.note((G(120), G(34)), ".ac dec 200 10 1000", size=1.8)

problems = sh.check()
print("check():", problems)

nets = sh.netlist()
for name, members in nets.items():
    print(name, sorted(members))

out = "/home/mads/DTU/5. Semester/Electroacoustics/KiCad/Problem_2.1-2.2_Helmholtz_Resonator/Problem_2.1-2.2_Helmholtz_Resonator.kicad_sch"
sh.emit(out)
print("emitted", out)
print("SHEET_UUID", sh.uuid)
