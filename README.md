# Math Visualizations

A project for creating mathematical visualizations using Manim, featuring affine curves, non-Euclidean manifolds, and information geometry.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run visualizations:

### Affine Curves
```bash
manim -pql simple_scene.py AffineCurves
manim -pql advanced_scene.py AdvancedAffineCurves
manim -pql coordinate_system_2d.py CoordinateSystem2D
```

### Non-Euclidean Manifolds
```bash
manim -pql non_euclidean_2d.py NonEuclidean2D
manim -pql manifold_scene.py NonEuclideanManifold
manim -pql torus_manifold.py TorusManifold
manim -pql manifold_projection.py ManifoldProjection
manim -pql metric_projection.py MetricProjection
manim -pql cauchy_sequences_topology.py CauchySequencesTopology
manim -pql parametric_space_visualization.py ParametricSpaceVisualization
```

### Information Geometry
```bash
manim -pql information_geometry.py InformationGeometry
manim -pql statistical_manifolds.py StatisticalManifolds
manim -pql ml_information_geometry.py MLInformationGeometry
manim -pql fisher_metric_visualization.py FisherMetricVisualization
manim -pql fisher_metric_detailed.py FisherMetricDetailed
manim -pql fisher_information_manifold.py FisherInformationManifold
```

### Smooth Manifolds & Differential Geometry
```bash
manim -pql manifold_charts_atlas.py ManifoldChartsAtlas
manim -pql metric_tensor_visualization.py MetricTensorVisualization
manim -pql affine_connection_visualization.py AffineConnectionVisualization
manim -pql metric_tensor_3d.py MetricTensor3D
manim -pql affine_connection_3d.py AffineConnection3D
```

## Features

### Affine Curves
- **Simple Affine Curves**: Parabola and ellipse with basic visualization
- **Advanced Affine Curves**: Parabola, ellipse, hyperbola, and circle
- **2D Coordinate System**: Coordinate grid with line between two points, distance calculation, slope, and line equation
- Interactive animations with moving points along curves
- Mathematical labels and equations

### Non-Euclidean Manifolds
- **2D Non-Euclidean Geometry**: Curved coordinate systems and geodesic deviation
- **3D Manifold Surfaces**: Hyperbolic paraboloids and curved spaces
- **Torus Manifold**: Parallel transport and geodesic paths on curved surfaces
- **Manifold Projections**: Mapping curved spaces to Euclidean coordinates
- **Metric Projections**: How metric tensors change under coordinate transformations
- **Cauchy Sequences in Non-Point Based Topology**: Convergence in abstract topological spaces
- **Parametric Space Visualization**: Exploring spaces defined by parameters and their evolution

### Manifold Projections
- **3D to 2D Projection**: Shows how curved manifolds appear when flattened
- **Metric Tensor Projection**: Demonstrates metric distortion under coordinate changes
- **Side-by-side Comparison**: Curved vs. flat coordinate systems
- **Geodesic Projection**: How shortest paths change under projection
- **Coordinate Grid Distortion**: Visual representation of metric changes

### Information Geometry
- **Basic Concepts**: Parameter space, probability space, Fisher metric
- **Statistical Manifolds**: Exponential families, natural and expectation parameters
- **Machine Learning Applications**: Natural gradient descent, optimization
- **Fisher Metric Visualization**: Distance between probability distributions
- **Detailed Fisher Analysis**: Probability density functions and metric evolution
- **Fisher Information Matrix on Statistical Manifold**: How probability distributions shape the manifold and determine distances

### Smooth Manifolds & Differential Geometry
- **Charts & Atlas**: Local coordinate systems covering the manifold
- **Chart Transformations**: Smooth transitions between coordinate systems
- **Metric Tensor g**: Defines distances, angles, and volumes on the manifold
- **Affine Connection ∇**: Determines parallel transport and geodesics
- **Tangent Spaces**: Local linearization of the manifold
- **Geodesic Equations**: Paths that minimize distance with respect to the metric
- **3D Metric Tensor**: Enhanced visualization showing metric on curved 3D surfaces
- **3D Affine Connection**: Advanced visualization of parallel transport and connection coefficients in 3D

## Mathematical Concepts

- **Affine Transformations**: Curves that preserve geometric properties under linear transformations
- **Non-Euclidean Geometry**: Spaces where parallel lines can intersect
- **Manifolds**: Curved surfaces with intrinsic geometry
- **Geodesics**: Shortest paths on curved surfaces
- **Parallel Transport**: How vectors change when moved along curved paths
- **Metric Tensor**: Mathematical object that defines distances and angles
- **Coordinate Projections**: How curved geometry appears in flat coordinates
- **Metric Distortion**: The effect of curvature on geometric measurements
- **Statistical Manifolds**: Spaces where points represent probability distributions
- **Fisher Information**: Metric that measures the information content of parameters
- **Natural Gradient**: Optimization method that respects the geometry of probability space
- **Exponential Families**: Important class of probability distributions with special geometric properties
- **Smooth Manifolds**: Topological spaces locally resembling Euclidean space
- **Charts & Atlas**: Collections of coordinate systems covering the manifold
- **Metric Tensor**: Mathematical object defining distances, angles, and volumes
- **Affine Connection**: Structure defining parallel transport and geodesics
- **Christoffel Symbols**: Connection coefficients in local coordinates
- **Parallel Transport**: Process of moving vectors along curves while maintaining parallelism

## Applications

- **Machine Learning**: Natural gradient descent, optimization on statistical manifolds
- **Statistics**: Maximum likelihood estimation, Bayesian inference
- **Physics**: Thermodynamics, quantum mechanics, general relativity
- **Neuroscience**: Neural coding and information processing
- **Information Theory**: Data compression, communication theory
- **Differential Geometry**: Modern geometric analysis and topology

## Requirements

- Python 3.8+
- Manim Community Edition
- NumPy, Matplotlib, SciPy

## Output

All visualizations generate high-quality MP4 videos in the `media/videos/` directory, perfect for:
- Mathematical presentations
- Educational content
- Research visualization
- Interactive demonstrations
- Understanding differential geometry concepts
- Learning information geometry and statistical inference
