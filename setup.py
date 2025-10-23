#!/usr/bin/env python3
"""
Setup script for AI + Intangible Cultural Heritage Thangka Image Restoration System
Developed by Wangchuk Mind
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("Django/requirements_paddle.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="thangka-restoration-ai",
    version="1.0.0",
    author="Wangchuk Mind",
    author_email="wangchuk.mind@example.com",
    description="AI-powered Thangka image restoration for intangible cultural heritage preservation",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/thangka-restoration-ai",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/thangka-restoration-ai/issues",
        "Source": "https://github.com/yourusername/thangka-restoration-ai",
        "Documentation": "https://github.com/yourusername/thangka-restoration-ai/wiki",
        "Hugging Face": "https://huggingface.co/yourusername/thangka-restoration-ai",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: PaddlePaddle",
    ],
    keywords=[
        "thangka", "cultural-heritage", "image-restoration", "ai", "paddlepaddle",
        "diffusion-models", "lora", "art-restoration", "intangible-cultural-heritage",
        "computer-vision", "image-processing", "machine-learning", "deep-learning"
    ],
    python_requires=">=3.9",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "thangka-restore=thangka_restoration.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "thangka_restoration": [
            "configs/*.yaml",
            "configs/*.json",
            "models/*.json",
            "templates/*.html",
            "static/*",
        ],
    },
    zip_safe=False,
)
