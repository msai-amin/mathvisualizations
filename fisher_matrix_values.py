from manim import *
import numpy as np

class FisherMatrixValues(Scene):
    def construct(self):
        # Set up the scene
        self.camera.background_color = "#1a1a1a"
        
        # Title
        title = Text("Fisher Information Matrix Values", font_size=32, color=WHITE).to_edge(UP)
        subtitle = Text("I(θ)_ij = E[(∂/∂θ_i logf(x;θ))(∂/∂θ_j logf(x;θ))]", font_size=20, color=BLUE).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(1)
        
        # Explanation of the formula
        formula_explanation = VGroup(
            Text("Where:", font_size=18, color=WHITE),
            Text("• I(θ)_ij = (i,j)-th element of Fisher Information Matrix", font_size=16, color=YELLOW),
            Text("• E[·] = Expectation over random variable X", font_size=16, color=GREEN),
            Text("• ∂/∂θ_i = Partial derivative with respect to parameter θ_i", font_size=16, color=ORANGE),
            Text("• logf(x;θ) = Log-likelihood function", font_size=16, color=RED)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(LEFT).shift(DOWN * 0.5)
        
        self.play(Write(formula_explanation))
        self.wait(2)
        
        # Create a 4x4 Fisher Information Matrix
        # For demonstration, we'll use a realistic example with normal distribution parameters
        matrix_size = 4
        
        # Create matrix with realistic Fisher Information values
        # For normal distribution N(μ, σ²), the Fisher matrix is:
        # I(μ,σ) = [[1/σ², 0], [0, 2/σ²]]
        # We'll extend this to 4 parameters for demonstration
        
        # Create the matrix values using proper LaTeX notation
        matrix_values = [
            [r"\frac{1}{\sigma^2}", "0", "0", "0"],
            ["0", r"\frac{2}{\sigma^2}", "0", "0"],
            ["0", "0", r"\frac{1}{\sigma^2}", "0"],
            ["0", "0", "0", r"\frac{2}{\sigma^2}"]
        ]
        
        # Create the matrix display using rectangles and lines
        matrix_display = VGroup()
        
        # Matrix label
        matrix_label = MathTex(r"I(\theta) =", font_size=24, color=WHITE)
        matrix_label.move_to([-5.5, 0, 0])
        matrix_display.add(matrix_label)
        
        # Create matrix elements
        matrix_elements = []
        element_width = 1.5
        element_height = 0.8
        
        for i in range(matrix_size):
            row_elements = []
            for j in range(matrix_size):
                element = MathTex(matrix_values[i][j], font_size=20, color=YELLOW)
                x_pos = (j - (matrix_size-1)/2) * element_width
                y_pos = ((matrix_size-1)/2 - i) * element_height
                element.move_to([x_pos, y_pos, 0])
                row_elements.append(element)
                matrix_elements.append(element)
            matrix_display.add(*row_elements)
        
        # Create matrix grid lines
        grid_lines = VGroup()
        
        # Vertical lines
        for j in range(matrix_size + 1):
            x_pos = (j - matrix_size/2) * element_width
            line = Line(
                start=[x_pos, -1.5, 0],
                end=[x_pos, 1.5, 0],
                color=WHITE,
                stroke_width=2
            )
            grid_lines.add(line)
        
        # Horizontal lines
        for i in range(matrix_size + 1):
            y_pos = (matrix_size/2 - i) * element_height
            line = Line(
                start=[-3, y_pos, 0],
                end=[3, y_pos, 0],
                color=WHITE,
                stroke_width=2
            )
            grid_lines.add(line)
        
        matrix_display.add(grid_lines)
        
        # Show the matrix
        self.play(Create(matrix_display))
        self.wait(2)
        
        # Add row and column labels
        row_labels = []
        col_labels = []
        
        for i in range(matrix_size):
            # Row labels (left side)
            row_label = MathTex(f"\\theta_{i+1}", font_size=18, color=BLUE)
            row_label.move_to([-5, ((matrix_size-1)/2 - i) * element_height, 0])
            row_labels.append(row_label)
            
            # Column labels (top)
            col_label = MathTex(f"\\theta_{i+1}", font_size=18, color=GREEN)
            col_label.move_to([(i - (matrix_size-1)/2) * element_width, 2, 0])
            col_labels.append(col_label)
        
        # Show labels
        self.play(Write(VGroup(*row_labels)), Write(VGroup(*col_labels)))
        self.wait(1)
        
        # Add explanation of what each element represents
        element_explanation = VGroup(
            Text("Matrix Elements:", font_size=18, color=WHITE),
            Text("• I(θ)_11 = E[(∂/∂θ₁ logf)²] = 1/σ²", font_size=16, color=YELLOW),
            Text("• I(θ)_22 = E[(∂/∂θ₂ logf)²] = 2/σ²", font_size=16, color=YELLOW),
            Text("• I(θ)_12 = E[(∂/∂θ₁ logf)(∂/∂θ₂ logf)] = 0", font_size=16, color=ORANGE),
            Text("• Zero elements indicate parameter independence", font_size=16, color=ORANGE)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(RIGHT).shift(DOWN * 0.5)
        
        self.play(Write(element_explanation))
        self.wait(2)
        
        # Show specific element calculations
        self.play(FadeOut(element_explanation))
        
        # Highlight specific elements and show their calculations
        calculations = VGroup(
            Text("Element Calculations:", font_size=20, color=WHITE),
            Text("I(θ)_11 = E[(∂/∂μ logf)²] = E[(x-μ)²/σ⁴] = 1/σ²", font_size=16, color=YELLOW),
            Text("I(θ)_22 = E[(∂/∂σ logf)²] = E[((x-μ)²-σ²)²/σ⁶] = 2/σ²", font_size=16, color=GREEN),
            Text("I(θ)_12 = E[(∂/∂μ logf)(∂/∂σ logf)] = E[(x-μ)((x-μ)²-σ²)/σ⁵] = 0", font_size=16, color=ORANGE)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(RIGHT).shift(DOWN * 0.5)
        
        self.play(Write(calculations))
        self.wait(2)
        
        # Show the expectation operation
        expectation_explanation = VGroup(
            Text("Expectation Operation E[·]:", font_size=18, color=WHITE),
            Text("• Integrates over the probability distribution", font_size=16, color=BLUE),
            Text("• E[g(X)] = ∫ g(x) f(x;θ) dx", font_size=16, color=GREEN),
            Text("• For discrete X: E[g(X)] = Σ g(x) P(X=x)", font_size=16, color=ORANGE),
            Text("• Measures average behavior of the function", font_size=16, color=YELLOW)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(LEFT).shift(UP * 1.5)
        
        self.play(FadeOut(calculations))
        self.play(Write(expectation_explanation))
        self.wait(2)
        
        # Show parameter interpretation
        parameter_interpretation = VGroup(
            Text("Parameter Interpretation:", font_size=18, color=WHITE),
            Text("• θ₁ = μ (mean parameter)", font_size=16, color=BLUE),
            Text("• θ₂ = σ (standard deviation parameter)", font_size=16, color=GREEN),
            Text("• θ₃, θ₄ = Additional parameters", font_size=16, color=ORANGE),
            Text("• Matrix shows information content about each parameter", font_size=16, color=YELLOW)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(RIGHT).shift(UP * 1.5)
        
        self.play(Write(parameter_interpretation))
        self.wait(2)
        
        # Show the complete matrix with all elements visible
        self.play(FadeOut(expectation_explanation), FadeOut(parameter_interpretation))
        
        # Create a more detailed matrix showing actual numerical values
        # Let's use σ = 1 for simplicity
        sigma = 1
        numerical_values = [
            [f"{1/sigma**2:.2f}", "0.00", "0.00", "0.00"],
            ["0.00", f"{2/sigma**2:.2f}", "0.00", "0.00"],
            ["0.00", "0.00", f"{1/sigma**2:.2f}", "0.00"],
            ["0.00", "0.00", "0.00", f"{2/sigma**2:.2f}"]
        ]
        
        # Create numerical matrix
        numerical_matrix = VGroup()
        numerical_elements = []
        
        for i in range(matrix_size):
            row_elements = []
            for j in range(matrix_size):
                element = MathTex(numerical_values[i][j], font_size=18, color=WHITE)
                element.move_to([(j - (matrix_size-1)/2) * element_width, ((matrix_size-1)/2 - i) * element_height, 0])
                row_elements.append(element)
                numerical_elements.append(element)
            numerical_matrix.add(*row_elements)
        
        # Replace symbolic matrix with numerical matrix
        self.play(Transform(VGroup(*[elem for row in matrix_elements for elem in row]), numerical_matrix))
        self.wait(2)
        
        # Add final explanation
        final_explanation = VGroup(
            Text("Fisher Information Matrix Properties:", font_size=20, color=WHITE),
            Text("• Symmetric: I(θ)_ij = I(θ)_ji", font_size=16, color=BLUE),
            Text("• Positive Semi-definite: All eigenvalues ≥ 0", font_size=16, color=GREEN),
            Text("• Diagonal elements: Information about individual parameters", font_size=16, color=YELLOW),
            Text("• Off-diagonal elements: Parameter interactions", font_size=16, color=ORANGE),
            Text("• Larger values = More information about parameters", font_size=16, color=RED)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(DOWN)
        
        self.play(Write(final_explanation))
        self.wait(3)
        
        # Final summary
        summary = VGroup(
            Text("Fisher Information Matrix I(θ)_ij", font_size=24, color=YELLOW),
            Text("Complete visualization of matrix values", font_size=18, color=WHITE),
            Text("for parameters θ₁, θ₂, θ₃, θ₄", font_size=18, color=BLUE)
        ).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        
        self.play(FadeOut(final_explanation), FadeOut(matrix_display), 
                  FadeOut(VGroup(*row_labels)), FadeOut(VGroup(*col_labels)))
        self.play(Write(summary))
        self.wait(2)
