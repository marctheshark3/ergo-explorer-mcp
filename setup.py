#!/usr/bin/env python
"""
Setup script for ergo-mcp package.
"""

from setuptools import setup, find_packages

setup(
    name="ergo-mcp",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "mcp>=0.5.0",
        "httpx",
        "python-dotenv",
        "argparse",
    ],
    entry_points={
        "console_scripts": [
            "ergo-mcp=ergo_explorer.__main__:main",
        ],
    },
    author="Ergo MCP Team",
    author_email="info@example.com",
    description="MCP server for exploring and analyzing the Ergo blockchain",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/marctheshark3/ergo-mcp",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
) 