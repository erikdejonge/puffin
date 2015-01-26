from __future__ import division, unicode_literals, absolute_import
import re


def match(regex, string, flags=0):
    return search('^' + regex, string, flags)


def search(regex, string, flags=0):
    match = re.search(regex, string, flags)
    if match:
        if not match.groups():
            return string
        return ','.join(match.groups())
