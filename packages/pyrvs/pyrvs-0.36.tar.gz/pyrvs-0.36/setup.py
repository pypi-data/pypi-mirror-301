from setuptools import setup, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext

import os

# Define the .pyd file to be included
def get_pyd_file():
    # Assuming the pyd file is in the pyrvs folder
    pyd_file = None
    for file in os.listdir('pyrvs'):
        if file.endswith('.pyd'):
            pyd_file = file
            break
    return pyd_file

pyd_file = get_pyd_file()

setup(
    name="pyrvs",
    version="0.36",
    author="Daniele Bonatto, Sarah Fachada",
    author_email="daniele.bonatto@ulb.be",
    description="Reference View Synthesizer (RVS) python package.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mpeg-i-visual/rvs",  # Optional if hosted on GitHub
    license="MIT",  # Specify your license
    cmdclass={"build_ext": build_ext},
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
    packages=find_packages(include=["pyrvs", "pyrvs.*"]),  # Adjust this to your package
    include_package_data=True,  # Include package data specified below
    package_data={
        'pyrvs': [pyd_file],  # Include the .pyd file in the pyrvs package
    },
)
