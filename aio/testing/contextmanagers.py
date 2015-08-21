import sys
import contextlib
import asyncio


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


class redirect_stderr:
    """Context manager for temporarily redirecting stderr to another file

        # How to send stderr to stdout
        with redirect_stderr(sys.stdout):
            import sys
            sys.stderr.write("EEK!")
    """

    def __init__(self, new_target):
        self._new_target = new_target
        # We use a list of old targets to make this CM re-entrant
        self._old_targets = []

    def __enter__(self):
        self._old_targets.append(sys.stderr)
        sys.stderr = self._new_target
        return self._new_target

    def __exit__(self, exctype, excinst, exctb):
        sys.stderr = self._old_targets.pop()


class redirect_all:
    """Context manager for temporarily redirecting stderr to another file

        # How to capture stdout and sterr
        import io
        with io.StringIO() as out, redirect_all(f):
            import sys
            sys.stdout.write("YAY!")
            sys.stderr.write("EEK!")
            result = out.getvalue()

        # How to write stdout and sterr to a file
        with open('output.txt', 'w') as f:
            with redirect_all(f):
                import sys
                sys.stdout.write("YAY!")
                sys.stderr.write("EEK!")
    """

    def __init__(self, new_stdout, new_stderr=None):
        self._new_stdout = new_stdout
        self._new_stderr = new_stderr or new_stdout
        # We use a list of old targets to make this CM re-entrant
        self._old_stdout = []
        self._old_stderr = []

    def __enter__(self):
        self._old_stdout.append(sys.stdout)
        self._old_stderr.append(sys.stderr)
        sys.stderr = self._new_stderr
        sys.stdout = self._new_stdout
        return self._new_stdout, self._new_stderr

    def __exit__(self, exctype, excinst, exctb):
        sys.stdout = self._old_stdout.pop()
        sys.stderr = self._old_stderr.pop()
