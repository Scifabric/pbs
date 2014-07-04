#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
    long_description = read_md('README.md')
except IOError:
    print("warning: README.md not found")
    long_description = ""
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    long_description = ""

setup(
    name="pybossa-pbs",
    version="1.0",
    author="Daniel Lombraña González",
    author_email="info@pybossa.com",
    description="PyBossa command line client",
    long_description=long_description,
    license="AGPLv3",
    url="https://github.com/PyBossa/pbs",
    classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',],
    py_modules=['pbs', 'helpers'],
    install_requires=['Click', 'pybossa-client', 'requests', 'nose', 'mock', 'coverage',
                      'rednose', 'pypandoc'],
    entry_points='''
        [console_scripts]
        pbs=pbs:cli
    '''
)
