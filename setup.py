#! /usr/bin/env python
from setuptools import setup
import gmat_py_simple

# some pip versions bark on comments
def read_without_comments(filename):
    with open(filename) as f:
        return [line for line in f.read().splitlines() if not len(line) == 0 and not line.startswith('#')]

test_required = read_without_comments('test-requirements')

setup(name='gmat_py_simple',
      version="0.0.1",
      py_modules=['gmat_py_simple'],
      # generate platform specific start script
      install_requires=[],
      url='https://github.com/paulk2space/GMAT-Python-simple',
      download_url='https://github.com/paulk2space/GMAT-Python-simple',
      keywords=[],
      maintainer='Paul DeTrempe, I guess',
      classifiers=['Development Status :: None'],
      description='Wrapper around GMAT python API to make it easier to use',
      long_description=open('README.md').read(),
      license='MIT',
      )