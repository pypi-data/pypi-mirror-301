from setuptools import setup, find_packages

setup(
    name="ideariver_core",                # Name of the package to be published on PyPI
    version="0.1.6",                      # Version of the package
    description="Core library for ideariver, containing abstract DTOs and interfaces.",  # Short description
    long_description=open("README.md").read(),  # Read the long description from the README
    long_description_content_type="text/markdown",  # README format
    author="ideariver",                    # Organization name
    author_email="contact@ideariver.com",  # Contact email
    url="https://github.com/nima70/ideariver-core-python",  # URL to your project repo
    packages=find_packages(),              # Automatically find packages (inside ideariver_core)
    classifiers=[                          # Metadata for the project
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',               # Minimum Python version
)
