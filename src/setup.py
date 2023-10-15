#!/usr/bin/env python3

from setuptools import setup, find_packages

import sylva as sylva

setup(
    name='sylva',
    packages=find_packages(where="."),
    package_dir={"sylva": "."},
    install_requires=[
        "python-dateutil==2.8.2",
        "pyyaml==6.0.1",
        "pymongo==4.5.0"
    ],
    tests_require=[],
    version=sylva.__version__,
    description='',
    download_url='',
    long_description="""A library providing classes for sylva-etl.""",
    platforms='OS Independent',
    classifiers=[],
)