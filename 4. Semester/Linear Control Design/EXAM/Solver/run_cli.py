"""LCD1 Solver CLI.

Allows offline question parsing, routing, solving, and option matching from the terminal.
Supports inline text arguments, file reading, and interactive pasting.

Usage:
  python run_cli.py --question "Consider an open-loop..."
  python run_cli.py --file question.txt
  python run_cli.py (runs interactively)
"""
from __future__ import annotations
import sys
import os
import argparse
import importlib
import ast
import math

# Adjust path to include solver root using absolute path
solver_dir = os.path.dirname(os.path.abspath(__file__))
if solver_dir not in sys.path:
    sys.path.append(solver_dir)

# Initialize a headless QApp before any Qt imports
from PyQt6.QtWidgets import QApplication
app = QApplication.instance() or QApplication([])

from lcd_solver.ui.forms import ALL_FORMS
from lcd_solver.ui.smart_paste import SmartPasteWidget
from lcd_solver.tf_input import parse_tf
from lcd_solver.types import Result, ResultKind
from lcd_solver.match import match as match_options

# Reconfigure stdout to gracefully handle encoding limitations on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors='replace')

# Enable ANSI colors on Windows
if os.name == 'nt':
    os.system('color')

# ANSI colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
GRAY = "\033[90m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def gather_cli_inputs(spec, parsed_inputs):
    kwargs = {}
    for f in spec.fields:
        # Check if parsed_inputs has it
        val = parsed_inputs.get(f.name)
        if val is None:
            # Fall back to default
            if f.default is not None:
                val = f.default
            else:
                continue

        # Convert to target kind
        if f.kind == "tf":
            if isinstance(val, str):
                kwargs[f.name] = parse_tf(val.strip())
            else:
                kwargs[f.name] = val
        elif f.kind == "dropdown":
            kwargs[f.name] = str(val)
        elif f.kind == "int":
            kwargs[f.name] = int(str(val).strip())
        elif f.kind == "float":
            kwargs[f.name] = float(str(val).strip())
        else:  # str
            txt = str(val).strip()
            try:
                kwargs[f.name] = ast.literal_eval(txt)
            except (ValueError, SyntaxError):
                kwargs[f.name] = txt
    return kwargs


def run_solver_cli(routing):
    func_name = routing["solver_function"]
    inputs = routing["inputs"]
    options_text = routing["options"]

    # Find matching FormSpec
    spec = next((s for s in ALL_FORMS if s.solver_function == func_name), None)
    if not spec:
        print(f"{RED}Error: Form specification for '{func_name}' not found.{RESET}")
        return

    title = spec.title.replace("—", "-")
    explanation = spec.explanation.replace("—", "-").splitlines()[0]
    print(f"\n{BOLD}{CYAN}------------------------------------------------------{RESET}")
    print(f"{BOLD}{CYAN}* ROUTED TO SOLVER: {title}{RESET}")
    print(f"{CYAN}Description: {explanation}{RESET}")
    print(f"{BOLD}{CYAN}------------------------------------------------------{RESET}")

    # Gather inputs
    try:
        kwargs = gather_cli_inputs(spec, inputs)
    except Exception as e:
        print(f"{RED}Error gathering inputs: {e}{RESET}")
        return

    print(f"\n{BOLD}[1] Detected Parameters:{RESET}")
    for k, v in kwargs.items():
        print(f"  - {k}: {v}")

    # Run solver
    print(f"\n{BOLD}[2] Solving...{RESET}")
    try:
        # Implied lead-only magnitude check
        if spec.solver_function == "solve_pi_lead" and kwargs.get("unknown") == "alpha" and "phi_G_deg" not in kwargs:
            if "tau_d" in kwargs and "omega_c" in kwargs:
                td_val = float(kwargs["tau_d"])
                wc_val = float(kwargs["omega_c"])
                raw = 1.0 / (td_val * wc_val) ** 2
            else:
                print(f"{RED}Error: Please provide phi_G_deg and gamma_M_deg to solve the phase budget, or both tau_d and omega_c for Lead-only magnitude.{RESET}")
                return
        else:
            mod = importlib.import_module(spec.solver_module)
            fn = getattr(mod, spec.solver_function)
            raw = fn(**kwargs)

        # Coerce solve_pi_lead float result to a dictionary containing derived metrics (like M_D, M_D_dB)
        if spec.solver_function == "solve_pi_lead":
            unknown = kwargs.get("unknown")
            if unknown == "alpha":
                alpha_val = float(raw)
                md_val = 1.0 / math.sqrt(alpha_val) if alpha_val > 0 else 0.0
                md_db = 20.0 * math.log10(md_val) if md_val > 0 else 0.0
                raw = {
                    "alpha": alpha_val,
                    "M_D": md_val,
                    "M_D_dB": md_db
                }
            elif unknown == "Ni":
                raw = {
                    "N_i": float(raw)
                }
            elif unknown == "KP":
                raw = {
                    "K_P": float(raw)
                }
    except Exception as e:
        print(f"{RED}Solver error: {e}{RESET}")
        return

    # Build the value-text
    if spec.result_kind == ResultKind.NUMBER:
        value_text = f"{float(raw):.6g}"
    elif spec.result_kind == ResultKind.DICT:
        value_text = ", ".join(f"{k} = {v:.6g}" for k, v in raw.items())
    elif spec.result_kind == ResultKind.PICK:
        if isinstance(raw, tuple):
            value_text = f"({', '.join(f'{x:.6g}' if isinstance(x, float) else str(x) for x in raw)})"
        elif isinstance(raw, dict):
            value_text = raw.get("formula_latex") or str(raw)
        else:
            value_text = str(raw)
    else:  # TF
        value_text = str(raw)

    print(f"  {GREEN}[OK] Solution calculated successfully!{RESET}")
    print(f"  {BOLD}Raw Result: {value_text}{RESET}")

    # Options matching
    if options_text:
        print(f"\n{BOLD}[3] Options Matching:{RESET}")
        try:
            matched_opts = match_options(Result(value=raw, kind=spec.result_kind), options_text, match_key="auto")
            
            for opt in matched_opts:
                if opt.flag == "match":
                    color = GREEN
                    prefix = " [OK MATCH]  "
                elif opt.flag == "also_plausible" or "ambiguous" in opt.note:
                    color = YELLOW
                    prefix = " [? AMBIGU]  "
                elif opt.flag == "unparseable":
                    color = GRAY
                    prefix = " [x ERROR]   "
                else:
                    color = RED
                    prefix = " [  MISMATCH]"
                
                note_str = opt.note.replace("\u0394", "d").replace("Δ", "d").replace("—", "-") if opt.note else ""
                note_str = f" ({note_str})" if note_str else ""
                print(f"{color}{prefix} Option: {opt.raw_text:<15} {note_str}{RESET}")
        except Exception as e:
            print(f"{RED}Error matching options: {e}{RESET}")
    else:
        print(f"\n{YELLOW}No multiple-choice options provided or parsed.{RESET}")
    print(f"{BOLD}{CYAN}------------------------------------------------------{RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="LCD1 Smart Solver CLI")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-q", "--question", type=str, help="Exam question text directly on command line")
    group.add_argument("-f", "--file", type=str, help="Path to text file containing exam question")
    args = parser.parse_args()

    question_text = ""
    if args.question:
        question_text = args.question
    elif args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                question_text = f.read()
        except Exception as e:
            print(f"{RED}Error reading file: {e}{RESET}")
            sys.exit(1)
    else:
        # Interactive mode
        print(f"\n{BOLD}{CYAN}======================================================{RESET}")
        print(f"{BOLD}{CYAN}* LCD1 Smart Solver CLI - 34722{RESET}")
        print(f"{BOLD}{CYAN}======================================================{RESET}")
        print("Please paste your exam question below (including the options).")
        print(f"When finished, press {BOLD}Ctrl+Z{RESET} and {BOLD}Enter{RESET} on Windows (or {BOLD}Ctrl+D{RESET} on Linux/macOS):")
        print(f"{GRAY}------------------------------------------------------{RESET}")
        try:
            question_text = sys.stdin.read()
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Cancelled.{RESET}")
            sys.exit(0)
        print(f"{GRAY}------------------------------------------------------{RESET}")

    question_text = question_text.strip()
    if not question_text:
        print(f"{RED}Error: No question text provided.{RESET}")
        sys.exit(1)

    sp_widget = SmartPasteWidget(None)
    routing = sp_widget.parse_question(question_text)
    if not routing or not routing.get("solver_function"):
        print(f"\n{RED}Could not automatically parse or route this question.{RESET}")
        print("Ensure keywords like 'crossover frequency', 'overshoot', 'stability', or 'step response' are present.")
        sys.exit(1)

    run_solver_cli(routing)


if __name__ == "__main__":
    main()
