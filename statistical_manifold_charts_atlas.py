from manim import *
import numpy as np

class StatisticalManifoldChartsAtlas(Scene):
    def construct(self):
        # Set up the scene
        title = Text("Charts & Atlas on Statistical Manifold", font_size=32, color=WHITE).to_edge(UP)
        subtitle = Text("Local Coordinate Systems for Probability Distributions", font_size=20, color=BLUE).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        
        # Create coordinate systems
        # Left: Statistical manifold with charts
        left_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=4,
            y_length=4
        )
        left_axes.move_to(LEFT * 3)
        
        # Right: Chart transformations and coordinate systems
        right_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=4,
            y_length=4
        )
        right_axes.move_to(RIGHT * 3)
        
        # Add labels
        left_label = Text("Statistical Manifold\nP(x|θ) with Charts", font_size=18, color=RED).next_to(left_axes, DOWN)
        right_label = Text("Chart Transformations\nφ₁₂ = φ₂ ∘ φ₁⁻¹", font_size=18, color=GREEN).next_to(right_axes, DOWN)
        
        # Show coordinate systems
        self.play(Create(left_axes), Create(right_axes))
        self.play(Write(left_label), Write(right_label))
        self.wait(1)
        
        # Create statistical manifold (space of probability distributions)
        # Each point represents a probability distribution P(x|θ)
        
        # Create coordinate grid
        coord_grid = VGroup()
        
        # Vertical lines (parameter θ₁)
        for x in np.linspace(-2, 2, 9):
            line = Line(
                start=left_axes.c2p(x, -2, 0),
                end=left_axes.c2p(x, 2, 0),
                color=BLUE,
                stroke_width=1
            )
            coord_grid.add(line)
        
        # Horizontal lines (parameter θ₂)
        for y in np.linspace(-2, 2, 9):
            line = Line(
                start=left_axes.c2p(-2, y, 0),
                end=left_axes.c2p(2, y, 0),
                color=RED,
                stroke_width=1
            )
            coord_grid.add(line)
        
        # Show coordinate grid
        self.play(Create(coord_grid))
        self.wait(1)
        
        # Create multiple charts covering the statistical manifold
        # Chart 1: Center region (Normal distributions)
        chart1_center = np.array([0, 0])
        chart1_radius = 1.2
        chart1_circle = Circle(radius=chart1_radius, color=RED, stroke_width=3)
        chart1_circle.move_to(left_axes.c2p(chart1_center[0], chart1_center[1], 0))
        
        # Chart 2: Upper right region (Exponential family)
        chart2_center = np.array([1.2, 1.2])
        chart2_radius = 0.8
        chart2_circle = Circle(radius=chart2_radius, color=GREEN, stroke_width=3)
        chart2_circle.move_to(left_axes.c2p(chart2_center[0], chart2_center[1], 0))
        
        # Chart 3: Lower left region (Gamma distributions)
        chart3_center = np.array([-1.2, -1.2])
        chart3_radius = 0.8
        chart3_circle = Circle(radius=chart3_radius, color=ORANGE, stroke_width=3)
        chart3_circle.move_to(left_axes.c2p(chart3_center[0], chart3_center[1], 0))
        
        # Show charts
        self.play(Create(chart1_circle))
        self.wait(0.5)
        self.play(Create(chart2_circle))
        self.wait(0.5)
        self.play(Create(chart3_circle))
        self.wait(1)
        
        # Add chart labels with statistical interpretation
        chart1_label = Text("Chart 1\n(U₁, φ₁)\nNormal Family", font_size=14, color=RED)
        chart1_label.move_to(left_axes.c2p(0, 0, 0) + UP * 0.4)
        
        chart2_label = Text("Chart 2\n(U₂, φ₂)\nExponential Family", font_size=14, color=GREEN)
        chart2_label.move_to(left_axes.c2p(1.2, 1.2, 0) + UP * 0.4)
        
        chart3_label = Text("Chart 3\n(U₃, φ₃)\nGamma Family", font_size=14, color=ORANGE)
        chart3_label.move_to(left_axes.c2p(-1.2, -1.2, 0) + UP * 0.4)
        
        self.play(Write(chart1_label), Write(chart2_label), Write(chart3_label))
        self.wait(1)
        
        # Show specific probability distributions at chart centers
        # Chart 1: Normal distribution
        normal_text = MathTex(r"P(x|\mu,\sigma) = \frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}", 
                            font_size=12, color=RED)
        normal_text.move_to(left_axes.c2p(0, -1.5, 0))
        
        # Chart 2: Exponential distribution
        exp_text = MathTex(r"P(x|\lambda) = \lambda e^{-\lambda x}", 
                          font_size=12, color=GREEN)
        exp_text.move_to(left_axes.c2p(1.2, -1.5, 0))
        
        # Chart 3: Gamma distribution
        gamma_text = MathTex(r"P(x|k,\theta) = \frac{x^{k-1}e^{-x/\theta}}{\theta^k\Gamma(k)}", 
                           font_size=12, color=ORANGE)
        gamma_text.move_to(left_axes.c2p(-1.2, -1.5, 0))
        
        self.play(Write(normal_text), Write(exp_text), Write(gamma_text))
        self.wait(2)
        
        # Show overlapping regions
        overlap_text = Text("Overlapping regions\nenable smooth transitions", font_size=16, color=YELLOW)
        overlap_text.move_to(ORIGIN + UP * 0.5)
        self.play(Write(overlap_text))
        self.wait(2)
        
        # Show chart transformation
        self.play(FadeOut(overlap_text))
        
        # Create chart transformation visualization
        # Show how coordinates transform between charts
        
        # Create coordinate grid in chart 1 (Normal family)
        chart1_grid = VGroup()
        for x in np.linspace(-0.8, 0.8, 5):
            for y in np.linspace(-0.8, 0.8, 5):
                point = left_axes.c2p(x, y, 0)
                dot = Dot(point=point, color=RED, radius=0.03)
                chart1_grid.add(dot)
        
        # Create transformed grid in chart 2 (Exponential family)
        chart2_grid = VGroup()
        for x in np.linspace(-0.8, 0.8, 5):
            for y in np.linspace(-0.8, 0.8, 5):
                # Transform from normal to exponential family coordinates
                # This is a simplified example transformation
                x2 = x + 1.2
                y2 = y + 1.2
                point = right_axes.c2p(x2, y2, 0)
                dot = Dot(point=point, color=GREEN, radius=0.03)
                chart2_grid.add(dot)
        
        # Show coordinate grids
        self.play(Create(chart1_grid))
        self.wait(1)
        
        # Show transformation arrows
        transformation_arrows = VGroup()
        for i in range(len(chart1_grid)):
            start_point = chart1_grid[i].get_center()
            end_point = chart2_grid[i].get_center()
            arrow = Arrow(start=start_point, end=end_point, color=YELLOW, stroke_width=2)
            transformation_arrows.add(arrow)
        
        self.play(Create(transformation_arrows))
        self.wait(1)
        
        # Show transformed grid
        self.play(Create(chart2_grid))
        self.wait(1)
        
        # Add transformation formula
        transform_formula = MathTex(
            r"\phi_{12} = \phi_2 \circ \phi_1^{-1}",
            font_size=20,
            color=YELLOW
        )
        transform_formula.move_to(right_axes.c2p(0, 1.5, 0))
        
        self.play(Write(transform_formula))
        self.wait(2)
        
        # Show statistical interpretation of charts
        stats_text = VGroup(
            Text("Statistical Interpretation:", font_size=20, color=WHITE),
            Text("• Each chart covers a family of distributions", font_size=16, color=BLUE),
            Text("• Natural parameters θ provide local coordinates", font_size=16, color=GREEN),
            Text("• Chart transitions preserve probability structure", font_size=16, color=YELLOW),
            Text("• Fisher metric is chart-independent", font_size=16, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(transformation_arrows), FadeOut(transform_formula))
        self.play(Write(stats_text))
        self.wait(2)
        
        # Show Fisher metric at different points
        fisher_points = [(-1, -1), (0, 0), (1, 1)]
        fisher_displays = VGroup()
        
        for point in fisher_points:
            x, y = point
            # Simplified Fisher metric for demonstration
            g_11 = 1 + 0.2 * x**2
            g_12 = 0.1 * x * y
            g_22 = 1 + 0.2 * y**2
            
            fisher_text = MathTex(
                f"g = \\begin{{pmatrix}} {g_11:.2f} & {g_12:.2f} \\\\ {g_12:.2f} & {g_22:.2f} \\end{{pmatrix}}",
                font_size=10,
                color=YELLOW
            )
            
            point_pos = left_axes.c2p(x, y, 0)
            fisher_text.move_to(point_pos + UP * 0.6)
            fisher_displays.add(fisher_text)
        
        self.play(*[Write(metric) for metric in fisher_displays])
        self.wait(2)
        
        # Show atlas structure for statistical manifold
        atlas_text = VGroup(
            Text("Atlas A = {(Uᵢ, φᵢ)}ᵢ for Statistical Manifold:", font_size=20, color=WHITE),
            Text("• Charts cover all probability distributions", font_size=16, color=BLUE),
            Text("• Smooth transitions between distribution families", font_size=16, color=GREEN),
            Text("• C^∞ manifold: infinitely differentiable", font_size=16, color=YELLOW),
            Text("• Fisher information provides Riemannian structure", font_size=16, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(stats_text))
        self.play(Write(atlas_text))
        self.wait(2)
        
        # Show information geometry concepts
        info_geo_text = VGroup(
            Text("Information Geometry Concepts:", font_size=20, color=WHITE),
            Text("• Statistical manifold: space of probability distributions", font_size=16, color=BLUE),
            Text("• Fisher metric: g_ij = E[∂ᵢlog p ∂ⱼlog p]", font_size=16, color=GREEN),
            Text("• Natural parameters: canonical coordinates", font_size=16, color=YELLOW),
            Text("• Dual coordinates: expectation parameters", font_size=16, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(atlas_text))
        self.play(Write(info_geo_text))
        self.wait(2)
        
        # Show moving point along a path in the statistical manifold
        # This represents a continuous change of probability distributions
        def distribution_path(t):
            # Path through different distribution families
            x = 1.5 * np.cos(t)
            y = 1.5 * np.sin(t)
            return np.array([x, y])
        
        # Create the path
        t_vals = np.linspace(0, 2*np.pi, 100)
        path_points = [distribution_path(t) for t in t_vals]
        path_coords = [left_axes.c2p(p[0], p[1], 0) for p in path_points]
        
        distribution_path_obj = VMobject()
        distribution_path_obj.set_points_as_corners(path_coords)
        distribution_path_obj.set_color(YELLOW)
        distribution_path_obj.set_stroke(width=3)
        
        # Show the path
        self.play(Create(distribution_path_obj))
        self.wait(1)
        
        # Show moving point along the path
        moving_point = Dot(color=YELLOW, radius=0.08)
        moving_point.move_to(path_coords[0])
        
        self.play(FadeIn(moving_point))
        
        # Animate the point along the path
        self.play(MoveAlongPath(moving_point, distribution_path_obj, run_time=4))
        self.wait(1)
        
        # Final explanation
        final_text = VGroup(
            Text("Charts provide local coordinate systems", font_size=20, color=YELLOW),
            Text("for probability distributions on the statistical manifold", font_size=20, color=YELLOW),
            Text("Atlas ensures complete coverage with smooth transitions", font_size=18, color=BLUE)
        ).arrange(DOWN, buff=0.4).to_edge(DOWN)
        
        self.play(FadeOut(info_geo_text))
        self.play(Write(final_text))
        self.wait(3)
