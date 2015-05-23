import asyncio


def run_until_complete(f):
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


def run_forever(*la, **kwa):
    """
    Runs an asyncio test with loop.run_forever.

    The test method is expected to return an async test function
    which is run after {timeout}s, the loop is then stopped.
    """

    timeout = kwa.get("timeout", 1)
    sleep = kwa.get("sleep", 0)

    def wrapper(f):

        def wrapped(*la, **kwa):
            parent_loop = asyncio.get_event_loop()
            try:
                loop = asyncio.new_event_loop()
                loop.set_debug(True)
                asyncio.set_event_loop(loop)
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

            finally:
                loop.stop()
                loop.close()
                asyncio.set_event_loop(parent_loop)
        return wrapped

    if len(la) == 1 and callable(la[0]):
        return wrapper(la[0])
    return wrapper

aiotest = run_until_complete
aiofuturetest = run_forever
