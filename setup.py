# SPDX-License-Identifier: MIT
#!/usr/bin/env python3
"""Setup script for Gemini Vision MCP Server."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="gemini-vision-mcp",
    version="1.0.0",
    description="MCP server for image analysis using Gemini 2.5 Pro through OpenRouter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/your-username/gemini-vision-mcp",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "mcp>=1.0.0",
        "aiohttp>=3.8.0",
        "Pillow>=9.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "mypy>=1.0.0",
            "flake8>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gemini-vision-mcp=gemini_vision.server:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="mcp model-context-protocol gemini vision image-analysis claude openrouter",
    project_urls={
        "Bug Reports": "https://github.com/your-username/gemini-vision-mcp/issues",
        "Source": "https://github.com/your-username/gemini-vision-mcp",
        "Documentation": "https://github.com/your-username/gemini-vision-mcp#readme",
    },
)