#!/usr/bin/env python
# encoding: utf-8

# from distutils.core import setup
from setuptools import setup

long_description = 'This a simple text translator, which can use Yandex or MyMemory translation services'
setup(
    name='translator',
    version="1.0.1",
    author='Dmitrii Sokolov',
    author_email='sokolovdp@gmail.com',
    description="Simple text translator",
    long_description=long_description,
    url=None,
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Education',
                 'Intended Audience :: End Users/Desktop',
                 'License :: Freeware',
                 'Operating System :: POSIX',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: MacOS :: MacOS X',
                 'Topic :: Education',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6'],
    install_requires=['requests',],
    scripts=['translator.py'],
)
