import io
import unittest

import os

from aio.testing.contextmanagers import redirect_stderr, redirect_all


ROOT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 os.path.join('..' * 3)))


class AioTestingContextmanagersTestCase(unittest.TestCase):

    def test_redirect_stderr(self):
        with io.StringIO() as o, redirect_stderr(o):
            import sys
            sys.stdout.write("YAY!")
            sys.stderr.write("EEK!")
            stderr = o.getvalue()
        self.assertEqual(stderr, "EEK!")

    def test_redirect_all(self):
        with io.StringIO() as o, redirect_all(o):
            import sys
            sys.stdout.write("YAY!")
            sys.stderr.write("EEK!")
            stdall = o.getvalue()
        self.assertEqual(stdall, "YAY!EEK!")

    def test_redirect_all_separate(self):
        with io.StringIO() as o, io.StringIO() as e, redirect_all(o, e):
            import sys
            sys.stdout.write("YAY!")
            sys.stderr.write("EEK!")
            stdout = o.getvalue()
            stderr = e.getvalue()
        self.assertEqual(stdout, "YAY!")
        self.assertEqual(stderr, "EEK!")


if __name__ == '__main__':
    import unittest
    unittest.main()
