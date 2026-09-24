# Lecture 1 problem solving (analogies, introduction) in LTspice

`p1.py` prints the hand answers to problems 1.1–1.3 and writes the three
schematics. It uses the Lab A schematic builder from the labs repo
(`../../Labs/Lab A/LTspice/gen_ltspice.py`), so that repo has to be cloned.

    python3 p1.py            # hand results + write the .asc/.plt
    python3 p1.py --verify   # run LTspice headless, compare with the closed form
    python3 p1.py --preview  # draw the schematics to preview/*.png and lint the layout

| File | Problem | Look at |
|---|---|---|
| `P1_1_DC_Duality.asc` | 1.1: V1 = 10 V, R1 = 100, R2 = 2k, R3 = 500 and its dual (I1 = 10 A, "G" values typed in as resistances) | `.op`: v3 = 8 V, i1 = 20 mA, i3 = 16 mA; dual: V(d_i1) = 20 mV, I(R_G2) = 8 A, I(R_G1) = 2 A, V(d_i3) = 16 mV |
| `P1_2_AC_Duality.asc` | 1.2: V1 – L1 – (C3 ‖ L2) and the dual I1 ‖ C1 – L3 – C2 | `V(vout)` and `I(C2)`: the same curve, 4.1 dB flat, resonance 3979 Hz |
| `P1_3_Series_Resonator.asc` | 1.3: series R = 10, L = 10m, C = 2u, and the same resonator drawn as mechanical and acoustical | `I(Vi)` and `V(vin)/I(Vi)`: 100 mA and 10 Ω at 1125.4 Hz, bandwidth 159 Hz |

The note on the sheet ("check default component settings, e.g. series
resistance for inductor") is about LTspice giving every inductor Rser = 1 mΩ.
In 1.2 that is kept on L1 and L2, and its exact dual (Rpar = 1 kΩ on C1 and C2)
is added, so the two circuits agree to machine precision. The peak is then
62 dB instead of infinite. Don't edit the `.asc` by hand; change `p1.py` and regenerate.
