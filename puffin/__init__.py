from __future__ import division, unicode_literals, absolute_import

from tempfile import NamedTemporaryFile
import argparse
import codecs
import shutil
import sys

from puffin import lib as puflib


def determine_streams(args):
    if args.file:
        for f in args.file:
            stream = codecs.open(f, 'r', 'utf8')
            if args.in_place is None:
                out = sys.stdout
            else:
                out = NamedTemporaryFile('w')
            yield stream, out
    else:
        yield sys.stdin, sys.stdout


def post_process(args, stream_in, stream_out):
    if args.in_place is not None and getattr(stream_in, 'name'):
        if args.in_place:
            shutil.move(stream_in.name, stream_in.name + args.in_place)
        shutil.move(stream_out.name, stream_in.name)


def interpret_stream(stream_in, line=False, skip_header=False, separator=None):
    if stream_in.isatty():
        yield {}
    else:
        if skip_header:
            stream_in.readline()  # skip, so no action necessary
        if line:
            for l, row in puflib.parse_lines(stream_in, separator):
                local = {
                    'line': l,
                    'row': row,
                    }
                yield local
        else:
            yield puflib.parse_buffer(stream_in, separator)


def evaluate(local, command, file):
    if file:
        execfile(file, globals(), local)
    elif command:
        return puflib.safe_evaluate(command, globals(), local)
    else:
        raise ValueError('Must supply either command or file.')


def main(params=None):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-l', '--line',
                    help='Execute the command for each line of input.',
                    action='store_true', default=False)
    # parsing arguments
    parser.add_argument('-s', '--separator', help='Custom column separator.', default=None)
    parser.add_argument('-t', '--tab-separator', help='Use tab as the column separator.', 
                        action='store_true', default=False)
    parser.add_argument('-h', '--skip-header',
                        help='Skip the first line of the stream.',
                        action='store_true', default=False)
    # execution options
    parser.add_argument('-b', '--before',
                        help='Statement to execute before the command '
                             '(e.g. set up accumulation variables).', default=None)
    parser.add_argument('-f', '--command-file',
                        help='Execute the file (instead of evaluating a '
                             'command). Incompatible with -r.', default=None)
    # output options
    parser.add_argument('-r', '--raw',
                        help='Print the raw result of the command. '
                             '(No smart display.)',
                        action='store_true', default=False)
    parser.add_argument('-i', '--in-place',
                        help='Edit files in-place, saving backups with the specified extension. '
                             'If a zero-length extension is given, no backup will be saved. '
                             'It is not recommended to give a zero-length extension when in-place '
                             'editing files, as you risk corruption or partial content in situations '
                             'where disk space is exhausted, etc.', default=None)
    parser.add_argument('--help', action='help', help='Display this help message.')
    parser.add_argument('--version', action='store_true', help='Display the version.')
    parser.add_argument('command', nargs='?')
    parser.add_argument('file', nargs='*')

    args = parser.parse_args(params)
    if args.tab_separator:
        args.separator = '\t'

    if args.version:
        import pkg_resources
        print pkg_resources.get_distribution('puffin').version
        return
    if not (args.command or args.command_file):
        return parser.print_help()

    if args.before:
        exec args.before in globals()

    for stream_in, stream_out in determine_streams(args):
        for local in interpret_stream(stream_in, args.line,
                                      args.skip_header, args.separator):
            result = evaluate(local, args.command, args.command_file)
            if args.command_file:
                continue
            if args.raw:
                puflib.display_raw(result, stream_out)
            else:
                puflib.display(result, stream_out)
        post_process(args, stream_in, stream_out)
