import puffin
import unittest
from cStringIO import StringIO
import sys
import re


class TestInterpret(unittest.TestCase):
    def test_intrepret(self):
        self.assertEqual(puffin.interp('5'), 5)
        self.assertEqual(puffin.interp('5.5'), 5.5)
        self.assertEqual(puffin.interp('a string'), 'a string')


class TestParsing(unittest.TestCase):
    def test_parse_lines(self):
        stream = StringIO(
            'foo    bar   \n'
            '5       3   \n'
        )
        results = list(puffin.parse_lines(stream))
        # line 1
        self.assertEqual(results[0][0], 'foo    bar   ')
        self.assertSequenceEqual(results[0][1], ['foo', 'bar'])
        # line 2
        self.assertEqual(results[1][0], '5       3   ')
        self.assertSequenceEqual(results[1][1], [5, 3])

    def test_parse_lines_separator(self):
        stream = StringIO(
            'id,name\n'
            '5,banana\n'
        )
        results = list(puffin.parse_lines(stream, ','))
        # line 1
        self.assertEqual(results[0][0], 'id,name')
        self.assertSequenceEqual(results[0][1], ['id', 'name'])
        # line 2
        self.assertEqual(results[1][0], '5,banana')
        self.assertSequenceEqual(results[1][1], [5, 'banana'])

    def test_parse_buffer(self):
        stream = StringIO(
            'foo    bar   \n'
            '5       3   \n'
        )
        result = puffin.parse_buffer(stream)
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


class TestDisplay(unittest.TestCase):
    def assertWasStreamed(self, s):
        self.sout.seek(0)
        self.assertEqual(self.sout.read(), s)

    def setUp(self):
        self._stdout = sys.stdout
        self.sout = StringIO()
        sys.stdout = self.sout

    def tearDown(self):
        sys.stdout = self._stdout

    def test_display_string(self):
        puffin.display('hello')
        self.assertWasStreamed('hello\n')

    def test_display_none(self):
        puffin.display(None)
        self.assertWasStreamed('')

    def test_display_iterable(self):
        puffin.display([1, 2, 3])
        self.assertWasStreamed('1\n2\n3\n')

    def test_display_mapping(self):
        puffin.display({'a': 5, 'b': 3})
        self.assertWasStreamed('a=5\nb=3\n')

    def test_display_number(self):
        puffin.display(5)
        self.assertWasStreamed('5\n')


class TestRetryEval(unittest.TestCase):
    def test_retry_eval(self):
        self.assertEqual(puffin.retry_eval('math.ceil(3.3)', {}, {}), 4)
        self.assertRaises(NameError, puffin.retry_eval, 'invalid_object.foo', {}, {})


class TestMain(TestDisplay):
    def setUp(self):
        super(TestMain, self).setUp()
        self._stdin = sys.stdin
        self.sin = StringIO()
        sys.stdin = self.sin

    def tearDown(self):
        super(TestMain, self).tearDown()
        sys.stdin = self._stdin

    def test_main(self):
        puffin.main(['range(3)'])
        self.assertWasStreamed('0\n1\n2\n')

    def test_main_initial(self):
        self.assertRaises(NameError, puffin.main, ['fake_object'])
        puffin.main(['-i', 'fake_object=5', 'fake_object*2'])
        self.assertWasStreamed('10\n')

    def test_main_raw(self):
        puffin.main(['-r', 'range(3)'])
        self.assertWasStreamed('[0, 1, 2]\n')

    def test_main_linemode(self):
        self.sin.write('file1\nfile2\nfile3')
        self.sin.seek(0)
        puffin.main(['-l', 'line+".txt"'])
        self.assertWasStreamed('file1.txt\nfile2.txt\nfile3.txt\n')

    def test_main_skipheader(self):
        self.sin.write('pid\n5\n3')
        self.sin.seek(0)
        puffin.main(['-hl', 'row[0]*2'])
        self.assertWasStreamed('10\n6\n')

    def test_version(self):
        puffin.main(['--version'])
        self.sout.seek(0)
        streamed = self.sout.read()
        self.assertTrue(re.match('\d+\.\d+\.\d+$', streamed))
