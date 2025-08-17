from manim import *
import numpy as np

class NonEuclidean2D(Scene):
    def construct(self):
        # Set up the scene
        title = Text("Non-Euclidean Geometry in 2D", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))
        
        # Create a curved coordinate system (Poincaré disk model)
        def poincare_metric(r):
            # Metric factor for hyperbolic geometry
            return 4 / (1 - r**2)**2
        
        # Create curved grid lines
        grid_lines = VGroup()
        
        # Radial lines (geodesics through origin)
        for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            line = Line(
                start=ORIGIN,
                end=2.5 * np.array([np.cos(angle), np.sin(angle), 0]),
                color=BLUE,
                stroke_width=2
            )
            grid_lines.add(line)
        
        # Concentric circles (equidistant curves)
        for r in np.linspace(0.5, 2.5, 5):
            circle = Circle(radius=r, color=RED, stroke_width=1)
            grid_lines.add(circle)
        
        # Show the curved grid
        self.play(Create(grid_lines))
        self.wait(1)
        
        # Create a triangle in non-Euclidean space
        # In hyperbolic geometry, triangle angles sum to less than 180°
        triangle_points = [
            np.array([0.5, 0.5, 0]),
            np.array([1.5, 0.3, 0]),
            np.array([0.8, 1.2, 0])
        ]
        
        triangle = Polygon(*triangle_points, color=YELLOW, stroke_width=3, fill_opacity=0.3)
        self.play(Create(triangle))
        
        # Add angle measurements
        angles = []
        for i in range(3):
            p1 = triangle_points[i]
            p2 = triangle_points[(i+1) % 3]
            p3 = triangle_points[(i+2) % 3]
            
            # Calculate angle
            v1 = p1 - p2
            v2 = p3 - p2
            cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            angle_rad = np.arccos(np.clip(cos_angle, -1, 1))
            angle_deg = angle_rad * 180 / np.pi
            
            angle_text = MathTex(f"{angle_deg:.1f}°", font_size=20, color=WHITE)
            angle_text.move_to(p2 + 0.3 * (v1 + v2) / (np.linalg.norm(v1) + np.linalg.norm(v2)))
            angles.append(angle_text)
        
        self.play(*[Write(angle) for angle in angles])
        
        # Show angle sum
        angle_sum = sum([float(angle.tex_string.replace("°", "")) for angle in angles])
        sum_text = MathTex(f"\\text{{Sum of angles: }} {angle_sum:.1f}° < 180°", 
                          font_size=24, color=YELLOW)
        sum_text.to_edge(DOWN)
        self.play(Write(sum_text))
        self.wait(2)
        
        # Clear and show parallel lines in non-Euclidean space
        self.play(FadeOut(triangle), FadeOut(sum_text), *[FadeOut(angle) for angle in angles])
        
        # Create parallel lines that diverge (hyperbolic parallel postulate)
        line1 = Line(start=np.array([-2, -1, 0]), end=np.array([2, -1, 0]), 
                    color=GREEN, stroke_width=3)
        line2 = Line(start=np.array([-2, 0, 0]), end=np.array([2, 0, 0]), 
                    color=GREEN, stroke_width=3)
        
        # Add a transversal
        transversal = Line(start=np.array([-1, -1.5, 0]), end=np.array([-1, 1.5, 0]), 
                          color=ORANGE, stroke_width=2)
        
        self.play(Create(line1), Create(line2))
        self.play(Create(transversal))
        
        # Show that these lines are not truly parallel in non-Euclidean space
        parallel_text = Text("In non-Euclidean space, 'parallel' lines can intersect!", 
                           font_size=24, color=RED)
        parallel_text.to_edge(DOWN)
        self.play(Write(parallel_text))
        self.wait(2)
        
        # Show geodesic deviation
        self.play(FadeOut(line1), FadeOut(line2), FadeOut(transversal), FadeOut(parallel_text))
        
        # Create two initially parallel geodesics that diverge
        t = np.linspace(0, 3, 100)
        geodesic1_x = t
        geodesic1_y = 0.1 * t**2  # Curved path
        
        geodesic2_x = t
        geodesic2_y = 0.1 * t**2 + 0.5  # Parallel curved path
        
        points1 = [np.array([x, y, 0]) for x, y in zip(geodesic1_x, geodesic1_y)]
        points2 = [np.array([x, y, 0]) for x, y in zip(geodesic2_x, geodesic2_y)]
        
        curve1 = VMobject()
        curve1.set_points_as_corners(points1)
        curve1.set_color(BLUE)
        curve1.set_stroke(width=3)
        
        curve2 = VMobject()
        curve2.set_points_as_corners(points2)
        curve2.set_color(RED)
        curve2.set_stroke(width=3)
        
        self.play(Create(curve1), Create(curve2))
        
        # Show deviation
        deviation_text = Text("Geodesic deviation shows curvature of space", 
                            font_size=24, color=WHITE)
        deviation_text.to_edge(DOWN)
        self.play(Write(deviation_text))
        self.wait(2)
        
        # Final explanation
        final_text = VGroup(
            Text("Key concepts of non-Euclidean geometry:", font_size=28, color=WHITE),
            Text("• Triangle angles don't sum to 180°", font_size=20, color=YELLOW),
            Text("• Parallel lines can intersect", font_size=20, color=GREEN),
            Text("• Geodesics deviate in curved space", font_size=20, color=BLUE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(deviation_text))
        self.play(Write(final_text))
        self.wait(3)
