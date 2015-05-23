aio.testing usage
=================


Aio testing provides 2 decorators for running asyncio tests

- *aiotest*:
 - creates a test loop
 - calls the test with loop.run_until_done
- *aiofuturetest*:
  
  - creates a test loop
  - calls test using loop.run_forever
  - waits for number of seconds specified in "timeout"
  - if test returns a coroutine, calls the coroutine
  - waits for number of seconds specified in "sleep"

aiotest
-------

Lets create a test

  >>> import asyncio
  >>> from aio.testing import aiotest

  >>> @aiotest
  ... def run_test(parent_loop):
  ...     yield from asyncio.sleep(1)
  ... 
  ...     print(asyncio.get_event_loop() == parent_loop)

And lets check that the test loop is not the same as the current one

  >>> loop_before_test = asyncio.get_event_loop()
  >>> run_test(loop_before_test)
  False

After the test has run we have the original event loop back

  >>> asyncio.get_event_loop() == loop_before_test
  True

We can raise an error in the test

  >>> @aiotest
  ... def run_test():
  ...     assert(True == False)

  >>> try:
  ...     run_test()
  ... except AssertionError as e:
  ...     print(repr(e))
  AssertionError()

  
aiofuturetest
-------------

Lets create a future test

  >>> import asyncio
  >>> from aio.testing import aiofuturetest

  >>> @aiofuturetest
  ... def run_test(parent_loop):
  ...     yield from asyncio.sleep(1)
  ... 
  ...     print(asyncio.get_event_loop() == parent_loop)

Just like with aiotest, the test is run in a separate loop

  >>> loop_before_test = asyncio.get_event_loop()  
  >>> run_test(loop_before_test)
  False

And again, after the test has run we have the original event loop back

  >>> asyncio.get_event_loop() == loop_before_test
  True
  
If the test returns a coroutine, the coroutine is called 1 second later.

The test_callback runs in the same loop as the test
  
  >>> @aiofuturetest
  ... def run_test():
  ...     test_loop = asyncio.get_event_loop()
  ... 
  ...     @asyncio.coroutine
  ...     def test_callback():
  ...         print(
  ...             asyncio.get_event_loop() == test_loop)
  ... 
  ...     return test_callback
  
  >>> run_test()
  True

We can raise an error in the test

  >>> @aiofuturetest
  ... def run_test():
  ...     assert(True == False)

  >>> try:
  ...     run_test()
  ... except AssertionError as e:
  ...     print(repr(e))
  AssertionError()

And we can raise an error in the test callback

  >>> @aiofuturetest
  ... def run_test():
  ... 
  ...     @asyncio.coroutine
  ...     def test_callback():
  ...         assert(True == False)
  ... 
  ...     return test_callback
  
  >>> try:
  ...     run_test()
  ... except AssertionError as e:
  ...     print(repr(e))
  AssertionError()

By default the test_callback is called 1 second after being returned

  >>> import time

  >>> @aiofuturetest
  ... def run_test():
  ...     test_run_at = int(time.time())
  ... 
  ...     @asyncio.coroutine
  ...     def test_callback():
  ...         callback_run_at = int(time.time())
  ...         print("callback called %s second(s) after test" % (
  ...             callback_run_at - test_run_at))
  ... 
  ...     return test_callback
  
  >>> run_test()
  callback called 1 second(s) after test

You can set the amount of time to wait before calling the test_callback by setting the "timeout" argument in the decorator

  >>> import time

  >>> @aiofuturetest(timeout=3)
  ... def run_test():
  ...     test_run_at = int(time.time())
  ... 
  ...     @asyncio.coroutine
  ...     def test_callback():
  ...         callback_run_at = int(time.time())
  ... 
  ...         print("callback called %s second(s) after test" % (
  ...             callback_run_at - test_run_at))
  ... 
  ...     return test_callback
  
  >>> run_test()
  callback called 3 second(s) after test
  
You can also set the amount of time to wait after the test has completely finished, including the test_callback, by setting the "sleep" argument on the decorator

  >>> @aiofuturetest(sleep=3)
  ... def run_test(test_time):
  ... 
  ...     @asyncio.coroutine
  ...     def test_callback():
  ...         test_time['completed_at'] = int(time.time())
  ... 
  ...     return test_callback

  >>> test_time = {}
  >>> run_test(test_time)
  >>> waiting_time = int(time.time()) - test_time['completed_at']
  >>> print("test waited %s second(s) after completing" % waiting_time)
  test waited 3 second(s) after completing
