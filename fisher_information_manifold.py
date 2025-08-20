from manim import *
import numpy as np
from scipy.stats import norm, gamma, beta

class FisherInformationManifold(ThreeDScene):
    def construct(self):
        # Set up the scene with better initial camera angle
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        
        title = Text("Fisher Information Matrix on Statistical Manifold", font_size=28, color=WHITE).to_edge(UP)
        subtitle = Text("How Probability Distributions Shape the Manifold", font_size=18, color=BLUE).next_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.play(Write(title), Write(subtitle))
        
        # Create coordinate system for the statistical manifold
        axes = ThreeDAxes(
            x_range=[-3, 3, 0.5],
            y_range=[-3, 3, 0.5],
            z_range=[0, 2, 0.5],
            x_length=6,
            y_length=6,
            z_length=4
        )
        
        # Add axis labels
        x_label = axes.get_x_axis_label(MathTex(r"\mu"))
        y_label = axes.get_y_axis_label(MathTex(r"\sigma"))
        z_label = axes.get_z_axis_label(MathTex(r"P(x)"))
        
        # Show coordinate system
        self.play(Create(axes), Write(x_label), Write(y_label), Write(z_label))
        self.wait(1)
        
        # Create the statistical manifold surface
        # Each point (μ, σ) represents a normal distribution N(μ, σ²)
        def statistical_manifold_surface(mu, sigma):
            # For visualization, we'll show the maximum probability density
            # P(x) = 1/(σ√(2π)) at x = μ (the mean)
            max_prob = 1 / (sigma * np.sqrt(2 * np.pi))
            return np.array([mu, sigma, max_prob])
        
        # Create the surface
        surface = Surface(
            lambda u, v: statistical_manifold_surface(u, v),
            u_range=[-2.5, 2.5],
            v_range=[0.3, 2.5],  # σ must be positive
            resolution=(30, 30)
        )
        surface.set_style(fill_opacity=0.7, stroke_width=1)
        surface.set_color_by_gradient(BLUE, GREEN, YELLOW, RED)
        
        # Show the statistical manifold surface
        self.play(Create(surface))
        self.wait(1)
        
        # Add camera movement to show different perspectives
        self.move_camera(phi=75 * DEGREES, theta=45 * DEGREES, run_time=3)
        self.wait(1)
        
        # Move camera to show the surface from another angle
        self.move_camera(phi=45 * DEGREES, theta=60 * DEGREES, run_time=3)
        self.wait(1)
        
        # Return to a good viewing angle
        self.move_camera(phi=65 * DEGREES, theta=35 * DEGREES, run_time=2)
        self.wait(1)
        
        # Add surface label
        surface_label = Text("Statistical Manifold: N(μ, σ²)", font_size=16, color=WHITE)
        surface_label.move_to(axes.c2p(0, 0, 2.5))
        self.add_fixed_in_frame_mobjects(surface_label)
        self.play(Write(surface_label))
        self.wait(1)
        
        # Show how each point represents a probability distribution
        # Create sample points on the manifold
        sample_points = [
            {"mu": -1.5, "sigma": 0.5, "color": RED, "name": "N(-1.5, 0.25)"},
            {"mu": 0, "sigma": 1.0, "color": GREEN, "name": "N(0, 1)"},
            {"mu": 1.5, "sigma": 1.5, "color": BLUE, "name": "N(1.5, 2.25)"}
        ]
        
        sample_dots = []
        sample_labels = []
        
        for sample in sample_points:
            mu, sigma = sample["mu"], sample["sigma"]
            z = statistical_manifold_surface(mu, sigma)[2]
            point = axes.c2p(mu, sigma, z)
            
            dot = Dot(point=point, color=sample["color"], radius=0.1)
            sample_dots.append(dot)
            
            label = Text(sample["name"], font_size=12, color=sample["color"])
            label.move_to(point + UP * 0.3)
            sample_labels.append(label)
        
        # Show sample points
        for dot, label in zip(sample_dots, sample_labels):
            self.play(FadeIn(dot), Write(label), run_time=0.5)
        
        self.wait(1)
        
        # Move camera to better see the sample points
        self.move_camera(phi=70 * DEGREES, theta=40 * DEGREES, run_time=2)
        self.wait(1)
        
        # Show probability density functions for each sample point
        pdf_explanation = VGroup(
            Text("Each Point = Probability Distribution", font_size=16, color=WHITE),
            Text("Distance measured by Fisher Information", font_size=14, color=YELLOW)
        ).arrange(DOWN, buff=0.2).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(pdf_explanation)
        
        self.play(Write(pdf_explanation))
        self.wait(2)
        
        # Now show the Fisher Information Matrix
        self.play(FadeOut(pdf_explanation), FadeOut(*sample_dots), FadeOut(*sample_labels))
        
        fisher_title = Text("Fisher Information Matrix", font_size=20, color=YELLOW).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(fisher_title)
        self.play(Write(fisher_title))
        
        # Show Fisher Information Matrix for normal distribution
        fisher_matrix = VGroup(
            MathTex(r"I(\mu, \sigma) = \begin{pmatrix} \frac{1}{\sigma^2} & 0 \\ 0 & \frac{2}{\sigma^2} \end{pmatrix}", font_size=18),
            Text("Determines distances on the manifold", font_size=14, color=BLUE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(fisher_matrix)
        
        self.play(FadeOut(fisher_title))
        self.play(Write(fisher_matrix))
        self.wait(2)
        
        # Show how Fisher Information affects distances
        self.play(FadeOut(fisher_matrix))
        
        # Create geodesic paths showing distances
        # Path 1: Constant μ, varying σ
        path1_points = []
        for sigma in np.linspace(0.5, 2.0, 20):
            mu = -1.0
            z = statistical_manifold_surface(mu, sigma)[2]
            path1_points.append(axes.c2p(mu, sigma, z))
        
        path1 = VMobject()
        path1.set_points_as_corners(path1_points)
        path1.set_color(RED)
        path1.set_stroke(width=3)
        
        # Path 2: Constant σ, varying μ
        path2_points = []
        for mu in np.linspace(-1.5, 1.5, 20):
            sigma = 1.0
            z = statistical_manifold_surface(mu, sigma)[2]
            path2_points.append(axes.c2p(mu, sigma, z))
        
        path2 = VMobject()
        path2.set_points_as_corners(path2_points)
        path2.set_color(GREEN)
        path2.set_stroke(width=3)
        
        # Show the geodesic paths
        self.play(Create(path1), Create(path2))
        self.wait(1)
        
        # Move camera to better see the paths
        self.move_camera(phi=60 * DEGREES, theta=50 * DEGREES, run_time=2)
        self.wait(1)
        
        # Add path labels
        path1_label = Text("Constant μ path", font_size=12, color=RED)
        path1_label.move_to(axes.c2p(-1, 1.25, 1.5))
        
        path2_label = Text("Constant σ path", font_size=12, color=GREEN)
        path2_label.move_to(axes.c2p(0, 1, 0.8))
        
        self.play(Write(path1_label), Write(path2_label))
        self.wait(1)
        
        # Show distance calculation using Fisher Information
        distance_explanation = VGroup(
            Text("Distance Calculation:", font_size=16, color=WHITE),
            MathTex(r"ds^2 = \frac{1}{\sigma^2} d\mu^2 + \frac{2}{\sigma^2} d\sigma^2", font_size=16, color=YELLOW),
            Text("Fisher Information determines metric", font_size=14, color=BLUE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(distance_explanation)
        
        self.play(FadeOut(path1_label), FadeOut(path2_label))
        self.play(Write(distance_explanation))
        self.wait(2)
        
        # Show how different regions have different "curvature"
        # due to Fisher Information varying with σ
        curvature_explanation = VGroup(
            Text("Manifold Curvature:", font_size=16, color=WHITE),
            Text("• Small σ: High Fisher Information → Dense metric", font_size=14, color=RED),
            Text("• Large σ: Low Fisher Information → Sparse metric", font_size=14, color=BLUE),
            Text("• Manifold is curved due to σ dependence", font_size=14, color=GREEN)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(curvature_explanation)
        
        self.play(FadeOut(distance_explanation))
        self.play(Write(curvature_explanation))
        self.wait(2)
        
        # Move camera to show the curvature effect
        self.move_camera(phi=80 * DEGREES, theta=25 * DEGREES, run_time=3)
        self.wait(1)
        
        # Show moving point that demonstrates the metric
        moving_point = Dot(color=YELLOW, radius=0.08)
        
        # Create a path that shows how distances vary
        metric_path_points = []
        t_values = np.linspace(0, 2*np.pi, 50)
        for t in t_values:
            mu = 1.5 * np.cos(t)
            sigma = 0.5 + 1.0 * np.sin(t)
            if sigma > 0.3:  # Ensure σ is positive
                z = statistical_manifold_surface(mu, sigma)[2]
                metric_path_points.append(axes.c2p(mu, sigma, z))
        
        metric_path = VMobject()
        metric_path.set_points_as_corners(metric_path_points)
        metric_path.set_color(YELLOW)
        metric_path.set_stroke(width=3)
        
        # Show the metric path
        self.play(Create(metric_path))
        self.wait(1)
        
        # Move camera to follow the moving point
        self.move_camera(phi=70 * DEGREES, theta=35 * DEGREES, run_time=2)
        self.wait(1)
        
        # Animate the moving point
        moving_point.move_to(metric_path_points[0])
        self.play(FadeIn(moving_point))
        self.play(MoveAlongPath(moving_point, metric_path, run_time=4))
        self.wait(1)
        
        # Final camera movement to show overall structure
        self.move_camera(phi=55 * DEGREES, theta=45 * DEGREES, run_time=3)
        self.wait(1)
        
        # Show final explanation of Fisher Information
        final_explanation = VGroup(
            Text("Fisher Information Matrix:", font_size=18, color=WHITE),
            Text("• Defines the metric tensor on statistical manifold", font_size=14, color=BLUE),
            Text("• Determines distances between probability distributions", font_size=14, color=GREEN),
            Text("• Varies with parameters, creating curved geometry", font_size=14, color=YELLOW),
            Text("• Enables natural gradient descent and optimization", font_size=14, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(final_explanation)
        
        self.play(FadeOut(curvature_explanation), FadeOut(moving_point), FadeOut(metric_path))
        self.play(Write(final_explanation))
        self.wait(3)
        
        # Final summary
        final_text = VGroup(
            Text("Statistical manifolds are shaped by", font_size=20, color=YELLOW),
            Text("probability distributions, with distances", font_size=20, color=YELLOW),
            Text("determined by the Fisher Information Matrix", font_size=18, color=BLUE)
        ).arrange(DOWN, buff=0.4).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(final_text)
        
        self.play(FadeOut(final_explanation))
        self.play(Write(final_text))
        self.wait(3)
