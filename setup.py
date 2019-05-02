#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script. Based on Jeff Knupp's Demo + Cookiecutter"""
import io
import os
from setuptools import setup, find_packages


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


NAME = 'tiingo'
AUTHOR = "Cameron Yick"
EMAIL = 'cameron.yick@gmail.com'
URL = 'https://github.com/hydrosquall/tiingo-python'
DESCRIPTION = "REST Client for Tiingo Data Platform API"
LONG_DESCRIPTION = read('README.rst', 'HISTORY.rst')

requirements = [
    'requests',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
    'vcrpy',
]

# Metadata about the module
# Load the package's __version__.py module as a dictionary.
# Via https://github.com/kennethreitz/setup.py/blob/master/setup.py
here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(include=[NAME]),
    include_package_data=True,
    install_requires=requirements,
    extras_require={'pandas': ['pandas>=0.18']},
    license="MIT license",
    zip_safe=False,
    keywords=['tiingo', 'finance', 'stocks', 'rest'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Office/Business :: Financial :: Investment',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
