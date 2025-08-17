from manim import *
import numpy as np

class TorusManifold(ThreeDScene):
    def construct(self):
        # Set up 3D camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        
        # Create a torus manifold
        def torus_surface(u, v):
            R = 2  # Major radius
            r = 0.8  # Minor radius
            x = (R + r * np.cos(v)) * np.cos(u)
            y = (R + r * np.cos(v)) * np.sin(u)
            z = r * np.sin(v)
            return np.array([x, y, z])
        
        # Create the torus surface
        torus = Surface(
            lambda u, v: torus_surface(u, v),
            u_range=[0, 2*np.pi],
            v_range=[0, 2*np.pi],
            resolution=(30, 30)
        )
        torus.set_style(
            fill_opacity=0.3,
            stroke_width=1,
            stroke_color=BLUE
        )
        
        # Create coordinate grid on the torus
        u_lines = []
        v_lines = []
        
        # Longitudinal lines (around the major circle)
        for u_val in np.linspace(0, 2*np.pi, 8, endpoint=False):
            line = ParametricFunction(
                lambda t: torus_surface(u_val, t),
                t_range=[0, 2*np.pi],
                color=RED,
                stroke_width=2
            )
            u_lines.append(line)
        
        # Latitudinal lines (around the minor circle)
        for v_val in np.linspace(0, 2*np.pi, 8, endpoint=False):
            line = ParametricFunction(
                lambda t: torus_surface(t, v_val),
                t_range=[0, 2*np.pi],
                color=GREEN,
                stroke_width=2
            )
            v_lines.append(line)
        
        # Create geodesic curves on the torus
        def geodesic_curve(t):
            # A geodesic that wraps around the torus
            u = 2 * t
            v = 3 * t
            return torus_surface(u, v)
        
        geodesic = ParametricFunction(
            lambda t: geodesic_curve(t),
            t_range=[0, 2*np.pi],
            color=YELLOW,
            stroke_width=4
        )
        
        # Create another geodesic (meridian)
        def meridian_geodesic(t):
            u = t
            v = 0
            return torus_surface(u, v)
        
        meridian = ParametricFunction(
            lambda t: meridian_geodesic(t),
            t_range=[0, 2*np.pi],
            color=ORANGE,
            stroke_width=4
        )
        
        # Create parallel transport demonstration
        def parallel_transport_curve(t):
            # A curve for parallel transport
            u = t
            v = np.pi/2 + 0.3 * np.sin(2*t)
            return torus_surface(u, v)
        
        parallel_curve = ParametricFunction(
            lambda t: parallel_transport_curve(t),
            t_range=[0, 2*np.pi],
            color=PURPLE,
            stroke_width=3
        )
        
        # Create a vector field that gets parallel transported
        vector_field = []
        t_vals = np.linspace(0, 2*np.pi, 12)
        for t in t_vals:
            point = parallel_transport_curve(t)
            # Create a tangent vector that changes as we move along the curve
            # This simulates parallel transport
            if t < np.pi:
                # First half: vector points in u direction
                direction = np.array([-np.sin(t), np.cos(t), 0])
            else:
                # Second half: vector points in v direction
                direction = np.array([0, 0, 1])
            
            # Normalize and scale
            direction = direction / np.linalg.norm(direction) * 0.3
            
            arrow = Arrow3D(
                start=point,
                end=point + direction,
                color=WHITE,
                thickness=0.03
            )
            vector_field.append(arrow)
        
        # Animation sequence
        title = Text("Torus Manifold with Non-Euclidean Geometry", font_size=28, color=WHITE).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        # Show the torus surface
        self.play(Create(torus))
        self.wait(1)
        
        # Show coordinate grid
        self.play(*[Create(line) for line in u_lines + v_lines])
        self.wait(1)
        
        # Show geodesics
        self.play(Create(geodesic))
        self.wait(0.5)
        self.play(Create(meridian))
        self.wait(1)
        
        # Show parallel transport curve
        self.play(Create(parallel_curve))
        self.wait(1)
        
        # Show vector field with parallel transport
        self.play(*[FadeIn(arrow) for arrow in vector_field])
        self.wait(1)
        
        # Add mathematical explanation
        explanation = VGroup(
            Text("This torus demonstrates non-Euclidean geometry:", font_size=20),
            Text("• Parallel lines can intersect (longitudinal lines)", font_size=16),
            Text("• Geodesics follow curved paths", font_size=16),
            Text("• Vector parallel transport shows curvature", font_size=16)
        ).arrange(DOWN, buff=0.2).to_edge(DOWN)
        
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(Write(explanation))
        self.wait(2)
        
        # Rotate camera to show 3D structure
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait(1)
        
        # Show how the manifold affects geometry
        final_text = Text("The torus has intrinsic curvature that affects", font_size=20, color=YELLOW)
        final_text2 = Text("all geometric measurements and parallel transport", font_size=20, color=YELLOW)
        final_text.to_edge(DOWN)
        final_text2.next_to(final_text, DOWN)
        
        self.add_fixed_in_frame_mobjects(final_text, final_text2)
        self.play(FadeOut(explanation))
        self.play(Write(final_text), Write(final_text2))
        self.wait(3)
