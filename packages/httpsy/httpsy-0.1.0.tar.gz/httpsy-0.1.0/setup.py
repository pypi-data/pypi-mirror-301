from setuptools import setup, find_packages

setup(
    name="httpsy",
    version="0.1.0",
    description="A simple Python package for sending http request",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
