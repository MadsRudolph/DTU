---
name: notebooklm
description: Use when working on DTU coursework or technical questions in the user's course domains — Digital Signal Processing (DSP, FIR/IIR filter design, multirate, under-sampling), Linear Control Design (Laplace, transfer functions, Bode, Nyquist, PI/LEAD), Digital Systems Design (VHDL, Vivado, Xilinx FPGA, block RAM), CMOS analog IC (op-amps, DACs, noise, Cadence, layout), Internet of Things (Arduino, microcontroller, embedded C, wireless) — DSP reexam prep, when the user mentions a DTU course code (34315, 34620, 34655, 34722, 62711, 62743), or asks to "check my notes", "verify against the lecture", "look this up in my course material".
---

# DTU NotebookLM Consultation

The user is a DTU student (Mads, semester 4/7) with 5 course-specific NotebookLM notebooks pre-loaded with slides, lecture material, exercises, and past exams. Use these to ground domain-specific answers in the user's actual coursework — not generic web knowledge.

## Notebook map

| Alias | Course | Notebook contains |
|-------|--------|-------------------|
| `dsp`  | 62743 Digital Signal Processing — **REEXAM PREP** | All slides, past exams E19-F25 with student solutions, weekly solutions, Champagne textbook chapter, MATLAB refs (100 sources) |
| `lcd1` | 34722 Linear Control Design 1 | Lecture slides 1-12 (Laplace, Bode, Nyquist, PI/LEAD, stability, sensitivity), MATLAB exercises (40 sources total) |
| `dsd`  | 62711 Digital Systems Design | Slides, full Xilinx Vivado/UG documentation, VHDL guides, Mano textbook, project specs (42 sources) |
| `iae2` | 34655 Integrated Analog Electronics 2 | Slides, CMOS analog IC textbook (Carusone/Johns/Martin), LTSpice guide, problems/solutions for op-amps/DACs/noise/layout (26 sources) |
| `iot`  | 34315 Internet of Things | Slides, Arduino beginner book, lecture plan, exercise specs (12 sources) |

## How to query

```
C:\Users\Mads2\.claude\skills\notebooklm\scripts\nlm.bat ask "your question" --notebook-id <alias>
```

Returns a grounded answer with citations to source documents. **Quote those citations** in your reply so the user can find the exact slide/page.

Example:

```
nlm.bat ask "what's the relationship between sampling rate and aliasing in the FIR filter design lectures?" --notebook-id dsp
```

## When to consult

**Proactively consult (silent, then cite)** when:
- Claude is uncertain about a domain-specific formula, definition, or notation in any of the 5 course areas above
- The user asks a technical question and a course notebook clearly covers the topic
- DSP reexam prep — assume all DSP technical questions should be grounded in the notebook by default

**Offer first** when:
- The user is doing a homework / assignment and might want to work it out themselves first ("Want me to check the lecture slides for the canonical approach?")
- The answer could go multiple ways and the user's specific course conventions matter

**Don't consult** when:
- The question is generic programming, devops, or anything outside DTU coursework (the user's budget dashboard, snus tracker, hotel work, etc.)
- Computational tasks — NotebookLM is text-only; it won't run MATLAB, compute integrals, or verify numeric answers
- The user has explicitly said "don't use my notes for this"

## Course-to-alias hints

Use these keyword associations to pick the right notebook:
- *Filter, FFT, FIR, IIR, multirate, decimation, interpolation, aliasing, sampling, DSP* → `dsp`
- *Transfer function, Laplace, Bode, Nyquist, root locus, stability margin, PI, LEAD, control loop* → `lcd1`
- *VHDL, Vivado, Xilinx, FPGA, flip-flop, block RAM, synthesis, testbench, ATmega* → `dsd`
- *Op-amp, CMOS, MOSFET, Cadence, transistor, DAC, ADC, analog IC, layout* → `iae2`
- *Arduino, ESP32, sensor, wireless protocol, embedded C, microcontroller pin* → `iot`

If multiple notebooks could apply, ask the user which one to prioritize, or query the most likely match first.

## Citing back to the user

When you use a NotebookLM answer in your reply, format citations so the user can find the source:

```
According to your DSP slides on Digital Filter Design FIR part 1 (cited by NotebookLM):
> [quoted finding]
```

Don't paraphrase as if it were your own knowledge — the value is grounding in *their* materials.

## When `ask` fails

Symptoms that look like auth: `Authentication expired`, `RPC GET_NOTEBOOK failed`, `status code 5 (Not found)`, `account-routing mismatch`, or any `ClientError` from `notebooklm.exceptions`.

**Before assuming it's auth**, run the cheap diagnostic:

```
nlm.bat auth-status
```

- If it prints `Auth looks fresh` → auth is fine; the failure is something else (most likely a wrong notebook ID — verify with `nlm.bat library-list` to see the alias map, or `nlm.bat list` for raw UUIDs).
- If it prints `NOT AUTHENTICATED` or warns about age >168h → tell the user:
  > "Your NotebookLM cookies have expired. Run `nlm.bat login` in PowerShell — opens a browser for ~30 seconds of Google sign-in."

Auto-refresh runs every 3 days via Windows scheduled task `NotebookLM Cookie Refresh`; manual re-login is only needed if the PC was off through several refresh windows.

## Full reference

See `reference.md` next to this file for the upstream skill's full CLI (notebook management, source uploads, audio/report generation, slide-deck prompt templates).
