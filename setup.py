#!/usr/bin/env python

from distutils.core import setup

setup(name='py-t2n',
      version='0.1',
      description='Talk To NXT with Python',
      author='Quentin Stievenart',
      author_email='quentin.stievenart@gmail.com',
      url='http://awesom.eu/~acieroid/articles/py-t2n.html',
      license='Gnu GPL v3',
      scripts=['py-t2n'],
      requires=['nxt']
      )
