from manim import *
import numpy as np

class FisherMatrixValues(Scene):
    def construct(self):
        # Set up the scene with white background for better visibility
        self.camera.background_color = WHITE
        
        # Simple title
        title = Text("Fisher Information Matrix Values", font_size=36, color=BLACK).to_edge(UP)
        self.play(Write(title))
        self.wait(2)
        
        # Show the main formula
        formula = MathTex(r"I(\theta)_{ij} = E\left[\left(\frac{\partial}{\partial\theta_i} \log f(x;\theta)\right)\left(\frac{\partial}{\partial\theta_j} \log f(x;\theta)\right)\right]", font_size=24, color=BLACK)
        self.play(Write(formula))
        self.wait(3)
        
        # Clear and show explanation
        self.play(FadeOut(formula))
        
        explanation = VGroup(
            Text("Formula Components:", font_size=28, color=BLACK),
            Text("• I(θ)_ij = (i,j)-th element of Fisher Information Matrix", font_size=20, color=BLUE),
            Text("• E[·] = Expectation over random variable X", font_size=20, color=GREEN),
            Text("• ∂/∂θ_i = Partial derivative with respect to parameter θ_i", font_size=20, color=RED),
            Text("• logf(x;θ) = Log-likelihood function", font_size=20, color=ORANGE)
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(ORIGIN)
        
        self.play(Write(explanation))
        self.wait(4)
        self.play(FadeOut(explanation))
        
        # Show a simple 2x2 Fisher Information Matrix
        self.play(Write(title))
        
        # Create a simple 2x2 matrix using rectangles and text
        matrix = VGroup()
        
        # Matrix elements as text
        element_11 = Text("1/σ²", font_size=32, color=BLUE)
        element_12 = Text("0", font_size=32, color=BLACK)
        element_21 = Text("0", font_size=32, color=BLACK)
        element_22 = Text("2/σ²", font_size=32, color=GREEN)
        
        # Position elements
        element_11.move_to([-1, 0.5, 0])
        element_12.move_to([1, 0.5, 0])
        element_21.move_to([-1, -0.5, 0])
        element_22.move_to([1, -0.5, 0])
        
        # Add elements to matrix
        matrix.add(element_11, element_12, element_21, element_22)
        
        # Create matrix grid using lines
        # Vertical lines
        v_line1 = Line(start=[-1.5, -1, 0], end=[-1.5, 1, 0], color=BLACK, stroke_width=3)
        v_line2 = Line(start=[0.5, -1, 0], end=[0.5, 1, 0], color=BLACK, stroke_width=3)
        v_line3 = Line(start=[2.5, -1, 0], end=[2.5, 1, 0], color=BLACK, stroke_width=3)
        
        # Horizontal lines
        h_line1 = Line(start=[-1.5, 1, 0], end=[2.5, 1, 0], color=BLACK, stroke_width=3)
        h_line2 = Line(start=[-1.5, 0, 0], end=[2.5, 0, 0], color=BLACK, stroke_width=3)
        h_line3 = Line(start=[-1.5, -1, 0], end=[2.5, -1, 0], color=BLACK, stroke_width=3)
        
        # Matrix label
        matrix_label = Text("I(θ) =", font_size=32, color=BLACK)
        matrix_label.move_to([-4.5, 0, 0])
        
        # Complete matrix
        complete_matrix = VGroup(matrix_label, matrix, v_line1, v_line2, v_line3, h_line1, h_line2, h_line3)
        
        # Show the matrix
        self.play(Create(complete_matrix))
        self.wait(3)
        
        # Add explanation
        matrix_explanation = VGroup(
            Text("Fisher Information Matrix for Normal Distribution N(μ, σ²):", font_size=24, color=BLACK),
            Text("• I(θ)_11 = 1/σ² (information about mean μ)", font_size=20, color=BLUE),
            Text("• I(θ)_22 = 2/σ² (information about standard deviation σ)", font_size=20, color=GREEN),
            Text("• I(θ)_12 = I(θ)_21 = 0 (parameters are independent)", font_size=20, color=BLACK)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([0, -2.5, 0])
        
        self.play(Write(matrix_explanation))
        self.wait(4)
        
        # Clear everything
        self.play(FadeOut(complete_matrix), FadeOut(matrix_explanation), FadeOut(title))
        
        # Show final summary
        final_summary = VGroup(
            Text("Fisher Information Matrix Summary:", font_size=28, color=BLACK),
            Text("", font_size=16),  # spacer
            Text("• Shows information content about parameters", font_size=20, color=BLUE),
            Text("• Diagonal elements: Individual parameter information", font_size=20, color=GREEN),
            Text("• Off-diagonal elements: Parameter interactions", font_size=20, color=RED),
            Text("• Used in parameter estimation and statistical inference", font_size=20, color=ORANGE)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(ORIGIN)
        
        self.play(Write(final_summary))
        self.wait(4)
        
        # Final formula
        final_formula = MathTex(r"I(\theta)_{ij} = E\left[\left(\frac{\partial}{\partial\theta_i} \log f(x;\theta)\right)\left(\frac{\partial}{\partial\theta_j} \log f(x;\theta)\right)\right]", font_size=20, color=BLACK)
        final_formula.move_to([0, -2.5, 0])
        
        self.play(Write(final_formula))
        self.wait(3)
