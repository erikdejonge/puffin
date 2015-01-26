from __future__ import division, unicode_literals, absolute_import

import argparse

from puf import cli_lib


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

    glob = {}
    if args.before:
        exec args.before in glob

    for stream_in, stream_out in cli_lib.determine_streams(args):
        for local in cli_lib.interpret_stream(
                stream_in, args.line, args.skip_header, args.separator):
            result = cli_lib.evaluate(local, glob, args.command, args.command_file)
            if args.command_file:
                continue
            try:
                if args.raw:
                    cli_lib.display_raw(result, stream_out)
                else:
                    cli_lib.display(result, stream_out)
            except IOError:
                return
        cli_lib.post_process(args, stream_in, stream_out)
