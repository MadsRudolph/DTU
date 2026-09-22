# Week 4 worked learning document

Open **Week4_Impedance_Intensity_Power.mlx** in MATLAB for the formatted walkthrough. It explains each question before showing a short calculation, and covers Problems 1–5, Exam A and all three multiple-choice questions. Run from the top once; then use Run Section. No extra toolboxes are required.

- `Week4_Impedance_Intensity_Power.html`: self-contained readable export with calculated answers, equations and two plots.
- `Week4_Impedance_Intensity_Power.m`: editable text source, also runnable as a sectioned MATLAB document.
- `../Week4/check_week4.py`: independent numerical checks using standard Python.

The source was executed in MATLAB R2026a. Main numerical results were checked against independent Python calculations and the problem sheet's printed answers. The Live Script is editable; use Run to populate its outputs. The HTML already contains the computed outputs.

PDF slides and the binary `.mlx` travel via Syncthing. The `.m`, this README and the self-contained HTML travel via git.

To regenerate the Live Script after editing the source (R2026a):

```matlab
matlab.internal.liveeditor.openAndSave('Week4_Impedance_Intensity_Power.m', ...
    'Week4_Impedance_Intensity_Power.mlx');
export('Week4_Impedance_Intensity_Power.mlx', ...
    'Week4_Impedance_Intensity_Power.html', ...
    Run=true, CatchError=false, OpenExportedFile=false);
```

The conversion helper is an internal MATLAB API, verified in this installation; it may change in later versions. MATLAB's editor Save As can also convert the `.m` source to a Live Script.
