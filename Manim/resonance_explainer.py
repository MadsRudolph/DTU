"""
Small Manim explainer: a driven mass-spring-damper, its resonance, and the
impedance analogy to a series RLC circuit (34870 style, M_M / C_M / R_M).

Render (from this folder):
    .venv/bin/manim -pql resonance_explainer.py ResonanceExplainer   # fast 480p preview
    .venv/bin/manim -pqh resonance_explainer.py ResonanceExplainer   # 1080p final
    .venv/bin/manim -s -ql resonance_explainer.py ResonanceExplainer # last frame as PNG only

Each part of the video is its own method below (intro, oscillator, resonance,
analogy, outro), so you can comment parts out in construct() while editing.
"""

from manim import *
import numpy as np

# ---------------------------------------------------------------------------
# Knobs to play with
# ---------------------------------------------------------------------------
M_M = 1.0    # moving mass [kg]
K = 40.0     # spring stiffness [N/m]  (C_M = 1/K)
R_M = 1.2    # mechanical resistance [N s/m]

W0 = np.sqrt(K / M_M)        # resonance [rad/s]
Q = W0 * M_M / R_M           # quality factor

MASS_COLOR = BLUE
SPRING_COLOR = GREEN
DAMPER_COLOR = ORANGE
CURVE_COLOR = YELLOW

config.background_color = "#14161b"


# ---------------------------------------------------------------------------
# Small drawing helpers
# ---------------------------------------------------------------------------
def zigzag(start, end, teeth=8, amp=0.18, lead=0.2):
    """Zigzag between two points: used for both the spring and the resistor."""
    start, end = np.array(start, float), np.array(end, float)
    d = end - start
    length = np.linalg.norm(d)
    u = d / length
    n = np.array([-u[1], u[0], 0])
    pts = [start, start + lead * u]
    for i in range(1, 2 * teeth):
        s = lead + (length - 2 * lead) * i / (2 * teeth)
        pts.append(start + s * u + amp * (1 if i % 2 else -1) * n)
    pts += [end - lead * u, end]
    return VMobject().set_points_as_corners(pts)


def inductor(start, end, loops=4):
    start, end = np.array(start, float), np.array(end, float)
    lead = 0.2
    r = (np.linalg.norm(end - start) - 2 * lead) / (2 * loops)
    g = VGroup(Line(start, start + RIGHT * lead))
    x = start + RIGHT * lead
    for _ in range(loops):
        g.add(Arc(radius=r, start_angle=PI, angle=-PI, arc_center=x + RIGHT * r))
        x = x + RIGHT * 2 * r
    g.add(Line(x, end))
    return g


def capacitor(start, end, gap=0.14, h=0.5):
    start, end = np.array(start, float), np.array(end, float)
    mid = (start + end) / 2
    return VGroup(
        Line(start, mid + LEFT * gap / 2),
        Line(mid + LEFT * gap / 2 + UP * h / 2, mid + LEFT * gap / 2 + DOWN * h / 2),
        Line(mid + RIGHT * gap / 2 + UP * h / 2, mid + RIGHT * gap / 2 + DOWN * h / 2),
        Line(mid + RIGHT * gap / 2, end),
    )


def dashpot(start, end, w=0.4):
    """Mechanical damper: a cup with a piston in it."""
    start, end = np.array(start, float), np.array(end, float)
    mid = (start + end) / 2
    cup = VMobject().set_points_as_corners([
        mid + RIGHT * 0.25 + UP * w / 2,
        mid + LEFT * 0.25 + UP * w / 2,
        mid + LEFT * 0.25 + DOWN * w / 2,
        mid + RIGHT * 0.25 + DOWN * w / 2,
    ])
    piston = Line(mid + UP * w * 0.35, mid + DOWN * w * 0.35)
    return VGroup(Line(start, mid + LEFT * 0.25), cup, piston, Line(mid, end))


def mobility(u):
    """|v/F| normalised to 1 at resonance, as a function of u = omega/omega0."""
    return 1 / np.sqrt(1 + Q**2 * (u - 1 / u) ** 2)


# ---------------------------------------------------------------------------
# The video
# ---------------------------------------------------------------------------
class ResonanceExplainer(Scene):
    def construct(self):
        self.intro()
        self.oscillator()
        self.resonance()
        self.analogy()
        self.outro()

    # 1 ---------------------------------------------------------------------
    def intro(self):
        title = Text("Why does a loudspeaker resonate?", font_size=44)
        sub = Text("mass + spring + friction = RLC", font_size=28, color=GRAY_B)
        sub.next_to(title, DOWN, buff=0.4)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.3))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(sub))

    # 2 ---------------------------------------------------------------------
    def oscillator(self):
        wall = VGroup(
            Line(UP * 1, DOWN * 1),
            *[Line(UP * y, UP * y + LEFT * 0.25 + DOWN * 0.25) for y in np.linspace(1, -0.75, 8)],
        ).move_to(LEFT * 5 + UP * 1.2)
        wall_x = wall[0].get_center()[0]

        t = ValueTracker(0)
        rest_x = -1.0

        def mass_x():
            return rest_x + 0.8 * np.sin(2.5 * t.get_value())

        mass = always_redraw(lambda: VGroup(
            Square(1.2, fill_color=MASS_COLOR, fill_opacity=0.8, stroke_color=WHITE),
            MathTex("M_M", font_size=36),
        ).move_to([mass_x(), 1.2, 0]))
        spring = always_redraw(lambda: zigzag(
            [wall_x, 1.55, 0], [mass_x() - 0.6, 1.55, 0]).set_stroke(SPRING_COLOR, 4))
        damper = always_redraw(lambda: dashpot(
            [wall_x, 0.85, 0], [mass_x() - 0.6, 0.85, 0]).set_stroke(DAMPER_COLOR, 4))
        def force_arrow():
            # Arrow floats right of the mass and flips with the sign of F(t)
            c = mass_x() + 1.5
            half = 0.6 * np.cos(2.5 * t.get_value())
            half = half if abs(half) > 0.05 else 0.05
            return Arrow([c - half, 1.2, 0], [c + half, 1.2, 0], buff=0, color=RED,
                         max_tip_length_to_length_ratio=0.35)

        force = always_redraw(force_arrow)
        f_label = always_redraw(lambda: MathTex("F", color=RED).next_to(force, UP, buff=0.1))

        labels = VGroup(
            MathTex("C_M = 1/k", color=SPRING_COLOR, font_size=32).move_to([-3.6, 2.3, 0]),
            MathTex("R_M", color=DAMPER_COLOR, font_size=32).move_to([-3.6, 0.1, 0]),
        )

        self.play(Create(wall), FadeIn(mass), Create(spring), Create(damper))
        self.play(FadeIn(labels), GrowArrow(force), FadeIn(f_label))
        self.add(force, f_label)

        eq = MathTex(
            r"M_M\,\ddot{x}", "+", r"R_M\,\dot{x}", "+", r"\frac{1}{C_M}\,x", "=", "F(t)",
            font_size=42,
        ).to_edge(DOWN, buff=1.2)
        eq[0].set_color(MASS_COLOR)
        eq[2].set_color(DAMPER_COLOR)
        eq[4].set_color(SPRING_COLOR)
        eq[6].set_color(RED)

        self.play(t.animate.set_value(2 * PI / 2.5), Write(eq), run_time=3, rate_func=linear)
        self.play(t.animate.set_value(4 * PI / 2.5), run_time=2.5, rate_func=linear)

        self.oscillator_eq = eq
        self.play(*[FadeOut(m) for m in [wall, mass, spring, damper, force, f_label, labels]],
                  eq.animate.to_edge(UP, buff=0.4).scale(0.8))

    # 3 ---------------------------------------------------------------------
    def resonance(self):
        axes = Axes(
            x_range=[0, 2.05, 0.5], y_range=[0, 1.15, 0.5],
            x_length=8, y_length=4.2,
            axis_config={"include_tip": False, "color": GRAY_B},
            x_axis_config={"numbers_to_include": [0.5, 1, 1.5, 2]},
        ).shift(DOWN * 0.6)
        x_lab = MathTex(r"\omega/\omega_0", font_size=30).next_to(axes.x_axis, DOWN, buff=0.4)
        y_lab = MathTex(r"|v/F|", font_size=30).next_to(axes.y_axis, UP, buff=0.15)
        curve = axes.plot(mobility, x_range=[0.05, 2.0, 0.005], color=CURVE_COLOR, stroke_width=4)

        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab))
        self.play(Create(curve), run_time=2)

        u = ValueTracker(0.2)
        dot = always_redraw(lambda: Dot(axes.c2p(u.get_value(), mobility(u.get_value())), color=RED))
        readout = always_redraw(lambda: VGroup(
            MathTex(r"\omega/\omega_0 =", font_size=30),
            DecimalNumber(u.get_value(), num_decimal_places=2, font_size=30),
        ).arrange(RIGHT, buff=0.15).to_corner(UR, buff=0.6).shift(DOWN * 0.8))
        self.play(FadeIn(dot), FadeIn(readout))
        self.play(u.animate.set_value(1.0), run_time=2.5)

        peak_line = DashedLine(axes.c2p(1, 0), axes.c2p(1, 1.1), color=GRAY_A)
        f0 = MathTex(r"f_0 = \frac{1}{2\pi\sqrt{M_M C_M}}", font_size=34)
        f0.next_to(axes.c2p(1, 1.0), RIGHT, buff=0.4)
        box = SurroundingRectangle(f0, color=CURVE_COLOR, buff=0.15)
        self.play(Create(peak_line), Write(f0), Create(box))
        self.wait(0.5)

        note = Tex(r"mass and spring cancel:\\only $R_M$ is left", font_size=30, color=GRAY_B)
        note.move_to(axes.c2p(0.5, 0.75))
        self.play(FadeIn(note, shift=UP * 0.2))
        self.play(u.animate.set_value(1.9), run_time=2)
        self.wait(0.5)

        self.play(*[FadeOut(m) for m in
                    [axes, x_lab, y_lab, curve, dot, readout, peak_line, f0, box, note]])

    # 4 ---------------------------------------------------------------------
    def analogy(self):
        rows = [
            (Square(0.6, fill_color=MASS_COLOR, fill_opacity=0.8, stroke_color=WHITE), "M_M",
             inductor(LEFT * 0.7, RIGHT * 0.7), "L", MASS_COLOR),
            (zigzag(LEFT * 0.7, RIGHT * 0.7, teeth=5).set_stroke(width=4), "C_M",
             capacitor(LEFT * 0.7, RIGHT * 0.7), "C", SPRING_COLOR),
            (dashpot(LEFT * 0.7, RIGHT * 0.7).set_stroke(width=4), "R_M",
             zigzag(LEFT * 0.7, RIGHT * 0.7, teeth=4, amp=0.15).set_stroke(width=4), "R", DAMPER_COLOR),
        ]
        table = VGroup()
        for mech, mlab, elec, elab, col in rows:
            mech.set_color(col)
            elec.set_color(col)
            row = VGroup(
                VGroup(mech, MathTex(mlab, font_size=34)).arrange(RIGHT, buff=0.35),
                Arrow(LEFT * 0.6, RIGHT * 0.6, color=GRAY_B),
                VGroup(elec, MathTex(elab, font_size=34)).arrange(RIGHT, buff=0.35),
            ).arrange(RIGHT, buff=0.6)
            table.add(row)
        table.arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(DOWN * 0.3)
        for row in table:
            row[1].move_to([0, row.get_center()[1], 0])
            row[0].next_to(row[1], LEFT, buff=0.6)
            row[2].next_to(row[1], RIGHT, buff=0.6)

        heads = VGroup(
            Text("mechanical", font_size=26, color=GRAY_B).next_to(table[0][0], UP, buff=0.5),
            Text("electrical", font_size=26, color=GRAY_B).next_to(table[0][2], UP, buff=0.5),
        )
        self.play(FadeIn(heads))
        for row in table:
            self.play(FadeIn(row[0]), GrowArrow(row[1]), run_time=0.6)
            self.play(TransformFromCopy(row[0], row[2]), run_time=0.9)
        self.wait(0.5)

        z_eq = MathTex(
            r"Z_M = R_M + j\omega M_M + \frac{1}{j\omega C_M}", r"\;\leftrightarrow\;",
            r"Z_E = R + j\omega L + \frac{1}{j\omega C}", font_size=28,
        ).to_edge(DOWN, buff=0.5)
        self.play(TransformMatchingShapes(self.oscillator_eq, z_eq[0]), run_time=1.5)
        self.play(Write(z_eq[1:]))
        self.wait(1.5)
        self.play(FadeOut(table), FadeOut(heads), FadeOut(z_eq))

    # 5 ---------------------------------------------------------------------
    def outro(self):
        msg = Text("Same equation, same resonance.", font_size=40)
        sub = Text("Solve the circuit, and you have solved the speaker.", font_size=26, color=GRAY_B)
        VGroup(msg, sub).arrange(DOWN, buff=0.4)
        self.play(Write(msg))
        self.play(FadeIn(sub, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(msg), FadeOut(sub))
