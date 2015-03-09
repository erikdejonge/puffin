# coding=utf-8
"""
-
"""
from __future__ import division, unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from builtins import int
from future import standard_library
standard_library.install_aliases()
from builtins import zip
from builtins import str

import collections
import re
from tempfile import NamedTemporaryFile

import codecs
import shutil
import sys


def interpret_segment(i):
    """
    Attempt to coerce i to an int or float
    :param i:
    :return:
    """
    try:
        return int(i)
    except ValueError:
        pass
    try:
        return float(i)
    except ValueError:
        pass

    return i


def parse_lines(stream, separator=None):
    """
    Takes each line of a stream, creating a generator that yields
    tuples of line, row - where row is the line split by separator
    (or by whitespace if separator is None.
    :param stream:
    :param separator: (optional)
    :return: generator
    """
    separator = None if separator is None else str(separator)
    for line in stream:
        line = line.rstrip(u'\r\n')
        row = [interpret_segment(i) for i in line.split(separator)]
        yield line, row


def parse_buffer(stream, separator=None):
    """
    Returns a dictionary of the lines of a stream, an array of rows of the
     stream (split by separator), and an array of the columns of the stream
     (also split by separator)
    :param stream:
    :param separator:
    :return: dict
    """
    rows = []
    lines = []

    for line, row in parse_lines(stream, separator):
        lines.append(line)
        rows.append(row)

    cols = list(zip(*rows))
    return {
        'rows': rows,
        'lines': lines,
        'cols': cols,
    }


def display_raw(result, stream):
    """
    :param result:
    :param stream:
    """
    stream.write(str(result))
    stream.write('\n')


def display(result, stream):
    """
    Intelligently print the result (or pass if result is None).
    :param stream:
    :param result:
    :return: None
    """
    if result is None:
        return
    elif isinstance(result, str):
        pass
    elif isinstance(result, collections.Mapping):
        result = u'\n'.join(u'%s=%s' % (k, v) for
                            k, v in result.items() if v is not None)

    elif isinstance(result, collections.Iterable):
        result = u'\n'.join(str(x) for x in result if x is not None)
    else:
        result = str(result)

    stream.write(result.encode('utf8'))
    stream.write('\n')


def safe_evaluate(command, glob, local):
    """
    Continue to attempt to execute the given command, importing objects which
    cause a NameError in the command

    :param command: command for eval
    :param glob: globals dict for eval
    :param local: locals dict for eval
    :return: command result
    """
    while True:
        try:
            return eval(command, glob, local)
        except NameError as e:
            match = re.match("name '(.*)' is not defined", str(e))

            if not match:
                raise e

            try:
                exec(('import %s' % (match.group(1), )), glob)
            except ImportError:
                raise e


def determine_streams(args):
    """
    :param args:
    """
    if args.file:
        for f in args.file:
            # noinspection PyArgumentEqualDefault
            stream = codecs.open(f, 'r', 'utf8')

            if args.in_place is None:
                out = sys.stdout
            else:
                out = NamedTemporaryFile('w')
            yield stream, out
    else:
        yield sys.stdin, sys.stdout


def post_process(args, stream_in, stream_out):
    """
    :param args:
    :param stream_in:
    :param stream_out:
    """
    if args.in_place is not None and getattr(stream_in, 'name'):
        if args.in_place:
            shutil.move(stream_in.name, stream_in.name + args.in_place)

        shutil.move(stream_out.name, stream_in.name)


def interpret_stream(stream_in, line=False, skip_header=False, separator=None):
    """
    :param stream_in:
    :param line:
    :param skip_header:
    :param separator:
    """
    if stream_in.isatty():
        yield {}
    else:
        if skip_header:
            stream_in.readline()  # skip, so no action necessary

        if line:
            for l, row in parse_lines(stream_in, separator):
                local = {
                    'line': l,
                    'row': row,
                }
                yield local
        else:
            yield parse_buffer(stream_in, separator)


def evaluate(local, glob, command, filename):
    """
    @type local: str, unicode
    @type glob: str, unicode
    @type command: str, unicode
    @type filename: str, unicode
    @return: None
    """
    if filename:
        with open(filename) as f:
            code = compile(f.read(), filename, 'exec')
            exec(code, glob, local)

    elif command:
        return safe_evaluate(command, glob, local)
    else:
        raise ValueError('Must supply either command or file.')
