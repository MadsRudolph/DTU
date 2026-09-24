# 34870 MATLAB worked problem sets

One Live Script per problem set. Open the `.mlx` in MATLAB and press Run. Every
step states the formula first, then one MATLAB line that is the same formula
typed in, then the result, with the official answer in the text next to it.
The `.html` next to each one is an export with all outputs and plots, readable
without MATLAB. The `.m` is the editable source; the `.mlx` is gitignored and
travels over Syncthing.

| Live Script | Problems | LTspice (in `../LTspice/`) |
|---|---|---|
| `Lecture1_Analogies_Problems` | 1.1 DC duality, 1.2 AC duality, 1.3 series resonator in three domains | `Lecture 1 - Analogies/` |
| `Lecture2_MechanicalSystems_Problems` | 2.1–2.4 (graphical conversion, mass-spring, Thevenin/Norton, two masses) + bonus problems 5–6 | `Lecture 2 - Mechanical Systems/` |
| `Lecture3_AcousticSystems_Problems` | 3.1–3.4 (Helmholtz resonator, tubes in a box, ear canal drawing). The slides number these 2.1–2.4 | `Lecture 3 - Acoustic Systems/` |
| `Lecture4A_Transducers_Problems` | 4.1–4.4 (bass-reflex box, piston + box, voice coil, coil on piston) | `Lecture 4A - Transducers/` |
| `Problems4_DynamicMicrophone` | Problems 4 (lecture 4B): design, sensitivity, two-cavity and vent extensions | `Problems 4 - Dynamic Microphone/` |
| `Problems5_CondenserMicrophone` | Problems 5: f0, Q, sensitivity, circuit with and without T(s), optimisation | `Problems 5-6 - Condenser Microphone/` |
| `Problems6_Metrology_Calibration` | Problems 6: GUM uncertainty, LTspice ±10 % runs, pistonphone and calibrator | `Problems 5-6 - Condenser Microphone/` |
| `Lecture7_Loudspeakers_Problems7` | Problems 7: T-S parameters, 315 SWR, efficiency, excursion, lossy L_E | `Problems 7 - Loudspeaker/` |

Each LTspice folder has a Python generator (`pN.py`) that writes the `.asc`
files; `--verify` runs LTspice headless and checks it against the hand
formulas, `--preview` draws the schematics. They reuse the Lab A builder from
the labs repo, so `Labs/` must be cloned.

## Where results differ from the official solutions (explained in the scripts)

- **Problems 6, M at 250 Hz:** 9.83 mV/Pa here, 9.6 officially. The official
  schematic types the electrical gain as 1.1m instead of E·Ce0/x0 = 1.126m;
  9.83 × 1.1/1.126 = 9.60. The ±10 % C_MD numbers scale the same way.
- **Problems 5 front air mass:** the official unflanged-tube value
  0.6133ρ/(πr) is used (f0 = 10 624 Hz, Q = 2.355). The vault's older worked
  note used the baffled value (10.57 kHz, 2.37).
- **Lecture 4A 4.1:** the peak |Z_A| is 1.09e6 here, 995e3 officially. The peak is
  very sharp, so the official cursor reading depends on the sweep density.
  Same for the 4.4a dip depth (−60.7 dB vs −40.5 dB). The frequencies agree.
- **Problems 4 2c/2d:** built on the 1b/1c design as in the official solution
  (not the sheet's 2a values). The vent opens to the outside pressure as in the
  official schematic; the older KiCad version vents to ground.

## Regenerating

After editing a source (R2026a):

```matlab
matlab.internal.liveeditor.openAndSave('<Name>.m', '<Name>.mlx');
export('<Name>.mlx', '<Name>.html', Run=true, CatchError=true, OpenExportedFile=false);
```

`CatchError=true` is needed on this install: headless `export` with
`CatchError=false` reports "an error occurred while running" even for a
one-line script, although nothing fails (the HTML has no error blocks).
