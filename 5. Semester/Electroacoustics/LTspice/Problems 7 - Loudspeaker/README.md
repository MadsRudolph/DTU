# Problems 7 (Loudspeakers 1) in LTspice

`p7.py` prints the hand answers to problems 1–3 and writes the two schematics
for problem 4. It uses the Lab A schematic builder from the labs repo
(`../../Labs/Lab A/LTspice/gen_ltspice.py`), so that repo has to be cloned.

    python3 p7.py                    # problems 1-3 + write the .asc/.plt
    python3 p7.py --verify --plots   # run LTspice headless, compare with the closed form, write the vault figures
    python3 p7.py --preview          # draw the schematics to preview/*.png and lint the layout

| File | Problem | Look at |
|---|---|---|
| `P7_315SWR_Baffle.asc` | 4.1, 4.2: voice coil = R_E only | `V(eg)/I(Vd1)` = Z_E (peak 46 Ω at 22.9 Hz); `V(SPLff)`, `V(SPLnf)` in dB = SPL for 1 V |
| `P7_315SWR_Baffle_LossyLe.asc` | 4.3: adds Z = 0.0106·(jω)^0.76 as a G source with a Laplace expression | same traces; `V(xD)` = displacement per volt |

Same topology as slide 27 of the lecture (Leach): impedance analogy in every
domain, H sources for the Bl couplings, F source for U = S_D·u, both radiation
impedances drawn as one baffled-piston network with every element doubled.
`M_MD = M_MS(baffled) − 2·S_D²·M_A1 = 74.6 g`, so the circuit's own air load
restores the data-sheet 88.2 g. Don't edit the `.asc` by hand; change `p7.py` and regenerate.
