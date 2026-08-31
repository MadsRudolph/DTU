# LCD1 Solver — Design Spec

**Date:** 2026-05-30
**Target use:** DTU course 34722 Linear Control Design 1, multiple-choice exam Tue 2-June-2026
**Status:** v1 design, pre-implementation

---

## 1. Purpose

Expert solver for the multiple-choice exam. The user picks the problem PATTERN from a menu, fills a structured form with the question's specifics, pastes the listed answer options, and the tool computes the true value via a deterministic Python backend, then ranks the user's options against it.

Must work fully offline (exam restrictions: no internet, no local LLM).

Not a generic control-theory tool — the variant list, traps, and pattern taxonomy are pulled 1:1 from the course-specific notes in `Obsidian/Courses/34722 Linear Control Design 1/Exam Prep/`.

---

## 2. Key design decisions (settled in brainstorming)

| Decision | Choice | Rationale |
|---|---|---|
| **Input model** | Pattern-first menu, structured forms | Maps 1:1 to existing P1–P7 taxonomy. Eliminates LLM router from critical path. |
| **UI form factor** | PyQt6 desktop app | Offline-friendly, self-contained, `pyinstaller`-able. Renders LaTeX via matplotlib mathtext; embeds matplotlib plots. |
| **Solve engine** | Pure deterministic Python (`python-control`, `sympy`, `numpy`) | No LLM anywhere. Exam-compliant. Trustworthy. |
| **Backend model** | Generalized solver functions, not exam-question lookups | Works on unseen exam questions. Existing MATLAB `solve_*.m` scripts become regression-test oracles, not the engine. |
| **v1 scope** | All 7 patterns, 1–3 variants each (14 solvers total) | Broad coverage in 3 days before exam. Depth where it pays off (P6, P3). |
| **Output depth** | Answer + ranked options. Optional one-line trap footnote. | Minimal. User already knows theory from the notes — tool just verifies. |
| **TF input format** | Single text field, sympy-parsed expression in `s` | Matches how exam papers print G(s). Widget echoes back parsed canonical form for sanity check. |

---

## 3. Architecture

### 3.1 Folder layout

```
4. Semester/Linear Control Design/EXAM/Solver/
├── README.md
├── requirements.txt
├── run.py                       # launcher: `python run.py`
├── lcd_solver/
│   ├── __init__.py
│   ├── tf_input.py              # sympy string → control.TransferFunction
│   ├── match.py                 # type-aware option matcher
│   ├── solvers/
│   │   ├── __init__.py
│   │   ├── p1_models.py
│   │   ├── p1_block_reduce.py
│   │   ├── p2_bode.py
│   │   ├── p3_stability.py
│   │   ├── p4_secondorder.py
│   │   ├── p5_ess.py
│   │   ├── p6_control.py
│   │   └── p7_theory.py
│   └── ui/
│       ├── __init__.py
│       ├── main_window.py       # PyQt6 main window + sidebar
│       ├── pattern_picker.py    # P1..P7 menu
│       ├── forms/               # one form widget per solver
│       │   ├── __init__.py
│       │   ├── form_p1_ode.py
│       │   ├── form_p1_ss.py
│       │   ├── form_p1_block.py
│       │   ├── form_p2_bode.py
│       │   ├── form_p3_stable_k.py
│       │   ├── form_p3_margins.py
│       │   ├── form_p4_2nd_order.py
│       │   ├── form_p4_k_for_spec.py
│       │   ├── form_p5_kp_from_ess.py
│       │   ├── form_p5_ess_table.py
│       │   ├── form_p6_pi_lead.py
│       │   ├── form_p6_p_for_pm.py
│       │   ├── form_p7_feedforward.py
│       │   └── form_p7_nested_ess.py
│       └── widgets.py           # TF input widget, result panel, options input
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── oracle_data.py           # facit values extracted from solve_*.m
    ├── test_p1.py
    ├── test_p2.py
    ├── test_p3.py
    ├── test_p4.py
    ├── test_p5.py
    ├── test_p6.py
    └── test_p7.py
```

### 3.2 Tech stack

- **python-control** — `tf`, `margin`, `freqresp`, `dcgain`, `pole`, `zero`. MATLAB-Control-Toolbox-equivalent API.
- **sympy** — parsing TFs from strings, symbolic equality checks for formula-option matching, symbolic root-finding for `solve_K_for_spec`.
- **numpy** — array math, `np.roots`, `np.interp`.
- **matplotlib** with `matplotlib.backends.backend_qtagg` — Bode/Nyquist/step plots embedded inside PyQt6.
- **PyQt6** — native widgets, offline, no browser.
- **pytest** — regression tests against historical exam answers.

All are pure-pip Windows-compatible. No internet at runtime.

### 3.3 Data flow (one solve)

```
[Pattern menu click]
    → sidebar loads the corresponding form widget
[User fills form fields + pastes options text]
    → form widget validates types, builds typed kwargs dict
    → calls solvers.pX.<solver_function>(**kwargs)
    → returns Result{value, kind, traps_hit, plot_data=None}
[Match module] (Result, options_text_block)
    → parses options per Result.kind (NUMBER / TF / DICT / PICK)
    → returns ranked OptionList[Option{text, parsed, distance, flag}]
[Result panel renders]
    → computed value (LaTeX where appropriate)
    → ranked options w/ closest match flagged ✓
    → traps_hit as one-line footnotes
    → embedded matplotlib plot if Result.plot_data is set
```

---

## 4. Solver inventory (14 solvers)

Every solver is a pure function — same inputs → same outputs, no global state.

### P1 — Models

**`solve_ode_to_tf(y_coeffs: list[float], u_coeffs: list[float]) -> TransferFunction`**
- LHS coefficient list for `aₙ y⁽ⁿ⁾ + … + a₀ y = bₘ u⁽ᵐ⁾ + … + b₀ u`.
- Returns `control.tf(u_coeffs, y_coeffs)`.
- Oracle tests: F22 Q8 (`3/(5s²+s+0.5)`), S21 Q8 (`1/(s²+2s+1)`), Theory Q4 (poles `{0,0,−4,−5}`).

**`solve_state_space_to_tf(A, B, C, D) -> TransferFunction`**
- Inputs: numpy 2D matrices. Validates shapes.
- Returns `control.ss2tf(control.ss(A, B, C, D))`.
- Oracle: REExam F21 Q6 (`G = 10/(s+1)`).

**`reduce_block_diagram(dsl_expr: str) -> sympy.Expr`**
- Tiny symbolic DSL evaluated against three primitives:
  - `series(*blocks)` → `prod(blocks)`
  - `parallel(*blocks)` → `sum(blocks)`
  - `feedback(forward, fb_path, sign=-1)` → `forward / (1 - sign*forward*fb_path)` (default negative feedback)
- Block names (`A`, `B`, `C`, ...) appearing in the expression are treated as opaque `sympy.Symbol`s — matches how exam questions label blocks. Specific TFs can also be substituted: `feedback(parallel(A, 1/(s+B)), 1)`.
- Returns `sympy.cancel(...)` of the resulting expression — canonical simplified form for option matching.
- Option matching uses TF-kind logic (canonical sympy form comparison). Since exam options also contain block-symbols, the matcher must compare two `sympy.Expr`s symbolically (`sympy.simplify(option - computed) == 0`), not coefficient lists.
- Oracle tests:
  - **S20 Q3:** `parallel(A, 1 / (1 + B/s))` → `((1+A)·s + A·B) / (s + B)`
  - **S21 Q1:** `feedback(parallel(series(A, B, C, D), series(E, C, D)), F, sign=-1)` (when fb tap is on the shared `B`) → `(A·B·C·D + E·C·D) / (1 + B·C·F)`
  - **F22 Q1:** `feedback(series(A, B, E, parallel(C, D), E), parallel(series(H1, "1/E"), H2))` — exact composition recovered from the F22 walkthrough; expected reduced form `A·B·E²·(C+D) / ((1+A·B)·(1 + (C+D)·E·H2)·E + A·B·E·(C+D)·H1)`.
- DSL parser is sympy's `parse_expr` with a `local_dict` registering the three primitives as Python callables. ~30 LOC.

### P2 — Bode read-off

**`compose_tf_from_bode(dc_gain_dB: float, corners: list[Corner], phase_events: list[PhaseEvent]) -> tuple[TransferFunction, Figure]`**
- `Corner = (omega: float, slope_change_dB_per_dec: int)` — e.g. `(10, -20)` means at ω=10 the magnitude slope drops by 20 dB/dec.
- `PhaseEvent = (omega: float, phase_change_deg: int)` — e.g. `(10, -90)` indicates phase falls 90° near ω=10.
- Algorithm: place a pole/zero at each corner. Sign of slope change → pole or zero. Sign of phase change disambiguates LHP vs RHP (RHP zero: slope +20, phase −90). DC gain sets static factor.
- Returns the composed `G(s)` plus a matplotlib Figure of its Bode for visual comparison.
- Oracle tests: S20 Q6, S21 Q5 (`100/((1+s)²(1−0.1s))` — RHP pole), F22 Q4 (RHP zero), F22 Q5 (`(s−2)/(1+s)²`), REExam Q5 (`100(s+10)/(s−1)`).

### P3 — Stability

**`solve_stable_K_range(G: TransferFunction) -> tuple[float, float]`**
- Detects open-loop RHP poles via `pole(G).real > 0`.
- **Stable plant** (`P = 0`): returns `(0, GM)` where `GM = margin(G)[0]`.
- **Unstable plant** (`P > 0`): samples `G(jω)` densely, finds Nyquist negative-real-axis crossings (zero crossings of `Im(G(jω))` where `Re(G(jω)) < 0`). Computes `K_min = 1 / |x_cross_nearest_to_origin|`. Returns `(K_min, math.inf)`.
- Oracles: S21 Q4 (`K/(s+1)³` → `0 < K < 8`), F22 Q12 (RHP pole → `K > 45`), REExam Q14 (`K < 0.398`), REExam Q16 (`K > 40.5`).

**`solve_margins(G: TransferFunction) -> dict`**
- Wrapper over `control.margin`. Returns `{GM, GM_dB, PM_deg, omega_pc, omega_gc}`.
- Oracle: F22 Q11 (`GM ≈ 15.71 dB`).

### P4 — Second-order

**`solve_2nd_order(*, Mp=None, zeta=None, omega_n=None, t_p=None, t_s_2pct=None) -> dict`**
- Bidirectional — accepts any consistent subset. ζ is determined by either `Mp` *or* `zeta`; ω_n by either `omega_n`, `t_p`, or `t_s_2pct`. Form has all five inputs, blank fields are inferred.
- Formulas: `Mp = exp(−πζ/√(1−ζ²))`, `ζ = ln(1/Mp)/√(π² + ln²(1/Mp))`, `t_p = π/(ω_n√(1−ζ²))`, `t_s = 4/(ζω_n)`, `t_r ≈ 1.8/ω_n`, `ω_BW = ω_n√((1−2ζ²) + √(4ζ⁴−4ζ²+2))`, `ω_r = ω_n√(1−2ζ²)` (only if `ζ < 0.707`), `M_r = 1/(2ζ√(1−ζ²))`.
- Returns dict of all derivable values. Raises `ValueError` on inconsistent inputs (e.g., both `Mp` and `zeta` given but disagreeing).
- Oracles: S21 Q10, REExam Q10 (ζ=√2/2 → 4.3%), F22 Q10.

**`solve_K_for_spec(G_str: str, spec: str) -> tuple[float, float]`**
- `G_str` is a sympy expression in symbols `s` and `K`. Example: `"K / (s*(s+5))"`.
- `spec` is a string like `"Mp <= 0.12"` or `"zeta >= 0.5"`.
- Algorithm: build symbolic closed-loop `G_cl(s, K) = G(s,K) / (1 + G(s,K))`. Match against standard 2nd-order form to extract `ω_n(K)` and `ζ(K)`. Invert the spec.
- v1 limitation: only handles closed loops reducible to 2nd-order standard form. Raises `NotImplementedError` with a clear message for higher-order cases.
- Oracle: S21 Q9 (`K ≤ 19.97`).

### P5 — Steady-state error

**`solve_KP_from_ess(G0: float, G0_unit: str, ess_target: float) -> float`**
- v1: step input on a type-0 plant only (the only variant in the historical solved scripts).
- `G0_unit ∈ {'linear', 'dB'}` — form has a dropdown. dB is converted via `10**(G0/20)` before use.
- `K_P = (1/ess − 1) / G(0)`.
- Ramp/parabola variants deferred — straightforward to add later via a `input_kind` arg, but no historical oracle for them.
- Oracle: F22 Q16 (`G(0)=−7.96 dB`, `ess=0.555` → `K_P=2`).

**`solve_ess_table(G: TransferFunction) -> dict`**
- Computes system type (count poles at origin), `K_p = lim_{s→0} G`, `K_v = lim_{s→0} s·G`, `K_a = lim_{s→0} s²·G`, then the steady-state error for step/ramp/parabola.
- Oracle: REExam Q4 (type-2 → step=0, ramp=0, parabola = `1/K_a = 1`).

### P6 — Controllers

**`solve_pi_lead(unknown: str, **knowns) -> float`**
- `unknown ∈ {'alpha', 'Ni', 'KP'}`.
- All three modes use the phase-budget equation `−180° + γ_M = φ_G + φ_Lead + φ_PI` with `φ_PI = −atan(1/N_i)` and `φ_Lead = asin((1−α)/(1+α))`. All arithmetic in **degrees** (uses `np.atan2d`, `np.sind`, etc.).
- `alpha` mode: needs (`omega_c`, `gamma_M_deg`, `phi_G_deg`, `N_i`).
- `Ni` mode: needs (`omega_c`, `gamma_M_deg`, `phi_G_deg`, `alpha`).
- `KP` mode: needs (`G: TF`, `gamma_M_deg`, `alpha`, `N_i`). Finds the required ω_c by interpolation over `freqresp(G)`, then builds full compensator and computes `K_P = 1 / |G(jω_c) C_PI(jω_c) C_d(jω_c)|`.
- Oracles: F22 Q17 (α=0.5), F22 Q19 (K_P=3.4154), REExam Q15 (M_D=3.3), REExam Q17 (N_i=1.57).

**`solve_P_for_PM(G: TransferFunction, target_PM_deg: float) -> dict`**
- Finds ω where `∠G(jω) = −180° + γ_M` via interpolation over `freqresp`. Sets `K_P = 1 / |G(jω)|`.
- Returns `{K_P, omega_c}`.
- Oracles: S20 Q9 (`K_P=0.06`), S21 Q6 (`K_P=88`).

### P7 — Theory structural picks

**`pick_feedforward_form(n_lags: int, D_order: int = 2) -> dict`**
- For a chain of `n` first-order lags with disturbance dynamics of order `D_order`, returns the proper-and-fast feedforward formula and the `τ_f ≤ min(τ_k)/5` bound.
- Returns `{formula_latex, tau_f_bound_text, explanation}`.
- Oracle: Theory Q8.

**`solve_nested_ess(architecture: str, **kwargs) -> float`**
- `architecture ∈ {'two_KP_same', 'nested_K1_K2'}`.
- For `two_KP_same` (Theory Q9): inputs `G0: float`, `ess_target: float`. Closed-form quadratic in `K_P` derived in `p7_theory.py` from `e(0) = (1 + K_P·G0) / (1 + K_P·G0 + K_P²·G0)`. Returns positive real root.
- For `nested_K1_K2` (Theory Q6): inputs `eps1`, `eps2`, `G2_0`. Returns `K_2 = (1 − eps2) / (eps2 · G2_0 · (1 − eps1))`.
- Oracles: Theory Q9 (`G0=0.75`, `ess=0.25` → `K_P=4`), Theory Q6 (`eps1=0.4`, `eps2=0.05`, `G2_0=0.4` → `K_2=79.17`).

---

## 5. TF input widget (`tf_input.py`)

Single text field accepting an expression in symbol `s`. Pipeline:

```python
def parse_tf(expr: str) -> control.TransferFunction:
    s = sympy.Symbol("s")
    parsed = sympy.parse_expr(expr, local_dict={"s": s})
    num, den = sympy.fraction(sympy.together(sympy.cancel(parsed)))
    num_coeffs = [float(c) for c in sympy.Poly(num, s).all_coeffs()]
    den_coeffs = [float(c) for c in sympy.Poly(den, s).all_coeffs()]
    return control.tf(num_coeffs, den_coeffs)
```

Widget echoes back below the input field:
- canonical factored form (zeros, poles, gain)
- DC gain `|G(0)|` in both linear and dB
- **red warning** if any pole has positive real part (the unstable-plant signal that flips the `solve_stable_K_range` interval)

That echo is the user-facing sanity check.

---

## 6. Option-matching (`match.py`)

Type-aware. Solver's `Result.kind` selects the strategy.

```python
class ResultKind(str, Enum):
    NUMBER = "number"
    TF     = "tf"
    DICT   = "dict"
    PICK   = "pick"

@dataclass
class Option:
    raw_text: str
    parsed: Any
    distance: float | None       # None for non-numeric or unparseable
    flag: str                    # "match" | "also_plausible" | "no_match" | "unparseable"

def match(result: Result, options_text: str) -> list[Option]: ...
```

### NUMBER
- Parse each line. Accept `−7.96 dB` → linear via `10**(x/20)`. Accept `1/2`, `pi/4`, etc. via sympy.
- Rank by `abs(option_val − computed_val) / abs(computed_val)`.
- Closest → `flag="match"`. Any within 1% → `flag="also_plausible"`. Others → `"no_match"`.
- If two options are <1% apart, surface ambiguity in the UI.

### TF
- Parse each option with sympy (same pipeline as `tf_input.py`).
- Compare numerator and denominator polynomial coefficient lists with relative tolerance 1e-3.
- Alternative: compare sorted pole and zero lists with absolute tolerance proportional to magnitude.

### DICT
- Form for any DICT-returning solver (`solve_margins`, `solve_2nd_order`, `solve_ess_table`, `solve_P_for_PM`) includes a key-selector dropdown listing the dict keys the solver returns. User picks "match against PM" or "match against K_P". Matching then falls back to NUMBER for the chosen scalar.
- Result panel still displays the **full** dict regardless — the dropdown only governs which key drives option matching.

### PICK
- Solver returns a structural choice (e.g. "option (d) — proper fast feedforward with `τ_f ≤ min(τ_k)/5`"). The result panel displays the canonical answer text and formula. User eyeball-matches. No symbolic option comparison — too brittle for full feedforward formulas with bounds.

---

## 7. Testing strategy

The MATLAB `solve_*.m` scripts in `4. Semester/Linear Control Design/EXAM/Scripts/solved/` contain official facit values for ~30 historical exam questions. These are the **oracle**.

### 7.1 Oracle data

```python
# tests/oracle_data.py
F22_Q17 = dict(unknown="alpha", omega_c=6.4, gamma_M_deg=75,
               phi_G_deg=-112.77, N_i=5, facit=0.5)

F22_Q19 = dict(unknown="KP", G="900/((0.25*s+1)*(s**2+50*s+3000))",
               gamma_M_deg=75, alpha=0.01, N_i=3, facit=3.4154)

REEXAM_F21_Q17 = dict(unknown="Ni", omega_c=25.04, gamma_M_deg=75,
                      phi_G_deg=-151.064, alpha=0.01, facit=1.57)

# ... one entry per historical question that exercises a generalized solver
```

### 7.2 Test pattern

```python
# tests/test_p6.py
def test_F22_Q17():
    args = {k: v for k, v in F22_Q17.items() if k != "facit"}
    result = solve_pi_lead(**args)
    assert result == pytest.approx(F22_Q17["facit"], rel=1e-3)
```

### 7.3 Coverage target

Every variant solver has ≥ 1 historical oracle test. Solvers with multiple historical occurrences (P6 PI-Lead, P3 stable-K) have one test per occurrence. CI green ⇔ all historical official answers reproduced.

---

## 8. PyQt6 UI (`ui/`)

### 8.1 Layout

Two-pane main window:
- Left sidebar: collapsible P1–P7 tree. Click a leaf → loads its form into the right pane.
- Right pane top: the form (input fields + options textarea + Solve button).
- Right pane bottom: the result panel (computed value, ranked options, optional embedded matplotlib plot, trap footnote).

### 8.2 Form widget contract

Each form is a `QWidget` subclass exposing:

```python
class SolverForm(QWidget):
    title: str            # for sidebar label
    pattern: str          # "P6"
    variant: str          # "PI-Lead 3-way"

    def inputs(self) -> dict:                # → kwargs for the solver
        ...

    def solver_fn(self) -> Callable:         # the generalized solver function
        ...
```

Adding a new solver = adding one file in `ui/forms/` + one line in the sidebar registry.

### 8.3 Result panel

- Top: bold computed value (LaTeX-rendered via `matplotlib.mathtext`).
- Middle: options table with ✓ on the matched line.
- Bottom (collapsible): traps-hit footnote and (if applicable) matplotlib Bode/Nyquist/step plot via `FigureCanvasQTAgg`.

---

## 9. Constraints and conventions (this repo)

- **Windows 11, Python 3.11+.**
- Tool path: `4. Semester/Linear Control Design/EXAM/Solver/`.
- Pip-installable deps only. Pinned in `requirements.txt`.
- Repo has a broken nested git repo at `Obsidian/Courses/34722 Linear Control Design 1/Exercises/Work/regbot/Report` — never use `git add -A`; always stage by explicit path.
- No `Co-Authored-By: Claude` or AI mention in commit messages.
- Do not commit unless the user explicitly asks.

---

## 10. Out of scope for v1 (deferred)

- **P1 linearization** — every nonlinearity has its own derivative; can't generalize cleanly.
- **P6 prefilter sub-solver** — covered by formula on the cheat-sheet, low exam frequency.
- **P6 stand-alone Lead** — subsumed by PI-Lead with `N_i → ∞`.
- **Full symbolic matching for PICK-kind answers** — too brittle; tool shows canonical answer instead.
- **`pyinstaller` portable .exe** — after exam if useful.

---

## 11. Acceptance criteria for v1

1. `python run.py` launches the PyQt6 window with no errors on a fresh Windows install of `requirements.txt`.
2. All 14 solvers wired to forms; navigable via sidebar.
3. `pytest tests/` is green — every historical oracle test passes.
4. Worked example: F22 Q17 (PI-Lead α). User fills (ω_c=6.4, γ_M=75, φ_G=−112.77, N_i=5), pastes options `0.1 / 0.5 / 0.9 / 1.5`, hits Solve. Result panel shows `α = 0.5000` and flags option `0.5` as match.
5. Worked example: F22 Q12 (stable-K, RHP plant). User enters `G(s) = 1/((s−2.5)·…)`, the TF echo flags the RHP pole, Solve returns `K > 45.0` (not `0 < K < 45`).
6. Runs offline — no network calls anywhere.
7. Worked example: F22 Q1 (block reduction). User types `feedback(parallel(series(A,B,C,D), series(E,C,D)), F)`, pastes the 5 algebraic-expression options, hits Solve. Result panel shows `(A·B·C·D + E·C·D)/(1 + B·C·F)` (or the equivalent canonical form) and flags the matching option.
