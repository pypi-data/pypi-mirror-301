import io
import os
import re
import sys
from shutil import rmtree
from typing import List
from torch.utils.cpp_extension import BuildExtension, CppExtension, CUDAExtension
from setuptools import Command, find_packages, setup

# Package meta-data.
name = "codeformer_kit"
description = "Unstructured set of the helper functions."
url = "https://github.com/datvtn/codeformer_kit"
email = "thanhdatnv2712@gmail.com"
author = "Dat Viet Thanh Nguyen"
requires_python = ">=3.8"
current_dir = os.path.abspath(os.path.dirname(__file__))


def get_version():
    version_file = os.path.join(current_dir, name, "__init__.py")
    with io.open(version_file, encoding="utf-8") as f:
        return re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', f.read(), re.M).group(1)

def make_cuda_ext(name, module, sources, sources_cuda=None):
    if sources_cuda is None:
        sources_cuda = []
    define_macros = []
    extra_compile_args = {'cxx': []}

    # if torch.cuda.is_available() or os.getenv('FORCE_CUDA', '0') == '1':
    if  os.getenv('FORCE_CUDA', '0') == '1':
        define_macros += [('WITH_CUDA', None)]
        extension = CUDAExtension
        extra_compile_args['nvcc'] = [
            '-D__CUDA_NO_HALF_OPERATORS__',
            '-D__CUDA_NO_HALF_CONVERSIONS__',
            '-D__CUDA_NO_HALF2_OPERATORS__',
        ]
        sources += sources_cuda
    else:
        print(f'Compiling {name} without CUDA')
        extension = CppExtension

    return extension(
        name=f'{module}.{name}',
        sources=[os.path.join(*module.split('.'), p) for p in sources],
        define_macros=define_macros,
        extra_compile_args=extra_compile_args)

# What packages are required for this module to be executed?
try:
    with open(os.path.join(current_dir, "requirements.txt"), encoding="utf-8") as f:
        required = f.read().split("\n")
except FileNotFoundError:
    required = []

# What packages are optional?
extras = {"test": ["pytest"]}

version = get_version()

about = {"__version__": version}


def get_test_requirements():
    requirements = ["pytest"]
    if sys.version_info < (3, 3):
        requirements.append("mock")
    return requirements


def get_long_description():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(base_dir, "README.md"), encoding="utf-8") as f:
        return f.read()


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options: List = []

    @staticmethod
    def status(s):
        """Print things in bold."""
        print(s)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(os.path.join(current_dir, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution...")
        os.system(f"{sys.executable} setup.py sdist bdist_wheel --universal")

        self.status("Uploading the package to PyPI via Twine...")
        os.system("twine upload dist/*")

        self.status("Pushing git tags...")
        os.system("git tag v{}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


if '--cuda_ext' in sys.argv:
    ext_modules = [
        make_cuda_ext(
            name='deform_conv_ext',
            module='ops.dcn',
            sources=['src/deform_conv_ext.cpp'],
            sources_cuda=['src/deform_conv_cuda.cpp', 'src/deform_conv_cuda_kernel.cu']),
        make_cuda_ext(
            name='fused_act_ext',
            module='ops.fused_act',
            sources=['src/fused_bias_act.cpp'],
            sources_cuda=['src/fused_bias_act_kernel.cu']),
        make_cuda_ext(
            name='upfirdn2d_ext',
            module='ops.upfirdn2d',
            sources=['src/upfirdn2d.cpp'],
            sources_cuda=['src/upfirdn2d_kernel.cu']),
    ]
    sys.argv.remove('--cuda_ext')
else:
    ext_modules = []

setup(
    name=name,
    version=version,
    description=description,
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Dat Viet Thanh Nguyen",
    license="MIT",
    url=url,
    packages=find_packages(exclude=["tests", "docs", "images"]),
    install_requires=required,
    extras_require=extras,
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    cmdclass={"upload": UploadCommand, 'build_ext': BuildExtension},
    setup_requires=['cython', 'numpy'],
    ext_modules=ext_modules,
)