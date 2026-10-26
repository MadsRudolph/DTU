#!/usr/bin/env python3
"""Run the five-layer wall (Lecture 10, slides 4-6) in ngspice and check all three rows
against the transfer-matrix closed form in ../../../LTspice/Lecture 10 - Mixed Models/p10.py."""
import sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
sys.path.insert(0, str(HERE.parents[2] / "LTspice" / "Lecture 10 - Mixed Models"))
from ngspice_ac import run_ac
import p10                                     # closed form: p10.chain(w, "lem" | "mix" | "tmm")

f, v = run_ac(HERE / "Problem_10_Wall_LEM_TMM.kicad_sch", ["v(/pout1)", "v(/pout2)", "v(/pout3)"])
ok = True
rows = (("1", "lem", "LEM (slide 5)", "-"), ("2", "mix", "LEM + TMM (slide 6 top)", "--"),
        ("3", "tmm", "full TMM (slide 6 bottom)", ":"))
for tag, model, _, _ in rows:
    ref = np.array([p10.chain(2 * np.pi * fi, model) for fi in f])
    worst = np.max(np.abs(20 * np.log10(np.abs(v[f"v(/pout{tag})"])) - 20 * np.log10(np.abs(ref))))
    good = worst < 0.05; ok &= good
    print(f"  {'OK ' if good else 'BAD'} row {tag} ({model}): worst deviation from the closed form {worst:.2e} dB over {len(f)} points")
print("ALL OK" if ok else "MISMATCH")

fig, ax = plt.subplots(figsize=(8, 4.2))
for tag, _, lab, ls in rows:
    ax.semilogx(f, 20 * np.log10(np.abs(v[f"v(/pout{tag})"])), ls=ls, lw=1.6, label=lab)
ax.set(xlabel="Frequency [Hz]", ylabel="Transmission p$_{out}$/p$_{in}$ [dB]", xlim=(20, 20000), ylim=(-200, 0),
       title="Five-layer wall in KiCad/ngspice (lecture 10, slides 5-6)")
ax.grid(True, which="both", alpha=0.3); ax.legend(fontsize=8, loc="lower left")
fig.tight_layout()
for outdir in (HERE, Path("/home/mads/DTU/Obsidian/Courses/34870 Electroacoustics/Images/Lecture10")):
    outdir.mkdir(parents=True, exist_ok=True)
    fig.savefig(outdir / "L10_wall_transmission_kicad.png", dpi=130)
print("saved")
sys.exit(0 if ok else 1)
