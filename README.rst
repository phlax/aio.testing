aio.testing
===========

Test utils for the [aio](https://github.com/phlax/aio) asyncio framework

Build status
------------
[![Build Status](https://travis-ci.org/phlax/aio.testing.svg?branch=master)](https://travis-ci.org/phlax/aio.testing)


Installation
------------
Install with:

.. code:: bash

	  pip install aio.testing


@aiotest decorator
------------------

aio.testing provides a method decorator for running asyncio-based tests

.. code:: python

	  import unittest
	  import asyncio

	  from aio.testing import aiotest


	  class MyTestCase(unittest.TestCase):

	      @aiotest
	      def test_example(self):
	          yield from asyncio.sleep(2)
		  self.assertTrue(True)

		  
Prior to the test running asyncio.get_new_loop() is called and set using asyncio.set_event_loop().

On completion of the test asyncio.set_event_loop() is again called with the original event loop.


@aiofuturetest decorator
------------------------

If your code needs to test long-running tasks, you can use the @aiofuturetest decorator

Any (async) setup required can be done in the body of the test function which returns a test callback

The callback returned should be a coroutine.

.. code:: python

	  import unittest
	  import asyncio

	  from aio.testing import aiofuturetest


	  class MyFutureTestCase(unittest.TestCase):

	      @aiofuturetest
	      def test_example(self):
	          yield from asyncio.sleep(2)

		  @asyncio.coroutine
		  def callback_test(self):
		      yield from asyncio.sleep(2)		  
		      self.asserTrue(True)

		  # this function is called 5 seconds after being returned		      
		  return callback_test

After the test_example function returns, the decorator waits for 5 seconds and then runs the tests in the callback_test function

As with aiotest, the test is run in a separate loop.

		  
@aiofuturetest decorator with timeout
-------------------------------------	  

You can specify how many seconds to wait *before* running the callback tests by setting the timeout value


.. code:: python

	  import unittest
	  import asyncio

	  from aio.testing import aiofuturetest


	  class MyFutureTestCase(unittest.TestCase):

	      @aiofuturetest(timeout=10)
	      def test_example(self):
	          yield from asyncio.sleep(2)

		  @asyncio.coroutine
		  def callback_test(self):
		      yield from asyncio.sleep(2)		  
		      self.asserTrue(True)

		  # this function is called 10 seconds after being returned		      
		  return callback_test


@aiofuturetest decorator with sleep
-------------------------------------	  

Sometimes a test needs to wait for some time after services have been stopped and the test loop has been destroyed.

You can specify how many seconds to wait *after* running the callback tests by setting the sleep value


.. code:: python

	  import unittest
	  import asyncio

	  from aio.testing import aiofuturetest


	  class MyFutureTestCase(unittest.TestCase):

	      @aiofuturetest(sleep=10)
	      def test_example(self):
	          yield from asyncio.sleep(2)

		  @asyncio.coroutine
		  def callback_test(self):
		      yield from asyncio.sleep(2)		  
		      self.asserTrue(True)

		  return callback_test
		  
