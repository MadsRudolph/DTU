# Lecture 4A problem solving (transducers) in LTspice

`p4a.py` prints the hand numbers and writes the schematics. It uses the Lab A
schematic builder from the labs repo (`../../Labs/Lab A/LTspice/gen_ltspice.py`).

    python3 p4a.py             # hand numbers + write the .asc/.plt
    python3 p4a.py --verify    # run LTspice headless, compare with the closed forms and both analogies with each other
    python3 p4a.py --preview   # draw the schematics to preview/*.png and lint the layout

| File | Problem | Look at |
|---|---|---|
| `P4-1_BassReflex_Box.asc` | 4.1: the lecture-3 vented box (12 cm × Ø10 cm vent, 23 L) driven by a massless baffled piston as big as the vent, radiation on the front and at the vent | `(V(pf)-V(pb))/I(G1)` = Z_A seen by the piston: peak ≈ 1.09e6 Pa·s/m³ at 79.4 Hz (official: 995e3). `V(pf)`, `V(pb)`, `V(pv)` = front, box and vent-mouth pressure for u = 1 m/s |
| `P4-4a_Piston_Box.asc` | 4.4a (= Problem 4.2 with numbers): piston 100 cm², 20 g, 2 cm baffle, 40 L box. Top: impedance analogy (E + F), bottom: mobility analogy (G + G) | `V(f)` and `1/V(u_m)` = Z_M = f/u, identical; sharp minimum at 20.4 Hz |
| `P4-4b_Voice_Coil.asc` | 4.4b (= Problem 4.3 with numbers): Bl = 2.1 Tm, 10 g, 1 mm/N, 2 Ns/m, 5 Ω, 0.3 mH. Top: impedance (H + H), bottom: mobility (E + F) | `V(v)` and `V(v_m)` = Z_E (i = 1 A): peak 7.2 Ω at 50 Hz. Velocity `I(Vu)` = `V(u_m)`; forces `V(m1)-V(m2)` (coil mass), `V(m2)-V(m3)` (spring), `V(m3)` (damper) |
| `P4-4c_Coil_on_Piston.asc` | 4.4c: the coil of b) glued to the piston of a), both analogies | `V(v)`, `V(v_m)`: peak moves to 33.0 Hz, 7.2 Ω |

In every sheet the piston is a volume-velocity source U = S·u that sits between
the front node `pf` and the back node `pb`, so `V(pf)-V(pb)` is the pressure
difference p that pushes back on the piston (f = S·p). 4.1 and 4.4 use the
official values: ρ = 1.18 / c = 344 for 4.1 (the lecture-3 box), ρ = 1.2 /
c = 343 for 4.4 (the official `.params`). Don't edit the `.asc` by hand; change
`p4a.py` and regenerate.
