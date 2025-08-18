from manim import *
import numpy as np

class AffineConnectionVisualization(Scene):
    def construct(self):
        # Set up the scene
        title = Text("Affine Connection ∇ on Manifold", font_size=32, color=WHITE).to_edge(UP)
        subtitle = Text("Parallel Transport & Geodesics", font_size=20, color=BLUE).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        
        # Create coordinate systems
        # Left: Manifold with connection
        left_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=4,
            y_length=4
        )
        left_axes.move_to(LEFT * 3)
        
        # Right: Connection coefficients
        right_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=4,
            y_length=4
        )
        right_axes.move_to(RIGHT * 3)
        
        # Add labels
        left_label = Text("Manifold M\nwith Connection ∇", font_size=18, color=RED).next_to(left_axes, DOWN)
        right_label = Text("Connection Coefficients\nΓ^λ_μν", font_size=18, color=GREEN).next_to(right_axes, DOWN)
        
        # Show coordinate systems
        self.play(Create(left_axes), Create(right_axes))
        self.play(Write(left_label), Write(right_label))
        self.wait(1)
        
        # Create coordinate grid
        coord_grid = VGroup()
        
        # Vertical lines
        for x in np.linspace(-2, 2, 9):
            line = Line(
                start=left_axes.c2p(x, -2, 0),
                end=left_axes.c2p(x, 2, 0),
                color=BLUE,
                stroke_width=1
            )
            coord_grid.add(line)
        
        # Horizontal lines
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
        
        # Create connection coefficients function
        def connection_coefficients(x, y):
            # Example connection coefficients (Christoffel symbols)
            # These determine how vectors change under parallel transport
            gamma_111 = 0.1 * x  # Γ¹₁₁
            gamma_112 = 0.05 * y # Γ¹₁₂
            gamma_121 = 0.05 * y # Γ¹₂₁
            gamma_122 = -0.1 * x # Γ¹₂₂
            gamma_211 = -0.05 * y # Γ²₁₁
            gamma_212 = 0.1 * x  # Γ²₁₂
            gamma_221 = 0.1 * x  # Γ²₂₁
            gamma_222 = 0.1 * y  # Γ²₂₂
            
            return {
                '111': gamma_111, '112': gamma_112, '121': gamma_121, '122': gamma_122,
                '211': gamma_211, '212': gamma_212, '221': gamma_221, '222': gamma_222
            }
        
        # Show connection coefficients at different points
        connection_points = [(-1.5, -1.5), (0, 0), (1.5, 1.5)]
        connection_displays = VGroup()
        
        for point in connection_points:
            x, y = point
            gamma = connection_coefficients(x, y)
            
            # Create connection display
            connection_text = MathTex(
                f"\\Gamma^1_{{11}} = {gamma['111']:.2f}",
                f"\\Gamma^1_{{12}} = {gamma['112']:.2f}",
                f"\\Gamma^2_{{21}} = {gamma['221']:.2f}",
                font_size=10,
                color=YELLOW
            ).arrange(DOWN, buff=0.1)
            
            # Position at the point
            point_pos = left_axes.c2p(x, y, 0)
            connection_text.move_to(point_pos + UP * 0.5)
            connection_displays.add(connection_text)
        
        # Show connection coefficients
        self.play(*[Write(display) for display in connection_displays])
        self.wait(2)
        
        # Create a curve for parallel transport
        def curve_parameterization(t):
            # Parameterized curve: x = t, y = 0.5 * t²
            x = t
            y = 0.5 * t**2
            return np.array([x, y])
        
        # Create the curve
        t_vals = np.linspace(-1.5, 1.5, 100)
        curve_points = [curve_parameterization(t) for t in t_vals]
        curve_coords = [left_axes.c2p(p[0], p[1], 0) for p in curve_points]
        
        curve_path = VMobject()
        curve_path.set_points_as_corners(curve_coords)
        curve_path.set_color(ORANGE)
        curve_path.set_stroke(width=3)
        
        # Show the curve
        self.play(Create(curve_path))
        self.wait(1)
        
        # Create initial vector at start of curve
        start_point = curve_points[0]
        initial_vector = Arrow(
            start=left_axes.c2p(start_point[0], start_point[1], 0),
            end=left_axes.c2p(start_point[0] + 0.3, start_point[1] + 0.3, 0),
            color=RED,
            stroke_width=4
        )
        
        # Add vector label
        vector_label = Text("V₀", font_size=16, color=RED)
        vector_label.move_to(left_axes.c2p(start_point[0] + 0.4, start_point[1] + 0.4, 0))
        
        self.play(Create(initial_vector), Write(vector_label))
        self.wait(1)
        
        # Create parallel transport visualization
        # Show how the vector changes along the curve
        transported_vectors = []
        sample_times = [0.25, 0.5, 0.75, 1.0]
        
        for t in sample_times:
            idx = int(t * (len(curve_points) - 1))
            point = curve_points[idx]
            
            # Calculate parallel transported vector (simplified)
            # In practice, this would solve the parallel transport equation
            # ∇_γ' V = 0, where γ' is the tangent vector to the curve
            
            # For visualization, we'll show the vector changing direction
            angle_change = 0.3 * t * np.pi  # Simplified rotation
            vector_end_x = point[0] + 0.3 * np.cos(angle_change)
            vector_end_y = point[1] + 0.3 * np.sin(angle_change)
            
            transported_vector = Arrow(
                start=left_axes.c2p(point[0], point[1], 0),
                end=left_axes.c2p(vector_end_x, vector_end_y, 0),
                color=interpolate_color(RED, BLUE, t),
                stroke_width=3
            )
            
            transported_vectors.append(transported_vector)
        
        # Show transported vectors
        for vector in transported_vectors:
            self.play(Create(vector), run_time=0.5)
        
        self.wait(1)
        
        # Show parallel transport equation
        transport_equation = MathTex(
            r"\nabla_{\gamma'} V = 0",
            font_size=20,
            color=YELLOW
        )
        transport_equation.move_to(right_axes.c2p(0, 1.5, 0))
        
        self.play(Write(transport_equation))
        self.wait(2)
        
        # Show geodesic equation
        geodesic_equation = MathTex(
            r"\frac{d^2 x^\mu}{dt^2} + \Gamma^\mu_{\nu\lambda} \frac{dx^\nu}{dt} \frac{dx^\lambda}{dt} = 0",
            font_size=16,
            color=ORANGE
        )
        geodesic_equation.move_to(right_axes.c2p(0, 0, 0))
        
        self.play(Write(geodesic_equation))
        self.wait(2)
        
        # Show moving point along the curve
        moving_point = Dot(color=YELLOW, radius=0.08)
        moving_point.move_to(curve_coords[0])
        
        self.play(FadeIn(moving_point))
        
        # Animate the point along the curve
        self.play(MoveAlongPath(moving_point, curve_path, run_time=4))
        self.wait(1)
        
        # Show connection properties
        properties_text = VGroup(
            Text("Affine Connection Properties:", font_size=20, color=WHITE),
            Text("• ∇_X(Y+Z) = ∇_X Y + ∇_X Z (linearity)", font_size=16, color=BLUE),
            Text("• ∇_(fX) Y = f ∇_X Y (tensor product rule)", font_size=16, color=GREEN),
            Text("• ∇_X(fY) = X(f)Y + f ∇_X Y (Leibniz rule)", font_size=16, color=YELLOW),
            Text("• Parallel transport preserves vector length", font_size=16, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(transport_equation), FadeOut(geodesic_equation))
        self.play(Write(properties_text))
        self.wait(3)
        
        # Show torsion and curvature
        curvature_text = VGroup(
            Text("Torsion & Curvature:", font_size=20, color=WHITE),
            Text("• T(X,Y) = ∇_X Y - ∇_Y X - [X,Y] (torsion)", font_size=16, color=BLUE),
            Text("• R(X,Y)Z = ∇_X ∇_Y Z - ∇_Y ∇_X Z - ∇_[X,Y] Z (curvature)", font_size=16, color=GREEN),
            Text("• Torsion-free connection: T = 0", font_size=16, color=YELLOW),
            Text("• Flat manifold: R = 0", font_size=16, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(properties_text))
        self.play(Write(curvature_text))
        self.wait(3)
        
        # Final explanation
        final_text = VGroup(
            Text("The affine connection ∇ defines how to transport vectors", font_size=20, color=YELLOW),
            Text("along curves on the manifold", font_size=20, color=YELLOW),
            Text("It determines geodesics and parallel transport", font_size=18, color=BLUE)
        ).arrange(DOWN, buff=0.4).to_edge(DOWN)
        
        self.play(FadeOut(curvature_text))
        self.play(Write(final_text))
        self.wait(3)
