import unittest
from cStringIO import StringIO
import sys


class StreamCaptureTest(unittest.TestCase):
    def assertWasStreamed(self, s):
        self.sout.seek(0)
        self.assertEqual(self.sout.read(), s)

    def setUp(self):
        self._stdout = sys.stdout
        self._stdin = sys.stdin
        self.sout = StringIO()
        self.sin = StringIO()
        sys.stdout = self.sout
        sys.stdin = self.sin

    def tearDown(self):
        sys.stdout = self._stdout
        sys.stdin = self._stdin
