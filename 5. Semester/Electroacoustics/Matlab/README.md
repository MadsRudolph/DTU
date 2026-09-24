# 34870 MATLAB worked problem sets

## Lecture 7 — Problems 7 (moving-coil loudspeakers)

Open **Lecture7_Loudspeakers_Problems7.mlx** in MATLAB and press Run. Each step
states the formula, then one MATLAB line that is the same formula typed in,
then the result, with the sheet's answer in the text next to it. Covers
Problems 1–4 (Problem 4's LTspice model is in `../LTspice/Problems 7 - Loudspeaker/`;
here the same circuit is solved directly to get the plots).

- `Lecture7_Loudspeakers_Problems7.html` — exported with outputs and plots, readable without MATLAB.
- `Lecture7_Loudspeakers_Problems7.m` — the editable source.

To regenerate the Live Script after editing the source (R2026a):

```matlab
matlab.internal.liveeditor.openAndSave('Lecture7_Loudspeakers_Problems7.m', ...
    'Lecture7_Loudspeakers_Problems7.mlx');
export('Lecture7_Loudspeakers_Problems7.mlx', 'Lecture7_Loudspeakers_Problems7.html', ...
    Run=true, CatchError=true, OpenExportedFile=false);
```

`CatchError=true` is needed on this install: headless `export` with
`CatchError=false` reports "an error occurred while running" even for a
one-line script, although nothing fails (the HTML has no error blocks).
