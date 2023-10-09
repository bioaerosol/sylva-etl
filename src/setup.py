#!/usr/bin/env python3

from setuptools import setup, find_packages

import sylva as sylva

setup(
    name='sylva',
    packages=find_packages(where="."),
    package_dir={"sylva": "./sylva"},
    install_requires=[
        "python-dateutil==2.8.2"
    ],
    tests_require=[],
    version=sylva.__version__,
    description='',
    download_url='',
    long_description="""A library providing classes for sylva-etl.""",
    platforms='OS Independent',
    classifiers=[],
)