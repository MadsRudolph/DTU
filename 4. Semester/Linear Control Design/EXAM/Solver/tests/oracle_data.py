"""Historical exam facit values, used as solver regression oracles.

Each entry is a dict of solver inputs plus the official facit.
Source: 4. Semester/Linear Control Design/EXAM/Scripts/solved/solve_*.m
"""

# P1: solve_ode_to_tf — coefficient lists ordered HIGHEST degree first
F22_Q8 = dict(
    y_coeffs=[5, 1, 0.5],       # 5y'' + y' + 0.5y
    u_coeffs=[3],               # = 3u
    facit_poles=[-0.1 + 0.3j, -0.1 - 0.3j],
)
S21_Q8 = dict(
    y_coeffs=[1, 2, 1],         # y'' + 2y' + y
    u_coeffs=[1],               # = u
    facit_poles=[-1.0, -1.0],
)
THEORY_Q4 = dict(
    y_coeffs=[1, 9, 20, 0, 0],  # y(4) + 9 y(3) + 20 y'' (zeros for y' and y)
    u_coeffs=[71],              # = 71 u
    facit_poles=[0.0, 0.0, -4.0, -5.0],
)

# P1: solve_state_space_to_tf
REEXAM_F21_Q6 = dict(
    A=[[-1.0, 0.0], [0.0, -1.0]],
    B=[[1.0], [9.0]],
    C=[[1.0, 1.0]],
    D=[[0.0]],
    facit_poles=[-1.0],
    facit_dc_gain=10.0,
)

# P1: reduce_block_diagram — the DSL expression string vs the expected simplified sympy form
S20_Q3 = dict(
    dsl="parallel(A, 1 / (1 + B/s))",
    facit_str="((1+A)*s + A*B) / (s + B)",
)
# S21 Q1: two forward paths share feedback through B*C*F. The TEXTBOOK reduced form is
# (A*B*C*D + E*C*D)/(1 + B*C*F). One valid algebraic composition that yields that
# canonical form symbolically:
S21_Q1 = dict(
    dsl="(series(A, B, C, D) + series(E, C, D)) / (1 + B*C*F)",
    facit_str="(A*B*C*D + E*C*D) / (1 + B*C*F)",
)
