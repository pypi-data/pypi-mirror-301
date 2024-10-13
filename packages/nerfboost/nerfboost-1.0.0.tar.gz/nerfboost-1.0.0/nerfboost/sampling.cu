#include <torch/extension.h>
#include <cuda.h>
#include <cuda_runtime.h>
#include <curand_kernel.h>  // Include curand for random number generation

// CUDA Kernel for Deterministic Stratified Sampling
__global__ void stratified_sampling_kernel(float* t_vals, float* stratified_samples, int num_samples) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (i < num_samples - 1) {
        // Calculate midpoint between consecutive t_vals
        stratified_samples[i] = 0.5f * (t_vals[i] + t_vals[i + 1]);
    }
}

// Launcher for the CUDA kernel
torch::Tensor stratified_sampling_cuda(float near, float far, int num_samples) {
    // Create an output tensor to hold the stratified samples (num_samples - 1)
    auto stratified_samples = torch::zeros({num_samples - 1}, torch::device(torch::kCUDA).dtype(torch::kFloat32));

    // Create a tensor to hold the t values (num_samples points)
    auto t_vals = torch::linspace(near, far, num_samples, torch::device(torch::kCUDA).dtype(torch::kFloat32));

    // Launch the CUDA kernel
    int threads_per_block = 256;
    int num_blocks = (num_samples - 1 + threads_per_block - 1) / threads_per_block;

    stratified_sampling_kernel<<<num_blocks, threads_per_block>>>(
        t_vals.data_ptr<float>(),        // Input t_vals
        stratified_samples.data_ptr<float>(),  // Output stratified_samples
        num_samples  // Number of samples
    );

    // Synchronize to ensure the kernel execution is complete
    cudaDeviceSynchronize();

    return stratified_samples;
}

// CUDA Kernel for Uniform Sampling
__global__ void uniform_sampling_kernel(float *t_vals, float near, float far, int num_samples) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < num_samples) {
        t_vals[i] = near + i * (far - near) / (num_samples - 1);
    }
}

// Launcher for the CUDA kernel
torch::Tensor uniform_sampling_cuda(float near, float far, int num_samples) {
    // Create an output tensor to hold the uniform samples
    auto t_vals = torch::zeros({num_samples}, torch::device(torch::kCUDA).dtype(torch::kFloat32));

    // Launch the CUDA kernel
    int threads_per_block = 256;
    int num_blocks = (num_samples + threads_per_block - 1) / threads_per_block;

    uniform_sampling_kernel<<<num_blocks, threads_per_block>>>(
        t_vals.data_ptr<float>(),  // Output t_vals
        near,  // Near value
        far,   // Far value
        num_samples  // Number of samples
    );

    // Synchronize to ensure the kernel execution is complete
    cudaDeviceSynchronize();

    return t_vals;
}


// Helper function to search CDF
__device__ int search_cdf(float *cdf, float u, int num_samples) {
    int low = 0;
    int high = num_samples - 1;

    while (low < high) {
        int mid = (low + high) / 2;
        if (cdf[mid] < u) {
            low = mid + 1;
        } else {
            high = mid;
        }
    }
    return low;
}

// CUDA Kernel for Hierarchical Sampling
__global__ void hierarchical_sampling_kernel(float *coarse_samples, float *cdf, float *fine_samples, int num_fine_samples, int num_coarse_samples) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < num_fine_samples) {  // Ensure index does not exceed the bounds
        
        // Initialize curand state using thread index as seed
        curandState state;
        curand_init(1234 + i, i, 0, &state);

        // Generate a random uniform number u between 0 and 1
        float u = curand_uniform(&state);

        // Get the index from the CDF search
        int idx = search_cdf(cdf, u, num_coarse_samples);

        // Use the index to sample from coarse_samples
        fine_samples[i] = coarse_samples[idx];
    }
}

// Launcher for the CUDA kernel
torch::Tensor hierarchical_sampling_cuda(torch::Tensor coarse_samples, torch::Tensor weights, int num_fine_samples) {
    int num_coarse_samples = coarse_samples.size(0);  // Get the number of coarse samples

    // Compute the CDF
    auto cdf = torch::cumsum(weights, 0);
    cdf = cdf / cdf[-1];

    // Create an output tensor to hold the fine samples
    auto fine_samples = torch::zeros({num_fine_samples}, torch::device(torch::kCUDA).dtype(torch::kFloat32));

    // Launch the CUDA kernel
    int threads_per_block = 256;
    int num_blocks = (num_fine_samples + threads_per_block - 1) / threads_per_block;

    hierarchical_sampling_kernel<<<num_blocks, threads_per_block>>>(
        coarse_samples.data_ptr<float>(),  // Coarse samples
        cdf.data_ptr<float>(),  // CDF
        fine_samples.data_ptr<float>(),  // Fine samples
        num_fine_samples,  // Number of fine samples
        num_coarse_samples  // Number of coarse samples
    );

    // Error checking and synchronization
    cudaError_t err = cudaGetLastError();
    if (err != cudaSuccess) {
        throw std::runtime_error("CUDA kernel launch failed: " + std::string(cudaGetErrorString(err)));
    }

    cudaDeviceSynchronize();

    return fine_samples;
}

// CUDA Kernel for Inverse Transform Sampling
__global__ void inverse_transform_sampling_kernel(float* cdf, int* samples, int num_samples, int cdf_size) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;

    if (i < num_samples) {
        // Initialize curand state
        curandState state;
        curand_init(1234, i, 0, &state);

        // Generate a uniform random number
        float u = curand_uniform(&state);

        // Search the CDF to find the corresponding sample
        int idx = search_cdf(cdf, u, cdf_size);

        // Store the sample index
        samples[i] = idx;
    }
}

// Launcher for the CUDA kernel
torch::Tensor inverse_transform_sampling_cuda(torch::Tensor weights, int num_samples) {
    int cdf_size = weights.size(0);

    // Compute the CDF on the host (or it can be done in the kernel if needed)
    auto cdf = torch::cumsum(weights, 0);
    cdf = cdf / cdf[-1];  // Normalize to 1

    // Allocate output tensor for the samples
    auto samples = torch::zeros({num_samples}, torch::device(torch::kCUDA).dtype(torch::kInt32));

    // Launch the CUDA kernel
    int threads_per_block = 256;
    int num_blocks = (num_samples + threads_per_block - 1) / threads_per_block;

    inverse_transform_sampling_kernel<<<num_blocks, threads_per_block>>>(
        cdf.data_ptr<float>(),  // CDF
        samples.data_ptr<int>(),  // Output samples
        num_samples,  // Number of samples
        cdf_size  // Size of the CDF
    );

    // Error checking and synchronization
    cudaError_t err = cudaGetLastError();
    if (err != cudaSuccess) {
        throw std::runtime_error("CUDA kernel launch failed: " + std::string(cudaGetErrorString(err)));
    }

    cudaDeviceSynchronize();

    return samples;
}