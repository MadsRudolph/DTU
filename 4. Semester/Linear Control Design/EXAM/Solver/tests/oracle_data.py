"""Historical exam facit values, used as solver regression oracles.

Each entry is a dict of solver inputs plus the official facit.
Source: 4. Semester/Linear Control Design/EXAM/Scripts/solved/solve_*.m
"""
import math

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

# P2: compose_tf_from_bode
# Each test gives the user's read-off (DC dB, corners, phase events) → expected factored G(s).
# A "corner" is (omega, slope_change_dB_per_dec) at that frequency.
# A "phase_event" is (omega, phase_change_deg) — sign disambiguates LHP vs RHP.

F22_Q5 = dict(
    # G(s) = (s-2)/(1+s)**2  →  RHP zero at +2, double LHP pole at -1
    # DC: G(0) = -2/1 = -2 → |G(0)| = 2 → 20*log10(2) ≈ 6.0206 dB
    dc_gain_dB=20.0 * math.log10(2.0),
    corners=[(1, -20), (1, -20), (2, +20)],          # two poles at 1, RHP zero at 2
    phase_events=[(1, -90), (1, -90), (2, -90)],     # RHP zero: phase DROPS
    facit_poles=[-1.0, -1.0],
    facit_zeros=[+2.0],
    facit_dc_gain_linear_abs=2.0,
)

REEXAM_F21_Q5 = dict(
    # G(s) = 100*(s+10)/(s-1)  →  LHP zero at -10, RHP pole at +1, DC = 100*10/(-1) = -1000 → 60 dB
    dc_gain_dB=60.0,
    corners=[(1, -20), (10, +20)],                    # pole at 1, zero at 10
    phase_events=[(1, +90), (10, +90)],               # RHP pole: phase RISES; LHP zero: phase RISES
    facit_poles=[+1.0],
    facit_zeros=[-10.0],
    facit_dc_gain_linear_abs=1000.0,
)

# P3: solve_stable_K_range — G as expression string for tf_input.parse_tf
S21_Q4 = dict(G="1 / (s+1)**3", facit_low=0.0, facit_high=8.0)
F22_Q12 = dict(G="1 / (s - 2.5)", facit_low=None, facit_high=None,
               # Documented in solve_F22.m: Nyquist crossing at -0.0222 → K_marginal ≈ 45
               facit_K_marginal=45.0)
REEXAM_F21_Q14 = dict(G="25 / (s**3 + s**2 + 10*s)", facit_low=0.0, facit_high=0.398)
REEXAM_F21_Q16 = dict(G_unstable_marginal=40.5)  # documented K_marginal
