from __future__ import division, unicode_literals, absolute_import
import re


def match(regex, string):
    return search('^' + regex, string)


def search(regex, string):
    match = re.search(regex, string)
    if match:
        if not match.groups():
            return string
        return ','.join(match.groups())
