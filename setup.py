import io
from setuptools import setup, find_packages

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fo:
    long_description = fo.read()

pkg = "bash_like"
setup(
    name=pkg,
    version="0.1.2",
    url="https://github.com/seanbreckenridge/bash_like",
    author="Sean Breckenridge",
    author_email="seanbrecke@gmail.com",
    description=(
        """A small utility library to handle arguments and read/write text to files using bash-like syntax"""
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    packages=find_packages(include=["bash_like"]),
    package_data={pkg: ['py.typed']},
    keywords="shell file",
    extras_require={
        "testing": [
            "pytest",
            "mypy",
        ]
    },
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
