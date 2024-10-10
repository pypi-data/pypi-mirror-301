# setup.py
from setuptools import setup, find_packages

setup(
    name="ideariver-services",  # new package name
    version="0.1.2",  # updated version number
    description="A collection of services used by the ideariver ecosystem.",
    author="Your Name",
    author_email="youremail@example.com",
    packages=find_packages(),
    install_requires=[
        # your dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

