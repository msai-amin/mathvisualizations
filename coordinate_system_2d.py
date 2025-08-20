from manim import *
import numpy as np

class CoordinateSystem2D(Scene):
    def construct(self):
        # Set up the scene
        title = Text("2D Coordinate System with Line Between Points", font_size=28, color=WHITE).to_edge(UP)
        subtitle = Text("Simple Line Geometry in 2D Space", font_size=18, color=BLUE).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        
        # Create 2D coordinate system
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": BLUE, "stroke_width": 2}
        )
        
        # Add axis labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        
        # Show coordinate system
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(1)
        
        # Create coordinate grid
        grid = VGroup()
        
        # Vertical lines
        for x in np.linspace(-4, 4, 9):
            line = Line(
                start=axes.c2p(x, -3, 0),
                end=axes.c2p(x, 3, 0),
                color=BLUE,
                stroke_width=0.5,
                stroke_opacity=0.3
            )
            grid.add(line)
        
        # Horizontal lines
        for y in np.linspace(-3, 3, 7):
            line = Line(
                start=axes.c2p(-4, y, 0),
                end=axes.c2p(4, y, 0),
                color=BLUE,
                stroke_width=0.5,
                stroke_opacity=0.3
            )
            grid.add(line)
        
        # Show coordinate grid
        self.play(Create(grid))
        self.wait(1)
        
        # Define two points
        point1_coords = (-2, -1)
        point2_coords = (3, 2)
        
        # Create the points
        point1 = Dot(point=axes.c2p(point1_coords[0], point1_coords[1], 0), color=RED, radius=0.08)
        point2 = Dot(point=axes.c2p(point2_coords[0], point2_coords[1], 0), color=GREEN, radius=0.08)
        
        # Add point labels
        point1_label = MathTex(f"P_1({point1_coords[0]}, {point1_coords[1]})", font_size=16, color=RED)
        point1_label.next_to(point1, UP + LEFT, buff=0.2)
        
        point2_label = MathTex(f"P_2({point2_coords[0]}, {point2_coords[1]})", font_size=16, color=GREEN)
        point2_label.next_to(point2, UP + RIGHT, buff=0.2)
        
        # Show the points
        self.play(FadeIn(point1), FadeIn(point2))
        self.play(Write(point1_label), Write(point2_label))
        self.wait(1)
        
        # Create the line between the points
        line = Line(
            start=point1.get_center(),
            end=point2.get_center(),
            color=YELLOW,
            stroke_width=4
        )
        
        # Show the line
        self.play(Create(line))
        self.wait(1)
        
        # Calculate and show the distance
        distance = np.sqrt((point2_coords[0] - point1_coords[0])**2 + (point2_coords[1] - point1_coords[1])**2)
        
        distance_text = VGroup(
            Text("Distance between points:", font_size=16, color=WHITE),
            MathTex(f"d = \\sqrt{{({point2_coords[0]} - ({point1_coords[0]}))^2 + ({point2_coords[1]} - ({point1_coords[1]}))^2}}", font_size=14, color=YELLOW),
            MathTex(f"d = \\sqrt{{({point2_coords[0] - point1_coords[0]})^2 + ({point2_coords[1] - point1_coords[1]})^2}}", font_size=14, color=YELLOW),
            MathTex(f"d = \\sqrt{{{point2_coords[0] - point1_coords[0]}^2 + {point2_coords[1] - point1_coords[1]}^2}}", font_size=14, color=YELLOW),
            MathTex(f"d = \\sqrt{{{int((point2_coords[0] - point1_coords[0])**2)} + {int((point2_coords[1] - point1_coords[1])**2)}}}", font_size=14, color=YELLOW),
            MathTex(f"d = \\sqrt{{{int((point2_coords[0] - point1_coords[0])**2 + (point2_coords[1] - point1_coords[1])**2)}}}", font_size=14, color=YELLOW),
            MathTex(f"d = {distance:.3f}", font_size=16, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(Write(distance_text))
        self.wait(2)
        
        # Show slope calculation
        slope = (point2_coords[1] - point1_coords[1]) / (point2_coords[0] - point1_coords[0])
        
        slope_text = VGroup(
            Text("Slope of the line:", font_size=16, color=WHITE),
            MathTex(f"m = \\frac{{y_2 - y_1}}{{x_2 - x_1}} = \\frac{{{point2_coords[1]} - ({point1_coords[1]})}}{{{point2_coords[0]} - ({point1_coords[0]})}}", font_size=14, color=BLUE),
            MathTex(f"m = \\frac{{{point2_coords[1] - point1_coords[1]}}}{{{point2_coords[0] - point1_coords[0]}}} = \\frac{{{point2_coords[1] - point1_coords[1]}}}{{{point2_coords[0] - point1_coords[0]}}}", font_size=14, color=BLUE),
            MathTex(f"m = {slope:.3f}", font_size=16, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(distance_text))
        self.play(Write(slope_text))
        self.wait(2)
        
        # Show line equation
        # y - y1 = m(x - x1)
        # y = mx + b where b = y1 - mx1
        
        b = point1_coords[1] - slope * point1_coords[0]
        
        equation_text = VGroup(
            Text("Line equation:", font_size=16, color=WHITE),
            MathTex(f"y - y_1 = m(x - x_1)", font_size=14, color=GREEN),
            MathTex(f"y - ({point1_coords[1]}) = {slope:.3f}(x - ({point1_coords[0]}))", font_size=14, color=GREEN),
            MathTex(f"y = {slope:.3f}x + {b:.3f}", font_size=16, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(slope_text))
        self.play(Write(equation_text))
        self.wait(2)
        
        # Final summary
        final_text = VGroup(
            Text("2D Coordinate System with Line Between Points", font_size=20, color=YELLOW),
            Text(f"Points: P₁({point1_coords[0]}, {point1_coords[1]}) and P₂({point2_coords[0]}, {point2_coords[1]})", font_size=16, color=WHITE),
            Text(f"Distance: {distance:.3f} units", font_size=16, color=WHITE),
            Text(f"Slope: {slope:.3f}", font_size=16, color=WHITE),
            Text(f"Equation: y = {slope:.3f}x + {b:.3f}", font_size=16, color=WHITE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(equation_text))
        self.play(Write(final_text))
        self.wait(3)
