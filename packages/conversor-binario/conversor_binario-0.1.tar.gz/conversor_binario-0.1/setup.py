# setup.py

from setuptools import setup, find_packages

setup(
    name="conversor_binario",
    version="0.1",
    packages=find_packages(),
    author="Tiago",
    description="Um pacote para converter números binários para decimal, octal e hexadecimal.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
