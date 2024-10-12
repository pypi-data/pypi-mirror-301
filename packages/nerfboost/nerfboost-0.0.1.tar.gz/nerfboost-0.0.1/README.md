# nerfboost

**nerfboost** is a CUDA-accelerated Python package that enhances common operations required for Neural Radiance Fields (NeRF) models. It provides high-performance implementations of key functions such as positional encoding, stratified sampling, volume rendering, and more, to accelerate NeRF training and rendering.

## Features

- **CUDA-accelerated functions** for efficient neural rendering tasks.
- Implements key operations for NeRF models like:
  - Positional encoding
  - Stratified, uniform, and hierarchical sampling
  - Volume rendering
  - MLP network processing
  - Rendering loss computation
- Easy integration with PyTorch using custom CUDA kernels.

## Installation

You can install **nerfboost** using the following command:

```bash
pip install nerfboost