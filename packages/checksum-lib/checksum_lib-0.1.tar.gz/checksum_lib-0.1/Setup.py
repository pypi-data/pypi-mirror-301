# setup.py
from setuptools import setup, find_packages

setup(
    name="checksum_lib",
    version="0.1",
    packages=find_packages(),
    description="Uma biblioteca simples para calcular e validar checksums.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Luiz Felipe",
    author_email="luiz.nogueira@ufpi.edu.br",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
