from manim import *
import numpy as np
from scipy.stats import norm

class NormalDistributionManifold(ThreeDScene):
    def construct(self):
        # Set up the scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        
        title = Text("Statistical Manifold of Normal Distributions", font_size=28, color=WHITE).to_edge(UP)
        subtitle = Text("Each point (μ, σ²) represents N(μ, σ²)", font_size=18, color=BLUE).next_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.play(Write(title), Write(subtitle))
        
        # Create coordinate system for the statistical manifold
        axes = ThreeDAxes(
            x_range=[-3, 3, 0.5],
            y_range=[0.2, 2, 0.2],
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
            v_range=[0.2, 2.0],  # σ must be positive
            resolution=(30, 30)
        )
        surface.set_style(fill_opacity=0.7, stroke_width=1)
        surface.set_color_by_gradient(BLUE, GREEN, YELLOW, RED)
        
        # Show the statistical manifold surface
        self.play(Create(surface))
        self.wait(2)
        
        # Add surface label
        surface_label = Text("Statistical Manifold: N(μ, σ²)", font_size=16, color=WHITE)
        surface_label.move_to(axes.c2p(0, 0, 2.5))
        self.add_fixed_in_frame_mobjects(surface_label)
        self.play(Write(surface_label))
        self.wait(1)
        
        # Show how each point represents a probability distribution
        # Create sample points on the manifold
        sample_points = [
            {"mu": -2, "sigma": 0.5, "color": RED, "name": "N(-2, 0.25)"},
            {"mu": 0, "sigma": 1.0, "color": GREEN, "name": "N(0, 1)"},
            {"mu": 2, "sigma": 1.5, "color": BLUE, "name": "N(2, 2.25)"}
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
        
        # Show explanation of what each point represents
        explanation_text = VGroup(
            Text("Each Point = Normal Distribution", font_size=16, color=WHITE),
            Text("• μ controls the center (mean)", font_size=14, color=BLUE),
            Text("• σ controls the spread (standard deviation)", font_size=14, color=GREEN),
            Text("• P(x) shows maximum probability density", font_size=14, color=YELLOW)
        ).arrange(DOWN, buff=0.2).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(explanation_text)
        
        self.play(Write(explanation_text))
        self.wait(2)
        
        # Now show actual probability density functions
        self.play(FadeOut(explanation_text), FadeOut(*sample_dots), FadeOut(*sample_labels))
        
        # Create a 2D view to show the actual normal distributions
        # We'll create a separate coordinate system for the PDFs
        pdf_axes = Axes(
            x_range=[-4, 4, 0.5],
            y_range=[0, 1.5, 0.2],
            x_length=6,
            y_length=4,
            axis_config={"color": WHITE, "stroke_width": 2}
        )
        pdf_axes.move_to(ORIGIN)
        
        # Add PDF axis labels
        pdf_x_label = pdf_axes.get_x_axis_label("x")
        pdf_y_label = pdf_axes.get_y_axis_label("P(x)")
        
        # Show PDF coordinate system
        self.play(Create(pdf_axes), Write(pdf_x_label), Write(pdf_y_label))
        self.wait(1)
        
        # Create and show multiple normal distributions
        distributions = [
            {"mu": -2, "sigma": 0.5, "color": RED, "name": "N(-2, 0.25)"},
            {"mu": 0, "sigma": 1.0, "color": GREEN, "name": "N(0, 1)"},
            {"mu": 2, "sigma": 1.5, "color": BLUE, "name": "N(2, 2.25)"}
        ]
        
        pdf_curves = []
        pdf_labels = []
        
        for dist in distributions:
            mu, sigma = dist["mu"], dist["sigma"]
            
            # Create the normal distribution curve
            x_values = np.linspace(-4, 4, 200)
            y_values = norm.pdf(x_values, mu, sigma)
            
            # Scale to fit in the coordinate system
            y_values = y_values * 1.5 / np.max(y_values)
            
            points = [pdf_axes.c2p(x, y, 0) for x, y in zip(x_values, y_values)]
            
            curve = VMobject()
            curve.set_points_as_corners(points)
            curve.set_color(dist["color"])
            curve.set_stroke(width=3)
            
            pdf_curves.append(curve)
            
            # Add label
            label = Text(dist["name"], font_size=12, color=dist["color"])
            label.move_to(pdf_axes.c2p(mu, 1.2, 0))
            pdf_labels.append(label)
        
        # Show the PDF curves
        for curve, label in zip(pdf_curves, pdf_labels):
            self.play(Create(curve), Write(label), run_time=1)
        
        self.wait(2)
        
        # Show the relationship between manifold and PDFs
        relationship_text = VGroup(
            Text("Manifold-PDF Relationship:", font_size=16, color=WHITE),
            Text("• Each point (μ, σ) on manifold", font_size=14, color=BLUE),
            Text("• Corresponds to a normal distribution N(μ, σ²)", font_size=14, color=GREEN),
            Text("• Manifold shows parameter space", font_size=14, color=YELLOW),
            Text("• PDFs show actual probability functions", font_size=14, color=ORANGE)
        ).arrange(DOWN, buff=0.2).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(relationship_text)
        
        self.play(Write(relationship_text))
        self.wait(2)
        
        # Return to 3D view to show the complete manifold
        self.play(FadeOut(pdf_axes), FadeOut(pdf_x_label), FadeOut(pdf_y_label), 
                  FadeOut(*pdf_curves), FadeOut(*pdf_labels), FadeOut(relationship_text))
        
        # Move camera to show different perspectives of the manifold
        self.set_camera_orientation(phi=60 * DEGREES, theta=60 * DEGREES)
        self.wait(2)
        
        # Show parameter space interpretation
        param_text = VGroup(
            Text("Parameter Space Interpretation:", font_size=16, color=WHITE),
            Text("• μ-axis: All possible mean values", font_size=14, color=BLUE),
            Text("• σ-axis: All possible standard deviations", font_size=14, color=GREEN),
            Text("• Surface: All possible normal distributions", font_size=14, color=YELLOW),
            Text("• Each point: One specific N(μ, σ²)", font_size=14, color=ORANGE)
        ).arrange(DOWN, buff=0.2).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(param_text)
        
        self.play(Write(param_text))
        self.wait(2)
        
        # Move camera to show the curvature
        self.set_camera_orientation(phi=80 * DEGREES, theta=30 * DEGREES)
        self.wait(2)
        
        # Show mathematical formulation
        math_text = VGroup(
            Text("Mathematical Formulation:", font_size=16, color=WHITE),
            MathTex(r"M = \{N(\mu, \sigma^2) : \mu \in \mathbb{R}, \sigma > 0\}", font_size=16, color=YELLOW),
            Text("Statistical manifold of all normal distributions", font_size=14, color=BLUE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(math_text)
        
        self.play(FadeOut(param_text))
        self.play(Write(math_text))
        self.wait(2)
        
        # Final camera movement to show overall structure
        self.set_camera_orientation(phi=65 * DEGREES, theta=45 * DEGREES)
        self.wait(2)
        
        # Final summary
        final_text = VGroup(
            Text("Statistical Manifold of Normal Distributions", font_size=20, color=YELLOW),
            Text("• Each point (μ, σ) represents N(μ, σ²)", font_size=16, color=WHITE),
            Text("• Parameter space covers all possible normal distributions", font_size=16, color=BLUE),
            Text("• Manifold structure reflects distribution properties", font_size=16, color=GREEN)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(final_text)
        
        self.play(FadeOut(math_text))
        self.play(Write(final_text))
        self.wait(3)
