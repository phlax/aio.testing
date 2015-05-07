import os
import io
import unittest

from aio.testing.contextmanagers import redirect_stderr, redirect_all


class AioTestingContextmanagersTestCase(unittest.TestCase):

    def test_redirect_stderr(self):
        with io.StringIO() as o, redirect_stderr(o):
            import sys
            sys.stdout.write("YAY!")
            sys.stderr.write("EEK!")
            stderr = o.getvalue()
        self.assertEquals(stderr, "EEK!")

    def test_redirect_all(self):
        with io.StringIO() as o, redirect_all(o):
            import sys
            sys.stdout.write("YAY!")
            sys.stderr.write("EEK!")
            stdall = o.getvalue()
        self.assertEquals(stdall, "YAY!EEK!")

    def test_redirect_all_separate(self):
        with io.StringIO() as o, io.StringIO() as e, redirect_all(o, e):
            import sys
            sys.stdout.write("YAY!")
            sys.stderr.write("EEK!")
            stdout = o.getvalue()
            stderr = e.getvalue()
        self.assertEquals(stdout, "YAY!")
        self.assertEquals(stderr, "EEK!")
