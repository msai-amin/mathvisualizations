# Math Visualizations

A project for creating mathematical visualizations using Manim, featuring affine curves and non-Euclidean manifolds.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run visualizations:

### Affine Curves
```bash
manim -pql simple_scene.py SimpleAffineCurves
manim -pql advanced_scene.py AdvancedAffineCurves
```

### Non-Euclidean Manifolds
```bash
manim -pql non_euclidean_2d.py NonEuclidean2D
manim -pql manifold_scene.py NonEuclideanManifold
manim -pql torus_manifold.py TorusManifold
```

## Features

### Affine Curves
- **Simple Scene**: Parabola (y = x²) and Ellipse (x²/4 + y² = 1)
- **Advanced Scene**: Parabola, Ellipse, Hyperbola (x² - y² = 1), and Circle (x² + y² = 2)
- Interactive animations with moving points along curves
- Mathematical labels and equations

### Non-Euclidean Manifolds
- **2D Non-Euclidean Geometry**: Demonstrates curved space concepts
- **3D Hyperbolic Paraboloid**: Shows manifold embedded in 3D space
- **Torus Manifold**: Demonstrates intrinsic curvature and parallel transport
- Geodesic curves and coordinate grids
- Tangent vectors and parallel transport visualization

## Mathematical Concepts

- **Affine Transformations**: Curves that preserve geometric properties under linear transformations
- **Non-Euclidean Geometry**: Spaces where parallel lines can intersect
- **Manifolds**: Curved surfaces with intrinsic geometry
- **Geodesics**: Shortest paths on curved surfaces
- **Parallel Transport**: How vectors change when moved along curved paths

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
