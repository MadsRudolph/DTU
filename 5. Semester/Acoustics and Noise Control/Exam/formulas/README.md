# Acoustics formulas (34840)

One offline page per topic. Each formula is a live row: fill in what you know and every
quantity that follows is worked out (in blue), with the substituted working underneath.
Any quantity can be the unknown; values are shared between the formulas on a page, so
results chain. Fields take arithmetic (`2*(5*8+5*3)`, `4*pi`, `10^(3/10)`, `2k`).

- **Open:** double-click `acoustics-formulas.html`. No internet, no install. Inputs are kept in the browser between visits.
- **Keys:** `/` search, Enter opens the first hit, Esc clears a field.
- **MATLAB:** every formula shows its MATLAB line (element-wise, so vectors work); click it to copy.
  The line is always solved for the unknown: when the page works something out from a row, the line switches
  to that variable (`R = sqrt(1 - alpha)`), and "MATLAB for" lets you pick any variable by hand.
  The rearranged forms come from MATLAB's symbolic solve (289 closed forms, 9 via `fzero`).
  **Copy as MATLAB** (top of each page) copies the constants, your given values and every formula used, in order,
  ready to paste into a live script. The sidebar copies the constants line alone.
- **Copy working:** copies the given values and each worked step as plain text for the hand-in.
- **Topics:** levels, plane waves and tubes, point sources, two sources, room modes, reverberation,
  absorbers, bands and weighting, hearing, vibration isolation, sound insulation, loudspeakers.
  Extra tools: combine/subtract levels and L_eq, band levels to L_A, list of room modes, composite wall.
- **Constants:** c and ρ are editable at the bottom of the sidebar (exam default 343 m/s, 1.2 kg/m³).

Edit the formulas in `src/formulas.js` (residual form, one line each), then:

    node build.js    # writes acoustics-formulas.html (KaTeX inlined from ../app/vendor/katex)
    node test.js     # every formula solved for every variable, plus toolkit spot values
    # after adding or changing a formula, regenerate the rearranged MATLAB lines:
    node gen_inverses.js > gen_inverses_run.m && matlab -batch gen_inverses_run   # writes src/inverses.json
    node gen_post.js                                                              # writes src/inverses.js
    node matlab_check.js > check_matlab_lines.m && matlab -batch check_matlab_lines   # all 298 lines = the page
