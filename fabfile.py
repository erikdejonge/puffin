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
from fabric.api import task, local


@task
def publish():
    """
    publish
    """
    local('rm dist/*')
    local('python setup.py sdist')
    local('twine upload dist/*')


@task
def cover():
    """
    cover
    """
    local('coverage run --omit="venv/*,tests/*,/usr/local/lib/python*" -m unittest discover tests')
    local('coverage report')
    local('coverage html')
    local('open htmlcov/index.html')


@task
def test(path='discover'):
    """
    :param path:
    """
    local('python -m unittest ' + path)
