from __future__ import division, print_function
import sys
import argparse
import collections
import codecs
import re


def interp(i):
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
    for line in stream:
        line = line.rstrip('\n')
        row = [interp(i) for i in line.split(separator)]
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


def display(result):
    """
    Intelligently print the result (or pass if result is None).

    :param result:
    :return: None
    """
    if result is None:
        pass
    elif isinstance(result, basestring):
        print(result)
    elif isinstance(result, collections.Mapping):
        print('\n'.join('%s=%s' % (k, v) for
                        k, v in result.iteritems() if v is not None))
    elif isinstance(result, collections.Iterable):
        print('\n'.join(str(x) for x in result if x is not None))
    else:
        print(str(result))


def retry_eval(command, glob, local):
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
        return retry_eval(command, glob, local)


def execute(local, glob, command=None, file=None, raw=False):
    """
    Execute either command or file using the passed dictionaries.
    Intelligently print the result (unless raw=True is passed)

    :param local: locals dict for exec
    :param glob: globals dict for exec
    :param command: command for eval
    :param file: file for exec
    :param raw: bool to print the result directly
    :return: None
    """
    if file:
        execfile(file, glob, local)
    else:
        result = retry_eval(command, glob, local)
        if raw:
            print(result)
        else:
            display(result)


def main(params=None):
    parser = argparse.ArgumentParser(add_help=False)
    # for, line, puf -
    parser.add_argument('-l', '--line',
                    help='Execute the command for each line of input.',
                    action='store_true', default=False)
    parser.add_argument('-s', '--separator', help='Custom column separator.', default=None)
    parser.add_argument('-h', '--skip-header',
                        help='Skip the first line of the stream.',
                        action='store_true', default=False)
    parser.add_argument('-r', '--raw',
                        help='Print the raw result of the command. '
                             '(No smart display.)',
                        action='store_true', default=False)
    parser.add_argument('-i', '--initial',
                        help='Statement to execute before the command '
                             '(e.g. set up accumulation variables).',
                        default=None)
    #parser.add_argument('-f', '--file',
    #                    help='Execute the file (instead of a '
    #                         'command). Incompatible with -l and -r.',
    #                    default=None)
    parser.add_argument('--help', action='help', help='Display this help message.')
    parser.add_argument('--version', action='store_true', help='Display the version.')
    parser.add_argument('command', nargs='?')
    parser.add_argument('file', nargs='?')

    args = parser.parse_args(params)

    if args.version:
        import pkg_resources
        print(pkg_resources.get_distribution('puffin').version)
        return
    if not args.command:  # or args.file:
        return parser.print_help()

    if args.file:
        stream = codecs.open(args.file, 'r', 'utf8')
    else:
        stream = sys.stdin

    if args.initial:
        exec args.initial in globals()

    if stream.isatty():
        execute({}, globals(), args.command, None, args.raw)
    else:
        if args.skip_header:
            stream.readline()  # skip, so no action necessary
        if args.line:
            for line, row in parse_lines(stream, args.separator):
                local = {
                    'line': line,
                    'row': row,
                }
                execute(local, globals(), args.command, None, args.raw)
        else:
            local = parse_buffer(stream, args.separator)
            execute(local, globals(), args.command, None, args.raw)
