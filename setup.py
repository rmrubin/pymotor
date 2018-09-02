
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymotor",
    version="0.3.5",
    install_requires=[
            'matplotlib',
            'numpy',
            'pandas',
            'scipy',
      ],
    author="Randy Rubin",
    author_email="randymrubin@gmail.com",
    description="Generates motion, force and torque profiles for electric motor selection.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rmrubin/pymotor",
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Physics",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
