# setup.py

from setuptools import setup, find_packages

setup(
    name="Your_library",
    version="0.1.0",
    description="A simple example of a Python library",
    author="SABBOT Zouhair",
    author_email="sabbout6@gmail.com",
    url="https://github.com/sabbotzouhair/Your_library",
    packages=find_packages(),  # Automatically find all packages (Your_library in this case)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
