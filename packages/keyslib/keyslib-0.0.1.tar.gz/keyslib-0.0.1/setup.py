#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="keyslib",
    version="0.0.1",
    license="MIT",
    description="a library and cli for key bindings",
    author="Adam Miller",
    author_email="miller@adammiller.io",
    url="https://github.com/adammillerio/keyslib",
    download_url="https://github.com/adammillerio/keyslib/archive/v0.0.1.tar.gz",
    keywords=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "python-dotenv",
        "invoke",
        "pyre-extensions",
    ],
    extras_require={"dev": ["ruff", "pyre-check", "testslide"]},
    entry_points="""
    [console_scripts]
    keys=keyslib.cli.cli:keys
  """,
)
