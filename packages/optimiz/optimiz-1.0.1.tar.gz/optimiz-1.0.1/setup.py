from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="optimiz",
    version="1.0.1",
    author="Amitesh Gangrade",
    author_email="gangradeamitesh@gmail.com",
    description="A simple optimization library for machine learning",
    long_description="A simple Optimization Library for Machine Learning Algorithms ",
    long_description_content_type="text/markdown",
    url="https://github.com/gangradeamitesh/optimiz_it.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy",
        "matplotlib",
    ],
)