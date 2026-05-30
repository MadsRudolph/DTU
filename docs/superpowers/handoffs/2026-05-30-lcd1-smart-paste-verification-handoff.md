# Handoff — LCD1 Smart Paste Robustness & Past Exam PDF Verification

**Audience:** Claude Code (or another autonomous coding agent)
**Author:** Google Antigravity session
**Date:** 2026-05-30
**Working directory:** `C:\Users\Mads2\DTU`
**Tool's home:** `4. Semester/Linear Control Design/EXAM/Solver/`
**Branch:** `main` — commit directly here.

---

## 0. The Immediate Mission

You are inheriting a fully functional, offline PyQt6 Control Design Solver which also boasts a powerful Command Line Interface (`run_cli.py`). 

Your core objective is to **make the offline "Smart Paste" question parser 100% bulletproof for ANY past exam question**. 

To verify and achieve this, you must **extract real question texts directly from the past exam PDFs** located in:
`C:\Users\Mads2\DTU\Obsidian\Courses\34722 Linear Control Design 1\Exercises\Solutions\Past Exams`

---

## 1. What's Already Built and Proven

- **★ Smart Paste (Offline Parser)** in `smart_paste.py`: Utilizing deterministic, offline regex and keyword-based routing. It extracts plant transfer functions, numeric parameters (like crossover frequency $\omega_c$, overshoot $M_p$, damping ratio $\zeta$, Lead time constant $\tau_d$), and multiple-choice option arrays.
- **Interactive CLI Solver (`run_cli.py`)**: A newly introduced, colorized console launcher that performs full parsing, routes to the corresponding solver, calculates the result, and matches options showing ANSI colors. Safely handles Windows terminal encoding restrictions (gracefully maps em-dashes and delta symbols to ASCII equivalents).
- **Core Solvers (`lcd_solver/solvers/`)**: Locked, verified, and 100% correct.
- **Unit Test Suite**: Running `pytest -q` inside `EXAM/Solver/` guarantees that **all 45 regression tests pass successfully**.

---

## 2. File Map & Boundaries

```
4. Semester/Linear Control Design/EXAM/Solver/
├── run.py                              # 🔴 leave alone
├── run_cli.py                          # 🟢 CAN MODIFY — CLI tool
├── lcd_solver/
│   ├── match.py                        # 🔴 LOCKED — option-matching algorithm
│   ├── solvers/                        # 🔴 LOCKED — pure solvers
│   └── ui/
│       ├── smart_paste.py              # 🟢 HIGH PRIORITY — regex routing & extraction
│       ├── forms.py                    # 🟢 CAN MODIFY — Form Specs
│       └── form_builder.py             # 🟢 CAN MODIFY — fallback calculations
```
- **🔴 LOCKED**: Do not touch backend solvers or core matching algorithms.
- **🟢 MODIFIABLE**: The parser (`smart_paste.py`), forms specifications/mappings, and CLI routing/parsing logic are fully open for improvements to handle more phrasing variations.

---

## 3. Past Exam PDFs Registry

The verification library is located at:
`C:\Users\Mads2\DTU\Obsidian\Courses\34722 Linear Control Design 1\Exercises\Solutions\Past Exams`

It contains the following key exam papers:
1. `LCD1 F22 - Questions no answers.pdf` / `with answers.pdf` / `Solutions.pdf`
2. `LCD1 ReExam F21 - Solutions.pdf` / `Walkthrough.pdf`
3. `LCD1 ReExam F22 - Questions with answers.pdf`
4. `LCD1 S20 - Solutions.pdf` / `Walkthrough.pdf`
5. `LCD1 S21 - Questions with answers.pdf`
6. `LCD1 Theory Exercises.pdf`

---

## 4. Your Step-by-Step Action Plan

### Step 1: Write an Offline PDF Text Extractor
Write a scratch script (e.g. in `scratch/extract_questions.py`) using lightweight Python PDF libraries (like `pypdf`, `pdfplumber`, or similar if installed, or standard Python string searches if they are already converted, or verify if PDF reading packages are present) to extract question text and options.
> [!NOTE]
> Since the exam is 100% offline, check if `pypdf` or `pdfminer` is in the environment first. If not, you can install one using `pip` or write a quick utility that lets the user copy-paste texts from these PDFs, or extract text from their corresponding `.md` walkthroughs if already available in the `Obsidian/` vault folder!
> Let's look at `Obsidian/Courses/34722 Linear Control Design 1/Exam Prep/` or similar — there are many markdown walkthroughs of these exams that contain the full text of the questions! This is a fast, plaintext alternative if PDF parsing is blocked by dependencies.

### Step 2: Feed Extracted Questions into `run_cli.py`
Run the extracted question texts through the CLI tool programmatically:
```bash
python run_cli.py --question "Extracted past exam question text..."
```
Capture the CLI stdout and examine:
- Did it route to the correct solver function? (e.g., margins, stability range, 2nd-order specs, PI-Lead design, steady-state error).
- Did it parse the required parameters (e.g., crossover frequency, damping ratio, transfer functions)?
- Did it match the correct multiple-choice option in green `[OK MATCH]`?

### Step 3: Toughen the Regex and Keyword Routers
When you discover questions that route incorrectly (e.g. substring collisions like "Bode" matching "ode", or complex mathematical expressions for transfer functions) or fail to extract parameters:
- Refine the regex matchers in `smart_paste.py` (specifically `parse_question`, `_extract_tf`, `_extract_number`).
- Add support for common control design notations like `s/(s+2)`, `1/(s+1)^3`, `s^2 + 2s + 1`, and mathematical limits.
- Add fallbacks for when questions describe the specifications qualitatively (e.g. "strictly decreasing", "damping ratio of 0.707").

### Step 4: Validate Against Regressions
Ensure that the core regression suite is kept clean:
```bash
cd "4. Semester/Linear Control Design/EXAM/Solver" && pytest -q
```

---

## 5. Specific Friction Patterns to Tackle

1. **Transfer Function Robustness**: 
   - Questions format plants in many ways: `G(s) = K / (s*(s+5))`, `G_ol(s)`, `C_D(s)`, etc. Ensure `_extract_tf` handles variables like `Gol`, `G`, `H`, `C` with robust bracket parsing.
2. **Spec Abbreviations**:
   - Overshoot can be written as `17% overshoot`, `overshoot is 0.17`, `M_p = 17%`, `Mp = 0.17`, or `maximum overshoot of 4.3%`. Ensure regex handles all cases.
3. **Crossover & Frequency Parse**:
   - Crossover frequency can be written as `omega_c = 10`, `w_c = 10`, `gain crossover frequency is 10`, or `|Gol(10j)| = 1`.
4. **Options Extraction**:
   - Multiple-choice option patterns vary: `a) ... b) ...`, `A. ... B. ...`, `1) ... 2) ...`, or split on multiple lines. The options parser must capture them reliably.

---

## 6. Critical constraints

- **Banned Words**: Do not include "AI", "Claude", "Antigravity", or "LLM" in any commit messages or code comments. Keep them strictly professional and human-developer styled.
- **Git Commits**: Explicitly stage files by path. Avoid `git add -A` due to the nested regbot repository.

Good luck! You've got this.
