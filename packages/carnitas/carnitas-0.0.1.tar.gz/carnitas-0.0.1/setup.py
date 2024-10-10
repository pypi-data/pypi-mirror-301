from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Audio processing suite for Long Lab at UCLA.' 

# Setting up
setup(
    name="carnitas",
    version=VERSION,
    author="Maxwell Xu",
    author_email="<maxwellxu@g.ucla.edu>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'pydub', 'boxsdk'],
    keywords=['python', 'audio'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)