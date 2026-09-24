# Lecture 2 problem solving (mechanical systems) in LTspice

`p2.py` prints the hand answers and writes the four schematics. It uses the Lab A
schematic builder from the labs repo (`../../Labs/Lab A/LTspice/gen_ltspice.py`).

    python3 p2.py            # hand results + write the .asc/.plt
    python3 p2.py --verify   # run LTspice headless, compare with the closed form (also the 2.4 limiting cases)
    python3 p2.py --preview  # draw the schematics to preview/*.png and lint the layout

| File | Problem | Look at |
|---|---|---|
| `P2_1_Graphical_Conversion.asc` | 2.1: the sheet's impedance-analogy ladder and its dual mobility circuit, with the solution's `.param` values | `I(Vu_M1)` vs `V(u_M1)` (same for M2, M3): identical; spring force `V(f1)` = `I(Vf_C1)` |
| `P2_2_Mass_Spring.asc` | 2.2: 20 g, 1 mm/N, 0.5 Ns/m; force-driven (10 N) and velocity-driven (1 m/s), both analogies | `I(Vu_A)`, `V(uC)`: velocity peak 20 m/s (26 dB) at 35.6 Hz; `V(fB)`, `I(Vf_D)`: force dip 0.5 N (−6 dB) |
| `P2_3_Equivalent_Sources.asc` | 2.3: Thevenin and Norton in both analogies (Laplace sources for u_No = f/Z_M and u_Th = Y_M f) | `I(Vu_A)`, `I(Vu_B)`, `V(uC)`, `V(uD)` on a linear axis: identical, 20 m/s at 35.6 Hz |
| `P2_4_Two_Mass.asc` | 2.4: two masses, spring ‖ damper, both analogies | `I(Vu1)`, `I(Vu2)`, `V(u1)`, `V(u2)`: u1 dip at 35.6 Hz, u1 peak at 71 Hz |

Impedance analogy: force = voltage, velocity = current (read through 0 V sense
sources, so the sign is right), mass = L, compliance = C, damper = R. Mobility
analogy: velocity = node voltage, force = current, mass = C to ground,
compliance = L, damper = resistor 1/R_M.

Where a voltage source sits in a loop of inductors (2.2 bottom right, 2.4 top),
the inductors get Rser = 1u: LTspice refuses an ideal inductor loop across a
voltage source ("over-defined circuit matrix"). The effect is below 3e-4.

The 2.4 limiting cases are run by `--verify` on temporary copies (M1 or M2 =
1e6 kg, C1 = 1e-12, R1 = 1e9, R1 = 1e-9 with C1 = 1e6); they reproduce the
solution's table. Don't edit the `.asc` by hand; change `p2.py` and regenerate.
