#!/usr/bin/env python3

from setuptools import setup

version = {}
with open("./src/cazart/version.py") as f:
    exec(f.read(), version)

with open("./README.md") as f:
    long_description = f.read()

setup(
    name="cazart",
    version=version["__version__"],
    license="MIT with restrictions",
    author="William Woodruff",
    author_email="william@yossarian.net",
    description="Flask + Schema = Cazart!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/woodruffw/cazart",
    packages=["cazart"],
    package_dir={"": "src"},
    platforms="any",
    python_requires=">=3.6",
    install_requires=[
        "flask",
        "schema",
    ],
    extras_require={
        "dev": [
            "flake8",
            "black",
            "isort[pyproject]",
            "pytest",
            "coverage",
            "twine",
        ]
    }
)
