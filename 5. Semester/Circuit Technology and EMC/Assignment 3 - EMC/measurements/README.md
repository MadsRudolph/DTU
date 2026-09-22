# Measurements — Assignment 3 EMC (34654)

Two rooms, three measurements. Fill the CSV templates in this folder on the day; the plots
and the slide tables are generated from them.

| # | What | Where | Template |
|---|---|---|---|
| 1 | Conducted emission of the bare EVM on the LISN | EMC chamber, **b.325 r.261** | `emi_nofilter.csv` |
| 2 | Filter response (S21) | network analyser in the scopes, **329A-020** | `filter_s21.csv` |
| 3 | Conducted emission with the filter in front of the EVM | EMC chamber again | `emi_withfilter.csv` |

Intro video to the EMC equipment: <https://youtu.be/fiSCyV1R1Fw>

## 1 / 3 — EMI receiver + LISN

Setup (CISPR 22 table-top): LISN on the ground plane, EVM on the insulating table, the
**input leads between LISN and EVM as short as you can and kept together**; the load
resistor (1.65 Ω, ≥ 7 W — a 2 A load dissipates 6.6 W, use a power resistor or the
electronic load) on the output. Receiver on **line 1 (L)** of the LISN, the other line
terminated in 50 Ω (the LISN does that itself when nothing is connected, check).

Record before the sweep (there is no "later"):

- [ ] LISN model and the receiver model + firmware (for the block diagram)
- [ ] Receiver settings: RBW **9 kHz** (CISPR band B), detector(s) used (**QP and AV** — the limit table has both), sweep 150 kHz – 30 MHz, attenuator / preamp, any transducer factor of the LISN entered or not
- [ ] Supply: 12.0 V at the LISN input, the supply current (≈ 0.65 A expected)
- [ ] Output: 3.3 V across the load, load current 2 A
- [ ] The actual switching frequency (read it off the fundamental in the spectrum: the RC oscillator is not exactly 300 kHz)
- [ ] Ambient sweep with the EVM **off** (12 V on, but the load open or the EVM disconnected) — that is your noise floor
- [ ] Photo of the setup, photo of the screen, **save the trace to USB** (CSV) — the marker table is not enough

Then the table (`emi_nofilter.csv`): the fundamental, harmonics 2–8, and the **last 5 harmonics
below 30 MHz** (n = 95…99 for exactly 300 kHz; recompute n from the measured f_s: n_max = floor(30 MHz / f_s)).
Note both QP and AV readings and the limit at that frequency.

Quick sanity numbers from the simulation (C1 ESR = 0.3 Ω, see `../results/`): fundamental
around **100 dBµV**, 2nd harmonic ~94, odd harmonics 3 and 6 weak (D ≈ 1/3 → the 3rd harmonic
nearly vanishes, sin(3πD) ≈ 0). Above ~10 MHz expect the common-mode part (switch node to
ground plane) and the layout to dominate, and the numbers there are *not* predicted by the model.

## 2 — Filter S21 on the network analyser (329A-020)

The scope's FRA/network analyser: output → port 1 of the filter (line side), input → port 2
(converter side), 50 Ω termination on port 2 (a feed-through terminator, or the scope input set to 50 Ω).
Sweep **10 kHz – 100 MHz**, log, ≥ 200 points, save the CSV → `filter_s21.csv`.

- [ ] Measure the **through** (no filter, cable to cable) first — that is the 0 dB reference and the noise floor of the setup
- [ ] Expect roughly −40 dB at 300 kHz and −60 … −80 dB from 1 MHz up, then the parasitics of the inductor bring it back up above ~20 MHz. If the floor is −70 dB, you are measuring the setup, not the filter.
- [ ] Also worth a minute: **S21 in the reverse direction** (swap the ports). A π-type filter is not symmetric when one side is only C and the other side is L.

## Parts to bring (proposed filter, see `../ltspice/gen_emc_ltspice.py` FILTER)

| Ref | Value | Notes |
|---|---|---|
| L_f | 10 µH, ≥ 1 A, shielded | e.g. Würth WE-PD 744771110 / Bourns SRR1260-100M; DCR ≤ 50 mΩ |
| C_f1 | 10 µF, 25 V, X7R, 1210 | keeps ~5 µF at 12 V bias; **not** a 0603/0805 |
| C_f2 | 100 nF, 50 V, X7R, 0603/0805 | the top of the band |
| R_d + C_d | 2.2 Ω + 47 µF/25 V electrolytic | damping of the L_f–C1 resonance (~5 kHz), keeps the converter's input from ringing |

Build on a scrap of copper-clad or a small perfboard with a **solid ground/return** — the two
filter caps go across + and return, and the return is one wide strip. Short leads to the EVM.
