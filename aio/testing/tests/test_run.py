import unittest

import asyncio
import os

from aio.testing import run_until_complete
from aio.testing.contextmanagers import current_loop


ROOT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 os.path.join('..' * 3)))


class AioTestingRunUntilCompleteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parent_loop = asyncio.get_event_loop()

    @run_until_complete
    def test_run_until_complete(self):
        self.assertEqual(self.test_run_until_complete.__name__,
                         'test_run_until_complete')
        self.assertNotEqual(asyncio.get_event_loop(),
                            AioTestingRunUntilCompleteTestCase.parent_loop)

    @run_until_complete(loop=current_loop)
    def test_run_until_complete_current_loop(self):
        self.assertEqual(self.test_run_until_complete_current_loop.__name__,
                         'test_run_until_complete_current_loop')
        self.assertEqual(asyncio.get_event_loop(),
                         AioTestingRunUntilCompleteTestCase.parent_loop)


if __name__ == '__main__':
    import unittest
    unittest.main()
