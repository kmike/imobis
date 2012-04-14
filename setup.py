#!/usr/bin/env python
from distutils.core import setup

for cmd in ('egg_info', 'develop'):
    import sys
    if cmd in sys.argv:
        from setuptools import setup

try:
    import sys
    reload(sys).setdefaultencoding("UTF-8")
except NameError:
    # python3 doesn't need this
    pass

version='0.3'

setup(
    name='imobis',
    version=version,
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',

    packages=['imobis'],

    url='https://bitbucket.org/kmike/imobis/',
    license = 'MIT license',
    description = "Python interface to http://sms-manager.ru/ (aka http://www.imobis.ru/ )",

    long_description = open('README.rst').read(),

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
