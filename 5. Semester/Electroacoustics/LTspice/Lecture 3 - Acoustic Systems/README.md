# Lecture 3 problem solving (acoustic systems) in LTspice

`p3.py` prints the hand numbers and writes the schematics. It uses the Lab A
schematic builder from the labs repo (`../../Labs/Lab A/LTspice/gen_ltspice.py`),
so that repo has to be cloned.

    python3 p3.py             # hand numbers + write the .asc/.plt
    python3 p3.py --verify    # run LTspice headless, compare with the closed forms
    python3 p3.py --preview   # draw the schematics to preview/*.png and lint the layout

The slides number these problems 2.1–2.4, the official solution sheet
(`34870_Solutions3.pdf`) 3.1–3.4. The files use the solution sheet's numbers.

| File | Problem | Look at |
|---|---|---|
| `P3-2_Helmholtz_100Hz.asc` | 3.2 (slides 2.2): tube in a box tuned to 100 Hz, M_A = 100 kg/m⁴, C_A = 2.53e-8 m⁵/N | `V(p_in)` = Z_A (U = 1 m³/s): V-shaped dip at 100 Hz, phase −90° → +90° |
| `P3-3_Tubes_in_Box.asc` | 3.3 (slides 2.3): three rows — f) wide tube + box, c–e) narrow tube added, driven from the wide tube, g) driven from the narrow tube | `V(p_in_f)`: dip 92.4 Hz · `V(p_box_de)`: box-pressure peak 9.2 Hz · `V(p_in_de)`: peak 9.2 Hz, dip 92.8 Hz · `V(p_in_g)`: peak 92.4 Hz right next to the dip at 92.8 Hz |

Acoustic impedance analogy: pressure = voltage, volume velocity = current, tube =
inductor (M_A = ρl/S), closed volume = capacitor to ground (C_A = V/ρc²). Problem
3.4 (the dynamic-microphone network) is a drawing only, with no simulation in the
official solution, so it has no schematic here. Don't edit the `.asc` by hand;
change `p3.py` and regenerate.
