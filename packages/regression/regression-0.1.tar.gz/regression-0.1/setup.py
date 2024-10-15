from setuptools import setup, find_packages
setup(
    name="regression",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.26.1",
        "matplotlib>=3.8.0"
    ]
)