#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

try:
    from pypandoc import convert
    long_description = convert('README.md', 'rst')
except IOError:
    print("warning: README.md not found")
    long_description = ""
except (ImportError, OSError):
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    long_description = ""

setup(
    name="pybossa-pbs",
    version="3.0.0",
    author="Scifabric LTD",
    author_email="info@scifabric.com",
    description="PYBOSSA command line client",
    long_description=long_description,
    license="AGPLv3",
    url="https://github.com/Scifabric/pbs",
    classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',],
    py_modules=['pbs', 'helpers', 'pbsexceptions'],
    install_requires=['Click>=7.0, <7.1', 'pybossa-client>=3.0.0, <3.1.0', 'requests', 'nose', 'mock', 'coverage',
                      'rednose', 'pypandoc', 'simplejson', 'jsonschema', 'polib', 'watchdog', 'openpyxl'],
    entry_points='''
        [console_scripts]
        pbs=pbs:cli
    '''
)
