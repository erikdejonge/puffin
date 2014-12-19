import sys
import argparse

# additional namespaces for execution
import random
import os
import re
import collections
import math

def interp(i):
    try:
        return int(i)
    except ValueError:
        pass
    try:
        return float(i)
    except ValueError:
        pass
    return i


def parse(stream, sep=None):
    rows = []
    lines = []
    for line in stream:
        lines.append(line.rstrip('\n'))
        row = [interp(i) for i in line.split(sep)]
        rows.append(row)
    cols = zip(*rows)
    return {
        'rows': rows,
        'lines': lines,
        'cols': cols,
    }


def display(result):
    if isinstance(result, basestring):
        return result
    if isinstance(result, collections.Mapping):
        return '\n'.join('%s=%s' % (k, v) for k, v in result.iteritems())
    if isinstance(result, collections.Iterable):
        return '\n'.join(str(x) for x in result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--separator', help='Separator between lines', default=None)
    parser.add_argument('-r', '--raw', help='Do not coerce row results', type=bool, default=False)
    parser.add_argument('-f', '--file', help='File to execute (instead of passed command.)', default=None)
    parser.add_argument('command', nargs='?')

    args = parser.parse_args()

    stream = sys.stdin
    if not stream.isatty():
        parsed_locals = parse(sys.stdin, args.separator)
    else:
        parsed_locals = {}

    if args.file:
        execfile(args.file, globals(), parsed_locals)
    elif args.command:
        result = eval(args.command, globals(), parsed_locals)
        if args.raw:
            print result
        else:
            print display(result)
    else:
        parser.print_help()