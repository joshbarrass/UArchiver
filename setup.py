#!/usr/bin/env python3
# coding: utf-8
import codecs
import os
import sys
from uarchiver import VERSION

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
    name='uarchiver',
    version=VERSION,
    description='Ultimate Archiver -- A modular archiving tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='joshbarrass',
    author_email='josh.barrass.work@gmail.com',
    url='https://github.com/joshbarrass/UArchiver',
    scripts=['uarchiver'],
    packages=['udl'],
    package_dir={
        'udl': 'udl',
    },
    install_requires=['docopt>=0.6.2', 'youtube_dl'],
    keywords='downloader archive dump',
    classifiers=[
        'Intended Audience :: End Users/Developers/Archivers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ]
)
