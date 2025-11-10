<!-- Improved and structured README for easier scanning and usage -->

<p align="center">
  <img src="Obsidian/Resources/banner_dtu.png" alt="DTU — Signal Integrity for My Brain" style="max-width:900px; width:100%; height:auto;">
</p>

# DTU — Signal Integrity for My Brain

A personal, organized vault with course notes, exercises, simulations and small tools used during the degree.

This repository documents and stores notes, assignment solutions, simulation files and a few helper scripts so you don't have to re-derive the same thing during exam season.

---

## Table of contents

- [Repository layout](#repository-layout)
- [Toolchain overview](#toolchain-overview)
- [Branching model](#branching-model)
- [SSH & clone (quickstart)](#ssh--clone-quickstart)
- [Included scripts](#included-scripts)
- [Notes & contact](#notes--contact)

---

## Repository layout

Top-level (high level):

```
DTU/
├─ 1. Semester/            # Intro programming & basic circuits
├─ 2. Semester/            # Math, modeling, LabVIEW, digital foundations
├─ 3. semester/            # DSP, Electromagnetics, Analog IC coursework
├─ Obsidian/               # Notes, course vault (Markdown + images)
└─ scripts/                # Small utilities for vault maintenance
```

Inside `Obsidian/` the structure is consistent per course:

- `Courses/<Course>/`
- `Exercises/` (work, solutions, lab files)
- `Lecture Notes/`, `Slides/`, `Formulas/`, `Images/`
- `MOC – Course overview mapping files`

Yes — it took a while to organize, but it saves time during revision.

---

## Toolchain overview

| Area                     | Tools / files                      | Notes                                    |
|-------------------------:|:----------------------------------:|:----------------------------------------|
| Notes / knowledge base   | Markdown (Obsidian vault)          | Human-readable, portable                 |
| DSP / Math               | MATLAB (`.mlx`), Maple             | Math notebooks and scripts               |
| Analog / Circuits        | LTspice (`.asc`, `.raw`)           | Per-lesson groups                         |
| Microcontrollers         | PlatformIO, VS Code                 | MCU projects and example sketches         |
| Version control          | Git + Git LFS                       | Large binaries (slides, PDFs) via LFS     |

---

## Branching model

- `main` — stable, reviewable state (what I expect to keep pristine).
- `haul` — bigger reorgs and folder moves happen here (temporary construction zone).
- feature branches — short-lived, e.g. `feat/dsp-week09-filter-derivations`.

If you plan to move or rename many files, create a branch off `haul` and test changes before merging to `main`.

---

## SSH & clone (quickstart)

Preferred clone method is SSH. Example commands (PowerShell / Windows):

```powershell
# Generate an ED25519 key (one-liner)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Ensure the ssh-agent is running and add your key
Start-Service ssh-agent
ssh-add $env:USERPROFILE\.ssh\id_ed25519

# Verify the key was added (optional)
ssh-add -l

# Test connection
ssh -T git@github.com

# Clone the repo (replace <username>)
git clone git@github.com:<username>/DTU.git
cd DTU
git lfs install
git lfs pull

# Create a feature branch
git switch -c feat/<task>
```

Linux / macOS variants use `eval "$(ssh-agent -s)"` and `ssh-add ~/.ssh/id_ed25519`.

If you prefer HTTPS, the repo still works with HTTPS clones — just use your normal GitHub flow.

---

## Included scripts

Small utilities that help keep the vault consistent and catch broken links.

| Script                                | Purpose                                            |
|--------------------------------------:|:--------------------------------------------------|
| `scripts/check_wikilinks.py`          | Find broken `[[wikilinks]]` in the Obsidian vault  |
| `scripts/check_wikilinks_courses.py`  | Scoped link checks per course                      |
| `scripts/wire_courses.py`             | Ensure course directory structure consistency      |
| `scripts/wire_em_vault.py`            | Maintain Electromagnetics vault index + refs       |

Run these from the repo root with your Python environment active.

---

## Notes & contact

This repo's primary goal is to keep the mental signal-to-noise ratio acceptable: well-organized notes reduce repeated re-derivations during study.

If you want changes to the README layout or extra badges/CI hooks, tell me which items you'd like emphasized and I can add them.

End of transmission.


