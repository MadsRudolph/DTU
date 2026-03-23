# DTU Obsidian Vault Restructure Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Unify all DTU study materials into the Obsidian vault, standardize resource organisation, add Formula Sheet and Concept note types, merge duplicate archives, and create cross-course concept notes.

**Architecture:** Five sequential proposals executed on a dedicated `vault-restructure` branch. Submodule moves use `git mv` + `.gitmodules` edits. Non-submodule file moves use `git mv`. New markdown files are created with Write tool. No files are deleted without confirmation.

**Tech Stack:** Git (submodules), Obsidian (Dataview, Templater), Markdown, VHDL, MATLAB files handled as opaque blobs.

---

## Submodule Reference (read-only, do NOT move unless instructed)

| Path | Remote | Action |
|------|--------|--------|
| `SPICEPilot` | github.com/MadsRudolph/SPICEPilot | **leave in place** |
| `spicepilot-kicad` | github.com/MadsRudolph/spicepilot-kicad | **leave in place** |
| `4. Semester/Digital Systems Design/team` | gigurd/Design-of-digital-systems-62711 | **move** to `Obsidian/Courses/62711 Digital Systems Design/Code/team` |
| `4. Semester/Internet of Things/Arduino/Ex13` | github.com/MadsRudolph/iot-ex13 | **move** to `Obsidian/Courses/34315 Internet of Things/Code/Ex13` |
| `Obsidian/Courses/34655 Integrated Analog Electronics 2/Report` | MadsRudolph/Design-af-opamp-analog-ic-2 | **leave in place** |
| `Obsidian/Courses/62711 Digital Systems Design/PWA Project/Report` | MadsRudolph/PWA | **leave in place** |
| `Obsidian/Courses/62711 Digital Systems Design/Report-PWB` | MadsRudolph/PWB | **leave in place** |

---

## Task 1: Create the branch

**Files:**
- No file changes, git only

**Step 1: Create and checkout vault-restructure branch from main**

```bash
cd /c/Users/Mads2/DTU
git checkout main
git pull
git checkout -b vault-restructure
```

Expected: `Switched to a new branch 'vault-restructure'`

**Step 2: Verify clean state**

```bash
git status
git submodule status
```

Expected: clean working tree, all submodules listed

**Step 3: Commit the docs/plans directory**

```bash
git add docs/plans/2026-03-23-vault-restructure.md
git commit -m "chore: add vault restructure implementation plan"
```

---

## Task 2: Fix corrupted UTF-8 folder names (Proposal 1, pre-step)

The following folders have double-encoded UTF-8 names that should be renamed before moving anything:

- `1. Semester/Elektroteknologi/Ã˜velser` → `1. Semester/Elektroteknologi/Øvelser`
- `1. Semester/MAM/eksamenssÃ¦t` → `1. Semester/MAM/eksamenssæt`

(Their correctly-named siblings already exist, so check for content overlap before renaming.)

**Step 1: Check for overlap**

```bash
ls "1. Semester/Elektroteknologi/Ã˜velser/" 2>/dev/null
ls "1. Semester/Elektroteknologi/Øvelser/" 2>/dev/null
ls "1. Semester/MAM/eksamenssÃ¦t/" 2>/dev/null
ls "1. Semester/MAM/eksamenssæt/" 2>/dev/null
```

**Step 2: If corrupted folders are empty, remove them with git rm -r**

```bash
git rm -r "1. Semester/Elektroteknologi/Ã˜velser" 2>/dev/null || true
git rm -r "1. Semester/MAM/eksamenssÃ¦t" 2>/dev/null || true
```

If they contain unique files, move them into the correctly-named sibling first:
```bash
git mv "1. Semester/Elektroteknologi/Ã˜velser/"* "1. Semester/Elektroteknologi/Øvelser/"
git rm -r "1. Semester/Elektroteknologi/Ã˜velser"
git mv "1. Semester/MAM/eksamenssÃ¦t/"* "1. Semester/MAM/eksamenssæt/"
git rm -r "1. Semester/MAM/eksamenssÃ¦t"
```

**Step 3: Commit**

```bash
git add -A
git commit -m "fix: remove corrupted UTF-8 duplicate folders in 1st semester"
```

---

## Task 3: Move 1st and 2nd semester into vault archive (Proposal 1)

**Files:**
- Move: `1. Semester/` → `Obsidian/Archive/1st Semester/`
- Move: `2. Semester/` → `Obsidian/Archive/2nd Semester/`
- Create: `Obsidian/Archive/1st Semester/` (implicit via git mv)

No submodules exist in these folders. Safe to `git mv` directly.

**Step 1: Move 1st semester**

```bash
cd /c/Users/Mads2/DTU
git mv "1. Semester" "Obsidian/Archive/1st Semester"
```

**Step 2: Move 2nd semester**

```bash
git mv "2. Semester" "Obsidian/Archive/2nd Semester"
```

**Step 3: Verify**

```bash
ls "Obsidian/Archive/"
```

Expected: `1st Semester  2nd Semester  3rd Semester`

**Step 4: Commit**

```bash
git commit -m "feat: move 1st and 2nd semester into Obsidian/Archive"
```

---

## Task 4: Merge 3rd semester external content into vault archive (Proposal 1)

The `3.semester/` folder has three subject folders. `Obsidian/Archive/3rd Semester/` already has `DSP`, `Electromagnetics`, `Integrated Analog Electronics`, and `EM`. The external folder has MATLAB, Python helpers, exam files, and lab code that the vault archive likely doesn't have.

**Step 1: Check what's in the external folder vs the archive**

```bash
ls "3.semester/DSP/"
ls "3.semester/Electromagnetics/"
ls "3.semester/Integrated Analog Electronics/"
ls "Obsidian/Archive/3rd Semester/DSP/"
ls "Obsidian/Archive/3rd Semester/Electromagnetics/"
ls "Obsidian/Archive/3rd Semester/Integrated Analog Electronics/"
```

**Step 2: Move non-overlapping content from each external subfolder into the archive**

For DSP (move subdirectories that don't conflict):
```bash
# Move each subfolder individually to avoid overwriting existing content
for dir in "3.semester/DSP/Assistant" "3.semester/DSP/EXAMS" "3.semester/DSP/Helpers" "3.semester/DSP/html" "3.semester/DSP/UGE1" "3.semester/DSP/UGE2" "3.semester/DSP/UGE3" "3.semester/DSP/UGE4" "3.semester/DSP/UGE7" "3.semester/DSP/UGE8" "3.semester/DSP/UGE10" "3.semester/DSP/UGE11" "3.semester/DSP/UGE12" "3.semester/DSP/UGE13"; do
  [ -d "$dir" ] && git mv "$dir" "Obsidian/Archive/3rd Semester/DSP/$(basename "$dir")"
done
```

For Electromagnetics:
```bash
for dir in "3.semester/Electromagnetics/Assistant" "3.semester/Electromagnetics/EXAM" "3.semester/Electromagnetics/GroupTutorials" "3.semester/Electromagnetics/Helpers" "3.semester/Electromagnetics/LAB"; do
  [ -d "$dir" ] && git mv "$dir" "Obsidian/Archive/3rd Semester/Electromagnetics/$(basename "$dir")"
done
```

For Integrated Analog Electronics:
```bash
ls "3.semester/Integrated Analog Electronics/"
# Then git mv each subfolder not already present in archive
```

**Step 3: Remove the now-empty 3.semester folder**

```bash
git rm -r "3.semester"
```

**Step 4: Commit**

```bash
git commit -m "feat: merge 3rd semester external content into Obsidian archive"
```

---

## Task 5: Move 4th semester code into course folders (Proposal 1)

Submodules that need moving:
- `4. Semester/Digital Systems Design/team` → `Obsidian/Courses/62711 Digital Systems Design/Code/team`
- `4. Semester/Internet of Things/Arduino/Ex13` → `Obsidian/Courses/34315 Internet of Things/Code/Ex13`

Non-submodule VHDL and Vivado code → `Obsidian/Courses/62711 Digital Systems Design/Code/`

**Step 1: Create target Code/ directories**

```bash
mkdir -p "Obsidian/Courses/62711 Digital Systems Design/Code"
mkdir -p "Obsidian/Courses/34315 Internet of Things/Code"
mkdir -p "Obsidian/Courses/34655 Integrated Analog Electronics 2/Code"
mkdir -p "Obsidian/Courses/34722 Linear Control Design 1/Code"
mkdir -p "Obsidian/Courses/34620 Basic Power Electronics/Code"
```

**Step 2: Move non-submodule VHDL/Vivado content**

```bash
git mv "4. Semester/Digital Systems Design/VHDL" "Obsidian/Courses/62711 Digital Systems Design/Code/VHDL"
git mv "4. Semester/Digital Systems Design/Vivado" "Obsidian/Courses/62711 Digital Systems Design/Code/Vivado"
git mv "4. Semester/Digital Systems Design/Tools" "Obsidian/Courses/62711 Digital Systems Design/Code/Tools"
git mv "4. Semester/Digital Systems Design/EXAM" "Obsidian/Courses/62711 Digital Systems Design/Code/EXAM"
```

**Step 3: Move the team submodule**

Submodule moves require: (a) git mv the directory, (b) edit .gitmodules path, (c) git add -A.

```bash
git mv "4. Semester/Digital Systems Design/team" "Obsidian/Courses/62711 Digital Systems Design/Code/team"
```

Then edit `.gitmodules`: change
```
path = 4. Semester/Digital Systems Design/team
```
to:
```
path = Obsidian/Courses/62711 Digital Systems Design/Code/team
```

Then:
```bash
git add .gitmodules
git submodule sync
```

**Step 4: Move IoT Arduino code and Ex13 submodule**

```bash
# Move non-submodule Arduino sketches first
for sketch in "4. Semester/Internet of Things/Arduino/Ex8" \
  "4. Semester/Internet of Things/Arduino/exercise1MorseCodeForLoop" \
  "4. Semester/Internet of Things/Arduino/exercise1MorseCodeFunctions" \
  "4. Semester/Internet of Things/Arduino/exercise1MorseCodeSimple"; do
  [ -d "$sketch" ] && git mv "$sketch" "Obsidian/Courses/34315 Internet of Things/Code/$(basename "$sketch")"
done

# Move Ex13 submodule
git mv "4. Semester/Internet of Things/Arduino/Ex13" "Obsidian/Courses/34315 Internet of Things/Code/Ex13"
```

Edit `.gitmodules`: change
```
path = 4. Semester/Internet of Things/Arduino/Ex13
```
to:
```
path = Obsidian/Courses/34315 Internet of Things/Code/Ex13
```

```bash
git add .gitmodules
git submodule sync
```

**Step 5: Move other 4th semester course code**

```bash
# IAE2 code
git mv "4. Semester/Integrated Analog Electronics 2/Kicad" "Obsidian/Courses/34655 Integrated Analog Electronics 2/Code/Kicad"
git mv "4. Semester/Integrated Analog Electronics 2/Spice" "Obsidian/Courses/34655 Integrated Analog Electronics 2/Code/Spice"
git mv "4. Semester/Integrated Analog Electronics 2/Matlab" "Obsidian/Courses/34655 Integrated Analog Electronics 2/Code/Matlab"
git mv "4. Semester/Integrated Analog Electronics 2/EXAM" "Obsidian/Courses/34655 Integrated Analog Electronics 2/Code/EXAM"

# Linear Control Design code
git mv "4. Semester/Linear Control Design" "Obsidian/Courses/34722 Linear Control Design 1/Code"

# Power Electronics code
git mv "4. Semester/Power Electronics/LTspice" "Obsidian/Courses/34620 Basic Power Electronics/Code/LTspice"
git mv "4. Semester/Power Electronics/Matlab" "Obsidian/Courses/34620 Basic Power Electronics/Code/Matlab"
git mv "4. Semester/Power Electronics/EXAM" "Obsidian/Courses/34620 Basic Power Electronics/Code/EXAM"
```

**Step 6: Move IoT exam content**

```bash
git mv "4. Semester/Internet of Things/EXAM" "Obsidian/Courses/34315 Internet of Things/Code/EXAM"
```

**Step 7: Remove now-empty 4. Semester/**

```bash
# Verify it's empty first
find "4. Semester" -type f 2>/dev/null
# If empty:
git rm -r "4. Semester"
```

**Step 8: Commit**

```bash
git add -A
git commit -m "feat: move 4th semester code into Obsidian course folders, update submodule paths"
```

---

## Task 6: Add Formula Sheet template (Proposal 2)

**Files:**
- Create: `Obsidian/Templates/Formula Sheet.md`
- Modify: `Obsidian/Templates/Course Home.md` (add Dataview block)

**Step 1: Create Formula Sheet template**

The template must match the style of existing templates (Templater syntax, same frontmatter pattern).

Create `Obsidian/Templates/Formula Sheet.md`:

```markdown
---
course: "<% tp.system.prompt("Course code (e.g. 34315)") %>"
course-name: "<% tp.system.prompt("Course name") %>"
type: formula
topic: "<% tp.system.prompt("Topic (e.g. Bode Plots, Z-Transform)") %>"
date: <% tp.date.now("YYYY-MM-DD") %>
tags:
  - <% tp.system.prompt("Short tag (e.g. IoT, PE, LCD)") %>
  - formula
---
# <% tp.file.title %>

> [!info] Formula Sheet
> **Course:** <% tp.frontmatter.course-name %>
> **Topic:** <% tp.frontmatter.topic %>
> **Date:** <% tp.date.now("YYYY-MM-DD") %>

---

## Key Formulas

| Symbol | Formula | Description |
|--------|---------|-------------|
|  |  |  |

---

## Derivations & Notes



---

## Conditions & Constraints

> [!warning] Valid when
> -

---

## Related

- [[]]
```

**Step 2: Add Dataview query to Course Home template**

In `Obsidian/Templates/Course Home.md`, after the `## Exercises & Quizzes` block, add a new section:

```markdown
---

## Formula Sheets

```dataview
TABLE topic AS "Topic", date AS "Date"
FROM "<% tp.file.folder(true) %>/Formulas"
WHERE type = "formula"
SORT date ASC
```
```

**Step 3: Commit**

```bash
git add "Obsidian/Templates/Formula Sheet.md" "Obsidian/Templates/Course Home.md"
git commit -m "feat: add Formula Sheet template and surface formulas on Course Home"
```

---

## Task 7: Standardize attachment subfolders (Proposal 3)

Each course folder under `Obsidian/Courses/` needs:
```
Attachments/
├── Slides/
├── Literature/
├── Guides/
└── Images/
```

Courses: `34315 Internet of Things`, `34620 Basic Power Electronics`, `34655 Integrated Analog Electronics 2`, `34722 Linear Control Design 1`, `62711 Digital Systems Design`, `62743 Digital Signal Processing (Reexam)`, `Electromagnetics`

> **Note:** Most courses already have `Slides/`, `Literature/`, `Images/` at the course root. The plan is to create an `Attachments/` wrapper containing subfolders, then move content into it. However, since Obsidian wikilinks break when files move, check for wikilinks before moving any file.

**Step 1: Scan for wikilinks to PDFs/images in course folders**

```bash
grep -r "\[\[.*\.pdf\|!\[\[.*\]\]" "/c/Users/Mads2/DTU/Obsidian/Courses" --include="*.md" | head -30
```

**Step 2: For each course, create Attachments/ subfolders and move content**

Run for each course (substitute `COURSE` with each course folder name):

```bash
COURSE="34315 Internet of Things"
BASE="Obsidian/Courses/$COURSE"
mkdir -p "$BASE/Attachments/Slides" "$BASE/Attachments/Literature" "$BASE/Attachments/Guides" "$BASE/Attachments/Images"

# Move existing Slides/ contents
[ -d "$BASE/Slides" ] && git mv "$BASE/Slides"/* "$BASE/Attachments/Slides/" 2>/dev/null; git rm -r "$BASE/Slides" 2>/dev/null || true

# Move existing Literature/ contents
[ -d "$BASE/Literature" ] && git mv "$BASE/Literature"/* "$BASE/Attachments/Literature/" 2>/dev/null; git rm -r "$BASE/Literature" 2>/dev/null || true

# Move existing Images/ contents
[ -d "$BASE/Images" ] && git mv "$BASE/Images"/* "$BASE/Attachments/Images/" 2>/dev/null; git rm -r "$BASE/Images" 2>/dev/null || true
```

Repeat for all 7 courses.

**Step 3: Scan all .md files for broken wikilinks and fix them**

```bash
grep -r "\[\[Slides/\|!\[\[Slides/" "Obsidian/Courses" --include="*.md" -l
grep -r "\[\[Literature/\|!\[\[Literature/" "Obsidian/Courses" --include="*.md" -l
grep -r "\[\[Images/\|!\[\[Images/" "Obsidian/Courses" --include="*.md" -l
```

For each file with a match, update the path from e.g. `[[Slides/foo.pdf]]` to `[[Attachments/Slides/foo.pdf]]`. Use Edit tool for each file.

**Step 4: Commit**

```bash
git add -A
git commit -m "feat: reorganize course attachments into Attachments/ subfolder structure"
```

---

## Task 8: Merge EM archive and fix DSP reexam paths (Proposal 4)

**Part A: Merge EM/ into Electromagnetics/**

`Obsidian/Archive/3rd Semester/EM/` contains Python tool scripts (B_field_inf_wire, Coulomb, Fresnel, etc.) and a README. These should go into `Obsidian/Archive/3rd Semester/Electromagnetics/Tools/`.

**Step 1: Create Tools/ subfolder and move EM tool scripts**

```bash
mkdir -p "Obsidian/Archive/3rd Semester/Electromagnetics/Tools"
for item in B_field_inf_wire Coulomb Fresnel Medium PlaneCheck Polarization Poynting Smithchart StubMatch TLine; do
  [ -e "Obsidian/Archive/3rd Semester/EM/$item" ] && \
    git mv "Obsidian/Archive/3rd Semester/EM/$item" "Obsidian/Archive/3rd Semester/Electromagnetics/Tools/$item"
done
git mv "Obsidian/Archive/3rd Semester/EM/EM_Toolbox_README.md" "Obsidian/Archive/3rd Semester/Electromagnetics/Tools/EM_Toolbox_README.md"
git rm -r "Obsidian/Archive/3rd Semester/EM"
```

**Step 2: Commit**

```bash
git commit -m "feat: merge EM toolbox archive into Electromagnetics/Tools"
```

**Part B: Fix DSP reexam hardcoded paths**

The file `Obsidian/Courses/62743 Digital Signal Processing (Reexam)/62743 Digital Signal Processing (Reexam).md` has a Key Locations callout with a hardcoded Windows path:
```
**MATLAB exercises & exams:** `C:\Users\Mads2\DTU\3.semester\DSP\`
```

Since `3.semester/DSP/` content was moved to `Obsidian/Archive/3rd Semester/DSP/` in Task 4, replace the hardcoded path with an Obsidian wikilink.

**Step 3: Read the DSP reexam home page**

Read `Obsidian/Courses/62743 Digital Signal Processing (Reexam)/62743 Digital Signal Processing (Reexam).md`

**Step 4: Replace hardcoded path with wikilink**

Change:
```
> **MATLAB exercises & exams:** `C:\Users\Mads2\DTU\3.semester\DSP\`
```
to:
```
> **MATLAB exercises & exams:** [[Archive/3rd Semester/DSP/|DSP Archive Folder]]
```

**Step 5: Commit**

```bash
git commit -m "fix: replace hardcoded Windows path with Obsidian wikilink in DSP reexam page"
```

---

## Task 9: Create Concept note type and starter concepts (Proposal 5)

**Files:**
- Create: `Obsidian/Templates/Concept.md`
- Create: `Obsidian/Concepts/` (new folder)
- Create: 7 concept notes

**Step 1: Create the Concept template**

Create `Obsidian/Templates/Concept.md`:

```markdown
---
type: concept
aliases:
  - "<% tp.system.prompt("Aliases (comma-separated, or leave blank)") %>"
tags:
  - concept
  - <% tp.system.prompt("Domain tag (e.g. signals, circuits, control)") %>
courses:
  - "<% tp.system.prompt("Course code(s) where this appears") %>"
date: <% tp.date.now("YYYY-MM-DD") %>
---
# <% tp.file.title %>

> [!abstract] Definition
> _One-sentence definition here._

---

## Key Equations

| Equation | Meaning |
|----------|---------|
|  |  |

---

## Intuition



---

## Conditions & Caveats

> [!warning]
> -

---

## Appears In

```dataview
TABLE file.folder AS "Course", type AS "Type"
FROM "Obsidian/Courses"
WHERE contains(file.content, this.file.name)
SORT file.name ASC
```

---

## See Also

- [[]]
```

**Step 2: Create Concepts/ folder and 7 starter notes**

Create `Obsidian/Concepts/Transfer Function.md`:

```markdown
---
type: concept
aliases: ["H(s)", "system function"]
tags: [concept, control, signals]
courses: ["34722", "62743"]
date: 2026-03-23
---
# Transfer Function

> [!abstract] Definition
> The ratio of the Laplace transform of the output to the Laplace transform of the input, assuming zero initial conditions: $H(s) = Y(s)/X(s)$.

---

## Key Equations

| Equation | Meaning |
|----------|---------|
| $H(s) = \frac{Y(s)}{X(s)}$ | Definition (zero IC) |
| $H(s) = \frac{b_m s^m + \cdots + b_0}{a_n s^n + \cdots + a_0}$ | Rational polynomial form |
| $H(j\omega)$ | Frequency response (substitute $s = j\omega$) |

---

## Intuition

A transfer function encodes how every frequency component is scaled and phase-shifted as it passes through a linear time-invariant system. Poles determine transient behaviour; zeros shape the frequency response.

---

## Conditions & Caveats

> [!warning]
> - Valid only for LTI systems with zero initial conditions
> - The region of convergence (ROC) must include the $j\omega$ axis for BIBO stability

---

## Appears In

```dataview
TABLE file.folder AS "Course", type AS "Type"
FROM "Obsidian/Courses"
WHERE contains(file.content, "Transfer Function") OR contains(file.content, "transfer function")
SORT file.name ASC
```

---

## See Also

- [[Bode Plot]]
- [[Feedback Stability]]
```

Create `Obsidian/Concepts/Bode Plot.md`:

```markdown
---
type: concept
aliases: ["frequency response plot", "Bode diagram"]
tags: [concept, control, signals]
courses: ["34722"]
date: 2026-03-23
---
# Bode Plot

> [!abstract] Definition
> A pair of plots showing magnitude $|H(j\omega)|$ in dB and phase $\angle H(j\omega)$ in degrees versus log-frequency $\omega$, used to analyse the frequency response of an LTI system.

---

## Key Equations

| Equation | Meaning |
|----------|---------|
| $|H(j\omega)|_\text{dB} = 20\log_{10}|H(j\omega)|$ | Magnitude in dB |
| Slope: $\pm 20n$ dB/decade | $n$ poles/zeros at a corner frequency |
| Phase contribution of pole at $s=-a$: $-\arctan(\omega/a)$ | Phase from real pole |

---

## Intuition

Each real pole bends the magnitude slope down by 20 dB/decade and contributes −90° of phase. Each zero does the opposite. Asymptotic (straight-line) Bode approximations give quick stability insights.

---

## Conditions & Caveats

> [!warning]
> - Asymptotic approximation is exact only far from corner frequencies
> - Complex conjugate pole pairs produce a resonance peak — the asymptotic method underestimates it

---

## Appears In

```dataview
TABLE file.folder AS "Course", type AS "Type"
FROM "Obsidian/Courses"
WHERE contains(file.content, "Bode") OR contains(file.content, "bode")
SORT file.name ASC
```

---

## See Also

- [[Transfer Function]]
- [[Feedback Stability]]
```

Create `Obsidian/Concepts/Z-Transform.md`:

```markdown
---
type: concept
aliases: ["Z transform", "bilateral Z-transform"]
tags: [concept, signals, DSP]
courses: ["62743"]
date: 2026-03-23
---
# Z-Transform

> [!abstract] Definition
> The discrete-time counterpart of the Laplace transform: $X(z) = \sum_{n=-\infty}^{\infty} x[n] z^{-n}$, mapping a discrete sequence into the complex $z$-plane.

---

## Key Equations

| Equation | Meaning |
|----------|---------|
| $X(z) = \sum_{n=-\infty}^{\infty} x[n]z^{-n}$ | Definition |
| $z = e^{j\omega}$ | Unit circle = DTFT |
| $x[n-k] \leftrightarrow z^{-k}X(z)$ | Delay property |
| $\text{ROC}$: ring $r_1 < \|z\| < r_2$ | Region of convergence |

---

## Intuition

Think of $z^{-1}$ as a one-sample delay operator. The unit circle in the $z$-plane corresponds to the DTFT. Poles inside the unit circle → stable causal systems.

---

## Conditions & Caveats

> [!warning]
> - Always state the ROC — the Z-transform is not unique without it
> - A causal, stable system requires all poles strictly inside the unit circle

---

## Appears In

```dataview
TABLE file.folder AS "Course", type AS "Type"
FROM "Obsidian/Courses"
WHERE contains(file.content, "Z-Transform") OR contains(file.content, "z-transform") OR contains(file.content, "Z transform")
SORT file.name ASC
```

---

## See Also

- [[Fourier Transform]]
- [[Transfer Function]]
```

Create `Obsidian/Concepts/Fourier Transform.md`:

```markdown
---
type: concept
aliases: ["FT", "DTFT", "DFT", "FFT"]
tags: [concept, signals, DSP, math]
courses: ["62743"]
date: 2026-03-23
---
# Fourier Transform

> [!abstract] Definition
> A transform decomposing a signal into its constituent frequencies. The continuous-time Fourier transform is $X(j\omega) = \int_{-\infty}^{\infty} x(t)e^{-j\omega t}dt$; the DTFT is $X(e^{j\omega}) = \sum_{n} x[n]e^{-j\omega n}$.

---

## Key Equations

| Equation | Meaning |
|----------|---------|
| $X(j\omega) = \int_{-\infty}^{\infty} x(t)e^{-j\omega t}dt$ | CTFT |
| $X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n]e^{-j\omega n}$ | DTFT |
| $X[k] = \sum_{n=0}^{N-1} x[n]e^{-j2\pi kn/N}$ | DFT |
| Parseval: $\sum_n \|x[n]\|^2 = \frac{1}{2\pi}\int_{-\pi}^{\pi}\|X(e^{j\omega})\|^2 d\omega$ | Energy conservation |

---

## Intuition

Every finite-energy signal can be written as a weighted superposition of complex exponentials. The transform tells you how much of each frequency is present.

---

## Conditions & Caveats

> [!warning]
> - CTFT requires absolute integrability (or use distributions for power signals)
> - DTFT is periodic with period $2\pi$
> - DFT assumes periodicity — leakage occurs when the signal is not periodic in the window

---

## Appears In

```dataview
TABLE file.folder AS "Course", type AS "Type"
FROM "Obsidian/Courses"
WHERE contains(file.content, "Fourier") OR contains(file.content, "DTFT") OR contains(file.content, "DFT")
SORT file.name ASC
```

---

## See Also

- [[Z-Transform]]
- [[Transfer Function]]
```

Create `Obsidian/Concepts/MOSFET Small-Signal Model.md`:

```markdown
---
type: concept
aliases: ["small signal model", "MOSFET SSM", "hybrid-pi model"]
tags: [concept, analog, circuits]
courses: ["34655"]
date: 2026-03-23
---
# MOSFET Small-Signal Model

> [!abstract] Definition
> A linearised equivalent circuit valid for small AC signals superimposed on a DC bias point. Replaces the MOSFET with a voltage-controlled current source $g_m v_{gs}$ in parallel with output resistance $r_o$.

---

## Key Equations

| Equation | Meaning |
|----------|---------|
| $g_m = \frac{\partial I_D}{\partial V_{GS}}\bigg|_{Q} = \sqrt{2\mu_n C_{ox}(W/L)I_D}$ | Transconductance |
| $r_o = \frac{1}{\lambda I_D}$ | Output resistance (channel-length modulation) |
| $i_d = g_m v_{gs} + v_{ds}/r_o$ | Small-signal drain current |
| $f_T = \frac{g_m}{2\pi(C_{gs}+C_{gd})}$ | Unity-gain frequency |

---

## Intuition

At the Q-point the MOSFET behaves like a linear amplifier. The gate voltage controls drain current via $g_m$; $r_o$ captures the finite slope of $I_D$–$V_{DS}$ curves.

---

## Conditions & Caveats

> [!warning]
> - Valid only when signal swings are small compared to $V_{GS}-V_{th}$
> - Capacitances ($C_{gs}$, $C_{gd}$, $C_{sb}$, $C_{db}$) must be included for RF/high-frequency analysis

---

## Appears In

```dataview
TABLE file.folder AS "Course", type AS "Type"
FROM "Obsidian/Courses"
WHERE contains(file.content, "small-signal") OR contains(file.content, "small signal") OR contains(file.content, "gm")
SORT file.name ASC
```

---

## See Also

- [[Noise Analysis]]
- [[Feedback Stability]]
```

Create `Obsidian/Concepts/Feedback Stability.md`:

```markdown
---
type: concept
aliases: ["stability", "BIBO stability", "closed-loop stability", "gain margin", "phase margin"]
tags: [concept, control, analog]
courses: ["34722", "34655"]
date: 2026-03-23
---
# Feedback Stability

> [!abstract] Definition
> A feedback system is stable when its closed-loop poles have strictly negative real parts (continuous-time) or lie strictly inside the unit circle (discrete-time). Gain margin and phase margin quantify distance from instability.

---

## Key Equations

| Equation | Meaning |
|----------|---------|
| $T(s) = \frac{L(s)}{1+L(s)}$ | Closed-loop TF (unity feedback) |
| $\text{GM} = -|L(j\omega_\text{pc})|_\text{dB}$ | Gain margin at phase crossover |
| $\text{PM} = 180° + \angle L(j\omega_\text{gc})$ | Phase margin at gain crossover |
| Nyquist criterion: encirclements of $-1$ | General stability test |

---

## Intuition

If the loop gain reaches 1 while the phase shift reaches −180°, the system reinforces its own errors — it oscillates. Gain and phase margins tell you how far you are from that condition.

---

## Conditions & Caveats

> [!warning]
> - Bode stability criterion assumes minimum-phase open-loop $L(s)$; use full Nyquist for non-minimum-phase systems
> - PM > 45° and GM > 6 dB are typical design targets

---

## Appears In

```dataview
TABLE file.folder AS "Course", type AS "Type"
FROM "Obsidian/Courses"
WHERE contains(file.content, "stability") OR contains(file.content, "phase margin") OR contains(file.content, "gain margin")
SORT file.name ASC
```

---

## See Also

- [[Transfer Function]]
- [[Bode Plot]]
```

Create `Obsidian/Concepts/Noise Analysis.md`:

```markdown
---
type: concept
aliases: ["noise figure", "thermal noise", "noise floor", "NF"]
tags: [concept, analog, circuits, RF]
courses: ["34655"]
date: 2026-03-23
---
# Noise Analysis

> [!abstract] Definition
> The process of quantifying random signal fluctuations in electronic circuits, typically characterised by noise spectral density, noise figure (NF), and equivalent input-referred noise voltage/current.

---

## Key Equations

| Equation | Meaning |
|----------|---------|
| $S_{vn} = 4kTR$ (V²/Hz) | Thermal (Johnson–Nyquist) noise PSD |
| $NF = 10\log_{10}(F)$, $F = \frac{\text{SNR}_\text{in}}{\text{SNR}_\text{out}}$ | Noise figure / noise factor |
| $v_{n,\text{total}}^2 = v_{n1}^2 + v_{n2}^2/A_1^2 + \cdots$ | Referred-to-input cascade formula |
| $S_{id} = 4kT\gamma g_m$ (A²/Hz) | MOSFET channel thermal noise |

---

## Intuition

Every resistor generates thermal noise. In amplifier chains the first stage dominates (Friis formula): maximise first-stage gain to suppress later noise contributions.

---

## Conditions & Caveats

> [!warning]
> - $1/f$ (flicker) noise dominates at low frequencies in MOSFETs
> - Noise is uncorrelated — add power spectral densities, not amplitudes

---

## Appears In

```dataview
TABLE file.folder AS "Course", type AS "Type"
FROM "Obsidian/Courses"
WHERE contains(file.content, "noise") OR contains(file.content, "NF") OR contains(file.content, "noise figure")
SORT file.name ASC
```

---

## See Also

- [[MOSFET Small-Signal Model]]
- [[Feedback Stability]]
```

**Step 3: Commit everything**

```bash
git add "Obsidian/Templates/Concept.md" "Obsidian/Concepts/"
git commit -m "feat: add Concept template and 7 starter cross-course concept notes"
```

---

## Task 10: Final verification and cleanup

**Step 1: Check submodule status is healthy**

```bash
git submodule status
```

Expected: all 7 submodules listed, no `-` prefix (unregistered)

**Step 2: Verify .gitmodules has correct paths**

```bash
cat .gitmodules
```

**Step 3: Check no dangling wikilinks to moved files**

```bash
grep -r "\[\[.*1\. Semester\|2\. Semester\|3\.semester\|4\. Semester" Obsidian/ --include="*.md" | head -20
```

Fix any found with Edit tool.

**Step 4: Verify top-level is clean**

```bash
ls /c/Users/Mads2/DTU
```

Expected: `.git`, `.gitmodules`, `.gitignore`, `.claude`, `.github`, `.githooks`, `Obsidian/`, `SPICEPilot/`, `spicepilot-kicad/`, `docs/`, `CONTRIBUTING.md`, `License.md`, `README.md`, `WARP.md`

**Step 5: Final summary commit**

```bash
git add -A
git status  # verify nothing unexpected
git commit -m "chore: vault restructure complete - all 5 proposals implemented" --allow-empty
```

---

## Execution Notes

- **Never** use `git add -A` before checking `git status` — risk of staging submodule state accidentally
- **Submodule moves**: `git mv` + edit `.gitmodules` + `git submodule sync` is the correct three-step sequence
- **Obsidian wikilinks**: Obsidian uses relative vault-root paths, not OS paths. `[[Archive/3rd Semester/DSP/]]` works from anywhere in the vault
- **3.semester content overlap**: Before moving any subfolder, `ls` both source and destination. If the destination already has a folder of the same name, move files individually
- If a `git mv` fails because the destination has content, use shell loop to move file-by-file

---
