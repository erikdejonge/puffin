from __future__ import division, unicode_literals
import collections
import re


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
    separator = None if separator is None else unicode(separator)
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
    cols = zip(*rows)
    return {
        'rows': rows,
        'lines': lines,
        'cols': cols,
        }


def display_raw(result, stream):
    stream.write(unicode(result))
    stream.write('\n')


def display(result, stream):
    """
    Intelligently print the result (or pass if result is None).

    :param result:
    :return: None
    """
    if result is None:
        return
    elif isinstance(result, basestring):
        pass
    elif isinstance(result, collections.Mapping):
        result = u'\n'.join(u'%s=%s' % (k, v) for
                            k, v in result.iteritems() if v is not None)
    elif isinstance(result, collections.Iterable):
        result = u'\n'.join(unicode(x) for x in result if x is not None)
    else:
        result = unicode(result)
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
    try:
        return eval(command, glob, local)
    except NameError as e:
        match = re.match("name '(.*)' is not defined", e.message)
        if not match:
            raise e
        try:
            exec ('import %s' % (match.group(1), )) in glob
        except ImportError:
            raise e
        return safe_evaluate(command, glob, local)
