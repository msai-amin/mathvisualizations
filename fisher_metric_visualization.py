from manim import *
import numpy as np

class FisherMetricVisualization(Scene):
    def construct(self):
        # Set up the scene
        title = Text("Fisher Metric on Statistical Manifold", font_size=32, color=WHITE).to_edge(UP)
        subtitle = Text("Measuring Distances Between Probability Distributions", font_size=20, color=BLUE).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        
        # Create coordinate systems
        # Left: Parameter space with Fisher metric
        left_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=4,
            y_length=4
        )
        left_axes.move_to(LEFT * 3)
        
        # Right: Probability distributions and Fisher distance
        right_axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[0, 1, 0.2],
            x_length=4,
            y_length=4
        )
        right_axes.move_to(RIGHT * 3)
        
        # Add labels
        left_label = Text("Parameter Space\n(θ₁, θ₂)", font_size=20, color=RED).next_to(left_axes, DOWN)
        right_label = Text("Probability Space\nwith Fisher Distance", font_size=20, color=GREEN).next_to(right_axes, DOWN)
        
        # Create coordinate grid
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
        
        # Show coordinate systems
        self.play(Create(left_axes), Create(right_axes))
        self.play(Write(left_label), Write(right_label))
        self.wait(1)
        
        # Show parameter grid
        self.play(Create(param_grid))
        self.wait(1)
        
        # Create two specific probability distributions
        # Distribution 1: Normal with parameters (μ₁, σ₁)
        dist1_params = np.array([-0.5, 0.3])  # (μ₁, σ₁)
        dist1_point = left_axes.c2p(dist1_params[0], dist1_params[1], 0)
        
        # Distribution 2: Normal with parameters (μ₂, σ₂)
        dist2_params = np.array([0.8, 0.6])   # (μ₂, σ₂)
        dist2_point = left_axes.c2p(dist2_params[0], dist2_params[1], 0)
        
        # Create points for the distributions
        dist1_dot = Dot(point=dist1_point, color=RED, radius=0.1)
        dist2_dot = Dot(point=dist2_point, color=BLUE, radius=0.1)
        
        # Add labels for the distributions
        dist1_label = Text("P₁(μ₁, σ₁)", font_size=16, color=RED)
        dist1_label.move_to(dist1_point + UP * 0.4)
        
        dist2_label = Text("P₂(μ₂, σ₂)", font_size=16, color=BLUE)
        dist2_label.move_to(dist2_point + UP * 0.4)
        
        # Show the two distributions
        self.play(FadeIn(dist1_dot), FadeIn(dist2_dot))
        self.play(Write(dist1_label), Write(dist2_label))
        self.wait(1)
        
        # Create Fisher metric at both points
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
            font_size=14,
            color=RED
        )
        metric1_text.move_to(dist1_point + DOWN * 0.5)
        
        metric2_text = MathTex(
            f"G_2 = \\begin{{pmatrix}} {G2[0,0]:.2f} & {G2[0,1]:.2f} \\\\ {G2[1,0]:.2f} & {G2[1,1]:.2f} \\end{{pmatrix}}",
            font_size=14,
            color=BLUE
        )
        metric2_text.move_to(dist2_point + DOWN * 0.5)
        
        self.play(Write(metric1_text), Write(metric2_text))
        self.wait(2)
        
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
        
        # Create Fisher distance calculation
        def fisher_distance(G1, G2, delta_theta):
            # Fisher distance: ds² = δθ^T G δθ
            # For infinitesimal displacement
            ds_squared = delta_theta.T @ G1 @ delta_theta
            return np.sqrt(ds_squared)
        
        # Calculate distances at different points along the path
        distances = []
        for i in range(len(path_points) - 1):
            delta_theta = path_points[i+1] - path_points[i]
            # Use metric at current point
            G_current = fisher_metric_normal(path_points[i][0], path_points[i][1])
            ds = fisher_distance(G_current, G_current, delta_theta)
            distances.append(ds)
        
        total_distance = sum(distances)
        
        # Show distance calculation
        distance_text = VGroup(
            Text("Fisher Distance Calculation:", font_size=24, color=WHITE),
            Text(f"ds² = δθ^T G(θ) δθ", font_size=20, color=YELLOW),
            Text(f"Total distance: {total_distance:.3f}", font_size=20, color=ORANGE)
        ).arrange(DOWN, buff=0.4).to_edge(DOWN)
        
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
                font_size=12,
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
            Text("Statistical Interpretation:", font_size=24, color=WHITE),
            Text("• Each point represents a probability distribution", font_size=18, color=BLUE),
            Text("• Fisher metric measures information content", font_size=18, color=GREEN),
            Text("• Distance = information loss between distributions", font_size=18, color=YELLOW),
            Text("• Geodesic = optimal path between distributions", font_size=18, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(distance_text))
        self.play(Write(interpretation_text))
        self.wait(3)
        
        # Final explanation
        final_text = VGroup(
            Text("The Fisher metric creates a Riemannian geometry", font_size=24, color=YELLOW),
            Text("on the space of probability distributions", font_size=24, color=YELLOW),
            Text("where distances measure information differences", font_size=20, color=BLUE)
        ).arrange(DOWN, buff=0.4).to_edge(DOWN)
        
        self.play(FadeOut(interpretation_text))
        self.play(Write(final_text))
        self.wait(3)
