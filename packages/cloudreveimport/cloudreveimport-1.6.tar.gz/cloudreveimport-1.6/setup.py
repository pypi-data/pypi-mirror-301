#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

package_dir = {
    'cloudreveimport': 'cloudreveimport',
}

setup(
    name='cloudreveimport',
    version='1.6',
    author='yindaheng98',
    author_email='yindaheng98@gmail.com',
    url='https://github.com/yindaheng98/cloudreveimport',
    description=u'Import your existing files into cloudreve!',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir=package_dir,
    packages=[key for key in package_dir],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
