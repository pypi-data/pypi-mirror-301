# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import re

with open('requirements-package.txt') as f:
    requirements = f.read().splitlines()

with open('shellypy/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="shellypy2",
    version=version,
    author="Sebastian Wolf",
    author_email="sebastian.wolf@pace-systems.de",
    description="Wrapper around the Shelly HTTP api forked from shellypy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SeRoWo83/ShellyPy",
    packages=find_packages(),
    license="MIT",
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
