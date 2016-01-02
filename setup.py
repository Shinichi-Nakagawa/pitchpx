#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__author__ = 'Shinichi Nakagawa'


setup(
    name='pitchpx',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'beautifulsoup4',
        'click',
        'FormEncode',
        'lxml',
        'python-dateutil',
        'pytz',
        'PyYAML',
    ],
    entry_points="""
        [console_scripts]
        pitchpx = pitchpx:main
    """,
)