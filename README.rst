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

aio.testing provides a decorator for running asyncio-based - @aiotest


.. code:: python

	  import unittest
	  import asyncio

	  from aio.testing import aiotest


	  class MyTestCase(unittest.TestCase):

	      @aiotest
	      def test_example(self):
	          yield from asyncio.sleep(2)
		  self.assertTrue(True)
