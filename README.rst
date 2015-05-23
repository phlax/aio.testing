aio.testing
===========

Test utils for the aio_ asyncio framework

.. _aio: https://github.com/phlax/aio


Build status
------------

.. image:: https://travis-ci.org/phlax/aio.testing.svg?branch=master
	       :target: https://travis-ci.org/phlax/aio.testing


Installation
------------
Install with:

.. code:: bash

	  pip install aio.testing


@aio.testing.run_until_complete decorator
-----------------------------------------

aio.testing provides a method decorator for running asyncio-based tests

.. code:: python

	  import unittest
	  import asyncio

	  import aio.testing


	  class MyTestCase(unittest.TestCase):

	      @aio.testing.run_until_complete
	      def test_example():
	          yield from asyncio.sleep(2)
		  self.assertTrue(True)

		  
Prior to the test running asyncio.get_new_loop() is called and set using asyncio.set_event_loop().

On completion of the test asyncio.set_event_loop() is again called with the original event loop.


@aio.testing.run_forever decorator
----------------------------------

If your code needs to test long-running tasks, you can use the @aio.testing.run_forever decorator.

The @aio.testing.run_forever decorator uses loop.run_forever to run the test.

Any setup required can be done in the body of the test function which can optionally return a test callback

The callback is wrapped in a coroutine, and called after 1 second

.. code:: python

	  import unittest
	  import asyncio

	  import aio.testing


	  class MyFutureTestCase(unittest.TestCase):

	      @aio.testing.run_forever
	      def test_example():
	          yield from asyncio.sleep(2)

		  def callback_test(self):
		      yield from asyncio.sleep(2)		  
		      self.assertTrue(True)

		  # this function is called 1 second after being returned		      
		  return callback_test


As with aio.testing.run_until_complete, the test is run in a separate loop.

		  
@aio.testing.run_forever decorator with timeout
-----------------------------------------------

You can specify how many seconds to wait *before* running the callback tests by setting the timeout value


.. code:: python

	  import unittest
	  import asyncio

	  from aio.testing import aio.testing.run_forever


	  class MyFutureTestCase(unittest.TestCase):

	      @aio.testing.run_forever(timeout=10)
	      def test_example():
	          yield from asyncio.sleep(2)

		  def callback_test(self):
		      yield from asyncio.sleep(2)		  
		      self.assertTrue(True)

		  # this function is called 10 seconds after being returned		      
		  return callback_test


@aio.testing.run_forever decorator with sleep
---------------------------------------------

Sometimes a test needs to wait for some time after services have been stopped and the test loop has been destroyed.

You can specify how many seconds to wait *after* running the callback tests by setting the sleep value


.. code:: python

	  import unittest
	  import asyncio

	  from aio.testing import aio.testing.run_forever


	  class MyFutureTestCase(unittest.TestCase):

	      @aio.testing.run_forever(sleep=10)
	      def test_example():
	          yield from asyncio.sleep(2)

		  def callback_test(self):
		      yield from asyncio.sleep(2)		  
		      self.assertTrue(True)

		  return callback_test
		  
