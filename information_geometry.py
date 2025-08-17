from manim import *
import numpy as np

class InformationGeometry(Scene):
    def construct(self):
        # Set up the scene
        title = Text("Information Geometry", font_size=36, color=WHITE).to_edge(UP)
        subtitle = Text("Geometry of Probability Distributions", font_size=20, color=BLUE).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        
        # Create coordinate systems
        # Left: Parameter space (statistical manifold)
        left_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=4,
            y_length=4
        )
        left_axes.move_to(LEFT * 3)
        
        # Right: Probability space
        right_axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[0, 1, 0.2],
            x_length=4,
            y_length=4
        )
        right_axes.move_to(RIGHT * 3)
        
        # Add labels
        left_label = Text("Parameter Space\n(θ₁, θ₂)", font_size=18, color=RED).next_to(left_axes, DOWN)
        right_label = Text("Probability Space\n(p₁, p₂)", font_size=18, color=GREEN).next_to(right_axes, DOWN)
        
        # Create Fisher information metric visualization
        # The Fisher metric varies with position in parameter space
        fisher_metrics = VGroup()
        positions = [(-1, -1), (0, 0), (1, 1), (-1, 1), (1, -1)]
        
        for pos in positions:
            x, y = pos
            # Fisher metric components (example for normal distribution)
            # g_11 = 1/σ², g_22 = 2/σ², g_12 = 0
            sigma = 1 + 0.3 * np.sqrt(x**2 + y**2)  # σ varies with position
            g_11 = 1 / (sigma**2)
            g_22 = 2 / (sigma**2)
            g_12 = 0
            
            metric_text = MathTex(
                f"g = \\begin{{pmatrix}} {g_11:.2f} & {g_12:.2f} \\\\ {g_12:.2f} & {g_22:.2f} \\end{{pmatrix}}",
                font_size=12,
                color=YELLOW
            )
            metric_text.move_to(left_axes.c2p(x, y, 0) + UP * 0.3)
            fisher_metrics.add(metric_text)
        
        # Create coordinate grid for parameter space
        param_grid = VGroup()
        
        # Vertical lines
        for x in np.linspace(-2, 2, 9):
            line = Line(
                start=left_axes.c2p(x, -2, 0),
                end=left_axes.c2p(x, 2, 0),
                color=BLUE,
                stroke_width=1
            )
            param_grid.add(line)
        
        # Horizontal lines
        for y in np.linspace(-2, 2, 9):
            line = Line(
                start=left_axes.c2p(-2, y, 0),
                end=left_axes.c2p(2, y, 0),
                color=RED,
                stroke_width=1
            )
            param_grid.add(line)
        
        # Create probability simplex (2D case)
        simplex = Polygon(
            right_axes.c2p(0, 0, 0),
            right_axes.c2p(1, 0, 0),
            right_axes.c2p(0.5, 0.866, 0),
            color=GREEN,
            stroke_width=3,
            fill_opacity=0.2
        )
        
        # Add simplex labels
        simplex_labels = VGroup(
            Text("(0,0)", font_size=14).move_to(right_axes.c2p(0, 0, 0) + DOWN * 0.2),
            Text("(1,0)", font_size=14).move_to(right_axes.c2p(1, 0, 0) + DOWN * 0.2),
            Text("(0,1)", font_size=14).move_to(right_axes.c2p(0.5, 0.866, 0) + UP * 0.2)
        )
        
        # Show coordinate systems
        self.play(Create(left_axes), Create(right_axes))
        self.play(Write(left_label), Write(right_label))
        self.wait(1)
        
        # Show parameter grid
        self.play(Create(param_grid))
        self.wait(1)
        
        # Show Fisher metrics
        self.play(*[Write(metric) for metric in fisher_metrics])
        self.wait(2)
        
        # Show probability simplex
        self.play(Create(simplex))
        self.play(*[Write(label) for label in simplex_labels])
        self.wait(1)
        
        # Create geodesic curves in parameter space
        def geodesic_curve(t):
            # A geodesic with respect to the Fisher metric
            theta1 = 1.5 * np.cos(t)
            theta2 = 1.5 * np.sin(t)
            return np.array([theta1, theta2])
        
        geodesic_path = ParametricFunction(
            lambda t: left_axes.c2p(*geodesic_curve(t), 0),
            t_range=[0, 2*np.pi],
            color=YELLOW,
            stroke_width=4
        )
        
        # Create corresponding curve in probability space
        def probability_curve(t):
            # Transform parameters to probabilities (example transformation)
            theta1, theta2 = geodesic_curve(t)
            # Simple transformation: p1 = sigmoid(theta1), p2 = sigmoid(theta2)
            p1 = 1 / (1 + np.exp(-theta1))
            p2 = 1 / (1 + np.exp(-theta2))
            return np.array([p1, p2])
        
        prob_path = ParametricFunction(
            lambda t: right_axes.c2p(*probability_curve(t), 0),
            t_range=[0, 2*np.pi],
            color=YELLOW,
            stroke_width=4
        )
        
        # Show geodesics
        self.play(Create(geodesic_path), Create(prob_path))
        self.wait(1)
        
        # Add information geometry explanation
        explanation = VGroup(
            Text("Information Geometry Concepts:", font_size=20, color=WHITE),
            Text("• Fisher Information Metric: g_ij = E[∂ᵢlog p ∂ⱼlog p]", font_size=16, color=YELLOW),
            Text("• Statistical Manifold: Space of probability distributions", font_size=16, color=BLUE),
            Text("• Geodesics: Shortest paths in information space", font_size=16, color=GREEN),
            Text("• Kullback-Leibler divergence: Distance between distributions", font_size=16, color=RED)
        ).arrange(DOWN, buff=0.2).to_edge(DOWN)
        
        self.play(Write(explanation))
        self.wait(2)
        
        # Show moving points along geodesics
        moving_point_param = Dot(color=YELLOW, radius=0.08)
        # Position at the start of the geodesic path
        start_point = geodesic_curve(0)
        moving_point_param.move_to(left_axes.c2p(*start_point, 0))
        
        moving_point_prob = Dot(color=YELLOW, radius=0.08)
        # Position at the start of the probability path
        start_prob = probability_curve(0)
        moving_point_prob.move_to(right_axes.c2p(*start_prob, 0))
        
        self.play(FadeIn(moving_point_param), FadeIn(moving_point_prob))
        
        # Animate points
        self.play(
            MoveAlongPath(moving_point_param, geodesic_path, run_time=4),
            MoveAlongPath(moving_point_prob, prob_path, run_time=4)
        )
        self.wait(1)
        
        # Show Kullback-Leibler divergence
        kl_text = VGroup(
            Text("Kullback-Leibler Divergence:", font_size=20, color=ORANGE),
            Text("D_KL(P||Q) = ∫ p(x) log(p(x)/q(x)) dx", font_size=16, color=YELLOW),
            Text("Measures information loss when Q approximates P", font_size=16, color=WHITE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(explanation))
        self.play(Write(kl_text))
        self.wait(3)
        
        # Final explanation
        final_text = VGroup(
            Text("Information geometry reveals the deep connection", font_size=20, color=YELLOW),
            Text("between probability theory and differential geometry", font_size=20, color=YELLOW),
            Text("Applications: Machine Learning, Statistics, Physics", font_size=18, color=BLUE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(kl_text))
        self.play(Write(final_text))
        self.wait(3)
