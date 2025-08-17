from manim import *
import numpy as np

class AffineCurves(Scene):
    def construct(self):
        # Set up the coordinate system
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": BLUE},
            tips=True
        )
        
        # Add coordinate labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        
        # Create the first affine curve: y = x² (parabola)
        parabola = axes.plot(
            lambda x: x**2,
            x_range=[-2, 2],
            color=RED,
            stroke_width=3
        )
        parabola_label = MathTex(r"y = x^2", color=RED).to_corner(UL)
        
        # Create the second affine curve: x²/4 + y² = 1 (ellipse)
        ellipse = axes.plot_implicit_curve(
            lambda x, y: x**2/4 + y**2 - 1,
            x_range=[-2.5, 2.5],
            y_range=[-1.5, 1.5],
            color=GREEN,
            stroke_width=3
        )
        ellipse_label = MathTex(r"\frac{x^2}{4} + y^2 = 1", color=GREEN).to_corner(UR)
        
        # Add title
        title = Text("Affine Curves", font_size=36, color=WHITE).to_edge(UP)
        
        # Animation sequence
        self.play(Write(title))
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)
        
        # Animate first curve
        self.play(Create(parabola), Write(parabola_label))
        self.wait(1)
        
        # Animate second curve
        self.play(Create(ellipse), Write(ellipse_label))
        self.wait(1)
        
        # Add some interactive elements
        # Create a moving point on the parabola
        dot_parabola = Dot(color=YELLOW, radius=0.08)
        dot_parabola.move_to(axes.c2p(0, 0))
        
        # Create a moving point on the ellipse
        dot_ellipse = Dot(color=ORANGE, radius=0.08)
        dot_ellipse.move_to(axes.c2p(2, 0))
        
        self.play(FadeIn(dot_parabola), FadeIn(dot_ellipse))
        
        # Animate the points moving along the curves
        parabola_path = axes.plot(lambda x: x**2, x_range=[-1.5, 1.5], color=YELLOW, stroke_width=2)
        ellipse_path = axes.plot_implicit_curve(
            lambda x, y: x**2/4 + y**2 - 1,
            x_range=[-2, 2],
            y_range=[-1, 1],
            color=ORANGE,
            stroke_width=2
        )
        
        # Move points along the curves
        self.play(
            MoveAlongPath(dot_parabola, parabola_path, run_time=3),
            MoveAlongPath(dot_ellipse, ellipse_path, run_time=3)
        )
        
        self.wait(2)
