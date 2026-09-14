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

# Large files (PDFs, slides, videos) arrive over Syncthing -- install it, then
# add this machine from the always-on node's UI at http://192.168.50.219:8384
# and share the "dtu" folder with it. Nothing to download by hand.
sudo pacman -S syncthing && systemctl --user enable --now syncthing

# If already cloned, initialize submodules
git submodule update --init --recursive
```

Open the `Obsidian/` folder as a vault in [Obsidian](https://obsidian.md/).

> **Note:** Large files (PDFs, slides, videos) are kept out of git to keep the repo lightweight. Syncthing replicates them between the two PCs and an always-on node on the home server (~1 750 files, ~3.6 GB); Google Drive is now only a nightly offsite backup written by that node. See the Syncthing section in `CLAUDE.md`.

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
│   └── MOC files
├── SPICEPilot/                          # Git submodule (SPICE simulation framework)
│   ├── examples/                        # Working circuit examples
│   ├── results/                         # Simulation outputs
│   ├── setup.bat                        # Automated setup script
│   └── SETUP_INSTRUCTIONS.md            # Setup guide
├── .gitignore                           # Excludes PDFs, slides (carried by Syncthing)
└── .stignore                            # What Syncthing carries: git owns text, Syncthing owns binaries
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
| Version Control | Git (text) + Syncthing (large files) |

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

### Large files

There are no sync scripts any more. Syncthing replicates every gitignored
binary between the two PCs, the `learn-sync` container and the always-on node
at `192.168.50.219`; what it carries is set by `.stignore` in the repo root.

```bash
# Is everything in sync?
curl -s -H "X-API-Key: $(grep -oP '(?<=<apikey>)[^<]+' \
  ~/.local/state/syncthing/config.xml)" \
  http://127.0.0.1:8384/rest/db/status?folder=dtu
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
