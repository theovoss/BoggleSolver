#!/usr/bin/env python

"""
Setup script for Boggle Solver.
"""

import setuptools

from bogglesolver import __project__, __version__

import os
if os.path.exists('README.md'):
    README = open('README.md').read()
else:
    README = ""  # a placeholder, readme is generated on release
CHANGES = open('CHANGES.md').read()


setuptools.setup(
    name=__project__,
    version=__version__,

    description="Boggle Solver is a Python 3 package for solving Boggle boards.",
    url='http://pypi.python.org/pypi/BoggleSolver',
    author='Theo Voss',
    author_email='theo.voss973@gmail.com',

    packages=setuptools.find_packages(),

    entry_points={'console_scripts': []},

    long_description=(README + '\n' + CHANGES),
    license='WTFPL',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
    ],

    install_requires=[],
)
