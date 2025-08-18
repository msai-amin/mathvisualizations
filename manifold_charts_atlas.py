from manim import *
import numpy as np

class ManifoldChartsAtlas(Scene):
    def construct(self):
        # Set up the scene
        title = Text("Smooth Manifold: Charts & Atlas", font_size=32, color=WHITE).to_edge(UP)
        subtitle = Text("Local Coordinate Systems & Chart Transformations", font_size=20, color=BLUE).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        
        # Create coordinate systems
        # Left: 2D manifold surface
        left_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=4,
            y_length=4
        )
        left_axes.move_to(LEFT * 3)
        
        # Right: Chart transformations
        right_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=4,
            y_length=4
        )
        right_axes.move_to(RIGHT * 3)
        
        # Add labels
        left_label = Text("2D Manifold M\nwith Charts", font_size=18, color=RED).next_to(left_axes, DOWN)
        right_label = Text("Chart Transformations\nφ₁₂ = φ₂ ∘ φ₁⁻¹", font_size=18, color=GREEN).next_to(right_axes, DOWN)
        
        # Show coordinate systems
        self.play(Create(left_axes), Create(right_axes))
        self.play(Write(left_label), Write(right_label))
        self.wait(1)
        
        # Create manifold surface (curved 2D surface)
        def manifold_surface(u, v):
            # Create a curved surface: z = 0.1 * (u² - v²) + 0.05 * sin(2πu) * cos(2πv)
            x = u
            y = v
            z = 0.1 * (u**2 - v**2) + 0.05 * np.sin(2*np.pi*u) * np.cos(2*np.pi*v)
            return np.array([x, y, z])
        
        # Create surface grid
        surface_grid = VGroup()
        for u in np.linspace(-2, 2, 15):
            for v in np.linspace(-2, 2, 15):
                point = manifold_surface(u, v)
                # Project to 2D for visualization
                dot = Dot(point=left_axes.c2p(point[0], point[1], 0), color=BLUE, radius=0.02)
                surface_grid.add(dot)
        
        # Show manifold surface
        self.play(Create(surface_grid))
        self.wait(1)
        
        # Create multiple charts covering the manifold
        # Chart 1: Center region
        chart1_center = np.array([0, 0])
        chart1_radius = 1.2
        chart1_circle = Circle(radius=chart1_radius, color=RED, stroke_width=3)
        chart1_circle.move_to(left_axes.c2p(chart1_center[0], chart1_center[1], 0))
        
        # Chart 2: Upper right region
        chart2_center = np.array([1.2, 1.2])
        chart2_radius = 0.8
        chart2_circle = Circle(radius=chart2_radius, color=GREEN, stroke_width=3)
        chart2_circle.move_to(left_axes.c2p(chart2_center[0], chart2_center[1], 0))
        
        # Chart 3: Lower left region
        chart3_center = np.array([-1.2, -1.2])
        chart3_radius = 0.8
        chart3_circle = Circle(radius=chart3_radius, color=ORANGE, stroke_width=3)
        chart3_circle.move_to(left_axes.c2p(chart3_center[0], chart3_center[1], 0))
        
        # Show charts
        self.play(Create(chart1_circle))
        self.wait(0.5)
        self.play(Create(chart2_circle))
        self.wait(0.5)
        self.play(Create(chart3_circle))
        self.wait(1)
        
        # Add chart labels
        chart1_label = Text("Chart 1\n(U₁, φ₁)", font_size=14, color=RED)
        chart1_label.move_to(left_axes.c2p(0, 0, 0) + UP * 0.3)
        
        chart2_label = Text("Chart 2\n(U₂, φ₂)", font_size=14, color=GREEN)
        chart2_label.move_to(left_axes.c2p(1.2, 1.2, 0) + UP * 0.3)
        
        chart3_label = Text("Chart 3\n(U₃, φ₃)", font_size=14, color=ORANGE)
        chart3_label.move_to(left_axes.c2p(-1.2, -1.2, 0) + UP * 0.3)
        
        self.play(Write(chart1_label), Write(chart2_label), Write(chart3_label))
        self.wait(1)
        
        # Show overlapping regions
        overlap_text = Text("Overlapping regions\nenable chart transitions", font_size=16, color=YELLOW)
        overlap_text.move_to(ORIGIN + UP * 0.5)
        self.play(Write(overlap_text))
        self.wait(2)
        
        # Show chart transformation
        self.play(FadeOut(overlap_text))
        
        # Create chart transformation visualization
        # Show how coordinates transform between charts
        def chart_transformation_12(x1, y1):
            # Transform from chart 1 to chart 2 coordinates
            # This is a simple example transformation
            x2 = x1 + 1.2
            y2 = y1 + 1.2
            return x2, y2
        
        # Create coordinate grid in chart 1
        chart1_grid = VGroup()
        for x in np.linspace(-0.8, 0.8, 5):
            for y in np.linspace(-0.8, 0.8, 5):
                point = left_axes.c2p(x, y, 0)
                dot = Dot(point=point, color=RED, radius=0.03)
                chart1_grid.add(dot)
        
        # Create transformed grid in chart 2
        chart2_grid = VGroup()
        for x in np.linspace(-0.8, 0.8, 5):
            for y in np.linspace(-0.8, 0.8, 5):
                x2, y2 = chart_transformation_12(x, y)
                point = right_axes.c2p(x2, y2, 0)
                dot = Dot(point=point, color=GREEN, radius=0.03)
                chart2_grid.add(dot)
        
        # Show coordinate grids
        self.play(Create(chart1_grid))
        self.wait(1)
        
        # Show transformation arrows
        transformation_arrows = VGroup()
        for i in range(len(chart1_grid)):
            start_point = chart1_grid[i].get_center()
            end_point = chart2_grid[i].get_center()
            arrow = Arrow(start=start_point, end=end_point, color=YELLOW, stroke_width=2)
            transformation_arrows.add(arrow)
        
        self.play(Create(transformation_arrows))
        self.wait(1)
        
        # Show transformed grid
        self.play(Create(chart2_grid))
        self.wait(1)
        
        # Add transformation formula
        transform_formula = MathTex(
            r"\phi_{12} = \phi_2 \circ \phi_1^{-1}",
            font_size=20,
            color=YELLOW
        )
        transform_formula.move_to(right_axes.c2p(0, 1.5, 0))
        
        self.play(Write(transform_formula))
        self.wait(2)
        
        # Show atlas structure
        atlas_text = VGroup(
            Text("Atlas A = {(Uᵢ, φᵢ)}ᵢ", font_size=20, color=WHITE),
            Text("• Charts cover entire manifold", font_size=16, color=BLUE),
            Text("• Smooth transitions between charts", font_size=16, color=GREEN),
            Text("• C^∞ manifold: infinitely differentiable", font_size=16, color=YELLOW)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(transformation_arrows), FadeOut(transform_formula))
        self.play(Write(atlas_text))
        self.wait(2)
        
        # Show tangent space at a point
        tangent_point = np.array([0.5, 0.5])
        tangent_dot = Dot(point=left_axes.c2p(tangent_point[0], tangent_point[1], 0), 
                         color=WHITE, radius=0.08)
        
        # Create tangent vectors
        tangent_vector1 = Arrow(
            start=left_axes.c2p(tangent_point[0], tangent_point[1], 0),
            end=left_axes.c2p(tangent_point[0] + 0.5, tangent_point[1], 0),
            color=RED, stroke_width=3
        )
        
        tangent_vector2 = Arrow(
            start=left_axes.c2p(tangent_point[0], tangent_point[1], 0),
            end=left_axes.c2p(tangent_point[0], tangent_point[1] + 0.5, 0),
            color=BLUE, stroke_width=3
        )
        
        tangent_label = Text("TₚM", font_size=16, color=WHITE)
        tangent_label.move_to(left_axes.c2p(tangent_point[0] + 0.3, tangent_point[1] + 0.3, 0))
        
        self.play(FadeIn(tangent_dot))
        self.play(Create(tangent_vector1), Create(tangent_vector2))
        self.play(Write(tangent_label))
        self.wait(1)
        
        # Final explanation
        final_text = VGroup(
            Text("A smooth manifold locally resembles Euclidean space", font_size=20, color=YELLOW),
            Text("Charts provide local coordinate systems", font_size=18, color=BLUE),
            Text("Atlas ensures complete coverage with smooth transitions", font_size=18, color=GREEN)
        ).arrange(DOWN, buff=0.4).to_edge(DOWN)
        
        self.play(FadeOut(atlas_text))
        self.play(Write(final_text))
        self.wait(3)
