from manim import *
import numpy as np

class ManifoldProjection(Scene):
    def construct(self):
        # Set up the scene
        title = Text("Manifold Projection in Euclidean Space", font_size=32, color=WHITE).to_edge(UP)
        self.play(Write(title))
        
        # Create coordinate systems
        # Left side: Curved manifold in 3D
        left_axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1, 2, 0.5],
            x_length=4,
            y_length=4,
            z_length=3
        )
        
        # Right side: 2D Euclidean projection
        right_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4,
            y_length=4
        )
        
        # Position the coordinate systems
        left_axes.move_to(LEFT * 3)
        right_axes.move_to(RIGHT * 3)
        
        # Add labels
        left_label = Text("3D Curved Manifold", font_size=20, color=BLUE).next_to(left_axes, DOWN)
        right_label = Text("2D Euclidean Projection", font_size=20, color=GREEN).next_to(right_axes, DOWN)
        
        # Create the curved surface (hyperbolic paraboloid)
        def manifold_surface(u, v):
            x = u
            y = v
            z = 0.1 * (u**2 - v**2)
            return np.array([x, y, z])
        
        # Create surface for 3D view
        surface_3d = Surface(
            lambda u, v: manifold_surface(u, v),
            u_range=[-2.5, 2.5],
            v_range=[-2.5, 2.5],
            resolution=(15, 15)
        )
        surface_3d.set_style(
            fill_opacity=0.3,
            stroke_width=1,
            stroke_color=BLUE
        )
        surface_3d.move_to(LEFT * 3)
        
        # Create coordinate grid on the manifold
        u_lines_3d = []
        v_lines_3d = []
        
        for u_val in np.linspace(-2.5, 2.5, 6):
            line = ParametricFunction(
                lambda t: manifold_surface(u_val, t),
                t_range=[-2.5, 2.5],
                color=RED,
                stroke_width=2
            )
            line.move_to(LEFT * 3)
            u_lines_3d.append(line)
        
        for v_val in np.linspace(-2.5, 2.5, 6):
            line = ParametricFunction(
                lambda t: manifold_surface(t, v_val),
                t_range=[-2.5, 2.5],
                color=GREEN,
                stroke_width=2
            )
            line.move_to(LEFT * 3)
            v_lines_3d.append(line)
        
        # Create 2D projection (just the u,v coordinates)
        def projection_2d(u, v):
            return np.array([u, v, 0])
        
        # Create projected coordinate grid
        u_lines_2d = []
        v_lines_2d = []
        
        for u_val in np.linspace(-2.5, 2.5, 6):
            line = Line(
                start=right_axes.c2p(u_val, -2.5, 0),
                end=right_axes.c2p(u_val, 2.5, 0),
                color=RED,
                stroke_width=2
            )
            u_lines_2d.append(line)
        
        for v_val in np.linspace(-2.5, 2.5, 6):
            line = Line(
                start=right_axes.c2p(-2.5, v_val, 0),
                end=right_axes.c2p(2.5, v_val, 0),
                color=GREEN,
                stroke_width=2
            )
            v_lines_2d.append(line)
        
        # Create geodesic curves
        def geodesic_curve(t):
            u = 2 * np.cos(t)
            v = 2 * np.sin(t)
            return manifold_surface(u, v)
        
        geodesic_3d = ParametricFunction(
            lambda t: geodesic_curve(t),
            t_range=[0, 2*np.pi],
            color=YELLOW,
            stroke_width=4
        )
        geodesic_3d.move_to(LEFT * 3)
        
        # Project the geodesic to 2D
        geodesic_2d = ParametricFunction(
            lambda t: right_axes.c2p(2*np.cos(t), 2*np.sin(t), 0),
            t_range=[0, 2*np.pi],
            color=YELLOW,
            stroke_width=4
        )
        
        # Create another geodesic (straight line in parameter space)
        def geodesic_straight(t):
            u = t
            v = t
            return manifold_surface(u, v)
        
        geodesic_straight_3d = ParametricFunction(
            lambda t: geodesic_straight(t),
            t_range=[-2, 2],
            color=ORANGE,
            stroke_width=4
        )
        geodesic_straight_3d.move_to(LEFT * 3)
        
        # Project the straight geodesic to 2D
        geodesic_straight_2d = Line(
            start=right_axes.c2p(-2, -2, 0),
            end=right_axes.c2p(2, 2, 0),
            color=ORANGE,
            stroke_width=4
        )
        
        # Animation sequence
        # Show coordinate systems
        self.play(Create(left_axes), Create(right_axes))
        self.play(Write(left_label), Write(right_label))
        self.wait(1)
        
        # Show 3D surface
        self.play(Create(surface_3d))
        self.wait(1)
        
        # Show coordinate grids
        self.play(*[Create(line) for line in u_lines_3d + v_lines_3d])
        self.play(*[Create(line) for line in u_lines_2d + v_lines_2d])
        self.wait(1)
        
        # Show geodesics
        self.play(Create(geodesic_3d), Create(geodesic_2d))
        self.wait(0.5)
        self.play(Create(geodesic_straight_3d), Create(geodesic_straight_2d))
        self.wait(1)
        
        # Add simple projection arrows (simplified to avoid coordinate issues)
        projection_text = Text("Projection: 3D → 2D", font_size=20, color=WHITE)
        projection_text.move_to(ORIGIN + UP * 0.5)
        self.play(Write(projection_text))
        self.wait(1)
        
        # Add mathematical explanation
        explanation = VGroup(
            Text("Projection from curved manifold to flat space:", font_size=20),
            Text("• 3D curved surface → 2D flat plane", font_size=16),
            Text("• Geodesics become curved in projection", font_size=16),
            Text("• Coordinate grid becomes regular", font_size=16),
            Text("• Metric distortion shows curvature", font_size=16)
        ).arrange(DOWN, buff=0.2).to_edge(DOWN)
        
        self.play(FadeOut(projection_text))
        self.play(Write(explanation))
        self.wait(2)
        
        # Show moving points
        # Create a moving point that shows the projection
        moving_point_3d = Dot3D(radius=0.08, color=YELLOW)
        moving_point_3d.move_to(manifold_surface(0, 0) + LEFT * 3)
        
        moving_point_2d = Dot(color=YELLOW, radius=0.08)
        moving_point_2d.move_to(right_axes.c2p(0, 0, 0))
        
        self.play(FadeIn(moving_point_3d), FadeIn(moving_point_2d))
        
        # Animate the points along the geodesic
        path_3d = ParametricFunction(
            lambda t: geodesic_curve(t),
            t_range=[0, 2*np.pi],
            color=YELLOW,
            stroke_width=2
        )
        path_3d.move_to(LEFT * 3)
        
        path_2d = ParametricFunction(
            lambda t: right_axes.c2p(2*np.cos(t), 2*np.sin(t), 0),
            t_range=[0, 2*np.pi],
            color=YELLOW,
            stroke_width=2
        )
        
        self.play(
            MoveAlongPath(moving_point_3d, path_3d, run_time=4),
            MoveAlongPath(moving_point_2d, path_2d, run_time=4)
        )
        self.wait(1)
        
        # Final explanation
        final_text = VGroup(
            Text("The projection reveals how curved geometry", font_size=20, color=YELLOW),
            Text("appears distorted in Euclidean coordinates", font_size=20, color=YELLOW)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(explanation))
        self.play(Write(final_text))
        self.wait(3)
