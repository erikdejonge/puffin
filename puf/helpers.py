# coding=utf-8
"""
-
"""
from __future__ import division, unicode_literals, absolute_import
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import re


def match(regex, string, flags=0):
    """

    :param regex:
    :param string:
    :param flags:
    :return:
    """
    return search('^' + regex, string, flags)


def search(regex, string, flags=0):
    """

    :param regex:
    :param string:
    :param flags:
    :return:
    """
    match2 = re.search(regex, string, flags)
    if match:
        if not match2.groups():
            return string
        return ','.join(match2.groups())
