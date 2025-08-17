from manim import *
import numpy as np

class StatisticalManifolds(Scene):
    def construct(self):
        # Set up the scene
        title = Text("Statistical Manifolds & Exponential Families", font_size=32, color=WHITE).to_edge(UP)
        subtitle = Text("Geometry of Statistical Inference", font_size=20, color=BLUE).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        
        # Create coordinate systems
        # Left: Natural parameters (canonical coordinates)
        left_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4,
            y_length=4
        )
        left_axes.move_to(LEFT * 3)
        
        # Right: Expectation parameters (dual coordinates)
        right_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=4,
            y_length=4
        )
        right_axes.move_to(RIGHT * 3)
        
        # Add labels
        left_label = Text("Natural Parameters\n(η₁, η₂)", font_size=18, color=RED).next_to(left_axes, DOWN)
        right_label = Text("Expectation Parameters\n(μ₁, μ₂)", font_size=18, color=GREEN).next_to(right_axes, DOWN)
        
        # Create exponential family manifold
        # Example: 2D Gaussian with varying parameters
        def exponential_family_manifold(eta1, eta2):
            # Natural parameters to expectation parameters
            # For Gaussian: μ = -η/2, σ² = 1/(2η)
            mu1 = -eta1 / 2
            mu2 = -eta2 / 2
            return np.array([mu1, mu2])
        
        # Create coordinate grid in natural parameter space
        natural_grid = VGroup()
        
        # Vertical lines
        for eta1 in np.linspace(-3, 3, 7):
            line = Line(
                start=left_axes.c2p(eta1, -3, 0),
                end=left_axes.c2p(eta1, 3, 0),
                color=BLUE,
                stroke_width=1
            )
            natural_grid.add(line)
        
        # Horizontal lines
        for eta2 in np.linspace(-3, 3, 7):
            line = Line(
                start=left_axes.c2p(-3, eta2, 0),
                end=left_axes.c2p(3, eta2, 0),
                color=RED,
                stroke_width=1
            )
            natural_grid.add(line)
        
        # Create dual grid in expectation parameter space
        expectation_grid = VGroup()
        
        # Transform grid points
        for eta1 in np.linspace(-3, 3, 7):
            for eta2 in np.linspace(-3, 3, 7):
                mu1, mu2 = exponential_family_manifold(eta1, eta2)
                if -2 <= mu1 <= 2 and -2 <= mu2 <= 2:
                    point = Dot(
                        point=right_axes.c2p(mu1, mu2, 0),
                        color=YELLOW,
                        radius=0.02
                    )
                    expectation_grid.add(point)
        
        # Show coordinate systems
        self.play(Create(left_axes), Create(right_axes))
        self.play(Write(left_label), Write(right_label))
        self.wait(1)
        
        # Show natural parameter grid
        self.play(Create(natural_grid))
        self.wait(1)
        
        # Show expectation parameter grid (dual coordinates)
        self.play(Create(expectation_grid))
        self.wait(1)
        
        # Create geodesic curves in natural parameter space
        def natural_geodesic(t):
            # A geodesic with respect to the Fisher metric
            eta1 = 2 * np.cos(t)
            eta2 = 2 * np.sin(t)
            return np.array([eta1, eta2])
        
        natural_path = ParametricFunction(
            lambda t: left_axes.c2p(*natural_geodesic(t), 0),
            t_range=[0, 2*np.pi],
            color=YELLOW,
            stroke_width=4
        )
        
        # Transform to expectation parameters
        def expectation_geodesic(t):
            eta1, eta2 = natural_geodesic(t)
            mu1, mu2 = exponential_family_manifold(eta1, eta2)
            return np.array([mu1, mu2])
        
        expectation_path = ParametricFunction(
            lambda t: right_axes.c2p(*expectation_geodesic(t), 0),
            t_range=[0, 2*np.pi],
            color=YELLOW,
            stroke_width=4
        )
        
        # Show geodesics
        self.play(Create(natural_path), Create(expectation_path))
        self.wait(1)
        
        # Create Fisher information metric at different points
        fisher_metrics = VGroup()
        positions = [(-2, -2), (0, 0), (2, 2), (-2, 2), (2, -2)]
        
        for pos in positions:
            eta1, eta2 = pos
            # Fisher metric for exponential family
            # g_ij = ∂²ψ/∂ηᵢ∂ηⱼ where ψ is the log partition function
            # For Gaussian: ψ = (η₁² + η₂²)/4
            g_11 = 0.5  # ∂²ψ/∂η₁²
            g_22 = 0.5  # ∂²ψ/∂η₂²
            g_12 = 0    # ∂²ψ/∂η₁∂η₂
            
            metric_text = MathTex(
                f"g = \\begin{{pmatrix}} {g_11:.1f} & {g_12:.1f} \\\\ {g_12:.1f} & {g_22:.1f} \\end{{pmatrix}}",
                font_size=10,
                color=ORANGE
            )
            metric_text.move_to(left_axes.c2p(eta1, eta2, 0) + UP * 0.3)
            fisher_metrics.add(metric_text)
        
        # Show Fisher metrics
        self.play(*[Write(metric) for metric in fisher_metrics])
        self.wait(2)
        
        # Add statistical manifold explanation
        explanation = VGroup(
            Text("Statistical Manifold Structure:", font_size=20, color=WHITE),
            Text("• Natural Parameters (η): Canonical coordinates", font_size=16, color=RED),
            Text("• Expectation Parameters (μ): Dual coordinates", font_size=16, color=GREEN),
            Text("• Fisher Metric: g_ij = ∂²ψ/∂ηᵢ∂ηⱼ", font_size=16, color=YELLOW),
            Text("• Exponential Family: p(x|η) = exp(η·T(x) - ψ(η))", font_size=16, color=BLUE)
        ).arrange(DOWN, buff=0.2).to_edge(DOWN)
        
        self.play(Write(explanation))
        self.wait(2)
        
        # Show moving points along geodesics
        moving_point_natural = Dot(color=YELLOW, radius=0.08)
        # Position at the start of the natural geodesic path
        start_natural = natural_geodesic(0)
        moving_point_natural.move_to(left_axes.c2p(*start_natural, 0))
        
        moving_point_expectation = Dot(color=YELLOW, radius=0.08)
        # Position at the start of the expectation geodesic path
        start_expectation = expectation_geodesic(0)
        moving_point_expectation.move_to(right_axes.c2p(*start_expectation, 0))
        
        self.play(FadeIn(moving_point_natural), FadeIn(moving_point_expectation))
        
        # Animate points
        self.play(
            MoveAlongPath(moving_point_natural, natural_path, run_time=4),
            MoveAlongPath(moving_point_expectation, expectation_path, run_time=4)
        )
        self.wait(1)
        
        # Show Legendre transformation
        legendre_text = VGroup(
            Text("Legendre Transformation:", font_size=20, color=ORANGE),
            Text("ψ(η) + φ(μ) = η·μ", font_size=16, color=YELLOW),
            Text("φ(μ) = sup_η {η·μ - ψ(η)}", font_size=16, color=WHITE),
            Text("Connects natural and expectation parameters", font_size=16, color=BLUE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(explanation))
        self.play(Write(legendre_text))
        self.wait(3)
        
        # Show applications
        applications_text = VGroup(
            Text("Applications of Information Geometry:", font_size=20, color=YELLOW),
            Text("• Machine Learning: Natural gradient descent", font_size=16, color=WHITE),
            Text("• Statistics: Maximum likelihood estimation", font_size=16, color=WHITE),
            Text("• Physics: Thermodynamics, quantum mechanics", font_size=16, color=WHITE),
            Text("• Neuroscience: Neural coding and information processing", font_size=16, color=WHITE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(legendre_text))
        self.play(Write(applications_text))
        self.wait(3)
        
        # Final explanation
        final_text = VGroup(
            Text("Information geometry provides the mathematical foundation", font_size=20, color=YELLOW),
            Text("for understanding the geometry of probability distributions", font_size=20, color=YELLOW),
            Text("and the optimal ways to learn from data", font_size=18, color=BLUE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(applications_text))
        self.play(Write(final_text))
        self.wait(3)
