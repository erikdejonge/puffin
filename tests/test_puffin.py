import puffin
import unittest
from tests import StreamCaptureTest
import re
from tempfile import NamedTemporaryFile

class TestMain(StreamCaptureTest):
    def test_main(self):
        puffin.main(['range(3)'])
        self.assertWasStreamed('0\n1\n2\n')

    def test_main_initial(self):
        self.assertRaises(NameError, puffin.main, ['fake_object'])
        puffin.main(['-b', 'fake_object=5', 'fake_object*2'])
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

    def test_passed_file(self):
        t = NamedTemporaryFile()
        t.write('bye\n')
        t.flush()
        puffin.main(['-l', 'line.replace("bye", "hi")', t.name])
        self.assertWasStreamed('hi\n')

    def test_passed_file_twice(self):
        t = NamedTemporaryFile()
        t.write('bye\n')
        t.flush()
        puffin.main(['-l', 'line.replace("bye", "hi")', t.name, t.name])
        self.assertWasStreamed('hi\nhi\n')
