from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A Python Tool Package'
LONG_DESCRIPTION = 'A Python library full of tools that make python code more readable and make life easy!'

# Setting up
setup(
    name="pryttier",
    version=VERSION,
    author="HussuBro010 (Hussain Vohra)",
    author_email="<hussainv2807@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib', 'pandas'],
    keywords=['python', 'graphing', 'math', 'tools', 'colors'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
