import os
import errno
import signal
from functools import wraps
import psutil
import time


def func_timeout(seconds, error_message=os.strerror(errno.ETIME)):
    """
    A decorator to enforce a timeout on the execution of a function.
    Raises a `TimeoutError` if the decorated function does not 
    complete execution within the specified number of seconds.

    Args:
        seconds (int): The maximum number of seconds the function is allowed to run.
        error_message (str, optional): The error message to include in the
            `TimeoutError`. Defaults to the system's error message for `ETIME`.

    Example:
        @func_timeout(5, "Function execution exceeded the timeout limit")
        def long_running_function():
            time.sleep(10)

        # TimeoutError is raised after 5 seconds.
        long_running_function()
    """
    def decorator(func):
        def _handler(signum, frame):
            raise TimeoutError(error_message)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Set the signal handler and the alarm
            signal.signal(signal.SIGALRM, _handler)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)  # Disable the alarm
            return result
        return wrapper
    return decorator


def method_timeout(func):
    """
    A decorator to enforce a timeout on methods of a class. The timeout duration
    is determined by the `timeout_timer` attribute of the class instance.

    Usage:
        - The class using this decorator must have an attribute `timeout_timer`
          that specifies the timeout duration in seconds.
        - Apply this decorator to methods of the class to enforce the timeout.
    """
    def _handler(signum, frame):
        raise TimeoutError("Timer expired")

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Set the signal handler and the alarm
        signal.signal(signal.SIGALRM, _handler)
        # Timeout time is the value of the object's timeout_time attr
        signal.alarm(self.timeout_timer)
        try:
            func(self, *args, **kwargs)
        finally:
            signal.alarm(0)  # Disable the alarm

    return wrapper


def track(func):
    """
    A decorator that tracks the memory usage and execution time of a function.

    This decorator measures the memory usage of the current process before and
    after the function execution, as well as the time taken to execute the function.

    Args:
        func (callable): The function to be wrapped and tracked.

    Returns:
        callable: The wrapped function with tracking functionality.
    """
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss
        start = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start
        mem_after = process.memory_info().rss
        print(f"{func.__name__}: "
              f"mem before: {mem_before}, "
              f"after: {mem_after}, "
              f"consumed: {mem_after - mem_before}; "
              f"exec time: {elapsed_time}")

        return result
    return wrapper
