
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymotor",
    version="0.2.7",
    install_requires=[
            'matplotlib==2.2.2',
            'numpy==1.15.0',
            'pandas==0.23.4',
            'scipy==1.1.0',
      ],
    author="Randy Rubin",
    author_email="randymrubin@gmail.com",
    description="Generates motion and force profiles.",
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
