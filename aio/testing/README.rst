aio.testing usage
=================


aio.testing.run_until_complete
------------------------------

Lets create a test

>>> import asyncio
>>> import aio.testing

>>> @aio.testing.run_until_complete
... def run_test(parent_loop):
...     yield from asyncio.sleep(1)
... 
...     print(asyncio.get_event_loop() != parent_loop)

And lets check that the test loop is not the same as the current one

>>> loop_before_test = asyncio.get_event_loop()
>>> run_test(loop_before_test)
True

After the test has run we have the original event loop back

>>> asyncio.get_event_loop() == loop_before_test
True

We can raise an error in the test

>>> @aio.testing.run_until_complete
... def run_test():
...     assert(True == False)

>>> try:
...     run_test()
... except Exception as e:
...     print(repr(e))
AssertionError()

  
aio.testing.run_forever
-----------------------

Lets create a future test

>>> import asyncio

>>> @aio.testing.run_forever
... def run_test(parent_loop):
...     yield from asyncio.sleep(1)
... 
...     print(asyncio.get_event_loop() != parent_loop)

Just like with aio.testing.run_until_complete, the test is run in a separate loop

>>> loop_before_test = asyncio.get_event_loop()  
>>> run_test(loop_before_test)
True

And again, after the test has run we have the original event loop back

>>> asyncio.get_event_loop() == loop_before_test
True
  
If the test returns a callable, its called 1 second later.

The test_callback runs in the same loop as the test
  
>>> @aio.testing.run_forever
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

The test_callback is always wrapped in asyncio.coroutine if its not one already

>>> @aio.testing.run_forever
... def run_test():
... 
...     def test_callback():
...         yield from asyncio.sleep(1)
...         print("test_callback is always wrapped in a coroutine!")
... 
...     return test_callback
  
>>> run_test()
test_callback is always wrapped in a coroutine!


We can raise an error in the test

>>> @aio.testing.run_forever
... def run_test():
...     assert(True == False)

>>> try:
...     run_test()
... except Exception as e:
...     print(repr(e))
AssertionError()

And we can raise an error in the test callback

>>> @aio.testing.run_forever
... def run_test():
... 
...     def test_callback():
...         assert(True == False)
... 
...     return test_callback
  
>>> try:
...     run_test()
... except Exception as e:
...     print(repr(e))
AssertionError()

By default the test_callback is called 1 second after being returned

>>> import time

>>> @aio.testing.run_forever
... def run_test():
...     test_run_at = int(time.time())
... 
...     return lambda: (
...         print("callback called %s second(s) after test" % (
...             int(time.time()) - test_run_at)))
  
>>> run_test()
callback called 1 second(s) after test

You can set the amount of time to wait before calling the test_callback by setting the "timeout" argument in the decorator

>>> import time

>>> @aio.testing.run_forever(timeout=3)
... def run_test():
...     test_run_at = int(time.time())
... 
...     return lambda: print(
...         "callback called %s second(s) after test" % (
...             int(time.time()) - test_run_at))
  
>>> run_test()
callback called 3 second(s) after test
  
You can also set the amount of time to wait after the test has completely finished, by setting the "sleep" argument on the decorator

>>> @aio.testing.run_forever(sleep=3)
... def run_test(test_time):
...     return lambda: (
...         test_time.__setitem__('completed_at', int(time.time())))

>>> test_time = {}
>>> run_test(test_time)
  
>>> print("test waited %s second(s) after completing" % (
...     int(time.time()) - test_time['completed_at']))
test waited 3 second(s) after completing
