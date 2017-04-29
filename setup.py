# -*- coding: utf-8 -*-
import setuptools

setuptools.setup(
    name="funcmap",
    version="1.0.0",
    url="",

    author="Arne Küderle",
    author_email="a.kuederle@gmail.com",

    description="A small Python module to provide convenient mapping between Python functions and text input",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    test_suite='tests',

    license='LICENSE.txt',

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
