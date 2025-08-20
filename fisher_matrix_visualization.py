from manim import *
import numpy as np
from scipy.stats import norm

class FisherMatrixVisualization(Scene):
    def construct(self):
        # Title and introduction
        title = Text("Fisher Information Matrix Visualization", font_size=28, color=WHITE).to_edge(UP)
        subtitle = Text("(I(θ))_ij = E[(∂/∂θ_i logf(x;θ))(∂/∂θ_j logf(x;θ))]", font_size=18, color=BLUE).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        
        # Show the mathematical formula
        formula = MathTex(
            r"(I(\theta))_{ij} = \mathbb{E}\left[\left(\frac{\partial}{\partial \theta_i} \log f(x;\theta)\right)\left(\frac{\partial}{\partial \theta_j} \log f(x;\theta)\right)\right]",
            font_size=24, color=YELLOW
        ).next_to(subtitle, DOWN, buff=0.5)
        self.play(Write(formula))
        self.wait(2)
        
        # Explanation of the formula
        explanation = VGroup(
            Text("Where:", font_size=16, color=WHITE),
            Text("• θ = (θ₁, θ₂, ..., θₙ) are the parameters", font_size=14, color=BLUE),
            Text("• f(x;θ) is the probability density function", font_size=14, color=GREEN),
            Text("• E[·] is the expectation operator", font_size=14, color=YELLOW),
            Text("• i, j are matrix indices", font_size=14, color=ORANGE)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(formula, DOWN, buff=0.5)
        self.play(Write(explanation))
        self.wait(2)
        
        # Clear previous content
        self.play(FadeOut(formula), FadeOut(explanation))
        
        # Show the matrix structure
        matrix_title = Text("Fisher Information Matrix Structure", font_size=20, color=WHITE).next_to(subtitle, DOWN)
        self.play(Write(matrix_title))
        
        # Create a 4x4 Fisher Information Matrix for demonstration
        # Using normal distribution with parameters μ and σ
        matrix_size = 4
        
        # Create the matrix with placeholder values
        matrix = Matrix(
            [[r"(I(\theta))_{11}", r"(I(\theta))_{12}", r"(I(\theta))_{13}", r"(I(\theta))_{14}"],
             [r"(I(\theta))_{21}", r"(I(\theta))_{22}", r"(I(\theta))_{23}", r"(I(\theta))_{24}"],
             [r"(I(\theta))_{31}", r"(I(\theta))_{32}", r"(I(\theta))_{33}", r"(I(\theta))_{34}"],
             [r"(I(\theta))_{41}", r"(I(\theta))_{42}", r"(I(\theta))_{43}", r"(I(\theta))_{44}"]],
            left_bracket="[",
            right_bracket="]"
        ).scale(0.8).next_to(matrix_title, DOWN, buff=0.5)
        
        self.play(Create(matrix))
        self.wait(2)
        
        # Show what each element represents
        element_explanation = VGroup(
            Text("Matrix Elements:", font_size=16, color=WHITE),
            Text("• (I(θ))_ij measures information about parameters θ_i and θ_j", font_size=14, color=BLUE),
            Text("• Diagonal elements: Information about individual parameters", font_size=14, color=GREEN),
            Text("• Off-diagonal elements: Information about parameter interactions", font_size=14, color=YELLOW)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(DOWN)
        self.play(Write(element_explanation))
        self.wait(2)
        
        # Clear and show specific example with normal distribution
        self.play(FadeOut(matrix), FadeOut(element_explanation), FadeOut(matrix_title))
        
        # Show specific example for normal distribution
        example_title = Text("Example: Normal Distribution N(μ, σ²)", font_size=20, color=WHITE).next_to(subtitle, DOWN)
        self.play(Write(example_title))
        
        # Show the parameters
        params = VGroup(
            Text("Parameters: θ = (μ, σ)", font_size=16, color=WHITE),
            Text("μ: mean, σ: standard deviation", font_size=14, color=BLUE)
        ).arrange(DOWN, buff=0.2).next_to(example_title, DOWN, buff=0.5)
        self.play(Write(params))
        self.wait(1)
        
        # Show the probability density function
        pdf_formula = MathTex(
            r"f(x;\mu,\sigma) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}",
            font_size=20, color=YELLOW
        ).next_to(params, DOWN, buff=0.5)
        self.play(Write(pdf_formula))
        self.wait(2)
        
        # Show the log-likelihood
        log_likelihood = MathTex(
            r"\log f(x;\mu,\sigma) = -\log(\sigma\sqrt{2\pi}) - \frac{(x-\mu)^2}{2\sigma^2}",
            font_size=18, color=GREEN
        ).next_to(pdf_formula, DOWN, buff=0.5)
        self.play(Write(log_likelihood))
        self.wait(2)
        
        # Clear and show partial derivatives
        self.play(FadeOut(params), FadeOut(pdf_formula), FadeOut(log_likelihood))
        
        # Show partial derivatives
        derivatives_title = Text("Partial Derivatives", font_size=18, color=WHITE).next_to(example_title, DOWN)
        self.play(Write(derivatives_title))
        
        # Show ∂/∂μ
        d_mu = MathTex(
            r"\frac{\partial}{\partial \mu} \log f(x;\mu,\sigma) = \frac{x-\mu}{\sigma^2}",
            font_size=18, color=BLUE
        ).next_to(derivatives_title, DOWN, buff=0.5)
        self.play(Write(d_mu))
        self.wait(1)
        
        # Show ∂/∂σ
        d_sigma = MathTex(
            r"\frac{\partial}{\partial \sigma} \log f(x;\mu,\sigma) = -\frac{1}{\sigma} + \frac{(x-\mu)^2}{\sigma^3}",
            font_size=18, color=GREEN
        ).next_to(d_mu, DOWN, buff=0.5)
        self.play(Write(d_sigma))
        self.wait(2)
        
        # Clear and show the Fisher Information Matrix
        self.play(FadeOut(derivatives_title), FadeOut(d_mu), FadeOut(d_sigma))
        
        # Show the actual Fisher Information Matrix for normal distribution
        fisher_matrix_title = Text("Fisher Information Matrix for N(μ, σ²)", font_size=18, color=WHITE).next_to(example_title, DOWN)
        self.play(Write(fisher_matrix_title))
        
        # Create the actual Fisher Information Matrix
        # For normal distribution: I(μ,σ) = [[1/σ², 0], [0, 2/σ²]]
        fisher_matrix = Matrix(
            [[r"\frac{1}{\sigma^2}", "0"],
             ["0", r"\frac{2}{\sigma^2}"]],
            left_bracket="[",
            right_bracket="]"
        ).scale(1.2).next_to(fisher_matrix_title, DOWN, buff=0.5)
        
        # Add parameter labels
        mu_label = Text("μ", font_size=16, color=BLUE).next_to(fisher_matrix, LEFT, buff=0.3)
        sigma_label = Text("σ", font_size=16, color=GREEN).next_to(fisher_matrix, LEFT, buff=0.3).shift(DOWN * 0.8)
        
        # Add top labels
        top_mu_label = Text("μ", font_size=16, color=BLUE).next_to(fisher_matrix, UP, buff=0.3)
        top_sigma_label = Text("σ", font_size=16, color=GREEN).next_to(fisher_matrix, UP, buff=0.3).shift(RIGHT * 0.8)
        
        self.play(Create(fisher_matrix), Write(mu_label), Write(sigma_label), 
                  Write(top_mu_label), Write(top_sigma_label))
        self.wait(2)
        
        # Show what each element means
        matrix_explanation = VGroup(
            Text("Matrix Elements:", font_size=16, color=WHITE),
            Text("• I₁₁ = 1/σ²: Information about μ", font_size=14, color=BLUE),
            Text("• I₂₂ = 2/σ²: Information about σ", font_size=14, color=GREEN),
            Text("• I₁₂ = I₂₁ = 0: No interaction between μ and σ", font_size=14, color=YELLOW)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(DOWN)
        self.play(Write(matrix_explanation))
        self.wait(2)
        
        # Clear and show numerical examples
        self.play(FadeOut(fisher_matrix), FadeOut(mu_label), FadeOut(sigma_label), 
                  FadeOut(top_mu_label), FadeOut(top_sigma_label), FadeOut(matrix_explanation))
        
        # Show numerical examples for different σ values
        numerical_title = Text("Numerical Examples", font_size=18, color=WHITE).next_to(fisher_matrix_title, DOWN)
        self.play(Write(numerical_title))
        
        # Create numerical matrices for different σ values
        sigma_values = [0.5, 1.0, 2.0]
        numerical_matrices = []
        
        for i, sigma in enumerate(sigma_values):
            # Calculate Fisher Information Matrix values
            I_mu_mu = 1 / (sigma**2)
            I_sigma_sigma = 2 / (sigma**2)
            
            # Create matrix
            matrix = Matrix(
                [[f"{I_mu_mu:.2f}", "0.00"],
                 ["0.00", f"{I_sigma_sigma:.2f}"]],
                left_bracket="[",
                right_bracket="]"
            ).scale(0.8)
            
            # Add σ label
            sigma_label = Text(f"σ = {sigma}", font_size=14, color=YELLOW)
            matrix_group = VGroup(matrix, sigma_label).arrange(DOWN, buff=0.2)
            
            numerical_matrices.append(matrix_group)
        
        # Arrange matrices horizontally
        matrices_row = VGroup(*numerical_matrices).arrange(RIGHT, buff=1.0).next_to(numerical_title, DOWN, buff=0.5)
        
        # Show matrices one by one
        for matrix_group in numerical_matrices:
            self.play(FadeIn(matrix_group), run_time=0.5)
        
        self.wait(2)
        
        # Show interpretation
        interpretation = VGroup(
            Text("Interpretation:", font_size=16, color=WHITE),
            Text("• Smaller σ → Larger Fisher Information → More precise parameter estimates", font_size=14, color=BLUE),
            Text("• Larger σ → Smaller Fisher Information → Less precise parameter estimates", font_size=14, color=GREEN),
            Text("• μ and σ are orthogonal (no interaction) in normal distribution", font_size=14, color=YELLOW)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(DOWN)
        self.play(Write(interpretation))
        self.wait(2)
        
        # Clear and show general case
        self.play(FadeOut(numerical_title), FadeOut(matrices_row), FadeOut(interpretation))
        
        # Show general case for n parameters
        general_title = Text("General Case: n Parameters", font_size=18, color=WHITE).next_to(fisher_matrix_title, DOWN)
        self.play(Write(general_title))
        
        # Show general matrix structure
        general_matrix = Matrix(
            [[r"(I(\theta))_{11}", r"(I(\theta))_{12}", r"\cdots", r"(I(\theta))_{1n}"],
             [r"(I(\theta))_{21}", r"(I(\theta))_{22}", r"\cdots", r"(I(\theta))_{2n}"],
             [r"\vdots", r"\vdots", r"\ddots", r"\vdots"],
             [r"(I(\theta))_{n1}", r"(I(\theta))_{n2}", r"\cdots", r"(I(\theta))_{nn}"]],
            left_bracket="[",
            right_bracket="]"
        ).scale(0.7).next_to(general_title, DOWN, buff=0.5)
        
        self.play(Create(general_matrix))
        self.wait(2)
        
        # Show properties
        properties = VGroup(
            Text("Matrix Properties:", font_size=16, color=WHITE),
            Text("• Symmetric: (I(θ))_ij = (I(θ))_ji", font_size=14, color=BLUE),
            Text("• Positive Semi-definite: All eigenvalues ≥ 0", font_size=14, color=GREEN),
            Text("• Measures information content about parameters", font_size=14, color=YELLOW),
            Text("• Used in Cramér-Rao bound and maximum likelihood estimation", font_size=14, color=ORANGE)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(DOWN)
        self.play(Write(properties))
        self.wait(2)
        
        # Clear and show final summary
        self.play(FadeOut(general_title), FadeOut(general_matrix), FadeOut(properties))
        
        # Final summary
        summary = VGroup(
            Text("Fisher Information Matrix Summary", font_size=20, color=YELLOW),
            Text("• (I(θ))_ij measures information about parameters θ_i and θ_j", font_size=16, color=WHITE),
            Text("• Matrix elements are expectations of log-likelihood derivatives", font_size=16, color=BLUE),
            Text("• Diagonal elements: Information about individual parameters", font_size=16, color=GREEN),
            Text("• Off-diagonal elements: Information about parameter interactions", font_size=16, color=ORANGE),
            Text("• Used in statistical inference and estimation theory", font_size=16, color=RED)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN)
        
        self.play(Write(summary))
        self.wait(3)
