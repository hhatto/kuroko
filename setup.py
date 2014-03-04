#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

exec(open('okonomi/_version.py').read())

setup(
    name='okonomi',
    version=__version__,
    description="Minimalistic Python Bot Framework",
    long_description=open("README.rst").read(),
    license='MIT License',
    author='Hideo Hattori',
    author_email='hhatto.jp@gmail.com',
    url='https://github.com/hhatto/okonomi',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords="bot framework",
    install_requires=('logbook', 'crontab', 'watchdog'),
    packages=['okonomi'],
    zip_safe=False,
)
