from manim import *
import numpy as np

class MetricProjection(Scene):
    def construct(self):
        # Set up the scene
        title = Text("Metric Tensor Projection", font_size=32, color=WHITE).to_edge(UP)
        subtitle = Text("How curved geometry appears in flat coordinates", font_size=20, color=BLUE).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        
        # Create coordinate systems
        # Left: Curved manifold with metric
        left_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=4,
            y_length=4
        )
        left_axes.move_to(LEFT * 3)
        
        # Right: Euclidean projection
        right_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=4,
            y_length=4
        )
        right_axes.move_to(RIGHT * 3)
        
        # Add labels
        left_label = Text("Curved Manifold\n(Metric g_μν)", font_size=18, color=RED).next_to(left_axes, DOWN)
        right_label = Text("Euclidean Projection\n(Flat Metric δ_μν)", font_size=18, color=GREEN).next_to(right_axes, DOWN)
        
        # Create the curved coordinate system (polar-like coordinates)
        def curved_coordinates(r, theta):
            # This creates a curved coordinate system
            x = r * np.cos(theta) * (1 + 0.2 * r**2)
            y = r * np.sin(theta) * (1 + 0.2 * r**2)
            return np.array([x, y])
        
        # Create coordinate grid for curved space
        curved_grid = VGroup()
        
        # Radial lines
        for theta in np.linspace(0, 2*np.pi, 8, endpoint=False):
            points = [curved_coordinates(r, theta) for r in np.linspace(0, 2, 20)]
            points = [left_axes.c2p(p[0], p[1], 0) for p in points]
            line = VMobject()
            line.set_points_as_corners(points)
            line.set_color(BLUE)
            line.set_stroke(width=2)
            curved_grid.add(line)
        
        # Concentric curves
        for r in np.linspace(0.5, 2, 4):
            points = [curved_coordinates(r, theta) for theta in np.linspace(0, 2*np.pi, 50)]
            points = [left_axes.c2p(p[0], p[1], 0) for p in points]
            line = VMobject()
            line.set_points_as_corners(points)
            line.set_color(RED)
            line.set_stroke(width=2)
            curved_grid.add(line)
        
        # Create regular grid for Euclidean space
        euclidean_grid = VGroup()
        
        # Vertical lines
        for x in np.linspace(-2, 2, 9):
            line = Line(
                start=right_axes.c2p(x, -2, 0),
                end=right_axes.c2p(x, 2, 0),
                color=BLUE,
                stroke_width=2
            )
            euclidean_grid.add(line)
        
        # Horizontal lines
        for y in np.linspace(-2, 2, 9):
            line = Line(
                start=right_axes.c2p(-2, y, 0),
                end=right_axes.c2p(2, y, 0),
                color=RED,
                stroke_width=2
            )
            euclidean_grid.add(line)
        
        # Show coordinate systems
        self.play(Create(left_axes), Create(right_axes))
        self.play(Write(left_label), Write(right_label))
        self.wait(1)
        
        # Show grids
        self.play(Create(curved_grid))
        self.play(Create(euclidean_grid))
        self.wait(1)
        
        # Create metric tensor representations
        # Curved metric (varies with position)
        curved_metric = VGroup()
        positions = [(-1, -1), (0, 0), (1, 1), (-1, 1), (1, -1)]
        
        for pos in positions:
            x, y = pos
            r = np.sqrt(x**2 + y**2)
            # Metric components that vary with position
            g_11 = 1 + 0.3 * r**2  # g_xx
            g_22 = 1 + 0.3 * r**2  # g_yy
            g_12 = 0.1 * r  # g_xy
            
            metric_text = MathTex(
                f"g = \\begin{{pmatrix}} {g_11:.2f} & {g_12:.2f} \\\\ {g_12:.2f} & {g_22:.2f} \\end{{pmatrix}}",
                font_size=14,
                color=YELLOW
            )
            metric_text.move_to(left_axes.c2p(x, y, 0) + UP * 0.3)
            curved_metric.add(metric_text)
        
        # Euclidean metric (constant)
        euclidean_metric = MathTex(
            "g = \\begin{pmatrix} 1 & 0 \\\\ 0 & 1 \\end{pmatrix}",
            font_size=20,
            color=GREEN
        )
        euclidean_metric.move_to(right_axes.get_center() + UP * 0.5)
        
        # Show metrics
        self.play(Write(euclidean_metric))
        self.play(*[Write(metric) for metric in curved_metric])
        self.wait(2)
        
        # Create geodesic curves
        def curved_geodesic(t):
            # A geodesic in curved space
            r = 1.5
            theta = t
            return curved_coordinates(r, theta)
        
        curved_path = ParametricFunction(
            lambda t: left_axes.c2p(*curved_geodesic(t), 0),
            t_range=[0, 2*np.pi],
            color=YELLOW,
            stroke_width=4
        )
        
        # Project to Euclidean space
        euclidean_path = Circle(
            radius=1.5,
            color=YELLOW,
            stroke_width=4
        )
        euclidean_path.move_to(right_axes.get_center())
        
        # Show geodesics
        self.play(Create(curved_path), Create(euclidean_path))
        self.wait(1)
        
        # Add projection arrows
        projection_arrows = []
        for i in range(6):
            t = i * np.pi / 3
            point_curved = curved_geodesic(t)
            point_curved = left_axes.c2p(*point_curved, 0)
            
            point_euclidean = euclidean_path.point_at_angle(t)
            point_euclidean = right_axes.get_center() + point_euclidean - euclidean_path.get_center()
            
            arrow = Arrow(
                start=point_curved,
                end=point_euclidean,
                color=WHITE,
                stroke_width=2,
                buff=0.1
            )
            projection_arrows.append(arrow)
        
        self.play(*[FadeIn(arrow) for arrow in projection_arrows])
        self.wait(1)
        
        # Show metric transformation
        transformation_text = VGroup(
            Text("Metric Transformation:", font_size=20, color=WHITE),
            Text("g'_μν = (∂x^α/∂x'^μ) (∂x^β/∂x'^ν) g_αβ", font_size=16, color=YELLOW),
            Text("Curved coordinates → Flat coordinates", font_size=16, color=BLUE)
        ).arrange(DOWN, buff=0.2).to_edge(DOWN)
        
        self.play(Write(transformation_text))
        self.wait(2)
        
        # Show moving points
        self.play(FadeOut(*projection_arrows))
        
        moving_point_curved = Dot(color=YELLOW, radius=0.08)
        # Position at the start of the curved path
        start_point = curved_geodesic(0)
        moving_point_curved.move_to(left_axes.c2p(*start_point, 0))
        
        moving_point_euclidean = Dot(color=YELLOW, radius=0.08)
        # Position at the start of the euclidean path
        moving_point_euclidean.move_to(right_axes.c2p(1.5, 0, 0))
        
        self.play(FadeIn(moving_point_curved), FadeIn(moving_point_euclidean))
        
        # Animate points
        self.play(
            MoveAlongPath(moving_point_curved, curved_path, run_time=4),
            MoveAlongPath(moving_point_euclidean, euclidean_path, run_time=4)
        )
        self.wait(1)
        
        # Final explanation
        final_text = VGroup(
            Text("The projection shows how curved geometry", font_size=20, color=YELLOW),
            Text("manifests as metric distortion in flat coordinates", font_size=20, color=YELLOW),
            Text("This is the essence of general relativity", font_size=18, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(transformation_text))
        self.play(Write(final_text))
        self.wait(3)
