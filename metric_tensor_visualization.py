from manim import *
import numpy as np

class MetricTensorVisualization(Scene):
    def construct(self):
        # Set up the scene
        title = Text("Metric Tensor g on Manifold", font_size=32, color=WHITE).to_edge(UP)
        subtitle = Text("Defining Distances, Angles & Volumes", font_size=20, color=BLUE).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        
        # Create coordinate systems
        # Left: Manifold with metric tensor
        left_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=4,
            y_length=4
        )
        left_axes.move_to(LEFT * 3)
        
        # Right: Metric tensor components
        right_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=4,
            y_length=4
        )
        right_axes.move_to(RIGHT * 3)
        
        # Add labels
        left_label = Text("Manifold M\nwith Metric g", font_size=18, color=RED).next_to(left_axes, DOWN)
        right_label = Text("Metric Components\ng_μν(x, y)", font_size=18, color=GREEN).next_to(right_axes, DOWN)
        
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
        
        # Create metric tensor function
        def metric_tensor(x, y):
            # Example metric: ds² = (1 + 0.2x²)dx² + (1 + 0.2y²)dy² + 0.1xy dx dy
            # This creates a position-dependent metric
            g_11 = 1 + 0.2 * x**2  # coefficient of dx²
            g_22 = 1 + 0.2 * y**2  # coefficient of dy²
            g_12 = 0.1 * x * y     # coefficient of dx dy
            g_21 = g_12             # symmetric metric
            return np.array([[g_11, g_12], [g_21, g_22]])
        
        # Show metric tensor at different points
        metric_points = [(-1.5, -1.5), (0, 0), (1.5, 1.5), (-1.5, 1.5), (1.5, -1.5)]
        metric_displays = VGroup()
        
        for point in metric_points:
            x, y = point
            G = metric_tensor(x, y)
            
            # Create metric matrix display
            metric_text = MathTex(
                f"g = \\begin{{pmatrix}} {G[0,0]:.2f} & {G[0,1]:.2f} \\\\ {G[1,0]:.2f} & {G[1,1]:.2f} \\end{{pmatrix}}",
                font_size=12,
                color=YELLOW
            )
            
            # Position at the point
            point_pos = left_axes.c2p(x, y, 0)
            metric_text.move_to(point_pos + UP * 0.4)
            metric_displays.add(metric_text)
        
        # Show metric tensors
        self.play(*[Write(metric) for metric in metric_displays])
        self.wait(2)
        
        # Create distance calculation visualization
        # Show two points and calculate distance
        point1 = np.array([-1, -1])
        point2 = np.array([1, 1])
        
        # Create points
        dot1 = Dot(point=left_axes.c2p(point1[0], point1[1], 0), color=RED, radius=0.08)
        dot2 = Dot(point=left_axes.c2p(point2[0], point2[1], 0), color=BLUE, radius=0.08)
        
        # Add labels
        point1_label = Text("P₁", font_size=16, color=RED)
        point1_label.move_to(left_axes.c2p(point1[0], point1[1], 0) + UP * 0.3)
        
        point2_label = Text("P₂", font_size=16, color=BLUE)
        point2_label.move_to(left_axes.c2p(point2[0], point2[1], 0) + UP * 0.3)
        
        self.play(FadeIn(dot1), FadeIn(dot2))
        self.play(Write(point1_label), Write(point2_label))
        self.wait(1)
        
        # Create path between points
        path_points = []
        for t in np.linspace(0, 1, 50):
            x = point1[0] + t * (point2[0] - point1[0])
            y = point1[1] + t * (point2[1] - point1[1])
            path_points.append(np.array([x, y]))
        
        path_coords = [left_axes.c2p(p[0], p[1], 0) for p in path_points]
        
        geodesic_path = VMobject()
        geodesic_path.set_points_as_corners(path_coords)
        geodesic_path.set_color(YELLOW)
        geodesic_path.set_stroke(width=3)
        
        # Show geodesic path
        self.play(Create(geodesic_path))
        self.wait(1)
        
        # Calculate distance using metric tensor
        def calculate_distance(point1, point2, metric_func):
            # Approximate distance by integrating along path
            path_points = []
            for t in np.linspace(0, 1, 100):
                x = point1[0] + t * (point2[0] - point1[0])
                y = point1[1] + t * (point2[1] - point1[1])
                path_points.append(np.array([x, y]))
            
            total_distance = 0
            for i in range(len(path_points) - 1):
                current_point = path_points[i]
                next_point = path_points[i + 1]
                delta = next_point - current_point
                
                # Get metric at current point
                G = metric_func(current_point[0], current_point[1])
                
                # Calculate infinitesimal distance: ds² = δx^T G δx
                ds_squared = delta.T @ G @ delta
                ds = np.sqrt(ds_squared)
                total_distance += ds
            
            return total_distance
        
        # Calculate distance
        distance = calculate_distance(point1, point2, metric_tensor)
        
        # Show distance calculation
        distance_text = VGroup(
            Text("Distance Calculation:", font_size=20, color=WHITE),
            Text(f"ds² = g_μν dx^μ dx^ν", font_size=18, color=YELLOW),
            Text(f"Distance = {distance:.3f}", font_size=18, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(Write(distance_text))
        self.wait(2)
        
        # Show metric tensor evolution along the path
        metric_evolution = VGroup()
        sample_points = [0, 0.25, 0.5, 0.75, 1.0]
        
        for t in sample_points:
            point = path_points[int(t * (len(path_points) - 1))]
            G = metric_tensor(point[0], point[1])
            
            metric_text = MathTex(
                f"g = \\begin{{pmatrix}} {G[0,0]:.2f} & {G[0,1]:.2f} \\\\ {G[1,0]:.2f} & {G[1,1]:.2f} \\end{{pmatrix}}",
                font_size=10,
                color=YELLOW
            )
            
            # Position along the path
            path_pos = left_axes.c2p(point[0], point[1], 0)
            metric_text.move_to(path_pos + RIGHT * 0.6)
            metric_evolution.add(metric_text)
        
        self.play(*[Write(metric) for metric in metric_evolution])
        self.wait(2)
        
        # Show moving point along the geodesic
        moving_point = Dot(color=YELLOW, radius=0.08)
        moving_point.move_to(path_coords[0])
        
        self.play(FadeIn(moving_point))
        
        # Animate the point along the path
        self.play(MoveAlongPath(moving_point, geodesic_path, run_time=4))
        self.wait(1)
        
        # Show metric tensor properties
        properties_text = VGroup(
            Text("Metric Tensor Properties:", font_size=20, color=WHITE),
            Text("• g_μν = g_νμ (symmetric)", font_size=16, color=BLUE),
            Text("• ds² = g_μν dx^μ dx^ν > 0 (positive definite)", font_size=16, color=GREEN),
            Text("• Defines angles: cos θ = g(u,v)/√(g(u,u)g(v,v))", font_size=16, color=YELLOW),
            Text("• Volume element: dV = √|det g| dx^1...dx^n", font_size=16, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(distance_text))
        self.play(Write(properties_text))
        self.wait(3)
        
        # Final explanation
        final_text = VGroup(
            Text("The metric tensor g defines the geometry of the manifold", font_size=20, color=YELLOW),
            Text("It determines distances, angles, and volumes", font_size=18, color=BLUE),
            Text("Position-dependent metrics create curved geometry", font_size=18, color=GREEN)
        ).arrange(DOWN, buff=0.4).to_edge(DOWN)
        
        self.play(FadeOut(properties_text))
        self.play(Write(final_text))
        self.wait(3)
