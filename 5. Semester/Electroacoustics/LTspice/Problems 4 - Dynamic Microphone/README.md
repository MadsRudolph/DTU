# Problems 4 (dynamic microphones) in LTspice

`p4.py` prints the hand answers to problem 1 and writes the schematics for
problem 2. It uses the Lab A schematic builder from the labs repo
(`../../Labs/Lab A/LTspice/gen_ltspice.py`), so that repo has to be cloned.

    python3 p4.py             # problem 1 + write the .asc/.plt
    python3 p4.py --verify    # run LTspice headless and compare V(out) with the closed form
    python3 p4.py --preview   # draw the schematics to preview/*.png and lint the layout

| File | Problem | Look at |
|---|---|---|
| `P4_2a_Basic.asc` | 2a: V = 5 cm³, R_AF = 2e7 | `V(out)` = sensitivity in V/Pa (p_i = 1 Pa): peak 1.643 mV/Pa (−55.7 dB re 1 V/Pa) at 1.22 kHz, band 291 Hz – 5.07 kHz |
| `P4_2b_Sensitivity.asc` | 2b: `.step param Raf list 1.2708e8 2e7 9.173e6` | `V(out)`: 0.300 / 1.643 / 3.000 mV/Pa, all peaking at 1.22 kHz |
| `P4_2c_TwoCavities.asc` | 2c: small cavity V1 + damped tube + large cavity V2 (official values) | `V(out)`: same −60 dB mid-band as the 1b/1c design, −3 dB point moves from 8.0 to 13.2 kHz |
| `P4_2d_Vent.asc` | 2d: 2c + vent tube from V2 to the outside (official compensated mic) | `V(out)`: bump near 56 Hz (f_H = 64.5 Hz), −3 dB from 46 Hz to 13 kHz |

Topology = the official solution's: impedance analogy in all three domains.
H sources for the two Bl couplings, E source for the force S_D·(p_f − p_b),
F source `F_U` for the diaphragm's volume velocity U = S_D·u. The front air
mass is the piston-in-a-tube value M_A1 = 0.6133ρ/(πa) = 18.14 kg/m⁴, as in
the official solution. The vent in 2d ends on the incident-pressure node `pi`
(outside air), not on ground. `P4_2c` has a 1 TΩ `R_leak` directive only so
LTspice finds a DC operating point. `--verify` agrees with the closed form to
better than 1e-4 on every file. Don't edit the `.asc` by hand; change `p4.py`
and regenerate.
