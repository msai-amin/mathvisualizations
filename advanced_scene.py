from manim import *
import numpy as np

class AdvancedAffineCurves(Scene):
    def construct(self):
        # Set up the coordinate system
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-4, 4, 1],
            x_length=10,
            y_length=8,
            axis_config={"color": BLUE},
            tips=True
        )
        
        # Add coordinate labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        
        # Create multiple affine curves
        
        # 1. Parabola: y = x²
        parabola = axes.plot(
            lambda x: x**2,
            x_range=[-2.5, 2.5],
            color=RED,
            stroke_width=3
        )
        parabola_label = MathTex(r"y = x^2", color=RED).to_corner(UL)
        
        # 2. Ellipse: x²/4 + y² = 1
        t = np.linspace(0, 2*np.pi, 100)
        x_ellipse = 2 * np.cos(t)
        y_ellipse = np.sin(t)
        ellipse_points = [axes.c2p(x, y) for x, y in zip(x_ellipse, y_ellipse)]
        ellipse = VMobject()
        ellipse.set_points_as_corners(ellipse_points)
        ellipse.set_color(GREEN)
        ellipse.set_stroke(width=3)
        ellipse_label = MathTex(r"\frac{x^2}{4} + y^2 = 1", color=GREEN).to_corner(UR)
        
        # 3. Hyperbola: x² - y² = 1
        x_hyperbola = np.linspace(-3, 3, 100)
        y_hyperbola_pos = np.sqrt(x_hyperbola**2 - 1)
        y_hyperbola_neg = -np.sqrt(x_hyperbola**2 - 1)
        
        # Filter out invalid values
        valid_indices = np.where(x_hyperbola**2 >= 1)[0]
        x_valid = x_hyperbola[valid_indices]
        y_pos = y_hyperbola_pos[valid_indices]
        y_neg = y_hyperbola_neg[valid_indices]
        
        hyperbola_pos_points = [axes.c2p(x, y) for x, y in zip(x_valid, y_pos)]
        hyperbola_neg_points = [axes.c2p(x, y) for x, y in zip(x_valid, y_neg)]
        
        hyperbola_pos = VMobject()
        hyperbola_pos.set_points_as_corners(hyperbola_pos_points)
        hyperbola_pos.set_color(PURPLE)
        hyperbola_pos.set_stroke(width=3)
        
        hyperbola_neg = VMobject()
        hyperbola_neg.set_points_as_corners(hyperbola_neg_points)
        hyperbola_neg.set_color(PURPLE)
        hyperbola_neg.set_stroke(width=3)
        
        hyperbola_label = MathTex(r"x^2 - y^2 = 1", color=PURPLE).to_corner(DL)
        
        # 4. Circle: x² + y² = 2
        t_circle = np.linspace(0, 2*np.pi, 100)
        x_circle = np.sqrt(2) * np.cos(t_circle)
        y_circle = np.sqrt(2) * np.sin(t_circle)
        circle_points = [axes.c2p(x, y) for x, y in zip(x_circle, y_circle)]
        circle = VMobject()
        circle.set_points_as_corners(circle_points)
        circle.set_color(ORANGE)
        circle.set_stroke(width=3)
        circle_label = MathTex(r"x^2 + y^2 = 2", color=ORANGE).to_corner(DR)
        
        # Add title
        title = Text("Advanced Affine Curves", font_size=36, color=WHITE).to_edge(UP)
        
        # Animation sequence
        self.play(Write(title))
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)
        
        # Animate curves one by one
        self.play(Create(parabola), Write(parabola_label))
        self.wait(0.5)
        
        self.play(Create(ellipse), Write(ellipse_label))
        self.wait(0.5)
        
        self.play(Create(hyperbola_pos), Create(hyperbola_neg), Write(hyperbola_label))
        self.wait(0.5)
        
        self.play(Create(circle), Write(circle_label))
        self.wait(1)
        
        # Add moving points on each curve
        dot_parabola = Dot(color=YELLOW, radius=0.08)
        dot_ellipse = Dot(color=YELLOW, radius=0.08)
        dot_hyperbola = Dot(color=YELLOW, radius=0.08)
        dot_circle = Dot(color=YELLOW, radius=0.08)
        
        dot_parabola.move_to(axes.c2p(0, 0))
        dot_ellipse.move_to(axes.c2p(2, 0))
        dot_hyperbola.move_to(axes.c2p(1, 0))
        dot_circle.move_to(axes.c2p(np.sqrt(2), 0))
        
        self.play(FadeIn(dot_parabola), FadeIn(dot_ellipse), 
                  FadeIn(dot_hyperbola), FadeIn(dot_circle))
        
        # Animate points moving along curves
        parabola_path = axes.plot(lambda x: x**2, x_range=[-2, 2], color=YELLOW, stroke_width=2)
        ellipse_path = VMobject()
        ellipse_path.set_points_as_corners([axes.c2p(2*np.cos(t), np.sin(t)) for t in np.linspace(0, 2*np.pi, 50)])
        ellipse_path.set_color(YELLOW)
        ellipse_path.set_stroke(width=2)
        
        hyperbola_path = VMobject()
        hyperbola_path.set_points_as_corners([axes.c2p(np.cosh(t), np.sinh(t)) for t in np.linspace(-1.5, 1.5, 50)])
        hyperbola_path.set_color(YELLOW)
        hyperbola_path.set_stroke(width=2)
        
        circle_path = VMobject()
        circle_path.set_points_as_corners([axes.c2p(np.sqrt(2)*np.cos(t), np.sqrt(2)*np.sin(t)) for t in np.linspace(0, 2*np.pi, 50)])
        circle_path.set_color(YELLOW)
        circle_path.set_stroke(width=2)
        
        # Move all points simultaneously
        self.play(
            MoveAlongPath(dot_parabola, parabola_path, run_time=4),
            MoveAlongPath(dot_ellipse, ellipse_path, run_time=4),
            MoveAlongPath(dot_hyperbola, hyperbola_path, run_time=4),
            MoveAlongPath(dot_circle, circle_path, run_time=4)
        )
        
        self.wait(2)
        
        # Add mathematical explanation
        explanation = VGroup(
            Text("Affine curves are curves that can be transformed", font_size=24),
            Text("by linear transformations (rotation, scaling, translation)", font_size=24),
            Text("while preserving their essential geometric properties.", font_size=24)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(Write(explanation))
        self.wait(3)
