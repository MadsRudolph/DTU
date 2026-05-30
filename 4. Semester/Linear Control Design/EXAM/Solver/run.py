"""LCD1 Solver launcher.

Usage: python run.py
"""
import sys

def main():
    from lcd_solver.ui.main_window import launch
    launch(sys.argv)

if __name__ == "__main__":
    main()
