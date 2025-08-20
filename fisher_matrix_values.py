from manim import *
import numpy as np

class FisherMatrixValues(Scene):
    def construct(self):
        # Set up the scene
        self.camera.background_color = "#1a1a1a"
        
        # Title - positioned at top but not overlapping
        title = Text("Fisher Information Matrix Values", font_size=28, color=WHITE).to_edge(UP, buff=0.5)
        subtitle = MathTex(r"I(\theta)_{ij} = E\left[\left(\frac{\partial}{\partial\theta_i} \log f(x;\theta)\right)\left(\frac{\partial}{\partial\theta_j} \log f(x;\theta)\right)\right]", font_size=16, color=BLUE).next_to(title, DOWN, buff=0.3)
        self.play(Write(title), Write(subtitle))
        self.wait(1)
        
        # Show formula explanation in a separate screen
        formula_explanation = VGroup(
            Text("Formula Components:", font_size=20, color=WHITE),
            Text("• I(θ)_ij = (i,j)-th element of Fisher Information Matrix", font_size=16, color=YELLOW),
            Text("• E[·] = Expectation over random variable X", font_size=16, color=GREEN),
            Text("• ∂/∂θ_i = Partial derivative with respect to parameter θ_i", font_size=16, color=ORANGE),
            Text("• logf(x;θ) = Log-likelihood function", font_size=16, color=RED)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(ORIGIN)
        
        self.play(FadeOut(subtitle))
        self.play(Write(formula_explanation))
        self.wait(3)
        self.play(FadeOut(formula_explanation))
        
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
        
        # Re-show title for matrix display
        self.play(Write(title))
        
        # Create the matrix display using rectangles and lines - centered and larger
        matrix_display = VGroup()
        
        # Matrix label
        matrix_label = MathTex(r"I(\theta) =", font_size=28, color=WHITE)
        matrix_label.move_to([-4, 0, 0])
        matrix_display.add(matrix_label)
        
        # Create matrix elements with larger spacing
        matrix_elements = []
        element_width = 1.8
        element_height = 1.0
        
        for i in range(matrix_size):
            row_elements = []
            for j in range(matrix_size):
                element = MathTex(matrix_values[i][j], font_size=24, color=YELLOW)
                x_pos = (j - (matrix_size-1)/2) * element_width
                y_pos = ((matrix_size-1)/2 - i) * element_height
                element.move_to([x_pos, y_pos, 0])
                row_elements.append(element)
                matrix_elements.append(element)
            matrix_display.add(*row_elements)
        
        # Create matrix grid lines with better positioning
        grid_lines = VGroup()
        
        # Vertical lines
        for j in range(matrix_size + 1):
            x_pos = (j - matrix_size/2) * element_width
            line = Line(
                start=[x_pos, -2, 0],
                end=[x_pos, 2, 0],
                color=WHITE,
                stroke_width=3
            )
            grid_lines.add(line)
        
        # Horizontal lines
        for i in range(matrix_size + 1):
            y_pos = (matrix_size/2 - i) * element_height
            line = Line(
                start=[-3.6, y_pos, 0],
                end=[3.6, y_pos, 0],
                color=WHITE,
                stroke_width=3
            )
            grid_lines.add(line)
        
        matrix_display.add(grid_lines)
        
        # Show the matrix
        self.play(Create(matrix_display))
        self.wait(2)
        
        # Add row and column labels with better positioning
        row_labels = []
        col_labels = []
        
        for i in range(matrix_size):
            # Row labels (left side)
            row_label = MathTex(f"\\theta_{i+1}", font_size=20, color=BLUE)
            row_label.move_to([-5, ((matrix_size-1)/2 - i) * element_height, 0])
            row_labels.append(row_label)
            
            # Column labels (top)
            col_label = MathTex(f"\\theta_{i+1}", font_size=20, color=GREEN)
            col_label.move_to([(i - (matrix_size-1)/2) * element_width, 2.5, 0])
            col_labels.append(col_label)
        
        # Show labels
        self.play(Write(VGroup(*row_labels)), Write(VGroup(*col_labels)))
        self.wait(2)
        
        # Clear screen and show element explanations separately
        self.play(FadeOut(matrix_display), FadeOut(VGroup(*row_labels)), FadeOut(VGroup(*col_labels)), FadeOut(title))
        
        # Show matrix element explanations on clean screen
        element_explanation = VGroup(
            Text("Matrix Elements Explanation:", font_size=24, color=WHITE),
            Text("", font_size=16),  # spacer
            MathTex(r"I(\theta)_{11} = E\left[\left(\frac{\partial}{\partial\theta_1} \log f\right)^2\right] = \frac{1}{\sigma^2}", font_size=18, color=YELLOW),
            Text("", font_size=12),  # spacer
            MathTex(r"I(\theta)_{22} = E\left[\left(\frac{\partial}{\partial\theta_2} \log f\right)^2\right] = \frac{2}{\sigma^2}", font_size=18, color=YELLOW),
            Text("", font_size=12),  # spacer
            MathTex(r"I(\theta)_{12} = E\left[\left(\frac{\partial}{\partial\theta_1} \log f\right)\left(\frac{\partial}{\partial\theta_2} \log f\right)\right] = 0", font_size=18, color=ORANGE),
            Text("", font_size=12),  # spacer
            Text("Zero off-diagonal elements indicate parameter independence", font_size=16, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT).move_to(ORIGIN)
        
        self.play(Write(element_explanation))
        self.wait(4)
        self.play(FadeOut(element_explanation))
        
        # Show detailed calculations on clean screen
        calculations = VGroup(
            Text("Detailed Element Calculations:", font_size=24, color=WHITE),
            Text("", font_size=16),  # spacer
            Text("For Normal Distribution N(μ, σ²):", font_size=18, color=BLUE),
            Text("", font_size=12),  # spacer
            MathTex(r"I(\theta)_{11} = E\left[\left(\frac{x-\mu}{\sigma^2}\right)^2\right] = \frac{1}{\sigma^2}", font_size=16, color=YELLOW),
            Text("", font_size=8),  # spacer
            MathTex(r"I(\theta)_{22} = E\left[\left(\frac{(x-\mu)^2-\sigma^2}{\sigma^3}\right)^2\right] = \frac{2}{\sigma^2}", font_size=16, color=GREEN),
            Text("", font_size=8),  # spacer
            MathTex(r"I(\theta)_{12} = E\left[\frac{(x-\mu)((x-\mu)^2-\sigma^2)}{\sigma^5}\right] = 0", font_size=16, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT).move_to(ORIGIN)
        
        self.play(Write(calculations))
        self.wait(4)
        self.play(FadeOut(calculations))
        
        # Show expectation operation explanation on clean screen
        expectation_explanation = VGroup(
            Text("Expectation Operation E[·]:", font_size=24, color=WHITE),
            Text("", font_size=16),  # spacer
            MathTex(r"E[g(X)] = \int_{-\infty}^{\infty} g(x) f(x;\theta) \, dx", font_size=18, color=GREEN),
            Text("", font_size=12),  # spacer
            Text("For discrete X:", font_size=16, color=BLUE),
            MathTex(r"E[g(X)] = \sum_{x} g(x) P(X=x)", font_size=18, color=ORANGE),
            Text("", font_size=12),  # spacer
            Text("Measures average behavior over the probability distribution", font_size=16, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT).move_to(ORIGIN)
        
        self.play(Write(expectation_explanation))
        self.wait(4)
        self.play(FadeOut(expectation_explanation))
        
        # Show parameter interpretation on clean screen
        parameter_interpretation = VGroup(
            Text("Parameter Interpretation:", font_size=24, color=WHITE),
            Text("", font_size=16),  # spacer
            MathTex(r"\theta_1 = \mu \text{ (mean parameter)}", font_size=18, color=BLUE),
            Text("", font_size=12),  # spacer
            MathTex(r"\theta_2 = \sigma \text{ (standard deviation parameter)}", font_size=18, color=GREEN),
            Text("", font_size=12),  # spacer
            MathTex(r"\theta_3, \theta_4 \text{ = Additional parameters}", font_size=18, color=ORANGE),
            Text("", font_size=12),  # spacer
            Text("Matrix shows information content about each parameter", font_size=16, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT).move_to(ORIGIN)
        
        self.play(Write(parameter_interpretation))
        self.wait(4)
        self.play(FadeOut(parameter_interpretation))
        
        # Show the final matrix with numerical values on clean screen
        # Re-show title and matrix
        title = Text("Fisher Information Matrix Values", font_size=28, color=WHITE).to_edge(UP, buff=0.5)
        subtitle = Text("Numerical Example (σ = 1)", font_size=18, color=BLUE).next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title), Write(subtitle))
        
        # Create numerical matrix values for σ = 1
        sigma = 1
        numerical_values = [
            [f"{1/sigma**2:.2f}", "0.00", "0.00", "0.00"],
            ["0.00", f"{2/sigma**2:.2f}", "0.00", "0.00"],
            ["0.00", "0.00", f"{1/sigma**2:.2f}", "0.00"],
            ["0.00", "0.00", "0.00", f"{2/sigma**2:.2f}"]
        ]
        
        # Create the numerical matrix display
        numerical_matrix_display = VGroup()
        
        # Matrix label
        matrix_label = MathTex(r"I(\theta) =", font_size=28, color=WHITE)
        matrix_label.move_to([-4, -0.5, 0])
        numerical_matrix_display.add(matrix_label)
        
        # Create matrix elements
        numerical_elements = []
        element_width = 1.8
        element_height = 1.0
        
        for i in range(matrix_size):
            row_elements = []
            for j in range(matrix_size):
                element = MathTex(numerical_values[i][j], font_size=24, color=WHITE)
                x_pos = (j - (matrix_size-1)/2) * element_width
                y_pos = ((matrix_size-1)/2 - i) * element_height - 0.5
                element.move_to([x_pos, y_pos, 0])
                row_elements.append(element)
                numerical_elements.append(element)
            numerical_matrix_display.add(*row_elements)
        
        # Create matrix grid lines
        grid_lines = VGroup()
        
        # Vertical lines
        for j in range(matrix_size + 1):
            x_pos = (j - matrix_size/2) * element_width
            line = Line(
                start=[x_pos, -2.5, 0],
                end=[x_pos, 1.5, 0],
                color=WHITE,
                stroke_width=3
            )
            grid_lines.add(line)
        
        # Horizontal lines
        for i in range(matrix_size + 1):
            y_pos = (matrix_size/2 - i) * element_height - 0.5
            line = Line(
                start=[-3.6, y_pos, 0],
                end=[3.6, y_pos, 0],
                color=WHITE,
                stroke_width=3
            )
            grid_lines.add(line)
        
        numerical_matrix_display.add(grid_lines)
        
        # Show the numerical matrix
        self.play(Create(numerical_matrix_display))
        self.wait(3)
        
        # Show final properties on clean screen
        self.play(FadeOut(numerical_matrix_display), FadeOut(title), FadeOut(subtitle))
        
        final_explanation = VGroup(
            Text("Fisher Information Matrix Properties:", font_size=24, color=WHITE),
            Text("", font_size=16),  # spacer
            MathTex(r"\text{• Symmetric: } I(\theta)_{ij} = I(\theta)_{ji}", font_size=18, color=BLUE),
            Text("", font_size=12),  # spacer
            MathTex(r"\text{• Positive Semi-definite: All eigenvalues} \geq 0", font_size=18, color=GREEN),
            Text("", font_size=12),  # spacer
            Text("• Diagonal elements: Information about individual parameters", font_size=18, color=YELLOW),
            Text("", font_size=12),  # spacer
            Text("• Off-diagonal elements: Parameter interactions", font_size=18, color=ORANGE),
            Text("", font_size=12),  # spacer
            Text("• Larger values = More information about parameters", font_size=18, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT).move_to(ORIGIN)
        
        self.play(Write(final_explanation))
        self.wait(4)
        self.play(FadeOut(final_explanation))
        
        # Final summary
        summary = VGroup(
            Text("Fisher Information Matrix", font_size=28, color=YELLOW),
            Text("", font_size=16),  # spacer
            MathTex(r"I(\theta)_{ij} = E\left[\left(\frac{\partial}{\partial\theta_i} \log f(x;\theta)\right)\left(\frac{\partial}{\partial\theta_j} \log f(x;\theta)\right)\right]", font_size=18, color=WHITE),
            Text("", font_size=12),  # spacer
            Text("Complete visualization of matrix values for parameters θ₁, θ₂, θ₃, θ₄", font_size=18, color=BLUE)
        ).arrange(DOWN, aligned_edge=LEFT).move_to(ORIGIN)
        
        self.play(Write(summary))
        self.wait(3)
