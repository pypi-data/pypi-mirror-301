#include <torch/extension.h>
#include <cuda.h>
#include <cuda_runtime.h>

// CUDA kernel for computing the squared differences
__global__ void mse_loss_kernel(const float* rendered_image, const float* ground_truth_image, float* loss, int size) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= size) return;

    float diff = rendered_image[idx] - ground_truth_image[idx];
    atomicAdd(loss, diff * diff);  // Accumulate the squared difference
}

// CUDA wrapper for computing MSE loss
torch::Tensor rendering_loss_cuda(torch::Tensor rendered_image, torch::Tensor ground_truth_image) {
    // Ensure the images have the same size
    TORCH_CHECK(rendered_image.sizes() == ground_truth_image.sizes(), "Images must have the same dimensions");

    // Total number of elements (H * W * 3)
    int size = rendered_image.numel();

    // Initialize the loss tensor to zero
    auto loss = torch::zeros(1, torch::device(rendered_image.device()).dtype(rendered_image.dtype()));

    // Define the block and grid sizes for CUDA
    int threads_per_block = 256;
    int num_blocks = (size + threads_per_block - 1) / threads_per_block;

    // Launch the kernel
    mse_loss_kernel<<<num_blocks, threads_per_block>>>(
        rendered_image.data_ptr<float>(),
        ground_truth_image.data_ptr<float>(),
        loss.data_ptr<float>(),
        size
    );

    // Ensure the CUDA kernel execution is completed
    cudaDeviceSynchronize();

    // Compute the mean loss (divide by number of elements)
    return loss / size;
}