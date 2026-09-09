#!/usr/bin/env python3
"""Tiny helper: export a KiCad schematic to a SPICE netlist with kicad-cli,
run an AC analysis in ngspice (batch), and return the complex vectors.

    from ngspice_ac import run_ac
    f, v = run_ac(Path("X.kicad_sch"), ["v(/u)", "i(v1)"])
    # v["v(/u)"] is a complex numpy array over f
"""
import subprocess, tempfile, re
from pathlib import Path
import numpy as np

def export(sch: Path) -> Path:
    cir = sch.with_suffix(".cir")
    subprocess.run(["kicad-cli", "sch", "export", "netlist", "--format", "spice",
                    "-o", str(cir), str(sch)], check=True, capture_output=True, text=True)
    return cir

def run_ac(sch: Path, vectors, extra_lines=()):
    cir = export(sch)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        data = td / "out.txt"
        deck = td / "run.cir"
        local = td / "net.cir"          # copy: paths with spaces break .include
        local.write_text(cir.read_text())
        deck.write_text(
            f".include {local}\n" + "\n".join(extra_lines) + "\n"
            ".control\nrun\nset wr_singlescale\nset wr_vecnames\n"
            f"wrdata {data} {' '.join(vectors)}\nquit\n.endc\n.end\n")
        res = subprocess.run(["ngspice", "-b", str(deck)], capture_output=True, text=True)
        if not data.exists():
            raise RuntimeError("ngspice produced no data:\n" + res.stdout + res.stderr)
        rows = [ln.split() for ln in data.read_text().splitlines() if ln.strip()]
    header, body = rows[0], np.array([[float(x) for x in r] for r in rows[1:]])
    f = body[:, 0]
    out, col = {}, 1
    for name in vectors:
        out[name] = body[:, col] + 1j * body[:, col + 1]
        col += 2
    return f, out
