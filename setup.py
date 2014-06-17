from __future__ import print_function

import sys
import os.path
from setuptools import setup, find_packages

readme = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = open(readme).read()

setup(
    name='docdriver',
    version='0.0.1',
    author='Fabio Pliger',
    author_email='fabio.pliger@gmail.com',
    url='',
    license='MIT',
    platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],
    description='DocDriver, a documention generator from test comments',
    long_description=long_description,
    keywords='docdriver webdriver comments documentation generator',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Operating System :: POSIX",
        "Topic :: Utilities",
        ],
    install_requires=['mako', 'click'],
)