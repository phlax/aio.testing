__version__ = "0.0.1"
import asyncio


def aiotest(f):
    """
    Runs an asyncio test with loop.run_until_complete.
    """

    def wrapper(*args, **kwargs):
        try:
            parent_loop = asyncio.get_event_loop()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            coro = asyncio.coroutine(f)
            future = coro(*args, **kwargs)
            loop.run_until_complete(
                asyncio.async(future, loop=loop))
        finally:
            loop.close()
            asyncio.set_event_loop(parent_loop)
    return wrapper


def aiofuturetest(*la, **kwa):
    """
    Runs an asyncio test with loop.run_forever.

    The test method is expected to return an async test function
    which is run after {timeout}s, the loop is then stopped.
    """

    timeout = kwa.get("timeout", 5)
    sleep = kwa.get("sleep", 0)

    def wrapper(f):

        def wrapped(*la, **kwa):
            parent_loop = asyncio.get_event_loop()
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                coro = asyncio.coroutine(f)
                future = coro(*la, **kwa)

                class Handler:
                    exception = None

                handler = Handler()

                def run_test(f):

                    @asyncio.coroutine
                    def wrapper():
                        try:
                            yield from f()
                        except Exception as e:
                            handler.exception = e
                        finally:
                            if sleep:
                                yield from asyncio.sleep(sleep)
                            loop.stop()
                            loop.close()
                    asyncio.async(wrapper())

                def on_setup(res):
                    try:
                        loop.call_later(
                            timeout, run_test, res.result())
                    except Exception as e:
                        handler.exception = e
                        loop.stop()
                        loop.close()

                task = asyncio.async(future)
                task.add_done_callback(on_setup)
                loop.run_forever()

                if handler.exception:
                    raise handler.exception
            finally:
                loop.stop()
                loop.close()
                asyncio.set_event_loop(parent_loop)
        return wrapped

    if len(la) == 1 and callable(la[0]):
        return wrapper(la[0])
    return wrapper
