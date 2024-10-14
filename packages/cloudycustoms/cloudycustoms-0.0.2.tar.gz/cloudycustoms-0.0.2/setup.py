from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'A collection of utility python modules'

# Setting up
setup(
    name="cloudycustoms",
    version=VERSION,
    author="CloudEater (Nath Abraham)",
    author_email="<nathCloud@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['random'],
    keywords=['python', 'utility', 'random', 'numbers'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.12"
    ]
)