from manim import *
import numpy as np

class FisherMetricDetailed(Scene):
    def construct(self):
        # Set up the scene
        title = Text("Detailed Fisher Metric Analysis", font_size=32, color=WHITE).to_edge(UP)
        subtitle = Text("Probability Densities & Metric Evolution", font_size=20, color=BLUE).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        
        # Create coordinate systems
        # Left: Parameter space with Fisher metric
        left_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[0.1, 1.5, 0.2],
            x_length=4,
            y_length=4
        )
        left_axes.move_to(LEFT * 3)
        
        # Right: Probability density functions
        right_axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 2, 0.5],
            x_length=4,
            y_length=4
        )
        right_axes.move_to(RIGHT * 3)
        
        # Add labels
        left_label = Text("Parameter Space\n(μ, σ)", font_size=20, color=RED).next_to(left_axes, DOWN)
        right_label = Text("Probability Density\np(x|μ,σ)", font_size=20, color=GREEN).next_to(right_axes, DOWN)
        
        # Create coordinate grid
        param_grid = VGroup()
        
        # Vertical lines (μ)
        for x in np.linspace(-2, 2, 9):
            line = Line(
                start=left_axes.c2p(x, 0.1, 0),
                end=left_axes.c2p(x, 1.5, 0),
                color=BLUE,
                stroke_width=1
            )
            param_grid.add(line)
        
        # Horizontal lines (σ)
        for y in np.linspace(0.1, 1.5, 8):
            line = Line(
                start=left_axes.c2p(-2, y, 0),
                end=left_axes.c2p(2, y, 0),
                color=RED,
                stroke_width=1
            )
            param_grid.add(line)
        
        # Show coordinate systems
        self.play(Create(left_axes), Create(right_axes))
        self.play(Write(left_label), Write(right_label))
        self.wait(1)
        
        # Show parameter grid
        self.play(Create(param_grid))
        self.wait(1)
        
        # Create two specific probability distributions
        # Distribution 1: Normal with parameters (μ₁, σ₁)
        dist1_params = np.array([-1.0, 0.4])  # (μ₁, σ₁)
        dist1_point = left_axes.c2p(dist1_params[0], dist1_params[1], 0)
        
        # Distribution 2: Normal with parameters (μ₂, σ₂)
        dist2_params = np.array([1.0, 0.8])   # (μ₂, σ₂)
        dist2_point = left_axes.c2p(dist2_params[0], dist2_params[1], 0)
        
        # Create points for the distributions
        dist1_dot = Dot(point=dist1_point, color=RED, radius=0.1)
        dist2_dot = Dot(point=dist2_point, color=BLUE, radius=0.1)
        
        # Add labels for the distributions
        dist1_label = Text("P₁(μ₁=-1, σ₁=0.4)", font_size=16, color=RED)
        dist1_label.move_to(dist1_point + UP * 0.4)
        
        dist2_label = Text("P₂(μ₂=1, σ₂=0.8)", font_size=16, color=BLUE)
        dist2_label.move_to(dist2_point + UP * 0.4)
        
        # Show the two distributions
        self.play(FadeIn(dist1_dot), FadeIn(dist2_dot))
        self.play(Write(dist1_label), Write(dist2_label))
        self.wait(1)
        
        # Create Fisher metric function
        def fisher_metric_normal(mu, sigma):
            # For normal distribution N(μ, σ²):
            # g_11 = 1/σ² (variance of μ)
            # g_22 = 2/σ² (variance of σ)
            # g_12 = g_21 = 0 (no correlation)
            g_11 = 1 / (sigma**2)
            g_22 = 2 / (sigma**2)
            g_12 = 0
            return np.array([[g_11, g_12], [g_12, g_22]])
        
        # Compute Fisher metrics
        G1 = fisher_metric_normal(dist1_params[0], dist1_params[1])
        G2 = fisher_metric_normal(dist2_params[0], dist2_params[1])
        
        # Display Fisher metrics
        metric1_text = MathTex(
            f"G_1 = \\begin{{pmatrix}} {G1[0,0]:.2f} & {G1[0,1]:.2f} \\\\ {G1[1,0]:.2f} & {G1[1,1]:.2f} \\end{{pmatrix}}",
            font_size=12,
            color=RED
        )
        metric1_text.move_to(dist1_point + DOWN * 0.5)
        
        metric2_text = MathTex(
            f"G_2 = \\begin{{pmatrix}} {G2[0,0]:.2f} & {G2[0,1]:.2f} \\\\ {G2[1,0]:.2f} & {G2[1,1]:.2f} \\end{{pmatrix}}",
            font_size=12,
            color=BLUE
        )
        metric2_text.move_to(dist2_point + DOWN * 0.5)
        
        self.play(Write(metric1_text), Write(metric2_text))
        self.wait(2)
        
        # Create probability density functions
        def normal_pdf(x, mu, sigma):
            return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma)**2)
        
        # Plot distribution 1
        x_vals = np.linspace(-4, 4, 200)
        y1_vals = [normal_pdf(x, dist1_params[0], dist1_params[1]) for x in x_vals]
        points1 = [right_axes.c2p(x, y, 0) for x, y in zip(x_vals, y1_vals)]
        
        pdf1 = VMobject()
        pdf1.set_points_as_corners(points1)
        pdf1.set_color(RED)
        pdf1.set_stroke(width=3)
        
        # Plot distribution 2
        y2_vals = [normal_pdf(x, dist2_params[0], dist2_params[1]) for x in x_vals]
        points2 = [right_axes.c2p(x, y, 0) for x, y in zip(x_vals, y2_vals)]
        
        pdf2 = VMobject()
        pdf2.set_points_as_corners(points2)
        pdf2.set_color(BLUE)
        pdf2.set_stroke(width=3)
        
        # Show probability density functions
        self.play(Create(pdf1))
        self.wait(0.5)
        self.play(Create(pdf2))
        self.wait(1)
        
        # Create a path between the two distributions
        def geodesic_path(t):
            # Linear interpolation in parameter space
            mu = dist1_params[0] + t * (dist2_params[0] - dist1_params[0])
            sigma = dist1_params[1] + t * (dist2_params[1] - dist1_params[1])
            return np.array([mu, sigma])
        
        # Create the path
        path_points = [geodesic_path(t) for t in np.linspace(0, 1, 50)]
        path_coords = [left_axes.c2p(p[0], p[1], 0) for p in path_points]
        
        geodesic_path_obj = VMobject()
        geodesic_path_obj.set_points_as_corners(path_coords)
        geodesic_path_obj.set_color(YELLOW)
        geodesic_path_obj.set_stroke(width=3)
        
        # Show the geodesic path
        self.play(Create(geodesic_path_obj))
        self.wait(1)
        
        # Show how the probability density evolves along the path
        # Create intermediate distributions
        intermediate_pdfs = []
        sample_times = [0.25, 0.5, 0.75]
        
        for t in sample_times:
            params = geodesic_path(t)
            y_vals = [normal_pdf(x, params[0], params[1]) for x in x_vals]
            points = [right_axes.c2p(x, y, 0) for x, y in zip(x_vals, y_vals)]
            
            pdf = VMobject()
            pdf.set_points_as_corners(points)
            pdf.set_color(interpolate_color(RED, BLUE, t))
            pdf.set_stroke(width=2)
            intermediate_pdfs.append(pdf)
        
        # Show intermediate PDFs
        for pdf in intermediate_pdfs:
            self.play(Create(pdf), run_time=0.5)
        
        self.wait(1)
        
        # Create Fisher distance calculation
        def fisher_distance(G, delta_theta):
            # Fisher distance: ds² = δθ^T G δθ
            ds_squared = delta_theta.T @ G @ delta_theta
            return np.sqrt(ds_squared)
        
        # Calculate distances at different points along the path
        distances = []
        for i in range(len(path_points) - 1):
            delta_theta = path_points[i+1] - path_points[i]
            # Use metric at current point
            G_current = fisher_metric_normal(path_points[i][0], path_points[i][1])
            ds = fisher_distance(G_current, delta_theta)
            distances.append(ds)
        
        total_distance = sum(distances)
        
        # Show distance calculation
        distance_text = VGroup(
            Text("Fisher Distance Calculation:", font_size=24, color=WHITE),
            Text(f"ds² = δθ^T G(θ) δθ", font_size=20, color=YELLOW),
            Text(f"Total distance: {total_distance:.3f}", font_size=20, color=ORANGE),
            Text("This measures information difference between distributions", font_size=18, color=BLUE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(Write(distance_text))
        self.wait(2)
        
        # Show how the metric changes along the path
        metric_evolution = VGroup()
        sample_points = [0, 0.25, 0.5, 0.75, 1.0]
        
        for t in sample_points:
            point = geodesic_path(t)
            G = fisher_metric_normal(point[0], point[1])
            
            metric_text = MathTex(
                f"G = \\begin{{pmatrix}} {G[0,0]:.2f} & {G[0,1]:.2f} \\\\ {G[1,0]:.2f} & {G[1,1]:.2f} \\end{{pmatrix}}",
                font_size=10,
                color=YELLOW
            )
            
            # Position along the path
            path_pos = left_axes.c2p(point[0], point[1], 0)
            metric_text.move_to(path_pos + RIGHT * 0.7)
            metric_evolution.add(metric_text)
        
        self.play(*[Write(metric) for metric in metric_evolution])
        self.wait(2)
        
        # Show moving point along the geodesic
        moving_point = Dot(color=YELLOW, radius=0.08)
        moving_point.move_to(path_coords[0])
        
        self.play(FadeIn(moving_point))
        
        # Animate the point along the path
        self.play(MoveAlongPath(moving_point, geodesic_path_obj, run_time=4))
        self.wait(1)
        
        # Show the statistical interpretation
        interpretation_text = VGroup(
            Text("Key Insights:", font_size=24, color=WHITE),
            Text("• Fisher metric G(θ) varies with parameters", font_size=18, color=BLUE),
            Text("• Higher σ → Lower metric values (less information)", font_size=18, color=GREEN),
            Text("• Distance measures information loss between distributions", font_size=18, color=YELLOW),
            Text("• Geodesic path respects the geometry of probability space", font_size=18, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(distance_text))
        self.play(Write(interpretation_text))
        self.wait(3)
        
        # Final explanation
        final_text = VGroup(
            Text("The Fisher metric reveals the intrinsic geometry", font_size=24, color=YELLOW),
            Text("of probability distributions, where distances", font_size=24, color=YELLOW),
            Text("measure information-theoretic differences", font_size=20, color=BLUE)
        ).arrange(DOWN, buff=0.4).to_edge(DOWN)
        
        self.play(FadeOut(interpretation_text))
        self.play(Write(final_text))
        self.wait(3)
