from manim import *
import numpy as np

class CauchySequencesTopology(Scene):
    def construct(self):
        # Set up the scene
        title = Text("Cauchy Sequences in Non-Point Based Topology", font_size=32, color=WHITE).to_edge(UP)
        subtitle = Text("Convergence in Abstract Topological Spaces", font_size=20, color=BLUE).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        
        # Create coordinate systems
        # Left: Traditional point-based convergence
        left_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=4,
            y_length=4
        )
        left_axes.move_to(LEFT * 3)
        
        # Right: Non-point based topology
        right_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=4,
            y_length=4
        )
        right_axes.move_to(RIGHT * 3)
        
        # Add labels
        left_label = Text("Point-Based\nConvergence", font_size=18, color=RED).next_to(left_axes, DOWN)
        right_label = Text("Non-Point Based\nTopology", font_size=18, color=GREEN).next_to(right_axes, DOWN)
        
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
        
        # Create Cauchy sequence in point-based space
        def cauchy_sequence_point(n):
            # Cauchy sequence: x_n = 1/n
            return 1 / (n + 1)
        
        # Show first few terms of the sequence
        sequence_points = []
        sequence_labels = []
        
        for n in range(8):
            x = cauchy_sequence_point(n)
            point = left_axes.c2p(x, 0, 0)
            dot = Dot(point=point, color=YELLOW, radius=0.06)
            sequence_points.append(dot)
            
            label = MathTex(f"x_{n} = {x:.3f}", font_size=12, color=YELLOW)
            label.move_to(point + UP * 0.3)
            sequence_labels.append(label)
        
        # Show sequence points
        for i, (point, label) in enumerate(zip(sequence_points, sequence_labels)):
            self.play(FadeIn(point), Write(label), run_time=0.3)
        
        self.wait(1)
        
        # Show convergence to a point
        limit_point = Dot(point=left_axes.c2p(0, 0, 0), color=RED, radius=0.08)
        limit_label = MathTex(r"\lim_{n \to \infty} x_n = 0", font_size=16, color=RED)
        limit_label.move_to(left_axes.c2p(0, 0, 0) + UP * 0.5)
        
        self.play(FadeIn(limit_point), Write(limit_label))
        self.wait(1)
        
        # Show Cauchy condition
        cauchy_text = VGroup(
            Text("Cauchy Condition:", font_size=16, color=WHITE),
            Text("∀ε > 0, ∃N: |x_n - x_m| < ε", font_size=14, color=YELLOW),
            Text("for all n, m > N", font_size=14, color=YELLOW)
        ).arrange(DOWN, buff=0.2).to_edge(DOWN)
        
        self.play(Write(cauchy_text))
        self.wait(2)
        
        # Now show non-point based topology
        self.play(FadeOut(cauchy_text))
        
        # Create abstract topological space (represented as a network of sets)
        # This represents a space where convergence is not to points but to sets or other structures
        
        # Create abstract "sets" as circles
        set1 = Circle(radius=0.4, color=BLUE, stroke_width=2)
        set1.move_to(right_axes.c2p(-1, 1, 0))
        
        set2 = Circle(radius=0.4, color=GREEN, stroke_width=2)
        set2.move_to(right_axes.c2p(1, 1, 0))
        
        set3 = Circle(radius=0.4, color=ORANGE, stroke_width=2)
        set3.move_to(right_axes.c2p(0, -1, 0))
        
        # Show the sets
        self.play(Create(set1), Create(set2), Create(set3))
        self.wait(1)
        
        # Add set labels
        set1_label = Text("A₁", font_size=14, color=BLUE)
        set1_label.move_to(set1.get_center())
        
        set2_label = Text("A₂", font_size=14, color=GREEN)
        set2_label.move_to(set2.get_center())
        
        set3_label = Text("A₃", font_size=14, color=ORANGE)
        set3_label.move_to(set3.get_center())
        
        self.play(Write(set1_label), Write(set2_label), Write(set3_label))
        self.wait(1)
        
        # Create Cauchy sequence in non-point based space
        # This sequence converges to a set or structure, not a point
        
        # Create sequence elements as moving points
        sequence_elements = []
        for n in range(6):
            # Create a point that moves through the space
            angle = n * np.pi / 3
            radius = 1.5 * (1 - 0.1 * n)  # Decreasing radius
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            
            point = Dot(point=right_axes.c2p(x, y, 0), color=YELLOW, radius=0.06)
            sequence_elements.append(point)
            
            # Add label
            label = MathTex(f"x_{n}", font_size=12, color=YELLOW)
            label.move_to(right_axes.c2p(x, y, 0) + UP * 0.3)
            sequence_elements.append(label)
        
        # Show sequence elements
        for i in range(0, len(sequence_elements), 2):
            self.play(FadeIn(sequence_elements[i]), Write(sequence_elements[i+1]), run_time=0.3)
        
        self.wait(1)
        
        # Show how the sequence converges to a set (not a point)
        # Create a "limit set" that the sequence approaches
        limit_set = Circle(radius=0.6, color=RED, stroke_width=3, fill_opacity=0.2)
        limit_set.move_to(right_axes.c2p(0, 0, 0))
        
        limit_set_label = Text("Limit Set", font_size=14, color=RED)
        limit_set_label.move_to(right_axes.c2p(0, 0, 0) + UP * 0.8)
        
        self.play(Create(limit_set), Write(limit_set_label))
        self.wait(1)
        
        # Show Cauchy condition in non-point based topology
        cauchy_nonpoint_text = VGroup(
            Text("Cauchy Condition in Non-Point Based Topology:", font_size=16, color=WHITE),
            Text("∀ε > 0, ∃N: d(x_n, x_m) < ε", font_size=14, color=YELLOW),
            Text("for all n, m > N", font_size=14, color=YELLOW),
            Text("where d is a generalized distance", font_size=14, color=BLUE)
        ).arrange(DOWN, buff=0.2).to_edge(DOWN)
        
        self.play(Write(cauchy_nonpoint_text))
        self.wait(2)
        
        # Show different types of convergence
        convergence_types = VGroup(
            Text("Types of Convergence in Non-Point Based Topology:", font_size=18, color=WHITE),
            Text("• Set convergence: x_n → A (set)", font_size=14, color=BLUE),
            Text("• Filter convergence: x_n → F (filter)", font_size=14, color=GREEN),
            Text("• Net convergence: x_n → N (net)", font_size=14, color=YELLOW),
            Text("• Ultra-filter convergence: x_n → U (ultra-filter)", font_size=14, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(cauchy_nonpoint_text))
        self.play(Write(convergence_types))
        self.wait(3)
        
        # Show abstract topological structure
        # Create connections between sets to show topology
        connection1 = Line(start=set1.get_center(), end=set2.get_center(), color=WHITE, stroke_width=2)
        connection2 = Line(start=set2.get_center(), end=set3.get_center(), color=WHITE, stroke_width=2)
        connection3 = Line(start=set3.get_center(), end=set1.get_center(), color=WHITE, stroke_width=2)
        
        self.play(Create(connection1), Create(connection2), Create(connection3))
        self.wait(1)
        
        # Show moving point along the sequence path
        moving_point = Dot(color=YELLOW, radius=0.08)
        moving_point.move_to(sequence_elements[0].get_center())
        
        # Create path for the moving point
        path_points = []
        for n in range(6):
            angle = n * np.pi / 3
            radius = 1.5 * (1 - 0.1 * n)
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            path_points.append(right_axes.c2p(x, y, 0))
        
        path = VMobject()
        path.set_points_as_corners(path_points)
        path.set_color(YELLOW)
        path.set_stroke(width=2)
        
        # Show the path
        self.play(Create(path))
        self.wait(1)
        
        # Animate the moving point along the path
        self.play(FadeIn(moving_point))
        self.play(MoveAlongPath(moving_point, path, run_time=3))
        self.wait(1)
        
        # Show final convergence explanation
        final_convergence = VGroup(
            Text("Convergence in Non-Point Based Topology:", font_size=18, color=WHITE),
            Text("• Sequence converges to a set/structure", font_size=14, color=BLUE),
            Text("• Traditional point limit may not exist", font_size=14, color=GREEN),
            Text("• Cauchy condition ensures sequence coherence", font_size=14, color=YELLOW),
            Text("• Topology defined by convergence patterns", font_size=14, color=ORANGE)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(FadeOut(convergence_types))
        self.play(Write(final_convergence))
        self.wait(3)
        
        # Final explanation
        final_text = VGroup(
            Text("Cauchy sequences in non-point based topology", font_size=20, color=YELLOW),
            Text("provide a framework for convergence", font_size=20, color=YELLOW),
            Text("in abstract topological spaces", font_size=18, color=BLUE)
        ).arrange(DOWN, buff=0.4).to_edge(DOWN)
        
        self.play(FadeOut(final_convergence))
        self.play(Write(final_text))
        self.wait(3)
