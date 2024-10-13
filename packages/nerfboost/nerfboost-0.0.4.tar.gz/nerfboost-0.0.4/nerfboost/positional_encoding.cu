#include <torch/extension.h>
#include <cuda.h>
#include <cuda_runtime.h>

// CUDA Kernel for Positional Encoding
__global__ void positional_encoding_kernel(float* x, float* encoded, int L, int x_size, int x_dim) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    if (idx >= x_size * x_dim) return;

    // Get the index of the element in x
    int element_idx = idx / x_dim;  // Which row of x this element belongs to
    int dim_idx = idx % x_dim;      // Which dimension in the x vector (e.g., 0, 1, or 2)

    float value = x[element_idx * x_dim + dim_idx];  // Get the current value of x

    // Perform the sine and cosine computations for each frequency
    for (int i = 0; i < L; i++) {
        float freq = powf(2.0f, i);  // Compute 2^i for the frequency

        // Store sine and cosine values in alternating positions, matching the CPU version
        encoded[element_idx * (x_dim * 2 * L) + i * 2 * x_dim + dim_idx] = sinf(freq * value);       // Sine value
        encoded[element_idx * (x_dim * 2 * L) + (i * 2 + 1) * x_dim + dim_idx] = cosf(freq * value);  // Cosine value
    }
}

// Launcher for the CUDA kernel
torch::Tensor positional_encoding_cuda(torch::Tensor x, int L) {
    int x_size = x.size(0);  // Number of elements (rows) in x
    int x_dim = x.size(1);   // Number of dimensions in each element (columns)

    // Create an output tensor to hold the encoded values
    auto encoded = torch::zeros({x_size, x_dim * 2 * L}, torch::device(x.device()).dtype(x.dtype()));

    // Launch the CUDA kernel
    int threads_per_block = 256;
    int num_blocks = (x_size * x_dim + threads_per_block - 1) / threads_per_block;

    positional_encoding_kernel<<<num_blocks, threads_per_block>>>(
        x.data_ptr<float>(),  // Input tensor (x)
        encoded.data_ptr<float>(),  // Output tensor (encoded)
        L,  // Number of encoding frequencies
        x_size,  // Number of elements in x
        x_dim  // Number of dimensions in each element
    );

    return encoded;
}