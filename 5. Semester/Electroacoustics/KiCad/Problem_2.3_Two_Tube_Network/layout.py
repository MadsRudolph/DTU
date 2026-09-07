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

sh = Sheet(paper="A4", title="Problem 2.3 - Tubes in a Box (Two-Tube Network)",
           project="Problem_2.3_Two_Tube_Network")

# Source: I1 = U, driven from the WIDE tube
i1 = sh.place("Simulation_SPICE:IDC", "I1", at=(G(20), G(40)), rot=0, value="1")
i1_top, i1_bot = topbot(i1)

# L1 = M_A1 (wide tube) - series element from source up to node p
l1 = sh.place("Device:L", "L1", at=(G(50), G(30)), rot=0, value="18.03")
l1_top, l1_bot = topbot(l1)

# C1 = C_A (box compliance) - parallel branch down to ground, right below node p
c1 = sh.place("Device:C", "C1", at=(G(50), G(50)), rot=0, value="164.7n")
c1_top, c1_bot = topbot(c1)

# L2 = M_A2 (narrow tube) - second parallel branch from node p to its own ground (p_out=0)
l2 = sh.place("Device:L", "L2", at=(G(80), G(40)), rot=0, value="1803")
l2_top, l2_bot = topbot(l2)

# top rail: I1 -> L1 (this node is the drive-point / Zin for part e/g)
sh.wire(i1_top, (i1_top.x, l1_top.y), l1_top)
sh.label(i1_top, "Zin", kind="local")

# node p: L1 bottom -> C1 top, and L1 bottom -> right -> L2 top
NODE_P_Y = l1_bot.y
sh.wire(l1_bot, (l1_bot.x, c1_top.y), c1_top)
sh.wire(l1_bot, (l2_top.x, NODE_P_Y), l2_top)
sh.label((l1_bot.x, NODE_P_Y), "p", kind="local")

# bottom ground rail: I1 bottom, C1 bottom, L2 bottom all to one rail
BOTY = G(64)
sh.wire(i1_bot, (i1_bot.x, BOTY))
sh.wire(c1_bot, (c1_bot.x, BOTY))
sh.wire(l2_bot, (l2_bot.x, BOTY))
sh.wire((i1_bot.x, BOTY), (l2_bot.x, BOTY))
sh.gnd((c1_bot.x, BOTY), drop=0)

# PWR_FLAG on its own stub off the ground rail, offset from the GND symbol.
PWRTAP = (G(72), BOTY)
sh.wire(PWRTAP, (PWRTAP[0], BOTY + G(4)))
sh.power("power:PWR_FLAG", (PWRTAP[0], BOTY + G(4)))

sh.note((G(14), G(14)), "Problem 2.3 - Tubes in a box, driven from the wide tube", size=1.6)
sh.note((G(14), G(18)), "L1 = M_A1 (wide tube, a=5cm, l*=12cm) = 18.03", size=1.3)
sh.note((G(14), G(21)), "C1 = C_A (box, V=23L) = 164.7n", size=1.3)
sh.note((G(14), G(24)), "L2 = M_A2 (narrow tube, a=0.5cm, l*=12cm) = 1803", size=1.3)
sh.note((G(14), G(27)), "Node p = box pressure. Expect anti-res ~9.2 Hz, main res ~92.8 Hz", size=1.3)
sh.note((G(14), G(30)), "For part g): move I1 to drive the L2 branch instead", size=1.3)

# Plain schematic directive text -- picked up by KiCad's ReadDirectives()
# even with no workbook loaded, so Run works with zero manual setup.
# Placed well clear of the circuit and the note block so it never crowds them.
sh.note((G(120), G(30)), "SPICE directive (read automatically, no workbook needed):", size=1.4)
sh.note((G(120), G(34)), ".ac dec 200 1 1000", size=1.8)

problems = sh.check()
print("check():", problems)

nets = sh.netlist()
for name, members in nets.items():
    print(name, sorted(members))

out = "/home/mads/DTU/5. Semester/Electroacoustics/KiCad/Problem_2.3_Two_Tube_Network/Problem_2.3_Two_Tube_Network.kicad_sch"
sh.emit(out)
print("emitted", out)
print("SHEET_UUID", sh.uuid)
