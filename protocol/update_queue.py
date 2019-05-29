import queue
from direct.interval.IntervalGlobal import Sequence, Func


q = queue.Queue()


started = False


def start():
    """
    If resolution hasn't started, start it
    Don't try to start resolution multiple times.
    This way, if we get an update while resolving it will wait for the previous update to finish
    """
    if not started:
        do_next()


def do_later(func):
    q.put(func)


def do_next():
    try:
        # Call the next function in the queue, get its return value
        val = q.get_nowait()()
        if isinstance(val, Sequence):
            val.append(Func(do_next))
            val.start()
        else:
            do_next()  # TODO: let's not stack overflow ourselves
    except queue.Empty:
        started = False
