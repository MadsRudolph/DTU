<p align="center">
  <img src="Obsidian/Resources/banner_dtu.png" alt="DTU — Signal Integrity for My Brain" style="max-width:900px; width:100%; height:auto;">
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/MadsRudolph/DTU/output/github-snake-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/MadsRudolph/DTU/output/github-snake.svg" />
    <img alt="Contribution snake" src="https://raw.githubusercontent.com/MadsRudolph/DTU/output/github-snake.svg" width="900" />
  </picture>
</p>

<h1 align="center">DTU — Signal Integrity for My Brain</h1>

<p align="center">
  Notes, cheat sheets, simulations, and tools to survive engineering exams.<br>
  Organized so you don't waste time re-deriving stuff. ⚡
</p>

---

## 📚 What's Inside

| Semester | Focus Areas |
|----------|-------------|
| **1. Semester** | Intro programming, basic circuits |
| **2. Semester** | Math, modeling, LabVIEW, digital foundations |
| **3. Semester** | DSP, Electromagnetics, Analog IC |

Everything lives in an **Obsidian vault** with consistent structure per course:
- Lecture notes, slides, formulas
- Exercises with solutions
- MOC (Map of Content) files for navigation

---

## 🚀 Quick Start

```bash
# Clone
git clone git@github.com:MadsRudolph/DTU.git
cd DTU

# Pull large files (slides, PDFs)
git lfs install
git lfs pull
```

Open the `Obsidian/` folder as a vault in [Obsidian](https://obsidian.md/).

---

## 🗂️ Repository Structure

```
DTU/
├── 1. Semester/
├── 2. Semester/
├── 3. semester/
├── Obsidian/
│   ├── Courses/<Course>/
│   ├── Exercises/
│   ├── Lecture Notes/
│   ├── Formulas/
│   └── MOC files
└── scripts/
```

---

## 🛠️ Tools Used

| Area | Tools |
|------|-------|
| Notes | Obsidian (Markdown) |
| DSP / Math | MATLAB, Maple |
| Circuits | LTspice |
| MCU | PlatformIO, VS Code |
| Version Control | Git + Git LFS |

---

## 📜 Scripts

Utilities for vault maintenance:

| Script | Purpose |
|--------|---------|
| `check_wikilinks.py` | Find broken `[[wikilinks]]` |
| `check_wikilinks_courses.py` | Per-course link checks |
| `wire_courses.py` | Directory structure consistency |
| `wire_em_vault.py` | EM vault index maintenance |

```bash
# Run from repo root
python scripts/check_wikilinks.py
```

---

## 🌿 Branching

| Branch | Purpose |
|--------|---------|
| `main` | Stable, safe to rely on |
| `haul` | Large reorganizations |
| `feat/...` | New features |
| `fix/...` | Bug fixes |
| `docs/...` | Documentation |

---

## ⚠️ Academic Integrity

This is **personal study material** — use it responsibly.

✅ **OK:** Learning from it, using as inspiration, building your own vault

❌ **Not OK:** Submitting as your own work, copying into graded assignments

You're responsible for following your university's rules on academic honesty.

---

## 🤝 Contributing

1. Fork → Branch → PR (keep PRs small)
2. Large changes: open an issue first or use `haul` branch
3. Run `python scripts/check_wikilinks.py` before submitting

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📄 License

See [LICENSE.md](License.md)
