# coding=utf-8
# coding=utf-8
"""
unittester
-
Active8 (05-03-15)
author: erik@a8.nl
license: GNU-GPL2
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from unittester import *

import unittest
from io import StringIO

import sys
import re
from tempfile import NamedTemporaryFile
from puf import cli
from puf import cli_lib as puflib


class StreamCaptureTest(unittest.TestCase):

    def assertWasStreamed(self, s):
        """
        @type s: str, unicode
        @return: None
        """
        self.sout.seek(0)
        self.assertEqual(self.sout.read(), s)

    def setUp(self):
        """
        setUp
        """
        self._stdout = sys.stdout
        self._stdin = sys.stdin
        self.sout = StringIO()
        self.sin = StringIO()
        sys.stdout = self.sout
        sys.stdin = self.sin

    def tearDown(self):
        """
        tearDown
        """
        sys.stdout = self._stdout
        sys.stdin = self._stdin


class TestInterpret(unittest.TestCase):

    def test_intrepret(self):
        """
        test_intrepret
        """
        self.assertEqual(puflib.interpret_segment('5'), 5)
        self.assertEqual(puflib.interpret_segment('5.5'), 5.5)
        self.assertEqual(puflib.interpret_segment('a string'), 'a string')


class TestParsing(unittest.TestCase):

    def test_parse_lines(self):
        """
        test_parse_lines
        """
        stream = StringIO(
            'foo    bar   \n'
            '5       3   \n'
        )
        results = list(puflib.parse_lines(stream))

        # line 1
        self.assertEqual(results[0][0], 'foo    bar   ')
        self.assertSequenceEqual(results[0][1], ['foo', 'bar'])

        # line 2
        self.assertEqual(results[1][0], '5       3   ')
        self.assertSequenceEqual(results[1][1], [5, 3])

    def test_parse_lines_separator(self):
        """
        test_parse_lines_separator
        """
        stream = StringIO(
            'id,name\n'
            '5,banana\n'
        )
        results = list(puflib.parse_lines(stream, ','))

        # line 1
        self.assertEqual(results[0][0], 'id,name')
        self.assertSequenceEqual(results[0][1], ['id', 'name'])

        # line 2
        self.assertEqual(results[1][0], '5,banana')
        self.assertSequenceEqual(results[1][1], [5, 'banana'])

    def test_parse_buffer(self):
        """
        test_parse_buffer
        """
        stream = StringIO(
            'foo    bar   \n'
            '5       3   \n'
        )
        result = puflib.parse_buffer(stream)

        # line 1
        self.assertSequenceEqual(result['lines'], [

            'foo    bar   ',
            '5       3   '
        ])
        self.assertSequenceEqual(result['rows'], [

            ['foo', 'bar'],
            [5, 3]
        ])
        self.assertSequenceEqual(result['cols'], [

            ('foo', 5),
            ('bar', 3)
        ])


class TestRetryEval(unittest.TestCase):

    def test_retry_eval(self):
        """
        test_retry_eval
        """
        self.assertEqual(puflib.safe_evaluate('math.ceil(3.3)', {}, {}), 4)
        self.assertRaises(NameError, puflib.safe_evaluate, 'invalid_object.foo', {}, {})


class TestDisplay(unittest.TestCase):

    def test_display_string(self):
        """
        test_display_string
        """
        stream = StringIO()
        puflib.display('hello', stream)
        stream.seek(0)
        self.assertEqual(stream.read(), 'hello\n')

    def test_display_none(self):
        """
        test_display_none
        """
        stream = StringIO()
        puflib.display(None, stream)
        stream.seek(0)
        self.assertEqual(stream.read(), '')

    def test_display_iterable(self):
        """
        test_display_iterable
        """
        stream = StringIO()
        puflib.display([1, None, 2, 'None', 3], stream)
        stream.seek(0)
        self.assertEqual(stream.read(), '1\n2\nNone\n3\n')

    def test_display_mapping(self):
        """
        test_display_mapping
        """
        stream = StringIO()
        puflib.display({'a': 5, 'b': 3, 'c': None, 'd': 'None'}, stream)
        stream.seek(0)
        self.assertEqual(stream.read(), 'a=5\nb=3\nd=None\n')

    def test_display_number(self):
        """
        test_display_number
        """
        stream = StringIO()
        puflib.display(5, stream)
        stream.seek(0)
        self.assertEqual(stream.read(), '5\n')


class TestMain(StreamCaptureTest):

    def test_main(self):
        """
        test_main
        """
        cli.main(['range(4)'])
        self.assertWasStreamed('0\n1\n2\n')

    def test_main_initial(self):
        """
        test_main_initial
        """
        self.assertRaises(NameError, cli.main, ['fake_object'])

        cli.main(['-b', 'fake_object=5', 'fake_object*2'])
        self.assertWasStreamed('10\n')

    def test_main_raw(self):
        """
        test_main_raw
        """
        cli.main(['-r', 'range(3)'])
        self.assertWasStreamed('[0, 1, 2]\n')

    def test_main_linemode(self):
        """
        test_main_linemode
        """
        self.sin.write('file1\nfile2\nfile3')
        self.sin.seek(0)
        cli.main(['-l', 'line+".txt"'])
        self.assertWasStreamed('file1.txt\nfile2.txt\nfile3.txt\n')

    def test_main_skipheader(self):
        """
        test_main_skipheader
        """
        self.sin.write('pid\n5\n3')
        self.sin.seek(0)
        cli.main(['-hl', 'row[0]*2'])
        self.assertWasStreamed('10\n6\n')

    def test_version(self):
        """
        test_version
        """
        cli.main(['--version'])
        self.sout.seek(0)
        streamed = self.sout.read()
        self.assertTrue(re.match('\d+\.\d+\.\d+$', streamed))

    def test_passed_file(self):
        """
        test_passed_file
        """
        t = NamedTemporaryFile()
        t.write('bye\n')
        t.flush()
        cli.main(['-l', 'line.replace("bye", "hi")', t.name])
        self.assertWasStreamed('hi\n')

    def test_passed_file_twice(self):
        """
        test_passed_file_twice
        """
        t = NamedTemporaryFile()
        t.write('bye\n')
        t.flush()
        cli.main(['-l', 'line.replace("bye", "hi")', t.name, t.name])
        self.assertWasStreamed('hi\nhi\n')

    def test_in_place_modification(self):
        """
        test_in_place_modification
        """
        t = NamedTemporaryFile()
        t.write('bye\n')
        t.flush()
        extension = '.bak'
        backup = t.name + extension
        cli.main(['-l', '-i', extension, 'line.replace("bye", "hi")', t.name])
        with open(backup) as f:
            self.assertEqual(f.read(), 'bye\n')

        with open(t.name) as f:
            self.assertEqual(f.read(), 'hi\n')

    def test_in_place_no_extension(self):
        """
        test_in_place_no_extension
        """
        t = NamedTemporaryFile()
        t.write('bye\n')
        t.flush()
        extension = ''
        cli.main(['-l', '-i', extension, 'line.replace("bye", "hi")', t.name])
        with open(t.name) as f:
            self.assertEqual(f.read(), 'hi\n')


def main():
    """
    main
    """
    unit_test_main(globals())


if __name__ == "__main__":
    main()
