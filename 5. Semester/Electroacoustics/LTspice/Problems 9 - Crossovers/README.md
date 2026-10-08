# Problems 9 (Loudspeakers 3: crossovers) in LTspice

`p9.py` prints the answers to problems 1–2 next to the brackets and writes the
two schematics for problem 3. It uses the Lab A schematic builder from the labs
repo (`../../Labs/Lab A/LTspice/gen_ltspice.py`), so that repo has to be cloned.

    python3 p9.py                    # problems 1-3 + write the .asc/.plt
    python3 p9.py --verify --plots   # run LTspice headless, compare with the closed form, write the vault figures
    python3 p9.py --preview          # draw the schematics to preview/*.png and lint the layout

| File | Problem | Look at |
|---|---|---|
| `P9_3_BW2_250Hz.asc` | 3a, 3b: 2nd-order Butterworth at 250 Hz on R_E; `pol=-1` inverts the midrange, `Q=0.5` makes it LR2 | `V(pw)*5e4`, `V(pm)*5e4`, `V(ptot)*5e4` in dB = SPL at 1 m for 2.83 V; `V(vw)` vs `V(vw_id)` = the filter into the driver vs into R_E |
| `P9_3_LR4_250Hz.asc` | 3c: 4th-order Linkwitz-Riley ladder of slide 15 | same traces; sum with `pol=1` |

Peerless SLS-P830669 in 40 L (f_C 65 Hz, Q_TC 1.12) and NE123W-08 in 2 L
(f_C 122 Hz, Q_TC 0.69), data-sheet T-S values, closed box with M_AB = M_A1 so
only the spring changes: C_MT = C_MS/(1 + V_AS/V_B). Impedance analogy, H sources
for the Bl couplings, far-field pressure from an E source with `Laplace=k*s` on
the velocity. Every filter element is a `.param` expression of `fc`, `Q` and R_E,
so changing `fc` redesigns the filter. Don't edit the `.asc` by hand; change
`p9.py` and regenerate.
