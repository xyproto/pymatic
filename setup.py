# -*- coding: utf-8 -*-

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pymatic",
    version = "0.1",
    author = "Alexander Rødseth",
    author_email = "rodseth@gmail.com",
    description = ("Library for automating GUI applications"),
    license = "MIT",
    keywords = "GUI automation xte",
    url = "http://github.com/xyproto/pymatic",
    packages=['pymatic'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Automation",
        "License :: OSI Approved :: MIT",
    ],
)
