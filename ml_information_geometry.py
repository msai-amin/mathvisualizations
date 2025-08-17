from manim import *
import numpy as np

class MLInformationGeometry(Scene):
    def construct(self):
        # Set up the scene
        title = Text("Information Geometry in Machine Learning", font_size=32, color=WHITE).to_edge(UP)
        subtitle = Text("Natural Gradient Descent & Optimization", font_size=20, color=BLUE).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        
        # Create coordinate systems
        # Left: Parameter space with Fisher metric
        left_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=4,
            y_length=4
        )
        left_axes.move_to(LEFT * 3)
        
        # Right: Loss landscape and optimization paths
        right_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[0, 4, 0.5],
            x_length=4,
            y_length=4
        )
        right_axes.move_to(RIGHT * 3)
        
        # Add labels
        left_label = Text("Parameter Space\nwith Fisher Metric", font_size=18, color=RED).next_to(left_axes, DOWN)
        right_label = Text("Loss Landscape\n& Optimization", font_size=18, color=GREEN).next_to(right_axes, DOWN)
        
        # Create Fisher metric visualization
        fisher_metrics = VGroup()
        positions = [(-1, -1), (0, 0), (1, 1), (-1, 1), (1, -1)]
        
        for pos in positions:
            x, y = pos
            # Fisher metric components
            sigma = 1 + 0.2 * np.sqrt(x**2 + y**2)
            g_11 = 1 / (sigma**2)
            g_22 = 1 / (sigma**2)
            g_12 = 0.1 * np.sin(x + y)
            
            metric_text = MathTex(
                f"g = \\begin{{pmatrix}} {g_11:.2f} & {g_12:.2f} \\\\ {g_12:.2f} & {g_22:.2f} \\end{{pmatrix}}",
                font_size=10,
                color=YELLOW
            )
            metric_text.move_to(left_axes.c2p(x, y, 0) + UP * 0.3)
            fisher_metrics.add(metric_text)
        
        # Create coordinate grid
        param_grid = VGroup()
        
        # Vertical lines
        for x in np.linspace(-2, 2, 9):
            line = Line(
                start=left_axes.c2p(x, -2, 0),
                end=left_axes.c2p(x, 2, 0),
                color=BLUE,
                stroke_width=1
            )
            param_grid.add(line)
        
        # Horizontal lines
        for y in np.linspace(-2, 2, 9):
            line = Line(
                start=left_axes.c2p(-2, y, 0),
                end=left_axes.c2p(2, y, 0),
                color=RED,
                stroke_width=1
            )
            param_grid.add(line)
        
        # Create loss landscape
        def loss_function(x, y):
            # Example loss function: L = (x-1)² + (y-1)² + 0.5*sin(2πx)*sin(2πy)
            return (x-1)**2 + (y-1)**2 + 0.5 * np.sin(2*np.pi*x) * np.sin(2*np.pi*y)
        
        # Create contour plot of loss function
        loss_contours = VGroup()
        for level in np.linspace(0.5, 3.5, 6):
            # Create contour at this level
            contour_points = []
            for x in np.linspace(-2, 2, 100):
                for y in np.linspace(-2, 2, 100):
                    if abs(loss_function(x, y) - level) < 0.1:
                        contour_points.append(right_axes.c2p(x, level, 0))
            
            if len(contour_points) > 10:
                # Create contour line
                contour = VMobject()
                contour.set_points_as_corners(contour_points)
                contour.set_color(interpolate_color(BLUE, RED, (level - 0.5) / 3))
                contour.set_stroke(width=2)
                loss_contours.add(contour)
        
        # Show coordinate systems
        self.play(Create(left_axes), Create(right_axes))
        self.play(Write(left_label), Write(right_label))
        self.wait(1)
        
        # Show parameter grid and Fisher metrics
        self.play(Create(param_grid))
        self.play(*[Write(metric) for metric in fisher_metrics])
        self.wait(1)
        
        # Show loss landscape
        self.play(Create(loss_contours))
        self.wait(1)
        
        # Create optimization paths
        # Standard gradient descent
        def standard_gradient_descent():
            # Start from (-1.5, -1.5)
            path = [np.array([-1.5, -1.5])]
            current = np.array([-1.5, -1.5])
            learning_rate = 0.1
            
            for _ in range(20):
                # Compute gradient
                dx = 2 * (current[0] - 1) + np.pi * np.cos(2*np.pi*current[0]) * np.sin(2*np.pi*current[1])
                dy = 2 * (current[1] - 1) + np.pi * np.sin(2*np.pi*current[0]) * np.cos(2*np.pi*current[1])
                gradient = np.array([dx, dy])
                
                # Update parameters
                current = current - learning_rate * gradient
                path.append(current.copy())
            
            return path
        
        # Natural gradient descent
        def natural_gradient_descent():
            # Start from (-1.5, -1.5)
            path = [np.array([-1.5, -1.5])]
            current = np.array([-1.5, -1.5])
            learning_rate = 0.1
            
            for _ in range(20):
                # Compute gradient
                dx = 2 * (current[0] - 1) + np.pi * np.cos(2*np.pi*current[0]) * np.sin(2*np.pi*current[1])
                dy = 2 * (current[1] - 1) + np.pi * np.sin(2*np.pi*current[0]) * np.cos(2*np.pi*current[1])
                gradient = np.array([dx, dy])
                
                # Compute Fisher metric at current point
                sigma = 1 + 0.2 * np.sqrt(current[0]**2 + current[1]**2)
                g_11 = 1 / (sigma**2)
                g_22 = 1 / (sigma**2)
                g_12 = 0.1 * np.sin(current[0] + current[1])
                
                # Fisher metric matrix
                G = np.array([[g_11, g_12], [g_12, g_22]])
                
                # Natural gradient: G^(-1) * gradient
                try:
                    G_inv = np.linalg.inv(G)
                    natural_grad = G_inv @ gradient
                except:
                    natural_grad = gradient
                
                # Update parameters
                current = current - learning_rate * natural_grad
                path.append(current.copy())
            
            return path
        
        # Create optimization paths
        standard_path = standard_gradient_descent()
        natural_path = natural_gradient_descent()
        
        # Convert to Manim objects
        standard_path_obj = VMobject()
        standard_points = [left_axes.c2p(p[0], p[1], 0) for p in standard_path]
        standard_path_obj.set_points_as_corners(standard_points)
        standard_path_obj.set_color(RED)
        standard_path_obj.set_stroke(width=3)
        
        natural_path_obj = VMobject()
        natural_points = [left_axes.c2p(p[0], p[1], 0) for p in natural_path]
        natural_path_obj.set_points_as_corners(natural_points)
        natural_path_obj.set_color(GREEN)
        natural_path_obj.set_stroke(width=3)
        
        # Show optimization paths
        self.play(Create(standard_path_obj))
        self.wait(0.5)
        self.play(Create(natural_path_obj))
        self.wait(1)
        
        # Add explanation
        explanation = VGroup(
            Text("Optimization Methods:", font_size=20, color=WHITE),
            Text("• Standard Gradient: θ_{t+1} = θ_t - α∇L(θ_t)", font_size=16, color=RED),
            Text("• Natural Gradient: θ_{t+1} = θ_t - αG^(-1)∇L(θ_t)", font_size=16, color=GREEN),
            Text("• G is the Fisher Information Matrix", font_size=16, color=YELLOW)
        ).arrange(DOWN, buff=0.2).to_edge(DOWN)
        
        self.play(Write(explanation))
        self.wait(2)
        
        # Show moving points along optimization paths
        standard_point = Dot(color=RED, radius=0.08)
        standard_point.move_to(standard_points[0])
        
        natural_point = Dot(color=GREEN, radius=0.08)
        natural_point.move_to(natural_points[0])
        
        self.play(FadeIn(standard_point), FadeIn(natural_point))
        
        # Animate points along paths
        self.play(
            MoveAlongPath(standard_point, standard_path_obj, run_time=4),
            MoveAlongPath(natural_point, natural_path_obj, run_time=4)
        )
        self.wait(1)
        
        # Show advantages of natural gradient
        advantages_text = VGroup(
            Text("Advantages of Natural Gradient:", font_size=20, color=YELLOW),
            Text("• Invariant to parameterization", font_size=16, color=WHITE),
            Text("• Respects the geometry of the statistical manifold", font_size=16, color=WHITE),
            Text("• More efficient convergence in many cases", font_size=16, color=WHITE),
            Text("• Natural for exponential families", font_size=16, color=WHITE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(explanation))
        self.play(Write(advantages_text))
        self.wait(3)
        
        # Final explanation
        final_text = VGroup(
            Text("Information geometry provides the optimal way", font_size=20, color=YELLOW),
            Text("to navigate the space of probability distributions", font_size=20, color=YELLOW),
            Text("enabling more efficient machine learning algorithms", font_size=18, color=BLUE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(advantages_text))
        self.play(Write(final_text))
        self.wait(3)
