from setuptools import setup, find_packages

VERSION = '0.0.6'
DESCRIPTION = 'Collection of utility python modules'

# Setting up
setup(
    name="cloudycustoms",
    version=VERSION,
    author="CloudEater (Nath Abraham)",
    author_email="<nathCloud@gmail.com>",
    description=DESCRIPTION,
    long_description="A collection of utility python modules. Uses python random module",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'utility', 'random', 'numbers'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.12"
    ]
)