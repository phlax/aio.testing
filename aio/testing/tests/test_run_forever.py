import unittest

import asyncio
import os

from aio.testing import run_forever
from aio.testing.contextmanagers import current_loop


ROOT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 os.path.join('..' * 3)))


class AioTestingRunForeverTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parent_loop = asyncio.get_event_loop()

    @run_forever
    def test_run_forever(self):
        self.assertEqual(
            self.test_run_forever.__name__,
            'test_run_forever')
        self.assertNotEqual(
            asyncio.get_event_loop(),
            AioTestingRunForeverTestCase.parent_loop)

    @run_forever(loop=current_loop)
    def test_run_forever_current_loop(self):
        self.assertEqual(
            self.test_run_forever.__name__,
            'test_run_forever')
        self.assertEqual(
            asyncio.get_event_loop(),
            AioTestingRunForeverTestCase.parent_loop)

    @run_forever(timeout=1)
    def test_run_forever_with_args(self):
        self.assertEqual(
            self.test_run_forever.__name__,
            'test_run_forever')
        self.assertNotEqual(
            asyncio.get_event_loop(),
            AioTestingRunForeverTestCase.parent_loop)

    @run_forever(timeout=1, loop=current_loop)
    def test_run_forever_with_args_current_loop(self):
        self.assertEqual(
            self.test_run_forever.__name__,
            'test_run_forever')
        self.assertEqual(
            asyncio.get_event_loop(),
            AioTestingRunForeverTestCase.parent_loop)


if __name__ == '__main__':
    import unittest
    unittest.main()
