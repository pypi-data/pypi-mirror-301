from setuptools import setup, find_packages
import os
import platform

# Path to the compiled .pyd/.so file
def get_shared_lib_file():
    ext = '.pyd' if platform.system() == 'Windows' else '.so'
    lib_path = os.path.join('_pyrvs', f'pyrvs.cp310-win_amd64{ext}')
    if os.path.isfile(lib_path):
        return lib_path
    raise FileNotFoundError(f"Shared library file not found: {lib_path}")

shared_lib_file = get_shared_lib_file()

setup(
    name="pyrvs",
    version="0.38",
    author="Daniele Bonatto, Sarah Fachada",
    author_email="daniele.bonatto@ulb.be",
    description="Reference View Synthesizer (RVS) python package.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mpeg-i-visual/rvs",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    zip_safe=False,
    install_requires=[
        'pybind11>=2.6.0',
        'numpy',
        'opencv-python'
    ],
    packages=find_packages(include=["pyrvs", "_pyrvs", "pyrvs.*", "_pyrvs.*"]),
    include_package_data=True,
    package_data={
        '_pyrvs': [shared_lib_file],  # Include the precompiled .pyd file
    },
)
