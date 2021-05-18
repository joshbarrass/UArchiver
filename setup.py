#!/usr/bin/env python3
# coding: utf-8
import codecs
import os
import sys
from udl import VERSION

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist')
    os.system('twine upload dist/*')
    sys.exit()

with codecs.open('README.md') as f:
    long_description = f.read()

setup(
    name='UArchiver',
    version=VERSION,
    description='Ultimate Archiver -- A modular archiving tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='joshbarrass',
    author_email='josh.barrass.work@gmail.com',
    url='https://github.com/joshbarrass/UArchiver',
    scripts=['uarchiver'],
    packages=['udl', 'udl.kernels'],
    package_dir={
        'udl': 'udl',
        'udl.kernels': 'udl/kernels',
    },
    install_requires=['docopt>=0.6.2', 'youtube_dl'],
    keywords='downloader archive dump',
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
    ]
)
