#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="pbs",
    version="1.0",
    author="Daniel Lombraña González",
    author_email="info@pybossa.com",
    description="PyBossa command line client",
    license="AGPLv3",
    url="https://github.com/PyBossa/pbs",
    classifiers = ['Development Status :: 0 - Production',
                   'Environment :: Consle',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU Affer v3',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',],
    py_modules=['pbs'],
    install_requires=['Click', 'pybossa-client', 'requests', 'nose', 'mock', 'coverage',
                      'rednose'],
    entry_points='''
        [console_scripts]
        pbs=pbs:cli
    '''
)
