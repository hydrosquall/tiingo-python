#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script. Based on Jeff Knupp's Demo + Cookiecutter"""
import io
from setuptools import setup, find_packages


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = read('README.rst', 'HISTORY.rst')

requirements = [
    'requests',
]

setup_requirements = [
    'pytest-runner',
    # TODO: put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
]

setup(
    name='tiingo',
    version='0.3.0',
    description="REST Client for Tiingo Data Platform API",
    long_description=long_description,
    author="Cameron Yick",
    author_email='cameron.yick@enigma.com',
    url='https://github.com/hydrosquall/tiingo-python',
    packages=find_packages(include=['tiingo']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords=['tiingo', 'finance', 'stocks'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
