from setuptools import setup, find_packages, Extension
import os
from pathlib import Path
import platform

# Define the .pyd/.so file to be included
def get_shared_lib_file():
    ext = '.pyd' if platform.system() == 'Windows' else '.so'
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(ext):
                print(file)
                return os.path.join(root, file)
    return None

shared_lib_file = get_shared_lib_file()

# Check if the .pyd or .so file was found
if not shared_lib_file:
    raise RuntimeError(f"No shared library file (.pyd or .so) found in the package directory")

setup(
    name="pyrvs",
    version="0.37",
    author="Daniele Bonatto, Sarah Fachada",
    author_email="daniele.bonatto@ulb.be",
    description="Reference View Synthesizer (RVS) python package.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mpeg-i-visual/rvs",  # Optional if hosted on GitHub
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
    packages=find_packages(include=["pyrvs", "pyrvs.*"]),
    include_package_data=True,
    package_data={
        '_pyrvs': [shared_lib_file],  # Corrected to the _pyrvs directory
    },
)
