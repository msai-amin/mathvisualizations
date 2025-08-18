from manim import *
import numpy as np

class AffineConnection3D(ThreeDScene):
    def construct(self):
        # Set up the 3D scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        
        # Title
        title = Text("3D Affine Connection ∇ on Curved Manifold", font_size=28, color=WHITE).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        # Create a 3D curved manifold surface
        def manifold_surface(u, v):
            # Create a curved surface: saddle surface with modulation
            x = u
            y = v
            z = 0.15 * (u**2 - v**2) + 0.08 * np.sin(3*np.pi*u) * np.cos(2*np.pi*v)
            return np.array([x, y, z])
        
        # Create the surface
        surface = Surface(
            lambda u, v: manifold_surface(u, v),
            u_range=[-2.5, 2.5],
            v_range=[-2.5, 2.5],
            resolution=(25, 25)
        )
        surface.set_style(fill_opacity=0.3, stroke_width=1, stroke_color=BLUE)
        
        # Show the surface
        self.play(Create(surface))
        self.wait(1)
        
        # Create coordinate grid on the surface
        u_lines = []
        for u_val in np.linspace(-2.5, 2.5, 6):
            u_lines.append(ParametricFunction(
                lambda t: manifold_surface(u_val, t),
                t_range=[-2.5, 2.5],
                color=RED,
                stroke_width=2
            ))
        
        v_lines = []
        for v_val in np.linspace(-2.5, 2.5, 6):
            v_lines.append(ParametricFunction(
                lambda t: manifold_surface(t, v_val),
                t_range=[-2.5, 2.5],
                color=GREEN,
                stroke_width=2
            ))
        
        # Show coordinate grid
        self.play(*[Create(line) for line in u_lines + v_lines])
        self.wait(1)
        
        # Create connection coefficients function for 3D surface
        def connection_coefficients_3d(u, v):
            # Calculate Christoffel symbols for the 3D surface
            # These depend on the metric and its derivatives
            
            # First derivatives of the surface
            du = np.array([1, 0, 0.3*u + 0.24*np.pi*np.cos(3*np.pi*u)*np.cos(2*np.pi*v)])
            dv = np.array([0, 1, -0.3*v - 0.16*np.pi*np.sin(3*np.pi*u)*np.sin(2*np.pi*v)])
            
            # Second derivatives
            duu = np.array([0, 0, 0.3 - 0.72*np.pi**2*np.sin(3*np.pi*u)*np.cos(2*np.pi*v)])
            duv = np.array([0, 0, -0.48*np.pi**2*np.cos(3*np.pi*u)*np.sin(2*np.pi*v)])
            dvv = np.array([0, 0, -0.3 - 0.32*np.pi**2*np.sin(3*np.pi*u)*np.cos(2*np.pi*v)])
            
            # Calculate metric components
            g_11 = np.dot(du, du)
            g_12 = np.dot(du, dv)
            g_22 = np.dot(dv, dv)
            
            # Calculate inverse metric
            det_g = g_11 * g_22 - g_12**2
            g_inv_11 = g_22 / det_g
            g_inv_12 = -g_12 / det_g
            g_inv_22 = g_11 / det_g
            
            # Calculate Christoffel symbols
            # Γ^λ_μν = (1/2) g^λσ (∂_μ g_νσ + ∂_ν g_μσ - ∂_σ g_μν)
            
            # ∂_u g_11 = 2 du · duu
            # ∂_v g_11 = 2 du · duv
            # ∂_u g_12 = du · duv + dv · duu
            # ∂_v g_12 = du · dvv + dv · duv
            # ∂_u g_22 = 2 dv · duv
            # ∂_v g_22 = 2 dv · dvv
            
            dg_11_u = 2 * np.dot(du, duu)
            dg_11_v = 2 * np.dot(du, duv)
            dg_12_u = np.dot(du, duv) + np.dot(dv, duu)
            dg_12_v = np.dot(du, dvv) + np.dot(dv, duv)
            dg_22_u = 2 * np.dot(dv, duv)
            dg_22_v = 2 * np.dot(dv, dvv)
            
            # Calculate Γ^1_11, Γ^1_12, Γ^1_22, Γ^2_11, Γ^2_12, Γ^2_22
            gamma_111 = 0.5 * (g_inv_11 * dg_11_u + g_inv_12 * (2*dg_12_u - dg_11_v))
            gamma_112 = 0.5 * (g_inv_11 * dg_12_v + g_inv_12 * dg_22_u)
            gamma_122 = 0.5 * (g_inv_11 * dg_22_v + g_inv_12 * (2*dg_12_v - dg_22_u))
            gamma_211 = 0.5 * (g_inv_12 * dg_11_u + g_inv_22 * (2*dg_12_u - dg_11_v))
            gamma_212 = 0.5 * (g_inv_12 * dg_12_v + g_inv_22 * dg_22_u)
            gamma_222 = 0.5 * (g_inv_12 * dg_22_v + g_inv_22 * (2*dg_12_v - dg_22_u))
            
            return {
                '111': gamma_111, '112': gamma_112, '122': gamma_122,
                '211': gamma_211, '212': gamma_212, '222': gamma_222
            }
        
        # Show connection coefficients at different points
        connection_points = [(-2, -2), (0, 0), (2, 2)]
        connection_displays = VGroup()
        
        for point in connection_points:
            u, v = point
            gamma = connection_coefficients_3d(u, v)
            
            # Create connection display
            connection_text = MathTex(
                f"\\Gamma^1_{{11}} = {gamma['111']:.2f}",
                f"\\Gamma^1_{{12}} = {gamma['112']:.2f}",
                f"\\Gamma^2_{{22}} = {gamma['222']:.2f}",
                font_size=10,
                color=YELLOW
            ).arrange(DOWN, buff=0.1)
            
            # Position at the 3D point
            point_3d = manifold_surface(u, v)
            connection_text.move_to(point_3d + np.array([0, 0, 0.6]))
            connection_displays.add(connection_text)
        
        # Show connection coefficients
        self.play(*[Write(display) for display in connection_displays])
        self.wait(2)
        
        # Create a curve for parallel transport
        def curve_parameterization(t):
            # Parameterized curve on the surface
            u = 1.5 * np.cos(t)
            v = 1.5 * np.sin(t)
            return manifold_surface(u, v)
        
        # Create the curve
        t_vals = np.linspace(0, 2*np.pi, 100)
        curve_points = [curve_parameterization(t) for t in t_vals]
        
        curve_path = ParametricFunction(
            lambda t: curve_parameterization(t),
            t_range=[0, 2*np.pi],
            color=ORANGE,
            stroke_width=3
        )
        
        # Show the curve
        self.play(Create(curve_path))
        self.wait(1)
        
        # Create initial vector at start of curve
        start_point = curve_points[0]
        initial_vector = Arrow3D(
            start=start_point,
            end=start_point + np.array([0.3, 0.3, 0]),
            color=RED,
            thickness=0.05
        )
        
        # Add vector label
        vector_label = Text("V₀", font_size=16, color=RED)
        vector_label.move_to(start_point + np.array([0.4, 0.4, 0.2]))
        self.add_fixed_in_frame_mobjects(vector_label)
        
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
            # based on the surface curvature and connection
            angle_change = 0.4 * t * np.pi  # Simplified rotation
            vector_end_x = point[0] + 0.3 * np.cos(angle_change)
            vector_end_y = point[1] + 0.3 * np.sin(angle_change)
            vector_end_z = point[2] + 0.1 * np.sin(angle_change)
            
            transported_vector = Arrow3D(
                start=point,
                end=np.array([vector_end_x, vector_end_y, vector_end_z]),
                color=interpolate_color(RED, BLUE, t),
                thickness=0.04
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
        transport_equation.move_to(np.array([0, 0, 2]))
        
        self.play(Write(transport_equation))
        self.wait(2)
        
        # Show geodesic equation
        geodesic_equation = MathTex(
            r"\frac{d^2 x^\mu}{dt^2} + \Gamma^\mu_{\nu\lambda} \frac{dx^\nu}{dt} \frac{dx^\lambda}{dt} = 0",
            font_size=16,
            color=ORANGE
        )
        geodesic_equation.move_to(np.array([0, 0, 1.5]))
        
        self.play(Write(geodesic_equation))
        self.wait(2)
        
        # Show moving point along the curve
        moving_point = Dot3D(radius=0.1, color=YELLOW)
        moving_point.move_to(curve_points[0])
        
        self.play(FadeIn(moving_point))
        
        # Animate the point along the curve
        self.play(MoveAlongPath(moving_point, curve_path, run_time=4))
        self.wait(1)
        
        # Show connection properties in 3D
        properties_text = VGroup(
            Text("3D Affine Connection Properties:", font_size=20, color=WHITE),
            Text("• ∇_X(Y+Z) = ∇_X Y + ∇_X Z (linearity)", font_size=16, color=BLUE),
            Text("• ∇_(fX) Y = f ∇_X Y (tensor product rule)", font_size=16, color=GREEN),
            Text("• ∇_X(fY) = X(f)Y + f ∇_X Y (Leibniz rule)", font_size=16, color=YELLOW),
            Text("• Parallel transport preserves vector length", font_size=16, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.add_fixed_in_frame_mobjects(properties_text)
        self.play(FadeOut(transport_equation), FadeOut(geodesic_equation))
        self.play(Write(properties_text))
        self.wait(3)
        
        # Show torsion and curvature in 3D
        curvature_text = VGroup(
            Text("3D Torsion & Curvature:", font_size=20, color=WHITE),
            Text("• T(X,Y) = ∇_X Y - ∇_Y X - [X,Y] (torsion)", font_size=16, color=BLUE),
            Text("• R(X,Y)Z = ∇_X ∇_Y Z - ∇_Y ∇_X Z - ∇_[X,Y] Z (curvature)", font_size=16, color=GREEN),
            Text("• Surface curvature affects parallel transport", font_size=16, color=YELLOW),
            Text("• Geodesics follow surface curvature", font_size=16, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.add_fixed_in_frame_mobjects(curvature_text)
        self.play(FadeOut(properties_text))
        self.play(Write(curvature_text))
        self.wait(3)
        
        # Final explanation
        final_text = VGroup(
            Text("The 3D affine connection ∇ defines how to transport vectors", font_size=20, color=YELLOW),
            Text("along curves on the curved surface", font_size=20, color=YELLOW),
            Text("It determines geodesics and parallel transport in 3D", font_size=18, color=BLUE)
        ).arrange(DOWN, buff=0.4).to_edge(DOWN)
        
        self.add_fixed_in_frame_mobjects(final_text)
        self.play(FadeOut(curvature_text))
        self.play(Write(final_text))
        self.wait(3)
        
        # Rotate camera to show 3D structure
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.wait(1)
