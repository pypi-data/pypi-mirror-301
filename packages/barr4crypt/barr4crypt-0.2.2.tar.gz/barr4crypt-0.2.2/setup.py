import os
from setuptools import setup, find_packages

# Read the contents of README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="barr4crypt",
    version="0.2.2",
    author="Francisco Barreira",
    author_email="franbarreira0@gmail.com",
    description="A simple rotation-based encryption tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/francool57/barr4encrypt",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[],
)