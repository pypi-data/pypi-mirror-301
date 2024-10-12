from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

setup(
    name='nerfboost',
    ext_modules=[
        CUDAExtension(
            name='nerfboost',
            sources=[
                'nerfboost/positional_encoding.cu', 
                'nerfboost/sampling.cu',
                'nerfboost/volume_rendering.cu',
                'nerfboost/mlp_network.cu',
                'nerfboost/rendering_loss.cu',
                'nerfboost/generate_rays.cu',
                'nerfboost/pybind_module.cu'
            ]
        )
    ],
    cmdclass={
        'build_ext': BuildExtension
    }
)