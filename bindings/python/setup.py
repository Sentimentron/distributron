#!/bin/env python3

import os
from setuptools import setup, find_packages

setup(
    name = "distrib",
    version = "0.1.0",
    author = "Richard Townsend",
    author_email = "richard@sentimentron.co.uk",
    description = ("Python bindings for Distributron"),
    license = "BSD",
    keywords = "microservices service discovery",
    url = "https://github.com/Sentimentron/distributron",
    packages=["distrib"],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    test_suite = 'discover_tests',
)
