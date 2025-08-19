from manim import *
import numpy as np

class ParametricSpaceVisualization(ThreeDScene):
    def construct(self):
        # Set up the scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        
        title = Text("Parametric Space Visualization", font_size=32, color=WHITE).to_edge(UP)
        subtitle = Text("Exploring Spaces Defined by Parameters", font_size=20, color=BLUE).next_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.play(Write(title), Write(subtitle))
        
        # Create coordinate system for parameter space
        axes = ThreeDAxes(
            x_range=[-3, 3, 0.5],
            y_range=[-3, 3, 0.5],
            z_range=[-2, 2, 0.5],
            x_length=6,
            y_length=6,
            z_length=4
        )
        
        # Add axis labels
        x_label = axes.get_x_axis_label(MathTex(r"\alpha"))
        y_label = axes.get_y_axis_label(MathTex(r"\beta"))
        z_label = axes.get_z_axis_label(MathTex(r"\gamma"))
        
        # Show coordinate system
        self.play(Create(axes), Write(x_label), Write(y_label), Write(z_label))
        self.wait(1)
        
        # Create parameter space grid
        grid = VGroup()
        
        # Create grid lines for different parameter values
        for alpha in np.linspace(-3, 3, 13):
            for beta in np.linspace(-3, 3, 13):
                # Create a point in parameter space
                point = axes.c2p(alpha, beta, 0)
                grid_point = Dot(point=point, color=BLUE, radius=0.02)
                grid.add(grid_point)
        
        # Show parameter space grid
        self.play(Create(grid))
        self.wait(1)
        
        # Create parameter space surface
        def parametric_surface(alpha, beta):
            # Define a parametric surface: z = f(alpha, beta)
            gamma = 0.3 * (alpha**2 - beta**2) + 0.1 * np.sin(alpha) * np.cos(beta)
            return np.array([alpha, beta, gamma])
        
        # Create the surface
        surface = Surface(
            lambda u, v: parametric_surface(u, v),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(20, 20)
        )
        surface.set_style(fill_opacity=0.6, stroke_width=1)
        surface.set_color_by_gradient(BLUE, GREEN, YELLOW, RED)
        
        # Show the parametric surface
        self.play(Create(surface))
        self.wait(1)
        
        # Add surface label
        surface_label = Text("Parametric Surface: γ = f(α, β)", font_size=16, color=WHITE)
        surface_label.move_to(axes.c2p(0, 0, 2.5))
        self.add_fixed_in_frame_mobjects(surface_label)
        self.play(Write(surface_label))
        self.wait(1)
        
        # Show parameter evolution
        # Create moving point that shows parameter evolution
        moving_point = Dot(color=YELLOW, radius=0.08)
        
        # Define parameter evolution path
        def parameter_path(t):
            alpha = 2 * np.cos(t)
            beta = 2 * np.sin(t)
            gamma = parametric_surface(alpha, beta)[2]
            return axes.c2p(alpha, beta, gamma)
        
        # Create the parameter path
        path_points = []
        for t in np.linspace(0, 2*np.pi, 50):
            path_points.append(parameter_path(t))
        
        path = VMobject()
        path.set_points_as_corners(path_points)
        path.set_color(YELLOW)
        path.set_stroke(width=3)
        
        # Show the parameter path
        self.play(Create(path))
        self.wait(1)
        
        # Animate the moving point along the parameter path
        moving_point.move_to(path_points[0])
        self.play(FadeIn(moving_point))
        self.play(MoveAlongPath(moving_point, path, run_time=4))
        self.wait(1)
        
        # Show parameter values during evolution
        param_text = VGroup(
            Text("Parameter Evolution:", font_size=16, color=WHITE),
            Text("α(t) = 2cos(t)", font_size=14, color=BLUE),
            Text("β(t) = 2sin(t)", font_size=14, color=GREEN),
            Text("γ(t) = f(α(t), β(t))", font_size=14, color=YELLOW)
        ).arrange(DOWN, buff=0.2).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(param_text)
        
        self.play(Write(param_text))
        self.wait(2)
        
        # Show different parameter configurations
        self.play(FadeOut(param_text))
        
        # Create multiple parameter configurations
        configs = [
            {"alpha": -2, "beta": -2, "color": RED, "name": "Config A"},
            {"alpha": 2, "beta": -2, "color": GREEN, "name": "Config B"},
            {"alpha": 2, "beta": 2, "color": BLUE, "name": "Config C"},
            {"alpha": -2, "beta": 2, "color": ORANGE, "name": "Config D"}
        ]
        
        config_points = []
        config_labels = []
        
        for config in configs:
            alpha, beta = config["alpha"], config["beta"]
            gamma = parametric_surface(alpha, beta)[2]
            point = axes.c2p(alpha, beta, gamma)
            
            dot = Dot(point=point, color=config["color"], radius=0.1)
            config_points.append(dot)
            
            label = Text(config["name"], font_size=12, color=config["color"])
            label.move_to(point + UP * 0.3)
            config_labels.append(label)
        
        # Show configuration points
        for point, label in zip(config_points, config_labels):
            self.play(FadeIn(point), Write(label), run_time=0.5)
        
        self.wait(1)
        
        # Show parameter space properties
        properties_text = VGroup(
            Text("Parametric Space Properties:", font_size=18, color=WHITE),
            Text("• Each point (α, β, γ) represents a configuration", font_size=14, color=BLUE),
            Text("• Parameters define the state of the system", font_size=14, color=GREEN),
            Text("• Continuous parameter changes create smooth evolution", font_size=14, color=YELLOW),
            Text("• Parameter space can be high-dimensional", font_size=14, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(properties_text)
        
        self.play(FadeOut(*config_points), FadeOut(*config_labels))
        self.play(Write(properties_text))
        self.wait(2)
        
        # Show parameter sensitivity
        self.play(FadeOut(properties_text))
        
        # Create sensitivity visualization
        sensitivity_text = Text("Parameter Sensitivity Analysis", font_size=18, color=WHITE).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(sensitivity_text)
        self.play(Write(sensitivity_text))
        
        # Show how small parameter changes affect the system
        base_alpha, base_beta = 0, 0
        base_gamma = parametric_surface(base_alpha, base_beta)[2]
        base_point = axes.c2p(base_alpha, base_beta, base_gamma)
        
        base_dot = Dot(point=base_point, color=WHITE, radius=0.1)
        self.play(FadeIn(base_dot))
        
        # Show sensitivity vectors
        sensitivity_vectors = []
        for delta_alpha in [-0.5, 0.5]:
            for delta_beta in [-0.5, 0.5]:
                new_alpha = base_alpha + delta_alpha
                new_beta = base_beta + delta_beta
                new_gamma = parametric_surface(new_alpha, new_beta)[2]
                new_point = axes.c2p(new_alpha, new_beta, new_gamma)
                
                vector = Arrow(start=base_point, end=new_point, color=YELLOW, buff=0.05)
                sensitivity_vectors.append(vector)
        
        # Show sensitivity vectors
        for vector in sensitivity_vectors:
            self.play(Create(vector), run_time=0.3)
        
        self.wait(1)
        
        # Show mathematical formulation
        math_text = VGroup(
            Text("Mathematical Formulation:", font_size=18, color=WHITE),
            Text("S = {(α, β, γ) ∈ ℝ³ | γ = f(α, β)}", font_size=16, color=YELLOW),
            Text("where f: ℝ² → ℝ is the parameter function", font_size=14, color=BLUE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(math_text)
        
        self.play(FadeOut(sensitivity_text), FadeOut(base_dot), FadeOut(*sensitivity_vectors))
        self.play(Write(math_text))
        self.wait(2)
        
        # Show applications
        applications_text = VGroup(
            Text("Applications of Parametric Spaces:", font_size=18, color=WHITE),
            Text("• Physics: Phase space, configuration space", font_size=14, color=BLUE),
            Text("• Engineering: Design parameter optimization", font_size=14, color=GREEN),
            Text("• Machine Learning: Hyperparameter tuning", font_size=14, color=YELLOW),
            Text("• Economics: Parameter space of models", font_size=14, color=ORANGE),
            Text("• Biology: Parameter space of biological systems", font_size=14, color=RED)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(applications_text)
        
        self.play(FadeOut(math_text))
        self.play(Write(applications_text))
        self.wait(3)
        
        # Final summary
        final_text = VGroup(
            Text("Parametric spaces provide a framework", font_size=20, color=YELLOW),
            Text("for understanding how systems evolve", font_size=20, color=YELLOW),
            Text("as their defining parameters change", font_size=18, color=BLUE)
        ).arrange(DOWN, buff=0.4).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(final_text)
        
        self.play(FadeOut(applications_text))
        self.play(Write(final_text))
        self.wait(3)
