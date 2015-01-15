#!/usr/bin/env python
""" Setup file for PyNginxConfig package """
 
from distutils.core import setup
setup(
    name='pynginxconfig',
    version='0.3.4',
    description=' PyNginxConfig - NginX config parser and generator',
    long_description = "PyNginxConfig is a python module for parsing and generating NginX configuration files. Module can parse blocks and single values of unlimited nesting.",
    author='Makarov Yurii',
    author_email='winnerer@yandex.com',
    url='http://code.google.com/p/pynginxconfig/',
    #packages=[ 'pynginxconfig', ],
    py_modules=[ 'pynginxconfig', ],

    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
    ),
    license="MIT",
)