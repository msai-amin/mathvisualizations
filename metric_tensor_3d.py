from manim import *
import numpy as np

class MetricTensor3D(ThreeDScene):
    def construct(self):
        # Set up the 3D scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        
        # Title
        title = Text("3D Metric Tensor g on Curved Manifold", font_size=28, color=WHITE).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        # Create a 3D curved manifold surface
        def manifold_surface(u, v):
            # Create a curved surface: hyperbolic paraboloid with modulation
            x = u
            y = v
            z = 0.1 * (u**2 - v**2) + 0.05 * np.sin(2*np.pi*u) * np.cos(2*np.pi*v)
            return np.array([x, y, z])
        
        # Create the surface
        surface = Surface(
            lambda u, v: manifold_surface(u, v),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(30, 30)
        )
        surface.set_style(fill_opacity=0.3, stroke_width=1, stroke_color=BLUE)
        
        # Show the surface
        self.play(Create(surface))
        self.wait(1)
        
        # Create coordinate grid on the surface
        u_lines = []
        for u_val in np.linspace(-3, 3, 7):
            u_lines.append(ParametricFunction(
                lambda t: manifold_surface(u_val, t),
                t_range=[-3, 3],
                color=RED,
                stroke_width=2
            ))
        
        v_lines = []
        for v_val in np.linspace(-3, 3, 7):
            v_lines.append(ParametricFunction(
                lambda t: manifold_surface(t, v_val),
                t_range=[-3, 3],
                color=GREEN,
                stroke_width=2
            ))
        
        # Show coordinate grid
        self.play(*[Create(line) for line in u_lines + v_lines])
        self.wait(1)
        
        # Create metric tensor function for 3D surface
        def metric_tensor_3d(u, v):
            # For a 3D surface, the metric is induced from the embedding
            # g_ij = ∂ᵢr · ∂ⱼr where r(u,v) is the surface parameterization
            
            # Calculate tangent vectors
            du = np.array([1, 0, 0.2*u + 0.1*np.pi*np.cos(2*np.pi*u)*np.cos(2*np.pi*v)])
            dv = np.array([0, 1, -0.2*v - 0.1*np.pi*np.sin(2*np.pi*u)*np.sin(2*np.pi*v)])
            
            # Calculate metric components
            g_11 = np.dot(du, du)  # g_uu
            g_12 = np.dot(du, dv)  # g_uv
            g_21 = g_12            # g_vu (symmetric)
            g_22 = np.dot(dv, dv)  # g_vv
            
            return np.array([[g_11, g_12], [g_21, g_22]])
        
        # Show metric tensor at different points
        metric_points = [(-2, -2), (0, 0), (2, 2), (-2, 2), (2, -2)]
        metric_displays = VGroup()
        
        for point in metric_points:
            u, v = point
            G = metric_tensor_3d(u, v)
            
            # Create metric matrix display
            metric_text = MathTex(
                f"g = \\begin{{pmatrix}} {G[0,0]:.2f} & {G[0,1]:.2f} \\\\ {G[1,0]:.2f} & {G[1,1]:.2f} \\end{{pmatrix}}",
                font_size=12,
                color=YELLOW
            )
            
            # Position at the 3D point
            point_3d = manifold_surface(u, v)
            metric_text.move_to(point_3d + np.array([0, 0, 0.5]))
            metric_displays.add(metric_text)
        
        # Show metric tensors
        self.play(*[Write(metric) for metric in metric_displays])
        self.wait(2)
        
        # Create tangent vectors at a point
        base_point = np.array([1, 1])
        base_point_3d = manifold_surface(base_point[0], base_point[1])
        
        # Calculate tangent vectors
        du = np.array([1, 0, 0.2*base_point[0] + 0.1*np.pi*np.cos(2*np.pi*base_point[0])*np.cos(2*np.pi*base_point[1])])
        dv = np.array([0, 1, -0.2*base_point[1] - 0.1*np.pi*np.sin(2*np.pi*base_point[0])*np.sin(2*np.pi*base_point[1])])
        
        # Normalize tangent vectors
        du_norm = du / np.linalg.norm(du)
        dv_norm = dv / np.linalg.norm(dv)
        
        # Create tangent vector arrows
        tangent_u = Arrow3D(
            start=base_point_3d,
            end=base_point_3d + 0.5 * du_norm,
            color=RED,
            thickness=0.05
        )
        
        tangent_v = Arrow3D(
            start=base_point_3d,
            end=base_point_3d + 0.5 * dv_norm,
            color=GREEN,
            thickness=0.05
        )
        
        # Show tangent vectors
        self.play(Create(tangent_u), Create(tangent_v))
        self.wait(1)
        
        # Create a geodesic curve on the surface
        def geodesic_curve(t):
            # Approximate geodesic: follows the surface curvature
            u = 2 * np.cos(t)
            v = 2 * np.sin(t)
            return manifold_surface(u, v)
        
        # Create the geodesic
        t_vals = np.linspace(0, 2*np.pi, 100)
        geodesic_points = [geodesic_curve(t) for t in t_vals]
        
        geodesic_path = ParametricFunction(
            lambda t: geodesic_curve(t),
            t_range=[0, 2*np.pi],
            color=YELLOW,
            stroke_width=4
        )
        
        # Show geodesic
        self.play(Create(geodesic_path))
        self.wait(1)
        
        # Calculate distance along the geodesic using the metric
        def calculate_geodesic_distance(metric_func):
            total_distance = 0
            for i in range(len(t_vals) - 1):
                t1, t2 = t_vals[i], t_vals[i+1]
                u1, v1 = 2*np.cos(t1), 2*np.sin(t1)
                u2, v2 = 2*np.cos(t2), 2*np.sin(t2)
                
                # Get metric at current point
                G = metric_func(u1, v1)
                
                # Calculate infinitesimal displacement
                du = u2 - u1
                dv = v2 - v1
                delta = np.array([du, dv])
                
                # Calculate distance: ds² = δx^T G δx
                ds_squared = delta.T @ G @ delta
                ds = np.sqrt(ds_squared)
                total_distance += ds
            
            return total_distance
        
        # Calculate distance
        distance = calculate_geodesic_distance(metric_tensor_3d)
        
        # Show distance calculation
        distance_text = VGroup(
            Text("Geodesic Distance:", font_size=20, color=WHITE),
            Text(f"ds² = g_μν dx^μ dx^ν", font_size=18, color=YELLOW),
            Text(f"Total distance = {distance:.3f}", font_size=18, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.add_fixed_in_frame_mobjects(distance_text)
        self.play(Write(distance_text))
        self.wait(2)
        
        # Show metric evolution along the geodesic
        metric_evolution = VGroup()
        sample_times = [0, 0.25, 0.5, 0.75, 1.0]
        
        for t in sample_times:
            t_val = t * 2 * np.pi
            u, v = 2*np.cos(t_val), 2*np.sin(t_val)
            G = metric_tensor_3d(u, v)
            
            metric_text = MathTex(
                f"g = \\begin{{pmatrix}} {G[0,0]:.2f} & {G[0,1]:.2f} \\\\ {G[1,0]:.2f} & {G[1,1]:.2f} \\end{{pmatrix}}",
                font_size=10,
                color=YELLOW
            )
            
            # Position along the geodesic
            point_3d = geodesic_curve(t_val)
            metric_text.move_to(point_3d + np.array([0.5, 0.5, 0.3]))
            metric_evolution.add(metric_text)
        
        self.play(*[Write(metric) for metric in metric_evolution])
        self.wait(2)
        
        # Show moving point along the geodesic
        moving_point = Dot3D(radius=0.1, color=YELLOW)
        moving_point.move_to(geodesic_points[0])
        
        self.play(FadeIn(moving_point))
        
        # Animate the point along the geodesic
        self.play(MoveAlongPath(moving_point, geodesic_path, run_time=4))
        self.wait(1)
        
        # Show metric tensor properties in 3D
        properties_text = VGroup(
            Text("3D Metric Tensor Properties:", font_size=20, color=WHITE),
            Text("• Induced from embedding: g_ij = ∂ᵢr · ∂ⱼr", font_size=16, color=BLUE),
            Text("• Defines surface geometry and curvature", font_size=16, color=GREEN),
            Text("• Determines geodesics and distances", font_size=16, color=YELLOW),
            Text("• Volume element: dV = √|det g| du dv", font_size=16, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.add_fixed_in_frame_mobjects(properties_text)
        self.play(FadeOut(distance_text))
        self.play(Write(properties_text))
        self.wait(3)
        
        # Final explanation
        final_text = VGroup(
            Text("The 3D metric tensor g defines the intrinsic geometry", font_size=20, color=YELLOW),
            Text("of the curved surface, determining distances and angles", font_size=20, color=YELLOW),
            Text("in the surface's own coordinate system", font_size=18, color=BLUE)
        ).arrange(DOWN, buff=0.4).to_edge(DOWN)
        
        self.add_fixed_in_frame_mobjects(final_text)
        self.play(FadeOut(properties_text))
        self.play(Write(final_text))
        self.wait(3)
        
        # Rotate camera to show 3D structure
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait(1)
