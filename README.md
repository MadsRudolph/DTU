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
| **3. Semester** | DSP, Electromagnetics, Analog IC (with SPICEPilot integration) |
| **4. Semester** | Digital Systems (VHDL), Control Design, IoT, Power Electronics, Analog IC 2 |

Everything lives in an **Obsidian vault** with consistent structure per course:
- Lecture notes, slides, formulas
- Exercises with solutions
- MOC (Map of Content) files for navigation

---

## 🚀 Quick Start

```bash
# Clone with submodules
git clone --recurse-submodules git@github.com:MadsRudolph/DTU.git
cd DTU

# Enable git hooks (auto-downloads new Drive files on pull)
git config core.hooksPath .githooks

# Download large files (PDFs, slides) from Google Drive
pip install -r Obsidian/scripts/drive-sync/requirements.txt
PYTHONUTF8=1 python Obsidian/scripts/drive-sync/download.py

# If already cloned, initialize submodules
git submodule update --init --recursive
```

Open the `Obsidian/` folder as a vault in [Obsidian](https://obsidian.md/).

> **Note:** Large files (PDFs, slides, videos) are stored in Google Drive to keep the repo lightweight. The download script fetches ~335 files (~1GB) automatically.

### Setting up SPICEPilot (for SPICE simulations)

```bash
cd SPICEPilot
setup.bat              # Automated setup (Windows)
# OR follow SETUP_INSTRUCTIONS.md for manual setup
```

See [SPICEPilot README](SPICEPilot/README.md) for details.

---

## 🗂️ Repository Structure

```
DTU/
├── 1. Semester/                         # Archived coursework
├── 2. Semester/
├── 3. semester/
├── 4. Semester/                         # Current semester project files
│   ├── Digital Systems Design/          # Vivado, VHDL
│   ├── Linear Control Design/           # Matlab, Simulink
│   ├── Internet of Things/              # Arduino
│   ├── Power Electronics/               # Matlab, LTspice
│   └── Integrated Analog Electronics 2/ # LTspice, Kicad, Matlab
├── Obsidian/                            # Notes vault
│   ├── Courses/                         # Course notes, slides, literature
│   │   ├── 34315 Internet of Things/
│   │   ├── 34620 Basic Power Electronics/
│   │   ├── 34655 Integrated Analog Electronics 2/
│   │   ├── 34722 Linear Control Design 1/
│   │   └── 62711 Digital Systems Design/
│   ├── Archive/                         # Past semester notes
│   ├── scripts/
│   │   └── drive-sync/                  # Google Drive sync for large files
│   └── MOC files
├── SPICEPilot/                          # Git submodule (SPICE simulation framework)
│   ├── examples/                        # Working circuit examples
│   ├── results/                         # Simulation outputs
│   ├── setup.bat                        # Automated setup script
│   └── SETUP_INSTRUCTIONS.md            # Setup guide
└── .gitignore                           # Excludes PDFs, slides (stored in Drive)
```

---

## 🛠️ Tools Used

| Area | Tools |
|------|-------|
| Notes | Obsidian (Markdown) |
| DSP / Math | MATLAB, Maple, Simulink |
| Analog Circuits | LTspice, KiCad 9.0 |
| Digital Design | Xilinx Vivado, VHDL |
| SPICE Simulation | SPICEPilot, PySpice, ngspice |
| MCU / IoT | Arduino IDE, PlatformIO, VS Code |
| Version Control | Git + Google Drive (large files) |

---

## ⚡ SPICEPilot Integration

[SPICEPilot](https://github.com/MadsRudolph/SPICEPilot) is an AI-powered SPICE simulation framework, integrated as a git submodule for analog circuit design and simulation.

### Features

- **PySpice Integration**: Python-based SPICE netlists with programmatic circuit generation
- **ngspice Backend**: Industry-standard SPICE simulator
- **Working Examples**:
  - Current mirror bias circuit (99.7% theoretical accuracy)
  - Two-stage CMOS operational amplifier
- **Automated Setup**: One-click installation script for all dependencies
- **Complete Documentation**: 11+ guides in Obsidian vault

### Quick Test

```bash
cd SPICEPilot/examples/1_current_mirror
python current_mirror_bias.py        # PySpice simulation
# OR
ngspice current_mirror_bias.cir      # Direct ngspice
```

### Documentation

Comprehensive guides in `Obsidian/Courses/Integrated Analog Electronics/LTspice & Kicad/`:
- Setup guide
- Circuit design examples
- Simulation workflows
- KiCad integration methods
- Troubleshooting

---

## 📜 Scripts

### Google Drive Sync (large files)

| Script | Purpose |
|--------|---------|
| `download.py` | Download all large files from Google Drive |
| `upload.py --scan` | Find new large files not yet in Drive |
| `upload.py --add` | Add a file to the manifest after uploading |

```bash
# Download missing files
PYTHONUTF8=1 python Obsidian/scripts/drive-sync/download.py

# Check for new files to upload
python Obsidian/scripts/drive-sync/upload.py --scan
```

### Vault Maintenance

| Script | Purpose |
|--------|---------|
| `check_wikilinks.py` | Find broken `[[wikilinks]]` |
| `check_wikilinks_courses.py` | Per-course link checks |
| `wire_courses.py` | Directory structure consistency |

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
