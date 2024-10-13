from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Logger'
LONG_DESCRIPTION = 'A package to make printing system'

# Setting up
setup(
    name="Cosmic-2",
    version=VERSION,
    author="Developer Vivek",
    author_email="ravanxd739@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['colorama','datetime'],
    keywords=['python', 'tutorial', 'CosmicLogger', 'area', 'developerravan'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)