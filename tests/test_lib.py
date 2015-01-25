from puf import cli_lib as puflib
import unittest
from cStringIO import StringIO


class TestInterpret(unittest.TestCase):
    def test_intrepret(self):
        self.assertEqual(puflib.interpret_segment('5'), 5)
        self.assertEqual(puflib.interpret_segment('5.5'), 5.5)
        self.assertEqual(puflib.interpret_segment('a string'), 'a string')


class TestParsing(unittest.TestCase):
    def test_parse_lines(self):
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
        self.assertEqual(puflib.safe_evaluate('math.ceil(3.3)', {}, {}), 4)
        self.assertRaises(NameError, puflib.safe_evaluate, 'invalid_object.foo', {}, {})


class TestDisplay(unittest.TestCase):
    def test_display_string(self):
        stream = StringIO()
        puflib.display('hello', stream)
        stream.seek(0)
        self.assertEqual(stream.read(), 'hello\n')

    def test_display_none(self):
        stream = StringIO()
        puflib.display(None, stream)
        stream.seek(0)
        self.assertEqual(stream.read(), '')

    def test_display_iterable(self):
        stream = StringIO()
        puflib.display([1, None, 2, 'None', 3], stream)
        stream.seek(0)
        self.assertEqual(stream.read(), '1\n2\nNone\n3\n')

    def test_display_mapping(self):
        stream = StringIO()
        puflib.display({'a': 5, 'b': 3, 'c': None, 'd': 'None'}, stream)
        stream.seek(0)
        self.assertEqual(stream.read(), 'a=5\nb=3\nd=None\n')

    def test_display_number(self):
        stream = StringIO()
        puflib.display(5, stream)
        stream.seek(0)
        self.assertEqual(stream.read(), '5\n')
