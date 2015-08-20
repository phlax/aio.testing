import io
import unittest

import asyncio
import os


ROOT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../'))
#sys.path.insert(0, ROOT_PATH)
#assert False, sys.path
#assert False, sys.path

from aio.testing.contextmanagers import redirect_stderr, redirect_all
from aio.testing import run_until_complete, run_forever, current_loop


class AioTestingContextmanagersTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parent_loop = asyncio.get_event_loop()

    @run_until_complete
    def test_run_until_complete(self):
        self.assertEqual(self.test_run_until_complete.__name__,
                         'test_run_until_complete')
        self.assertNotEqual(asyncio.get_event_loop(),
                            AioTestingContextmanagersTestCase.parent_loop)

    @run_until_complete(loop=current_loop)
    def test_run_until_complete_current_loop(self):
        self.assertEqual(self.test_run_until_complete_current_loop.__name__,
                         'test_run_until_complete_current_loop')
        self.assertEqual(asyncio.get_event_loop(),
                         AioTestingContextmanagersTestCase.parent_loop)

    @run_forever
    def test_run_forever(self):
        self.assertEqual(self.test_run_forever.__name__,
                         'test_run_forever')
        self.assertNotEqual(asyncio.get_event_loop(),
                            AioTestingContextmanagersTestCase.parent_loop)

    @run_forever(loop=current_loop)
    def test_run_forever_current_loop(self):
        self.assertEqual(self.test_run_forever.__name__,
                         'test_run_forever')
        self.assertEqual(asyncio.get_event_loop(),
                         AioTestingContextmanagersTestCase.parent_loop)

    @run_forever(timeout=1)
    def test_run_forever_with_args(self):
        self.assertEqual(self.test_run_forever.__name__,
            'test_run_forever')
        self.assertNotEqual(asyncio.get_event_loop(),
                            AioTestingContextmanagersTestCase.parent_loop)

    @run_forever(timeout=1, loop=current_loop)
    def test_run_forever_with_args_current_loop(self):
        self.assertEqual(self.test_run_forever.__name__,
                         'test_run_forever')
        self.assertEqual(asyncio.get_event_loop(),
                         AioTestingContextmanagersTestCase.parent_loop)

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
