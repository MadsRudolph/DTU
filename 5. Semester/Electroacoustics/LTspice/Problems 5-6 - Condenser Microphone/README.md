# Problems 5–6 (condenser microphone) in LTspice

`p5.py` prints the Problems 5 hand results and writes four schematics of the
course's condenser-microphone circuit (the one in the official solution to
Problems 5, page 2, and Problems 6, figure 1). It uses the Lab A schematic
builder from the labs repo (`../../Labs/Lab A/LTspice/gen_ltspice.py`), so that
repo has to be cloned.

    python3 p5.py             # hand results + write the .asc/.plt
    python3 p5.py --verify    # run LTspice headless, compare every run with the closed form
    python3 p5.py --preview   # draw the schematics to preview/*.png and lint the layout

| File | Problem | Look at |
|---|---|---|
| `P5_2b_Pressure.asc` | P5 Q2a/b: sheet values, T(s) = 1 (Gpb off, `Tsw=0`), RL = 500 MΩ | `V(out)` = sensitivity [V/Pa]: 9.83 mV/Pa flat, peak 22.5 mV/Pa at 10.1 kHz |
| `P5_2d_FreeField.asc` | P5 Q2d: the same with T(s) on (`Tsw=1`, Gpb = V(p_i)/Ra2) | `V(out)`; `V(pF)` = T(s), 1 → 2 (+6 dB) |
| `P5_2ce_Optimised.asc` | P5 Q2c/e: RL = 1 GΩ, Ras = 80 MΩ (official), `.step param Tsw list 0 1` | run 1 = pressure response, run 2 = free-field response (0 to +1.5 dB up to 8 kHz) |
| `P6_Q2_Sensitivity.asc` | P6 Q2a–d: Q2b circuit, `.step param run 1 14 1` | `V(out)` on a linear axis; the log (Ctrl+L) lists `M250` per run. Runs 2–7 = M_MD, R_MD, C_MD ×0.9/×1.1, runs 8–14 = the same with Gpb on |

Topology (as in the official solution): electrical side a Norton current source
`E·Ce0/x0 · u` into Ce0 ‖ RL; mechanical side an impedance-analogy loop
(Cmd, Vd1, Mmd, Rmd, force source `Sd·(pB − pF)`) with the electrostatic force as a Norton source
`E·Cmd/x0 · i` across Cmd; acoustic side in the impedance analogy, with `U = Sd·u`
taken out of the front node and pushed into the back network (Cab1, Mas + Ras, Cab2).
The front is the unflanged-tube radiation impedance (Ma1 ‖ [Ra2 + Ra1 ‖ Ca1]) to the
1 Pa source, plus the free-field generator Gpb = V(p_i)/Ra2, which makes the blocked
front pressure T(s)·p_i = (1 + Zar/Ra2)·p_i.

`--verify` result: every run matches the closed form of the same circuit to 3e-10.
M(250 Hz) = 9.83 mV/Pa. The official solution reads 9.6 because its figure types the electrical
gain as `1.1m` instead of E·Ce0/x0 = 1.126m (9.83 × 1.1/1.126 = 9.60, and its ±10 % C_MD steps
+0.922/−0.929 become +0.924/−0.930 the same way). Here ±10 % C_MD gives +0.946/−0.952 mV/Pa,
a coefficient of 2373 (V/Pa)/(m/N) against the GUM derivative 2370. M_MD and R_MD move M250 by
under 0.001 mV/Pa, and switching Gpb on changes it by at most 0.07 %.
Using the slide method (−90° phase, linear peak ratio), the full circuit gives f0 = 10.71 kHz and Q = 2.22
where the lumped theory gives 10.62 kHz and 2.36. The difference is real: at 10 kHz ka = 1.6, so the
radiation load is no longer a pure mass. With the radiation replaced by jωMa1, the same method returns
10.64 kHz and 2.33.

Don't edit the `.asc` by hand. Change `p5.py` and regenerate.
