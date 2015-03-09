# coding=utf-8
"""
-
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from setuptools import setup
setup(name='puffin',
      version='0.2.0',

      description='Python replacement for awk',
      url='http://github.com/kespindler/puffin',
      author='Kurt Spindler',
      author_email='kespindler@gmail.com',
      license='MIT',
      packages=['puf'],
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'puf=puf.cli:main',
          ],
      },
      requires=['future', 'unittester', 'fabric'])
