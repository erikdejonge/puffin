# Puffin

Puffin is a Python replacement for awk, cut, tr, and many other command line tools. Use familiar Python instead of a half dozen tools.

    # Other method to sum a column of numbers
    $ wc -l *.txt  | awk '{s+=$1} END {print $s}'
    468
    # Puffin
    $ wc -l *.txt  | puf 'sum(cols[0])'
    468

    # Other methods to get the second column of a csv
    $ awk -F "\"*,\"*" '{print $2}' data.csv > names.txt
    $ cat data.csv | cut -f2 -s > names.txt
    # Puffin
    $ puf -s, 'cols[1]' data.csv > names.txt


PRs, issues (especially use cases that Puffin doesn't currently address) welcome.

## Install

    pip install puffin

## Quickstart

#### Puffin evaluates arbitrary python code

    $ puf 27/2.5
    10.8

    $ puf 'range(3)'
    0
    1
    2

#### Puffin understands the input

    $ wc -l *.txt  | puf 'sum(cols[0])'
    468

#### Puffin can do complex filters in a single pass

    # gives pids of all processes owned by kurt
    $ ps aux | puf -l 'row[1] if row[0] == "kurt" else None'
    5231
    155
    ...

## Description

#### Basics

Puffin reads its input and creates 3 variables (`lines`, `rows`, `cols`). It then evaluates
the given python command and attempts to intelligently print the result.

- *lines* - an array of each newline-stripped line of stream
- *rows* - the separated components of each line
- *cols* - each column of the stream

Some examples of these in action

    # Turn a list into comma-separated values
    $ puf '",".join(lines)' invalid.txt
    3021,4439,9544,3985,1262

    # Check the validity of a csv
    $ puf -s, '[len(r) for r in rows]' cities.csv
    13
    14
    13
    13

    # Get all pids
    $ ps aux | puf -h 'cols[1]'
    5231
    155
    ...

    # Get every second pid
    $ ps aux | puf 'cols[::2]'
    5231
    5495
    ...

#### Line operation

With the `-l` option, Puffin evaluates the command on each line individually.
Lines that evaluate to None are skipped, allowing complex filtering of results.
In this case, the provided namespace is just `line` and `row`.

    # filter for all pids owned by kurt and have pid mod 10
    $ ps aux | puf -l 'row[1] if row[0] == "kurt" and row[1] % 10 == 0 else None'
    48560
    94390
    ...

#### Import statements

Puffin will attempt to import anything that is unreferenced.

    $ puf 'uuid.uuid4()'
    f079dbbe-6bbc-430a-a3d1-e0f53a0ef719

Specifically, Puffin will catch `NameError`s and attempt an import. If that fails with ImportError, it re-raises.

## Options

    -l, --line

Puffin normally operates on the entire stream at a single time. This option changes that behavior to perform the operation per line.
This also changes the available local variables to `line` and `row`.

    -s SEPARATOR, --separator SEPARATOR

Use this option to split lines into rows and columns on something other than whitespace (comma is a common alternative)

    -t, --tab-separator

This is equivalent to `-s$'\t'`.

      -h, --skip-header

Some streams (`ps`, csv files) have headers. This option skips the first line of the input stream so you don't have to worry about
handling those lines correctly.

      -r, --raw

Normally, puffin tries to intelligently display results.

      -b BEFORE, --before BEFORE

Puffin will execute this command before anything else, in order to set up accumulation variables, do import renames, or other setup.

      -f FILE, --file FILE

Puffin can instead execute a regular python file with the namespace of `lines`, `rows`, `cols`. Puffin executes this file
as normal Python, without intelligent printing of any results, etc. This option is incompatible with -l and -r.

    -i IN_PLACE, --in-place IN_PLACE

This is the same as `sed`s in-place option. Pass a file extension and pass file arguments to `puffin`. Sed will then replace the contents of the file
with the results from the puffin operation, creating a backup with the provided extenion. It's suggested using the `-l` option in conjunction. If you
do not want a backup, you must pass the empty string with a space in bash like so: `puf -i '' <command>`.

## Testing

Run `make test` or `make cover`. Currently 95% coverage.

## Extras

Puffins are members of the family of birds Alcidae, or Auks.
