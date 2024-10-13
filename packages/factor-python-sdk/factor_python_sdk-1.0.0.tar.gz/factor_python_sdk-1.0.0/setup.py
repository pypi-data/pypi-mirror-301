# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="factor-python-sdk",  # Replace with your package name
    version="1.0.0",
    author="Factor",
    author_email="",
    description="A Python SDK for the Factor analytics platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codeibrahima/factor-python-sdk",  # Replace with your repository URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose your license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests>=2.20.0",
    ],
)
