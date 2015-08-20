import asyncio
from aio.testing.contextmanagers import redirect_stderr, redirect_all
(redirect_stderr, redirect_all)

import contextlib
import functools


@contextlib.contextmanager
def current_loop():
    """A context manager which simply yields the current event loop."""
    yield asyncio.get_event_loop()


class child_loop:
    """
    A context manager to create a new event loop,
    restoring the original loop on exit.
    """
    def __init__(self):
        self._parent_loop = None
        self._child_loop = None

    def __enter__(self):
        self._parent_loop = asyncio.get_event_loop()
        self._child_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._child_loop)
        return self._child_loop

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._child_loop.stop()
        self._child_loop.close()
        asyncio.set_event_loop(self._parent_loop)


def run_until_complete(*la, **kwa):
    """
    Runs an asyncio test with loop.run_until_complete.
    """
    loop_context = kwa.get("loop", child_loop)
    def wrapper(f):
        def wrapped(*args, **kwargs):
            with loop_context() as loop:
                coro = asyncio.coroutine(f)
                future = coro(*args, **kwargs)
                loop.run_until_complete(
                    asyncio.async(future, loop=loop))

        functools.update_wrapper(wrapped, f)
        return wrapped

    if len(la) == 1 and callable(la[0]):
        f = la[0]
        w = wrapper(f)
        functools.update_wrapper(w, f)
        return w
    return wrapper


def run_forever(*la, **kwa):
    """
    Runs an asyncio test with loop.run_forever.

    The test method is expected to return an async test function
    which is run after {timeout}s, the loop is then stopped.
    """

    timeout = kwa.get("timeout", 1)
    sleep = kwa.get("sleep", 0)
    loop_context = kwa.get("loop", child_loop)

    def wrapper(f):

        def wrapped(*la, **kwa):
            with loop_context() as loop:
                coro = asyncio.coroutine(f)
                future = coro(*la, **kwa)

                class Handler:
                    exception = None
                    called = False

                handler = Handler()

                def run_test_callback(f):
                    if not callable(f):
                        loop.stop()
                        handler.called = True
                        return

                    @asyncio.coroutine
                    def wrapper(cb):
                        if not asyncio.iscoroutinefunction(cb):
                            cb = asyncio.coroutine(cb)
                        try:
                            yield from cb()
                            handler.called = True
                        except Exception as e:
                            handler.exception = e
                        finally:
                            if sleep:
                                yield from asyncio.sleep(sleep)
                            loop.stop()
                    asyncio.async(wrapper(f))

                def on_setup(res):
                    try:
                        loop.call_later(
                            timeout, run_test_callback, res.result())
                    except Exception as e:
                        handler.exception = e
                        loop.stop()

                task = asyncio.async(future)
                task.add_done_callback(on_setup)

                def exception_handler(loop, context):
                    handler.exception = context['exception']

                loop.set_exception_handler(exception_handler)
                loop.run_forever()

                if not handler.exception and not handler.called:
                    handler.exception = Exception(
                        "Loop already stopped: test failed to run")

                if handler.exception:
                    raise handler.exception

        functools.update_wrapper(wrapped, f)
        return wrapped

    if len(la) == 1 and callable(la[0]):
        f = la[0]
        w = wrapper(f)
        functools.update_wrapper(w, f)
        return w
    return wrapper

aiotest = run_until_complete
aiofuturetest = run_forever
