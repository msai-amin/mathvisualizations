from manim import *
import numpy as np

class NonEuclideanManifold(ThreeDScene):
    def construct(self):
        # Set up 3D camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        
        # Create a curved 2D manifold (hyperbolic paraboloid)
        def manifold_surface(u, v):
            x = u
            y = v
            z = 0.1 * (u**2 - v**2)  # Hyperbolic paraboloid
            return np.array([x, y, z])
        
        # Create the surface using surface
        surface = Surface(
            lambda u, v: manifold_surface(u, v),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(20, 20)
        )
        surface.set_style(
            fill_opacity=0.3,
            stroke_width=1,
            stroke_color=BLUE
        )
        
        # Create coordinate grid on the manifold
        u_lines = []
        v_lines = []
        
        for u_val in np.linspace(-3, 3, 7):
            line = ParametricFunction(
                lambda t: manifold_surface(u_val, t),
                t_range=[-3, 3],
                color=RED,
                stroke_width=2
            )
            u_lines.append(line)
        
        for v_val in np.linspace(-3, 3, 7):
            line = ParametricFunction(
                lambda t: manifold_surface(t, v_val),
                t_range=[-3, 3],
                color=GREEN,
                stroke_width=2
            )
            v_lines.append(line)
        
        # Create geodesic curves (approximated)
        def geodesic_curve(t):
            # A geodesic on the hyperbolic paraboloid
            u = 2 * np.cos(t)
            v = 2 * np.sin(t)
            return manifold_surface(u, v)
        
        geodesic = ParametricFunction(
            lambda t: geodesic_curve(t),
            t_range=[0, 2*np.pi],
            color=YELLOW,
            stroke_width=4
        )
        
        # Create another geodesic (straight line in parameter space)
        def geodesic_straight(t):
            u = t
            v = t
            return manifold_surface(u, v)
        
        geodesic_straight_line = ParametricFunction(
            lambda t: geodesic_straight(t),
            t_range=[-2, 2],
            color=ORANGE,
            stroke_width=4
        )
        
        # Create tangent vectors at a point
        def tangent_vectors(u, v):
            # Partial derivatives
            du = np.array([1, 0, 0.2 * u])
            dv = np.array([0, 1, -0.2 * v])
            
            # Normalize
            du = du / np.linalg.norm(du)
            dv = dv / np.linalg.norm(dv)
            
            return du, dv
        
        # Create tangent vectors at point (1, 1)
        du, dv = tangent_vectors(1, 1)
        point = manifold_surface(1, 1)
        
        tangent_u = Arrow3D(
            start=point,
            end=point + 0.5 * du,
            color=RED,
            thickness=0.05
        )
        tangent_v = Arrow3D(
            start=point,
            end=point + 0.5 * dv,
            color=GREEN,
            thickness=0.05
        )
        
        # Create a moving point that follows a geodesic
        moving_point = Dot3D(radius=0.1, color=YELLOW)
        moving_point.move_to(manifold_surface(0, 0))
        
        # Animation sequence
        title = Text("Non-Euclidean Manifold", font_size=36, color=WHITE).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        # Show the surface
        self.play(Create(surface))
        self.wait(1)
        
        # Show coordinate grid
        self.play(*[Create(line) for line in u_lines + v_lines])
        self.wait(1)
        
        # Show geodesics
        self.play(Create(geodesic))
        self.wait(0.5)
        self.play(Create(geodesic_straight_line))
        self.wait(1)
        
        # Show tangent vectors
        self.play(Create(tangent_u), Create(tangent_v))
        self.wait(1)
        
        # Animate moving point along geodesic
        self.play(FadeIn(moving_point))
        
        # Create path for moving point
        path = ParametricFunction(
            lambda t: geodesic_curve(t),
            t_range=[0, 4*np.pi],
            color=YELLOW,
            stroke_width=2
        )
        
        self.play(MoveAlongPath(moving_point, path, run_time=6))
        self.wait(1)
        
        # Add mathematical explanation
        explanation = VGroup(
            Text("This surface represents a 2D manifold", font_size=24),
            Text("embedded in 3D Euclidean space", font_size=24),
            Text("The red and green lines form a coordinate grid", font_size=24),
            Text("Yellow and orange curves are geodesics", font_size=24),
            Text("(shortest paths on the curved surface)", font_size=24)
        ).arrange(DOWN, buff=0.2).to_edge(DOWN)
        
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(Write(explanation))
        self.wait(3)
        
        # Rotate camera to show 3D structure
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.wait(1)
